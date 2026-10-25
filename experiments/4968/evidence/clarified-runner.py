"""No-spend preparation and bounded subscription-only prompt portability diagnostic."""
import argparse
import hashlib
import importlib
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PLAN_PATH = HERE / "plan.json"
PLAN = json.loads(PLAN_PATH.read_text())
CORE_FILES = ("pilot_runner.py", "fixture_server.py", "fixture.json", "cases.json", "operations.json", "evidence.py")
INPUT_FILES = ("prompt.txt", "command.json", "mcp.json", "settings.json", "state.json", "rpc.jsonl")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def source_hashes(catalog):
    paths = [HERE / "run.py", PLAN_PATH]
    paths += [ROOT / "plugins/vc/alludium/agent-templates" / (agent + ".yaml") for agent in PLAN["agents"]]
    paths += [catalog / name for name in CORE_FILES]
    return {str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else "catalog/" + path.name: digest(path) for path in paths}


def verify_source_revision():
    for agent in PLAN["agents"]:
        relative = "plugins/vc/alludium/agent-templates/" + agent + ".yaml"
        pinned = subprocess.run(["git", "show", PLAN["packs_revision"] + ":" + relative], cwd=ROOT, capture_output=True, check=True).stdout
        if pinned != (ROOT / relative).read_bytes():
            raise ValueError("Pack template differs from declared revision: " + agent)


def input_hashes(directory):
    return {name: digest(directory / name) for name in INPUT_FILES}


def render(template, variables):
    text = template["prompt"]["template"]
    for key, value in variables.items():
        text = text.replace("{{" + key + "}}", value)
    if re.search(r"\{\{.*?\}\}", text):
        raise ValueError("Unresolved template variable")
    return text


def assert_frozen(preflight, catalog):
    if preflight["source_hashes"] != source_hashes(catalog):
        raise ValueError("Frozen source changed; refuse continuation")


def prepare(out, catalog, core, prior_ledgers=()):
    verify_source_revision()
    prior_ledgers = [path.resolve() for path in prior_ledgers]
    if len(set(prior_ledgers)) != len(prior_ledgers):
        raise ValueError("Duplicate predecessor ledger")
    prior_count = sum(len(path.read_text().splitlines()) for path in prior_ledgers)
    limits = PLAN["ceilings"]
    if prior_count + limits["attempts"] != limits.get("cumulative_attempts", limits["attempts"]):
        raise ValueError("Predecessor attempts do not match the frozen cumulative plan")
    if out.exists():
        raise ValueError("Preflight output already exists")
    out.mkdir(parents=True)
    env = core.clean_env()
    auth = {client: core.attest(client, env) for client in PLAN["clients"]}
    versions = {client: subprocess.run([client, "--version"], capture_output=True, text=True, env=env, timeout=15, check=True).stdout.strip() for client in PLAN["clients"]}
    cells = []
    for agent, cases in PLAN["agents"].items():
        template = yaml.safe_load((ROOT / "plugins/vc/alludium/agent-templates" / (agent + ".yaml")).read_text())
        prompt_text = render(template, PLAN["variables"])
        for case in cases:
            for client, model in PLAN["clients"].items():
                for guidance in PLAN["guidance"]:
                    cell_id = f"{agent}-{case}-{client}-{guidance}"
                    directory = out / cell_id
                    directory.mkdir()
                    command = core.configure(directory, client, model, PLAN["catalog_arm"], case)
                    fixture_scope = "Trusted synthetic context: incoming message is from a human, humanAuthorization=true; current Deal=deal-a; workspace binding=vc_deal_pipeline. Only the listed synthetic operations exist. Native operation names and skills mentioned below are not installed; use an available equivalent only when its schema and purpose fit, otherwise report the limitation. Do not invent a native call or claim native persistence."
                    prompt = core.BASE + "\n\n" + fixture_scope + "\n\n"
                    if guidance == "packs":
                        prompt += "Current rendered Packs template instructions:\n" + prompt_text + "\n\n"
                    prompt += "User job:\n" + core.CASES[case]["prompt"]
                    if case in PLAN.get("case_clarifications", {}):
                        prompt += "\n" + PLAN["case_clarifications"][case]
                    command[-1] = prompt
                    (directory / "prompt.txt").write_text(prompt)
                    dump(directory / "command.json", command)
                    cells.append({"id": cell_id, "agent": agent, "template_version": template["version"], "guidance": guidance, "case": case, "client": client, "model": model, "input_hashes": input_hashes(directory)})
    if len(cells) != PLAN["ceilings"]["attempts"]:
        raise ValueError("Plan cells differ from cumulative attempt ceiling")
    manifest = {"plan": PLAN, "source_hashes": source_hashes(catalog), "auth": auth, "client_versions": versions, "cells": cells, "provider_calls_in_preflight": 0, "prior_ledgers": {str(path.resolve()): digest(path) for path in prior_ledgers}}
    dump(out / "preflight.json", manifest)
    return manifest


def execute(out, catalog, core, diagnosis=None):
    preflight = json.loads((out / "preflight.json").read_text())
    assert_frozen(preflight, catalog)
    if preflight.get("plan", PLAN) != PLAN:
        raise ValueError("Prepared plan changed")
    for path, expected in preflight.get("prior_ledgers", {}).items():
        if digest(Path(path)) != expected:
            raise ValueError("Predecessor ledger changed")
    for cell in preflight["cells"]:
        directory = out / cell["id"]
        if (directory / "result.json").exists():
            previous = json.loads((directory / "result.json").read_text())
            if previous["returncode"] or previous["stop_reason"]:
                if not diagnosis:
                    raise ValueError("Prior infrastructure failure requires --diagnosis before continuing remaining cells")
                dump(directory / "continuation-diagnosis.json", {"reason": diagnosis, "action": "Continue remaining planned cells; failed cell is retained and not retried"})
            continue
        if (directory / "stdout.jsonl").exists():
            raise ValueError("Interrupted attempt requires diagnosis; no automatic retry")
        assert_frozen(preflight, catalog)
        if input_hashes(directory) != cell["input_hashes"]:
            raise ValueError("Prepared subject input changed")
        env = core.clean_env()
        core.attest(cell["client"], env)
        ceiling = PLAN["ceilings"]
        manifest = {"hashes": preflight["source_hashes"], "client": cell["client"], "arm": cell["guidance"], "case": cell["case"]}
        reservation = core.reserve(out / "ledger.jsonl", directory, manifest, ceiling["attempts"], ceiling["seconds"], ceiling["output_bytes"], list(preflight.get("prior_ledgers", {})), ceiling.get("cumulative_attempts", ceiling["attempts"]))
        code, reason, duration, size = core.run_bounded(json.loads((directory / "command.json").read_text()), directory, env, ceiling["seconds"], ceiling["output_bytes"])
        result = {"cell": cell, "returncode": code, "stop_reason": reason, "duration_seconds": duration, "output_bytes": size, "reservation": reservation, "score": core.summarize(directory, cell["case"], core.CASES[cell["case"]], cell["client"])}
        dump(directory / "result.json", result)
        print(json.dumps({"cell": cell["id"], "returncode": code, "stop_reason": reason, "trace_pass": result["score"]["trace_checks_pass"]}), flush=True)
        if code or reason:
            raise RuntimeError("Stopped after infrastructure failure; diagnose before any continuation")


def main():
    global PLAN_PATH, PLAN
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog-runner", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--plan", type=Path, default=PLAN_PATH)
    parser.add_argument("--prior-ledger", type=Path, action="append", default=[])
    parser.add_argument("--diagnosis", help="Recorded explanation permitting remaining cells after a diagnosed infrastructure failure; does not retry or increase the cap")
    args = parser.parse_args()
    PLAN_PATH = args.plan.resolve()
    PLAN = json.loads(PLAN_PATH.read_text())
    limits = PLAN["ceilings"]
    if not (1 <= limits["attempts"] <= 24 and limits["attempts"] <= limits.get("cumulative_attempts", limits["attempts"]) <= 28 and 1 <= limits["seconds"] <= 120 and 1 <= limits["output_bytes"] <= 2000000 and limits["tool_calls"] == 24):
        raise ValueError("Plan exceeds the bounded experiment envelope")
    if limits.get("cumulative_attempts", limits["attempts"]) != limits["attempts"] and not args.prior_ledger and not args.execute:
        raise ValueError("Follow-up preflight requires the original ledger")
    catalog = args.catalog_runner.resolve()
    sys.path.insert(0, str(catalog))
    core = importlib.import_module("pilot_runner")
    if args.execute:
        execute(args.out.resolve(), catalog, core, args.diagnosis)
    else:
        result = prepare(args.out.resolve(), catalog, core, args.prior_ledger)
        print(json.dumps({"status": "prepared-not-run", "cells": len(result["cells"]), "provider_calls": 0}))


if __name__ == "__main__":
    main()
