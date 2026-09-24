#!/usr/bin/env python3
"""Offline checks for the paired Deal Manager prompt comparison; every provider is mocked."""
from __future__ import annotations

import hashlib
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import yaml

import compare_deal_manager_prompts as compare
import evaluate_deal_manager
from evaluate_deal_manager import DECK, PROJECT, TASK

HERE = Path(__file__).resolve().parent
PACK_DIR = HERE.parent / "alludium"
OLD, NEW = "old-rev", "new-rev"
NEW_SENTENCE = "Synthetic candidate sentence for offline tests only."
SUBJECT = "gpt-5.6-luna"
JUDGE = "global.anthropic.claude-opus-4-8"


def fake_show(revision: str, path: str) -> str:
    """Serve working-tree Pack files; the new revision differs only in one prompt sentence."""
    text = (PACK_DIR.parent / path.removeprefix("plugins/vc/")).read_text()
    if revision == NEW and path == compare.TEMPLATE_PATH:
        text = text.replace("## Turn Completion Contract", f"## Turn Completion Contract\n\n    {NEW_SENTENCE}", 1)
    return text


def fake_blob(revision: str, path: str) -> str:
    return hashlib.sha1(fake_show(revision, path).encode()).hexdigest()


class FakeGit:
    def __enter__(self):
        self.patches = [mock.patch.object(compare, "git_show", fake_show), mock.patch.object(compare, "git_blob", fake_blob),
                        mock.patch.object(compare, "resolve_commit", lambda revision: revision)]
        for patch in self.patches:
            patch.start()
        return self

    def __exit__(self, *exc):
        for patch in self.patches:
            patch.stop()


CALLS = {"n": 0}


def reply(text: str | None = None, tools: list[tuple[str, dict]] = (), status: str = "completed", tokens: int = 100,
          reason: str = "max_output_tokens") -> dict:
    """Responses API shape: an encrypted reasoning item, optional message, then function calls."""
    CALLS["n"] += 1
    n = CALLS["n"]
    output = [{"type": "reasoning", "id": f"rs_{n}", "encrypted_content": f"ENC-{n}", "summary": []}]
    if text:
        output.append({"type": "message", "id": f"msg_{n}", "role": "assistant", "status": "completed",
                       "content": [{"type": "output_text", "text": text, "annotations": []}]})
    output += [{"type": "function_call", "id": f"fc_{n}_{i}", "call_id": f"call_{n}_{i}", "name": name.replace(".", "_"),
                "arguments": json.dumps(params), "status": "completed"} for i, (name, params) in enumerate(tools)]
    response = {"id": f"resp_{n}", "object": "response", "status": status, "output": output,
                "usage": {"input_tokens": tokens, "input_tokens_details": {"cached_tokens": 0},
                          "output_tokens": tokens // 10, "output_tokens_details": {"reasoning_tokens": tokens // 20},
                          "total_tokens": tokens + tokens // 10}}
    if status == "incomplete":
        response["incomplete_details"] = {"reason": reason}
    return response


def judge_reply(text: str) -> dict:
    """Bedrock Converse shape for the Opus judge route."""
    return {"output": {"message": {"role": "assistant", "content": [{"text": text}]}}, "stopReason": "end_turn",
            "usage": {"inputTokens": 500, "outputTokens": 50, "totalTokens": 550}}


def user_texts(request: dict) -> list[str]:
    return [item["content"][0]["text"] for item in request["input"] if item.get("role") == "user"]


def create_screening(extra_input: dict | None = None) -> tuple[str, dict]:
    return ("task-management.createTask", {"projectId": PROJECT, "taskDefinitionId": compare.definition_id(compare.SCREENING),
                                           "title": "Screening Report", "instruction": "Screen Terraview; mark Fund fit unknown.",
                                           "input": {"company_name": "Terraview Analytics", **(extra_input or {})}})


class Policy:
    """Scripted subject. `fund_first` asks about the Fund on the first human turn, like the reported loop."""

    def __init__(self, fund_first: bool = False, duplicate_on_second_turn: bool = False):
        self.fund_first, self.duplicate = fund_first, duplicate_on_second_turn
        self.requests: list[dict] = []

    def __call__(self, request: dict, path: Path, settings: dict) -> dict:
        self.requests.append(request)
        items = request["input"]
        developer = [item for item in items if item.get("role") == "developer"]
        runtime = json.loads(developer[1]["content"][0]["text"].split("\n", 1)[1])
        human_turns = user_texts(request)
        if items[-1].get("type") == "function_call_output":
            results = []
            for item in reversed(items):
                if item.get("type") != "function_call_output":
                    break
                results.append(json.loads(item["output"]))
            receipt = next((r for r in results if "taskId" in r and "task" in r), None)
            if receipt:
                return reply(tools=[("task-management.getTaskDetail", {"taskId": receipt["taskId"]})])
            return reply("Screening is running with Fund fit marked unknown. Next: review the report when it lands.")
        text = human_turns[-1]
        if len(developer) > 2:
            return reply("Deal Analyst recommends a Screening Report. Do you approve starting it?")
        if "Term Sheet" in text:
            return reply("The Term Sheet Review needs the current term sheet. Could you upload it?")
        open_tasks = runtime["project"]["openTasks"]
        if open_tasks and not (self.duplicate and len(human_turns) > 1):
            return reply(tools=[("task-management.getTaskDetail", {"taskId": open_tasks[0]["id"]})])
        if self.fund_first and len(human_turns) == 1:
            return reply("Which Fund should this Deal sit in?")
        return reply(tools=[create_screening()])


def args_for(output: Path, **overrides) -> object:
    args = compare.parse_args(["--old-revision", OLD, "--new-revision", NEW, "--output", str(output), "--max-spend-usd", "10", "--execute"])
    for key, value in overrides.items():
        setattr(args, key, value)
    return args


class ComparisonTests(unittest.TestCase):
    def setUp(self):
        self.git = FakeGit().__enter__()
        self.tmp = tempfile.TemporaryDirectory()
        self.out = Path(self.tmp.name) / "run"

    def tearDown(self):
        self.git.__exit__()
        self.tmp.cleanup()

    def frozen(self) -> dict:
        return compare.load_frozen(OLD, NEW)

    def ledger(self, ceiling: float = 25, path: Path | None = None) -> compare.SpendLedger:
        return compare.SpendLedger(self.frozen()["cases"]["run"]["prices"], ceiling, path)

    def attempt(self, case_id: str, variant: str, invoke, ledger=None) -> dict:
        item = {"index": 1, "case": case_id, "variant": variant, "repetition": 1, "folder": f"attempts/{case_id}-{variant}"}
        return compare.run_attempt(self.frozen(), item, self.out, invoke, ledger or self.ledger(), {})

    # Preflight and frozen inputs -------------------------------------------------

    def test_preflight_makes_zero_provider_calls(self):
        def forbidden(*args, **kwargs):
            raise AssertionError("provider called during preflight")
        with mock.patch.object(compare, "bedrock_invoke", forbidden), mock.patch.object(compare, "openai_invoke", forbidden), \
                mock.patch.object(compare, "default_invoke", forbidden), mock.patch.object(compare, "call_provider", forbidden), \
                mock.patch.object(compare.urllib.request, "urlopen", forbidden):
            report = compare.preflight(compare.parse_args(["--old-revision", OLD, "--new-revision", NEW]))
        self.assertTrue(report["preparationReady"], report["blockingProblems"])
        self.assertEqual(0, report["providerCalls"])
        self.assertEqual({"cases": 6, "variants": 2, "repetitions": 3, "attempts": 36, "potentialJudgeCalls": 36},
                         {k: v for k, v in report["counts"].items() if k != "maxSubjectCalls"})
        self.assertGreater(report["cost"]["worstTotalPlatformBillableUsd"], report["cost"]["expectedTotalPlatformBillableUsd"])
        self.assertGreater(report["cost"]["expectedSubjectPlatformBillableUsd"], report["cost"]["expectedSubjectDirectProviderListUsd"])
        self.assertTrue(report["paidReady"])
        self.assertFalse(report["spendApproved"])

    def test_preflight_rejects_template_changes_beyond_the_prompt(self):
        def drifted(revision, path):
            text = fake_show(revision, path)
            return text.replace("WEB_SEARCH", "SANDBOX_EXECUTION") if revision == NEW and path == compare.TEMPLATE_PATH else text
        with mock.patch.object(compare, "git_show", drifted):
            self.assertIn("capabilityProfile", " ".join(compare.load_frozen(OLD, NEW)["problems"]))

    def test_preflight_rejects_misspelt_assertion_keys(self):
        text = compare.EXPECTATIONS.read_text().replace("readBackAfterCreate", "readbackAfterCreate", 1)
        with mock.patch.object(compare, "EXPECTATIONS", mock.Mock(read_text=lambda: text)):
            self.assertIn("unknown assertion keys", " ".join(compare.load_frozen(OLD, NEW)["problems"]))

    def test_preflight_rejects_identical_prompts(self):
        self.assertIn("identical", " ".join(compare.load_frozen(OLD, OLD)["problems"]))

    def test_preflight_detects_variant_dependent_context(self):
        frozen = self.frozen()
        requests = compare.first_requests(frozen)
        self.assertEqual([], compare.shared_input_problems(frozen, requests))
        requests[("existing-screening-task-reuse", "new")]["input"] = requests[("existing-screening-task-reuse", "new")]["input"][:-1] + [
            compare.message_item("user", "hint")]
        requests[("agent-origin-screening-recommendation", "old")]["input"] = [
            requests[("agent-origin-screening-recommendation", "old")]["input"][0], compare.message_item("developer", "different runtime"),
            *requests[("agent-origin-screening-recommendation", "old")]["input"][2:]]
        self.assertEqual(["existing-screening-task-reuse: variants differ outside the prompt block",
                          "agent-origin-screening-recommendation: variants differ outside the prompt block"],
                         compare.shared_input_problems(frozen, requests))

    def test_plan_interleaves_variants_with_unique_paths(self):
        plan = compare.plan_attempts(self.frozen()["cases"]["cases"], 3)
        self.assertEqual(36, len(plan))
        self.assertEqual(36, len({item["folder"] for item in plan}))
        firsts = [plan[i]["variant"] for i in range(0, 36, 2)]
        self.assertIn("old", firsts)
        self.assertIn("new", firsts)
        for i in range(0, 36, 2):
            self.assertEqual({"old", "new"}, {plan[i]["variant"], plan[i + 1]["variant"]})
            self.assertEqual(plan[i]["case"], plan[i + 1]["case"])

    def test_variants_share_every_input_except_the_prompt(self):
        requests = {}
        for variant in compare.VARIANTS:
            policy = Policy()
            self.attempt("screening-optional-gaps-single-turn", variant, policy)
            requests[variant] = policy.requests[0]
        old, new = requests["old"], requests["new"]
        self.assertNotEqual(old["input"][0], new["input"][0])
        self.assertIn(NEW_SENTENCE, new["input"][0]["content"][0]["text"])
        self.assertEqual(old["input"][1:], new["input"][1:])
        self.assertEqual({k: v for k, v in old.items() if k != "input"}, {k: v for k, v in new.items() if k != "input"})

    def test_expectations_and_rubric_never_reach_subject_requests(self):
        compare.execute(args_for(self.out), invoke=Policy())
        expectations = yaml.safe_load(compare.EXPECTATIONS.read_text())
        leaks = ["noBlockingQuestion", "readBackAfterCreate", "followsCorrection", "respectsGenuinePrerequisite",
                 *expectations["judge"]["situations"].values(), expectations["judge"]["instructions"]]
        requests = list((self.out / "attempts").rglob("*-request.json"))
        self.assertTrue(requests)
        for path in requests:
            text = path.read_text()
            for leak in leaks:
                self.assertNotIn(leak[:60], text, path.name)

    # Multi-turn behaviour ---------------------------------------------------------

    def test_second_turn_carries_full_history_and_current_state(self):
        policy = Policy(fund_first=True)
        record = self.attempt("screening-live-correction-two-turn", "old", policy)
        turn_two = next(r for r in policy.requests if len(user_texts(r)) == 2)
        texts = [item["content"][0]["text"] for item in turn_two["input"] if item.get("role") in ("user", "assistant")]
        self.assertTrue(texts[0].startswith("New deal: Terraview"))
        self.assertEqual("Which Fund should this Deal sit in?", texts[1])
        self.assertTrue(texts[2].startswith("Forget the Fund"))
        self.assertTrue(record["deterministic"]["passed"], record["deterministic"]["errors"])
        self.assertEqual(1, record["deterministic"]["firstCreateTurn"])

    def test_proceeding_on_first_turn_is_not_forced_to_duplicate(self):
        record = self.attempt("screening-live-correction-two-turn", "new", Policy())
        self.assertTrue(record["deterministic"]["passed"], record["deterministic"]["errors"])
        self.assertEqual(0, record["deterministic"]["firstCreateTurn"])
        self.assertEqual("task-management.getTaskDetail", record["turns"][1]["calls"][0]["name"])

    def test_duplicate_creation_after_correction_fails(self):
        record = self.attempt("screening-live-correction-two-turn", "new", Policy(duplicate_on_second_turn=True))
        self.assertIn("creates.total", " ".join(record["deterministic"]["errors"]))

    def test_frozen_prefix_is_labelled_and_precedes_live_turn(self):
        policy = Policy()
        record = self.attempt("screening-frozen-offer-then-yes", "old", policy)
        self.assertEqual("frozen-reconstructed", record["prefixKind"])
        self.assertEqual(["user", "assistant", "user"], [i["role"] for i in policy.requests[0]["input"] if i.get("role") != "developer"])
        self.assertEqual("Yes, please.", policy.requests[0]["input"][-1]["content"][0]["text"])
        self.assertTrue(record["deterministic"]["passed"], record["deterministic"]["errors"])

    def test_reopening_waived_fund_after_yes_fails(self):
        def reopen(request, path, settings):
            return reply("Before I start, which Fund should I use?")
        record = self.attempt("screening-frozen-offer-then-yes", "old", reopen)
        errors = " ".join(record["deterministic"]["errors"])
        self.assertIn("noQuestionAbout", errors)
        self.assertIn("creates.total", errors)

    # Controls and scorer failure injection ---------------------------------------

    def test_controls_pass_with_correct_behaviour(self):
        for case in ("term-sheet-review-required-input-insistence", "existing-screening-task-reuse",
                     "agent-origin-screening-recommendation", "screening-optional-gaps-single-turn"):
            record = self.attempt(case, "new", Policy())
            self.assertTrue(record["deterministic"]["passed"], (case, record["deterministic"]["errors"]))

    def test_term_sheet_insistence_substituting_the_deck_fails(self):
        steps = iter([reply(tools=[("task-management.createTask", {
            "projectId": PROJECT, "taskDefinitionId": compare.definition_id("review-refresh-term-sheet"), "title": "Term sheet",
            "instruction": "Review", "input": {"company_name": "Terraview Analytics", "current_term_sheet_artifact_id": DECK}})]),
            reply("I've started the Term Sheet Review.")])
        record = self.attempt("term-sheet-review-required-input-insistence", "new", lambda *a: next(steps))
        self.assertIn("does not reference", record["turns"][0]["calls"][0]["error"])
        errors = " ".join(record["deterministic"]["errors"])
        for rule in ("noFabricatedInputs", "creates.total", "asksAbout", "noInvalidToolCalls"):
            self.assertIn(rule, errors)

    def test_fabricated_fund_fails_even_when_task_is_created(self):
        steps = iter([reply(tools=[create_screening({"fund_id": "climate-fund-i"})]),
                      reply(tools=[("task-management.getTaskDetail", {"taskId": TASK})]), reply("Started.")])
        record = self.attempt("screening-optional-gaps-single-turn", "new", lambda *a: next(steps))
        self.assertEqual(["noFabricatedInputs: supplied a Fund or term sheet that does not exist"], record["deterministic"]["errors"])

    def test_missing_readback_and_agent_origin_creation_fail(self):
        steps = iter([reply(tools=[create_screening()]), reply("Started.")])
        record = self.attempt("screening-optional-gaps-single-turn", "new", lambda *a: next(steps))
        self.assertIn("readBackAfterCreate", " ".join(record["deterministic"]["errors"]))
        steps = iter([reply(tools=[create_screening()]), reply("Started the Screening Report.")])
        self.out = self.out / "second"
        record = self.attempt("agent-origin-screening-recommendation", "new", lambda *a: next(steps))
        errors = " ".join(record["deterministic"]["errors"])
        self.assertIn("creates.total", errors)
        self.assertIn("requestsHumanApproval", errors)

    def test_document_authoring_and_unknown_tools_fail(self):
        steps = iter([reply(tools=[("artifact.createTextArtifact", {"title": "Screening"}), ("crm.write", {})]), reply("Done.")])
        record = self.attempt("screening-optional-gaps-single-turn", "new", lambda *a: next(steps))
        errors = " ".join(record["deterministic"]["errors"])
        self.assertIn("noDocumentAuthoringWrites", errors)
        self.assertIn("noInvalidToolCalls", errors)

    def test_step_limit_is_incomplete_not_a_pass(self):
        record = self.attempt("screening-optional-gaps-single-turn", "new",
                              lambda *a: reply(tools=[("project-task.listByProject", {"projectId": PROJECT})]))
        self.assertEqual("incomplete", record["status"])
        self.assertEqual(8, len(record["turns"][0]["calls"]))
        self.assertIn("allTurnsComplete", " ".join(record["deterministic"]["errors"]))

    def test_max_tokens_stop_is_incomplete(self):
        record = self.attempt("screening-optional-gaps-single-turn", "new", lambda *a: reply("Partial", status="incomplete"))
        self.assertEqual("incomplete", record["status"])

    # Run-level retention, errors, budget and judging -------------------------------

    def test_provider_errors_are_retained_and_the_run_continues(self):
        policy = Policy()
        calls = {"n": 0}

        def flaky(request, path, settings):
            calls["n"] += 1
            if calls["n"] == 1:
                raise compare.ProviderError("ThrottlingException")
            return policy(request, path, settings)
        manifest = compare.execute(args_for(self.out), invoke=flaky)
        first = manifest["records"][0]
        self.assertEqual("provider_error", first["status"])
        self.assertTrue((self.out / first["folder"] / "provider-error.txt").exists())
        self.assertTrue((self.out / first["folder"] / "t0-s00-request.json").exists())
        self.assertEqual(35, sum(r["status"] == "completed" for r in manifest["records"]))
        self.assertEqual(36, len(list((self.out / "attempts").iterdir())))

    def test_consecutive_provider_errors_halt_remaining_attempts(self):
        def down(*args):
            raise compare.ProviderError("AccessDenied")
        manifest = compare.execute(args_for(self.out), invoke=down)
        self.assertEqual("consecutive provider errors", manifest["halted"])
        self.assertEqual(3, sum(r["status"] == "provider_error" for r in manifest["records"]))
        self.assertEqual(33, sum(r["status"] == "not_run" for r in manifest["records"]))

    def test_malformed_response_without_usage_stops_accounting(self):
        ledger = self.ledger()
        record = self.attempt("screening-optional-gaps-single-turn", "new", lambda *a: {"unexpected": True}, ledger)
        self.assertEqual("accounting_stop", record["status"])
        self.assertNotIn("deterministic", record)
        self.assertEqual(1, ledger.unreconciled)
        self.assertGreater(ledger.exposure, 0)

    def test_spend_ceiling_stops_before_the_next_call(self):
        manifest = compare.execute(args_for(self.out, max_spend_usd=0.5), invoke=lambda *a: reply("Which Fund?", tokens=40000))
        self.assertEqual("spend ceiling", manifest["halted"])
        self.assertLessEqual(manifest["spend"]["spentUsd"], 0.5)
        self.assertTrue(any(r["status"] == "not_run" for r in manifest["records"]))

    def test_ceiling_above_frozen_proposal_is_refused(self):
        with self.assertRaises(SystemExit):
            compare.execute(args_for(self.out, max_spend_usd=1000), invoke=Policy())

    def test_existing_output_directory_is_never_reused(self):
        self.out.mkdir(parents=True)
        with self.assertRaises(FileExistsError):
            compare.execute(args_for(self.out), invoke=Policy())

    def test_judge_input_is_blind_and_cannot_rescue_deterministic_failure(self):
        subject = Policy()
        judge_payloads = []

        def invoke(request, path, settings):
            if request.get("modelId") == JUDGE:
                payload = json.loads(request["messages"][0]["content"][0]["text"])
                judge_payloads.append(request)
                return judge_reply(json.dumps({"criteria": {c: {"score": 2, "rationale": "ok"} for c in payload["criteria"]}}))
            if "Term Sheet" in user_texts(request)[0]:
                return reply("I've started the Term Sheet Review.")
            return subject(request, path, settings)
        manifest = compare.execute(args_for(self.out, judge=True), invoke=invoke)
        self.assertEqual(36, len(judge_payloads))
        dumped = json.dumps(judge_payloads)
        for forbidden in ('"old"', '"new"', "variant", "deterministic", "Turn Completion Contract", "passed"):
            self.assertNotIn(forbidden, dumped)
        term = manifest["cells"]["term-sheet-review-required-input-insistence"]["new"]
        self.assertEqual(0, term["deterministicPass"])
        self.assertEqual([2, 2, 2], term["judgeScores"]["respectsGenuinePrerequisite"])

    def test_invalid_judge_output_is_a_judge_error(self):
        subject = Policy()

        def invoke(request, path, settings):
            if request.get("modelId") == JUDGE:
                return judge_reply("Looks fine to me.")
            return subject(request, path, settings)
        manifest = compare.execute(args_for(self.out, judge=True), invoke=invoke)
        self.assertTrue(all(r["judge"]["status"] == "judge_error" for r in manifest["records"]))
        self.assertTrue(all(r["deterministic"]["passed"] for r in manifest["records"]))

    def test_judge_not_run_is_distinct_from_judge_error(self):
        manifest = compare.execute(args_for(self.out), invoke=Policy())
        self.assertTrue(all("judge" not in r for r in manifest["records"]))
        self.assertIn("not_run", json.dumps(manifest["cells"]))


class Counting:
    """Wraps a provider; counts every dispatch so tests can prove nothing is sent after a stop."""

    def __init__(self, inner, fault=None):
        self.inner, self.fault, self.calls = inner, fault, 0

    def __call__(self, request, path, settings):
        self.calls += 1
        if self.fault:
            outcome = self.fault(self.calls, request)
            if outcome is not None:
                return outcome
        return self.inner(request, path, settings)


def oai_usage(inp, out, cached=0, reasoning=0, total=None):
    return {"input_tokens": inp, "input_tokens_details": {"cached_tokens": cached}, "output_tokens": out,
            "output_tokens_details": {"reasoning_tokens": reasoning},
            "total_tokens": total if total is not None else (inp + out if all(isinstance(v, int) for v in (inp, out)) else None)}


def with_usage(usage):
    response = reply("Which Fund should this Deal sit in?")
    if usage is None:
        response.pop("usage")
    else:
        response["usage"] = usage
    return response


class SpendAccountingTests(unittest.TestCase):
    def setUp(self):
        self.git = FakeGit().__enter__()
        self.tmp = tempfile.TemporaryDirectory()
        self.out = Path(self.tmp.name) / "run"
        self.prices = compare.load_frozen(OLD, NEW)["cases"]["run"]["prices"]

    def tearDown(self):
        self.git.__exit__()
        self.tmp.cleanup()

    def events(self) -> list[dict]:
        return [json.loads(line) for line in (self.out / "ledger.jsonl").read_text().splitlines()]

    def test_missing_or_invalid_usage_is_charged_and_stops_all_later_dispatch(self):
        bad = {"missing": None, "empty": {}, "negative": oai_usage(-1, 5), "string": oai_usage("900", 5),
               "boolean": oai_usage(True, 5), "zero input": oai_usage(0, 5), "missing output": {"input_tokens": 900},
               "total mismatch": oai_usage(900, 5, total=7), "cached above input": oai_usage(900, 5, cached=901),
               "reasoning above output": oai_usage(900, 5, reasoning=6)}
        for label, usage in bad.items():
            with self.subTest(label):
                self.out = Path(self.tmp.name) / label.replace(" ", "-")
                provider = Counting(Policy(), lambda n, r: with_usage(usage) if n == 1 else None)
                manifest = compare.execute(args_for(self.out, judge=True), invoke=provider)
                spend = manifest["spend"]
                self.assertEqual(1, provider.calls)
                self.assertEqual(1, spend["dispatchedCalls"])
                self.assertEqual(0, spend["settledCalls"])
                self.assertEqual(0, spend["confirmedUsd"])
                reserved = next(e["reservedUsd"] for e in self.events() if e["event"] == "reserve")
                self.assertAlmostEqual(reserved, spend["unreconciledExposureUsd"], places=6)
                self.assertEqual("accounting_stop", manifest["records"][0]["status"])
                self.assertEqual(35, sum(r["status"] == "not_run" for r in manifest["records"]))
                self.assertEqual("incomplete", manifest["executionStatus"])

    def test_halted_ledger_refuses_every_later_dispatch(self):
        ledger = compare.SpendLedger(self.prices, 25)
        request = compare.first_requests(compare.load_frozen(OLD, NEW))[("screening-optional-gaps-single-turn", "old")]
        self.out.mkdir(parents=True)
        provider = Counting(lambda *a: with_usage(None))
        with self.assertRaises(compare.AccountingStop):
            compare.call_provider(provider, ledger, "subject", "first", request, self.out / "a-request.json", {})
        for kind in ("subject", "judge"):
            with self.assertRaises(compare.AccountingStop):
                compare.call_provider(provider, ledger, kind, "later", request, self.out / f"{kind}-request.json", {})
        self.assertEqual(1, provider.calls)
        self.assertEqual(1, ledger.dispatched)

    def test_usage_above_the_reserved_bound_is_counted_and_halts(self):
        provider = Counting(Policy(), lambda n, r: with_usage(oai_usage(900, 200000)) if n == 1 else None)
        manifest = compare.execute(args_for(self.out), invoke=provider)
        self.assertEqual(1, provider.calls)
        self.assertIn("exceeded its reservation bounds", manifest["halted"])
        self.assertAlmostEqual((900 * 0.26 + 200000 * 1.56) / 1e6, manifest["spend"]["confirmedUsd"], places=6)
        self.assertEqual(["bound_violation"], [e["event"] for e in self.events() if e["event"] == "bound_violation"])

    def test_timeout_after_submission_keeps_its_reservation_as_exposure(self):
        def fault(n, request):
            if n == 1:
                raise compare.subprocess.TimeoutExpired("aws", 135)
        provider = Counting(Policy(), fault)
        manifest = compare.execute(args_for(self.out), invoke=provider)
        spend = manifest["spend"]
        self.assertEqual("provider_error", manifest["records"][0]["status"])
        self.assertEqual(1, spend["unreconciledCalls"])
        exposure = next(e for e in self.events() if e["event"] == "exposure")
        self.assertEqual(1, exposure["callId"])
        self.assertAlmostEqual(exposure["chargedUsd"], spend["unreconciledExposureUsd"], places=6)
        self.assertAlmostEqual(spend["spentUsd"], spend["confirmedUsd"] + spend["unreconciledExposureUsd"], places=5)
        self.assertEqual(spend["dispatchedCalls"], provider.calls)
        self.assertEqual("incomplete", manifest["executionStatus"])

    def test_exhausted_reservations_stop_before_dispatch(self):
        first = compare.SpendLedger(self.prices, 25)
        request = compare.first_requests(compare.load_frozen(OLD, NEW))[("screening-optional-gaps-single-turn", "old")]
        reservation = compare.usd(self.prices["platformBillable"]["usdPerMillionTokens"][SUBJECT],
                                  {"inputTokens": compare.input_token_bound(request), "cachedInputTokens": 0,
                                   "outputTokens": compare.output_token_bound(request)})
        del first
        # Room for two failed calls' reservations but not a third.
        ceiling = round(reservation * 2.5, 4)

        def down(n, r):
            raise compare.ProviderError("ServiceUnavailable")
        provider = Counting(Policy(), down)
        manifest = compare.execute(args_for(self.out, max_spend_usd=ceiling), invoke=provider)
        self.assertEqual(2, provider.calls)
        self.assertEqual("spend ceiling", manifest["halted"])
        self.assertLessEqual(manifest["spend"]["spentUsd"], ceiling)
        self.assertEqual(0, manifest["spend"]["confirmedUsd"])
        self.assertEqual("budget_stop", manifest["records"][2]["status"])

    def test_first_reservation_larger_than_ceiling_dispatches_nothing(self):
        provider = Counting(Policy())
        manifest = compare.execute(args_for(self.out, max_spend_usd=0.01), invoke=provider)
        self.assertEqual(0, provider.calls)
        self.assertEqual(0, manifest["spend"]["dispatchedCalls"])
        self.assertEqual("incomplete", manifest["executionStatus"])

    def test_invalid_ceilings_and_prices_are_refused(self):
        for ceiling in (float("nan"), float("inf"), 0, -1, "5", True, None):
            with self.subTest(ceiling=ceiling):
                with self.assertRaises(ValueError):
                    compare.SpendLedger(self.prices, ceiling)
        for ceiling in (float("nan"), float("inf"), 0, -3):
            with self.subTest(execute_ceiling=ceiling), self.assertRaises(SystemExit):
                compare.execute(args_for(Path(self.tmp.name) / f"c{ceiling}", max_spend_usd=ceiling), invoke=Counting(Policy()))
        broken = {"negative": -1, "nan": float("nan"), "zero": 0, "missing": None, "below direct": 0.1}
        for label, value in broken.items():
            with self.subTest(price=label):
                prices = json.loads(json.dumps(self.prices))
                rate = prices["platformBillable"]["usdPerMillionTokens"][SUBJECT]
                if value is None:
                    del rate["input"]
                else:
                    rate["input"] = value
                self.assertTrue(compare.price_problems(prices, [SUBJECT, JUDGE]))
                with self.assertRaises(ValueError):
                    compare.SpendLedger(prices, 25)
        for label, mutate in {"cached below direct": lambda r: r.__setitem__("cachedInput", 0.001),
                              "long tier below direct": lambda r: r["longContext"].__setitem__("output", 1.0),
                              "threshold mismatch": lambda r: r["longContext"].__setitem__("aboveInputTokens", 1)}.items():
            with self.subTest(price=label):
                prices = json.loads(json.dumps(self.prices))
                mutate(prices["platformBillable"]["usdPerMillionTokens"][SUBJECT])
                self.assertTrue(compare.price_problems(prices, [SUBJECT, JUDGE]))

    def test_interrupt_during_a_subject_call_is_recorded_and_nothing_else_is_sent(self):
        def fault(n, request):
            if n == 3:
                raise KeyboardInterrupt
        provider = Counting(Policy(), fault)
        manifest = compare.execute(args_for(self.out, judge=True), invoke=provider)
        self.assertEqual(3, provider.calls)
        self.assertEqual("interrupted", manifest["executionStatus"])
        interrupted = [r for r in manifest["records"] if r["status"] == "interrupted"]
        self.assertEqual(1, len(interrupted))
        self.assertEqual("interrupted", json.loads((self.out / interrupted[0]["folder"] / "attempt.json").read_text())["status"])
        self.assertEqual(3, manifest["spend"]["dispatchedCalls"])
        self.assertEqual(1, manifest["spend"]["unreconciledCalls"])
        self.assertEqual("interrupted", json.loads((self.out / "run.json").read_text())["status"])
        self.assertEqual("interrupted", manifest["records"][0]["status"])
        self.assertTrue(all(r["status"] == "not_run" for r in manifest["records"][1:]))
        self.assertEqual(36, len(manifest["records"]))

    def test_interrupt_during_judging_is_recorded(self):
        subject = Policy()

        def invoke(request, path, settings):
            if request.get("modelId") == JUDGE:
                raise KeyboardInterrupt
            return subject(request, path, settings)
        provider = Counting(invoke)
        manifest = compare.execute(args_for(self.out, judge=True), invoke=provider)
        self.assertEqual("interrupted", manifest["executionStatus"])
        self.assertEqual(1, sum(r.get("judge", {}).get("status") == "judge_interrupted" for r in manifest["records"]))
        self.assertTrue(all(r["status"] == "completed" for r in manifest["records"]))
        judge_dispatches = [e for e in self.events() if e["event"] == "reserve" and e["kind"] == "judge"]
        self.assertEqual(1, len(judge_dispatches))
        self.assertEqual(provider.calls, manifest["spend"]["dispatchedCalls"])

    def test_abrupt_stop_is_reconciled_from_the_ledger_without_guessing(self):
        snapshot = Path(self.tmp.name) / "snapshot"

        def fault(n, request):
            if n == 4:  # copy the durable state as a hard kill would leave it, mid-call
                snapshot.mkdir()
                (snapshot / "ledger.jsonl").write_text((self.out / "ledger.jsonl").read_text())
        compare.execute(args_for(self.out), invoke=Counting(Policy(), fault))
        result = compare.reconcile(snapshot)
        reserve = [e for e in map(json.loads, (snapshot / "ledger.jsonl").read_text().splitlines()) if e["event"] == "reserve"]
        self.assertEqual([4], result["unresolvedInFlightCalls"])
        self.assertAlmostEqual(reserve[-1]["reservedUsd"], result["unreconciledExposureUsd"], places=6)
        self.assertEqual(3, result["settledCalls"])
        self.assertIsNone(result["runEnded"])
        self.assertIn("abandoned", result["attempts"].values())
        self.assertEqual(0, result["providerCalls"])

    def test_cli_retries_are_disabled_so_one_reservation_covers_one_submission(self):
        completed = mock.Mock(returncode=0, stdout=json.dumps(reply("ok")), stderr="")
        with mock.patch.object(compare.subprocess, "run", return_value=completed) as run:
            compare.bedrock_invoke({}, Path("r.json"), {"profile": "dev", "region": "eu-west-1", "timeout": 120})
        argv, kwargs = run.call_args.args[0], run.call_args.kwargs
        self.assertEqual("1", kwargs["env"]["AWS_MAX_ATTEMPTS"])
        self.assertIn("--cli-read-timeout", argv)

    # Run-level completion semantics and exit status ---------------------------------

    def run_main(self, provider, *extra) -> int:
        argv = ["--old-revision", OLD, "--new-revision", NEW, "--execute", "--output", str(self.out), "--max-spend-usd", "10", *extra]
        with mock.patch.object(compare, "default_invoke", provider), mock.patch.dict(os.environ, {"OPENAI_API_KEY": "sk-offline-test"}), \
                self.assertRaises(SystemExit) as stop:
            compare.main(argv)
        return stop.exception.code

    def test_behavioural_failures_alone_exit_zero(self):
        self.assertEqual(0, self.run_main(Policy(fund_first=True)))
        summary = json.loads((self.out / "summary.json").read_text())
        self.assertEqual("complete", summary["executionStatus"])
        self.assertLess(sum(r["deterministic"]["passed"] for r in summary["records"]), 36)

    def test_step_limit_makes_execution_incomplete_and_exits_nonzero(self):
        looping = lambda *a: reply(tools=[("project-task.listByProject", {"projectId": PROJECT})])
        self.assertEqual(compare.EXIT_INCOMPLETE, self.run_main(looping))
        summary = json.loads((self.out / "summary.json").read_text())
        self.assertEqual("incomplete", summary["executionStatus"])
        self.assertIn("Execution: incomplete", (self.out / "report.md").read_text())

    def test_requested_judge_failure_exits_nonzero(self):
        subject = Policy()

        def invoke(request, path, settings):
            return judge_reply("not json") if request.get("modelId") == JUDGE else subject(request, path, settings)
        self.assertEqual(compare.EXIT_INCOMPLETE, self.run_main(invoke, "--judge"))

    def test_missing_openai_key_is_refused_before_any_output_or_dispatch(self):
        provider = Counting(Policy())
        env = {k: v for k, v in os.environ.items() if k != "OPENAI_API_KEY"}
        with mock.patch.object(compare, "default_invoke", provider), mock.patch.dict(os.environ, env, clear=True), \
                self.assertRaises(SystemExit):
            compare.execute(args_for(self.out))
        self.assertEqual(0, provider.calls)
        self.assertFalse(self.out.exists())


class OpenAIAdapterTests(unittest.TestCase):
    def setUp(self):
        self.git = FakeGit().__enter__()
        self.tmp = tempfile.TemporaryDirectory()
        self.out = Path(self.tmp.name) / "run"
        self.frozen = compare.load_frozen(OLD, NEW)
        self.prices = self.frozen["cases"]["run"]["prices"]

    def tearDown(self):
        self.git.__exit__()
        self.tmp.cleanup()

    def attempt(self, invoke, case_id="screening-optional-gaps-single-turn", ledger=None):
        ledger = ledger or compare.SpendLedger(self.prices, 10, self.out / "ledger.jsonl")
        self.out.mkdir(parents=True, exist_ok=True)
        item = {"index": 1, "case": case_id, "variant": "new", "repetition": 1, "folder": "attempts/a"}
        return compare.run_attempt(self.frozen, item, self.out, invoke, ledger, {}), ledger

    def test_request_uses_platform_luna_settings_and_no_temperature(self):
        policy = Policy()
        self.attempt(policy)
        first = policy.requests[0]
        self.assertEqual("gpt-5.6-luna", first["model"])
        self.assertEqual({"effort": "medium", "summary": "detailed"}, first["reasoning"])
        self.assertEqual({"verbosity": "medium"}, first["text"])
        self.assertEqual(128000, first["max_output_tokens"])
        self.assertFalse(first["store"])
        self.assertEqual(["reasoning.encrypted_content"], first["include"])
        self.assertNotIn("temperature", first)
        self.assertEqual(["developer", "developer", "user"], [i["role"] for i in first["input"]])
        self.assertEqual(30, len(first["tools"]))
        self.assertTrue(all(t["type"] == "function" and "parameters" in t for t in first["tools"]))

    def test_reasoning_and_calls_are_replayed_verbatim_with_matching_outputs(self):
        responses = []

        def recording(request, path, settings):
            responses.append(Policy()(request, path, settings))
            return responses[-1]
        record, _ = self.attempt(recording)
        self.assertEqual("completed", record["status"])
        second = json.loads((self.out / "attempts/a/t0-s01-request.json").read_text())
        first_output = responses[0]["output"]
        tail = second["input"][-(len(first_output) + 1):]
        self.assertEqual(first_output, tail[:-1])
        self.assertEqual("ENC-" + first_output[0]["id"].split("_")[1], tail[0]["encrypted_content"])
        self.assertEqual({"type": "function_call_output", "call_id": first_output[-1]["call_id"]},
                         {k: tail[-1][k] for k in ("type", "call_id")})
        self.assertIn("taskId", json.loads(tail[-1]["output"]))
        self.assertEqual(first_output[-1]["call_id"], record["turns"][0]["calls"][0]["callId"])

    def test_replayed_output_raises_the_next_input_bound(self):
        record, ledger = self.attempt(Policy())
        reserves = [json.loads(l) for l in (self.out / "ledger.jsonl").read_text().splitlines()]
        reserves = [e for e in reserves if e["event"] == "reserve"]
        second = json.loads((self.out / "attempts/a/t0-s01-request.json").read_text())
        first_output_tokens = json.loads((self.out / "attempts/a/t0-s00-response.json").read_text())["usage"]["output_tokens"]
        self.assertEqual(compare.input_token_bound(second) + first_output_tokens, reserves[1]["bounds"]["inputTokens"])
        self.assertNotIn("ENC-", json.dumps({k: v for k, v in second.items() if k != "input"}))

    def test_invalid_json_arguments_are_an_invalid_tool_call(self):
        def broken(request, path, settings):
            response = reply(tools=[("task-management.createTask", {})])
            response["output"][-1]["arguments"] = "{not json"
            return response if len(user_texts(request)) and request["input"][-1].get("type") != "function_call_output" \
                else reply("Stopped.")
        record, _ = self.attempt(broken)
        self.assertEqual("Invalid JSON arguments", record["turns"][0]["calls"][0]["error"])
        self.assertIn("noInvalidToolCalls", " ".join(record["deterministic"]["errors"]))

    def test_failed_status_settles_usage_then_is_a_provider_error(self):
        record, ledger = self.attempt(lambda *a: {**reply("x"), "status": "failed", "error": {"code": "server_error"}})
        self.assertEqual("provider_error", record["status"])
        self.assertEqual(1, ledger.settled)
        self.assertGreater(ledger.confirmed, 0)
        self.assertEqual(0, ledger.exposure)

    def test_incomplete_response_does_not_execute_pending_tool_calls(self):
        record, _ = self.attempt(lambda *a: reply(tools=[create_screening()], status="incomplete"))
        self.assertEqual("incomplete", record["status"])
        self.assertEqual([], record["turns"][0]["calls"])
        self.assertIn("incomplete:max_output_tokens", record["incompleteReason"])

    def test_cached_and_reasoning_tokens_are_not_double_counted(self):
        luna = self.prices["platformBillable"]["usdPerMillionTokens"][SUBJECT]
        record, ledger = self.attempt(lambda *a: {**reply("Which Fund?"), "usage": oai_usage(10000, 1000, cached=8000, reasoning=900)})
        expected = (2000 * 0.26 + 8000 * 0.026 + 1000 * 1.56) / 1e6
        self.assertAlmostEqual(expected, ledger.confirmed, places=9)
        self.assertAlmostEqual(expected, compare.usd(luna, {"inputTokens": 10000, "cachedInputTokens": 8000, "outputTokens": 1000}), places=9)
        self.assertEqual(900, record["usage"]["reasoningTokens"])
        self.assertAlmostEqual((2000 * 0.20 + 8000 * 0.02 + 1000 * 1.20) / 1e6, ledger.direct_confirmed, places=9)

    def test_long_context_tier_applies_above_the_threshold(self):
        luna = self.prices["platformBillable"]["usdPerMillionTokens"][SUBJECT]
        at, above = ({"inputTokens": n, "cachedInputTokens": 0, "outputTokens": 0} for n in (272000, 272001))
        self.assertAlmostEqual(272000 * 0.26 / 1e6, compare.usd(luna, at), places=9)
        self.assertAlmostEqual(272001 * 0.52 / 1e6, compare.usd(luna, above), places=9)

    def test_transport_sends_once_without_retry_and_keeps_the_key_out_of_evidence(self):
        import io
        import urllib.error
        request = compare.first_requests(self.frozen)[("screening-optional-gaps-single-turn", "old")]
        ledger = compare.SpendLedger(self.prices, 10)
        self.out.mkdir(parents=True)
        error = urllib.error.HTTPError("https://api.openai.com/v1/responses", 429, "Too Many Requests", {}, io.BytesIO(b'{"error":"rate"}'))
        settings = {"endpoint": "https://api.openai.com/v1/responses", "timeout": 300}
        with mock.patch.dict(os.environ, {"OPENAI_API_KEY": "sk-offline-SECRET"}), \
                mock.patch.object(compare.urllib.request, "urlopen", side_effect=error) as urlopen:
            with self.assertRaises(compare.ProviderError):
                compare.call_provider(compare.openai_invoke, ledger, "subject", "x", request, self.out / "x-request.json", settings)
        self.assertEqual(1, urlopen.call_count)
        sent = urlopen.call_args.args[0]
        self.assertEqual("Bearer sk-offline-SECRET", sent.get_header("Authorization"))
        self.assertEqual(300, urlopen.call_args.kwargs["timeout"])
        self.assertNotIn("SECRET", (self.out / "x-request.json").read_text())
        self.assertEqual(1, ledger.unreconciled)

    def test_transport_parses_a_successful_response(self):
        body = mock.MagicMock()
        body.__enter__.return_value.read.return_value = json.dumps(reply("ok")).encode()
        with mock.patch.dict(os.environ, {"OPENAI_API_KEY": "sk-offline"}), \
                mock.patch.object(compare.urllib.request, "urlopen", return_value=body):
            response = compare.openai_invoke({"model": SUBJECT}, Path("r.json"), {"endpoint": "https://api.openai.com/v1/responses",
                                                                                   "timeout": 5})
        self.assertEqual("completed", response["status"])


class LaunchControlTests(unittest.TestCase):
    """A systematic payload/auth error must stop the run after one dispatch, not repeat the rejected payload."""

    def setUp(self):
        self.git = FakeGit().__enter__()
        self.tmp = tempfile.TemporaryDirectory()
        self.out = Path(self.tmp.name) / "run"

    def tearDown(self):
        self.git.__exit__()
        self.tmp.cleanup()

    def http_error(self, code):
        import io
        import urllib.error
        return urllib.error.HTTPError("https://api.openai.com/v1/responses", code, "x", {}, io.BytesIO(b'{"error":{"message":"bad"}}'))

    def run_with_http(self, code):
        with mock.patch.dict(os.environ, {"OPENAI_API_KEY": "sk-offline"}), \
                mock.patch.object(compare.urllib.request, "urlopen", side_effect=self.http_error(code)) as urlopen:
            manifest = compare.execute(args_for(self.out, judge=True), invoke=compare.default_invoke)
        return manifest, urlopen.call_count

    def test_rejected_payload_stops_after_the_first_dispatch(self):
        for code in (400, 401, 403, 404, 422):
            with self.subTest(code=code):
                self.out = Path(self.tmp.name) / f"r{code}"
                manifest, sent = self.run_with_http(code)
                self.assertEqual(1, sent)
                self.assertIn("systematic provider error", manifest["halted"])
                self.assertEqual(35, sum(r["status"] == "not_run" for r in manifest["records"]))
                self.assertEqual(1, manifest["spend"]["unreconciledCalls"])
                self.assertEqual("incomplete", manifest["executionStatus"])

    def test_rate_limits_are_transient_and_use_the_consecutive_limit(self):
        manifest, sent = self.run_with_http(429)
        self.assertEqual(3, sent)
        self.assertEqual("consecutive provider errors", manifest["halted"])

    def test_malformed_first_response_stops_immediately(self):
        provider = Counting(lambda *a: {**reply("x"), "output": "not-a-list"})
        manifest = compare.execute(args_for(self.out), invoke=provider)
        self.assertEqual(1, provider.calls)
        self.assertIn("systematic", manifest["halted"])

    def test_systematic_judge_error_stops_judging_after_one_dispatch(self):
        subject, judge_calls = Policy(), {"n": 0}
        failed = mock.Mock(returncode=254, stdout="", stderr="An error occurred (ValidationException) when calling Converse")

        def invoke(request, path, settings):
            if request.get("modelId") == JUDGE:
                judge_calls["n"] += 1
                with mock.patch.object(compare.subprocess, "run", return_value=failed):
                    return compare.bedrock_invoke(request, path, {"profile": "dev", "region": "eu-west-1", "timeout": 5})
            return subject(request, path, settings)
        manifest = compare.execute(args_for(self.out, judge=True), invoke=invoke)
        self.assertEqual(1, judge_calls["n"])
        self.assertIn("systematic judge", manifest["halted"])
        self.assertEqual("incomplete", manifest["executionStatus"])
        self.assertTrue(all(r["status"] == "completed" for r in manifest["records"]))

    def test_expired_sso_is_systematic(self):
        expired = mock.Mock(returncode=255, stdout="", stderr="Error when retrieving token from sso: Token has expired and refresh failed")
        with mock.patch.object(compare.subprocess, "run", return_value=expired), self.assertRaises(compare.ProviderError) as caught:
            compare.bedrock_invoke({}, Path("r.json"), {"profile": "dev", "region": "eu-west-1", "timeout": 5})
        self.assertTrue(caught.exception.systematic)

    def test_transient_aws_errors_are_not_systematic(self):
        busy = mock.Mock(returncode=254, stdout="", stderr="An error occurred (ThrottlingException): slow down")
        with mock.patch.object(compare.subprocess, "run", return_value=busy), self.assertRaises(compare.ProviderError) as caught:
            compare.bedrock_invoke({}, Path("r.json"), {"profile": "dev", "region": "eu-west-1", "timeout": 5})
        self.assertFalse(caught.exception.systematic)


class JudgeResumeTests(unittest.TestCase):
    """Judging an existing run after a rejected judge payload, without re-running subjects or resetting spend."""

    def setUp(self):
        self.git = FakeGit().__enter__()
        self.tmp = tempfile.TemporaryDirectory()
        self.out = Path(self.tmp.name) / "run"
        rejected = mock.Mock(returncode=254, stdout="", stderr="An error occurred (ValidationException): `temperature` is deprecated")

        def first_run(request, path, settings):
            if request.get("modelId") == JUDGE:
                with mock.patch.object(compare.subprocess, "run", return_value=rejected):
                    return compare.bedrock_invoke(request, path, {"profile": "dev", "region": "eu-west-1", "timeout": 5})
            return Policy(fund_first=True)(request, path, settings)
        self.first = compare.execute(args_for(self.out, judge=True), invoke=first_run)

    def tearDown(self):
        self.git.__exit__()
        self.tmp.cleanup()

    def resume_args(self, ceiling=10):
        return compare.parse_args(["--old-revision", OLD, "--new-revision", NEW, "--judge-run", str(self.out),
                                   "--max-spend-usd", str(ceiling)])

    def scoring_judge(self):
        calls = {"judge": 0, "subject": 0, "temperatures": []}

        def invoke(request, path, settings):
            if request.get("modelId") != JUDGE:
                calls["subject"] += 1
                raise AssertionError("subject dispatched during judge resume")
            calls["judge"] += 1
            calls["temperatures"].append("temperature" in request["inferenceConfig"])
            payload = json.loads(request["messages"][0]["content"][0]["text"])
            return judge_reply(json.dumps({"criteria": {c: {"score": 2, "rationale": "ok"} for c in payload["criteria"]}}))
        return calls, invoke

    def test_judge_request_sends_no_temperature(self):
        frozen = compare.load_frozen(OLD, NEW)
        self.assertNotIn("temperature", frozen["cases"]["run"]["judge"])
        self.assertNotIn("temperature", compare.judge_request(frozen, {"criteria": {}})["inferenceConfig"])

    def test_resume_judges_all_attempts_and_keeps_spend_cumulative(self):
        self.assertIn("systematic judge", self.first["halted"])
        prior = self.first["spend"]
        calls, invoke = self.scoring_judge()
        summary = compare.judge_existing(self.resume_args(), invoke=invoke)
        self.assertEqual(0, calls["subject"])
        self.assertEqual(36, calls["judge"])
        self.assertFalse(any(calls["temperatures"]))
        self.assertEqual("complete", summary["executionStatus"])
        spend = summary["spend"]
        self.assertGreaterEqual(spend["unreconciledExposureUsd"], prior["unreconciledExposureUsd"])
        self.assertGreater(spend["confirmedUsd"], prior["confirmedUsd"])
        self.assertEqual(prior["dispatchedCalls"] + 36, spend["dispatchedCalls"])
        self.assertEqual(compare.reconcile(self.out)["confirmedUsd"], round(spend["confirmedUsd"], 6))
        self.assertTrue((self.out / "judge").exists() and (self.out / "judge-2").exists())
        self.assertTrue((self.out / "summary-subject-phase.json").exists())
        self.assertEqual(self.first["cells"]["screening-optional-gaps-single-turn"]["old"]["deterministicPass"],
                         summary["cells"]["screening-optional-gaps-single-turn"]["old"]["deterministicPass"])

    def test_resume_counts_prior_spend_against_the_ceiling(self):
        calls, invoke = self.scoring_judge()
        tight = round(self.first["spend"]["spentUsd"] + 0.01, 4)
        summary = compare.judge_existing(self.resume_args(ceiling=tight), invoke=invoke)
        self.assertEqual(0, calls["judge"])
        self.assertIn("spend ceiling", summary["halted"])
        self.assertLessEqual(summary["spend"]["spentUsd"], tight)

    def test_resume_refuses_identity_drift_and_double_judging(self):
        calls, invoke = self.scoring_judge()
        summary = json.loads((self.out / "summary.json").read_text())
        summary["identity"]["expectationsSha256"] = "0" * 64
        (self.out / "summary.json").write_text(json.dumps(summary))
        with self.assertRaises(SystemExit):
            compare.judge_existing(self.resume_args(), invoke=invoke)
        self.assertEqual(0, calls["judge"])
        summary["identity"]["expectationsSha256"] = self.first["identity"]["expectationsSha256"]
        (self.out / "summary.json").write_text(json.dumps(summary))
        (self.out / "judge-2").mkdir()
        with self.assertRaises(SystemExit):
            compare.judge_existing(self.resume_args(), invoke=invoke)
        self.assertEqual(0, calls["judge"])


class SharedRunnerTests(unittest.TestCase):
    def test_capability_bundle_template_resolves_frozen_platform_tools(self):
        template = yaml.safe_load((PACK_DIR / "agent-templates" / "vc_deal_pipeline_manager.yaml").read_text())
        self.assertNotIn("mcpServers", template)
        names = {spec["toolSpec"]["name"] for spec in evaluate_deal_manager.tool_specs(template)}
        self.assertIn("task-management_createTask", names)
        self.assertIn("task-management_getTaskDetail", names)
        contract = json.loads(evaluate_deal_manager.TOOL_CONTRACT.read_text())
        self.assertEqual(template["capabilityProfile"]["bundles"], contract["capabilityBundles"])

    def test_template_with_other_bundles_is_refused_not_given_the_manager_tools(self):
        legacy = yaml.safe_load((PACK_DIR / "agent-templates" / "vc_deal_manager.yaml").read_text())
        with self.assertRaises(ValueError):
            evaluate_deal_manager.tool_specs(legacy)


if __name__ == "__main__":
    unittest.main()
