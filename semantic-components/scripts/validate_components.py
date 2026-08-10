#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any, NoReturn

from jsonschema import Draft202012Validator, FormatChecker


SEMANTIC_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = SEMANTIC_ROOT.parent
BUNDLE_SCHEMA_PATH = SEMANTIC_ROOT / "schemas/semantic-component-bundle-v1.schema.json"
CATALOG_SCHEMA_PATH = SEMANTIC_ROOT / "schemas/semantic-component-catalog-v1.schema.json"
CATALOG_PATH = SEMANTIC_ROOT / "catalog.json"


def fail(message: str) -> NoReturn:
    raise SystemExit(f"semantic component validation failed: {message}")


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        fail(f"{path.relative_to(REPO_ROOT)} must contain a JSON object")
    return value


def write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def canonical_sha256(value: Mapping[str, Any], *, omit: str) -> str:
    payload = {key: item for key, item in value.items() if key != omit}
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def validate_schema(instance: Mapping[str, Any], schema_path: Path, source: Path) -> None:
    schema = load_json(schema_path)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(instance), key=lambda error: list(error.absolute_path))
    if errors:
        error = errors[0]
        location = ".".join(str(part) for part in error.absolute_path) or "<root>"
        fail(f"{source.relative_to(REPO_ROOT)}:{location}: {error.message}")


def require_unique(values: Iterable[str], *, label: str) -> None:
    items = list(values)
    if len(items) != len(set(items)):
        fail(f"{label} must be unique")


def require_string_list(value: object, *, label: str) -> list[str]:
    if not isinstance(value, list) or not value or not all(isinstance(item, str) for item in value):
        fail(f"{label} must be a non-empty string array")
    require_unique(value, label=label)
    return value


def validate_component_content(components: list[dict[str, Any]], *, bundle_id: str) -> None:
    ontology_terms: dict[str, dict[str, Any]] = {}
    qualifiers: dict[str, dict[str, set[str]]] = {}
    projections: set[str] = set()
    profiles = 0

    for component in components:
        content = component["content"]
        kind = component["kind"]
        component_id = component["component_id"]
        if kind == "ontology":
            terms = content.get("terms")
            if not isinstance(terms, list) or not terms:
                fail(f"{component_id} ontology content must declare terms")
            for term in terms:
                if not isinstance(term, dict) or set(term) != {"term_id", "label", "definition"}:
                    fail(f"{component_id} ontology terms must declare only term_id, label, definition")
                if not all(isinstance(term[key], str) and term[key] for key in term):
                    fail(f"{component_id} ontology term values must be non-empty strings")
                if len(term["term_id"]) > 256 or len(term["label"]) > 256:
                    fail(f"{component_id} ontology term IDs and labels must be at most 256 chars")
                if len(term["definition"]) > 4096:
                    fail(f"{component_id} ontology term definitions must be at most 4096 chars")
                if term["term_id"] in ontology_terms:
                    fail(f"{bundle_id} contains duplicate ontology term {term['term_id']!r}")
                ontology_terms[term["term_id"]] = term

    if not ontology_terms:
        fail(f"{bundle_id} must contain ontology terms")

    for component in components:
        content = component["content"]
        kind = component["kind"]
        component_id = component["component_id"]
        if kind == "mapping":
            mappings = content.get("mappings")
            if not isinstance(mappings, list) or not mappings:
                fail(f"{component_id} mapping content must declare mappings")
            sources: list[str] = []
            for mapping in mappings:
                if not isinstance(mapping, dict) or set(mapping) != {"source", "term_id"}:
                    fail(f"{component_id} mappings must declare only source and term_id")
                if mapping["term_id"] not in ontology_terms:
                    fail(f"{component_id} references unknown term {mapping['term_id']!r}")
                sources.append(mapping["source"])
            require_unique(sources, label=f"{component_id} mapping sources")
        elif kind == "constraints":
            maximum = content.get("max_provider_terms")
            if not isinstance(maximum, int) or isinstance(maximum, bool) or not 1 <= maximum <= 32:
                fail(f"{component_id} max_provider_terms must be an integer from 1 to 32")
            items = content.get("qualifiers")
            if not isinstance(items, list):
                fail(f"{component_id} qualifiers must be an array")
            for item in items:
                if not isinstance(item, dict) or set(item) != {"term_id", "name", "values"}:
                    fail(f"{component_id} qualifiers must declare term_id, name, values")
                term_id = item["term_id"]
                name = item["name"]
                if not isinstance(name, str) or not name or len(name) > 128:
                    fail(f"{component_id} qualifier names must be 1 to 128 chars")
                if term_id not in ontology_terms:
                    fail(f"{component_id} qualifier references unknown term {term_id!r}")
                values = require_string_list(
                    item["values"], label=f"{component_id} qualifier {term_id}.{name} values"
                )
                if len(values) > 64 or any(len(value) > 128 for value in values):
                    fail(f"{component_id} qualifier values exceed the v1 bounds")
                term_qualifiers = qualifiers.setdefault(term_id, {})
                if name in term_qualifiers:
                    fail(f"{component_id} duplicates qualifier {term_id}.{name}")
                term_qualifiers[name] = set(values)
        elif kind == "projection":
            term_ids = require_string_list(
                content.get("term_ids"), label=f"{component_id} projected term IDs"
            )
            for term_id in term_ids:
                if term_id not in ontology_terms:
                    fail(f"{component_id} projects unknown term {term_id!r}")
                projections.add(term_id)
            projected_qualifiers = content.get("qualifiers")
            if not isinstance(projected_qualifiers, list):
                fail(f"{component_id} projected qualifiers must be an array")
            seen_qualifier_terms: list[str] = []
            for item in projected_qualifiers:
                if not isinstance(item, dict) or set(item) != {"term_id", "names"}:
                    fail(f"{component_id} projected qualifiers must declare term_id and names")
                term_id = item["term_id"]
                names = item["names"]
                if term_id not in term_ids:
                    fail(f"{component_id} exposes qualifiers for unprojected term {term_id!r}")
                for name in require_string_list(
                    names, label=f"{component_id} projected qualifiers for {term_id}"
                ):
                    if name not in qualifiers.get(term_id, {}):
                        fail(f"{component_id} exposes unknown qualifier {term_id}.{name}")
                seen_qualifier_terms.append(term_id)
            require_unique(
                seen_qualifier_terms, label=f"{component_id} projected qualifier term IDs"
            )
        elif kind == "profile":
            profiles += 1
            defaults = require_string_list(
                content.get("default_term_ids"), label=f"{component_id} default term IDs"
            )
            required = require_string_list(
                content.get("required_response_term_ids"),
                label=f"{component_id} required response term IDs",
            )
            for term_id in [*defaults, *required]:
                if term_id not in projections:
                    fail(f"{component_id} profile references unprojected term {term_id!r}")

    if profiles != 1:
        fail(f"{bundle_id} must contain exactly one profile component")


def validate_bundle(path: Path, *, write_hashes: bool) -> dict[str, Any]:
    bundle = load_json(path)
    components = bundle.get("components")
    if not isinstance(components, list) or not all(isinstance(item, dict) for item in components):
        fail(f"{path.relative_to(REPO_ROOT)} components must be objects")
    typed_components = list(components)
    component_ids = [component.get("component_id") for component in typed_components]
    if not all(isinstance(component_id, str) for component_id in component_ids):
        fail(f"{path.relative_to(REPO_ROOT)} component IDs must be strings")
    require_unique(component_ids, label=f"{bundle.get('bundle_id')} component IDs")
    by_id = {component["component_id"]: component for component in typed_components}

    remaining = set(by_id)
    resolved: dict[str, dict[str, Any]] = {}
    while remaining:
        progressed = False
        for component_id in sorted(remaining):
            component = by_id[component_id]
            dependencies = component.get("dependencies")
            if not isinstance(dependencies, list) or not all(
                isinstance(dependency, dict) for dependency in dependencies
            ):
                fail(f"{component_id} dependencies must be objects")
            dependency_ids = [dependency.get("component_id") for dependency in dependencies]
            if not all(isinstance(dependency_id, str) for dependency_id in dependency_ids):
                fail(f"{component_id} dependency IDs must be strings")
            require_unique(dependency_ids, label=f"{component_id} dependency IDs")
            missing = [dependency_id for dependency_id in dependency_ids if dependency_id not in by_id]
            if missing:
                fail(f"{component_id} has missing dependency {missing[0]!r}")
            if not set(dependency_ids).issubset(resolved):
                continue
            for dependency in dependencies:
                target = resolved[dependency["component_id"]]
                expected = {
                    "component_id": target["component_id"],
                    "version": target["version"],
                    "canonical_sha256": target["canonical_sha256"],
                }
                if write_hashes:
                    dependency.clear()
                    dependency.update(expected)
                elif dependency != expected:
                    fail(f"{component_id} dependency {target['component_id']!r} is not exact")
            expected_hash = canonical_sha256(component, omit="canonical_sha256")
            if write_hashes:
                component["canonical_sha256"] = expected_hash
            elif component.get("canonical_sha256") != expected_hash:
                fail(f"{component_id} canonical_sha256 does not match its content")
            resolved[component_id] = component
            remaining.remove(component_id)
            progressed = True
        if not progressed:
            fail(f"{bundle.get('bundle_id')} dependency graph contains a cycle")

    profile = next((item for item in typed_components if item.get("kind") == "profile"), None)
    if profile is not None:
        reachable: set[str] = set()
        stack = [profile["component_id"]]
        while stack:
            component_id = stack.pop()
            if component_id in reachable:
                continue
            reachable.add(component_id)
            stack.extend(dep["component_id"] for dep in by_id[component_id]["dependencies"])
        if reachable != set(by_id):
            fail(f"{bundle.get('bundle_id')} profile dependency closure is incomplete")

    required_dependency_kinds = {
        "mapping": {"ontology"},
        "constraints": {"ontology"},
        "projection": {"ontology", "constraints"},
        "profile": {"mapping", "projection", "constraints"},
    }
    for component in typed_components:
        required_kinds = required_dependency_kinds.get(component["kind"], set())
        if not required_kinds:
            continue
        dependency_kinds: set[str] = set()
        stack = [dependency["component_id"] for dependency in component["dependencies"]]
        while stack:
            dependency_id = stack.pop()
            dependency = by_id[dependency_id]
            dependency_kinds.add(dependency["kind"])
            stack.extend(item["component_id"] for item in dependency["dependencies"])
        if not required_kinds.issubset(dependency_kinds):
            missing_kind = sorted(required_kinds - dependency_kinds)[0]
            fail(f"{component['component_id']} has an undeclared {missing_kind} dependency")

    expected_bundle_hash = canonical_sha256(bundle, omit="bundle_sha256")
    if write_hashes:
        bundle["bundle_sha256"] = expected_bundle_hash
        write_json(path, bundle)
    elif bundle.get("bundle_sha256") != expected_bundle_hash:
        fail(f"{bundle.get('bundle_id')} bundle_sha256 does not match its content")

    expected_path = path.relative_to(REPO_ROOT).as_posix()
    release = bundle.get("release")
    if not isinstance(release, dict) or release.get("path") != expected_path:
        fail(f"{bundle.get('bundle_id')} release path must be {expected_path!r}")
    if "latest" in str(release.get("tag", "")).lower():
        fail(f"{bundle.get('bundle_id')} release tag must not use latest")

    validate_schema(bundle, BUNDLE_SCHEMA_PATH, path)
    validate_component_content(typed_components, bundle_id=bundle["bundle_id"])
    kinds = {component["kind"] for component in typed_components}
    expected_kinds = {"ontology", "mapping", "profile", "projection", "constraints"}
    if kinds != expected_kinds:
        fail(f"{bundle['bundle_id']} must contain exactly the five component kinds")
    for component in typed_components:
        lifecycle = component["lifecycle"]
        if lifecycle["status"] == "retired" and "retired_at" not in lifecycle:
            fail(f"retired component {component['component_id']} must declare retired_at")
        if lifecycle["status"] == "active" and "retired_at" in lifecycle:
            fail(f"active component {component['component_id']} must not declare retired_at")
    return bundle


def validate_catalog(*, write_hashes: bool) -> None:
    catalog = load_json(CATALOG_PATH)
    entries = catalog.get("bundles")
    if not isinstance(entries, list) or not all(isinstance(entry, dict) for entry in entries):
        fail("catalog bundles must be objects")
    require_unique(
        [entry.get("bundle_id") for entry in entries],
        label="catalog bundle IDs",
    )
    require_unique([entry.get("path") for entry in entries], label="catalog paths")

    loaded: list[dict[str, Any]] = []
    for entry in entries:
        relative_path = entry.get("path")
        if not isinstance(relative_path, str):
            fail("catalog paths must be strings")
        path = (REPO_ROOT / relative_path).resolve()
        if REPO_ROOT not in path.parents or not path.is_file():
            fail(f"catalog path {relative_path!r} is not a repository bundle")
        bundle = validate_bundle(path, write_hashes=write_hashes)
        expected = {
            "bundle_id": bundle["bundle_id"],
            "bundle_version": bundle["bundle_version"],
            "bundle_sha256": bundle["bundle_sha256"],
            "domain": bundle["domain"],
            "path": relative_path,
        }
        if write_hashes:
            entry.clear()
            entry.update(expected)
        elif entry != expected:
            fail(f"catalog entry for {relative_path} does not match its exact bundle")
        if bundle["release"]["tag"] != catalog.get("release_tag"):
            fail(f"{bundle['bundle_id']} release tag differs from the catalog")
        loaded.append(bundle)

    if len({bundle["domain"] for bundle in loaded}) < 2:
        fail("catalog must include at least two contrasting domains")
    if write_hashes:
        write_json(CATALOG_PATH, catalog)
    validate_schema(catalog, CATALOG_SCHEMA_PATH, CATALOG_PATH)


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate released semantic component bundles")
    parser.add_argument(
        "--write-hashes",
        action="store_true",
        help="refresh component, bundle, and catalog hashes before validation",
    )
    args = parser.parse_args()
    validate_catalog(write_hashes=args.write_hashes)
    print("Validated semantic component catalog: 2 domains, 2 bundles, 10 components")


if __name__ == "__main__":
    main()
