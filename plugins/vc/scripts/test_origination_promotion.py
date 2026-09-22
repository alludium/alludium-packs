import unittest
import json
import yaml
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

class PromotionContractTests(unittest.TestCase):
    def test_candidate_manager_receives_canonical_fund_mandates(self):
        manager = yaml.safe_load((ROOT / "alludium/agent-templates/vc_origination_candidate_manager.yaml").read_text())
        prompt = manager["prompt"]
        funds = next(variable for variable in prompt["variables"] if variable["key"] == "funds")
        self.assertEqual(funds["type"], "array")
        self.assertEqual(funds["value"], [])
        self.assertEqual(funds["binding"], {
            "source": "workspace.variable",
            "path": "vc.funds",
            "fallback": [],
            "overridePolicy": "workspace_admin_only",
        })

        # A declared binding alone leaves the manager blind unless the prompt renders it.
        fund_block = prompt["template"].split("{{#each funds}}", 1)[1].split("{{/each}}", 1)[0]
        for field in ("id", "name", "status", "stage", "sectors", "geographies", "thesis",
                      "minimumCheckSize", "maximumCheckSize", "currency", "exclusions", "scoringFramework"):
            self.assertIn("{{" + field + "}}", fund_block)
        self.assertIn("{{else}}", fund_block)
        self.assertIn("No configured Funds.", fund_block)
        self.assertIn("whose status is `actively_investing`", prompt["template"])
        self.assertIn("selected Fund is unknown or inactive", prompt["template"])
        self.assertIn("user to explicitly choose the exact active target Fund", prompt["template"])

        generated = (ROOT / "agents/vc-origination-candidate-manager.md").read_text()
        self.assertIn(fund_block, generated)
        self.assertIn("workspace binding `vc.funds`", generated)

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
        generated_task = (ROOT / "tasks/promote-candidate-to-deal-pipeline.md").read_text()
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
        self.assertIn(
            "`dealCreationProposal.createRequest.fieldValues.company_name`",
            generated_task,
        )
        self.assertNotIn(
            "`dealCreationProposal.createRequest.fieldValues.company name`",
            generated_task,
        )

if __name__ == "__main__":
    unittest.main()
