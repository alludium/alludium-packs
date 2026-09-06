"""Prevent Pack instructions from weakening the Platform run-attribution contract."""
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_task(name):
    return yaml.safe_load((ROOT / "alludium/task-definition-templates/vc-workflows" / name).read_text())


class OriginationRunAttributionTests(unittest.TestCase):
    def test_manual_registration_does_not_require_a_run(self):
        task = load_task("register-origination-candidate.yaml")
        inputs = {field["key"]: field for field in task["fields"]["input"]}
        self.assertFalse(inputs["sourcing_run_task_id"]["required"])
        self.assertEqual(inputs["sourcing_run_task_id"]["fieldType"], "string")
        self.assertEqual({key for key, field in inputs.items() if field["required"]},
                         {"company_name", "sourcing_line_project_id", "source_evidence"})
        instructions = task["definition"]["definitionJson"]["instructions"]["executionInstructions"]
        self.assertIn("Standalone/manual registration omits this optional input and remains valid", instructions)
        self.assertIn("rather than silently dropping it", instructions)

    def test_run_derived_registration_preserves_the_exact_parent_run(self):
        task = load_task("run-vc-sourcing-pipeline.yaml")
        instructions = task["definition"]["definitionJson"]["instructions"]["executionInstructions"]
        self.assertIn("as `sourcing_run_task_id`", instructions)
        self.assertIn("supported guided Register launcher", instructions)
        self.assertIn("do not substitute a source child task ID", instructions)

    def test_proposals_and_legacy_line_fields_are_not_committed_outcomes(self):
        task = load_task("run-vc-sourcing-pipeline.yaml")
        instructions = task["definition"]["definitionJson"]["instructions"]["executionInstructions"]
        self.assertNotIn("call `project.update` for the exact Sourcing Line", instructions)
        self.assertIn("Do not call `project.update` to write", instructions)
        self.assertIn("a `projectCreation` proposal is not a created Candidate", instructions)
        self.assertIn("proposed/created/reused/rejected/failed", instructions)
        self.assertIn("Missing finalization evidence means unknown, not success", instructions)
        outputs = {field["key"]: field for field in task["fields"]["output"]}
        self.assertEqual(outputs["new_candidates_count"]["name"], "Proposed New Candidates Count")
        for key in ("run_receipt_artifact_id", "candidate_batch_artifact_id", "source_state_artifact_id"):
            self.assertTrue(outputs[key]["required"])
            self.assertEqual(outputs[key]["fieldType"], "file")


if __name__ == "__main__":
    unittest.main()
