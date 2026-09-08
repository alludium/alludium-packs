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

    def test_candidate_identity_stays_in_relationship_not_deal_fields(self):
        task = yaml.safe_load((ROOT / "alludium/task-definition-templates/vc-workflows/promote-candidate-to-deal-pipeline.yaml").read_text())
        instructions = task["definition"]["definitionJson"]["instructions"]["executionInstructions"]
        proposal = next(field for field in task["fields"]["output"] if field["key"] == "dealCreationProposal")
        field_values_schema = proposal["config"]["schema"]["properties"]["createRequest"]["properties"]["fieldValues"]

        self.assertIn("never add `origination_candidate_project_id` to `createRequest.fieldValues`", instructions)
        self.assertEqual(
            field_values_schema["not"]["required"],
            ["origination_candidate_project_id"],
        )

    def test_promotion_requires_canonical_non_empty_company_name(self):
        task = yaml.safe_load((ROOT / "alludium/task-definition-templates/vc-workflows/promote-candidate-to-deal-pipeline.yaml").read_text())
        instructions = task["definition"]["definitionJson"]["instructions"]
        proposal = next(field for field in task["fields"]["output"] if field["key"] == "dealCreationProposal")
        proposal_config = proposal["config"]
        schema = proposal_config["schema"]
        create_request_schema = schema["properties"]["createRequest"]
        field_values_schema = create_request_schema["properties"]["fieldValues"]

        self.assertEqual(task["version"], "0.1.17")
        self.assertIn("createRequest.fieldValues.company_name", proposal_config["requiredPaths"])
        self.assertIn("createRequest", schema["required"])
        self.assertIn("fieldValues", create_request_schema["required"])
        self.assertIn("company_name", field_values_schema["required"])
        self.assertEqual(
            field_values_schema["properties"]["company_name"],
            {"type": "string", "minLength": 1},
        )
        self.assertIn("canonical company name", instructions["executionInstructions"])
        self.assertIn("canonical non-empty `company_name`", instructions["missingInputPolicy"])

if __name__ == "__main__":
    unittest.main()
