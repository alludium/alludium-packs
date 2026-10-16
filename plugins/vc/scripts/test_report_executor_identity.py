"""Report-task executors stay read-only for identity records (#4286).

Screening, Evaluation, IC Memo and Term Sheet Review runs carry no verifiable direct-human signal
for identity work, so whoever or whatever started the task, the executor must not be able to
create, link or change People and Organisations.
"""

from __future__ import annotations

import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path
from typing import Any

import yaml


SOURCE_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = SOURCE_ROOT / "scripts" / "validate_pack.py"
VALIDATOR_SPEC = importlib.util.spec_from_file_location("validate_pack", VALIDATOR_PATH)
if VALIDATOR_SPEC is None or VALIDATOR_SPEC.loader is None:  # pragma: no cover - test setup guard
    raise RuntimeError(f"Unable to load {VALIDATOR_PATH}")
VALIDATOR = importlib.util.module_from_spec(VALIDATOR_SPEC)
VALIDATOR_SPEC.loader.exec_module(VALIDATOR)

ANALYST = Path("alludium") / "agent-templates" / "vc_deal_analyst.yaml"
SCREENING = Path("alludium") / "task-definition-templates" / "vc-workflows" / "generate-refresh-screening-report.yaml"


class ReportExecutorIdentityReadOnlyTests(unittest.TestCase):
    def _copy_pack(self, temporary_root: str) -> Path:
        pack_root = Path(temporary_root) / "repository" / "plugins" / "vc"
        shutil.copytree(SOURCE_ROOT, pack_root)
        return pack_root

    def _read(self, path: Path) -> dict[str, Any]:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(value, dict):  # pragma: no cover - fixture invariant
            raise TypeError(f"{path} must be an object")
        return value

    def _write(self, path: Path, value: dict[str, Any]) -> None:
        path.write_text(yaml.safe_dump(value, sort_keys=False, allow_unicode=True), encoding="utf-8")

    def _validate(self, pack_root: Path) -> None:
        VALIDATOR.ROOT = pack_root.resolve()
        VALIDATOR.validate_report_executors_identity_read_only()

    def test_current_report_executors_hold_no_identity_writes(self) -> None:
        self._validate(SOURCE_ROOT)
        analyst = self._read(SOURCE_ROOT / ANALYST)
        self.assertNotIn("IDENTITY_RECORD_MAINTENANCE", analyst["capabilityProfile"]["bundles"])
        self.assertNotIn(
            "platform_identity_maintenance",
            [skill["externalId"] for skill in analyst["skills"]],
        )

    def test_rejects_identity_write_bundle_on_a_report_executor(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_root:
            pack_root = self._copy_pack(temporary_root)
            analyst = self._read(pack_root / ANALYST)
            analyst["capabilityProfile"]["bundles"].append("IDENTITY_RECORD_MAINTENANCE")
            self._write(pack_root / ANALYST, analyst)
            with self.assertRaises(SystemExit):
                self._validate(pack_root)

    def test_rejects_identity_maintenance_skill_on_a_report_executor(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_root:
            pack_root = self._copy_pack(temporary_root)
            analyst = self._read(pack_root / ANALYST)
            analyst["skills"].append({"externalId": "platform_identity_maintenance", "activationMode": "ALWAYS"})
            self._write(pack_root / ANALYST, analyst)
            with self.assertRaises(SystemExit):
                self._validate(pack_root)

    def test_rejects_a_report_executor_prompt_without_the_read_only_rule(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_root:
            pack_root = self._copy_pack(temporary_root)
            analyst = self._read(pack_root / ANALYST)
            analyst["prompt"]["template"] = analyst["prompt"]["template"].replace(
                VALIDATOR.REPORT_EXECUTOR_IDENTITY_RULE, ""
            )
            self._write(pack_root / ANALYST, analyst)
            with self.assertRaises(SystemExit):
                self._validate(pack_root)

    def test_checks_whichever_agent_a_report_task_routes_to(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_root:
            pack_root = self._copy_pack(temporary_root)
            screening = self._read(pack_root / SCREENING)
            # A writer-capable agent must not become a report executor.
            screening["definition"]["definitionJson"]["recommendedAgentTemplate"] = "vc_deal_pipeline_manager"
            self._write(pack_root / SCREENING, screening)
            with self.assertRaises(SystemExit):
                self._validate(pack_root)


if __name__ == "__main__":
    unittest.main()
