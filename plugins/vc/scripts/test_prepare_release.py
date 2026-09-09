#!/usr/bin/env python3
"""Exercise release generation against the real VC artifact structure."""
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import prepare_release as prepare


class PrepareReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.pack = Path(self.temp.name) / "vc"
        shutil.copytree(prepare.PACK_ROOT, self.pack, ignore=shutil.ignore_patterns("__pycache__"))

    def apply(self, version=None):
        outputs = prepare.metadata_outputs(self.pack, version)
        for path, body in outputs.items():
            path.write_bytes(body)
        return outputs

    def test_bump_preserves_history_and_authored_components_and_is_idempotent(self):
        historical_readme = (self.pack / "README.md").read_text().split("Version `", 1)[1]
        component_root = self.pack / "alludium/ontology-components/components"
        originals = {path: path.read_bytes() for path in component_root.glob("*.json")}
        for folder in ("agent-templates", "task-definition-templates", "project-types"):
            originals.update({p: p.read_bytes() for p in (self.pack / "alludium" / folder).rglob("*") if p.is_file()})
        outputs = self.apply("99.0.0")
        self.assertEqual(outputs, prepare.metadata_outputs(self.pack))
        self.assertEqual(historical_readme, (self.pack / "README.md").read_text().split("Version `", 1)[1])
        for path, body in originals.items():
            self.assertEqual(path.read_bytes(), body)
        catalog_path = self.pack / "alludium/ontology-components/catalog.v1.json"
        catalog = json.loads(catalog_path.read_bytes())
        self.assertEqual(catalog["release"]["tag"], "v99.0.0")
        for ref in catalog["packages"]:
            package_path = catalog_path.parent / ref["path"]
            package = json.loads(package_path.read_bytes())
            self.assertEqual(package["release"], catalog["release"])
            self.assertNotIn("releaseProvenance", package)
            self.assertEqual(ref["sha256"], hashlib.sha256(package_path.read_bytes()).hexdigest())
            self.assertEqual(ref["version"], package["version"])

    def test_component_edit_propagates_hash_to_dependencies_and_catalog(self):
        root = self.pack / "alludium/ontology-components"
        component = root / "components/finance-screening.ontology.v1.json"
        component.write_bytes(component.read_bytes() + b"\n")
        digest = hashlib.sha256(component.read_bytes()).hexdigest()
        self.apply()
        package = json.loads((root / "packages/finance-screening.v1.json").read_bytes())
        references = [ref for ref in package["components"] if ref["kind"] == "ontology"]
        dependencies = [dep for ref in package["components"] for dep in ref["dependencies"]]
        self.assertTrue(dependencies)
        for ref in references + dependencies:
            self.assertEqual(ref["sha256"], digest)

    def test_bad_dependency_fails_before_any_writes(self):
        path = self.pack / "alludium/ontology-components/packages/finance-screening.v1.json"
        package = json.loads(path.read_bytes())
        package["components"][0]["dependencies"][0]["id"] = "missing"
        path.write_bytes(prepare.json_bytes(package))
        before = {p: p.read_bytes() for p in self.pack.rglob("*") if p.is_file()}
        with self.assertRaisesRegex(ValueError, "Unknown dependency"):
            prepare.metadata_outputs(self.pack, "99.0.0")
        self.assertEqual(before, {p: p.read_bytes() for p in before})

    def test_identity_mismatch_is_not_silently_repaired(self):
        path = self.pack / "alludium/ontology-components/components/finance-screening.ontology.v1.json"
        component = json.loads(path.read_bytes())
        component["version"] = "99.0.0"
        path.write_bytes(prepare.json_bytes(component))
        with self.assertRaisesRegex(ValueError, "version mismatch"):
            prepare.metadata_outputs(self.pack)

    def test_rejects_invalid_versions_and_downgrades(self):
        for version in ("v1.0.0", "01.0.0", "1.0.0-beta", "", "0.0.0"):
            with self.subTest(version=version), self.assertRaises(ValueError):
                prepare.metadata_outputs(self.pack, version)

    def test_rejects_path_escape(self):
        with self.assertRaisesRegex(ValueError, "escapes"):
            prepare.child_file(self.pack, "../outside.json")

    def test_cli_check_detects_drift_without_writing_and_generation_repairs_it(self):
        script = self.pack / "scripts/prepare_release.py"
        self.apply()
        path = self.pack / ".codex-plugin/plugin.json"
        plugin = json.loads(path.read_bytes())
        plugin["version"] = "0.0.0"
        path.write_bytes(prepare.json_bytes(plugin, canonical=False))
        before = path.read_bytes()
        result = subprocess.run([sys.executable, str(script), "--check"], capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(b"Stale release metadata", result.stderr)
        self.assertEqual(path.read_bytes(), before)
        subprocess.run([sys.executable, str(script)], check=True, capture_output=True)
        subprocess.run([sys.executable, str(script), "--check"], check=True, capture_output=True)

    def test_cli_check_detects_stale_markdown_without_rewriting_it(self):
        self.apply()
        script = self.pack / "scripts/prepare_release.py"
        path = next((self.pack / "agents").glob("*.md"))
        path.write_text("stale\n")
        result = subprocess.run([sys.executable, str(script), "--check"], capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(b"Stale generated file", result.stderr)
        self.assertEqual(path.read_text(), "stale\n")

    def test_version_update_preserves_manifest_comments_and_other_fields(self):
        path = self.pack / "alludium/manifest.yaml"
        text = path.read_text()
        current = prepare.yaml.safe_load(text)["pack"]["version"]
        text = text.replace(f"  version: {current}", f"  version: '{current}' # release version", 1)
        path.write_text(text)
        outputs = prepare.metadata_outputs(self.pack, "99.0.0")
        self.assertEqual(outputs[path].decode(), text.replace(f"'{current}' # release version", "99.0.0 # release version", 1))


if __name__ == "__main__":
    unittest.main()
