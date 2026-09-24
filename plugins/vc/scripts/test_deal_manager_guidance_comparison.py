#!/usr/bin/env python3
"""Offline checks for the Packs PR #97 (issue #4313) guidance suites; every provider is mocked."""
from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import yaml

import compare_deal_manager_prompts as compare
from evaluate_deal_manager import ROOT
from test_deal_manager_prompt_comparison import Counting, judge_reply, reply, user_texts

HERE = Path(__file__).resolve().parent
PACK_DIR = HERE.parent / "alludium"
OLD, NEW = "old-rev", "new-rev"
NEW_SENTENCE = "Synthetic guidance sentence for offline tests only."
JUDGE = "global.anthropic.claude-opus-4-8"
SUITES = ("pr97-4313-pipeline", "pr97-4313-legacy")
TEMPLATE_PATHS = {compare.TEMPLATE_PATH, compare.LEGACY_TEMPLATE_PATH}
CLEAN = ("We still need to verify the EUR 180k ARR because it drives valuation; next, ask the founders for invoices "
         "and bank statements, book two customer reference calls, and request the cap table and incorporation documents.")


def fake_show(revision: str, path: str) -> str:
    """Working-tree Pack files; the new revision adds one prompt sentence to either manager template."""
    text = (PACK_DIR.parent / path.removeprefix("plugins/vc/")).read_text()
    if revision == NEW and path in TEMPLATE_PATHS:
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


def args_for(suite: str, output: Path | None = None, **overrides) -> object:
    argv = ["--suite", suite, "--old-revision", OLD, "--new-revision", NEW]
    if output:
        argv += ["--output", str(output), "--max-spend-usd", "5", "--execute"]
    args = compare.parse_args(argv)
    for key, value in overrides.items():
        setattr(args, key, value)
    return args


def contract_names(path: Path) -> list[str]:
    return [tool["name"] for tool in json.loads(path.read_text())["tools"]]


def runtime_of(request: dict) -> dict:
    developer = [item for item in request["input"] if item.get("role") == "developer"]
    return json.loads(developer[1]["content"][0]["text"].split("\n", 1)[1])


class Advisor:
    """Scripted subject: reads the report output when one exists, then answers. `write` makes it
    also create a task (an unauthorised mutation); `text` overrides the final wording."""

    def __init__(self, text: str = CLEAN, write: str | None = None):
        self.text, self.write, self.requests = text, write, []

    def __call__(self, request: dict, path: Path, settings: dict) -> dict:
        self.requests.append(request)
        items = request["input"]
        if items[-1].get("type") == "function_call_output":
            return reply(self.text)
        runtime = runtime_of(request)
        calls = []
        if runtime["project"]["latestOutputArtifactId"]:
            calls.append(("artifact.getArtifact", {"artifactId": runtime["project"]["latestOutputArtifactId"]}))
        if self.write:
            definition = runtime["availableTaskDefinitions"][0]["id"]
            calls.append((self.write, {"projectId": compare.PROJECT, "taskDefinitionId": definition, "title": "Verify ARR",
                                       "instruction": "Collect ARR evidence."}))
        return reply(tools=calls) if calls else reply(self.text)


def score_judge(request: dict) -> dict:
    payload = json.loads(request["messages"][0]["content"][0]["text"])
    return judge_reply(json.dumps({"criteria": {c: {"score": 2, "rationale": "ok"} for c in payload["criteria"]}}))


class GuidanceSuiteTests(unittest.TestCase):
    def setUp(self):
        self.git = FakeGit().__enter__()
        self.tmp = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.git.__exit__()
        self.tmp.cleanup()

    def frozen(self, suite: str) -> dict:
        return compare.load_frozen(OLD, NEW, suite)

    def test_both_suites_are_ready_with_exact_counts_and_no_provider_access(self):
        forbidden = mock.Mock(side_effect=AssertionError("provider access during preflight"))
        with mock.patch.object(compare, "default_invoke", forbidden), mock.patch.object(compare, "call_provider", forbidden), \
                mock.patch.object(compare.urllib.request, "urlopen", forbidden), mock.patch.object(compare, "bedrock_invoke", forbidden):
            for suite in SUITES:
                with self.subTest(suite=suite):
                    report = compare.preflight(args_for(suite))
                    self.assertTrue(report["preparationReady"], report["blockingProblems"])
                    self.assertEqual(0, report["providerCalls"])
                    self.assertEqual({"cases": 5, "variants": 2, "repetitions": 3, "attempts": 30, "potentialJudgeCalls": 30},
                                     {k: v for k, v in report["counts"].items() if k != "maxSubjectCalls"})
                    self.assertTrue(report["sharedInputsVerified"])
                    self.assertIn(f"--suite {suite} ", report["executeCommand"])
                    self.assertEqual(5, report["proposedCeilingUsd"])

    def test_each_template_gets_only_its_own_platform_tools(self):
        pipeline = compare.first_requests(self.frozen("pr97-4313-pipeline"))
        legacy = compare.first_requests(self.frozen("pr97-4313-legacy"))
        pipeline_tools = {t["name"] for t in next(iter(pipeline.values()))["tools"]}
        legacy_tools = {t["name"] for t in next(iter(legacy.values()))["tools"]}
        self.assertEqual({n.replace(".", "_") for n in contract_names(compare.TOOL_CONTRACT)}, pipeline_tools)
        self.assertEqual({n.replace(".", "_") for n in contract_names(compare.LEGACY_TOOL_CONTRACT)}, legacy_tools)
        self.assertIn("task-management_createTask", pipeline_tools)
        self.assertNotIn("task-management_createTask", legacy_tools)
        self.assertNotIn("artifact_createTextArtifact", legacy_tools)
        self.assertTrue({"task-management_createTaskFromDefinition", "agent_findAvailableForCurrentUser"} <= legacy_tools)
        for requests in (pipeline, legacy):
            self.assertEqual(1, len({json.dumps(r["tools"]) for r in requests.values()}))

    def test_contracts_match_their_template_bundles_and_are_not_interchangeable(self):
        for suite in SUITES:
            self.assertEqual([], self.frozen(suite)["problems"])
        with mock.patch.object(compare, "LEGACY_TOOL_CONTRACT", compare.TOOL_CONTRACT):
            self.assertIn("bundles do not match", " ".join(self.frozen("pr97-4313-legacy")["problems"]))

    def test_variants_share_every_input_except_the_prompt_and_render_all_variables(self):
        for suite in SUITES:
            frozen = self.frozen(suite)
            requests = compare.first_requests(frozen)
            self.assertEqual([], compare.shared_input_problems(frozen, requests))
            for request in requests.values():
                self.assertNotIn("{{", request["input"][0]["content"][0]["text"])
        legacy = compare.first_requests(self.frozen("pr97-4313-legacy"))
        self.assertIn("`europe-seed`", legacy[("concrete-gaps-next-step", "old")]["input"][0]["content"][0]["text"])

    def test_cases_are_shared_across_templates_and_expectations_stay_out_of_subject_inputs(self):
        expectations = yaml.safe_load(compare.GUIDANCE_EXPECTATIONS.read_text())
        rubric = list(expectations["judge"]["criteria"]) + [s[:60] for s in expectations["judge"]["situations"].values()]
        rubric += ["noLeakedIdentifiers", "noForbiddenMutations", "Advice only", "4313", "PR #97"]
        users = {}
        for suite in SUITES:
            requests = compare.first_requests(self.frozen(suite))
            dumped = json.dumps(list(requests.values()))
            for marker in rubric:
                self.assertNotIn(marker, dumped)
            users[suite] = {key: user_texts(r) for key, r in requests.items()}
        self.assertEqual(users["pr97-4313-pipeline"], users["pr97-4313-legacy"])

    def test_prohibited_phrase_is_not_planted_in_every_input(self):
        requests = compare.first_requests(self.frozen("pr97-4313-pipeline"))
        planted = {case for (case, variant), r in requests.items() if "bounded validation program" in json.dumps(r).lower()}
        self.assertEqual({"internal-phrase-translation", "explicit-system-question"}, planted)
        in_user = {case for (case, _), r in requests.items() if "bounded validation program" in " ".join(user_texts(r)).lower()}
        self.assertEqual({"explicit-system-question"}, in_user)

    def test_simulator_answers_every_read_tool_in_both_contracts(self):
        for suite in SUITES:
            frozen = self.frozen(suite)
            case = next(c for c in frozen["cases"]["cases"] if c["id"] == "internal-phrase-translation")
            simulator = compare.GuidanceSimulator(frozen, case)
            params = {"projectId": compare.PROJECT, "taskId": compare.EXISTING_TASK, "artifactId": compare.REPORT,
                      "id": next(iter(simulator.catalog))}
            for name in frozen["toolNames"]:
                if name in compare.GUIDANCE_WRITES:
                    continue
                with self.subTest(suite=suite, tool=name):
                    self.assertIsNone(simulator.handle(name, params)[1])
            self.assertEqual([], simulator.mutations)
            self.assertIn("bounded validation program", simulator.handle("artifact.getArtifact", params)[0]["content"])

    def test_missing_evidence_case_has_no_report_or_completed_task(self):
        frozen = self.frozen("pr97-4313-legacy")
        case = next(c for c in frozen["cases"]["cases"] if c["id"] == "missing-evidence-no-report")
        simulator = compare.GuidanceSimulator(frozen, case)
        self.assertEqual([], simulator.tasks)
        self.assertEqual([compare.DECK], simulator.project()["artifactIds"])
        self.assertIsNotNone(simulator.handle("artifact.getArtifact", {"artifactId": compare.REPORT})[1])

    def record(self, text: str, calls: list[dict] | None = None, case: str = "internal-phrase-translation") -> dict:
        return {"case": case, "status": "completed",
                "turns": [{"index": 0, "author": "human", "texts": [text], "final": text, "complete": True, "calls": calls or []}]}

    def test_scorer_contracts(self):
        frozen = self.frozen("pr97-4313-pipeline")
        score = lambda *a, **k: compare.score_guidance(frozen, k.pop("case", "internal-phrase-translation"), self.record(*a, **k))
        self.assertTrue(score(CLEAN)["passed"])
        # No question mark is needed or rewarded.
        self.assertNotIn("?", CLEAN)
        self.assertIn("noLeakedIdentifiers", score("Next, run the Bounded Validation Program.")["errors"][0])
        self.assertTrue(score("Next, run the bounded validation program.", case="explicit-system-question")["passed"])
        self.assertEqual(["generate-refresh-screening-report"], score("Use generate-refresh-screening-report.")["leaks"])
        self.assertEqual(["task-management_createTask"], score("I can call task-management_createTask.")["leaks"])
        self.assertEqual(["BVP-2"], score("Start with BVP-2.")["leaks"])
        write = {"name": "task-management.createTask", "input": {}, "error": None, "createdTaskId": "x"}
        self.assertIn("noForbiddenMutations", score(CLEAN, [write])["errors"][0])
        update = {"name": "project.update", "input": {}, "error": None}
        self.assertFalse(score(CLEAN, [update])["passed"])
        attach = {"name": "artifact.attachToChat", "input": {}, "error": None}
        self.assertTrue(score(CLEAN, [attach])["passed"])
        self.assertIn("noFalseExecutionClaim", " ".join(score("I've started the verification work.")["errors"]))
        rejected = {"name": "project.unknownTool", "input": {}, "error": "Unknown tool"}
        self.assertIn("noInvalidToolCalls", score(CLEAN, [rejected])["errors"][0])

    def test_legacy_slugs_are_checked_against_the_legacy_template(self):
        frozen = self.frozen("pr97-4313-legacy")
        record = self.record("Run run-investment-fit-screen then agent_findAvailableForCurrentUser.")
        self.assertEqual(["agent_findAvailableForCurrentUser", "run-investment-fit-screen"],
                         compare.score_guidance(frozen, "internal-phrase-translation", record)["leaks"])

    def test_execute_records_unauthorised_write_and_keeps_judge_blind(self):
        judged = []

        def invoke(request, path, settings):
            if request.get("modelId") == JUDGE:
                judged.append(request)
                return score_judge(request)
            return subject(request, path, settings)
        subject = Advisor(write="task-management.createTaskFromDefinition")
        out = Path(self.tmp.name) / "legacy"
        manifest = compare.execute(args_for("pr97-4313-legacy", out, judge=True), invoke=invoke)
        self.assertEqual("complete", manifest["executionStatus"])
        self.assertEqual(30, len(judged))
        self.assertTrue(all(not r["deterministic"]["passed"] for r in manifest["records"]))
        self.assertTrue(all(r["mutations"] and r["deterministic"]["mutations"] == ["task-management.createTaskFromDefinition"]
                            for r in manifest["records"]))
        dumped = json.dumps([json.loads(r["messages"][0]["content"][0]["text"]) for r in judged])
        # Verdict and variant markers are JSON keys: Pack workflow text legitimately uses words like "deterministic".
        # Catalogue text may name agent templates (a fact the subject saw); runner identity must never appear.
        for forbidden in ('"old"', '"new"', '"variant"', '"deterministic"', '"passed"', "1.0.4", "1.0.5", "User-facing language",
                          '"templateId"', '"suite"', '"gitBlob"', '"promptSha256"'):
            self.assertNotIn(forbidden, dumped)
        payload = json.loads(judged[0]["messages"][0]["content"][0]["text"])
        self.assertIn("evidenceAvailable", payload)
        system_case = [json.loads(r["messages"][0]["content"][0]["text"]) for r in judged]
        system_case = [p for p in system_case if "how the system would handle" in json.dumps(p["criteria"])]
        self.assertEqual(6, len(system_case))
        self.assertTrue(all(set(p["criteria"]) == {"answersSystemQuestion", "faithfulToEvidence"} for p in system_case))
        self.assertTrue((out / "ledger.jsonl").exists())
        self.assertIn("issue #4313, vc_deal_manager", (out / "report.md").read_text())

    def test_clean_advice_passes_and_reports_template_results_separately(self):
        outputs = {}
        for suite in SUITES:
            out = Path(self.tmp.name) / suite
            outputs[suite] = compare.execute(args_for(suite, out), invoke=Advisor())
            self.assertTrue(all(r["deterministic"]["passed"] for r in outputs[suite]["records"]))
            self.assertEqual(suite, outputs[suite]["identity"]["suite"])
        self.assertNotEqual(outputs[SUITES[0]]["identity"]["toolContract"], outputs[SUITES[1]]["identity"]["toolContract"])

    def test_systematic_subject_error_stops_after_one_dispatch(self):
        provider = Counting(lambda *a: (_ for _ in ()).throw(compare.ProviderError("HTTP 400: bad", systematic=True)))
        manifest = compare.execute(args_for("pr97-4313-pipeline", Path(self.tmp.name) / "e"), invoke=provider)
        self.assertEqual(1, provider.calls)
        self.assertIn("systematic provider error", manifest["halted"])
        self.assertEqual(29, sum(r["status"] == "not_run" for r in manifest["records"]))

    def test_ceiling_above_the_frozen_proposal_is_refused(self):
        with self.assertRaises(SystemExit):
            compare.execute(args_for("pr97-4313-pipeline", Path(self.tmp.name) / "c", max_spend_usd=5.01), invoke=Advisor())

    def test_judge_resume_refuses_a_run_from_another_suite(self):
        out = Path(self.tmp.name) / "resume"
        compare.execute(args_for("pr97-4313-pipeline", out), invoke=Advisor())
        args = compare.parse_args(["--suite", "pr97-4313-legacy", "--old-revision", OLD, "--new-revision", NEW,
                                   "--judge-run", str(out), "--max-spend-usd", "5"])
        with self.assertRaises(SystemExit) as caught:
            compare.judge_existing(args, invoke=score_judge)
        self.assertIn("suite", str(caught.exception))


class Explainer(Advisor):
    """Answers the system question after looking up the report workflow and the available agents."""

    def __call__(self, request: dict, path: Path, settings: dict) -> dict:
        self.requests.append(request)
        if request["input"][-1].get("type") == "function_call_output":
            return reply(self.text)
        runtime = runtime_of(request)
        report_task = runtime["project"]["tasks"][0] if runtime["project"]["tasks"] else None
        calls = [("agent.findAvailableForCurrentUser", {})] if "agent_findAvailableForCurrentUser" in \
            {t["name"] for t in request["tools"]} else []
        if report_task:
            calls += [("task-definitions.findById", {"id": report_task["taskDefinitionId"]}),
                      ("artifact.getArtifact", {"artifactId": compare.REPORT})]
        return reply(tools=calls) if calls else reply(self.text)


class JudgeEvidenceTests(unittest.TestCase):
    """The judge must see the system facts the subject saw, so a truthful answer is not scored as invented."""

    def setUp(self):
        self.git = FakeGit().__enter__()
        self.tmp = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.git.__exit__()
        self.tmp.cleanup()

    def judged(self, suite: str) -> tuple[dict, list[dict], dict]:
        payloads = []

        def invoke(request, path, settings):
            if request.get("modelId") == JUDGE:
                payloads.append(json.loads(request["messages"][0]["content"][0]["text"]))
                return score_judge(request)
            return subject(request, path, settings)
        subject = Explainer()
        manifest = compare.execute(args_for(suite, Path(self.tmp.name) / suite, judge=True), invoke=invoke)
        by_blind = {r["judge"]["blindId"]: r for r in manifest["records"]}
        return manifest, [{**p, "_record": by_blind[p["attempt"]]} for p in payloads], subject.requests[0]

    def test_explicit_system_case_carries_the_catalogue_agents_and_readbacks_the_subject_saw(self):
        for suite, own, other in (("pr97-4313-legacy", ("run-investment-fit-screen", "First Look Analyst", "vc_deal_room"),
                                   ("generate-refresh-screening-report", "Deal Analyst", "vc_deal_pipeline")),
                                  ("pr97-4313-pipeline", ("generate-refresh-screening-report", "Deal Analyst", "vc_deal_pipeline"),
                                   ("run-investment-fit-screen", "First Look Analyst", "vc_deal_room"))):
            with self.subTest(suite=suite):
                manifest, payloads, first = self.judged(suite)
                system = [p for p in payloads if p["_record"]["case"] == "explicit-system-question"]
                self.assertEqual(6, len(system))
                seen = runtime_of(first)["availableTaskDefinitions"]
                for payload in system:
                    context = payload["systemContext"]
                    self.assertEqual(seen, context["availableTaskDefinitions"])
                    self.assertTrue(context["project"]["fundConfirmed"])
                    tools = [r["tool"] for r in payload["toolReadbacks"]]
                    self.assertIn("task-definitions.findById", tools)
                    self.assertNotIn("artifact.getArtifact", tools)
                    dumped = json.dumps({k: v for k, v in payload.items() if k != "_record"})
                    for fact in own:
                        self.assertIn(fact, dumped)
                    for fact in other:
                        self.assertNotIn(fact, dumped)
                    for forbidden in ('"old"', '"new"', '"variant"', '"deterministic"', '"passed"', "User-facing language",
                                      "Turn Completion Contract", "1.0.4", "1.0.5", "1.0.6", "1.0.7", suite, '"templateId"',
                                      '"gitBlob"', '"promptSha256"'):
                        self.assertNotIn(forbidden, dumped)
                self.assertIn("agent.findAvailableForCurrentUser", json.dumps(system[0]["toolReadbacks"])) \
                    if suite.endswith("legacy") else self.assertNotIn("agent.", json.dumps(system[0]["toolReadbacks"]))

    def test_old_and_new_receive_identical_judge_evidence_for_a_template(self):
        _, payloads, _ = self.judged("pr97-4313-legacy")
        evidence = {}
        for payload in payloads:
            key = payload["_record"]["case"]
            facts = {k: payload[k] for k in ("evidenceNote", "evidenceAvailable", "systemContext", "toolReadbacks")}
            evidence.setdefault(key, {}).setdefault(payload["_record"]["variant"], []).append(json.dumps(facts, sort_keys=True))
        for case, variants in evidence.items():
            self.assertEqual(1, len(set(variants["old"] + variants["new"])), case)

    def test_other_cases_get_a_compact_projection_without_catalogue_instructions(self):
        _, payloads, _ = self.judged("pr97-4313-legacy")
        compact = [p for p in payloads if p["_record"]["case"] == "concrete-gaps-next-step"]
        definitions = compact[0]["systemContext"]["availableTaskDefinitions"]
        self.assertEqual(6, len(definitions))
        self.assertTrue(all("definitionJson" not in d and d["slug"] and "requiredInputs" in d for d in definitions))
        self.assertIn("run-investment-fit-screen", {d["slug"] for d in definitions})

    def test_pr98_judge_input_is_unchanged(self):
        manifest = compare.execute(compare.parse_args(["--old-revision", OLD, "--new-revision", NEW, "--output",
                                                       str(Path(self.tmp.name) / "pr98"), "--max-spend-usd", "10", "--execute"]),
                                   invoke=lambda *a: reply("Which Fund?"))
        frozen = compare.load_frozen(OLD, NEW)
        payload = compare.judge_input(frozen, manifest["records"][0], "blind")
        self.assertEqual({"attempt", "situation", "criteria", "conversation"}, set(payload))


class EstimateTests(unittest.TestCase):
    """Preflight judge cost for guidance suites comes from the payloads they build, not a fixed 6k guess."""

    def setUp(self):
        self.git = FakeGit().__enter__()

    def tearDown(self):
        self.git.__exit__()

    def test_guidance_judge_estimate_is_sized_from_prepared_payloads(self):
        for suite in SUITES:
            with self.subTest(suite=suite):
                frozen = compare.load_frozen(OLD, NEW, suite)
                plan = compare.plan_attempts(frozen["cases"]["cases"], frozen["cases"]["run"]["repetitions"])
                forbidden = mock.Mock(side_effect=AssertionError("provider access during estimate"))
                with mock.patch.object(compare, "call_provider", forbidden), mock.patch.object(compare, "default_invoke", forbidden):
                    cost = compare.estimate(frozen, plan, judge=True)
                sizes = cost["judgeInputTokensEstimateByCase"]
                self.assertEqual(set(sizes), {c["id"] for c in frozen["cases"]["cases"]})
                self.assertGreater(sizes["explicit-system-question"], sizes["concrete-gaps-next-step"])
                self.assertGreater(sizes["concrete-gaps-next-step"], sizes["missing-evidence-no-report"])
                self.assertIn("prepared judge payloads", cost["method"])
                self.assertNotIn("judge expected 6k", cost["method"])
                self.assertEqual(30, cost["judgeCalls"])
                # The sizing record is estimation-only and matches what judge_input would really build.
                record = compare.assumed_judge_record(frozen, plan[0], compare.ASSUMED_ANSWER_CHARS)
                payload = compare.judge_input(frozen, record, "estimate")
                self.assertIn("systemContext", payload)
        legacy = compare.estimate(compare.load_frozen(OLD, NEW, "pr97-4313-legacy"),
                                  compare.plan_attempts(compare.load_frozen(OLD, NEW, "pr97-4313-legacy")["cases"]["cases"], 3), True)
        self.assertGreater(legacy["judgeInputTokensEstimateByCase"]["explicit-system-question"], 6000)

    def test_pr98_estimate_keeps_its_fixed_historical_judge_assumption(self):
        frozen = compare.load_frozen(OLD, NEW)
        cost = compare.estimate(frozen, compare.plan_attempts(frozen["cases"]["cases"], 3), judge=True)
        self.assertIn("judge expected 6k in/800 out", cost["method"])
        self.assertNotIn("judgeInputTokensEstimateByCase", cost)

    def test_estimate_does_not_touch_the_budget_guard(self):
        frozen = compare.load_frozen(OLD, NEW, "pr97-4313-legacy")
        self.assertEqual(5, frozen["cases"]["run"]["proposedCeilingUsd"])
        report = compare.preflight(args_for("pr97-4313-legacy"))
        self.assertEqual(report["cost"]["guard"]["kind"], "enforced reservation")
        self.assertIn("--max-spend-usd 5 ", report["executeCommand"])


class DefaultSuiteTests(unittest.TestCase):
    def test_pr98_defaults_are_unchanged(self):
        args = compare.parse_args([])
        self.assertEqual(("pr98-4308", compare.DEFAULT_OLD_REVISION, compare.DEFAULT_NEW_REVISION, 4308),
                         (args.suite, args.old_revision, args.new_revision, args.seed))
        pr97 = compare.parse_args(["--suite", "pr97-4313-legacy"])
        self.assertEqual((compare.PR97_OLD_REVISION, compare.PR97_NEW_REVISION, 4313),
                         (pr97.old_revision, pr97.new_revision, pr97.seed))


def have(revision: str) -> bool:
    return not subprocess.run(["git", "cat-file", "-e", f"{revision}^{{commit}}"], cwd=ROOT, capture_output=True).returncode


@unittest.skipUnless(have(compare.PR97_NEW_REVISION), "PR #97 head not fetched (git fetch origin pull/97/head)")
class FrozenPr97IdentityTests(unittest.TestCase):
    EXPECTED = {"pr97-4313-pipeline": ("1.0.6", "5005c16a8322dab38ca4f76173de5a3d078c7231", "1.0.7", "52d0a9c326cc56b6490ff2d2c5b1399ea293ca77"),
                "pr97-4313-legacy": ("1.0.4", "25538e60d675da54c39fd965bb457ad39a6806d8", "1.0.5", "33412df164b1c0a189468199228a855444ac0a76")}

    def test_real_pr97_blobs_and_prompt_only_change(self):
        for suite, (old_version, old_blob, new_version, new_blob) in self.EXPECTED.items():
            with self.subTest(suite=suite):
                frozen = compare.load_frozen(compare.PR97_OLD_REVISION, compare.PR97_NEW_REVISION, suite)
                self.assertEqual([], frozen["problems"])
                templates = frozen["identity"]["templates"]
                self.assertEqual((old_version, old_blob, new_version, new_blob),
                                 (templates["old"]["version"], templates["old"]["gitBlob"],
                                  templates["new"]["version"], templates["new"]["gitBlob"]))
                self.assertIn("## User-facing language", frozen["parsed"]["new"]["prompt"]["template"])
                self.assertNotIn("## User-facing language", frozen["parsed"]["old"]["prompt"]["template"])


if __name__ == "__main__":
    unittest.main()
