#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml


THIS_FILE = Path(__file__).resolve()
ROOT = THIS_FILE.parents[1]
REPO_ROOT = THIS_FILE.parents[3]
SECRET_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in [
        r"api[_-]?key\s*[:=]\s*['\"][^'\"]+['\"]",
        r"secret\s*[:=]\s*['\"][^'\"]+['\"]",
        r"token\s*[:=]\s*['\"][^'\"]+['\"]",
        r"-----BEGIN (?:RSA |EC |OPENSSH |)PRIVATE KEY-----",
    ]
]
PUBLIC_READINESS_PATTERNS = [
    (
        "legacy SVV naming",
        re.compile(pattern, re.IGNORECASE),
    )
    for pattern in [
        r"\bSVV\b",
        r"Sure Valley",
        r"\bsvv_",
        r"alludium-vc",
        r"/Users/",
        r"craft-ai-agents",
    ]
]


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def read_yaml(path: Path) -> Any:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return yaml.safe_load(handle)
    except Exception as exc:  # pragma: no cover - defensive CLI guard
        fail(f"Failed to parse YAML {path.relative_to(ROOT)}: {exc}")


def read_json(path: Path) -> Any:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except Exception as exc:  # pragma: no cover - defensive CLI guard
        fail(f"Failed to parse JSON {path.relative_to(ROOT)}: {exc}")


def parse_frontmatter(path: Path) -> dict[str, Any]:
    body = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    if not body.startswith("---\n"):
        fail(f"{path.relative_to(ROOT)} is missing YAML frontmatter")

    marker = body.find("\n---\n", 4)
    if marker == -1:
        fail(f"{path.relative_to(ROOT)} has invalid frontmatter delimiters")

    parsed = yaml.safe_load(body[4:marker])
    if not isinstance(parsed, dict):
        fail(f"{path.relative_to(ROOT)} frontmatter must be an object")
    return parsed


def validate_plugin_manifest(path: Path) -> None:
    manifest = read_json(path)
    if manifest.get("name") != "vc":
        fail(f"{path.relative_to(ROOT)} name must be vc")
    if manifest.get("skills") != "./skills/":
        fail(f"{path.relative_to(ROOT)} skills path must be ./skills/")
    if manifest.get("mcpServers") != "./.mcp.json":
        fail(f"{path.relative_to(ROOT)} mcpServers path must be ./.mcp.json")


def validate_skills(manifest: dict[str, Any]) -> set[str]:
    skill_ids = manifest["surfaces"]["skills"]["ids"]
    if len(skill_ids) != len(set(skill_ids)):
        fail("Duplicate skill IDs in alludium/manifest.yaml")

    discovered: set[str] = set()
    for skill_id in skill_ids:
        skill_dir = ROOT / "skills" / skill_id
        entry = skill_dir / "SKILL.md"
        if not entry.exists():
            fail(f"Manifest skill missing SKILL.md: {skill_id}")

        frontmatter = parse_frontmatter(entry)
        frontmatter_id = frontmatter.get("id", skill_id)
        if frontmatter_id != skill_id:
            fail(f"Skill directory {skill_id} does not match frontmatter id {frontmatter_id}")
        if not frontmatter.get("name"):
            fail(f"Skill {skill_id} is missing frontmatter name")
        if not frontmatter.get("description"):
            fail(f"Skill {skill_id} is missing frontmatter description")
        if frontmatter.get("internalOnly") is True:
            fail(f"Public plugin cannot include internalOnly skill: {skill_id}")

        discovered.add(skill_id)

    actual_dirs = {path.name for path in (ROOT / "skills").iterdir() if path.is_dir()}
    extra_dirs = actual_dirs - discovered
    if extra_dirs:
        fail(f"Skills present on disk but missing from manifest: {sorted(extra_dirs)}")

    return discovered


def validate_templates(manifest: dict[str, Any], skill_ids: set[str]) -> None:
    template_ids = manifest["surfaces"]["alludiumAgentTemplates"]["ids"]
    if len(template_ids) != len(set(template_ids)):
        fail("Duplicate Alludium agent-template IDs in alludium/manifest.yaml")

    for template_id in template_ids:
        template_path = ROOT / "alludium" / "agent-templates" / f"{template_id}.yaml"
        if not template_path.exists():
            fail(f"Manifest agent template missing YAML: {template_id}")

        template = read_yaml(template_path)
        if not isinstance(template, dict):
            fail(f"Agent template must be an object: {template_path.relative_to(ROOT)}")
        if template.get("id") != template_id:
            fail(f"Agent template file/id mismatch for {template_id}")

        for skill in template.get("skills", []):
            external_id = skill.get("externalId") if isinstance(skill, dict) else None
            if not external_id:
                fail(f"Template {template_id} has a skill entry without externalId")
            if external_id not in skill_ids:
                fail(f"Template {template_id} references missing skill {external_id}")


def validate_no_obvious_secrets() -> None:
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".svg"}:
            continue
        body = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in SECRET_PATTERNS:
            if pattern.search(body):
                fail(f"Potential secret-like value found in {path.relative_to(ROOT)}")


def validate_no_public_readiness_leakage() -> None:
    for path in REPO_ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or path.resolve() == THIS_FILE:
            continue
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".svg"}:
            continue
        body = path.read_text(encoding="utf-8", errors="ignore")
        for label, pattern in PUBLIC_READINESS_PATTERNS:
            if pattern.search(body):
                fail(f"Public-readiness leak ({label}) found in {path.relative_to(REPO_ROOT)}")


def main() -> None:
    validate_plugin_manifest(ROOT / ".codex-plugin" / "plugin.json")
    validate_plugin_manifest(ROOT / ".claude-plugin" / "plugin.json")
    read_json(ROOT / ".mcp.json")

    manifest = read_yaml(ROOT / "alludium" / "manifest.yaml")
    if not isinstance(manifest, dict):
        fail("alludium/manifest.yaml must be an object")
    if manifest.get("boundaries", {}).get("secretsAllowed") is not False:
        fail("Manifest must declare boundaries.secretsAllowed: false")

    skill_ids = validate_skills(manifest)
    validate_templates(manifest, skill_ids)
    recommendations_path = manifest["surfaces"]["alludiumMcpRecommendations"]["path"]
    if not (ROOT / recommendations_path).exists():
        fail(f"Missing Alludium MCP recommendations file: {recommendations_path}")
    read_yaml(ROOT / recommendations_path)
    validate_no_obvious_secrets()
    validate_no_public_readiness_leakage()

    print(
        "Validated vc pack: "
        f"{len(skill_ids)} skills, "
        f"{len(manifest['surfaces']['alludiumAgentTemplates']['ids'])} agent templates"
    )


if __name__ == "__main__":
    main()
