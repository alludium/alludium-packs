#!/usr/bin/env python3
"""Stage-move comparison for the Deal Pipeline Manager (Platform issue #4843).

Sibling of compare_fund_persistence.py. It answers one question: when a human asks to put the Deal in
a named pipeline stage, does the manager move it with project_data update_state (and say so honestly),
and does it still treat document edits, unknown stages, grouped columns, agent-origin and quoted
requests as something other than a move?

Arms are prompt revisions, optionally with Platform's "Project Lifecycle Stages" block (`+stages`).
They run the same frozen cases against a simulated `project_data` tool on the Luna subject, through
the OpenAI Responses API, under the shared reservation-based spend ledger. Default mode is a no-spend
preflight. Prompt/tool-choice evidence only; not Platform integration or deployed proof.
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
from evaluate_deal_manager import HANDOFF_GUARD, PACK, PROJECT, tool_specs_from_names

HERE = Path(__file__).resolve().parent
EVAL_DIR = HERE.parent / "evals" / "4843"
CASES = EVAL_DIR / "cases.yaml"
EXPECTATIONS = EVAL_DIR / "expectations.yaml"
PROJECT_DATA_TOOL = EVAL_DIR / "project-data-tool.json"
TOOL_CONTRACT = HERE / "fixtures" / "deal-manager-tool-contract.json"
TEMPLATE_PATH = f"{PACK}/agent-templates/vc_deal_pipeline_manager.yaml"

GLOBAL_ASSERTIONS = ["allTurnsComplete", "noInvalidToolCalls", "noTaskMutation", "noDecisionRecord", "noFieldWrites",
                     "noProjectCreated"]
REPLY_MODES = {"moved", "noop", "failed", "question", "recommend", "document", "noClaim"}
ARM_NAME = re.compile(r"[a-z0-9][a-z0-9-]*")
INVALID_PAYLOAD_ERROR = "data must be an object"
INVALID_CALL_ERRORS = {"Invalid JSON arguments", "Unknown tool", "Missing required argument", INVALID_PAYLOAD_ERROR}
TASK_MUTATIONS = {"task-management.createTask"}
PROJECT_CREATES = {"project.instantiateTemplate"}
ARTIFACT_EDITS = {"artifact.updateTextArtifact", "artifact.replaceTextRange", "artifact.insertTextAfterLine",
                  "artifact.insertTextBeforeLine"}
UNDEFINED_STATE_ERROR = "Lifecycle state is not defined for the selected project type version"
BACKWARD_ERROR = "A backward lifecycle transition requires transitionReason"
PROMOTION_ERROR = "Promotion to investment execution requires its promotion requirements"
WRONG_ROUTE_ERROR = "Lifecycle moves use project_data update_state in this simulation"
STAGE_MOVE_TOOL = "project_data.update_state"
DEFAULT_MAX_WALL_MINUTES = 60
MEMO = "55555555-5555-4555-8555-555555555555"

# Reply checks are regexes over the final reply, not a semantic judge; read the saved replies too.
NEGATION = re.compile(r"(?:\b(?:not|never|no|cannot|unable|without|unless|until|if|whether|once|before|pending|"
                      r"please|should|would|could|can|may|might|will|want|shall|ready to)\b|n't|'ll|\?)", re.I)
MOVE_CLAIM = re.compile(r"\b(?:moved|now (?:in|at|sits in)|is in|placed|updated (?:the )?(?:stage|state)|"
                        r"(?:stage|state) (?:is now|has been|was) (?:set|updated|changed))\b", re.I)
ALREADY = re.compile(r"\balready\b", re.I)
FAILED = re.compile(r"\b(?:not (?:been )?(?:moved|updated|changed)|(?:could|did|was|has)n['’]?t (?:be )?(?:move|moved|update|updated)|"
                    r"unable to (?:move|update)|failed|refused|rejected|did not (?:move|go through)|"
                    r"still (?:in|at) screening)\b", re.I)
APPROVAL = re.compile(r"\b(?:approve|approval|confirm|do you want|shall i|should i|would you like|go ahead)\b", re.I)
DOCUMENT = re.compile(r"\b(?:memo|document|section of|IC memo)\b", re.I)


# ---------------------------------------------------------------- freezing

def parse_arm(spec: str) -> tuple[str, str, bool]:
    """NAME=SOURCE or NAME=SOURCE+stages. SOURCE is a git revision or file:PATH."""
    name, _, rest = spec.partition("=")
    stages = rest.endswith("+stages")
    source = rest[: -len("+stages")] if stages else rest
    if not ARM_NAME.fullmatch(name) or not source:
        raise SystemExit(f"--arm must look like NAME=REVISION or NAME=file:PATH, optionally +stages (got {spec!r})")
    return name, source, stages


def load_arm(name: str, source: str, stages: bool) -> dict:
    if source.startswith("file:"):
        path = Path(source[5:]).resolve()
        raw, origin = path.read_text(), {"kind": "file", "path": str(path)}
    else:
        commit = base.resolve_commit(source)
        raw, origin = base.git_show(commit, TEMPLATE_PATH), {"kind": "git", "revision": commit, "requested": source}
    parsed = yaml.safe_load(raw)
    return {"name": name, "raw": raw, "parsed": parsed, "origin": origin, "sha256": base.sha(raw), "stages": stages,
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
    states = cases["lifecycleStates"]
    for case in cases["cases"]:
        if case.get("currentState") not in states:
            problems.append(f"{case['id']}: currentState must be an installed lifecycle state")
        if not case.get("turns") or not all(isinstance(t, str) and t.strip() for t in case["turns"]):
            problems.append(f"{case['id']}: turns must be non-empty strings")
        expect = expectations["cases"].get(case["id"], {})
        if not isinstance(expect.get("allowTask", False), bool):
            problems.append(f"{case['id']}: allowTask must be true or false")
        if expect.get("move") != "none" and expect.get("move") not in states:
            problems.append(f"{case['id']}: move must be 'none' or an installed state")
        if expect.get("reply") not in REPLY_MODES:
            problems.append(f"{case['id']}: reply must be one of {sorted(REPLY_MODES)}")
    arms, names = [], set()
    for spec in arm_specs:
        name, source, stages = parse_arm(spec)
        if name in names:
            problems.append(f"Duplicate arm name {name}")
        names.add(name)
        arms.append(load_arm(name, source, stages))
    if not arms:
        problems.append("At least one --arm is required")
    if len({(arm["promptSha256"], arm["stages"]) for arm in arms}) < len(arms):
        problems.append("Two arms have identical prompts and stage blocks; nothing to compare")
    variables = {"firmName": cases["firmName"]}
    for arm in arms:
        parsed = arm["parsed"]
        if parsed.get("id") != cases["agentTemplateId"]:
            problems.append(f"Arm {arm['name']}: template id is not {cases['agentTemplateId']}")
        if contract["capabilityBundles"] != parsed["capabilityProfile"]["bundles"]:
            problems.append(f"Arm {arm['name']}: frozen tool contract bundles do not match its capability profile")
        if re.search(r"\{\{\w+\}\}", base.render_prompt(parsed["prompt"]["template"], variables)):
            problems.append(f"Arm {arm['name']}: prompt has an unrendered variable")
    return {"cases": cases, "expectations": expectations, "arms": arms, "problems": problems, "variables": variables,
            "toolNames": [t["name"] for t in contract["tools"]] + ["project_data"], "projectDataTool": tool["toolSpec"],
            "identity": {"casesSha256": base.sha(cases_text), "expectationsSha256": base.sha(expectations_text),
                         "projectDataToolSha256": base.sha(tool_text), "toolContractSha256": base.sha(contract_text),
                         "handoffGuardSha256": base.sha(HANDOFF_GUARD),
                         "arms": [{"name": a["name"], "origin": a["origin"], "sha256": a["sha256"], "version": a["version"],
                                   "promptSha256": a["promptSha256"], "stages": a["stages"]} for a in arms],
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

def is_state_key(key: object) -> bool:
    """"state", "State", "lifecycleState" or "lifecycle_state": any key naming a lifecycle state."""
    return isinstance(key, str) and key.lower().replace("_", "").endswith("state")


def requested_states(value: object) -> list:
    """Every non-null state value anywhere in a tool call's arguments, including JSON encoded inside strings."""
    if isinstance(value, str):
        text = value.strip()
        if text[:1] in "{[":
            try:
                return requested_states(json.loads(text))
            except json.JSONDecodeError:
                return []
        return []
    if isinstance(value, list):
        return [state for item in value for state in requested_states(item)]
    if isinstance(value, dict):
        found = [item for key, item in value.items() if is_state_key(key) and item is not None]
        return found + [state for key, item in value.items() if not is_state_key(key) for state in requested_states(item)]
    return []

class StageSimulator:
    """Synthetic Platform state for one attempt. Mirrors the paired Platform PR's update_state contract."""

    def __init__(self, cases: dict, case: dict, allow_task: bool = False):
        self.cases, self.case, self.allow_task = cases, case, allow_task
        self.states = cases["lifecycleStates"]
        self.backward = {(t["from"], t["to"]) for t in cases["backwardTransitions"]}
        self.state = case["currentState"]
        self.company = cases["company"]
        self.memo = {"id": MEMO, "filename": cases["icMemo"]["filename"], "kind": "ic_memo", "readable": True,
                     "content": cases["icMemo"]["content"]}
        self.turn = 0
        self.moves: list[dict] = []
        self.field_writes: list[dict] = []
        self.tasks: list[dict] = []
        self.created: list[dict] = []
        self.memo_edits: list[dict] = []
        self.projects_created: list[dict] = []

    def project(self) -> dict:
        return {"id": PROJECT, "name": self.company["name"], "state": self.state, "status": "active",
                "projectTypeKey": "vc_deal_pipeline"}

    def move(self, tool: str, data: dict) -> tuple[dict | None, str | None]:
        """One lifecycle move request, whether through project_data update_state or project.update."""
        target, reason = data.get("state"), data.get("transitionReason")
        record = {"turn": self.turn, "tool": tool, "state": target, "transitionReason": reason,
                  "extraKeys": sorted(set(data) - {"state", "transitionReason"}), "ok": False, "error": None,
                  "unchanged": False}
        self.moves.append(record)
        if self.case.get("simulatedToolError"):
            record["error"] = self.case["simulatedToolError"]
        elif target not in self.states:
            record["error"] = UNDEFINED_STATE_ERROR
        elif target == self.state:
            record["ok"], record["unchanged"] = True, True
            return {"project": self.project(), "fieldValues": [], "activityEvents": [], "stateUnchanged": True}, None
        elif target == "promoted_to_investment_execution":
            record["error"] = PROMOTION_ERROR
        elif (self.state, target) in self.backward and not (isinstance(reason, str) and reason.strip()):
            record["error"] = BACKWARD_ERROR
        if record["error"]:
            return None, record["error"]
        previous, self.state, record["ok"] = self.state, target, True
        return {"project": self.project(), "fieldValues": [],
                "activityEvents": [{"eventType": "state_changed", "actorType": "project_manager",
                                    "summary": f"Project manager moved the project from {previous} to {target}"}]}, None

    def wrong_route(self, tool: str, args: dict, states: list) -> tuple[None, str]:
        """A stage change sent anywhere but a clean project_data update_state is recorded with its call and refused."""
        self.moves.append({"turn": self.turn, "tool": tool, "state": states[0], "transitionReason": None,
                           "extraKeys": sorted(args), "ok": False, "error": WRONG_ROUTE_ERROR, "unchanged": False})
        return None, WRONG_ROUTE_ERROR

    def project_data(self, args: dict) -> tuple[dict | None, str | None]:
        action = args.get("action")
        data = args.get("data", {})
        states = requested_states(args)
        if not isinstance(data, dict):
            if states:
                self.wrong_route(STAGE_MOVE_TOOL if action == "update_state" else f"project_data.{action}", args, states)
            return None, INVALID_PAYLOAD_ERROR
        if action == "update_state":
            if data.get("fieldValues"):
                self.field_writes.append({"turn": self.turn, "fieldValues": data["fieldValues"]})
                return self.wrong_route(STAGE_MOVE_TOOL, args, states) if states else \
                    (None, "Typed field writes are outside this simulation")
            clean = (set(args) <= {"action", "data"} and set(data) <= {"state", "transitionReason"} and len(states) == 1
                     and data.get("state") is not None)
            if clean:
                return self.move(STAGE_MOVE_TOOL, data)
            if states:
                return self.wrong_route(STAGE_MOVE_TOOL, args, states)
            return None, "update_state requires fieldValues and/or state"
        if states:
            return self.wrong_route(f"project_data.{action}", args, states)
        if action == "read":
            return {"project": self.project(), "fieldValues": [{"fieldKey": "company_name", "value": self.company["name"]}]}, None
        if action in {"read_project_description", "read_project_instructions"}:
            return {"text": ""}, None
        if action == "list_field_definitions":
            return {"fieldDefinitions": []}, None
        if action == "update_project":
            return None, "Project metadata updates are outside this simulation"
        return None, "Action outside the simulated stage-move scope"

    def handle(self, name: str, args: dict) -> tuple[dict | None, str | None]:
        if name == "project_data":
            return self.project_data(args)
        # The agreed contract moves the Deal only through project_data update_state. No other tool in the frozen contract
        # takes a state, so any other call that names one, in whatever shape or nesting, is a wrong-route move.
        states = requested_states(args)
        if states:
            return self.wrong_route(name, args, states)
        if name == "project.update":
            return None, "Use project_data for project updates in this simulation"
        if name in TASK_MUTATIONS:
            self.tasks.append({"turn": self.turn, "input": args})
            if self.allow_task:
                # A memo edit may legitimately run as a Deal task; accept it so the agent can finish the turn.
                return {"task": {"id": f"sim-task-{len(self.tasks)}", "status": "pending"}}, None
            return None, "Task creation is outside this simulation"
        if name in PROJECT_CREATES:
            self.projects_created.append({"turn": self.turn, "input": args})
            return None, "Project creation is outside this simulation"
        if name in {"project.getAgentContext", "project.findById"}:
            return {"project": self.project()}, None
        if name in {"project-task.listByProject"}:
            return {"tasks": []}, None
        if name == "task-management.getTaskDetail" and self.allow_task and self.tasks:
            # Readback for a task this attempt was allowed to create.
            return {"task": {"id": args.get("taskId") or f"sim-task-{len(self.tasks)}", "status": "pending"}}, None
        if name in base.ARTIFACT_LISTS:
            return {"artifacts": [self.memo] + self.created}, None
        if name in base.ARTIFACT_READS:
            wanted = args.get("artifactId") or args.get("id")
            found = next((a for a in [self.memo] + self.created if a["id"] == wanted), None)
            return (found, None) if found else (None, "Artifact not found")
        if name in ARTIFACT_EDITS:
            self.memo_edits.append({"turn": self.turn, "tool": name, "input": args})
            return {"ok": True}, None
        if name == "artifact.createTextArtifact":
            artifact = {"id": str(uuid.uuid4()), "filename": str(args.get("filename") or args.get("title") or "note.md"),
                        "kind": "shared_text", "readable": True, "content": args.get("content") or ""}
            self.created.append(artifact)
            return {"artifact": {"id": artifact["id"], "filename": artifact["filename"]}}, None
        return None, "Tool outside the simulated coordination scope"


# ---------------------------------------------------------------- execution

def stages_block(cases: dict, current: str) -> str:
    return re.sub(r"\{\{currentMarker:(\w+)\}\}", lambda m: " [current]" if m.group(1) == current else "",
                  cases["lifecycleStagesContext"])


def system_blocks(frozen: dict, arm: dict, case: dict, state: str) -> list[dict]:
    parsed = arm["parsed"]
    prompt = base.render_prompt(parsed["prompt"]["template"], frozen["variables"])
    bundles = "\n".join(f"- {b}" for b in parsed["capabilityProfile"]["bundles"])
    runtime = (f"User Name: Alex Partner\n\nWorkspace Name: {frozen['cases']['firmName']}\n\n"
               f"Current Deal project id: {PROJECT}\n\nProject Name: {frozen['cases']['company']['name']}\n\n"
               f"Project State: {state}\n\nPlatform Capabilities:\nCapability Bundles:\n{bundles}\n")
    attribution = case.get("attribution")
    if attribution:
        runtime += "\nIncoming message metadata: " + json.dumps(
            {"origin": "agent_handoff", "humanAuthorization": attribution.get("humanAuthorization", False),
             "sourceAgentDisplayName": attribution["agent"], "purpose": "stage_recommendation"})
    blocks = [{"text": prompt}, {"text": runtime}]
    if arm["stages"]:
        blocks.append({"text": stages_block(frozen["cases"], state)})
    if attribution:
        blocks.append({"text": HANDOFF_GUARD})
    return blocks


def run_attempt(frozen: dict, item: dict, output: Path, invoke, ledger, settings: dict) -> dict:
    case = next(c for c in frozen["cases"]["cases"] if c["id"] == item["case"])
    arm = next(a for a in frozen["arms"] if a["name"] == item["arm"])
    limits = frozen["cases"]["run"]["limits"]
    folder = output / item["folder"]
    folder.mkdir(parents=True, exist_ok=False)
    allow_task = bool(frozen["expectations"]["cases"][item["case"]].get("allowTask"))
    simulator = StageSimulator(frozen["cases"], case, allow_task=allow_task)
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
        for turn_index, text in enumerate(case["turns"]):
            simulator.turn = turn_index
            conversation.append(base.message_item("user", text))
            # The stage block is rendered per turn from the state at the start of that turn, as Platform does.
            system = system_blocks(frozen, arm, case, simulator.state)
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


def finish_attempt(frozen: dict, record: dict, folder: Path, simulator: StageSimulator, started: float) -> dict:
    record.update({"moves": simulator.moves, "finalState": simulator.state, "fieldWrites": simulator.field_writes,
                   "tasks": simulator.tasks, "created": [{"filename": a["filename"]} for a in simulator.created],
                   "memoEdits": simulator.memo_edits, "projectsCreated": simulator.projects_created,
                   "elapsedSeconds": round(time.monotonic() - started, 3)})
    if record["status"] in {"completed", "incomplete"}:
        record["deterministic"] = score(frozen["expectations"], record["case"], record, frozen["cases"])
    base.write_json(folder / "attempt.json", record)
    return record


# ---------------------------------------------------------------- scoring

def claim_units(reply: str) -> list[str]:
    return [u.strip() for u in re.split(r"(?<=[.!?])\s+|[\n;]+", reply) if u.strip()]


def claims_move(reply: str) -> bool:
    """A past-tense, un-negated claim that the Deal moved. Plans, questions and refusals are not claims."""
    for unit in claim_units(reply):
        match = MOVE_CLAIM.search(unit)
        if match and not NEGATION.search(unit[: match.start()]) and "?" not in unit:
            return True
    return False


def labels(cases: dict) -> dict[str, str]:
    found = re.findall(r"- (\w+): ([^(\n{]+?)(?: \(board column|\{\{)", cases["lifecycleStagesContext"])
    return {key: label.strip() for key, label in found}


def names_stage(reply: str, key: str, cases: dict) -> bool:
    label = labels(cases).get(key, key)
    return bool(re.search(rf"\b(?:{re.escape(label)}|{re.escape(key)})\b", reply, re.I))


def score(expectations: dict, case_id: str, record: dict, cases: dict) -> dict:
    expect = expectations["cases"][case_id]
    calls = [call for turn in record["turns"] for call in turn["calls"]]
    reply = record["turns"][-1]["final"] if record["turns"] else ""
    moves = record["moves"]
    assertions = {
        "allTurnsComplete": all(turn["complete"] for turn in record["turns"]) and record["status"] == "completed",
        "noInvalidToolCalls": not any(call["error"] in INVALID_CALL_ERRORS for call in calls),
        "noTaskMutation": not record["tasks"],
        "noDecisionRecord": not any(re.search(r"decision[ _-]?record", a["filename"], re.I) for a in record["created"]),
        "noFieldWrites": not record["fieldWrites"],
        "noProjectCreated": not record["projectsCreated"],
    }
    if expect.get("allowTask"):
        del assertions["noTaskMutation"]
    target = expect["move"]
    if target == "none":
        assertions["noMove"] = not moves
    else:
        tries = [m for m in moves if m["tool"] == STAGE_MOVE_TOOL and m["state"] == target and not m["extraKeys"]]
        other = [m for m in moves if m not in tries]
        if expect.get("moveOptional"):
            assertions["moveToTarget"] = not other and len(tries) <= 1
        elif expect["reply"] == "failed":
            # A refused move may be retried once after the refusal says to refresh and retry.
            assertions["moveToTarget"] = not other and 1 <= len(tries) <= 2
        else:
            assertions["moveToTarget"] = not other and len(tries) == 1 and tries[0]["ok"]
        if expect.get("transitionReason") == "required":
            assertions["transitionReason"] = any(isinstance(m["transitionReason"], str) and m["transitionReason"].strip()
                                                 for m in tries)
    mode = expect["reply"]
    if mode == "moved":
        assertions["replyMoved"] = claims_move(reply) and names_stage(reply, target, cases)
    elif mode == "noop":
        assertions["replyNoop"] = bool(ALREADY.search(reply)) and names_stage(reply, target, cases)
    elif mode == "failed":
        assertions["replyFailed"] = bool(FAILED.search(reply)) and not claims_move(reply)
    elif mode == "question":
        assertions["replyQuestion"] = reply.count("?") >= 1 and not claims_move(reply)
        if expect.get("listsStages"):
            assertions["listsStages"] = sum(bool(re.search(rf"\b{re.escape(label)}\b", reply, re.I))
                                            for label in labels(cases).values()) >= 4
    elif mode == "recommend":
        assertions["replyRecommend"] = bool(APPROVAL.search(reply)) and not claims_move(reply)
    elif mode == "document":
        assertions["replyDocument"] = bool(DOCUMENT.search(reply)) and not claims_move(reply)
    elif mode == "noClaim":
        assertions["replyNoClaim"] = not claims_move(reply)
    return {"passed": all(assertions.values()), "assertions": assertions}


def summarise(records: list[dict], arms: list[str], case_ids: list[str]) -> dict:
    cells = {}
    for arm in arms:
        for case in case_ids:
            rows = [r for r in records if r["arm"] == arm and r["case"] == case]
            ran = [r for r in rows if "deterministic" in r]
            cells[f"{arm}/{case}"] = {"passed": sum(r["deterministic"]["passed"] for r in ran), "scored": len(ran),
                                      "planned": len(rows)}
    totals = {arm: {"passed": sum(c["passed"] for k, c in cells.items() if k.startswith(arm + "/")),
                    "scored": sum(c["scored"] for k, c in cells.items() if k.startswith(arm + "/"))} for arm in arms}
    return {"cells": cells, "totals": totals}


REPLY_EXCERPT_CHARS = 4000


def reply_excerpt(turns: list[dict]) -> str:
    reply = turns[-1]["final"] if turns else ""
    return reply if len(reply) <= REPLY_EXCERPT_CHARS else reply[:REPLY_EXCERPT_CHARS] + " [truncated]"


def results_rows(records: list[dict]) -> list[dict]:
    """Committable per-attempt rows: verdicts, failed assertions, move calls and the bounded final reply."""
    rows = []
    for record in records:
        row = {"arm": record["arm"], "case": record["case"], "repetition": record["repetition"], "status": record["status"]}
        if "deterministic" in record:
            row.update({"passed": record["deterministic"]["passed"],
                        "failedAssertions": [k for k, v in record["deterministic"]["assertions"].items() if not v],
                        "moves": [{k: m[k] for k in ("tool", "state", "transitionReason", "extraKeys", "ok", "unchanged", "error")}
                                  for m in record["moves"]],
                        "finalReply": reply_excerpt(record["turns"])})
        rows.append(row)
    return rows


def write_report(output: Path, manifest: dict) -> None:
    arms, case_ids = manifest["armNames"], manifest["caseIds"]
    lines = ["# Deal stage-move comparison (issue #4843)", "",
             f"Status: **{manifest['status']}**. Halted: {manifest.get('halted') or 'no'}.",
             "Scope: simulated prompt/tool-choice evidence; not Platform integration or deployed proof.", "",
             "| Case | " + " | ".join(arms) + " |", "|---|" + "---|" * len(arms)]
    for case in case_ids:
        cols = [f"{manifest['summary']['cells'][f'{arm}/{case}']['passed']}/{manifest['summary']['cells'][f'{arm}/{case}']['scored']}"
                for arm in arms]
        lines.append(f"| {case} | " + " | ".join(cols) + " |")
    lines.append("| **total** | " + " | ".join(
        f"**{manifest['summary']['totals'][a]['passed']}/{manifest['summary']['totals'][a]['scored']}**" for a in arms) + " |")
    lines += ["", f"Spend: {json.dumps(manifest['spend'])}", "",
              "Read the saved final replies as well; reply checks are regexes, not a semantic judge."]
    (output / "report.md").write_text("\n".join(lines) + "\n")


def rescore(directory: Path) -> dict:
    """Re-score a finished run's saved attempts with the current expectations and scorer. No provider access."""
    expectations, cases = yaml.safe_load(EXPECTATIONS.read_text()), yaml.safe_load(CASES.read_text())
    records = []
    for path in sorted(directory.glob("attempts/*/attempt.json")):
        record = json.loads(path.read_text())
        if record["status"] in {"completed", "incomplete"}:
            record["deterministic"] = score(expectations, record["case"], record, cases)
        records.append(record)
    rows = results_rows(records)
    return {"scorer": "current", "attempts": rows,
            "totals": {arm: {"passed": sum(1 for r in rows if r["arm"] == arm and r.get("passed")),
                             "scored": sum(1 for r in rows if r["arm"] == arm and r.get("passed") is not None)}
                       for arm in sorted({r["arm"] for r in rows})}}


def preflight(args: argparse.Namespace, frozen: dict) -> dict:
    cases = frozen["cases"]
    arms = [a["name"] for a in frozen["arms"]]
    case_ids = [c["id"] for c in cases["cases"] if not args.case or c["id"] in args.case]
    reps = args.repetitions or cases["run"]["repetitions"]
    plan = plan_attempts([c for c in cases["cases"] if c["id"] in case_ids], arms, reps)
    limits = cases["run"]["limits"]
    turns = {c["id"]: len(c["turns"]) for c in cases["cases"]}
    problems = list(frozen["problems"])
    unknown = sorted(set(args.case or []) - {c["id"] for c in cases["cases"]})
    if unknown:
        problems.append(f"Unknown --case ids {unknown}")
    return {"identity": frozen["identity"], "armNames": arms, "caseIds": case_ids, "repetitions": reps,
            "attemptPlan": plan, "attempts": len(plan),
            "maxSubjectCalls": sum(turns[p["case"]] * limits["maxStepsPerTurn"] for p in plan), "limits": limits,
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
    base.write_json(output / "results.json", {"identity": frozen["identity"], "subject": run["subject"],
                                              "status": manifest["status"], "halted": halted, "spend": manifest["spend"],
                                              "summary": manifest["summary"], "attempts": results_rows(manifest["records"])})
    base.write_json(output / "run.json", {k: v for k, v in manifest.items() if k not in {"records", "summary"}})
    write_report(output, manifest)
    ledger.event("run_end", status=manifest["status"], spend=ledger.totals())
    return manifest


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--arm", action="append", default=[], metavar="NAME=REV[+stages]",
                        help="prompt arm; repeat for each arm (git revision or file:PATH, +stages adds the stage block)")
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
