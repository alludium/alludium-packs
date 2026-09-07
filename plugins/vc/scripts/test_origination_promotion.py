import unittest
import json
import yaml
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

class PromotionContractTests(unittest.TestCase):
    def test_candidate_declares_current_deal_target_and_defers_state_to_platform(self):
        project = json.loads((ROOT / "alludium/project-types/vc_origination_candidate.json").read_text())
        relation = next(edge for edge in project["initialVersion"]["extensions"]["projectRelationships"] if edge["typeKey"] == "vc.origination_candidate_promoted_to_deal")
        self.assertIn("vc_deal_pipeline", relation["targetProjectTypeKeys"])
        task = yaml.safe_load((ROOT / "alludium/task-definition-templates/vc-workflows/promote-candidate-to-deal-pipeline.yaml").read_text())
        instructions = task["definition"]["definitionJson"]["instructions"]["executionInstructions"]
        self.assertIn("Omit guessed project type UUIDs and lifecycle state", instructions)
        self.assertIn("Review and create Deal", instructions)

if __name__ == "__main__":
    unittest.main()
