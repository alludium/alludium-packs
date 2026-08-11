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


def _rehash_package(component_root: Path, package_filename: str) -> None:
    package_path = component_root / "packages" / package_filename
    catalog_path = component_root / "catalog.v1.json"
    catalog = _read_json(catalog_path)
    for package_ref in catalog["packages"]:
        if package_ref["path"] == f"packages/{package_filename}":
            package_ref["sha256"] = _sha256(package_path)
            break
    _write_canonical(catalog_path, catalog)


def _rehash_component(
    component_root: Path,
    package_filename: str,
    component_filename: str,
) -> None:
    component_path = component_root / "components" / component_filename
    package_path = component_root / "packages" / package_filename
    package = _read_json(package_path)
    component_id: str | None = None
    component_sha256 = _sha256(component_path)
    for component_ref in package["components"]:
        if component_ref["path"] == f"components/{component_filename}":
            component_ref["sha256"] = component_sha256
            component_id = component_ref["id"]
            break
    if component_id is None:  # pragma: no cover - fixture invariant
        raise AssertionError(f"missing component {component_filename}")
    for component_ref in package["components"]:
        for dependency in component_ref["dependencies"]:
            if dependency["id"] == component_id:
                dependency["sha256"] = component_sha256
    _write_canonical(package_path, package)
    _rehash_package(component_root, package_filename)


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
        for forbidden_key in ("providerPrompt", "apiTokens"):
            with self.subTest(forbidden_key=forbidden_key), tempfile.TemporaryDirectory(
            ) as temporary_root:
                pack_root = self._copy_pack(temporary_root)
                component_root = pack_root / "alludium" / "ontology-components"
                component_path = (
                    component_root / "components" / "finance-screening.profile.v1.json"
                )
                component = _read_json(component_path)
                component["content"][forbidden_key] = "forbidden runtime instruction"
                _write_canonical(component_path, component)
                _rehash_component(
                    component_root,
                    "finance-screening.v1.json",
                    "finance-screening.profile.v1.json",
                )

                result = self._run_validator(pack_root)

            self.assertEqual(result.returncode, 1)
            self.assertIn(
                f"must not embed runtime control {forbidden_key}",
                result.stderr,
            )

    def test_component_content_schema_rejects_unrecognized_runtime_controls(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_root:
            pack_root = self._copy_pack(temporary_root)
            component_root = pack_root / "alludium" / "ontology-components"
            component_path = (
                component_root / "components" / "finance-screening.profile.v1.json"
            )
            component = _read_json(component_path)
            component["content"]["temperature"] = 0
            _write_canonical(component_path, component)
            _rehash_component(
                component_root,
                "finance-screening.v1.json",
                "finance-screening.profile.v1.json",
            )

            result = self._run_validator(pack_root)

        self.assertEqual(result.returncode, 1)
        self.assertIn("profile content keys must be exact", result.stderr)

    def test_ontology_surface_rejects_unreferenced_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_root:
            pack_root = self._copy_pack(temporary_root)
            component_root = pack_root / "alludium" / "ontology-components"
            orphan_path = component_root / "components" / "orphan.v1.json"
            _write_canonical(
                orphan_path,
                {
                    "apiVersion": "alludium/v1alpha1",
                    "content": {"temperature": 0},
                    "id": "fixture.orphan",
                    "kind": "profile",
                    "lifecycle": "active",
                    "version": "latest",
                },
            )

            result = self._run_validator(pack_root)

        self.assertEqual(result.returncode, 1)
        self.assertIn("contains unreferenced artifacts", result.stderr)
        self.assertIn("components/orphan.v1.json", result.stderr)

    def test_ontology_surface_rejects_symlink_artifacts(self) -> None:
        for target_name in ("finance-screening.profile.v1.json", "missing.v1.json"):
            with self.subTest(target_name=target_name), tempfile.TemporaryDirectory(
            ) as temporary_root:
                pack_root = self._copy_pack(temporary_root)
                component_root = pack_root / "alludium" / "ontology-components"
                alias_path = component_root / "components" / "alias.v1.json"
                alias_path.symlink_to(target_name)

                result = self._run_validator(pack_root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("must not contain symlink artifacts", result.stderr)
            self.assertIn("components/alias.v1.json", result.stderr)

    def test_ontology_surface_root_stays_beneath_pack_and_is_not_a_symlink(self) -> None:
        for case in ("traversal", "symlink"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as temporary_root:
                pack_root = self._copy_pack(temporary_root)
                manifest_path = pack_root / "alludium" / "manifest.yaml"
                manifest_text = manifest_path.read_text(encoding="utf-8")
                if case == "traversal":
                    outside_root = pack_root.parent / "outside"
                    shutil.copytree(
                        pack_root / "alludium" / "ontology-components",
                        outside_root,
                    )
                    replacement = "path: ../outside"
                else:
                    alias_root = pack_root / "alludium" / "ontology-components-link"
                    alias_root.symlink_to("ontology-components")
                    replacement = "path: alludium/ontology-components-link"
                manifest_path.write_text(
                    manifest_text.replace(
                        "path: alludium/ontology-components",
                        replacement,
                    ),
                    encoding="utf-8",
                )

                result = self._run_validator(pack_root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("surfaces.ontologyComponents.path must", result.stderr)

    def test_versions_reject_ranges_wildcards_and_arbitrary_text(self) -> None:
        cases = (
            ("package", "^1.0.0"),
            ("component_reference", ">=1.0"),
            ("component_artifact", "1.x"),
            ("dependency", "release-one"),
        )
        for case, invalid_version in cases:
            with self.subTest(case=case), tempfile.TemporaryDirectory() as temporary_root:
                pack_root = self._copy_pack(temporary_root)
                component_root = pack_root / "alludium" / "ontology-components"
                package_path = component_root / "packages" / "finance-screening.v1.json"
                package = _read_json(package_path)

                if case == "package":
                    package["version"] = invalid_version
                    _write_canonical(package_path, package)
                    catalog_path = component_root / "catalog.v1.json"
                    catalog = _read_json(catalog_path)
                    catalog["packages"][0]["version"] = invalid_version
                    catalog["packages"][0]["sha256"] = _sha256(package_path)
                    _write_canonical(catalog_path, catalog)
                elif case == "component_reference":
                    package["components"][0]["version"] = invalid_version
                    _write_canonical(package_path, package)
                    _rehash_package(component_root, "finance-screening.v1.json")
                elif case == "component_artifact":
                    component_path = (
                        component_root
                        / "components"
                        / "finance-screening.constraints.v1.json"
                    )
                    component = _read_json(component_path)
                    component["version"] = invalid_version
                    _write_canonical(component_path, component)
                    _rehash_component(
                        component_root,
                        "finance-screening.v1.json",
                        "finance-screening.constraints.v1.json",
                    )
                else:
                    package["components"][0]["dependencies"][0]["version"] = invalid_version
                    _write_canonical(package_path, package)
                    _rehash_package(component_root, "finance-screening.v1.json")

                result = self._run_validator(pack_root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("must use an exact semantic version", result.stderr)

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

    def test_required_versions_and_stage_components_cannot_be_empty(self) -> None:
        for case in ("package_version", "component_version", "stage_components"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as temporary_root:
                pack_root = self._copy_pack(temporary_root)
                component_root = pack_root / "alludium" / "ontology-components"
                package_path = component_root / "packages" / "finance-screening.v1.json"
                package = _read_json(package_path)

                if case == "package_version":
                    package["version"] = ""
                    catalog_path = component_root / "catalog.v1.json"
                    catalog = _read_json(catalog_path)
                    catalog["packages"][0]["version"] = ""
                    _write_canonical(catalog_path, catalog)
                elif case == "component_version":
                    component_path = (
                        component_root
                        / "components"
                        / "finance-screening.constraints.v1.json"
                    )
                    component = _read_json(component_path)
                    component["version"] = ""
                    _write_canonical(component_path, component)
                    component_id = package["components"][0]["id"]
                    package["components"][0]["version"] = ""
                    for component_ref in package["components"]:
                        for dependency in component_ref["dependencies"]:
                            if dependency["id"] == component_id:
                                dependency["version"] = ""
                    package["components"][0]["sha256"] = _sha256(component_path)
                else:
                    package["stageBindings"][0]["componentIds"] = []

                _write_canonical(package_path, package)
                _rehash_package(component_root, "finance-screening.v1.json")
                result = self._run_validator(pack_root)

            self.assertEqual(result.returncode, 1)
            if case == "stage_components":
                self.assertIn("componentIds must be a non-empty list", result.stderr)
            else:
                self.assertIn("must declare a non-empty exact version", result.stderr)


if __name__ == "__main__":
    unittest.main()
