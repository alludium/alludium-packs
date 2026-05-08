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
WORKSPACE_VARIABLE_VALUE_TYPES = {"string", "number", "boolean", "object", "array"}
WORKSPACE_VARIABLE_RENDER_TYPES = {"text", "textarea", "select", "checkbox", "number"}
WORKSPACE_VARIABLE_REQUIREMENT_LEVELS = {"optional", "recommended", "required"}
WORKSPACE_VARIABLE_SENSITIVITY_LEVELS = {"standard", "sensitive"}
APPLICATION_RECOMMENDATION_STATUSES = {"available", "future", "missing"}
APPLICATION_RECOMMENDATION_LEVELS = {"required", "recommended", "optional"}
TASK_TEMPLATE_REQUIRED_SKILL_REFERENCE_FIELDS = ["requiredSkills", "plannedRequiredSkills"]
TASK_TEMPLATE_AGENT_TEMPLATE_REFERENCE_FIELDS = [
    "recommendedAgentTemplate",
    "plannedRecommendedAgentTemplate",
    "preferredAgentType",
]
TASK_TEMPLATE_PLATFORM_CAPABILITY = "external-task-definition-template-ingest"
PROJECT_TYPE_PLATFORM_CAPABILITY = "external-project-type-ingest"
EXPECTED_VC_TASK_TEMPLATE_VERTICAL_KEYS = ["venture_capital", "vc"]
PROJECT_TYPE_FIELD_KINDS = {"date", "enum", "member", "number", "text"}
PROJECT_TASK_MAPPING_SOURCES = {"constant", "project.field", "project.id", "project.state"}
PROJECT_TASK_MAPPING_TARGETS = {"project.field", "project.state"}
PROJECT_TASK_ACTIVATION_MODES = {"manual", "manual_review", "auto_start"}
PROJECT_SCOPES = {"project_instance", "project_management"}
DEFAULT_PROJECT_SCOPE = "project_instance"
VC_DEAL_ROOM_LIFECYCLE_STAGES = {
    "intake",
    "assessment",
    "diligence",
    "review",
    "term_sheet",
    "closing",
}
VC_DEAL_ROOM_REPLACED_TASK_FIELDS = {"pitch_deck_url", "meeting_transcript_url"}
VC_DEAL_ROOM_FORBIDDEN_TASK_FIELDS = {
    "prior_task_outputs",
    "team_review_pack",
    "stage_outputs",
    "dd_summaries",
    "ic_memo",
    "ic_pack",
    "closing_summary",
    "investment_terms",
    "architecture_docs",
    "financial_statements",
    "forecast_model",
    "closing_workplan",
    "cp_checklist",
    "evidence_links",
}
VC_DEAL_ROOM_FORBIDDEN_CONTEXT_FIELDS = {
    "deal_room_url",
    "source_artifacts",
    "open_questions",
    "prior_task_outputs",
}
ARTIFACT_FIELD_KEY_PATTERN = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*_artifact_id$")
VC_ARTIFACT_OUTPUTS = {
    "source-thesis-targets": ["thesis_target_list_artifact_id"],
    "prepare-lead-gen-packet": ["lead_generation_packet_artifact_id"],
    "screen-inbound-opportunity": ["first_look_scorecard_artifact_id"],
    "request-founder-materials": ["founder_materials_request_artifact_id"],
    "prepare-initial-call": ["initial_call_brief_artifact_id"],
    "summarize-initial-call": ["customer_insights_artifact_id"],
    "run-follow-up-evaluation": ["follow_up_evaluation_artifact_id"],
    "run-ten-factor-screen": ["ten_factor_scorecard_artifact_id"],
    "generate-82-factor-questions": ["eighty_two_factor_questions_artifact_id"],
    "run-founder-evaluation": ["founder_evaluation_artifact_id"],
    "prepare-team-review-pack": ["team_review_pack_artifact_id"],
    "prepare-partner-review-pack": ["partner_review_pack_artifact_id"],
    "run-commercial-dd": [
        "commercial_dd_artifact_id",
        "market_analysis_artifact_id",
        "customer_reference_summary_artifact_id",
    ],
    "run-financial-dd": [
        "financial_dd_artifact_id",
        "unit_economics_artifact_id",
    ],
    "run-technical-dd": ["technical_dd_artifact_id"],
    "create-ic-memo": ["investment_memo_artifact_id"],
    "review-ic-memo": ["ic_memo_review_artifact_id"],
    "prepare-ic-agenda": ["ic_agenda_artifact_id"],
    "record-ic-decision": ["ic_decision_record_artifact_id"],
    "review-term-sheet": ["term_sheet_review_artifact_id"],
    "manage-closing-checklist": ["closing_checklist_artifact_id"],
    "verify-conditions-precedent": ["conditions_precedent_verification_artifact_id"],
    "prepare-portfolio-onboarding": ["portfolio_onboarding_plan_artifact_id"],
}
VC_ARTIFACT_INPUTS = {
    "screen-inbound-opportunity": ["pitch_deck_artifact_id"],
    "prepare-initial-call": ["pitch_deck_artifact_id"],
    "summarize-initial-call": ["meeting_record_artifact_ids"],
    "run-follow-up-evaluation": [
        "first_look_scorecard_artifact_id",
        "customer_insights_artifact_id",
    ],
    "run-ten-factor-screen": ["pitch_deck_artifact_id"],
    "run-financial-dd": ["financial_source_artifact_ids"],
    "run-technical-dd": ["technical_source_artifact_ids"],
    "prepare-team-review-pack": [
        "commercial_dd_artifact_id",
        "financial_dd_artifact_id",
        "founder_evaluation_artifact_id",
        "technical_dd_artifact_id",
        "eighty_two_factor_questions_artifact_id",
    ],
    "prepare-partner-review-pack": [
        "commercial_dd_artifact_id",
        "financial_dd_artifact_id",
        "founder_evaluation_artifact_id",
        "technical_dd_artifact_id",
        "eighty_two_factor_questions_artifact_id",
        "team_review_pack_artifact_id",
    ],
    "create-ic-memo": [
        "commercial_dd_artifact_id",
        "financial_dd_artifact_id",
        "founder_evaluation_artifact_id",
        "technical_dd_artifact_id",
        "eighty_two_factor_questions_artifact_id",
        "team_review_pack_artifact_id",
        "partner_review_pack_artifact_id",
    ],
    "prepare-ic-agenda": ["investment_memo_artifact_id"],
    "review-ic-memo": ["investment_memo_artifact_id", "ic_agenda_artifact_id"],
    "record-ic-decision": [
        "investment_memo_artifact_id",
        "ic_agenda_artifact_id",
    ],
    "manage-closing-checklist": [
        "ic_decision_record_artifact_id",
        "term_sheet_review_artifact_id",
        "closing_source_artifact_ids",
    ],
    "verify-conditions-precedent": [
        "closing_checklist_artifact_id",
        "closing_source_artifact_ids",
    ],
    "review-term-sheet": ["term_sheet_artifact_id"],
    "prepare-portfolio-onboarding": [
        "ic_decision_record_artifact_id",
        "closing_checklist_artifact_id",
        "conditions_precedent_verification_artifact_id",
    ],
}


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


def resolve_manifest_surface_path(
    manifest: dict[str, Any],
    surface_key: str,
    expected_kind: str,
) -> Path:
    surface = manifest["surfaces"].get(surface_key)
    if not isinstance(surface, dict):
        fail(f"Manifest must declare surfaces.{surface_key}")
    surface_path = surface.get("path")
    if not isinstance(surface_path, str) or not surface_path:
        fail(f"surfaces.{surface_key}.path must be declared")

    resolved = (ROOT / surface_path).resolve()
    try:
        resolved.relative_to(ROOT.resolve())
    except ValueError:
        fail(f"surfaces.{surface_key}.path must resolve inside the pack root")

    if expected_kind == "file" and not resolved.is_file():
        fail(f"surfaces.{surface_key}.path must reference an existing file: {surface_path}")
    if expected_kind == "directory" and not resolved.is_dir():
        fail(f"surfaces.{surface_key}.path must reference an existing directory: {surface_path}")

    return resolved


def validate_workspace_variables(manifest: dict[str, Any]) -> set[str]:
    variables_path = resolve_manifest_surface_path(manifest, "workspaceVariables", "file")
    surface = read_yaml(variables_path)
    if not isinstance(surface, dict):
        fail(f"{variables_path.relative_to(ROOT)} must be an object")
    if not isinstance(surface.get("schemaVersion"), str):
        fail(f"{variables_path.relative_to(ROOT)} must declare schemaVersion")
    if surface.get("status") != "platform-workspace-variable-declarations":
        fail(
            f"{variables_path.relative_to(ROOT)} status must be "
            "platform-workspace-variable-declarations"
        )

    variables = surface.get("workspaceVariables")
    if not isinstance(variables, list) or not variables:
        fail(f"{variables_path.relative_to(ROOT)} workspaceVariables must be a non-empty list")

    keys: set[str] = set()
    for variable in variables:
        if not isinstance(variable, dict):
            fail(f"{variables_path.relative_to(ROOT)} workspaceVariables entries must be objects")

        namespace = variable.get("namespace")
        key = variable.get("key")
        if not isinstance(namespace, str) or not namespace:
            fail("Workspace variables must declare namespace")
        if not isinstance(key, str) or not key:
            fail("Workspace variables must declare key")
        variable_key = f"{namespace}.{key}"
        if variable_key in keys:
            fail(f"Duplicate workspace variable declaration: {variable_key}")
        keys.add(variable_key)

        for field_name in ["label", "description"]:
            if not isinstance(variable.get(field_name), str) or not variable.get(field_name):
                fail(f"Workspace variable {variable_key} must declare {field_name}")
        if variable.get("valueType") not in WORKSPACE_VARIABLE_VALUE_TYPES:
            fail(f"Workspace variable {variable_key} has invalid valueType")
        render_metadata = variable.get("renderMetadata")
        if not isinstance(render_metadata, dict):
            fail(f"Workspace variable {variable_key} must declare renderMetadata")
        if render_metadata.get("render") not in WORKSPACE_VARIABLE_RENDER_TYPES:
            fail(f"Workspace variable {variable_key} has invalid renderMetadata.render")
        if variable.get("requirement") not in WORKSPACE_VARIABLE_REQUIREMENT_LEVELS:
            fail(f"Workspace variable {variable_key} has invalid requirement")
        if variable.get("sensitivity") not in WORKSPACE_VARIABLE_SENSITIVITY_LEVELS:
            fail(f"Workspace variable {variable_key} has invalid sensitivity")
        if "defaultValue" in variable:
            fail(f"Public workspace variable {variable_key} must not declare defaultValue")

    return keys


def validate_application_recommendations(
    manifest: dict[str, Any],
    recommendations: dict[str, Any],
) -> None:
    app_surface_path = resolve_manifest_surface_path(
        manifest,
        "alludiumApplicationRecommendations",
        "file",
    )
    mcp_surface_path = resolve_manifest_surface_path(
        manifest,
        "alludiumMcpRecommendations",
        "file",
    )
    app_surface = recommendations
    if app_surface_path != mcp_surface_path:
        app_surface = read_yaml(app_surface_path)
        if not isinstance(app_surface, dict):
            fail(f"{app_surface_path.relative_to(ROOT)} must be an object")

    if "applicationRecommendations" in app_surface:
        fail("Use a single recommendations list; applicationRecommendations must not be declared")

    application_recommendations = app_surface.get("recommendations")
    if not isinstance(application_recommendations, list) or not application_recommendations:
        fail("recommendations must be a non-empty list")

    mcp_manifest = read_json(ROOT / manifest["surfaces"]["mcpServers"]["path"])
    mcp_servers = mcp_manifest.get("mcpServers")
    if not isinstance(mcp_servers, dict):
        fail(".mcp.json must define mcpServers")

    ids: set[str] = set()
    for recommendation in application_recommendations:
        if not isinstance(recommendation, dict):
            fail("recommendations entries must be objects")
        if "id" in recommendation or "title" in recommendation or "externalMcpId" in recommendation:
            fail(
                "Application recommendations must use the integrated MCP mapping contract "
                "(externalId/name/applicationRecommendation), not id/title/externalMcpId"
            )
        recommendation_id = recommendation.get("externalId")
        if not isinstance(recommendation_id, str) or not recommendation_id:
            fail("recommendations entries must declare externalId")
        if recommendation_id in ids:
            fail(f"Duplicate recommendation externalId: {recommendation_id}")
        ids.add(recommendation_id)

        for field_name in ["name", "use"]:
            if not isinstance(recommendation.get(field_name), str) or not recommendation.get(
                field_name
            ):
                fail(f"Application recommendation {recommendation_id} must declare {field_name}")
        if not isinstance(recommendation.get("category"), str) or not recommendation.get("category"):
            fail(f"Application recommendation {recommendation_id} must declare category")
        status = recommendation.get("status", "available")
        if status not in APPLICATION_RECOMMENDATION_STATUSES:
            fail(f"Application recommendation {recommendation_id} has invalid status")

        recommendation_status = recommendation.get("recommendationStatus")
        recommendation_metadata = recommendation.get("applicationRecommendation")
        if recommendation_status is None and recommendation_metadata is None:
            continue
        if recommendation_status not in APPLICATION_RECOMMENDATION_LEVELS:
            fail(f"Application recommendation {recommendation_id} has invalid recommendationStatus")
        if not isinstance(recommendation_metadata, dict):
            fail(
                f"Application recommendation {recommendation_id} must declare "
                "applicationRecommendation"
            )
        if status in {"future", "missing"} and not isinstance(recommendation.get("reason"), str):
            fail(f"Application recommendation {recommendation_id} must explain unavailable status")

        for metadata_field in [
            "pickerGroup",
            "systemCategory",
            "authorizationBoundary",
            "evidenceRequirement",
        ]:
            if not isinstance(recommendation_metadata.get(metadata_field), str) or not recommendation_metadata.get(metadata_field):
                fail(
                    f"Application recommendation {recommendation_id} metadata must declare "
                    f"{metadata_field}"
                )
        if "unlocks" in recommendation_metadata:
            require_string_list(
                recommendation_metadata.get("unlocks"),
                f"Application recommendation {recommendation_id} applicationRecommendation.unlocks",
            )
        if "alternatives" in recommendation_metadata:
            require_string_list(
                recommendation_metadata.get("alternatives"),
                f"Application recommendation {recommendation_id} applicationRecommendation.alternatives",
            )

        if status == "available" and recommendation_id not in mcp_servers:
            fail(
                f"Application recommendation {recommendation_id} is available but missing "
                "from .mcp.json"
            )


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


def normalize_supported_project_scopes(
    template_id: str,
    definition_json: dict[str, Any],
    supported_project_types: list[str],
) -> list[str]:
    value = definition_json.get("supportedProjectScopes")
    if value is None:
        return [DEFAULT_PROJECT_SCOPE] if supported_project_types else []

    scopes = require_string_list(
        value,
        f"Task template {template_id} definitionJson.supportedProjectScopes",
    )
    if not supported_project_types:
        fail(
            f"Task template {template_id} definitionJson.supportedProjectScopes "
            "requires supportedProjectTypes"
        )
    if not scopes:
        fail(f"Task template {template_id} definitionJson.supportedProjectScopes must not be empty")
    unknown_scopes = sorted(set(scopes) - PROJECT_SCOPES)
    if unknown_scopes:
        fail(
            f"Task template {template_id} definitionJson.supportedProjectScopes "
            f"contains unknown scopes: {unknown_scopes}"
        )
    if len(scopes) != len(set(scopes)):
        fail(f"Task template {template_id} definitionJson.supportedProjectScopes has duplicates")
    return scopes


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


def validate_project_type_platform_ingest_contract(surface: dict[str, Any]) -> None:
    platform_ingest = surface.get("platformIngest")
    if not isinstance(platform_ingest, dict):
        fail("surfaces.projectTypes.platformIngest must be declared")
    if platform_ingest.get("requiresCapability") != PROJECT_TYPE_PLATFORM_CAPABILITY:
        fail(
            "surfaces.projectTypes.platformIngest.requiresCapability must be "
            f"{PROJECT_TYPE_PLATFORM_CAPABILITY}"
        )
    if not isinstance(platform_ingest.get("minimumPlatformVersion"), str):
        fail("surfaces.projectTypes.platformIngest.minimumPlatformVersion must be declared")
    if not isinstance(platform_ingest.get("status"), str):
        fail("surfaces.projectTypes.platformIngest.status must be declared")


def field_map(template_id: str, section_name: str, fields: Any) -> dict[str, dict[str, Any]]:
    if fields is None:
        return {}
    if not isinstance(fields, list):
        fail(f"Task template {template_id} fields.{section_name} must be a list")

    mapped: dict[str, dict[str, Any]] = {}
    positions: dict[int, str] = {}
    for field in fields:
        if not isinstance(field, dict):
            fail(f"Task template {template_id} fields.{section_name} entries must be objects")
        key = field.get("key")
        if not isinstance(key, str) or not key:
            fail(f"Task template {template_id} fields.{section_name} entries must declare key")
        if key in mapped:
            fail(f"Task template {template_id} fields.{section_name} has duplicate key {key}")
        position = field.get("position")
        if not isinstance(position, int) or isinstance(position, bool):
            fail(
                f"Task template {template_id} fields.{section_name}.{key} must declare "
                "an integer position"
            )
        duplicate_key = positions.get(position)
        if duplicate_key is not None:
            fail(
                f"Task template {template_id} fields.{section_name} has duplicate "
                f"position {position}: {duplicate_key}, {key}"
            )
        positions[position] = key
        mapped[key] = field
    return mapped


def validate_artifact_field_shape(
    template_id: str,
    section_name: str,
    field: dict[str, Any],
) -> None:
    key = field["key"]
    is_artifact_key = key.endswith("_artifact_id")
    is_file_field = field.get("fieldType") == "file"
    if not is_artifact_key and not is_file_field:
        return
    if not ARTIFACT_FIELD_KEY_PATTERN.match(key):
        fail(
            f"Task template {template_id} fields.{section_name}.{key} must match "
            f"{ARTIFACT_FIELD_KEY_PATTERN.pattern}"
        )
    if field.get("fieldType") != "file":
        fail(f"Task template {template_id} fields.{section_name}.{key} must use fieldType: file")
    if field.get("required") is not True:
        fail(f"Task template {template_id} fields.{section_name}.{key} must set required: true")


def validate_required_artifact_fields(
    template_id: str,
    slug: str,
    fields: dict[str, Any],
) -> None:
    input_fields = field_map(template_id, "input", fields.get("input"))
    context_fields = field_map(template_id, "context", fields.get("context"))
    output_fields = field_map(template_id, "output", fields.get("output"))
    for section_name, mapped_fields in [
        ("input", input_fields),
        ("context", context_fields),
        ("output", output_fields),
    ]:
        for field in mapped_fields.values():
            validate_artifact_field_shape(template_id, section_name, field)

    for key in VC_ARTIFACT_INPUTS.get(slug, []):
        field = input_fields.get(key)
        if field is None:
            fail(f"Task template {template_id} ({slug}) is missing required artifact input {key}")
        validate_artifact_field_shape(template_id, "input", field)

    for key in VC_ARTIFACT_OUTPUTS.get(slug, []):
        field = output_fields.get(key)
        if field is None:
            fail(f"Task template {template_id} ({slug}) is missing required artifact output {key}")
        validate_artifact_field_shape(template_id, "output", field)


def validate_vc_deal_room_task_template_shape(
    template_id: str,
    slug: str,
    definition_json: dict[str, Any],
    fields: dict[str, Any],
    supported_project_types: list[str],
) -> None:
    if "vc_deal_room" not in supported_project_types:
        return

    stage = definition_json.get("stage")
    if stage not in VC_DEAL_ROOM_LIFECYCLE_STAGES:
        fail(
            f"Task template {template_id} ({slug}) definitionJson.stage must be one of "
            f"{sorted(VC_DEAL_ROOM_LIFECYCLE_STAGES)} for vc_deal_room"
        )

    for section_name in ["input", "context", "output"]:
        for field_key in field_map(template_id, section_name, fields.get(section_name)):
            if field_key in VC_DEAL_ROOM_FORBIDDEN_TASK_FIELDS:
                fail(
                    f"Task template {template_id} ({slug}) fields.{section_name}.{field_key} "
                    "must be replaced by explicit task fields or artifacts"
                )
            if field_key in VC_DEAL_ROOM_REPLACED_TASK_FIELDS:
                fail(
                    f"Task template {template_id} ({slug}) fields.{section_name}.{field_key} "
                    "must use the artifact-backed replacement field"
                )

    for field_key in field_map(template_id, "context", fields.get("context")):
        if field_key in VC_DEAL_ROOM_FORBIDDEN_CONTEXT_FIELDS:
            fail(
                f"Task template {template_id} ({slug}) fields.context.{field_key} "
                "must be modeled as an explicit input/output or left to runtime task Q&A context"
            )


def validate_project_type_field(project_type_id: str, field: Any) -> tuple[str, str]:
    if not isinstance(field, dict):
        fail(f"Project type {project_type_id} fieldsSchema entries must be objects")
    field_id = field.get("id")
    if not isinstance(field_id, str) or not field_id:
        fail(f"Project type {project_type_id} field is missing id")
    field_key = field.get("key")
    if not isinstance(field_key, str) or not field_key:
        fail(f"Project type {project_type_id} field {field_id} is missing key")
    if not isinstance(field.get("label"), str) or not field.get("label"):
        fail(f"Project type {project_type_id} field {field_key} is missing label")
    field_kind = field.get("kind")
    if field_kind not in PROJECT_TYPE_FIELD_KINDS:
        fail(
            f"Project type {project_type_id} field {field_key} kind must be one of "
            f"{sorted(PROJECT_TYPE_FIELD_KINDS)}"
        )
    if not isinstance(field.get("required"), bool):
        fail(f"Project type {project_type_id} field {field_key} must declare required as a boolean")
    if field_kind == "enum":
        options = field.get("options")
        if not isinstance(options, list) or not options:
            fail(f"Project type {project_type_id} enum field {field_key} must declare options")
        option_values: list[str] = []
        for option in options:
            if not isinstance(option, dict):
                fail(f"Project type {project_type_id} enum field {field_key} options must be objects")
            option_value = option.get("value")
            if not isinstance(option_value, str) or not option_value:
                fail(f"Project type {project_type_id} enum field {field_key} option is missing value")
            if not isinstance(option.get("label"), str) or not option.get("label"):
                fail(f"Project type {project_type_id} enum field {field_key} option is missing label")
            option_values.append(option_value)
        if len(option_values) != len(set(option_values)):
            fail(f"Project type {project_type_id} enum field {field_key} has duplicate option values")
    return field_id, field_key


def validate_vc_deal_room_command_view(project_type_id: str, initial_version: dict[str, Any]) -> None:
    command_view = initial_version.get("commandView")
    if not isinstance(command_view, dict):
        fail(f"Project type {project_type_id} initialVersion.commandView must be declared")

    for field_name in [
        "key",
        "typeLabel",
        "collectionLabel",
        "overviewTitle",
        "overviewAriaLabel",
        "overviewFallback",
        "executionTitle",
    ]:
        if not isinstance(command_view.get(field_name), str) or not command_view.get(field_name):
            fail(f"Project type {project_type_id} commandView.{field_name} must be declared")

    stage_groups = command_view.get("stageGroups")
    if not isinstance(stage_groups, list) or not stage_groups:
        fail(f"Project type {project_type_id} commandView.stageGroups must be a non-empty list")
    lifecycle_states = set(require_string_list(
        initial_version.get("lifecycleStates"),
        f"Project type {project_type_id} initialVersion.lifecycleStates",
    ))
    stage_group_keys: set[str] = set()
    for stage_group in stage_groups:
        if not isinstance(stage_group, dict):
            fail(f"Project type {project_type_id} commandView.stageGroups entries must be objects")
        for field_name in ["key", "label"]:
            if not isinstance(stage_group.get(field_name), str) or not stage_group.get(field_name):
                fail(f"Project type {project_type_id} commandView.stageGroups entries must declare {field_name}")
        if stage_group["key"] in stage_group_keys:
            fail(f"Project type {project_type_id} commandView.stageGroups has duplicate key {stage_group['key']}")
        stage_group_keys.add(stage_group["key"])
        states = require_string_list(
            stage_group.get("states"),
            f"Project type {project_type_id} commandView.stageGroups.{stage_group['key']}.states",
        )
        unknown_states = sorted(set(states) - lifecycle_states)
        if unknown_states:
            fail(
                f"Project type {project_type_id} commandView stage group "
                f"{stage_group['key']} references unknown lifecycle states: {unknown_states}"
            )

    output_slots = command_view.get("outputSlots")
    if not isinstance(output_slots, list) or not output_slots:
        fail(f"Project type {project_type_id} commandView.outputSlots must be a non-empty list")
    for output_slot in output_slots:
        if not isinstance(output_slot, dict):
            fail(f"Project type {project_type_id} commandView.outputSlots entries must be objects")
        for field_name in ["key", "title", "description"]:
            if not isinstance(output_slot.get(field_name), str) or not output_slot.get(field_name):
                fail(f"Project type {project_type_id} commandView.outputSlots entries must declare {field_name}")
        stage_key = output_slot.get("stageKey")
        if not isinstance(stage_key, str) or not stage_key:
            fail(
                f"Project type {project_type_id} commandView.outputSlots."
                f"{output_slot['key']} must declare stageKey"
            )
        if stage_key not in stage_group_keys:
            fail(
                f"Project type {project_type_id} commandView.outputSlots."
                f"{output_slot['key']} references unknown stageKey {stage_key}"
            )
        if stage_key == "outcomes":
            fail(
                f"Project type {project_type_id} commandView.outputSlots."
                f"{output_slot['key']} must reference an active workflow stage, not outcomes"
            )
        artifact_outputs = output_slot.get("artifactOutputs")
        if not isinstance(artifact_outputs, list) or not artifact_outputs:
            fail(
                f"Project type {project_type_id} commandView.outputSlots.{output_slot['key']} "
                "must declare artifactOutputs"
            )
        for artifact_output in artifact_outputs:
            if not isinstance(artifact_output, dict):
                fail(
                    f"Project type {project_type_id} commandView.outputSlots."
                    f"{output_slot['key']}.artifactOutputs entries must be objects"
                )
            for field_name in ["key", "title", "producerTaskDefinitionSlug", "outputFieldKey"]:
                if not isinstance(artifact_output.get(field_name), str) or not artifact_output.get(field_name):
                    fail(
                        f"Project type {project_type_id} commandView output artifact "
                        f"for {output_slot['key']} must declare {field_name}"
                    )
            if artifact_output["outputFieldKey"] not in VC_ARTIFACT_OUTPUTS.get(
                artifact_output["producerTaskDefinitionSlug"],
                [],
            ):
                fail(
                    f"Project type {project_type_id} commandView output artifact "
                    f"{artifact_output['key']} references an undeclared producer output field"
                )


def validate_project_type_file(path: Path, expected_id: str) -> str:
    project_type = read_json(path)
    relative_path = path.relative_to(ROOT)
    if not isinstance(project_type, dict):
        fail(f"Project type must be an object: {relative_path}")
    if project_type.get("kind") != "project-type":
        fail(f"{relative_path} kind must be project-type")
    if project_type.get("apiVersion") != "alludium/v1alpha1":
        fail(f"{relative_path} apiVersion must be alludium/v1alpha1")

    project_type_id = project_type.get("key")
    if project_type_id != expected_id:
        fail(f"Project type file/id mismatch: expected {expected_id}, found {project_type_id}")
    if not isinstance(project_type.get("name"), str) or not project_type.get("name"):
        fail(f"Project type {expected_id} is missing name")
    if not isinstance(project_type.get("description"), str) or not project_type.get("description"):
        fail(f"Project type {expected_id} is missing description")

    initial_version = project_type.get("initialVersion")
    if not isinstance(initial_version, dict):
        fail(f"Project type {expected_id} initialVersion must be an object")
    if not isinstance(initial_version.get("version"), str) or not initial_version.get("version"):
        fail(f"Project type {expected_id} initialVersion.version must be declared")
    fields_schema = initial_version.get("fieldsSchema")
    if not isinstance(fields_schema, list) or not fields_schema:
        fail(f"Project type {expected_id} initialVersion.fieldsSchema must be a non-empty list")
    field_ids: list[str] = []
    field_keys: list[str] = []
    for field in fields_schema:
        field_id, field_key = validate_project_type_field(expected_id, field)
        field_ids.append(field_id)
        field_keys.append(field_key)
    if len(field_ids) != len(set(field_ids)):
        fail(f"Project type {expected_id} has duplicate field ids")
    if len(field_keys) != len(set(field_keys)):
        fail(f"Project type {expected_id} has duplicate field keys")

    if not isinstance(initial_version.get("instructionTemplate"), str) or not initial_version.get(
        "instructionTemplate"
    ):
        fail(f"Project type {expected_id} initialVersion.instructionTemplate must be declared")

    lifecycle_states = require_string_list(
        initial_version.get("lifecycleStates"),
        f"Project type {expected_id} initialVersion.lifecycleStates",
    )
    if not lifecycle_states:
        fail(f"Project type {expected_id} initialVersion.lifecycleStates must not be empty")
    if len(lifecycle_states) != len(set(lifecycle_states)):
        fail(f"Project type {expected_id} has duplicate lifecycle states")

    lifecycle_transitions = initial_version.get("lifecycleTransitions")
    if not isinstance(lifecycle_transitions, list) or not lifecycle_transitions:
        fail(f"Project type {expected_id} initialVersion.lifecycleTransitions must be a non-empty list")
    transition_pairs: list[tuple[str, str]] = []
    lifecycle_state_set = set(lifecycle_states)
    for transition in lifecycle_transitions:
        if not isinstance(transition, dict):
            fail(f"Project type {expected_id} lifecycle transitions must be objects")
        from_state = transition.get("from")
        to_state = transition.get("to")
        if not isinstance(from_state, str) or not isinstance(to_state, str):
            fail(f"Project type {expected_id} lifecycle transitions must declare from/to strings")
        if from_state not in lifecycle_state_set:
            fail(f"Project type {expected_id} transition from unknown state {from_state}")
        if to_state not in lifecycle_state_set:
            fail(f"Project type {expected_id} transition to unknown state {to_state}")
        transition_pairs.append((from_state, to_state))
    if len(transition_pairs) != len(set(transition_pairs)):
        fail(f"Project type {expected_id} has duplicate lifecycle transitions")

    if expected_id == "vc_deal_room":
        validate_vc_deal_room_command_view(expected_id, initial_version)

    return expected_id


def validate_project_types(manifest: dict[str, Any]) -> set[str]:
    surface = manifest["surfaces"].get("projectTypes")
    if not isinstance(surface, dict):
        fail("Manifest must declare surfaces.projectTypes")
    surface_path = surface.get("path")
    if not isinstance(surface_path, str) or not surface_path:
        fail("surfaces.projectTypes.path must be declared")
    manifest_project_type_ids = surface.get("ids")
    if not isinstance(manifest_project_type_ids, list) or not all(
        isinstance(item, str) for item in manifest_project_type_ids
    ):
        fail("surfaces.projectTypes.ids must be a list of strings")
    if len(manifest_project_type_ids) != len(set(manifest_project_type_ids)):
        fail("Duplicate project type IDs in alludium/manifest.yaml")
    validate_project_type_platform_ingest_contract(surface)

    project_type_root = ROOT / surface_path
    resolved_project_type_root = project_type_root.resolve()
    try:
        resolved_project_type_root.relative_to(ROOT.resolve())
    except ValueError:
        fail(f"surfaces.projectTypes.path must resolve inside the pack root: {surface_path}")
    catalog_path = project_type_root / "catalog.v1.json"
    if not catalog_path.exists():
        fail(f"Missing project type catalog: {catalog_path.relative_to(ROOT)}")
    catalog = read_json(catalog_path)
    if not isinstance(catalog, dict):
        fail(f"{catalog_path.relative_to(ROOT)} must be an object")
    if catalog.get("kind") != "project-type-catalog":
        fail(f"{catalog_path.relative_to(ROOT)} kind must be project-type-catalog")
    if catalog.get("apiVersion") != "alludium/v1alpha1":
        fail(f"{catalog_path.relative_to(ROOT)} apiVersion must be alludium/v1alpha1")

    discovered_ids: list[str] = []
    discovered_paths: set[Path] = set()
    catalog_entries = catalog.get("projectTypes")
    if not isinstance(catalog_entries, list) or not catalog_entries:
        fail(f"{catalog_path.relative_to(ROOT)} projectTypes must be a non-empty list")
    for entry in catalog_entries:
        if not isinstance(entry, dict):
            fail("Project type catalog entries must be objects")
        project_type_id = entry.get("id")
        relative_project_type_path = entry.get("path")
        if not isinstance(project_type_id, str) or not project_type_id:
            fail("Project type catalog entries must declare id")
        if not isinstance(relative_project_type_path, str) or not relative_project_type_path:
            fail(f"Project type catalog entry {project_type_id} must declare path")
        project_type_path = project_type_root / relative_project_type_path
        resolved_project_type_path = project_type_path.resolve()
        try:
            resolved_project_type_path.relative_to(resolved_project_type_root)
        except ValueError:
            fail(
                "Project type catalog path escapes project-type surface: "
                f"{relative_project_type_path}"
            )
        if not project_type_path.exists():
            fail(f"Project type catalog references missing file {relative_project_type_path}")
        discovered_paths.add(resolved_project_type_path)
        discovered_ids.append(validate_project_type_file(resolved_project_type_path, project_type_id))

    if len(discovered_ids) != len(set(discovered_ids)):
        fail("Duplicate project type IDs in catalog files")
    if set(discovered_ids) != set(manifest_project_type_ids):
        fail(
            "Manifest project type IDs do not match catalog files: "
            f"manifest_only={sorted(set(manifest_project_type_ids) - set(discovered_ids))}, "
            f"catalog_only={sorted(set(discovered_ids) - set(manifest_project_type_ids))}"
        )

    actual_json_paths = {
        path.resolve() for path in project_type_root.glob("**/*.json") if path.name != "catalog.v1.json"
    }
    extra_json_paths = actual_json_paths - discovered_paths
    if extra_json_paths:
        fail(
            "Project type files present on disk but missing from catalog: "
            f"{sorted(str(path.relative_to(project_type_root)) for path in extra_json_paths)}"
        )

    return set(discovered_ids)


def validate_task_template_file(
    path: Path,
    expected_pack: dict[str, Any],
    skill_ids: set[str],
    agent_template_ids: set[str],
    project_type_ids: set[str],
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
    slug = definition["slug"]

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
    supported_project_scopes = normalize_supported_project_scopes(
        template_id,
        definition_json,
        supported_project_types,
    )
    validate_task_template_reference_list(
        template_id,
        "supportedProjectTypes",
        supported_project_types,
        project_type_ids,
        "included project types",
    )

    fields = template.get("fields") or {}
    if not isinstance(fields, dict):
        fail(f"Task template {template_id} fields must be an object when declared")
    validate_required_artifact_fields(template_id, slug, fields)
    validate_vc_deal_room_task_template_shape(
        template_id,
        slug,
        definition_json,
        fields,
        supported_project_types,
    )

    pack_vertical_keys = expected_pack.get("verticalKeys") or []
    if expected_pack.get("availability") == "vertical" and not pack_vertical_keys:
        fail(f"Task template pack {expected_pack.get('id')} must declare verticalKeys")

    return template_id


def validate_task_definition_templates(
    manifest: dict[str, Any],
    skill_ids: set[str],
    agent_template_ids: set[str],
    project_type_ids: set[str],
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
        if (
            pack.get("id") == "vc-workflows"
            and pack.get("verticalKeys") != EXPECTED_VC_TASK_TEMPLATE_VERTICAL_KEYS
        ):
            fail(
                "Task definition template catalog pack vc-workflows verticalKeys must be "
                f"{EXPECTED_VC_TASK_TEMPLATE_VERTICAL_KEYS}"
            )
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
                    project_type_ids,
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


def load_task_template_contracts() -> dict[str, dict[str, Any]]:
    contracts: dict[str, dict[str, Any]] = {}
    for path in (ROOT / "alludium" / "task-definition-templates").glob("**/*.yaml"):
        template = read_yaml(path)
        if not isinstance(template, dict):
            continue
        template_id = template.get("id")
        definition = template.get("definition") or {}
        slug = definition.get("slug")
        definition_json = definition.get("definitionJson") or {}
        fields = template.get("fields") or {}
        if not isinstance(template_id, str) or not isinstance(slug, str):
            continue
        if not isinstance(definition_json, dict):
            continue
        supported_project_types = require_string_list(
            definition_json.get("supportedProjectTypes"),
            f"Task template {template_id} definitionJson.supportedProjectTypes",
        )
        contracts[slug] = {
            "id": template_id,
            "supportedProjectTypes": supported_project_types,
            "supportedProjectScopes": normalize_supported_project_scopes(
                template_id,
                definition_json,
                supported_project_types,
            ),
            "fields": {
                "input": field_map(template_id, "input", fields.get("input")),
                "context": field_map(template_id, "context", fields.get("context")),
                "output": field_map(template_id, "output", fields.get("output")),
            },
        }
    return contracts


def require_mapping_list(value: Any, context: str) -> list[dict[str, Any]]:
    if value is None:
        return []
    if not isinstance(value, list):
        fail(f"{context} must be a list")
    for entry in value:
        if not isinstance(entry, dict):
            fail(f"{context} entries must be objects")
    return value


def validate_project_task_mapping_contracts() -> None:
    project_type = read_json(ROOT / "alludium" / "project-types" / "vc_deal_room.json")
    initial_version = project_type.get("initialVersion") or {}
    project_type_id = project_type.get("key", "vc_deal_room")
    project_field_keys = {
        field["key"]
        for field in initial_version.get("fieldsSchema", [])
        if isinstance(field, dict) and isinstance(field.get("key"), str)
    }
    lifecycle_states = set(require_string_list(
        initial_version.get("lifecycleStates"),
        f"Project type {project_type_id} initialVersion.lifecycleStates",
    ))
    task_contracts = load_task_template_contracts()
    project_instance_supported_slugs = {
        slug
        for slug, contract in task_contracts.items()
        if "vc_deal_room" in contract.get("supportedProjectTypes", [])
        and DEFAULT_PROJECT_SCOPE in contract.get("supportedProjectScopes", [])
    }
    mappings = require_mapping_list(
        initial_version.get("projectTaskMappings"),
        f"Project type {project_type_id} initialVersion.projectTaskMappings",
    )
    if not mappings:
        fail(f"Project type {project_type_id} must declare projectTaskMappings")

    mapping_ids: list[str] = []
    mapped_outputs_by_slug: dict[str, set[str]] = {}
    for mapping in mappings:
        mapping_id = mapping.get("id")
        if not isinstance(mapping_id, str) or not mapping_id:
            fail(f"Project type {project_type_id} projectTaskMappings entries must declare id")
        mapping_ids.append(mapping_id)

        slug = mapping.get("taskDefinitionSlug")
        template_id = mapping.get("taskDefinitionTemplateId")
        if not isinstance(slug, str) or not slug:
            fail(f"Project type {project_type_id} mapping {mapping_id} must declare taskDefinitionSlug")
        if not isinstance(template_id, str) or not template_id:
            fail(f"Project type {project_type_id} mapping {mapping_id} must declare taskDefinitionTemplateId")
        task_contract = task_contracts.get(slug)
        if task_contract is None:
            fail(f"Project type {project_type_id} mapping {mapping_id} references unknown task {slug}")
        if task_contract["id"] != template_id:
            fail(
                f"Project type {project_type_id} mapping {mapping_id} references template id "
                f"{template_id}, but {slug} has id {task_contract['id']}"
            )

        project_scope = mapping.get("projectScope", DEFAULT_PROJECT_SCOPE)
        if not isinstance(project_scope, str) or not project_scope:
            fail(f"Project type {project_type_id} mapping {mapping_id} projectScope must be a string")
        if project_scope not in PROJECT_SCOPES:
            fail(
                f"Project type {project_type_id} mapping {mapping_id} projectScope must be one of "
                f"{sorted(PROJECT_SCOPES)}"
            )
        if project_scope not in task_contract["supportedProjectScopes"]:
            fail(
                f"Project type {project_type_id} mapping {mapping_id} uses projectScope "
                f"{project_scope}, but task {slug} supports "
                f"{task_contract['supportedProjectScopes']}"
            )

        lifecycle_stage = mapping.get("lifecycleStage")
        if lifecycle_stage not in lifecycle_states:
            fail(
                f"Project type {project_type_id} mapping {mapping_id} references unknown "
                f"lifecycleStage {lifecycle_stage}"
            )
        if lifecycle_stage in {"invested", "passed", "archived"}:
            fail(f"Project type {project_type_id} mapping {mapping_id} must not target terminal outcome stage")

        if require_mapping_list(
            mapping.get("contextMappings"),
            f"Project type {project_type_id} mapping {mapping_id}.contextMappings",
        ):
            fail(f"Project type {project_type_id} mapping {mapping_id} must not declare contextMappings")

        for section_name in ["inputMappings", "outputMappings"]:
            for entry in require_mapping_list(
                mapping.get(section_name),
                f"Project type {project_type_id} mapping {mapping_id}.{section_name}",
            ):
                task_field = entry.get("taskField")
                if not isinstance(task_field, str) or not task_field:
                    fail(f"Project type {project_type_id} mapping {mapping_id}.{section_name} entry must declare taskField")
                field_section = "input" if section_name == "inputMappings" else "output"
                if task_field not in task_contract["fields"][field_section]:
                    fail(
                        f"Project type {project_type_id} mapping {mapping_id}.{section_name}.{task_field} "
                        f"references an unknown task {field_section} field"
                    )
                if section_name == "inputMappings":
                    source = entry.get("source")
                    if source not in PROJECT_TASK_MAPPING_SOURCES:
                        fail(
                            f"Project type {project_type_id} mapping {mapping_id}.inputMappings.{task_field} "
                            f"source must be one of {sorted(PROJECT_TASK_MAPPING_SOURCES)}"
                        )
                    source_path = entry.get("sourcePath")
                    if source == "project.field" and source_path not in project_field_keys:
                        fail(
                            f"Project type {project_type_id} mapping {mapping_id}.inputMappings.{task_field} "
                            f"sourcePath references unknown project field {source_path}"
                        )
                    if source == "constant" and "constantValue" not in entry:
                        fail(
                            f"Project type {project_type_id} mapping {mapping_id}.inputMappings.{task_field} "
                            "must declare constantValue for source constant"
                        )
                    if "requiredForActivation" in entry and not isinstance(entry["requiredForActivation"], bool):
                        fail(
                            f"Project type {project_type_id} mapping {mapping_id}.inputMappings.{task_field} "
                            "requiredForActivation must be a boolean"
                        )
                    continue
                target = entry.get("target")
                if section_name == "outputMappings":
                    if target not in PROJECT_TASK_MAPPING_TARGETS:
                        fail(
                            f"Project type {project_type_id} mapping {mapping_id}.outputMappings.{task_field} "
                            f"target must be one of {sorted(PROJECT_TASK_MAPPING_TARGETS)}"
                        )
                    target_path = entry.get("targetPath")
                    if target == "project.field" and target_path not in project_field_keys:
                        fail(
                            f"Project type {project_type_id} mapping {mapping_id}.outputMappings.{task_field} "
                            f"targetPath references unknown project field {target_path}"
                        )
                    if "requiredForCompletion" in entry and not isinstance(entry["requiredForCompletion"], bool):
                        fail(
                            f"Project type {project_type_id} mapping {mapping_id}.outputMappings.{task_field} "
                            "requiredForCompletion must be a boolean"
                        )
                    if project_scope == DEFAULT_PROJECT_SCOPE:
                        mapped_outputs_by_slug.setdefault(slug, set()).add(task_field)

        activation_policy = mapping.get("activationPolicy")
        if not isinstance(activation_policy, dict):
            fail(f"Project type {project_type_id} mapping {mapping_id} must declare activationPolicy")
        if activation_policy.get("mode") not in PROJECT_TASK_ACTIVATION_MODES:
            fail(
                f"Project type {project_type_id} mapping {mapping_id} activationPolicy.mode "
                f"must be one of {sorted(PROJECT_TASK_ACTIVATION_MODES)}"
            )
        if activation_policy.get("mode") != "manual_review":
            fail(f"Project type {project_type_id} mapping {mapping_id} must use manual_review activation")
        if activation_policy.get("autoStartWhenRequiredInputsAvailable") is not False:
            fail(
                f"Project type {project_type_id} mapping {mapping_id} must set "
                "autoStartWhenRequiredInputsAvailable: false"
            )
        if activation_policy.get("requiresHumanApproval") is not True:
            fail(f"Project type {project_type_id} mapping {mapping_id} must set requiresHumanApproval: true")
        if activation_policy.get("createTaskWhenLifecycleStageEntered") is not False:
            fail(
                f"Project type {project_type_id} mapping {mapping_id} must set "
                "createTaskWhenLifecycleStageEntered: false"
            )

    if len(mapping_ids) != len(set(mapping_ids)):
        fail(f"Project type {project_type_id} has duplicate projectTaskMappings ids")

    for slug, artifact_fields in VC_ARTIFACT_OUTPUTS.items():
        if slug not in project_instance_supported_slugs:
            continue
        missing_project_fields = sorted(set(artifact_fields) - project_field_keys)
        if missing_project_fields:
            fail(
                f"Project type {project_type_id} is missing artifact index fields for {slug}: "
                f"{missing_project_fields}"
            )
        missing_mappings = sorted(set(artifact_fields) - mapped_outputs_by_slug.get(slug, set()))
        if missing_mappings:
            fail(
                f"Project type {project_type_id} projectTaskMappings for {slug} are missing "
                f"artifact output mappings: {missing_mappings}"
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

    if recommendations.get("status") != "platform-mapping":
        fail("alludiumMcpRecommendations must declare status: platform-mapping")

    recommendation_entries = recommendations.get("recommendations")
    if not isinstance(recommendation_entries, list) or not recommendation_entries:
        fail("alludiumMcpRecommendations must declare a non-empty recommendations list")

    recommendation_ids: set[str] = set()
    for item in recommendation_entries:
        if not isinstance(item, dict):
            fail("All MCP recommendation entries must be objects")
        if "id" in item or "title" in item or "externalMcpId" in item or "metadata" in item:
            fail(
                "MCP recommendations must use externalId/name/use plus optional "
                "applicationRecommendation metadata"
            )
        external_id = item.get("externalId")
        if not isinstance(external_id, str) or not external_id:
            fail("All MCP recommendation entries must declare externalId")
        if external_id in recommendation_ids:
            fail(f"Duplicate MCP recommendation externalId: {external_id}")
        recommendation_ids.add(external_id)
        if external_id not in mcp_servers:
            continue
        for field_name in [
            "name",
            "category",
            "use",
            "pluginCredentialBoundary",
            "alludiumPlatformMapping",
        ]:
            if not isinstance(item.get(field_name), str) or not item.get(field_name):
                fail(f"MCP recommendation {external_id} must declare {field_name}")
        if not isinstance(item.get("platformDefaultAvailable"), bool):
            fail(f"MCP recommendation {external_id} must declare platformDefaultAvailable")

    missing_from_plugin = set(mcp_servers) - recommendation_ids
    if missing_from_plugin:
        fail(
            ".mcp.json servers missing from MCP recommendations: "
            f"{sorted(missing_from_plugin)}"
        )

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
    project_type_ids = validate_project_types(manifest)
    validate_task_definition_templates(manifest, skill_ids, agent_template_ids, project_type_ids)
    validate_project_task_mapping_contracts()
    recommendations_path = manifest["surfaces"]["alludiumMcpRecommendations"]["path"]
    if not (ROOT / recommendations_path).exists():
        fail(f"Missing Alludium MCP recommendations file: {recommendations_path}")
    recommendations = read_yaml(ROOT / recommendations_path)
    if not isinstance(recommendations, dict):
        fail(f"{recommendations_path} must be an object")
    validate_mcp_definitions(manifest, recommendations)
    validate_workspace_variables(manifest)
    validate_application_recommendations(manifest, recommendations)
    validate_no_obvious_secrets()
    validate_no_public_readiness_leakage()

    print(
        "Validated vc pack: "
        f"{len(skill_ids)} skills, "
        f"{len(manifest['surfaces']['alludiumAgentTemplates']['ids'])} agent templates, "
        f"{len(manifest['surfaces']['taskDefinitionTemplates']['ids'])} task definition templates, "
        f"{len(project_type_ids)} project types"
    )


if __name__ == "__main__":
    main()
