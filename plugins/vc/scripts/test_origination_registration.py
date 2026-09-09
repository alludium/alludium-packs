"""Keep guided registration instructions consistent with the output contract."""
import json
import unittest
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]

class RegistrationContractTests(unittest.TestCase):
    def test_dedupe_policy_is_available_before_candidate_creation(self):
        document_id = "vc.document.dedupe_novelty_policy"
        line = json.loads(
            (ROOT / "alludium/project-types/vc_sourcing_line.json").read_text()
        )
        catalog = json.loads(
            (ROOT / "alludium/documents/catalog.v1.json").read_text()
        )
        policy = next(
            document for document in catalog["documents"] if document["id"] == document_id
        )

        self.assertIn(
            document_id, line["initialVersion"]["documentLibrary"]["documentIds"]
        )
        self.assertIn("vc_sourcing_line", policy["supportedProjectTypes"])

    def test_proposal_shape_and_identity_checks_match_the_native_contract(self):
        task = yaml.safe_load((ROOT / "alludium/task-definition-templates/vc-workflows/register-origination-candidate.yaml").read_text())
        output = next(field for field in task["fields"]["output"] if field["key"] == "projectCreation")
        instructions = task["definition"]["definitionJson"]["instructions"]["executionInstructions"]
        self.assertIn("fieldValues.company_name", output["config"]["requiredPaths"])
        self.assertIn("relationships", output["config"]["requiredPaths"])
        schema = output["config"]["schema"]
        self.assertEqual(schema["type"], "object")
        self.assertEqual(set(schema["required"]), {"fieldValues", "relationships"})
        field_values = schema["properties"]["fieldValues"]
        self.assertEqual(
            set(field_values["required"]),
            {"company_name", "candidate_key", "source_evidence_summary"},
        )
        for field_key in field_values["required"]:
            self.assertEqual(field_values["properties"][field_key]["type"], "string")
        relationships = schema["properties"]["relationships"]
        self.assertEqual(
            relationships["items"]["properties"]["direction"]["enum"],
            ["incoming", "outgoing"],
        )
        self.assertNotIn("inbound", relationships["items"]["properties"]["direction"]["enum"])
        self.assertEqual(
            relationships["contains"]["properties"]["direction"]["const"], "incoming"
        )
        self.assertEqual(
            relationships["contains"]["properties"]["relationshipTypeKey"]["const"],
            "vc.sourcing_line_originated_candidate",
        )
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
