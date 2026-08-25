#!/usr/bin/env python3
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


class CapabilityContractRegressionTests(unittest.TestCase):
    def _copy_pack(self, temporary_root: str) -> Path:
        pack_root = Path(temporary_root) / "repository" / "plugins" / "vc"
        shutil.copytree(SOURCE_ROOT, pack_root)
        return pack_root

    def _manifest(self, pack_root: Path) -> dict[str, Any]:
        value = yaml.safe_load((pack_root / "alludium" / "manifest.yaml").read_text(encoding="utf-8"))
        if not isinstance(value, dict):  # pragma: no cover - fixture invariant
            raise TypeError("manifest must be an object")
        return value

    def _capability_path(self, pack_root: Path) -> Path:
        return pack_root / "alludium" / "capabilities" / "vc.financial_workbook_evaluation.yaml"

    def _read_capability(self, pack_root: Path) -> dict[str, Any]:
        value = yaml.safe_load(self._capability_path(pack_root).read_text(encoding="utf-8"))
        if not isinstance(value, dict):  # pragma: no cover - fixture invariant
            raise TypeError("capability must be an object")
        return value

    def _write_yaml(self, path: Path, value: dict[str, Any]) -> None:
        path.write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")

    def _validate(self, pack_root: Path) -> None:
        VALIDATOR.ROOT = pack_root.resolve()
        VALIDATOR.validate_capabilities(self._manifest(pack_root))

    def test_rejects_unsafe_surface_path(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_root:
            pack_root = self._copy_pack(temporary_root)
            manifest = self._manifest(pack_root)
            manifest["surfaces"]["capabilities"]["path"] = "alludium/../capabilities"
            self._write_yaml(pack_root / "alludium" / "manifest.yaml", manifest)

            with self.assertRaises(SystemExit):
                self._validate(pack_root)

    def test_rejects_unreferenced_capability_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_root:
            pack_root = self._copy_pack(temporary_root)
            orphan = pack_root / "alludium" / "capabilities" / "orphan.yaml"
            orphan.write_text("id: orphan\n", encoding="utf-8")

            with self.assertRaises(SystemExit):
                self._validate(pack_root)

    def test_rejects_capability_symlinks(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_root:
            pack_root = self._copy_pack(temporary_root)
            alias = pack_root / "alludium" / "capabilities" / "alias.yaml"
            alias.symlink_to("vc.financial_workbook_evaluation.yaml")

            with self.assertRaises(SystemExit):
                self._validate(pack_root)

    def test_rejects_unknown_capability_keys(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_root:
            pack_root = self._copy_pack(temporary_root)
            capability = self._read_capability(pack_root)
            capability["unexpected"] = True
            self._write_yaml(self._capability_path(pack_root), capability)

            with self.assertRaises(SystemExit):
                self._validate(pack_root)

    def test_rejects_identity_and_version_mismatches(self) -> None:
        for field, value in (("id", "vc.other_capability"), ("version", "2.0.0")):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as temporary_root:
                pack_root = self._copy_pack(temporary_root)
                capability = self._read_capability(pack_root)
                capability[field] = value
                self._write_yaml(self._capability_path(pack_root), capability)

                with self.assertRaises(SystemExit):
                    self._validate(pack_root)

    def test_rejects_frozen_limit_and_output_contract_mismatches(self) -> None:
        mutations = (
            ("retry phase", ("limits", "automaticRetry", "executionPhase"), "after-execution"),
            ("retry class", ("limits", "automaticRetry", "failureClasses"), ["any-failure"]),
            ("output bound", ("limits", "outputBytesScope"), "artifact-only"),
            ("output schema", ("outputContract", "schemaVersion"), "deal-workbook-evaluation-output-v2"),
            ("output reference", ("outputContract", "reference"), "unrelated-schema"),
        )
        for description, path, value in mutations:
            with self.subTest(description=description), tempfile.TemporaryDirectory() as temporary_root:
                pack_root = self._copy_pack(temporary_root)
                capability = self._read_capability(pack_root)
                target: Any = capability
                for key in path[:-1]:
                    target = target[key]
                target[path[-1]] = value
                self._write_yaml(self._capability_path(pack_root), capability)

                with self.assertRaises(SystemExit):
                    self._validate(pack_root)


if __name__ == "__main__":
    unittest.main()
