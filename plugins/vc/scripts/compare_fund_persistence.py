#!/usr/bin/env python3
"""Fund-persistence comparison for the Deal Pipeline Manager (Platform issue #4449).

Sibling of compare_deal_manager_prompts.py. It answers one question: when a human names a Fund in
the Deal-creation context, does the manager write it to fund_id (and say so honestly), and does it
correctly refuse to write ambiguous, unknown, inactive, absent or merely suggested Funds?

Two or more prompt "arms" (git revisions or working-tree template files) run the same frozen cases
against a simulated `project_data` tool on the Luna subject, through the OpenAI Responses API,
under the same reservation-based spend ledger as the #4308 comparison. Default mode is a no-spend
preflight. Prompt/tool-choice evidence only; not Platform integration or deployed proof.

Loop safety is layered: a spend ceiling, a per-step limit, a per-attempt wall clock, a per-call
timeout, a consecutive-provider-error stop and an overall --max-wall-minutes stop.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import signal
import subprocess
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

import yaml

import compare_deal_manager_prompts as base
from evaluate_deal_manager import DECK, MEMBER, PACK, PROJECT, ROOT, tool_specs_from_names

HERE = Path(__file__).resolve().parent
EVAL_DIR = HERE.parent / "evals" / "4449"
CASES = EVAL_DIR / "cases.yaml"
EXPECTATIONS = EVAL_DIR / "expectations.yaml"
PROJECT_DATA_TOOL = EVAL_DIR / "project-data-tool.json"
TOOL_CONTRACT = HERE / "fixtures" / "deal-manager-tool-contract.json"
TEMPLATE_PATH = f"{PACK}/agent-templates/vc_deal_pipeline_manager.yaml"

GLOBAL_ASSERTIONS = ["allTurnsComplete", "noInvalidToolCalls", "noTaskCreated", "noLifecycleChange", "noOtherMutations"]
HONESTY_MODES = {"saved", "unresolved", "noClaim"}
ARM_NAME = re.compile(r"[a-z0-9][a-z0-9-]*")
# The kickoff permits exactly one Deal mutation: saving the named Fund. Producing the PROJECT_SHARED evidence artifact
# the kickoff itself asks for (creating it, then editing that same artifact) is not a Deal mutation, so artifact writes
# are allowed except edits to the pre-existing deck. Any other project write is forbidden.
PROJECT_DATA_MUTATIONS = {"update_project", "attach_documents", "detach_documents"}
ALLOWED_FIELD_WRITE = "fund_id"
ARTIFACT_EDITS = {"artifact.updateTextArtifact", "artifact.replaceTextRange", "artifact.insertTextAfterLine",
                  "artifact.insertTextBeforeLine"}
FORBIDDEN_TOOL_WRITES = {"project.update", "project.instantiateTemplate"}
INVALID_CALL_ERRORS = {"Invalid JSON arguments", "Unknown tool", "Missing required argument"}
DEFAULT_MAX_WALL_MINUTES = 60

_SAVE_VERBS = r"(?:sav(?:e|ed|es)|assign(?:ed|s)?|record(?:ed|s)?|persist(?:ed|s)?|writ(?:e|ten)|stor(?:e|ed)|set)"
# Claims are past-tense assertions only, so nouns ("Fund records", "active matches"), imperatives ("confirm the Fund")
# and plans ("I will save it") are not read as claims.
_SAVE_PAST = r"(?:saved|assigned|recorded|persisted|written|stored|set (?:to|as))"
SAVE_CLAIM = re.compile(rf"\b{_SAVE_PAST}\b", re.I)
# Words that also present a Fund as settled; the prompt forbids them unless the Fund was saved.
ASSERT_CLAIM = re.compile(rf"\b(?:{_SAVE_PAST}|confirmed|resolved|matched|selected|chosen)\b", re.I)
# Negation, modality or a condition before the verb makes a unit a non-claim ("not saved", "should be recorded",
# "must be identified and confirmed", "please confirm", "once you confirm", "I'll save it").
NEGATION = re.compile(r"(?:\b(?:not|never|no|none|nothing|cannot|unable|without|unless|until|if|whether|once|before|"
                      r"pending|awaiting|yet to be|please|should|would|could|can|may|might|will|must|need|needs|neither|nor|"
                      r"to be)\b|n't|'ll)", re.I)
FUND_NAME = re.compile(r"\b(?:Growth\s+)?Fund\s+(?:\d+|[IVX]+)\b", re.I)
SAVED = re.compile(rf"\bfund\b[^.\n]{{0,80}}\b{_SAVE_VERBS}\b|\b{_SAVE_VERBS}\b[^.\n]{{0,40}}\bfund\b", re.I)
NEGATED_SAVE = re.compile(
    rf"\b(?:not|n't|never|no|none|isn't|hasn't|haven't|wasn't|without|nothing|yet to be)\b[^.\n]{{0,90}}\b{_SAVE_VERBS}\b"
    r"|\bunassigned\b|\bno fund (?:is |has been )?(?:assigned|set|saved|confirmed)\b|\bhas no fund\b", re.I)
UNRESOLVED = re.compile(
    r"\b(?:unresolved|not (?:been )?(?:found|resolved|matched)|couldn'?t (?:be )?(?:find|found|resolve|resolved|match|matched)|"
    r"could not (?:be )?(?:find|found|resolve|resolved|match|matched)|cannot (?:resolve|find|match|verify)|unable to (?:resolve|find|match|verify)|"
    r"no (?:active |matching |exact |selectable )?(?:fund|match|record)|ambiguous|more than one|multiple|"
    r"which (?:fund|one)|please confirm|confirm (?:which|the|that|whether)|inactive|closed|"
    r"not (?:currently )?(?:active|selectable)|(?:doesn'?t|does not) (?:match|exist))\b", re.I)


# ---------------------------------------------------------------- freezing

def parse_arm(spec: str) -> tuple[str, str, str]:
    """NAME=SOURCE or NAME=SOURCE+guard=KEY. SOURCE is a git revision or file:PATH; KEY picks the kickoff guard."""
    name, _, rest = spec.partition("=")
    source, _, guard = rest.partition("+guard=")
    if not ARM_NAME.fullmatch(name) or not source:
        raise SystemExit(f"--arm must look like NAME=REVISION, NAME=file:PATH, optionally +guard=KEY (got {spec!r})")
    return name, source, guard or "current"


def load_arm(name: str, source: str, guard: str = "current") -> dict:
    if source.startswith("file:"):
        path = Path(source[5:]).resolve()
        raw, origin = path.read_text(), {"kind": "file", "path": str(path)}
    else:
        commit = base.resolve_commit(source)
        raw, origin = base.git_show(commit, TEMPLATE_PATH), {"kind": "git", "revision": commit}
    parsed = yaml.safe_load(raw)
    return {"name": name, "raw": raw, "parsed": parsed, "origin": origin, "sha256": base.sha(raw), "guard": guard,
            "version": parsed.get("version"), "promptSha256": base.sha(parsed["prompt"]["template"])}


def freeze(arm_specs: list[str]) -> dict:
    """Resolve every input shared by all arms and record problems before any provider access."""
    cases_text, expectations_text = CASES.read_text(), EXPECTATIONS.read_text()
    cases, expectations = yaml.safe_load(cases_text), yaml.safe_load(expectations_text)
    tool_text, contract_text = PROJECT_DATA_TOOL.read_text(), TOOL_CONTRACT.read_text()
    tool, contract = json.loads(tool_text), json.loads(contract_text)
    problems: list[str] = []
    if expectations.get("global") != GLOBAL_ASSERTIONS:
        problems.append(f"Global assertions must be exactly {GLOBAL_ASSERTIONS}")
    case_ids = [case["id"] for case in cases["cases"]]
    if len(set(case_ids)) != len(case_ids):
        problems.append("Duplicate case IDs")
    if set(case_ids) != set(expectations["cases"]):
        problems.append("Cases and expectations do not cover the same IDs")
    for case in cases["cases"]:
        if case["fundSet"] not in cases["fundSets"]:
            problems.append(f"{case['id']}: unknown fund set {case['fundSet']}")
        if not case.get("turns") or case["turns"][0].get("initialRequest") is None:
            problems.append(f"{case['id']}: the first turn must carry an initialRequest")
        for turn in case.get("turns", []):
            if turn.get("author") != "human" or not (turn.get("initialRequest") or turn.get("text")):
                problems.append(f"{case['id']}: turns must be human with initialRequest or text")
        expect = expectations["cases"].get(case["id"], {})
        write = expect.get("fundWrite")
        if write != "none" and not (isinstance(write, dict) and {"value", "turn"} <= set(write)):
            problems.append(f"{case['id']}: fundWrite must be 'none' or {{value, turn}}")
        if expect.get("honesty") not in HONESTY_MODES:
            problems.append(f"{case['id']}: honesty must be one of {sorted(HONESTY_MODES)}")
    arms = []
    names = set()
    for spec in arm_specs:
        name, source, guard = parse_arm(spec)
        if guard not in cases["guards"]:
            problems.append(f"Arm {name}: unknown guard {guard!r}; choose from {sorted(cases['guards'])}")
        if name in names:
            problems.append(f"Duplicate arm name {name}")
        names.add(name)
        arms.append(load_arm(name, source, guard))
    if len(arms) < 1:
        problems.append("At least one --arm is required")
    if len({(arm["promptSha256"], arm["guard"]) for arm in arms}) < len(arms):
        problems.append("Two arms have identical prompts and guards; nothing to compare")
    variables = {"firmName": cases["firmName"]}
    for arm in arms:
        parsed = arm["parsed"]
        if parsed.get("id") != cases["agentTemplateId"]:
            problems.append(f"Arm {arm['name']}: template id is not {cases['agentTemplateId']}")
        for key in ("capabilityProfile", "capabilityAccess", "skills"):
            if parsed.get(key) != arms[0]["parsed"].get(key):
                problems.append(f"Arm {arm['name']}: template {key} differs from the first arm; only the prompt may change")
        if contract["capabilityBundles"] != parsed["capabilityProfile"]["bundles"]:
            problems.append(f"Arm {arm['name']}: frozen tool contract bundles do not match its capability profile")
        if re.search(r"\{\{\w+\}\}", base.render_prompt(parsed["prompt"]["template"], variables)):
            problems.append(f"Arm {arm['name']}: prompt has an unrendered variable")
    return {"cases": cases, "expectations": expectations, "arms": arms, "problems": problems, "variables": variables,
            "toolNames": [t["name"] for t in contract["tools"]] + ["project_data"], "projectDataTool": tool["toolSpec"],
            "identity": {"casesSha256": base.sha(cases_text), "expectationsSha256": base.sha(expectations_text),
                         "projectDataToolSha256": base.sha(tool_text), "toolContractSha256": base.sha(contract_text),
                         "arms": [{"name": a["name"], "origin": a["origin"], "sha256": a["sha256"], "version": a["version"],
                                   "promptSha256": a["promptSha256"], "guard": a["guard"],
                                   "guardSha256": base.sha(cases["guards"][a["guard"]]["text"]) if a["guard"] in cases["guards"] else None}
                                  for a in arms],
                         "runnerSha256": base.sha(Path(__file__).read_text()),
                         "baseRunnerSha256": base.sha((HERE / "compare_deal_manager_prompts.py").read_text())}}


def plan_attempts(cases: list[dict], arms: list[str], repetitions: int) -> list[dict]:
    """Interleave arms; the order rotates with repetition and case position so no arm is always first."""
    plan = []
    for repetition in range(1, repetitions + 1):
        for index, case in enumerate(cases):
            shift = (repetition + index) % len(arms)
            for arm in arms[shift:] + arms[:shift]:
                plan.append({"index": len(plan) + 1, "case": case["id"], "arm": arm, "repetition": repetition,
                             "folder": f"attempts/{len(plan) + 1:03}-{case['id']}--{arm}--r{repetition}"})
    return plan


# ---------------------------------------------------------------- simulation

class FundSimulator:
    """Synthetic Platform state for one attempt. Persists across the attempt's turns."""

    def __init__(self, cases: dict, case: dict):
        self.cases, self.case = cases, case
        self.funds = [dict(f) for f in cases["fundSets"][case["fundSet"]]]
        self.definitions = cases["fieldDefinitions"]
        fund_def = next(d for d in self.definitions if d["key"] == "fund_id")
        self.selectable = set(fund_def["optionSource"]["selectableStatuses"])
        self.company = cases["company"]
        self.description = case["turns"][0]["initialRequest"]
        self.fields = {"company_name": self.company["name"], "fund_id": None}
        self.deck = {"id": DECK, "filename": "routewise-deck.txt", "kind": "pitch_deck", "readable": True,
                     "content": self.company["deck"]}
        self.turn = 0
        self.fund_attempts: list[dict] = []
        self.state_requests: list[dict] = []
        self.tasks_created: list[dict] = []
        self.created: list[dict] = []

    def project(self) -> dict:
        return {"id": PROJECT, "name": self.company["name"], "state": "screening", "status": "active",
                "description": self.description}

    def option(self, fund: dict) -> dict:
        return {"label": fund["name"], "value": fund["id"], "status": fund["status"],
                "selectable": fund["status"] in self.selectable}

    def matches(self, query: str | None) -> list[dict]:
        if not query:
            return list(self.funds)
        needle = query.strip().lower()
        found = []
        for fund in self.funds:
            hints = " ".join(str(v) for k in ("stage", "sectors", "geographies") for v in
                             (fund.get(k) if isinstance(fund.get(k), list) else [fund.get(k, "")]))
            if needle in fund["id"].lower() or needle in fund["name"].lower() or needle in hints.lower():
                found.append(fund)
        return found

    def project_data(self, args: dict) -> tuple[dict | None, str | None]:
        action, data = args.get("action"), args.get("data") or {}
        if action == "read":
            return {"project": self.project(), "fieldDefinitions": self.definitions,
                    "fieldValues": [{"fieldKey": k, "value": v} for k, v in self.fields.items() if v is not None]}, None
        if action == "list_field_options":
            query = data.get("fieldOptions") or {}
            if query.get("fieldKey") != "fund_id":
                return None, "Field has no option source"
            options = [self.option(f) for f in self.matches(query.get("query"))][: int(query.get("limit") or 10)]
            return {"fieldOptions": {"source": {"path": "vc.funds", "type": "workspaceVariableCollection"},
                                     "options": options, "fieldKey": "fund_id", "totalCount": len(options),
                                     "resolutionState": "resolved"}}, None
        if action == "read_field_option":
            selected = self.fields["fund_id"]
            fund = next((f for f in self.funds if f["id"] == selected), None)
            return ({"fieldOptionRecord": {"fieldKey": "fund_id", "record": fund}}, None) if fund \
                else (None, "No option is currently selected for this field")
        if action == "read_field_value":
            key = (data.get("fieldValue") or {}).get("fieldKey")
            return ({"fieldValue": {"fieldKey": key, "value": self.fields.get(key)}}, None) if key in self.fields \
                else (None, "Unknown field key")
        if action in {"read_project_description", "read_project_instructions"}:
            return {"text": self.description if action == "read_project_description" else ""}, None
        if action == "list_field_definitions":
            return {"fieldDefinitions": self.definitions}, None
        if action == "update_state":
            return self.update_state(data)
        return None, "Action outside the simulated Fund-persistence scope"

    def update_state(self, data: dict) -> tuple[dict | None, str | None]:
        values, state = data.get("fieldValues") or [], data.get("state")
        if state is not None:
            self.state_requests.append({"turn": self.turn, "state": state})
        if not values and state is None:
            return None, "update_state requires fieldValues and/or state"
        known = {d["key"] for d in self.definitions}
        pending, error = {}, None
        for item in values:
            key, value = item.get("fieldKey"), item.get("value")
            attempt = {"turn": self.turn, "fieldKey": key, "value": value, "ok": False, "error": None}
            if key not in known:
                error = f"Unknown field key {key!r}"
            elif key == "fund_id":
                option = next((f for f in self.funds if f["id"] == value), None)
                if option is None:
                    error = f"Field fund_id value {value!r} does not match a record in vc.funds"
                elif option["status"] not in self.selectable:
                    error = f"Field fund_id value {value!r} is not a currently selectable option of vc.funds"
            if key == "fund_id":
                attempt["error"] = error
                self.fund_attempts.append(attempt)
            if error:
                break
            pending[key] = value
        if error:
            return None, error
        for attempt in self.fund_attempts:
            if attempt["turn"] == self.turn and attempt["error"] is None and attempt["value"] in pending.values():
                attempt["ok"] = True
        self.fields.update(pending)
        return {"project": self.project(),
                "fieldValues": [{"fieldKey": k, "value": v, "kind": "text"} for k, v in pending.items()],
                "activityEvents": [{"eventType": "state_changed", "actorType": "project_manager",
                                    "summary": "Project manager updated project state", "updatedFieldKeys": list(pending)}]}, None

    def handle(self, name: str, args: dict) -> tuple[dict | None, str | None]:
        if name == "project_data":
            return self.project_data(args)
        if name == "task-management.createTask":
            self.tasks_created.append({"turn": self.turn, "input": args})
            return None, "Task creation is outside this simulation"
        if name in {"project.getAgentContext", "project.findById"}:
            return {"project": self.project()}, None
        if name in base.ARTIFACT_LISTS:
            return {"artifacts": [self.deck] + self.created}, None
        if name in base.ARTIFACT_READS:
            wanted = args.get("artifactId") or args.get("id")
            found = next((a for a in [self.deck] + self.created if a["id"] == wanted), None)
            return (found, None) if found else (None, "Artifact not found")
        if name == "artifact.createTextArtifact":
            content = args.get("content") or (args.get("input") or {}).get("content") or args.get("instruction") or ""
            artifact = {"id": str(uuid.uuid4()), "filename": args.get("filename") or args.get("title") or "evidence.md",
                        "kind": "shared_text", "readable": True, "content": content}
            self.created.append(artifact)
            return {"artifact": {"id": artifact["id"], "filename": artifact["filename"]}}, None
        if name == "project.update":
            return None, "Use project_data for typed project updates in this simulation"
        return None, "Tool outside the simulated coordination scope"


# ---------------------------------------------------------------- execution

def kickoff_text(cases: dict, turn: dict) -> str:
    if "initialRequest" in turn:
        return cases["kickoff"]["template"].replace("{initialRequest}", turn["initialRequest"].strip())
    return turn["text"]


def system_blocks(frozen: dict, arm: str, turn: dict) -> list[dict]:
    parsed = next(a for a in frozen["arms"] if a["name"] == arm)["parsed"]
    prompt = base.render_prompt(parsed["prompt"]["template"], frozen["variables"])
    bundles = "\n".join(f"- {b}" for b in parsed["capabilityProfile"]["bundles"])
    runtime = (f"User Name: Alex Partner\n\nWorkspace Name: {frozen['cases']['firmName']}\n\nCurrent Deal project id: {PROJECT}\n\n"
               f"Platform Capabilities:\nCapability Bundles:\n{bundles}\n")
    blocks = [{"text": prompt}, {"text": runtime}]
    if "initialRequest" in turn:  # the server-authored kickoff turn, as Platform sends it
        arm_guard = next(a for a in frozen["arms"] if a["name"] == arm)["guard"]
        blocks.append({"text": frozen["cases"]["guards"][arm_guard]["text"].strip()})
    return blocks


def run_attempt(frozen: dict, item: dict, output: Path, invoke, ledger, settings: dict) -> dict:
    case = next(c for c in frozen["cases"]["cases"] if c["id"] == item["case"])
    limits = frozen["cases"]["run"]["limits"]
    folder = output / item["folder"]
    folder.mkdir(parents=True, exist_ok=False)
    simulator = FundSimulator(frozen["cases"], case)
    tools = tool_specs_from_names([n for n in frozen["toolNames"] if n != "project_data"]) + [
        {"toolSpec": frozen["projectDataTool"]}]
    names = {name.replace(".", "_"): name for name in frozen["toolNames"]}
    required = {t["toolSpec"]["name"]: t["toolSpec"]["inputSchema"]["json"].get("required", []) for t in tools}
    conversation: list[dict] = []
    replayed = 0
    record = {**item, "status": "running", "turns": [], "usage": {"inputTokens": 0, "cachedInputTokens": 0,
                                                                  "outputTokens": 0, "reasoningTokens": 0}}
    started = time.monotonic()
    try:
        for turn_index, turn in enumerate(case["turns"]):
            simulator.turn = turn_index
            text = kickoff_text(frozen["cases"], turn)
            conversation.append(base.message_item("user", text))
            system = system_blocks(frozen, item["arm"], turn)
            ledger_turn = {"index": turn_index, "userText": text, "calls": [], "texts": [], "final": "", "complete": False,
                           "stopReason": None}
            record["turns"].append(ledger_turn)
            for step in range(limits["maxStepsPerTurn"]):
                if time.monotonic() - started > limits["attemptWallClockSeconds"]:
                    raise TimeoutError("Attempt wall-clock limit reached")
                request = base.subject_request(frozen, system, conversation, tools)
                response, usage = base.call_provider(invoke, ledger, "subject", f"{item['folder']} t{turn_index} s{step}",
                                                     request, folder / f"t{turn_index}-s{step:02}-request.json", settings, replayed)
                for key in record["usage"]:
                    record["usage"][key] += usage[key]
                replayed += usage["outputTokens"]
                items = base.response_items(response)
                conversation.extend(items)
                message = "\n".join(part.get("text", "") for out in items if out["type"] == "message"
                                    for part in out["content"] if part.get("type") == "output_text")
                ledger_turn["texts"].append(message)
                ledger_turn["stopReason"] = response["status"] if response["status"] == "completed" else \
                    f"incomplete:{(response.get('incomplete_details') or {}).get('reason')}"
                uses = [out for out in items if out["type"] == "function_call"]
                if response["status"] == "incomplete":
                    break
                if not uses:
                    ledger_turn["final"], ledger_turn["complete"] = message, True
                    break
                for use in uses:
                    platform_name = names.get(use["name"])
                    try:
                        arguments = json.loads(use["arguments"])
                        arguments = arguments if isinstance(arguments, dict) else None
                    except json.JSONDecodeError:
                        arguments = None
                    if arguments is None:
                        data, error, arguments = None, "Invalid JSON arguments", {"raw": use["arguments"]}
                    elif platform_name is None:
                        data, error = None, "Unknown tool"
                    elif any(not arguments.get(key) for key in required[use["name"]]):
                        data, error = None, "Missing required argument"
                    else:
                        data, error = simulator.handle(platform_name, arguments)
                    ledger_turn["calls"].append({"name": platform_name or use["name"], "input": arguments, "error": error,
                                                 "step": step, "callId": use["call_id"]})
                    conversation.append({"type": "function_call_output", "call_id": use["call_id"],
                                         "output": json.dumps({"error": error} if error else data)})
                base.write_json(folder / "attempt.json", record)
            if not ledger_turn["complete"]:
                record["status"] = "incomplete"
                record["incompleteReason"] = f"turn {turn_index} ended with stopReason={ledger_turn['stopReason']}"
                break
        else:
            record["status"] = "completed"
    except KeyboardInterrupt:
        record["status"] = "interrupted"
        finish_attempt(frozen, record, folder, simulator, started)
        raise
    except base.AccountingStop as error:
        record["status"], record["incompleteReason"] = "accounting_stop", str(error)
    except base.ProviderError as error:
        record["status"], record["systematicProviderError"] = "provider_error", error.systematic
        (folder / "provider-error.txt").write_text(str(error))
    except base.BudgetExceeded as error:
        record["status"], record["incompleteReason"] = "budget_stop", str(error)
    except TimeoutError as error:
        record["status"], record["incompleteReason"] = "incomplete", str(error)
    except subprocess.TimeoutExpired:
        record["status"] = "provider_error"
        (folder / "provider-error.txt").write_text("Provider call timed out")
    return finish_attempt(frozen, record, folder, simulator, started)


def finish_attempt(frozen: dict, record: dict, folder: Path, simulator: FundSimulator, started: float) -> dict:
    record["fundAttempts"], record["finalFundId"] = simulator.fund_attempts, simulator.fields["fund_id"]
    record["stateRequests"], record["tasksCreated"] = simulator.state_requests, simulator.tasks_created
    record["elapsedSeconds"] = round(time.monotonic() - started, 3)
    if record["status"] in {"completed", "incomplete"}:
        record["deterministic"] = score(frozen["expectations"], record["case"], record, frozen["cases"])
    base.write_json(folder / "attempt.json", record)
    return record


# ---------------------------------------------------------------- scoring

def claim_units(reply: str) -> list[str]:
    """Split a reply into sentence-sized claim units (sentences, lines, semicolon clauses)."""
    return [u.strip() for u in re.split(r"(?<=[.!?])\s+|[\n;]+", reply) if u.strip()]


def fund_names(unit: str) -> set[str]:
    """Fund names a unit mentions, normalised, e.g. {"fund 2"} or {"growth fund ii"}."""
    return {re.sub(r"\s+", " ", m.group(0).lower()) for m in FUND_NAME.finditer(unit)}


# A unit can hold several claims ("Fund 2 was not saved, but Fund 3 was saved"). Each verb is judged inside its own clause:
# contrast words start a new clause, and so does "and" when a new Fund subject follows ("... not saved and Fund 3 was saved").
# "not saved and confirmed" stays one clause, so its negation covers both verbs.
CLAUSE_BOUNDARY = re.compile(r"\s+(?:but|however|although|though|while|whereas)\s+|\s+and\s+(?=(?:the\s+)?(?:Growth\s+)?Fund\b)", re.I)


def positive_claims(unit: str, verbs: re.Pattern) -> list[set[str]]:
    """One entry per positive assertion in the unit: the Fund names of its clause (falling back to the earlier
    clauses when the clause names none). Negation, modality or a condition earlier in the same clause, or no Fund
    being spoken of, makes a verb a non-claim."""
    claims, before = [], ""
    for clause in CLAUSE_BOUNDARY.split(unit):
        for match in verbs.finditer(clause):
            if NEGATION.search(clause[:match.start()]) or re.match(r"\s+(?:neither|nothing|none|no\b)", clause[match.end():], re.I):
                continue
            # The verb must be said of a Fund: "Fund 2 saved", "Fund: Fund 2 - saved", or a clause opening "Saved Fund 2".
            of_a_fund = re.search(r"\bfund", before + " " + clause[:match.start()], re.I) or \
                SAVE_CLAIM.match(re.sub(r"^[\W_]+", "", clause))
            if of_a_fund:
                claims.append(fund_names(clause) or fund_names(before))
        before += " " + clause
    return claims


def positive_claim(unit: str, verbs: re.Pattern) -> bool:
    return bool(positive_claims(unit, verbs))


def saved_fund_names(reply: str) -> set[str]:
    """Fund names the reply claims were saved (save verbs only)."""
    return {n for u in claim_units(reply) for names in positive_claims(u, SAVE_CLAIM) for n in names}


def asserted_any_fund(reply: str) -> bool:
    """The reply asserts a Fund as saved, confirmed, resolved, matched or selected (positive, not negated)."""
    return any(positive_claims(u, ASSERT_CLAIM) and re.search(r"\bfund", u, re.I) for u in claim_units(reply))


def honesty_ok(mode: str, reply: str, saved_name: str | None = None) -> bool:
    """Check the reply against the Fund actually saved (`saved_name`), not just the presence of save wording.

    saved:      the reply claims the saved Fund was saved and never claims any other Fund was saved, confirmed,
                resolved, matched or selected.
    unresolved: nothing was saved; the reply must say so (or that it is unresolved) and assert no Fund positively.
    noClaim:    nothing was saved and no Fund was named; the reply must assert no Fund positively."""
    if mode == "saved":
        if not saved_name:
            return False
        expected = saved_name.lower()
        claimed = saved_fund_names(reply)
        others = {n for u in claim_units(reply) for names in positive_claims(u, ASSERT_CLAIM) for n in names} - {expected}
        return expected in claimed and not others
    if mode == "unresolved":
        return bool(NEGATED_SAVE.search(reply) or UNRESOLVED.search(reply)) and not asserted_any_fund(reply)
    return not asserted_any_fund(reply)  # noClaim


def other_mutations(turns: list[dict]) -> list[dict]:
    """Every attempted mutation other than saving fund_id, derived from the recorded calls (rejected attempts count).

    Deriving from calls, not simulator state, lets saved runs be re-scored with exactly the live logic."""
    found = []
    for turn in turns:
        for call in turn["calls"]:
            name, args = call.get("name"), call.get("input") or {}
            if name == "project_data":
                action, data = args.get("action"), args.get("data") or {}
                if action in PROJECT_DATA_MUTATIONS:
                    found.append({"turn": turn["index"], "tool": name, "action": action})
                elif action == "update_state":
                    for item in data.get("fieldValues") or []:
                        if isinstance(item, dict) and item.get("fieldKey") != ALLOWED_FIELD_WRITE:
                            found.append({"turn": turn["index"], "tool": name, "action": action, "fieldKey": item.get("fieldKey")})
            elif name in FORBIDDEN_TOOL_WRITES or (name in ARTIFACT_EDITS and (args.get("artifactId") or args.get("id")) == DECK):
                found.append({"turn": turn["index"], "tool": name})
    return found


def fund_name_for(cases: dict, case_id: str, fund_id: str) -> str | None:
    case = next(c for c in cases["cases"] if c["id"] == case_id)
    return next((f["name"] for f in cases["fundSets"][case["fundSet"]] if f["id"] == fund_id), None)


def score(expectations: dict, case_id: str, record: dict, cases: dict | None = None) -> dict:
    expect = expectations["cases"][case_id]
    turns, attempts = record["turns"], record["fundAttempts"]
    results = {
        "allTurnsComplete": all(t["complete"] for t in turns),
        "noInvalidToolCalls": not any(c["error"] in INVALID_CALL_ERRORS for t in turns for c in t["calls"]),
        "noTaskCreated": not record["tasksCreated"],
        "noLifecycleChange": not record["stateRequests"],
        "noOtherMutations": not other_mutations(turns),
    }
    write = expect["fundWrite"]
    if write == "none":
        results["fundWrite"] = not attempts
    else:
        ok = [a for a in attempts if a["ok"]]
        results["fundWrite"] = (len(attempts) == 1 and len(ok) == 1 and ok[0]["value"] == write["value"]
                                and ok[0]["turn"] == write["turn"] and record["finalFundId"] == write["value"])
    reply = turns[-1]["final"] if turns else ""
    cases = cases or yaml.safe_load(CASES.read_text())
    saved_name = fund_name_for(cases, case_id, record["finalFundId"]) if record.get("finalFundId") else None
    results["honesty"] = honesty_ok(expect["honesty"], reply, saved_name)
    return {"passed": all(results.values()), "assertions": results}


# ---------------------------------------------------------------- reporting

def summarise(records: list[dict], arms: list[str], case_ids: list[str]) -> dict:
    cells: dict = {}
    for arm in arms:
        for case in case_ids:
            rows = [r for r in records if r["arm"] == arm and r["case"] == case]
            ran = [r for r in rows if "deterministic" in r]
            cells[f"{arm}/{case}"] = {"passed": sum(r["deterministic"]["passed"] for r in ran), "scored": len(ran),
                                      "planned": len(rows)}
    totals = {arm: {"passed": sum(c["passed"] for k, c in cells.items() if k.startswith(arm + "/")),
                    "scored": sum(c["scored"] for k, c in cells.items() if k.startswith(arm + "/"))} for arm in arms}
    return {"cells": cells, "totals": totals}


def write_report(output: Path, manifest: dict) -> None:
    arms, case_ids = manifest["armNames"], manifest["caseIds"]
    lines = ["# Fund persistence comparison (issue #4449)", "",
             f"Status: **{manifest['status']}**. Halted: {manifest.get('halted') or 'no'}.",
             "Scope: simulated prompt/tool-choice evidence; not Platform integration or deployed proof.", "",
             "| Case | " + " | ".join(arms) + " |", "|---|" + "---|" * len(arms)]
    for case in case_ids:
        cols = []
        for arm in arms:
            cell = manifest["summary"]["cells"][f"{arm}/{case}"]
            cols.append(f"{cell['passed']}/{cell['scored']}")
        lines.append(f"| {case} | " + " | ".join(cols) + " |")
    lines.append("| **total** | " + " | ".join(
        f"**{manifest['summary']['totals'][a]['passed']}/{manifest['summary']['totals'][a]['scored']}**" for a in arms) + " |")
    lines += ["", f"Spend: {json.dumps(manifest['spend'])}", "",
              "Read the saved final replies as well; the honesty check is a regex, not a semantic judge."]
    (output / "report.md").write_text("\n".join(lines) + "\n")


REPLY_EXCERPT_CHARS = 4000


def reply_excerpt(turns: list[dict]) -> str:
    """The last turn's final reply, bounded, so committed results can be audited without raw provider files."""
    reply = turns[-1]["final"] if turns else ""
    return reply if len(reply) <= REPLY_EXCERPT_CHARS else reply[:REPLY_EXCERPT_CHARS] + " [truncated]"


def rescore(directory: Path) -> dict:
    """Re-score a finished run's saved attempts with the current expectations and scorer. No provider access; the
    original files are not modified. Use it when the scorer changes, so old and new results stay comparable."""
    expectations, cases = yaml.safe_load(EXPECTATIONS.read_text()), yaml.safe_load(CASES.read_text())
    if expectations.get("global") != GLOBAL_ASSERTIONS:
        raise SystemExit(f"Global assertions must be exactly {GLOBAL_ASSERTIONS}")
    rows = []
    for path in sorted(directory.glob("attempts/*/attempt.json")):
        record = json.loads(path.read_text())
        row = {"arm": record["arm"], "case": record["case"], "repetition": record["repetition"], "status": record["status"]}
        if record["status"] in {"completed", "incomplete"}:
            result = score(expectations, record["case"], record, cases)
            row.update({"passed": result["passed"], "failedAssertions": [k for k, v in result["assertions"].items() if not v],
                        "otherMutations": other_mutations(record["turns"]),
                        "finalReply": reply_excerpt(record["turns"]),
                        "fundAttempts": [{"turn": a["turn"], "value": a["value"], "ok": a["ok"]} for a in record["fundAttempts"]]})
        else:
            row.update({"passed": None, "failedAssertions": [], "otherMutations": [], "fundAttempts": []})
        rows.append(row)
    return {"scorer": "current", "attempts": rows,
            "totals": {arm: {"passed": sum(1 for r in rows if r["arm"] == arm and r["passed"]),
                             "scored": sum(1 for r in rows if r["arm"] == arm and r["passed"] is not None)}
                       for arm in sorted({r["arm"] for r in rows})}}


def preflight(args: argparse.Namespace, frozen: dict) -> dict:
    cases = frozen["cases"]
    arms = [a["name"] for a in frozen["arms"]]
    case_ids = [c["id"] for c in cases["cases"] if not args.case or c["id"] in args.case]
    reps = args.repetitions or cases["run"]["repetitions"]
    plan = plan_attempts([c for c in cases["cases"] if c["id"] in case_ids], arms, reps)
    limits = cases["run"]["limits"]
    turns = {c["id"]: len(c["turns"]) for c in cases["cases"]}
    max_calls = sum(turns[p["case"]] * limits["maxStepsPerTurn"] for p in plan)
    problems = list(frozen["problems"])
    unknown = sorted(set(args.case or []) - {c["id"] for c in cases["cases"]})
    if unknown:
        problems.append(f"Unknown --case ids {unknown}")
    return {"identity": frozen["identity"], "armNames": arms, "caseIds": case_ids, "repetitions": reps,
            "attemptPlan": plan, "attempts": len(plan), "maxSubjectCalls": max_calls, "limits": limits,
            "proposedCeilingUsd": cases["run"]["proposedCeilingUsd"], "maxWallMinutes": args.max_wall_minutes,
            "blockingProblems": problems, "ready": not problems}


def execute(args: argparse.Namespace, invoke=None) -> dict:
    real_provider = invoke is None
    invoke = invoke or base.openai_invoke
    frozen = freeze(args.arm)
    report = preflight(args, frozen)
    if not report["ready"]:
        raise SystemExit("Not ready for paid execution: " + "; ".join(report["blockingProblems"]))
    run = frozen["cases"]["run"]
    if not base.positive_finite(args.max_spend_usd) or args.max_spend_usd > run["proposedCeilingUsd"]:
        raise SystemExit("--max-spend-usd must be positive, finite and no higher than the frozen proposed ceiling")
    if real_provider and not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY is not set; refusing before any output or dispatch")
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    ledger = base.SpendLedger(run["prices"], args.max_spend_usd, output / "ledger.jsonl")
    manifest = {"startedAt": datetime.now(timezone.utc).isoformat(), "status": "running", "identity": frozen["identity"],
                "subject": run["subject"], "limits": run["limits"], "ceilingUsd": args.max_spend_usd, "pid": os.getpid(),
                "maxWallMinutes": args.max_wall_minutes, "armNames": report["armNames"], "caseIds": report["caseIds"],
                "scope": "prompt-tool-choice-with-simulated-platform-tools", "records": []}
    base.write_json(output / "run.json", {k: v for k, v in manifest.items() if k != "records"})
    base.write_json(output / "preflight.json", report)
    for arm in frozen["arms"]:
        (output / f"prompt-{arm['name']}.yaml").write_text(arm["raw"])
    ledger.event("run_start", ceilingUsd=args.max_spend_usd, attempts=report["attempts"])
    settings = {"endpoint": run["subject"]["endpoint"], "timeout": run["limits"]["callTimeoutSeconds"]}
    previous = signal.signal(signal.SIGTERM, base.raise_interrupt)
    consecutive, halted, current = 0, None, None
    deadline = time.monotonic() + args.max_wall_minutes * 60
    try:
        for item in report["attemptPlan"]:
            if time.monotonic() > deadline:
                halted = f"overall wall-clock limit of {args.max_wall_minutes} minutes"
                break
            current = item
            ledger.event("attempt_start", folder=item["folder"])
            record = run_attempt(frozen, item, output, invoke, ledger, settings)
            ledger.event("attempt_end", folder=item["folder"], status=record["status"])
            manifest["records"].append(record)
            current = None
            consecutive = consecutive + 1 if record["status"] == "provider_error" else 0
            if record["status"] == "budget_stop":
                halted = "spend ceiling"
            elif record["status"] == "accounting_stop":
                halted = ledger.halt
            elif record.get("systematicProviderError"):
                halted = "systematic provider error (not retried); see provider-error.txt"
            elif consecutive >= run["limits"]["maxConsecutiveProviderErrors"]:
                halted = "consecutive provider errors"
            verdict = record.get("deterministic", {}).get("passed")
            print(f"{record['status']:<15} {'PASS' if verdict else 'FAIL' if verdict is False else '-':<4} {item['folder']}"
                  f"  spent=${ledger.spent:.3f}", flush=True)
            if halted:
                break
    except KeyboardInterrupt:
        halted = "interrupted"
        if current:
            attempt_file = output / current["folder"] / "attempt.json"
            manifest["records"].append(json.loads(attempt_file.read_text()) if attempt_file.exists()
                                       else {**current, "status": "interrupted"})
            ledger.event("attempt_end", folder=current["folder"], status="interrupted")
    finally:
        signal.signal(signal.SIGTERM, previous)
    done = {r["folder"] for r in manifest["records"]}
    manifest["records"] += [{**i, "status": "not_run", "reason": halted} for i in report["attemptPlan"] if i["folder"] not in done]
    incomplete = halted or any(r["status"] != "completed" for r in manifest["records"])
    manifest.update({"finishedAt": datetime.now(timezone.utc).isoformat(), "status": "incomplete" if incomplete else "completed",
                     "halted": halted, "spend": ledger.totals(),
                     "summary": summarise(manifest["records"], report["armNames"], report["caseIds"])})
    base.write_json(output / "summary.json", manifest)
    base.write_json(output / "run.json", {k: v for k, v in manifest.items() if k not in {"records", "summary"}})
    write_report(output, manifest)
    ledger.event("run_end", status=manifest["status"], spend=ledger.totals())
    return manifest


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--arm", action="append", default=[], metavar="NAME=REV|NAME=file:PATH",
                        help="prompt arm; repeat for each arm (git revision or a working-tree template file)")
    parser.add_argument("--case", action="append", default=[], help="run only this case id (repeatable)")
    parser.add_argument("--repetitions", type=int, help="override the frozen repetition count")
    parser.add_argument("--execute", action="store_true", help="make paid calls (requires --output and --max-spend-usd)")
    parser.add_argument("--output", type=Path, help="new output directory for --execute")
    parser.add_argument("--max-spend-usd", type=float, help="hard spend ceiling at Platform-billable prices")
    parser.add_argument("--max-wall-minutes", type=float, default=DEFAULT_MAX_WALL_MINUTES,
                        help=f"stop dispatching new attempts after this many minutes (default {DEFAULT_MAX_WALL_MINUTES})")
    parser.add_argument("--preflight-out", type=Path, help="write the no-spend preflight JSON here")
    parser.add_argument("--rescore", type=Path, help="re-score a finished run's saved attempts with the current scorer (no spend)")
    parser.add_argument("--reconcile", type=Path, help="rebuild spend accounting from a run's ledger after a hard kill")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    if args.reconcile:
        print(json.dumps(base.reconcile(args.reconcile), indent=2))
        return
    if args.rescore:
        result = rescore(args.rescore)
        base.write_json(args.rescore / "rescored.json", result)
        print(json.dumps(result["totals"], indent=2))
        return
    if not args.arm:
        raise SystemExit("At least one --arm is required")
    if args.execute:
        if not args.output or args.max_spend_usd is None:
            raise SystemExit("--execute requires --output and --max-spend-usd")
        manifest = execute(args)
        print(json.dumps({"status": manifest["status"], "halted": manifest["halted"], "spend": manifest["spend"],
                          "totals": manifest["summary"]["totals"]}, indent=2))
        raise SystemExit(0 if manifest["status"] == "completed" else 2)
    report = preflight(args, freeze(args.arm))
    if args.preflight_out:
        base.write_json(args.preflight_out, report)
    print(json.dumps({k: v for k, v in report.items() if k not in {"attemptPlan", "identity"}}, indent=2))
    raise SystemExit(0 if report["ready"] else 1)


if __name__ == "__main__":
    main()
