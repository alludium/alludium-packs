"""Guard regressions: refuse drift or unreviewed failure before launching a client."""
import importlib.util
import fcntl
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

spec = importlib.util.spec_from_file_location("agent_eval", Path(__file__).with_name("run.py"))
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class Guards(unittest.TestCase):
    def fixture(self, root):
        directory = root / "cell"
        directory.mkdir()
        for name in runner.INPUT_FILES:
            (directory / name).write_text("[]")
        cell = {"id": "cell", "client": "codex", "case": "C01", "guidance": "packs", "input_hashes": runner.input_hashes(directory)}
        (root / "preflight.json").write_text(json.dumps({"cells": [cell], "source_hashes": {"source": "pinned"}}))
        core = SimpleNamespace(clean_env=Mock(), attest=Mock(), reserve=Mock(), run_bounded=Mock())
        return directory, core

    def test_declared_pack_revision_matches_actual_templates(self):
        runner.verify_source_revision()

    def test_unresolved_prompt_variable_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Unresolved"):
            runner.render({"prompt": {"template": "Hello {{missing}}"}}, {})

    def test_source_drift_never_attests_or_launches_client(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _, core = self.fixture(root)
            with patch.object(runner, "source_hashes", return_value={"source": "changed"}):
                with self.assertRaisesRegex(ValueError, "Frozen source changed"):
                    runner.execute(root, root, core)
            core.attest.assert_not_called()
            core.run_bounded.assert_not_called()

    def test_each_input_mutation_is_rejected_before_client_launch(self):
        for name in runner.INPUT_FILES:
            with self.subTest(input=name), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                directory, core = self.fixture(root)
                (directory / name).write_text("changed")
                with patch.object(runner, "source_hashes", return_value={"source": "pinned"}):
                    with self.assertRaisesRegex(ValueError, "Prepared subject input changed"):
                        runner.execute(root, root, core)
                core.attest.assert_not_called()
                core.reserve.assert_not_called()
                core.run_bounded.assert_not_called()

    def test_failed_turn_requires_diagnosis_and_is_not_retried(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            directory, core = self.fixture(root)
            (directory / "result.json").write_text(json.dumps({"returncode": 1, "stop_reason": None}))
            with patch.object(runner, "source_hashes", return_value={"source": "pinned"}):
                with self.assertRaisesRegex(ValueError, "Prior infrastructure failure"):
                    runner.execute(root, root, core)
                runner.execute(root, root, core, "Known client failure; retain this cell")
            self.assertTrue((directory / "continuation-diagnosis.json").exists())
            core.reserve.assert_not_called()
            core.run_bounded.assert_not_called()

    def test_interrupted_turn_never_retries(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            directory, core = self.fixture(root)
            (directory / "stdout.jsonl").touch()
            with patch.object(runner, "source_hashes", return_value={"source": "pinned"}):
                with self.assertRaisesRegex(ValueError, "Interrupted attempt"):
                    runner.execute(root, root, core)
            core.reserve.assert_not_called()
            core.run_bounded.assert_not_called()

    def test_predecessor_ledger_drift_never_launches(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _, core = self.fixture(root)
            ledger = root / "prior.jsonl"
            ledger.write_text("{}\n")
            preflight = json.loads((root / "preflight.json").read_text())
            preflight["prior_ledgers"] = {str(ledger): runner.digest(ledger)}
            (root / "preflight.json").write_text(json.dumps(preflight))
            ledger.write_text("{}\n{}\n")
            with patch.object(runner, "source_hashes", return_value={"source": "pinned"}):
                with self.assertRaisesRegex(ValueError, "Predecessor ledger changed"):
                    runner.execute(root, root, core)
            core.reserve.assert_not_called()
            core.run_bounded.assert_not_called()

    def test_reserved_attempt_without_capture_is_not_retried(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            directory, core = self.fixture(root)
            (root / "ledger.jsonl").write_text(json.dumps({"out": str(directory)}) + "\n")
            with patch.object(runner, "source_hashes", return_value={"source": "pinned"}):
                with self.assertRaisesRegex(ValueError, "Reserved attempt lacks result"):
                    runner.execute(root, root, core)
            core.reserve.assert_not_called()
            core.run_bounded.assert_not_called()

    def test_second_executor_cannot_enter_same_run(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _, core = self.fixture(root)
            with (root / "execution.lock").open("a") as lock:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                with self.assertRaisesRegex(ValueError, "active executor"):
                    runner.execute(root, root, core)
            core.reserve.assert_not_called()
            core.run_bounded.assert_not_called()

    def test_followup_requires_full_prior_exposure_before_auth(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            ledger = root / "prior.jsonl"
            ledger.write_text("{}\n")
            core = SimpleNamespace(clean_env=Mock(), attest=Mock())
            plan = {"ceilings": {"attempts": 4, "cumulative_attempts": 28}}
            with patch.object(runner, "PLAN", plan), patch.object(runner, "verify_source_revision"):
                with self.assertRaisesRegex(ValueError, "Predecessor attempts"):
                    runner.prepare(root / "output", root, core, [ledger])
            core.attest.assert_not_called()

    def test_published_receipts_keep_exact_runner_sources_and_cumulative_exposure(self):
        evidence = Path(__file__).parent / "evidence"
        baseline = json.loads((evidence / "baseline.json").read_text())
        clarified = json.loads((evidence / "clarified.json").read_text())
        for name, receipt in (("baseline", baseline), ("clarified", clarified)):
            self.assertEqual(runner.digest(evidence / (name + "-runner.py")), receipt["source_hashes"]["experiments/4968/run.py"])
            for agent in runner.PLAN["agents"]:
                relative = "plugins/vc/alludium/agent-templates/" + agent + ".yaml"
                if relative in receipt["source_hashes"]:
                    self.assertEqual(runner.digest(runner.ROOT / relative), receipt["source_hashes"][relative])
        self.assertEqual(clarified["predecessor_ledger_sha256"], [baseline["raw_sha256"]["ledger.jsonl"]])
        self.assertEqual(baseline["attempts_reserved"] + clarified["attempts_reserved"], 28)
        reviews = json.loads((evidence / "manual-review.json").read_text())["reviews"]
        self.assertEqual({(r["run"], r["cell"]) for r in reviews}, {(name, r["cell"]["id"]) for name, receipt in (("baseline", baseline), ("clarified", clarified)) for r in receipt["results"]})


if __name__ == "__main__":
    unittest.main()
