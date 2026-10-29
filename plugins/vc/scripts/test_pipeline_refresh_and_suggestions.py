"""Pipeline report refresh, archived-Deal wording and field suggestions (#5056, #5039, #4394).

Task-run report sources are immutable on the Platform, so a refresh reads the existing report as
its baseline and creates one new complete report. An archived Deal admits no new task work and has
no reopen path. A suggested change to a populated Deal, Person or Organisation field names both
values and asks, so the human's "yes" is an explicit request.
"""

from __future__ import annotations

import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path


SOURCE_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = SOURCE_ROOT / "scripts" / "validate_pack.py"
VALIDATOR_SPEC = importlib.util.spec_from_file_location("validate_pack", VALIDATOR_PATH)
if VALIDATOR_SPEC is None or VALIDATOR_SPEC.loader is None:  # pragma: no cover - test setup guard
    raise RuntimeError(f"Unable to load {VALIDATOR_PATH}")
VALIDATOR = importlib.util.module_from_spec(VALIDATOR_SPEC)
VALIDATOR_SPEC.loader.exec_module(VALIDATOR)

TEMPLATES = Path("alludium") / "agent-templates"
WORKFLOWS = Path("alludium") / "task-definition-templates" / "vc-workflows"
ANALYST = TEMPLATES / "vc_deal_analyst.yaml"
MANAGER = TEMPLATES / "vc_deal_pipeline_manager.yaml"
SCREENING_TASK = WORKFLOWS / "generate-refresh-screening-report.yaml"
MEETING_TASK = WORKFLOWS / "summarize-pipeline-meeting.yaml"
LIVING_REPORT_SKILL = Path("skills") / "generate-or-refresh-living-report" / "SKILL.md"


class PipelineRefreshAndSuggestionTests(unittest.TestCase):
    def _assert_rejected(self, path: Path, old: str, new: str, validate, count: int = 1) -> None:
        with tempfile.TemporaryDirectory() as temporary_root:
            pack_root = Path(temporary_root) / "repository" / "plugins" / "vc"
            shutil.copytree(SOURCE_ROOT, pack_root)
            target = pack_root / path
            text = target.read_text(encoding="utf-8")
            self.assertIn(old, text)
            target.write_text(text.replace(old, new, count), encoding="utf-8")
            VALIDATOR.ROOT = pack_root.resolve()
            try:
                with self.assertRaises(SystemExit):
                    validate()
            finally:
                VALIDATOR.ROOT = SOURCE_ROOT.resolve()

    def test_current_guidance_passes(self) -> None:
        VALIDATOR.ROOT = SOURCE_ROOT.resolve()
        VALIDATOR.validate_pipeline_refresh_and_suggestion_guidance()

    def test_skill_refresh_creates_a_new_report_and_never_edits_the_old_one(self) -> None:
        skill = (SOURCE_ROOT / LIVING_REPORT_SKILL).read_text(encoding="utf-8")
        self.assertIn("create exactly one new project-shared", skill)
        self.assertIn("never call a text-artifact update tool on it", skill)
        self.assertNotIn("update that exact artifact in place", skill)

    def test_rejects_an_analyst_that_refreshes_in_place(self) -> None:
        self._assert_rejected(
            ANALYST,
            "creates one new complete report",
            "is updated in place",
            VALIDATOR.validate_pipeline_refresh_and_suggestion_guidance,
        )

    def test_rejects_a_manager_that_keeps_one_logical_artifact(self) -> None:
        self._assert_rejected(
            MANAGER,
            "creates one new complete report",
            "updates the same logical artifact",
            VALIDATOR.validate_pipeline_refresh_and_suggestion_guidance,
        )

    def test_rejects_a_manager_that_suggests_reopening_an_archived_deal(self) -> None:
        self._assert_rejected(
            MANAGER,
            "Do not tell the human to reopen, restore or unarchive it.",
            "Ask the human to reopen the Deal.",
            VALIDATOR.validate_pipeline_refresh_and_suggestion_guidance,
        )

    def test_rejects_a_manager_without_the_supported_new_deal_path(self) -> None:
        self._assert_rejected(
            MANAGER,
            "create a new Deal for the correct Organisation, or do the work on an active Deal",
            "wait",
            VALIDATOR.validate_pipeline_refresh_and_suggestion_guidance,
        )

    def test_rejects_a_suggestion_that_does_not_ask(self) -> None:
        for path in (ANALYST, MANAGER):
            with self.subTest(path=path):
                self._assert_rejected(
                    path,
                    "Want me to update it?",
                    "",
                    VALIDATOR.validate_pipeline_refresh_and_suggestion_guidance,
                    count=-1,
                )

    def test_rejects_a_manager_that_only_asks_for_deal_fields(self) -> None:
        self._assert_rejected(
            MANAGER,
            "Deal, Person or Organisation field",
            "Deal field",
            VALIDATOR.validate_pipeline_refresh_and_suggestion_guidance,
        )

    def test_rejects_a_pipeline_task_that_does_not_ask(self) -> None:
        for path in (SCREENING_TASK, MEETING_TASK):
            with self.subTest(path=path):
                self._assert_rejected(
                    path,
                    "and ask whether to update it;",
                    "and note it;",
                    VALIDATOR.validate_pipeline_refresh_and_suggestion_guidance,
                )

    def test_rejects_a_report_task_without_the_new_report_refresh(self) -> None:
        self._assert_rejected(
            SCREENING_TASK,
            "create one new complete report",
            "refresh the report",
            VALIDATOR.validate_pipeline_refresh_and_suggestion_guidance,
        )

    def test_rejects_a_skill_that_refreshes_in_place(self) -> None:
        self._assert_rejected(
            LIVING_REPORT_SKILL,
            "Earlier reports are immutable task evidence.",
            "Earlier reports are immutable task evidence. Otherwise update that exact artifact in place.",
            VALIDATOR.validate_vc_deal_pipeline_contract,
        )


if __name__ == "__main__":
    unittest.main()
