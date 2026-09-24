#!/usr/bin/env python3
"""Offline checks for the --suite-file interface and the requestsInput assertion; every provider is mocked."""
from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import yaml

import compare_deal_manager_prompts as compare
from test_deal_manager_prompt_comparison import NEW, OLD, FakeGit, Policy
from test_deal_manager_guidance_comparison import Advisor, FakeGit as GuidanceGit, score_judge

HERE = Path(__file__).resolve().parent
FIXTURES = "plugins/vc/scripts/fixtures"
BUILT_IN = set(compare.SUITES)


def suite_spec(**overrides) -> dict:
    """A new suite that reuses the PR #98 optional-context kind and its frozen fixtures under a new identity."""
    spec = {"schemaVersion": "0.1", "id": "test-new-issue-case", "kind": "optional-context", "issue": "4308",
            "templateId": "vc_deal_pipeline_manager", "revisions": {"old": OLD, "new": NEW}, "seed": 7,
            "cases": f"{FIXTURES}/deal-manager-4308-cases.yaml",
            "expectations": f"{FIXTURES}/deal-manager-4308-expectations.yaml",
            "toolContract": f"{FIXTURES}/deal-manager-tool-contract.json"}
    return {**spec, **overrides}


def record_with_final(text: str) -> dict:
    return {"status": "completed", "turns": [{"index": 0, "complete": True, "calls": [], "texts": [text], "final": text}]}


class SuiteFileTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        for suite_id in set(compare.SUITES) - BUILT_IN:
            del compare.SUITES[suite_id]
        self.tmp.cleanup()

    def write(self, spec: dict, name: str = "suite.yaml") -> Path:
        path = self.dir / name
        path.write_text(yaml.safe_dump(spec, sort_keys=False))
        return path

    def test_registers_new_suite_and_preflights_without_provider_calls(self):
        path = self.write(suite_spec())
        with FakeGit():
            args = compare.parse_args(["--suite-file", str(path)])
            report = compare.preflight(args)
        self.assertEqual(args.suite, "test-new-issue-case")
        self.assertEqual((args.old_revision, args.new_revision, args.seed), (OLD, NEW, 7))
        self.assertEqual(report["providerCalls"], 0)
        self.assertTrue(report["preparationReady"], report["blockingProblems"])
        self.assertEqual(report["identity"]["suite"], "test-new-issue-case")
        self.assertEqual(report["identity"]["suiteFile"]["sha256"], compare.sha(path.read_text()))
        self.assertIn(f"--suite-file {path} ", report["executeCommand"])
        self.assertEqual(report["counts"]["attempts"], 36)

    def test_built_in_suite_identity_has_no_suite_file_key(self):
        with FakeGit():
            report = compare.preflight(compare.parse_args(["--old-revision", OLD, "--new-revision", NEW]))
        self.assertNotIn("suiteFile", report["identity"])
        self.assertNotIn("--suite", report["executeCommand"])

    def test_suite_file_and_suite_are_mutually_exclusive(self):
        path = self.write(suite_spec())
        with self.assertRaises(SystemExit):
            compare.parse_args(["--suite", "pr97-4313-legacy", "--suite-file", str(path)])

    def test_same_file_registers_idempotently_but_a_different_file_cannot_reuse_the_id(self):
        path = self.write(suite_spec())
        self.assertEqual(compare.register_suite_file(path), compare.register_suite_file(path))
        other = self.write(suite_spec(seed=8), "other.yaml")
        with self.assertRaisesRegex(SystemExit, "already a registered suite"):
            compare.register_suite_file(other)

    def test_rejects_invalid_declarations_before_any_provider_access(self):
        cases = [
            (suite_spec(id="pr98-4308"), "already a registered suite"),
            (suite_spec(kind="free-form"), "a new kind needs runner code"),
            (suite_spec(cases="/etc/hosts"), "repository-relative"),
            (suite_spec(expectations="../outside.yaml"), "repository-relative"),
            (suite_spec(toolContract=f"{FIXTURES}/missing.json"), "file not found"),
            (suite_spec(revisions={"old": OLD}), "revisions must map exactly old and new"),
            (suite_spec(seed="7"), "seed must be an integer"),
            (suite_spec(prompt="inline prompt"), "unknown key prompt"),
            ({k: v for k, v in suite_spec().items() if k != "issue"}, "missing key issue"),
        ]
        for spec, message in cases:
            with self.subTest(message=message), self.assertRaisesRegex(SystemExit, message):
                compare.register_suite_file(self.write(spec))

    def test_new_issue_namespaces_simulated_definition_ids_consistently(self):
        path = self.write(suite_spec(issue="SYN-1"))
        with FakeGit():
            frozen = compare.load_frozen(OLD, NEW, compare.parse_args(["--suite-file", str(path)]).suite)
        case = frozen["cases"]["cases"][0]
        catalog_ids = set(compare.make_simulator(frozen, case).catalog)
        identity_ids = {meta["id"] for meta in frozen["identity"]["taskDefinitions"].values()}
        self.assertEqual(catalog_ids, identity_ids)
        self.assertEqual(catalog_ids, {compare.definition_id(slug, "SYN-1") for slug in frozen["definitions"]})

    def test_mocked_execution_records_the_suite_file_identity(self):
        path = self.write(suite_spec())
        output = self.dir / "run"
        with FakeGit():
            args = compare.parse_args(["--suite-file", str(path), "--output", str(output), "--max-spend-usd", "5", "--execute"])
            manifest = compare.execute(args, invoke=Policy())
        self.assertEqual(manifest["executionStatus"], "complete")
        run = json.loads((output / "run.json").read_text())
        self.assertEqual(run["identity"]["suiteFile"], manifest["identity"]["suiteFile"])
        self.assertIn("test-new-issue-case", json.dumps(run["identity"]))
        self.assertIn("Platform issue #4308", (output / "report.md").read_text())

    def test_judge_resume_refuses_a_changed_suite_file(self):
        path = self.write(suite_spec())
        output = self.dir / "run"
        with FakeGit():
            compare.execute(compare.parse_args(["--suite-file", str(path), "--output", str(output), "--max-spend-usd", "5",
                                                "--execute"]), invoke=Policy())
            summary = json.loads((output / "summary.json").read_text())
            summary["identity"]["suiteFile"]["sha256"] = "0" * 64
            (output / "summary.json").write_text(json.dumps(summary))
            args = compare.parse_args(["--suite-file", str(path), "--judge-run", str(output), "--max-spend-usd", "5"])
            with self.assertRaisesRegex(SystemExit, "suiteFile"):
                compare.judge_existing(args, invoke=lambda *a: self.fail("no provider call expected"))


class RequestsInputTests(unittest.TestCase):
    EXPECTATIONS = {"cases": {"c": {"creates": {"total": 0}, "requestsInput": {"topic": "termSheet"}}}}
    FROZEN_RULE = {"cases": {"c": {"creates": {"total": 0}, "asksAbout": {"topic": "termSheet"}}}}

    def errors(self, text: str, expectations: dict | None = None) -> list[str]:
        return [e for e in compare.score(expectations or self.EXPECTATIONS, "c", record_with_final(text))["errors"]
                if e.startswith(("requestsInput", "asksAbout"))]

    def test_accepts_questions_and_direct_requests(self):
        for text in ("Please upload a readable current term sheet for Terraview; it is required to run the review.",
                     "Could you upload the term sheet?",
                     "I'll need the term sheet before I can start the Term Sheet Review.",
                     "The review is blocked.\n- Upload the current term sheet and I'll start it.",
                     "Once you've uploaded the term sheet, I can run the review.",
                     "Kindly share the signed term sheet when it arrives."):
            with self.subTest(text=text):
                self.assertEqual(self.errors(text), [])

    def test_rejects_statements_wrong_topics_and_claims(self):
        for text in ("I can't run the Term Sheet Review without the term sheet.",
                     "The term sheet has not been uploaded yet.",
                     "Please upload the deck again.",
                     "I've started the Term Sheet Review using the deck.",
                     "Which Fund is this for? The term sheet is missing."):
            with self.subTest(text=text):
                self.assertEqual(len(self.errors(text)), 1)

    def test_frozen_asks_about_rule_is_unchanged(self):
        self.assertEqual(len(self.errors("Please upload the term sheet.", self.FROZEN_RULE)), 1)
        self.assertEqual(self.errors("Could you upload the term sheet?", self.FROZEN_RULE), [])

    def test_requests_input_is_an_accepted_assertion_key(self):
        self.assertIn("requestsInput", compare.ASSERTIONS)


class JudgeResumeCaseIdentityTests(unittest.TestCase):
    """--judge-run must refuse when the cases behind a suite file changed, even with the same suite YAML and case IDs."""

    FACT = "EUR 180k ARR"

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve() / "repo"
        fixtures = self.root / FIXTURES
        fixtures.mkdir(parents=True)
        for name in ("deal-manager-4313-cases.yaml", "deal-manager-4313-expectations.yaml",
                     "deal-manager-legacy-tool-contract.json"):
            shutil.copy(HERE / "fixtures" / name, fixtures / name)
        self.cases = fixtures / "deal-manager-4313-cases.yaml"
        self.suite = Path(self.tmp.name) / "suite.yaml"
        self.suite.write_text(yaml.safe_dump(suite_spec(
            id="test-resume-guidance", kind="guidance", issue="4313", templateId="vc_deal_manager",
            cases=f"{FIXTURES}/deal-manager-4313-cases.yaml", expectations=f"{FIXTURES}/deal-manager-4313-expectations.yaml",
            toolContract=f"{FIXTURES}/deal-manager-legacy-tool-contract.json"), sort_keys=False))
        root_patch = mock.patch.object(compare, "ROOT", self.root)
        root_patch.start()
        self.addCleanup(root_patch.stop)
        git = GuidanceGit().__enter__()
        self.addCleanup(git.__exit__)
        self.addCleanup(lambda: [compare.SUITES.pop(suite_id) for suite_id in set(compare.SUITES) - BUILT_IN])
        self.out = Path(self.tmp.name) / "run"
        self.first = compare.execute(compare.parse_args(["--suite-file", str(self.suite), "--output", str(self.out),
                                                         "--max-spend-usd", "5", "--execute"]), invoke=Advisor())
        self.calls = {"judge": 0, "subject": 0}

    def invoke(self, request, path, settings):
        if "modelId" not in request or "messages" not in request:
            self.calls["subject"] += 1
            raise AssertionError("subject dispatched during judge resume")
        self.calls["judge"] += 1
        return score_judge(request)

    def resume(self):
        return compare.judge_existing(compare.parse_args(["--suite-file", str(self.suite), "--judge-run", str(self.out),
                                                          "--max-spend-usd", "5"]), invoke=self.invoke)

    def test_edited_case_fact_is_refused_before_any_dispatch(self):
        text = self.cases.read_text()
        self.assertIn(self.FACT, text)
        self.cases.write_text(text.replace(self.FACT, "EUR 900k ARR"))
        suite_before = self.suite.read_bytes()
        with self.assertRaisesRegex(SystemExit, "casesExceptJudgeSha256"):
            self.resume()
        self.assertEqual(self.suite.read_bytes(), suite_before)
        self.assertEqual(self.calls, {"judge": 0, "subject": 0})
        self.assertFalse((self.out / "judge-2").exists())
        self.assertEqual(self.first["records"], json.loads((self.out / "summary.json").read_text())["records"])

    def test_unchanged_inputs_resume_with_judge_calls_only(self):
        summary = self.resume()
        self.assertEqual(self.calls, {"judge": 30, "subject": 0})
        self.assertEqual("complete", summary["executionStatus"])
        self.assertEqual(self.first["identity"]["casesExceptJudgeSha256"], summary["judgePhase"]["casesExceptJudgeSha256"])

    def test_judge_configuration_repair_alone_stays_resumable(self):
        parsed = yaml.safe_load(self.cases.read_text())
        parsed["run"]["judge"]["maxTokens"] = 1024
        self.cases.write_text(yaml.safe_dump(parsed, sort_keys=False))
        summary = self.resume()
        self.assertEqual(self.calls["subject"], 0)
        self.assertEqual(1024, summary["judgePhase"]["judgeConfig"]["maxTokens"])
        self.assertNotEqual(self.first["identity"]["casesSha256"], summary["judgePhase"]["casesSha256"])

    def test_run_recorded_before_the_field_requires_byte_identical_cases(self):
        summary = json.loads((self.out / "summary.json").read_text())
        del summary["identity"]["casesExceptJudgeSha256"]
        (self.out / "summary.json").write_text(json.dumps(summary))
        parsed = yaml.safe_load(self.cases.read_text())
        parsed["run"]["judge"]["maxTokens"] = 1024
        self.cases.write_text(yaml.safe_dump(parsed, sort_keys=False))
        with self.assertRaisesRegex(SystemExit, "casesSha256"):
            self.resume()
        self.assertEqual(self.calls, {"judge": 0, "subject": 0})


if __name__ == "__main__":
    unittest.main()
