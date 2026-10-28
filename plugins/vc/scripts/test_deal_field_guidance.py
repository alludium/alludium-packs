"""Deal agents and tasks write fields only through the dedicated field tools (#4687).

`project_data` and `project.update` refuse agent field writes from 3.4.0 (#4394). Deal task agents
fill eligible empty Deal fields through the Platform Record Field Maintenance skill, so their
instructions must point at `field-values.setField`, must not teach a refused route, and must keep
CRM write prohibitions scoped to external systems.
"""

from __future__ import annotations

import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path

import yaml


SOURCE_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = SOURCE_ROOT / "scripts" / "validate_pack.py"
VALIDATOR_SPEC = importlib.util.spec_from_file_location("validate_pack", VALIDATOR_PATH)
if VALIDATOR_SPEC is None or VALIDATOR_SPEC.loader is None:  # pragma: no cover - test setup guard
    raise RuntimeError(f"Unable to load {VALIDATOR_PATH}")
VALIDATOR = importlib.util.module_from_spec(VALIDATOR_SPEC)
VALIDATOR_SPEC.loader.exec_module(VALIDATOR)

TEMPLATES = Path("alludium") / "agent-templates"
WORKFLOWS = Path("alludium") / "task-definition-templates" / "vc-workflows"
MEETING_TASK = WORKFLOWS / "summarize-meeting-records.yaml"
SCREENING_TASK = WORKFLOWS / "generate-refresh-screening-report.yaml"
MEETING_OPERATOR = TEMPLATES / "vc_meeting_operator.yaml"
PIPELINE_MANAGER = TEMPLATES / "vc_deal_pipeline_manager.yaml"
ANALYST = TEMPLATES / "vc_deal_analyst.yaml"


class DealFieldGuidanceTests(unittest.TestCase):
    def _copy_pack(self, temporary_root: str) -> Path:
        pack_root = Path(temporary_root) / "repository" / "plugins" / "vc"
        shutil.copytree(SOURCE_ROOT, pack_root)
        return pack_root

    def _replace(self, path: Path, old: str, new: str) -> None:
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text)
        path.write_text(text.replace(old, new, 1), encoding="utf-8")

    def _validate(self, pack_root: Path) -> None:
        VALIDATOR.ROOT = pack_root.resolve()
        VALIDATOR.validate_deal_field_maintenance_guidance()

    def _assert_rejected(self, path: Path, old: str, new: str) -> None:
        with tempfile.TemporaryDirectory() as temporary_root:
            pack_root = self._copy_pack(temporary_root)
            self._replace(pack_root / path, old, new)
            with self.assertRaises(SystemExit):
                self._validate(pack_root)

    def test_current_deal_guidance_uses_the_field_tools(self) -> None:
        self._validate(SOURCE_ROOT)
        for path in (MEETING_TASK, SCREENING_TASK):
            instructions = yaml.safe_load((SOURCE_ROOT / path).read_text(encoding="utf-8"))["definition"][
                "definitionJson"
            ]["instructions"]["executionInstructions"]
            self.assertIn("fill editable empty Deal fields", instructions)
            self.assertIn("suggest rather than make any change to a populated field", instructions)

    def test_report_executor_fills_deal_fields_but_stays_identity_read_only(self) -> None:
        prompt = yaml.safe_load((SOURCE_ROOT / ANALYST).read_text(encoding="utf-8"))["prompt"]["template"]
        self.assertIn(VALIDATOR.REPORT_EXECUTOR_IDENTITY_RULE, prompt)
        self.assertIn(VALIDATOR.DEAL_FIELD_ROUTE_RULE, prompt)
        self.assertIn("all People and Organisation records, to the human and the Deal Manager", prompt)

    def test_rejects_a_deal_task_without_the_field_tool_pointer(self) -> None:
        self._assert_rejected(MEETING_TASK, "use `field-values.setField` to fill", "fill")

    def test_rejects_an_unscoped_crm_prohibition_in_a_deal_task(self) -> None:
        self._assert_rejected(MEETING_TASK, "write external CRM records", "mutate CRM records")

    def test_rejects_an_unscoped_crm_prohibition_in_a_deal_agent(self) -> None:
        self._assert_rejected(MEETING_OPERATOR, "write to an external CRM or deal system", "update CRM/deal-system fields")

    def test_rejects_a_deal_agent_without_the_route_rule(self) -> None:
        self._assert_rejected(MEETING_OPERATOR, VALIDATOR.DEAL_FIELD_ROUTE_RULE, "Prefer the field tools")

    def test_rejects_a_project_data_field_write(self) -> None:
        self._assert_rejected(
            PIPELINE_MANAGER,
            "save its stable `id` to the Fund field with `field-values.setField`",
            'save its stable `id` with `project_data` `update_state` and `fieldValues: [{ fieldKey: "fund_id" }]`',
        )

    def test_rejects_a_project_update_field_write(self) -> None:
        self._assert_rejected(
            PIPELINE_MANAGER,
            "Register the saved document with `project.registerDecisionRecord`",
            "After creation, use `project.update` to set the fields, one field at a time",
        )

    def test_rejects_retry_guidance_that_only_preserves_ids(self) -> None:
        self._assert_rejected(
            PIPELINE_MANAGER,
            "replay the entire original `project.registerDecisionRecord` payload unchanged",
            "retry with the same artifactId and requestId",
        )

    def test_rejects_omitting_any_original_request_argument(self) -> None:
        arguments = "projectId, artifactId, requestId, sourceRevisionNumber, sourceContentHash, expectedDefinitionRevision, all five expectedRevisions, currentDecision, decisionRationale, and decisionConditions"
        for argument in (
            "projectId", "artifactId", "requestId", "sourceRevisionNumber", "sourceContentHash",
            "expectedDefinitionRevision", "all five expectedRevisions", "currentDecision",
            "decisionRationale", "decisionConditions",
        ):
            with self.subTest(argument=argument):
                self._assert_rejected(
                    PIPELINE_MANAGER,
                    arguments,
                    arguments.replace(argument, "[omitted]"),
                )

    def test_rejects_refreshing_revisions_after_an_ambiguous_outcome(self) -> None:
        self._assert_rejected(
            PIPELINE_MANAGER,
            "Do not substitute freshly read revisions or values, regenerate the requestId, or create another artifact while the outcome is unknown",
            "Refresh the field revisions before retrying with the same requestId",
        )

    def test_rejects_treating_an_unknown_outcome_as_a_no_write_conflict(self) -> None:
        self._assert_rejected(
            PIPELINE_MANAGER,
            "Only an explicit returned conflict outcome establishes that attempt changed no fields",
            "A timeout establishes that attempt changed no fields",
        )

    def test_rejects_rebuilding_an_unavailable_original_request(self) -> None:
        self._assert_rejected(
            PIPELINE_MANAGER,
            "if they are unavailable, inspect canonical state and report the unresolved outcome instead of constructing a different request",
            "if they are unavailable, rebuild the request using the latest field revisions",
        )


if __name__ == "__main__":
    unittest.main()
