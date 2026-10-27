"""Approved v5 catalogue (#4347) with the first-cutover compatibility boundary (#4625)."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

import validate_pack as validator


ROOT = Path(__file__).resolve().parents[1]
PIPELINE = ROOT / "alludium/project-types/vc_deal_pipeline.json"
APPROVED = ROOT / "scripts/fixtures/vc-deal-pipeline-approved-v5-catalogue.json"
LEGACY_COMPANY = {"company_name", "company_domain", "company_logo_url"}
# Added after the approved catalogue: the CRM history document pointer (#4841).
CRM_HISTORY = "crm_history_artifact_id"


class PipelineCatalogueTests(unittest.TestCase):
    def setUp(self) -> None:
        self.project = json.loads(PIPELINE.read_text())
        self.version = self.project["initialVersion"]
        self.fields = {field["key"]: field for field in self.version["fieldsSchema"]}
        self.groups = self.version["extensions"]["projectDataSections"]

    def validate(self) -> None:
        for field in self.version["fieldsSchema"]:
            validator.validate_project_type_field("vc_deal_pipeline", field)
        validator.validate_project_field_layout("vc_deal_pipeline", self.version)

    def test_matches_the_approved_catalogue_plus_legacy_compatibility(self) -> None:
        approved = json.loads(APPROVED.read_text())
        self.assertEqual(
            [
                field
                for field in self.version["fieldsSchema"]
                if field["key"] not in LEGACY_COMPANY and field["key"] != CRM_HISTORY
            ],
            approved["fieldsSchema"],
        )
        groups = copy.deepcopy(self.groups)
        for group in groups:
            group["fieldKeys"] = [key for key in group["fieldKeys"] if key != CRM_HISTORY]
        self.assertEqual(groups, approved["extensions"]["projectDataSections"])
        self.assertEqual(len(self.fields), 35)
        self.assertEqual(
            self.fields[CRM_HISTORY],
            {
                "id": "field-crm-history-artifact-id",
                "key": CRM_HISTORY,
                "label": "CRM history and context",
                "kind": "text",
                "required": False,
                "description": "Internal pointer to the current CRM history and context document for this Deal.",
                "settingsPolicy": "excluded",
            },
        )
        assessment = next(group for group in self.groups if group["key"] == "assessment_documents")
        self.assertEqual(assessment["fieldKeys"][-1], CRM_HISTORY)
        for key in LEGACY_COMPANY:
            self.assertEqual(self.fields[key]["id"], "field-" + key.replace("_", "-"))
            self.assertEqual(self.fields[key]["kind"], "text")
            self.assertFalse(self.fields[key]["required"])
            self.assertEqual(self.fields[key]["settingsPolicy"], "excluded")
        self.validate()

    def test_creation_and_summaries_do_not_read_retired_fields(self) -> None:
        creation = self.project["projectCreation"]
        self.assertEqual(creation["recommendedFieldKeys"], ["fund_id", "deal_source"])
        self.assertEqual(creation["requiredFieldKeys"], [])
        self.assertEqual(creation["advancedFieldKeys"], [])
        command = self.version["commandView"]
        self.assertNotIn("primarySummaryField", command)
        self.assertNotIn("secondarySummaryField", command)
        self.assertEqual(command["badgeFields"], [])
        validator.validate_project_command_view_platform_contract(
            "vc_deal_pipeline", self.version, set(self.fields), set(self.version["lifecycleStates"])
        )

    def test_rejects_invalid_relationship_declarations(self) -> None:
        for key, changes in [
            ("introducer", {"cardinality": "many"}),
            ("introducer", {"relationshipType": "round_investor"}),
            ("introducer", {"required": True}),
            ("introducer", {"options": []}),
            ("introducer", {"optionSource": {}}),
            ("introducer", {"roleOptions": []}),
            ("introducer", {"relationshipType": None}),
            ("introducer", {"key": "founder"}),
            ("other_investors", {"roleOptions": []}),
            ("other_investors", {"roleOptions": [{"value": "non_lead", "label": "Investor"}] * 3}),
            ("arr", {"cardinality": "one"}),
            ("arr", {"settingsPolicy": "hidden"}),
            ("arr", {"settingsPolicy": []}),
        ]:
            with self.subTest(key=key, changes=changes), self.assertRaises(SystemExit):
                validator.validate_project_type_field("vc_deal_pipeline", {**self.fields[key], **changes})

    def test_rejects_invalid_groups(self) -> None:
        mutations = [
            lambda groups: groups.append(copy.deepcopy(groups[0])),
            lambda groups: groups[1]["fieldKeys"].append("missing"),
            lambda groups: groups[1]["fieldKeys"].append("round_stage"),
            lambda groups: groups[1]["fieldKeys"].remove("round_stage"),
            lambda groups: groups[1].update(settingsPolicy="excluded"),
            lambda groups: groups[1].update(settingsPolicy="hidden"),
            lambda groups: groups[1].update(settingsPolicy=[]),
            lambda groups: groups[1].update(key=" round_dynamics "),
            lambda groups: groups[1].update(label=" " * 2),
            lambda groups: groups[1].update(label="x" * 81),
            lambda groups: groups[1].update(fallback=True),
        ]
        for index, mutate in enumerate(mutations):
            with self.subTest(case=index), self.assertRaises(SystemExit):
                version = copy.deepcopy(self.version)
                mutate(version["extensions"]["projectDataSections"])
                validator.validate_project_field_layout("vc_deal_pipeline", version)

    def test_legacy_types_without_layouts_remain_supported(self) -> None:
        validator.validate_project_field_layout("legacy", {
            "fieldsSchema": [{"id": "old", "key": "old", "kind": "text", "required": False}],
        })

    def test_relationship_fields_are_restricted_to_deal_types(self) -> None:
        with self.assertRaises(SystemExit):
            validator.validate_project_type_field("vc_origination_candidate", self.fields["introducer"])

    def test_policy_declarations_require_a_layout_for_managed_fields(self) -> None:
        self.version["extensions"].pop("projectDataSections")
        with self.assertRaises(SystemExit):
            self.validate()

    def test_existing_task_and_decision_contracts_still_hold(self) -> None:
        validator.validate_vc_deal_pipeline_contract()


if __name__ == "__main__":
    unittest.main()
