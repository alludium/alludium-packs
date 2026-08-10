#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any


SOURCE_ROOT = Path(__file__).resolve().parents[1]


def _write_canonical(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):  # pragma: no cover - fixture invariant
        raise TypeError(f"{path} must contain an object")
    return value


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class OntologyComponentContractRegressionTests(unittest.TestCase):
    def _copy_pack(self, temporary_root: str) -> Path:
        pack_root = Path(temporary_root) / "repository" / "plugins" / "vc"
        shutil.copytree(SOURCE_ROOT, pack_root)
        return pack_root

    def _run_validator(self, pack_root: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(pack_root / "scripts" / "validate_pack.py")],
            cwd=pack_root.parents[1],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_component_content_rejects_composite_provider_control_keys(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_root:
            pack_root = self._copy_pack(temporary_root)
            component_root = pack_root / "alludium" / "ontology-components"
            component_path = component_root / "components" / "finance-screening.profile.v1.json"
            component = _read_json(component_path)
            component["content"]["providerPrompt"] = "forbidden runtime instruction"
            _write_canonical(component_path, component)

            package_path = component_root / "packages" / "finance-screening.v1.json"
            package = _read_json(package_path)
            for component_ref in package["components"]:
                if component_ref["path"] == "components/finance-screening.profile.v1.json":
                    component_ref["sha256"] = _sha256(component_path)
                    break
            _write_canonical(package_path, package)

            catalog_path = component_root / "catalog.v1.json"
            catalog = _read_json(catalog_path)
            for package_ref in catalog["packages"]:
                if package_ref["path"] == "packages/finance-screening.v1.json":
                    package_ref["sha256"] = _sha256(package_path)
                    break
            _write_canonical(catalog_path, catalog)

            result = self._run_validator(pack_root)

        self.assertEqual(result.returncode, 1)
        self.assertIn("must not embed runtime control providerPrompt", result.stderr)

    def test_catalog_rejects_an_unrecognized_api_version(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_root:
            pack_root = self._copy_pack(temporary_root)
            catalog_path = (
                pack_root / "alludium" / "ontology-components" / "catalog.v1.json"
            )
            catalog = _read_json(catalog_path)
            catalog["apiVersion"] = "alludium/v2"
            _write_canonical(catalog_path, catalog)

            result = self._run_validator(pack_root)

        self.assertEqual(result.returncode, 1)
        self.assertIn("must use alludium/v1alpha1", result.stderr)


if __name__ == "__main__":
    unittest.main()
