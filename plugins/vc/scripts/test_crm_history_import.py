"""Import or Refresh CRM History keeps its own contract beside the four Deal reports (#4841).

Each rejection test breaks one rule in a copy of the Pack and checks the validator fails, so a
passing validator proves the rule is enforced rather than merely present.
"""

from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from typing import Any, Callable

import yaml


SOURCE_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = SOURCE_ROOT / "scripts" / "validate_pack.py"
VALIDATOR_SPEC = importlib.util.spec_from_file_location("validate_pack_crm_history", VALIDATOR_PATH)
if VALIDATOR_SPEC is None or VALIDATOR_SPEC.loader is None:  # pragma: no cover - test setup guard
    raise RuntimeError(f"Unable to load {VALIDATOR_PATH}")
VALIDATOR = importlib.util.module_from_spec(VALIDATOR_SPEC)
VALIDATOR_SPEC.loader.exec_module(VALIDATOR)

ANALYST = Path("alludium") / "agent-templates" / "vc_deal_analyst.yaml"
MANAGER = Path("alludium") / "agent-templates" / "vc_deal_pipeline_manager.yaml"
TASK = Path("alludium") / "task-definition-templates" / "vc-workflows" / "import-refresh-crm-history.yaml"
PIPELINE = Path("alludium") / "project-types" / "vc_deal_pipeline.json"
TEMPLATE = Path("alludium") / "documents" / "deal-pipeline" / "crm-history-template.html"
SKILL = Path("skills") / "import-crm-history" / "SKILL.md"
CRM_SLUG = "import-refresh-crm-history"


def read_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):  # pragma: no cover - fixture invariant
        raise TypeError(f"{path} must be an object")
    return value


def write_yaml(path: Path, value: dict[str, Any]) -> None:
    path.write_text(yaml.safe_dump(value, sort_keys=False, allow_unicode=True), encoding="utf-8")


def crm_mapping(pipeline: dict[str, Any]) -> dict[str, Any]:
    return next(
        mapping
        for mapping in pipeline["initialVersion"]["projectTaskMappings"]
        if mapping["taskDefinitionSlug"] == CRM_SLUG
    )


class CrmHistoryImportContractTests(unittest.TestCase):
    def _validate(self, pack_root: Path) -> None:
        VALIDATOR.ROOT = pack_root.resolve()
        VALIDATOR.validate_vc_deal_pipeline_contract()

    def _assert_rejected(self, mutate: Callable[[Path], None]) -> None:
        with tempfile.TemporaryDirectory() as temporary_root:
            pack_root = Path(temporary_root) / "repository" / "plugins" / "vc"
            shutil.copytree(SOURCE_ROOT, pack_root)
            mutate(pack_root)
            with self.assertRaises(SystemExit):
                self._validate(pack_root)

    def _edit_yaml(self, relative: Path, change: Callable[[dict[str, Any]], None]) -> Callable[[Path], None]:
        def mutate(pack_root: Path) -> None:
            value = read_yaml(pack_root / relative)
            change(value)
            write_yaml(pack_root / relative, value)

        return mutate

    def _edit_pipeline(self, change: Callable[[dict[str, Any]], None]) -> Callable[[Path], None]:
        def mutate(pack_root: Path) -> None:
            value = json.loads((pack_root / PIPELINE).read_text(encoding="utf-8"))
            change(value)
            (pack_root / PIPELINE).write_text(json.dumps(value, indent=2), encoding="utf-8")

        return mutate

    def _edit_text(self, relative: Path, old: str, new: str) -> Callable[[Path], None]:
        def mutate(pack_root: Path) -> None:
            text = (pack_root / relative).read_text(encoding="utf-8")
            self.assertIn(old, text)
            (pack_root / relative).write_text(text.replace(old, new), encoding="utf-8")

        return mutate

    # Current Pack ---------------------------------------------------------------------------

    def test_current_pack_passes_and_keeps_one_document_pointer(self) -> None:
        self._validate(SOURCE_ROOT)
        pipeline = json.loads((SOURCE_ROOT / PIPELINE).read_text(encoding="utf-8"))
        mapping = crm_mapping(pipeline)
        self.assertEqual(
            [entry["taskField"] for entry in mapping["outputMappings"]],
            ["crm_history_artifact_id"],
        )
        task = read_yaml(SOURCE_ROOT / TASK)
        self.assertEqual(task["version"], "1.0.3")
        self.assertFalse(task["runtime"]["executionProfile"]["requiresHumanConfirmationToComplete"])

    # Task definition ------------------------------------------------------------------------

    def test_rejects_the_living_report_skill_on_the_crm_task(self) -> None:
        def change(task: dict[str, Any]) -> None:
            task["definition"]["definitionJson"]["requiredSkills"].append("generate-or-refresh-living-report")

        self._assert_rejected(self._edit_yaml(TASK, change))

    def test_rejects_wording_that_blocks_template_instantiation(self) -> None:
        def change(task: dict[str, Any]) -> None:
            task["definition"]["definitionJson"]["instructions"]["executionInstructions"] += (
                " Save with artifact.createTextArtifact as crm-history.html using text/html."
            )

        self._assert_rejected(self._edit_yaml(TASK, change))

    def test_rejects_an_import_with_a_task_instance_policy(self) -> None:
        def change(task: dict[str, Any]) -> None:
            task["definition"]["definitionJson"]["activeInstancePolicy"] = {
                "scope": "project", "maxActiveInstances": 1, "onConflict": "return_existing"}

        self._assert_rejected(self._edit_yaml(TASK, change))

    def test_rejects_a_manager_that_creates_another_import_after_a_block(self) -> None:
        self._assert_rejected(
            self._edit_text(
                MANAGER,
                "Only when its status is running is the import underway",
                "Any open import is underway",
            )
        )

    def test_rejects_human_confirmation_to_complete(self) -> None:
        def change(task: dict[str, Any]) -> None:
            task["runtime"]["executionProfile"]["requiresHumanConfirmationToComplete"] = True

        self._assert_rejected(self._edit_yaml(TASK, change))

    def test_rejects_a_business_field_output(self) -> None:
        def change(task: dict[str, Any]) -> None:
            task["fields"]["output"].append(
                {"key": "fund_id", "name": "Fund", "fieldType": "string", "required": False, "position": 1}
            )

        self._assert_rejected(self._edit_yaml(TASK, change))

    def test_rejects_a_stage_bound_crm_task(self) -> None:
        def change(task: dict[str, Any]) -> None:
            task["definition"]["definitionJson"]["stageIndependent"] = False
            task["definition"]["definitionJson"]["stage"] = "screening"

        self._assert_rejected(self._edit_yaml(TASK, change))

    def test_rejects_instructions_that_allow_a_second_document(self) -> None:
        self._assert_rejected(
            self._edit_text(TASK, "Never create a second CRM history document for this Deal.", "")
        )

    # Project type ---------------------------------------------------------------------------

    def test_rejects_a_missing_crm_mapping(self) -> None:
        def change(pipeline: dict[str, Any]) -> None:
            mappings = pipeline["initialVersion"]["projectTaskMappings"]
            pipeline["initialVersion"]["projectTaskMappings"] = [
                mapping for mapping in mappings if mapping["taskDefinitionSlug"] != CRM_SLUG
            ]

        self._assert_rejected(self._edit_pipeline(change))

    def test_still_rejects_a_missing_report_mapping(self) -> None:
        def change(pipeline: dict[str, Any]) -> None:
            mappings = pipeline["initialVersion"]["projectTaskMappings"]
            pipeline["initialVersion"]["projectTaskMappings"] = [
                mapping for mapping in mappings if mapping["taskDefinitionSlug"] != "review-refresh-term-sheet"
            ]

        self._assert_rejected(self._edit_pipeline(change))

    def test_rejects_a_stage_created_import(self) -> None:
        def change(pipeline: dict[str, Any]) -> None:
            crm_mapping(pipeline)["activationPolicy"]["createTaskWhenLifecycleStageEntered"] = True

        self._assert_rejected(self._edit_pipeline(change))

    def test_rejects_an_extra_output_mapping(self) -> None:
        def change(pipeline: dict[str, Any]) -> None:
            crm_mapping(pipeline)["outputMappings"].append(
                {"taskField": "fund_id", "target": "project.field", "targetPath": "fund_id", "requiredForCompletion": False}
            )

        self._assert_rejected(self._edit_pipeline(change))

    def test_rejects_a_company_name_from_a_deal_field(self) -> None:
        def change(pipeline: dict[str, Any]) -> None:
            for entry in crm_mapping(pipeline)["inputMappings"]:
                if entry["taskField"] == "company_name":
                    entry["source"] = "project.field"
                    entry["sourcePath"] = "company_name"

        self._assert_rejected(self._edit_pipeline(change))

    def test_rejects_a_missing_existing_document_input(self) -> None:
        def change(pipeline: dict[str, Any]) -> None:
            mapping = crm_mapping(pipeline)
            mapping["inputMappings"] = [
                entry for entry in mapping["inputMappings"]
                if entry["taskField"] != "existing_crm_history_artifact_id"
            ]

        self._assert_rejected(self._edit_pipeline(change))

    def test_rejects_an_unpresented_document_pointer(self) -> None:
        def change(pipeline: dict[str, Any]) -> None:
            for section in pipeline["initialVersion"]["extensions"]["projectDataSections"]:
                section["fieldKeys"] = [key for key in section["fieldKeys"] if key != "crm_history_artifact_id"]

        self._assert_rejected(self._edit_pipeline(change))

    # Template and skill ---------------------------------------------------------------------

    def test_rejects_a_living_report_manifest_in_the_template(self) -> None:
        self._assert_rejected(
            self._edit_text(
                TEMPLATE,
                "</article>",
                '<section hidden data-evidence-basis-manifest="v1"><pre>{}</pre></section></article>',
            )
        )

    def test_rejects_a_template_without_the_source_appendix(self) -> None:
        self._assert_rejected(self._edit_text(TEMPLATE, "<h2>Source appendix</h2>", "<h2>Sources</h2>"))

    def test_rejects_a_skill_that_allows_shortened_notes(self) -> None:
        self._assert_rejected(
            self._edit_text(SKILL, "Never shorten, summarise, excerpt or drop a note.", "Shorten long notes.")
        )

    def test_rejects_a_skill_without_the_partial_import_rule(self) -> None:
        self._assert_rejected(self._edit_text(SKILL, "mark the import **partial**", "carry on"))

    def test_rejects_a_skill_that_imports_without_a_matching_record(self) -> None:
        self._assert_rejected(
            self._edit_text(SKILL, "If no record matches, the import is **blocked**", "If no record matches, carry on")
        )

    def test_rejects_a_skill_without_the_note_source_pairing(self) -> None:
        self._assert_rejected(
            self._edit_text(SKILL, "That pairing, not the record you had in mind, is each note's source record", "")
        )

    def test_rejects_a_skill_that_reads_people_and_lists(self) -> None:
        self._assert_rejected(
            self._edit_text(
                SKILL,
                "Do not read person records, person notes, lists, list entries or field definitions",
                "Also read person records and lists",
            )
        )

    def test_rejects_a_skill_that_cannot_resume_its_own_document(self) -> None:
        self._assert_rejected(
            self._edit_text(SKILL, "The one exception is this task's own earlier document", "There is no exception")
        )

    def test_rejects_a_skill_that_stops_because_another_import_is_open(self) -> None:
        self._assert_rejected(
            self._edit_text(
                SKILL,
                "if the Deal now has a CRM history document set, or if",
                "if the Deal now has a CRM history document set, if another CRM history import task for this\n"
                "   Deal is still open, or if",
            )
        )

    def test_rejects_a_skill_that_hides_a_blocker_from_the_manager(self) -> None:
        self._assert_rejected(
            self._edit_text(
                SKILL,
                "purpose `attention_required`, `relatedTaskId` set to this task's ID",
                "purpose `status_update`",
            )
        )

    def test_rejects_a_skill_that_allows_another_create_tool(self) -> None:
        self._assert_rejected(
            self._edit_text(
                SKILL,
                "Create the document once, only with `project.instantiateTemplate`",
                "Create the document with any available tool",
            )
        )

    # Agents ---------------------------------------------------------------------------------

    def test_rejects_an_always_on_living_report_skill(self) -> None:
        def change(analyst: dict[str, Any]) -> None:
            for skill in analyst["skills"]:
                if skill["externalId"] == "generate-or-refresh-living-report":
                    skill["activationMode"] = "ALWAYS"

        self._assert_rejected(self._edit_yaml(ANALYST, change))

    def test_rejects_the_unscoped_living_report_instruction(self) -> None:
        self._assert_rejected(
            self._edit_text(
                ANALYST,
                "For the four living report tasks, activate and apply `generate-or-refresh-living-report`",
                "For every task, apply `generate-or-refresh-living-report`",
            )
        )

    def test_rejects_an_analyst_without_the_crm_skill(self) -> None:
        def change(analyst: dict[str, Any]) -> None:
            analyst["skills"] = [
                skill for skill in analyst["skills"] if skill["externalId"] != "import-crm-history"
            ]

        self._assert_rejected(self._edit_yaml(ANALYST, change))

    def test_rejects_a_manager_that_imports_in_chat(self) -> None:
        self._assert_rejected(
            self._edit_text(
                MANAGER,
                "Do not perform the import yourself or create a CRM history document in this chat.",
                "Perform the import yourself.",
            )
        )

    def test_rejects_a_manager_that_cannot_start_the_task(self) -> None:
        def change(manager: dict[str, Any]) -> None:
            manager["metadata"]["supportedTaskDefinitions"].remove(CRM_SLUG)

        self._assert_rejected(self._edit_yaml(MANAGER, change))


if __name__ == "__main__":
    unittest.main()
