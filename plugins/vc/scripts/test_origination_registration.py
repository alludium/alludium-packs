"""Keep guided registration instructions consistent with the output contract."""
import unittest
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]

class RegistrationContractTests(unittest.TestCase):
    def test_proposal_shape_and_identity_checks_match_the_native_contract(self):
        task = yaml.safe_load((ROOT / "alludium/task-definition-templates/vc-workflows/register-origination-candidate.yaml").read_text())
        output = next(field for field in task["fields"]["output"] if field["key"] == "projectCreation")
        instructions = task["definition"]["definitionJson"]["instructions"]["executionInstructions"]
        self.assertIn("fieldValues.company_name", output["config"]["requiredPaths"])
        self.assertIn("relationships", output["config"]["requiredPaths"])
        self.assertIn("`fieldValues` at its root", instructions)
        self.assertNotIn("emit `projectCreation.createRequest`", instructions)
        self.assertIn("text fields must be strings", instructions)
        self.assertIn("`collection: active`", instructions)
        self.assertIn("`collection: portfolio`", instructions)
        self.assertIn('"key":"candidate_key"', instructions)

class ScoringConcurrencyContractTests(unittest.TestCase):
    def test_scoring_uses_prior_metadata_and_bounded_conflict_recovery(self):
        task = yaml.safe_load((ROOT / "alludium/task-definition-templates/vc-workflows/score-sourcing-candidate.yaml").read_text())
        instructions = task["definition"]["definitionJson"]["instructions"]["executionInstructions"]
        self.assertIn("`expectedMetadata`", instructions)
        self.assertIn("unchanged prior snapshot", instructions)
        self.assertIn("returns409 conflict", instructions)
        self.assertIn("retry once", instructions)
        self.assertIn("never perform an unconditional overwrite", instructions)
        self.assertIn("every existing `scoring_by_fund` entry unchanged", instructions)

if __name__ == "__main__":
    unittest.main()
