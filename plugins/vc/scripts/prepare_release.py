#!/usr/bin/env python3
"""Generate VC release bookkeeping from the Pack manifest; never publish tags."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

import yaml

import generate_markdown
from release_identity import release_identity

PACK_ROOT = Path(__file__).resolve().parents[1]
SEMVER = re.compile(r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)")


def json_bytes(value: dict, *, canonical: bool = True) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=canonical) + "\n").encode()


def read_json(path: Path) -> dict:
    value = json.loads(path.read_bytes())
    if not isinstance(value, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return value


def child_file(root: Path, relative: str) -> Path:
    path = root / relative
    if Path(relative).is_absolute() or not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f"Path escapes ontology root: {relative}")
    if path.is_symlink():
        raise ValueError(f"Symlink is not a release source: {relative}")
    return path


def metadata_outputs(pack_root: Path, version: str | None = None) -> dict[Path, bytes]:
    """Plan all metadata before writing. Keep authored content and versions intact."""
    manifest_path = pack_root / "alludium/manifest.yaml"
    manifest_text = manifest_path.read_text()
    manifest = yaml.safe_load(manifest_text)
    if not isinstance(manifest, dict) or not isinstance(manifest.get("pack"), dict):
        raise ValueError("Manifest must contain a pack object")
    pack = manifest["pack"]
    current = pack.get("version")
    if not isinstance(current, str) or not SEMVER.fullmatch(current):
        raise ValueError("Current manifest version must be strict X.Y.Z")
    version = version if version is not None else current
    if not isinstance(version, str) or not SEMVER.fullmatch(version):
        raise ValueError("Pack version must be strict X.Y.Z (no v prefix or prerelease)")
    outputs: dict[Path, bytes] = {}
    plugin_paths = [pack_root / folder / "plugin.json" for folder in (".claude-plugin", ".codex-plugin")]
    plugins = {path: read_json(path) for path in plugin_paths}
    # Both input paths use the same local baseline. Remote/main monotonicity is
    # still the responsibility of validate_release_contract.py before pushing.
    baselines = [current, *(plugin.get("version") for plugin in plugins.values())]
    target = tuple(map(int, version.split(".")))
    for baseline in baselines:
        if isinstance(baseline, str) and SEMVER.fullmatch(baseline):
            if target < tuple(map(int, baseline.split("."))):
                raise ValueError(f"Pack version cannot move backwards from {baseline} to {version}")
    if version != current:
        # Patch only the pack.version scalar; preserve YAML formatting and comments.
        document = yaml.compose(manifest_text)
        pack_nodes = [value for key, value in document.value if key.value == "pack"]
        if len(pack_nodes) != 1 or not isinstance(pack_nodes[0], yaml.MappingNode):
            raise ValueError("Manifest must contain exactly one explicit pack mapping")
        version_nodes = [value for key, value in pack_nodes[0].value if key.value == "version"]
        if len(version_nodes) != 1 or not isinstance(version_nodes[0], yaml.ScalarNode):
            raise ValueError("Manifest must contain exactly one explicit pack.version scalar")
        version_node = version_nodes[0]
        manifest_text = (
            manifest_text[:version_node.start_mark.index]
            + version
            + manifest_text[version_node.end_mark.index:]
        )
    outputs[manifest_path] = manifest_text.encode()

    for path, plugin in plugins.items():
        plugin["version"] = version
        outputs[path] = json_bytes(plugin, canonical=False)

    # Only current-release metadata is derived; historical prose is authored.
    for relative in ("README.md", "alludium/inventory.md"):
        path = pack_root / relative
        body = path.read_text()
        label = f"**Version**: {version}"
        pattern = r"^\*\*Version\*\*:.*$"
        count = len(re.findall(pattern, body, flags=re.MULTILINE))
        if count > 1:
            raise ValueError(f"Multiple current-version labels: {path}")
        if count:
            body = re.sub(pattern, lambda _: label, body, flags=re.MULTILINE)
        else:
            title, separator, rest = body.partition("\n")
            if not separator or not title.startswith("# "):
                raise ValueError(f"Expected Markdown title: {path}")
            body = title + "\n\n" + label + "\n" + rest
        if relative == "README.md":
            for pattern in (
                r"(Their catalog and package provenance are re-pinned to `)v[^`]+(`)",
                r"(The current `)v[^`]+(` pack surface includes)",
            ):
                body, count = re.subn(pattern, lambda match: match[1] + f"v{version}" + match[2], body)
                if count != 1:
                    raise ValueError("README must contain exactly one of each current-release provenance/surface statement")
        outputs[path] = body.encode()

    release = release_identity({**pack, "version": version})
    root = pack_root / "alludium/ontology-components"
    catalog_path = root / "catalog.v1.json"
    catalog = read_json(catalog_path)
    catalog["release"] = release
    for package_ref in catalog["packages"]:
        package_path = child_file(root, package_ref["path"])
        package = read_json(package_path)
        package["release"] = release
        refs = package["components"]
        by_id = {ref["id"]: ref for ref in refs}
        if len(by_id) != len(refs):
            raise ValueError(f"Duplicate component IDs: {package_path}")
        for ref in refs:
            component_path = child_file(root, ref["path"])
            component = read_json(component_path)
            # An authored identity mismatch is not bookkeeping to silently fix.
            for field in ("id", "version", "kind", "lifecycle"):
                if ref[field] != component[field]:
                    raise ValueError(f"Component {field} mismatch: {component_path}")
            ref["sha256"] = hashlib.sha256(component_path.read_bytes()).hexdigest()
            ref["releaseProvenance"] = release
        for ref in refs:
            for dependency in ref["dependencies"]:
                target = by_id.get(dependency["id"])
                if target is None or dependency["version"] != target["version"]:
                    raise ValueError(f"Unknown dependency or version mismatch: {dependency['id']}")
                dependency["sha256"] = target["sha256"]
        encoded = json_bytes(package)
        outputs[package_path] = encoded
        package_ref["sha256"] = hashlib.sha256(encoded).hexdigest()
    outputs[catalog_path] = json_bytes(catalog)
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", help="Set pack.version once, then generate release metadata")
    parser.add_argument("--check", action="store_true", help="Check metadata and Markdown without writing")
    args = parser.parse_args()
    if args.check and args.version:
        parser.error("--check reads the manifest version; do not combine it with --version")
    try:
        outputs = metadata_outputs(PACK_ROOT, args.version)
        markdown = generate_markdown.expected_outputs()
        changed = [path for path, body in outputs.items() if path.read_bytes() != body]
        if args.check:
            for path in changed:
                print(f"Stale release metadata: {path.relative_to(PACK_ROOT)}", file=sys.stderr)
            try:
                generate_markdown.check_outputs(markdown)
            except SystemExit as error:
                raise ValueError("Run python3 plugins/vc/scripts/prepare_release.py to refresh metadata and Markdown") from error
            if changed:
                raise ValueError("Run python3 plugins/vc/scripts/prepare_release.py")
            print("Release metadata and generated Markdown are up to date")
            return
        for path in changed:
            path.write_bytes(outputs[path])
            print(f"Updated {path.relative_to(PACK_ROOT)}")
        generate_markdown.write_outputs(markdown)
        print("Release prepared locally. Run Pack and release-contract validation before pushing.")
    except (ValueError, KeyError, OSError, yaml.YAMLError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
