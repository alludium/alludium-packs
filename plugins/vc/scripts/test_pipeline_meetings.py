"""Cross-contract regressions for Pipeline meeting routing and output isolation (#4998)."""
from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml
import validate_pack as validator

ROOT = Path(__file__).resolve().parents[1]
PROJECT = "alludium/project-types/vc_deal_pipeline.json"
PREP = "alludium/task-definition-templates/vc-workflows/prepare-pipeline-meeting.yaml"
SUMMARY = "alludium/task-definition-templates/vc-workflows/summarize-pipeline-meeting.yaml"
ANALYST = "alludium/agent-templates/vc_deal_analyst.yaml"


class PipelineMeetingTests(unittest.TestCase):
    def test_current_contract_and_catalogue(self) -> None:
        validator.validate_vc_deal_pipeline_contract()
        catalogue = json.loads((ROOT / "alludium/task-definition-templates/catalog.v1.json").read_text())
        registered = {p for pack in catalogue["packs"] for p in pack["templates"]}
        for slug in validator.PIPELINE_MEETING_TASKS:
            self.assertIn(f"vc-workflows/{slug}.yaml", registered)

    def reject(self, path, mutate) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "vc"
            shutil.copytree(ROOT / "alludium", root / "alludium")
            target = root / path
            obj = yaml.safe_load(target.read_text())
            mutate(obj)
            target.write_text(json.dumps(obj) if path.endswith(".json") else yaml.safe_dump(obj))
            with patch.object(validator, "ROOT", root), self.assertRaises(SystemExit):
                validator.validate_pipeline_meeting_contract()

    def test_rejects_operator_on_locked_analyst_pipeline(self) -> None:
        for task in [PREP, SUMMARY]:
            for key in ["recommendedAgentTemplate", "plannedRecommendedAgentTemplate"]:
                with self.subTest(task=task, key=key):
                    self.reject(task, lambda t: t["definition"]["definitionJson"].update({key: "vc_meeting_operator"}))
            self.reject(task, lambda t: t["runtime"]["executionProfile"].update(preferredAgentType="vc_meeting_operator"))

    def test_rejects_legacy_company_identity_and_deck_activation_gate(self) -> None:
        self.reject(PROJECT, lambda p: p["initialVersion"]["projectTaskMappings"][-1]["inputMappings"][0].update(source="project.field", sourcePath="company_name"))
        self.reject(PROJECT, lambda p: p["initialVersion"]["projectTaskMappings"][-2]["inputMappings"].append({"taskField": "pitch_deck_artifact_id", "source": "project.field", "sourcePath": "pitch_deck_artifact_id", "requiredForActivation": True}))
        self.reject(PREP, lambda t: next(f for f in t["fields"]["input"] if f["key"] == "pitch_deck_artifact_id").update(required=True))

    def test_rejects_singleton_report_overwrite(self) -> None:
        self.reject(PROJECT, lambda p: p["initialVersion"]["projectTaskMappings"][-1].update(outputMappings=[{"taskField": "meeting_summary_artifact_id", "target": "project.field", "targetPath": "screening_report_artifact_id"}]))
        self.reject(SUMMARY, lambda t: t["fields"]["output"][0].update(required=False))

    def test_rejects_stage_trigger_and_missing_human_review(self) -> None:
        self.reject(PROJECT, lambda p: p["initialVersion"]["projectTaskMappings"][-1]["activationPolicy"].update(createTaskWhenLifecycleStageEntered=True))
        self.reject(SUMMARY, lambda t: t["runtime"]["executionProfile"].update(requiresHumanConfirmationToComplete=False))

    def test_rejects_missing_skill_or_template(self) -> None:
        self.reject(ANALYST, lambda a: a.update(skills=[s for s in a["skills"] if s["externalId"] != "meeting-prep-and-summary"]))
        self.reject(PROJECT, lambda p: p["initialVersion"]["documentLibrary"]["documentIds"].remove("vc.document.initial_call_brief_template"))

    def test_legacy_room_tasks_keep_their_executor(self) -> None:
        for name in ["prepare-meeting", "summarize-meeting-records"]:
            task = yaml.safe_load((ROOT / f"alludium/task-definition-templates/vc-workflows/{name}.yaml").read_text())
            self.assertEqual(task["definition"]["definitionJson"]["supportedProjectTypes"], ["vc_deal_room"])
            self.assertEqual(task["runtime"]["executionProfile"]["preferredAgentType"], "vc_meeting_operator")


if __name__ == "__main__":
    unittest.main()
