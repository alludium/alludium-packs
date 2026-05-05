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
EXPECTED_WORKSPACE_VARIABLE_BINDINGS = {
    "fundStage": "vc.fundStage",
    "fundSectors": "vc.fundSectors",
    "fundGeography": "vc.fundGeography",
}
TASK_TEMPLATE_REQUIRED_SKILL_REFERENCE_FIELDS = ["requiredSkills", "plannedRequiredSkills"]
TASK_TEMPLATE_AGENT_TEMPLATE_REFERENCE_FIELDS = [
    "recommendedAgentTemplate",
    "plannedRecommendedAgentTemplate",
    "preferredAgentType",
]
TASK_TEMPLATE_PLATFORM_CAPABILITY = "external-task-definition-template-ingest"


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
        if not isinstance(template.get("platform_managed"), bool):
            fail(f"Agent template {template_id} must explicitly declare platform_managed")

        prompt = template.get("prompt") or {}
        variables = prompt.get("variables") or []
        if variables and not isinstance(variables, list):
            fail(f"Agent template {template_id} prompt.variables must be a list")
        for variable in variables:
            if not isinstance(variable, dict):
                fail(f"Agent template {template_id} prompt variable entries must be objects")
            key = variable.get("key")
            binding = variable.get("binding")
            expected_path = EXPECTED_WORKSPACE_VARIABLE_BINDINGS.get(key)
            if expected_path is None:
                if binding is not None:
                    fail(
                        f"Template {template_id} variable {key} has unexpected workspace binding"
                    )
                continue
            if not isinstance(binding, dict):
                fail(f"Template {template_id} variable {key} must bind to {expected_path}")
            if binding.get("source") != "workspace.variable":
                fail(f"Template {template_id} variable {key} binding source must be workspace.variable")
            if binding.get("path") != expected_path:
                fail(f"Template {template_id} variable {key} binding path must be {expected_path}")
            if binding.get("fallback") != "Not configured":
                fail(f"Template {template_id} variable {key} binding fallback must be Not configured")
            if binding.get("overridePolicy") != "workspace_admin_only":
                fail(
                    f"Template {template_id} variable {key} binding overridePolicy must be workspace_admin_only"
                )

        for skill in template.get("skills", []):
            external_id = skill.get("externalId") if isinstance(skill, dict) else None
            if not external_id:
                fail(f"Template {template_id} has a skill entry without externalId")
            if external_id not in skill_ids:
                fail(f"Template {template_id} references missing skill {external_id}")


def require_string_list(value: Any, context: str) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        fail(f"{context} must be a list of strings")
    return value


def normalize_workspace_methodology_skills(value: Any, context: str) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        fail(f"{context} must be a list")

    skills: list[str] = []
    for item in value:
        if isinstance(item, str):
            skills.append(item)
            continue
        if isinstance(item, dict) and isinstance(item.get("skill"), str):
            skills.append(item["skill"])
            continue
        fail(f"{context} entries must be strings or objects with a skill string")
    return skills


def validate_task_template_reference_list(
    template_id: str,
    field_name: str,
    values: list[str],
    allowed_ids: set[str],
    allowed_label: str,
) -> None:
    missing = sorted(set(values) - allowed_ids)
    if missing:
        fail(
            f"Task template {template_id} {field_name} references missing {allowed_label}: {missing}"
        )


def validate_task_template_platform_ingest_contract(surface: dict[str, Any]) -> None:
    platform_ingest = surface.get("platformIngest")
    if not isinstance(platform_ingest, dict):
        fail("surfaces.taskDefinitionTemplates.platformIngest must be declared")
    if platform_ingest.get("requiresCapability") != TASK_TEMPLATE_PLATFORM_CAPABILITY:
        fail(
            "surfaces.taskDefinitionTemplates.platformIngest.requiresCapability must be "
            f"{TASK_TEMPLATE_PLATFORM_CAPABILITY}"
        )
    if not isinstance(platform_ingest.get("minimumPlatformVersion"), str):
        fail("surfaces.taskDefinitionTemplates.platformIngest.minimumPlatformVersion must be declared")
    if not isinstance(platform_ingest.get("status"), str):
        fail("surfaces.taskDefinitionTemplates.platformIngest.status must be declared")


def get_declared_project_type_dependencies(manifest: dict[str, Any]) -> set[str]:
    dependencies = manifest.get("dependencies") or {}
    if not isinstance(dependencies, dict):
        fail("Manifest dependencies must be an object when declared")
    project_type_dependencies = dependencies.get("projectTypes") or []
    if not isinstance(project_type_dependencies, list):
        fail("Manifest dependencies.projectTypes must be a list when declared")

    declared: set[str] = set()
    for dependency in project_type_dependencies:
        if not isinstance(dependency, dict):
            fail("Manifest dependencies.projectTypes entries must be objects")
        dependency_id = dependency.get("id")
        if not isinstance(dependency_id, str) or not dependency_id:
            fail("Manifest dependencies.projectTypes entries must declare id")
        declared.add(dependency_id)

    project_type_surface = manifest["surfaces"].get("projectTypes") or {}
    included_ids = project_type_surface.get("ids") if isinstance(project_type_surface, dict) else None
    if included_ids is not None:
        if not isinstance(included_ids, list) or not all(isinstance(item, str) for item in included_ids):
            fail("surfaces.projectTypes.ids must be a list of strings when declared")
        declared.update(included_ids)

    return declared


def validate_task_template_file(
    path: Path,
    expected_pack: dict[str, Any],
    skill_ids: set[str],
    agent_template_ids: set[str],
    declared_project_type_ids: set[str],
) -> str:
    template = read_yaml(path)
    relative_path = path.relative_to(ROOT)
    if not isinstance(template, dict):
        fail(f"Task definition template must be an object: {relative_path}")
    if template.get("kind") != "task-definition-template":
        fail(f"{relative_path} is not a task-definition-template")

    template_id = template.get("id")
    if not isinstance(template_id, str) or not template_id:
        fail(f"{relative_path} is missing id")
    if not isinstance(template.get("version"), str) or not template.get("version"):
        fail(f"Task template {template_id} is missing version")

    definition = template.get("definition")
    if not isinstance(definition, dict):
        fail(f"Task template {template_id} definition must be an object")
    if not isinstance(definition.get("name"), str) or not definition.get("name"):
        fail(f"Task template {template_id} is missing definition.name")
    if not isinstance(definition.get("slug"), str) or not definition.get("slug"):
        fail(f"Task template {template_id} is missing definition.slug")

    definition_json = definition.get("definitionJson")
    if definition_json is None:
        definition_json = {}
    if not isinstance(definition_json, dict):
        fail(f"Task template {template_id} definition.definitionJson must be an object")

    for field_name in TASK_TEMPLATE_REQUIRED_SKILL_REFERENCE_FIELDS:
        values = require_string_list(
            definition_json.get(field_name),
            f"Task template {template_id} definitionJson.{field_name}",
        )
        validate_task_template_reference_list(
            template_id,
            field_name,
            values,
            skill_ids,
            "skills",
        )
    validate_task_template_reference_list(
        template_id,
        "workspaceConfiguredMethodologySkills",
        normalize_workspace_methodology_skills(
            definition_json.get("workspaceConfiguredMethodologySkills"),
            f"Task template {template_id} definitionJson.workspaceConfiguredMethodologySkills",
        ),
        skill_ids,
        "skills",
    )

    for field_name in TASK_TEMPLATE_AGENT_TEMPLATE_REFERENCE_FIELDS:
        value = definition_json.get(field_name)
        if value is None:
            runtime = template.get("runtime") or {}
            if isinstance(runtime, dict):
                execution_profile = runtime.get("executionProfile") or {}
                if isinstance(execution_profile, dict):
                    value = execution_profile.get(field_name)
        if value is None:
            continue
        if not isinstance(value, str):
            fail(f"Task template {template_id} {field_name} must be a string")
        if value not in agent_template_ids:
            fail(f"Task template {template_id} {field_name} references missing agent template {value}")

    supported_project_types = require_string_list(
        definition_json.get("supportedProjectTypes"),
        f"Task template {template_id} definitionJson.supportedProjectTypes",
    )
    validate_task_template_reference_list(
        template_id,
        "supportedProjectTypes",
        supported_project_types,
        declared_project_type_ids,
        "declared project type dependencies",
    )

    pack_vertical_keys = expected_pack.get("verticalKeys") or []
    if expected_pack.get("availability") == "vertical" and not pack_vertical_keys:
        fail(f"Task template pack {expected_pack.get('id')} must declare verticalKeys")

    return template_id


def validate_task_definition_templates(
    manifest: dict[str, Any],
    skill_ids: set[str],
    agent_template_ids: set[str],
) -> None:
    surface = manifest["surfaces"].get("taskDefinitionTemplates")
    if not isinstance(surface, dict):
        fail("Manifest must declare surfaces.taskDefinitionTemplates")
    surface_path = surface.get("path")
    if not isinstance(surface_path, str) or not surface_path:
        fail("surfaces.taskDefinitionTemplates.path must be declared")
    manifest_template_ids = surface.get("ids")
    if not isinstance(manifest_template_ids, list) or not all(
        isinstance(item, str) for item in manifest_template_ids
    ):
        fail("surfaces.taskDefinitionTemplates.ids must be a list of strings")
    if len(manifest_template_ids) != len(set(manifest_template_ids)):
        fail("Duplicate task-definition-template IDs in alludium/manifest.yaml")
    validate_task_template_platform_ingest_contract(surface)
    declared_project_type_ids = get_declared_project_type_dependencies(manifest)

    task_root = ROOT / surface_path
    resolved_task_root = task_root.resolve()
    catalog_path = task_root / "catalog.v1.json"
    if not catalog_path.exists():
        fail(f"Missing task definition template catalog: {catalog_path.relative_to(ROOT)}")
    catalog = read_json(catalog_path)
    if not isinstance(catalog, dict):
        fail(f"{catalog_path.relative_to(ROOT)} must be an object")
    if catalog.get("kind") != "task-definition-template-catalog":
        fail(f"{catalog_path.relative_to(ROOT)} kind must be task-definition-template-catalog")

    discovered_ids: list[str] = []
    discovered_paths: set[Path] = set()
    for pack in catalog.get("packs") or []:
        if not isinstance(pack, dict):
            fail("Task definition template catalog packs must be objects")
        templates = pack.get("templates") or []
        if not isinstance(templates, list):
            fail(f"Task definition template catalog pack {pack.get('id')} templates must be a list")
        for entry in templates:
            relative_template_path = entry if isinstance(entry, str) else entry.get("path")
            if not isinstance(relative_template_path, str) or not relative_template_path:
                fail(f"Task definition template catalog pack {pack.get('id')} has an invalid entry")
            template_path = task_root / relative_template_path
            resolved_template_path = template_path.resolve()
            try:
                resolved_template_path.relative_to(resolved_task_root)
            except ValueError:
                fail(
                    "Task definition template catalog path escapes task-template surface: "
                    f"{relative_template_path}"
                )
            if not template_path.exists():
                fail(f"Task definition template catalog references missing file {relative_template_path}")
            discovered_paths.add(resolved_template_path)
            discovered_ids.append(
                validate_task_template_file(
                    resolved_template_path,
                    pack,
                    skill_ids,
                    agent_template_ids,
                    declared_project_type_ids,
                )
            )

    if len(discovered_ids) != len(set(discovered_ids)):
        fail("Duplicate task-definition-template IDs in catalog files")
    if set(discovered_ids) != set(manifest_template_ids):
        fail(
            "Manifest task-definition-template IDs do not match catalog files: "
            f"manifest_only={sorted(set(manifest_template_ids) - set(discovered_ids))}, "
            f"catalog_only={sorted(set(discovered_ids) - set(manifest_template_ids))}"
        )

    actual_yaml_paths = {path.resolve() for path in task_root.glob("**/*.yaml")}
    extra_yaml_paths = actual_yaml_paths - discovered_paths
    if extra_yaml_paths:
        fail(
            "Task definition template files present on disk but missing from catalog: "
            f"{sorted(str(path.relative_to(task_root)) for path in extra_yaml_paths)}"
        )


def validate_mcp_definitions(manifest: dict[str, Any], recommendations: dict[str, Any]) -> None:
    mcp_manifest = read_json(ROOT / manifest["surfaces"]["mcpServers"]["path"])
    mcp_servers = mcp_manifest.get("mcpServers")
    if not isinstance(mcp_servers, dict) or not mcp_servers:
        fail(".mcp.json must define at least one MCP server")

    for server_id, server in mcp_servers.items():
        if not isinstance(server, dict):
            fail(f".mcp.json server {server_id} must be an object")
        has_command = isinstance(server.get("command"), str)
        has_url = isinstance(server.get("url"), str)
        if has_command == has_url:
            fail(f".mcp.json server {server_id} must define exactly one of command or url")

    recommendation_ids = {
        item.get("externalId")
        for item in recommendations.get("recommendations", [])
        if isinstance(item, dict)
    }
    if None in recommendation_ids:
        fail("All MCP recommendations must include externalId")

    missing_from_plugin = recommendation_ids - set(mcp_servers)
    if missing_from_plugin:
        fail(f"MCP recommendations missing from .mcp.json: {sorted(missing_from_plugin)}")

    platform_only_ids = {
        item.get("externalId")
        for item in recommendations.get("platformOnlyTemplateIntegrations", [])
        if isinstance(item, dict)
    }
    if None in platform_only_ids:
        fail("All platform-only template integrations must include externalId")

    template_mcp_ids: set[str] = set()
    template_ids = manifest["surfaces"]["alludiumAgentTemplates"]["ids"]
    for template_id in template_ids:
        template = read_yaml(ROOT / "alludium" / "agent-templates" / f"{template_id}.yaml")
        template_mcp_ids.update((template.get("mcpServers") or {}).keys())

    allowed_template_mcp_ids = recommendation_ids | platform_only_ids
    missing_from_recommendations = template_mcp_ids - allowed_template_mcp_ids
    if missing_from_recommendations:
        fail(f"Template MCP references missing from MCP mapping: {sorted(missing_from_recommendations)}")

    missing_from_plugin = template_mcp_ids - set(mcp_servers)
    if missing_from_plugin:
        unexpected_missing = missing_from_plugin - platform_only_ids
        if unexpected_missing:
            fail(f"Template MCP references missing from .mcp.json: {sorted(unexpected_missing)}")


def validate_no_obvious_secrets() -> None:
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if "__pycache__" in path.parts or path.suffix == ".pyc":
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
        if "__pycache__" in path.parts or path.suffix == ".pyc":
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
    agent_template_ids = set(manifest["surfaces"]["alludiumAgentTemplates"]["ids"])
    validate_task_definition_templates(manifest, skill_ids, agent_template_ids)
    recommendations_path = manifest["surfaces"]["alludiumMcpRecommendations"]["path"]
    if not (ROOT / recommendations_path).exists():
        fail(f"Missing Alludium MCP recommendations file: {recommendations_path}")
    recommendations = read_yaml(ROOT / recommendations_path)
    if not isinstance(recommendations, dict):
        fail(f"{recommendations_path} must be an object")
    validate_mcp_definitions(manifest, recommendations)
    validate_no_obvious_secrets()
    validate_no_public_readiness_leakage()

    print(
        "Validated vc pack: "
        f"{len(skill_ids)} skills, "
        f"{len(manifest['surfaces']['alludiumAgentTemplates']['ids'])} agent templates, "
        f"{len(manifest['surfaces']['taskDefinitionTemplates']['ids'])} task definition templates"
    )


if __name__ == "__main__":
    main()
