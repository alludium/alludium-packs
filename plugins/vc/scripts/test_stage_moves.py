#!/usr/bin/env python3
"""Offline tests for compare_stage_moves.py. No provider is contacted and nothing is spent."""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))

import compare_stage_moves as sm  # noqa: E402
from evaluate_deal_manager import ROOT  # noqa: E402

TEMPLATE = ROOT / sm.TEMPLATE_PATH
ARMS = [f"candidate=file:{TEMPLATE}+stages", f"prompt-only=file:{TEMPLATE}"]


def call(name: str, arguments: dict, call_id: str) -> dict:
    return {"type": "function_call", "call_id": call_id, "name": name, "arguments": json.dumps(arguments)}


def message(text: str) -> dict:
    return {"type": "message", "content": [{"type": "output_text", "text": text}]}


def response(items: list[dict]) -> dict:
    return {"status": "completed", "output": items,
            "usage": {"input_tokens": 1000, "output_tokens": 100, "total_tokens": 1100,
                      "input_tokens_details": {"cached_tokens": 0}, "output_tokens_details": {"reasoning_tokens": 0}}}


def frozen() -> dict:
    return sm.freeze(ARMS)


def case(frozen_inputs: dict, case_id: str) -> dict:
    return next(c for c in frozen_inputs["cases"]["cases"] if c["id"] == case_id)


def record(moves: list[dict], reply: str, **extra) -> dict:
    base = {"status": "completed", "turns": [{"calls": [], "final": reply, "complete": True}], "moves": moves,
            "fieldWrites": [], "tasks": [], "created": [], "projectsCreated": []}
    base.update(extra)
    return base


def move(state: str, ok: bool = True, reason: str | None = None, unchanged: bool = False) -> dict:
    return {"turn": 0, "tool": "project_data.update_state", "state": state, "transitionReason": reason, "extraKeys": [],
            "ok": ok, "error": None if ok else "refused", "unchanged": unchanged}


class SimulatorTests(unittest.TestCase):
    def sim(self, case_id: str) -> sm.StageSimulator:
        inputs = frozen()
        return sm.StageSimulator(inputs["cases"], case(inputs, case_id))

    def test_forward_move_by_key_changes_state_and_reports_activity(self):
        sim = self.sim("reported-phrase")
        data, error = sim.project_data({"action": "update_state", "data": {"state": "decision"}})
        self.assertIsNone(error)
        self.assertEqual(sim.state, "decision")
        self.assertEqual(data["project"]["state"], "decision")

    def test_label_and_unknown_states_are_refused_without_change(self):
        sim = self.sim("reported-phrase")
        for state in ("Decision", "decision_review", "Diligence"):
            _, error = sim.project_data({"action": "update_state", "data": {"state": state}})
            self.assertEqual(error, sm.UNDEFINED_STATE_ERROR)
        self.assertEqual(sim.state, "screening")

    def test_repeat_into_current_stage_is_an_honest_no_op(self):
        sim = self.sim("already-there")
        data, error = sim.project_data({"action": "update_state", "data": {"state": "decision"}})
        self.assertIsNone(error)
        self.assertTrue(data["stateUnchanged"])
        self.assertEqual(data["activityEvents"], [])

    def test_backward_move_needs_a_reason(self):
        sim = self.sim("backtrack-with-reason")
        _, error = sim.project_data({"action": "update_state", "data": {"state": "evaluation"}})
        self.assertEqual(error, sm.BACKWARD_ERROR)
        _, error = sim.project_data({"action": "update_state", "data": {"state": "evaluation", "transitionReason": "calls"}})
        self.assertIsNone(error)
        self.assertEqual(sim.state, "evaluation")

    def test_simulated_refusal_and_promotion_are_errors(self):
        sim = self.sim("refused-move")
        _, error = sim.project_data({"action": "update_state", "data": {"state": "decision"}})
        self.assertIn("Refresh and retry", error)
        self.assertEqual(sim.state, "screening")
        sim = self.sim("reported-phrase")
        _, error = sim.project_data({"action": "update_state", "data": {"state": "promoted_to_investment_execution"}})
        self.assertEqual(error, sm.PROMOTION_ERROR)

    def test_field_writes_tasks_and_direct_update_moves_are_recorded(self):
        sim = self.sim("reported-phrase")
        sim.project_data({"action": "update_state", "data": {"fieldValues": [{"fieldKey": "fund_id", "value": "x"}]}})
        sim.handle("task-management.createTask", {"title": "t"})
        _, error = sim.handle("project.update", {"id": "p", "data": {"state": "decision", "name": "x"}})
        self.assertEqual(len(sim.field_writes), 1)
        self.assertEqual(len(sim.tasks), 1)
        self.assertEqual(error, sm.WRONG_ROUTE_ERROR)
        self.assertEqual(sim.state, "screening")
        self.assertEqual((sim.moves[-1]["tool"], sim.moves[-1]["extraKeys"]), ("project.update", ["name"]))


    def test_every_wrong_route_stage_change_is_recorded_and_refused(self):
        attempts = [
            ("project_data", {"action": "update_project", "data": {"state": "decision"}}),
            ("project_data", {"action": "update_project", "data": {"project": {"state": "decision"}}}),
            ("project.update", {"id": "p", "data": {"name": "x"}, "state": "decision"}),
        ]
        for name, args in attempts:
            sim = self.sim("quoted-control")
            _, error = sim.handle(name, args)
            self.assertEqual(error, sm.WRONG_ROUTE_ERROR, args)
            self.assertEqual(len(sim.moves), 1, args)
            self.assertEqual(sim.state, "screening")

    def test_a_non_object_payload_is_an_invalid_call_not_a_crash(self):
        _, error = self.sim("reported-phrase").handle("project_data", {"action": "update_state", "data": "{}"})
        self.assertIn(error, sm.INVALID_CALL_ERRORS)


class ContextTests(unittest.TestCase):
    def test_stage_block_marks_only_the_current_state_and_matches_platform_wording(self):
        inputs = frozen()
        block = sm.stages_block(inputs["cases"], "decision")
        self.assertIn("- decision: Decision [current]", block)
        self.assertIn("- screening: Screening\n", block)
        self.assertIn("- passed: Passed (board column: Outcomes)\n", block)
        self.assertNotIn("{{", block)

    def test_only_stage_arms_get_the_block_and_only_agent_cases_get_the_guard(self):
        inputs = frozen()
        with_stages, without = inputs["arms"]
        reported, agent = case(inputs, "reported-phrase"), case(inputs, "agent-origin-control")
        self.assertEqual(len(sm.system_blocks(inputs, with_stages, reported, "screening")), 3)
        self.assertEqual(len(sm.system_blocks(inputs, without, reported, "screening")), 2)
        blocks = sm.system_blocks(inputs, without, agent, "screening")
        self.assertEqual(blocks[-1]["text"], sm.HANDOFF_GUARD)
        self.assertIn('"humanAuthorization": false', blocks[1]["text"])

    def test_labels_are_parsed_from_the_stage_block(self):
        labels = sm.labels(frozen()["cases"])
        self.assertEqual(labels["term_sheet"], "Term Sheet")
        self.assertEqual(labels["passed"], "Passed")
        self.assertEqual(len(labels), 7)


class ScoringTests(unittest.TestCase):
    def score(self, case_id: str, rec: dict) -> dict:
        inputs = frozen()
        return sm.score(inputs["expectations"], case_id, rec, inputs["cases"])

    def test_reported_phrase_passes_only_with_one_move_and_an_honest_reply(self):
        self.assertTrue(self.score("reported-phrase", record([move("decision")], "Done. Recurvia is now in Decision."))["passed"])
        asked = self.score("reported-phrase", record([], "Which decision section do you mean?"))
        self.assertFalse(asked["passed"])
        self.assertFalse(asked["assertions"]["moveToTarget"])

    def test_a_move_through_the_wrong_tool_or_with_extra_keys_fails(self):
        wrong = {**move("decision"), "tool": "project.update"}
        self.assertFalse(self.score("reported-phrase", record([wrong], "Recurvia is now in Decision."))["passed"])
        extra = {**move("decision"), "extraKeys": ["fieldValues"]}
        self.assertFalse(self.score("reported-phrase", record([extra], "Recurvia is now in Decision."))["passed"])

    def test_a_planned_or_negated_move_is_not_a_claim(self):
        self.assertFalse(sm.claims_move("I will move it to Decision once you confirm."))
        self.assertFalse(sm.claims_move("Recurvia was not moved."))
        self.assertTrue(sm.claims_move("Recurvia has moved to Decision."))

    def test_already_there_accepts_a_no_op_call_or_none(self):
        self.assertTrue(self.score("already-there", record([move("decision", unchanged=True)], "Recurvia is already in Decision."))["passed"])
        self.assertTrue(self.score("already-there", record([], "Recurvia is already in Decision."))["passed"])
        self.assertFalse(self.score("already-there", record([move("decision"), move("decision")], "Already in Decision."))["passed"])

    def test_backtrack_requires_a_reason(self):
        reply = "Moved Recurvia back to Evaluation."
        self.assertTrue(self.score("backtrack-with-reason", record([move("evaluation", reason="calls")], reply))["passed"])
        self.assertFalse(self.score("backtrack-with-reason", record([move("evaluation")], reply))["passed"])

    def test_refused_move_must_be_reported_as_not_moved(self):
        self.assertTrue(self.score("refused-move", record([move("decision", ok=False)], "Recurvia was not moved: the stage changed."))["passed"])
        self.assertFalse(self.score("refused-move", record([move("decision", ok=False)], "Recurvia is now in Decision."))["passed"])

    def test_controls_fail_on_any_move(self):
        for case_id in ("memo-edit-control", "unknown-stage-control", "grouped-column-control", "agent-origin-control",
                        "quoted-control"):
            self.assertFalse(self.score(case_id, record([move("decision")], "Moved it."))["passed"], case_id)

    def test_unknown_stage_question_must_list_real_stages(self):
        listed = "There is no Diligence stage. The stages are Screening, Evaluation, Decision, Term Sheet, Passed and Archived. Which one?"
        self.assertTrue(self.score("unknown-stage-control", record([], listed))["passed"])
        self.assertFalse(self.score("unknown-stage-control", record([], "Which stage?"))["passed"])

    def test_global_assertions_catch_side_effects(self):
        rec = record([move("decision")], "Recurvia is now in Decision.", tasks=[{"turn": 0}],
                     created=[{"filename": "Recurvia Decision Record.md"}])
        result = self.score("reported-phrase", rec)
        self.assertFalse(result["assertions"]["noTaskMutation"])
        self.assertFalse(result["assertions"]["noDecisionRecord"])


class PreflightTests(unittest.TestCase):
    def test_preflight_is_ready_and_bounded(self):
        args = argparse.Namespace(arm=ARMS, case=[], repetitions=None, max_wall_minutes=60)
        report = sm.preflight(args, frozen())
        self.assertTrue(report["ready"], report["blockingProblems"])
        self.assertEqual(report["attempts"], 12 * 2 * 3)

    def test_identical_arms_are_refused(self):
        self.assertTrue(sm.freeze([ARMS[0], ARMS[0].replace("candidate=", "other=")])["problems"])

    def test_bad_arm_specs_are_refused(self):
        with self.assertRaises(SystemExit):
            sm.parse_arm("Bad Name=HEAD")


class ExecutionTests(unittest.TestCase):
    def run_case(self, invoke, tmp: Path, case_id: str = "reported-phrase", wall: float = 60) -> dict:
        args = argparse.Namespace(arm=[ARMS[0]], case=[case_id], repetitions=1, execute=True, output=tmp / "run",
                                  max_spend_usd=1.0, max_wall_minutes=wall, preflight_out=None, reconcile=None)
        with mock.patch.dict("os.environ", {"OPENAI_API_KEY": "test"}):
            return sm.execute(args, invoke)

    def scripted(self, moves: bool):
        state = {"n": 0}

        def invoke(request, path, settings):
            step = state["n"]
            state["n"] += 1
            if step == 0 and moves:
                return response([call("project_data", {"action": "update_state", "data": {"state": "decision"}}, "c1")])
            return response([message("Recurvia is now in Decision." if moves else "Which decision section do you mean?")])
        return invoke

    def test_a_scripted_move_passes_end_to_end_and_writes_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest = self.run_case(self.scripted(True), Path(tmp))
            self.assertEqual(manifest["status"], "completed")
            self.assertEqual(manifest["summary"]["totals"]["candidate"], {"passed": 1, "scored": 1})
            out = Path(tmp) / "run"
            for name in ("run.json", "summary.json", "results.json", "ledger.jsonl", "report.md", "prompt-candidate.yaml"):
                self.assertTrue((out / name).exists(), name)
            results = json.loads((out / "results.json").read_text())
            self.assertEqual(results["attempts"][0]["moves"][0]["state"], "decision")

    def test_the_reported_clarification_fails_like_issue_4843(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest = self.run_case(self.scripted(False), Path(tmp))
            self.assertEqual(manifest["summary"]["totals"]["candidate"], {"passed": 0, "scored": 1})

    def test_the_stage_block_reaches_the_request(self):
        seen = []

        def invoke(request, path, settings):
            seen.append(json.dumps(request["input"]))
            return response([message("Which section?")])
        with tempfile.TemporaryDirectory() as tmp:
            self.run_case(invoke, Path(tmp))
        self.assertIn("Project Lifecycle Stages", seen[0])
        self.assertIn("screening: Screening [current]", seen[0])

    def test_a_looping_model_is_stopped_by_the_step_limit(self):
        def loop(request, path, settings):
            return response([call("project_data", {"action": "read"}, "c")])
        with tempfile.TemporaryDirectory() as tmp:
            manifest = self.run_case(loop, Path(tmp))
            self.assertEqual(manifest["records"][0]["status"], "incomplete")
            self.assertEqual(len(manifest["records"][0]["turns"][0]["calls"]), 8)

    def test_the_spend_ceiling_halts_before_dispatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            args = argparse.Namespace(arm=[ARMS[0]], case=["reported-phrase"], repetitions=1, execute=True,
                                      output=Path(tmp) / "run", max_spend_usd=0.0001, max_wall_minutes=60,
                                      preflight_out=None, reconcile=None)
            calls = []
            with mock.patch.dict("os.environ", {"OPENAI_API_KEY": "test"}):
                manifest = sm.execute(args, lambda *a: calls.append(1) or response([message("x")]))
            self.assertEqual(calls, [])
            self.assertEqual(manifest["halted"], "spend ceiling")

    def test_rescore_reads_saved_attempts_without_spend(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.run_case(self.scripted(True), Path(tmp))
            result = sm.rescore(Path(tmp) / "run")
            self.assertEqual(result["totals"]["candidate"], {"passed": 1, "scored": 1})


if __name__ == "__main__":
    unittest.main()
