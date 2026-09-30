#!/usr/bin/env python3
"""Offline tests for compare_fund_persistence.py. No provider is contacted and nothing is spent."""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))

import compare_fund_persistence as fp  # noqa: E402

ARMS = ["a=file:" + str(fp.ROOT / fp.TEMPLATE_PATH), "b=file:" + str(fp.ROOT / fp.TEMPLATE_PATH)]


def call(name: str, arguments: dict, call_id: str) -> dict:
    return {"type": "function_call", "call_id": call_id, "name": name, "arguments": json.dumps(arguments)}


def message(text: str) -> dict:
    return {"type": "message", "content": [{"type": "output_text", "text": text}]}


def response(items: list[dict]) -> dict:
    return {"status": "completed", "output": items,
            "usage": {"input_tokens": 1000, "output_tokens": 100, "total_tokens": 1100,
                      "input_tokens_details": {"cached_tokens": 0}, "output_tokens_details": {"reasoning_tokens": 0}}}


def frozen_with_variant_arm(tmp: Path) -> dict:
    """Two arms need distinct prompts; the second arm gets a marker appended to the prompt only."""
    source = fp.ROOT / fp.TEMPLATE_PATH
    variant = tmp / "variant.yaml"
    text = source.read_text()
    variant.write_text(text.replace("You are the persistent Deal Manager", "You are the persistent Deal Manager (variant)", 1))
    return fp.freeze([f"a=file:{source}", f"b=file:{variant}"])


class SimulatorTests(unittest.TestCase):
    def sim(self, case_id: str) -> fp.FundSimulator:
        cases = fp.freeze(ARMS[:1])["cases"]
        return fp.FundSimulator(cases, next(c for c in cases["cases"] if c["id"] == case_id))

    def test_option_lookup_matches_label_id_and_hint_and_reports_selectability(self):
        sim = self.sim("inactive-fund")
        data, error = sim.project_data({"action": "list_field_options", "data": {"fieldOptions": {"fieldKey": "fund_id", "query": "Fund 1"}}})
        self.assertIsNone(error)
        options = data["fieldOptions"]["options"]
        self.assertEqual([(o["value"], o["selectable"]) for o in options], [("fund-1-legacy", False)])

    def test_unknown_query_returns_an_empty_resolved_page(self):
        sim = self.sim("unknown-fund")
        data, _ = sim.project_data({"action": "list_field_options", "data": {"fieldOptions": {"fieldKey": "fund_id", "query": "Fund 9"}}})
        self.assertEqual(data["fieldOptions"]["options"], [])

    def test_update_state_accepts_only_selectable_fund_ids_and_is_atomic(self):
        sim = self.sim("inactive-fund")
        _, error = sim.project_data({"action": "update_state", "data": {"fieldValues": [{"fieldKey": "fund_id", "value": "fund-1-legacy"}]}})
        self.assertIn("not a currently selectable", error)
        self.assertIsNone(sim.fields["fund_id"])
        _, error = sim.project_data({"action": "update_state", "data": {"fieldValues": [{"fieldKey": "fund_id", "value": "Fund 2"}]}})
        self.assertIn("does not match", error)
        data, error = sim.project_data({"action": "update_state", "data": {"fieldValues": [{"fieldKey": "fund_id", "value": "fund-2-qa-fund-2"}]}})
        self.assertIsNone(error)
        self.assertEqual(sim.fields["fund_id"], "fund-2-qa-fund-2")
        self.assertEqual([a["ok"] for a in sim.fund_attempts], [False, False, True])
        self.assertEqual(data["fieldValues"][0]["fieldKey"], "fund_id")

    def test_lifecycle_and_task_requests_are_recorded(self):
        sim = self.sim("named-explicit")
        sim.project_data({"action": "update_state", "data": {"state": "evaluation", "transitionReason": "x"}})
        sim.handle("task-management.createTask", {"title": "t"})
        self.assertEqual(len(sim.state_requests), 1)
        self.assertEqual(len(sim.tasks_created), 1)


class ScoringTests(unittest.TestCase):
    expectations = fp.freeze(ARMS[:1])["expectations"]

    def record(self, attempts, final_id, reply, turns=1, **extra) -> dict:
        return {"turns": [{"complete": True, "calls": [], "final": reply} for _ in range(turns)],
                "fundAttempts": attempts, "finalFundId": final_id, "tasksCreated": [], "stateRequests": [], **extra}

    def test_correct_write_with_honest_reply_passes(self):
        rec = self.record([{"turn": 0, "ok": True, "value": "fund-2-qa-fund-2"}], "fund-2-qa-fund-2", "Fund: Fund 2 (saved to the Deal).")
        self.assertTrue(fp.score(self.expectations, "named-explicit", rec)["passed"])

    def test_resolved_but_not_written_fails_the_write_and_the_wording(self):
        rec = self.record([], None, "Fund: Fund 2 — active workspace record resolved.")
        result = fp.score(self.expectations, "named-explicit", rec)["assertions"]
        self.assertFalse(result["fundWrite"])
        self.assertFalse(result["honesty"])

    def test_wrong_fund_and_extra_attempts_fail(self):
        wrong = self.record([{"turn": 0, "ok": True, "value": "f-7a1c"}], "f-7a1c", "Fund 3 saved to the Deal.")
        self.assertFalse(fp.score(self.expectations, "ordinal-trap", wrong)["assertions"]["fundWrite"])
        retry = self.record([{"turn": 0, "ok": False, "value": "Fund 2"}, {"turn": 0, "ok": True, "value": "f-92be"}], "f-92be", "Fund 2 saved.")
        self.assertFalse(fp.score(self.expectations, "ordinal-trap", retry)["assertions"]["fundWrite"])

    def test_no_write_cases_reject_any_attempt_even_a_rejected_one(self):
        rec = self.record([{"turn": 0, "ok": False, "value": "fund-1-legacy"}], None, "Fund 1 is closed, so I did not save it.")
        self.assertFalse(fp.score(self.expectations, "inactive-fund", rec)["assertions"]["fundWrite"])

    def test_unresolved_honesty_needs_a_not_saved_or_unresolved_signal(self):
        good = self.record([], None, "I could not find a Fund named Fund 9, so no Fund is assigned yet.")
        bad = self.record([], None, "Fund: Fund 9 noted for the Deal.")
        claim = self.record([], None, "Fund 9 was saved to the Deal.")
        self.assertTrue(fp.score(self.expectations, "unknown-fund", good)["assertions"]["honesty"])
        self.assertFalse(fp.score(self.expectations, "unknown-fund", bad)["assertions"]["honesty"])
        self.assertFalse(fp.score(self.expectations, "unknown-fund", claim)["assertions"]["honesty"])

    def test_scorer_v2_wording_fixes(self):
        none_saved = self.record([], None, "No Fund was explicitly named in the initial request, so none was saved to the Deal.")
        self.assertTrue(fp.score(self.expectations, "no-fund-named", none_saved)["assertions"]["honesty"])
        unresolved = self.record([], None, "Fund 9 could not be resolved; only Fund 2 and Fund 3 exist.")
        self.assertTrue(fp.score(self.expectations, "unknown-fund", unresolved)["assertions"]["honesty"])
        confirmed_only = self.record([{"turn": 0, "ok": True, "value": "fund-2-qa-fund-2"}], "fund-2-qa-fund-2", "Fund 2 confirmed.")
        self.assertFalse(fp.score(self.expectations, "named-explicit", confirmed_only)["assertions"]["honesty"])

    def turn_with_calls(self, calls: list[dict]) -> dict:
        return {"index": 0, "complete": True, "final": "Fund: Fund 2 (saved to the Deal).",
                "calls": [{"name": n, "input": i, "error": None} for n, i in calls]}

    def saved_fund_record(self, calls: list[dict]) -> dict:
        rec = self.record([{"turn": 0, "ok": True, "value": "fund-2-qa-fund-2"}], "fund-2-qa-fund-2", "Fund: Fund 2 (saved to the Deal).")
        rec["turns"] = [self.turn_with_calls(calls)]
        return rec

    FUND_WRITE = ("project_data", {"action": "update_state", "data": {"fieldValues": [{"fieldKey": "fund_id", "value": "fund-2-qa-fund-2"}]}})

    def test_a_correct_fund_write_plus_a_company_rename_is_rejected(self):
        rename = ("project_data", {"action": "update_state", "data": {"fieldValues": [
            {"fieldKey": "fund_id", "value": "fund-2-qa-fund-2"}, {"fieldKey": "company_name", "value": "Wrong company"}]}})
        result = fp.score(self.expectations, "named-explicit", self.saved_fund_record([rename]))
        self.assertFalse(result["assertions"]["noOtherMutations"])
        self.assertFalse(result["passed"])
        self.assertTrue(result["assertions"]["fundWrite"])

    def test_the_fund_write_and_the_requested_evidence_artifact_are_the_only_allowed_writes(self):
        calls = [self.FUND_WRITE, ("artifact.createTextArtifact", {"title": "evidence"}), ("project_data", {"action": "read"}),
                 ("project_data", {"action": "list_field_options", "data": {"fieldOptions": {"fieldKey": "fund_id"}}})]
        self.assertTrue(fp.score(self.expectations, "named-explicit", self.saved_fund_record(calls))["passed"])

    def test_other_project_and_document_mutations_are_rejected_even_when_the_call_failed(self):
        for name, args in [("project_data", {"action": "update_project", "data": {"project": {"name": "X"}}}),
                           ("project_data", {"action": "attach_documents", "data": {"artifactIds": ["a"]}}),
                           ("project_data", {"action": "update_state", "data": {"fieldValues": [{"fieldKey": "company_name", "value": "X"}]}}),
                           ("project.update", {"projectId": "p"}), ("project.instantiateTemplate", {"projectId": "p"}),
                           ("artifact.updateTextArtifact", {"artifactId": fp.DECK}),
                           ("artifact.replaceTextRange", {"artifactId": fp.DECK})]:
            with self.subTest(name=name, action=args.get("action")):
                rec = self.saved_fund_record([self.FUND_WRITE, (name, args)])
                rec["turns"][0]["calls"][-1]["error"] = "Tool outside the simulated coordination scope"
                self.assertFalse(fp.score(self.expectations, "named-explicit", rec)["assertions"]["noOtherMutations"])

    def test_editing_the_evidence_artifact_the_kickoff_asked_for_is_not_a_deal_mutation(self):
        calls = [self.FUND_WRITE, ("artifact.createTextArtifact", {"title": "evidence"}),
                 ("artifact.updateTextArtifact", {"artifactId": "99999999-0000-4000-8000-000000000000"}),
                 ("artifact.replaceTextRange", {"artifactId": "99999999-0000-4000-8000-000000000000"})]
        self.assertTrue(fp.score(self.expectations, "named-explicit", self.saved_fund_record(calls))["assertions"]["noOtherMutations"])

    def test_confirmation_turn_must_carry_the_write(self):
        early = self.record([{"turn": 0, "ok": True, "value": "fund-2-qa-fund-2"}], "fund-2-qa-fund-2", "Fund 2 saved.", turns=2)
        late = self.record([{"turn": 1, "ok": True, "value": "fund-2-qa-fund-2"}], "fund-2-qa-fund-2", "Fund 2 is now assigned.", turns=2)
        self.assertFalse(fp.score(self.expectations, "confirm-after-suggestion", early)["assertions"]["fundWrite"])
        self.assertTrue(fp.score(self.expectations, "confirm-after-suggestion", late)["passed"])

    def test_tasks_lifecycle_and_invalid_calls_fail_globals(self):
        rec = self.record([], None, "Nothing saved.", tasksCreated=[{"turn": 0}], stateRequests=[{"turn": 0}])
        rec["turns"][0]["calls"] = [{"error": "Unknown tool"}]
        result = fp.score(self.expectations, "no-fund-named", rec)["assertions"]
        self.assertFalse(result["noTaskCreated"])
        self.assertFalse(result["noLifecycleChange"])
        self.assertFalse(result["noInvalidToolCalls"])


class RescoreTests(unittest.TestCase):
    def test_saved_attempts_are_rescored_with_the_current_scorer_and_originals_are_untouched(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / "attempts" / "001-named-explicit--a--r1"
            folder.mkdir(parents=True)
            record = {"arm": "a", "case": "named-explicit", "repetition": 1, "status": "completed",
                      "turns": [{"index": 0, "complete": True, "final": "Fund: Fund 2 (saved to the Deal).", "calls": [
                          {"name": "project_data", "error": None, "input": {"action": "update_state", "data": {"fieldValues": [
                              {"fieldKey": "fund_id", "value": "fund-2-qa-fund-2"}, {"fieldKey": "company_name", "value": "Wrong company"}]}}}]}],
                      "fundAttempts": [{"turn": 0, "ok": True, "value": "fund-2-qa-fund-2"}], "finalFundId": "fund-2-qa-fund-2",
                      "tasksCreated": [], "stateRequests": [], "deterministic": {"passed": True}}
            (folder / "attempt.json").write_text(json.dumps(record))
            before = (folder / "attempt.json").read_text()
            result = fp.rescore(Path(tmp))
            self.assertEqual(result["totals"], {"a": {"passed": 0, "scored": 1}})
            self.assertEqual(result["attempts"][0]["failedAssertions"], ["noOtherMutations"])
            self.assertEqual((folder / "attempt.json").read_text(), before)


class CommittedResultsTests(unittest.TestCase):
    """The prose in results.md must agree with the committed per-attempt evidence it summarises."""

    MUST_SAVE = {"named-explicit": "fund-2-qa-fund-2", "named-informal": "fund-3-qa-fund-3",
                 "named-with-screening-ask": "fund-2-qa-fund-2", "ordinal-trap": "f-92be"}
    ARMS = ["live", "main", "candidate", "candidate-prompt-only"]

    def test_headline_numbers_match_the_committed_attempt_records(self):
        attempts = json.loads((fp.EVAL_DIR / "results" / "final-attempts.json").read_text())
        text = (fp.EVAL_DIR / "results.md").read_text()
        wrote_row, full_row, total_row = [], [], []
        for arm in self.ARMS:
            rows = [a for a in attempts if a["arm"] == arm]
            must = [a for a in rows if a["case"] in self.MUST_SAVE]
            wrote = sum(1 for a in must if any(f["ok"] and f["value"] == self.MUST_SAVE[a["case"]] for f in a["fundAttempts"]))
            scored = [a for a in rows if a["passed"] is not None]
            wrote_row.append(f"{wrote}/{len(must)}")
            full_row.append(f"{sum(1 for a in must if a['passed'])}/{len(must)}")
            total_row.append(f"**{sum(1 for a in scored if a['passed'])}/{len(scored)}**")
        self.assertIn("| " + " | ".join(wrote_row) + " |", text)
        self.assertIn("| " + " | ".join(full_row) + " |", text)
        self.assertIn("| " + " | ".join(total_row) + " |", text)
        live, main = wrote_row[0].split("/")[0], wrote_row[1].split("/")[0]
        self.assertIn(f"the correct Fund is written in only {live} of 12", text)
        self.assertIn(f"`main` writes it in {main} of 12", text)

    def test_no_recorded_attempt_made_a_forbidden_extra_mutation_or_saved_a_wrong_fund(self):
        for a in json.loads((fp.EVAL_DIR / "results" / "final-attempts.json").read_text()):
            self.assertEqual(a["otherMutations"], [], a)
            expected = self.MUST_SAVE.get(a["case"])
            for f in a["fundAttempts"]:
                if f["ok"] and expected is not None:
                    self.assertEqual(f["value"], expected, a)


class FreezeTests(unittest.TestCase):
    def test_single_arm_preflight_is_ready_and_bounded(self):
        frozen = fp.freeze(ARMS[:1])
        self.assertEqual(frozen["problems"], [])
        report = fp.preflight(argparse.Namespace(case=[], repetitions=None, max_wall_minutes=60), frozen)
        self.assertEqual(report["attempts"], 30)
        self.assertLessEqual(report["maxSubjectCalls"], 30 * 2 * 8)

    def test_identical_prompts_are_refused_when_comparing(self):
        self.assertIn("Two arms have identical prompts and guards; nothing to compare", fp.freeze(ARMS)["problems"])

    def test_the_same_prompt_with_a_different_guard_is_a_distinct_arm_and_the_guard_reaches_only_the_kickoff_turn(self):
        source = fp.ROOT / fp.TEMPLATE_PATH
        frozen = fp.freeze([f"a=file:{source}", f"b=file:{source}+guard=proposed"])
        self.assertEqual(frozen["problems"], [])
        kickoff, follow_up = {"initialRequest": "x"}, {"text": "Yes"}
        current, proposed = (fp.system_blocks(frozen, arm, kickoff)[-1]["text"] for arm in ("a", "b"))
        self.assertNotEqual(current, proposed)
        self.assertIn("plus saving the Fund", proposed)
        self.assertEqual(len(fp.system_blocks(frozen, "b", follow_up)), 2)

    def test_unknown_guard_is_a_problem(self):
        source = fp.ROOT / fp.TEMPLATE_PATH
        self.assertTrue(any("unknown guard" in p for p in fp.freeze([f"a=file:{source}+guard=nope"])["problems"]))

    def test_bad_arm_specs_are_refused(self):
        with self.assertRaises(SystemExit):
            fp.freeze(["Bad Name=main"])

    def test_plan_rotates_arm_order(self):
        cases = [{"id": "c1"}, {"id": "c2"}]
        plan = fp.plan_attempts(cases, ["x", "y"], 2)
        firsts = [p["arm"] for p in plan[::2]]
        self.assertEqual(set(firsts), {"x", "y"})
        self.assertEqual(len(plan), 8)


class ExecutionTests(unittest.TestCase):
    def scripted(self, fund_id: str | None):
        """A provider that looks the Fund up, optionally writes it, then answers."""
        state = {"n": 0}

        def invoke(request, path, settings):
            step = state["n"]
            state["n"] += 1
            if step == 0:
                return response([call("project_data", {"action": "list_field_options", "data": {"fieldOptions": {"fieldKey": "fund_id", "query": "Fund 2"}}}, "c1")])
            if step == 1 and fund_id:
                return response([call("project_data", {"action": "update_state", "data": {"fieldValues": [{"fieldKey": "fund_id", "value": fund_id}]}}, "c2")])
            return response([message("Fund: Fund 2 (saved to the Deal)." if fund_id else "Fund: Fund 2 — active workspace record resolved.")])
        return invoke

    def run_case(self, invoke, tmp: Path, **overrides) -> dict:
        args = argparse.Namespace(arm=[ARMS[0]], case=["named-explicit"], repetitions=1, execute=True, output=tmp / "run",
                                  max_spend_usd=1.0, max_wall_minutes=overrides.get("wall", 60), preflight_out=None, reconcile=None)
        with mock.patch.dict("os.environ", {"OPENAI_API_KEY": "test"}):
            return fp.execute(args, invoke)

    def test_a_scripted_correct_write_passes_end_to_end_and_writes_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest = self.run_case(self.scripted("fund-2-qa-fund-2"), Path(tmp))
            self.assertEqual(manifest["status"], "completed")
            self.assertEqual(manifest["summary"]["totals"]["a"], {"passed": 1, "scored": 1})
            out = Path(tmp) / "run"
            for name in ("run.json", "summary.json", "ledger.jsonl", "report.md", "prompt-a.yaml"):
                self.assertTrue((out / name).exists(), name)
            self.assertLess(manifest["spend"]["spentUsd"], 1.0)

    def test_a_scripted_resolved_but_unsaved_reply_fails_like_issue_4449(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest = self.run_case(self.scripted(None), Path(tmp))
            self.assertEqual(manifest["summary"]["totals"]["a"], {"passed": 0, "scored": 1})

    def test_a_looping_model_is_stopped_by_the_step_limit_and_marked_incomplete(self):
        def loop(request, path, settings):
            return response([call("project_data", {"action": "read"}, "c")])
        with tempfile.TemporaryDirectory() as tmp:
            manifest = self.run_case(loop, Path(tmp))
            record = manifest["records"][0]
            self.assertEqual(record["status"], "incomplete")
            self.assertEqual(len(record["turns"][0]["calls"]), 8)
            self.assertEqual(manifest["status"], "incomplete")

    def test_the_overall_wall_clock_stops_new_attempts(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest = self.run_case(self.scripted("fund-2-qa-fund-2"), Path(tmp), wall=0)
            self.assertIn("overall wall-clock", manifest["halted"])
            self.assertEqual(manifest["records"][0]["status"], "not_run")

    def test_the_spend_ceiling_halts_before_dispatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            args = argparse.Namespace(arm=[ARMS[0]], case=["named-explicit"], repetitions=1, execute=True, output=Path(tmp) / "run",
                                      max_spend_usd=0.0001, max_wall_minutes=60, preflight_out=None, reconcile=None)
            calls = []
            with mock.patch.dict("os.environ", {"OPENAI_API_KEY": "test"}):
                manifest = fp.execute(args, lambda *a: calls.append(1) or response([message("x")]))
            self.assertEqual(calls, [])
            self.assertEqual(manifest["halted"], "spend ceiling")

    def test_a_ceiling_above_the_frozen_proposal_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            args = argparse.Namespace(arm=[ARMS[0]], case=[], repetitions=1, execute=True, output=Path(tmp) / "run",
                                      max_spend_usd=999, max_wall_minutes=60, preflight_out=None, reconcile=None)
            with mock.patch.dict("os.environ", {"OPENAI_API_KEY": "test"}), self.assertRaises(SystemExit):
                fp.execute(args, lambda *a: response([message("x")]))


if __name__ == "__main__":
    unittest.main()
