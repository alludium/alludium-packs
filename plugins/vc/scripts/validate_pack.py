#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from functools import lru_cache
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
APPLICATION_ONLY_AVAILABLE_EXTERNAL_IDS = {"google_drive", "notion", "slack_v2"}
INTEGRATION_ENTITY_ROLES = {
    "document",
    "message_or_conversation",
    "organization",
    "person",
    "project",
    "repository",
    "task_or_issue",
    "opportunity",
    "account",
    "custom",
}
INTEGRATION_TASK_ACTION_KINDS = {"setup"}
# Integration recommendations expose one setup entry point. The setup task
# owns the detailed discovery/read/write subtask plan so application cards do
# not become miniature workflow declarations.
EXPECTED_RECOMMENDATION_ACTIONS = {
    "affinity-mcp-server": {
        "setup": "vc.affinity_setup",
    },
    "slack_v2": {
        "setup": "vc.slack_setup",
    },
    "google_drive": {
        "setup": "vc.google_drive_setup",
    },
    "notion": {
        "setup": "vc.notion_setup",
    },
    "harmonic-mcp-oauth": {
        "setup": "vc.harmonic_setup",
    },
    "apify-actors-mcp": {
        "setup": "vc.apify_setup",
    },
    "firecrawl-mcp-hosted": {
        "setup": "vc.companies_house_setup",
    },
}
EXPECTED_SETUP_CHILD_TASKS = {
    "vc.affinity_setup": {
        "applicationExternalId": "affinity-mcp-server",
        "childTaskDefinitionTemplateIds": {
            "discovery": "vc.affinity_discovery",
            "syncRead": "vc.affinity_sync_read",
            "syncWrite": "vc.affinity_sync_write",
        },
    },
    "vc.slack_setup": {
        "applicationExternalId": "slack_v2",
        "childTaskDefinitionTemplateIds": {
            "discovery": "vc.slack_discovery",
            "syncRead": "vc.slack_sync_read",
            "syncWrite": "vc.slack_sync_write",
        },
    },
    "vc.google_drive_setup": {
        "applicationExternalId": "google_drive",
        "childTaskDefinitionTemplateIds": {
            "discovery": "vc.google_drive_discovery",
            "syncRead": "vc.google_drive_sync_read",
            "syncWrite": "vc.google_drive_sync_write",
        },
    },
    "vc.notion_setup": {
        "applicationExternalId": "notion",
        "childTaskDefinitionTemplateIds": {
            "discovery": "vc.notion_discovery",
            "syncRead": "vc.notion_sync_read",
            "syncWrite": "vc.notion_sync_write",
        },
    },
    "vc.harmonic_setup": {
        "applicationExternalId": "harmonic-mcp-oauth",
        "childTaskDefinitionTemplateIds": {
            "discovery": "vc.harmonic_discovery",
            "syncRead": "vc.harmonic_sync_read",
        },
    },
    "vc.apify_setup": {
        "applicationExternalId": "apify-actors-mcp",
        "childTaskDefinitionTemplateIds": {
            "discovery": "vc.apify_discovery",
            "syncRead": "vc.apify_sync_read",
        },
    },
    "vc.companies_house_setup": {
        "applicationExternalId": "firecrawl-mcp-hosted",
        "childTaskDefinitionTemplateIds": {
            "discovery": "vc.companies_house_discovery",
            "syncRead": "vc.companies_house_sync_read",
        },
    },
}
TASK_TEMPLATE_REQUIRED_SKILL_REFERENCE_FIELDS = ["requiredSkills", "plannedRequiredSkills"]
TASK_TEMPLATE_AGENT_TEMPLATE_REFERENCE_FIELDS = [
    "recommendedAgentTemplate",
    "plannedRecommendedAgentTemplate",
    "preferredAgentType",
]
TASK_TEMPLATE_PLATFORM_CAPABILITY = "external-task-definition-template-ingest"
PROJECT_TYPE_PLATFORM_CAPABILITY = "external-project-type-ingest"
DOCUMENT_SURFACE_STATUS = "pack-native-document-sources"
DOCUMENT_CATALOG_PATH = "alludium/documents/catalog.v1.json"
DOCUMENT_TYPES = {"checklist", "methodology", "policy", "sop", "style_guide", "template"}
DOCUMENT_STATUSES = {"source"}
DOCUMENT_AUTHORING_LEAK_PATTERNS = [
    "delete this section",
    "remove this section",
    "do not include this",
    "the agent should",
    "authoring note",
    "prompt trace",
]
DOCUMENT_REF_USAGE_DOCUMENT_TYPES = {
    "checklist": {"checklist"},
    "methodology": {"methodology"},
    "operating_guidance": {"methodology", "policy", "sop", "template"},
    "output_template": {"checklist", "template"},
    "policy": {"policy"},
    "setup_checklist": {"checklist"},
    "style_guide": {"style_guide"},
}
TEMPLATE_USE_GUIDANCE_DOCUMENT_ID = "vc.document.template_use_guidance"
TEMPLATE_USE_GUIDANCE_REQUIRED_USAGES = {"checklist", "output_template"}
DOCUMENT_REF_USAGES = {
    "checklist",
    "methodology",
    "operating_guidance",
    "output_template",
    "policy",
    "setup_checklist",
    "style_guide",
}
DOCUMENT_REF_STRUCTURED_ARTIFACT_OUTPUT_FIELDS = {
    "child_task_plan_artifact_id",
    "run_receipt_artifact_id",
    "source_state_artifact_id",
    "sync_plan_artifact_id",
}
EXPECTED_VC_TASK_TEMPLATE_VERTICAL_KEYS = ["venture_capital", "vc"]
PROJECT_TYPE_FIELD_KINDS = {"date", "enum", "member", "number", "text"}
PROJECT_TASK_MAPPING_SOURCES = {"constant", "project.field", "project.id", "project.state"}
PROJECT_TASK_MAPPING_TARGETS = {"project.field", "project.state"}
PROJECT_TASK_ACTIVATION_MODES = {"manual", "manual_review", "auto_start"}
PROJECT_SCOPES = {"project_instance", "project_management"}
DEFAULT_PROJECT_SCOPE = "project_instance"
PROJECT_MANAGEMENT_SCOPE = "project_management"
TASK_SCHEDULING_SETUP_STEPS = {"schedules"}
TASK_SCHEDULING_TYPES = {"cron", "one_off"}
TASK_SCHEDULING_DEFAULT_REFS = {"scheduleDefaults"}
PROJECT_SETUP_STEP_TYPES = {"source_choice", "source_setup", "variables", "schedules", "invite"}
PROJECT_SETUP_POST_APPROVAL_ACTIONS = {
    "applyVariables",
    "importProjects",
    "inviteCollaborators",
    "enableSchedules",
}
PROJECT_CREATION_KEYS = {
    "launcherLabel",
    "starterId",
    "aliases",
    "requiredFieldKeys",
    "recommendedFieldKeys",
    "advancedFieldKeys",
    "sourceReference",
    "defaultState",
    "guidedTask",
    "postCreate",
}
PROJECT_CREATION_FIELD_LISTS = [
    "requiredFieldKeys",
    "recommendedFieldKeys",
    "advancedFieldKeys",
]
PROJECT_CREATION_STARTER_ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PROJECT_CREATION_SOURCE_REFERENCE_INPUT_KINDS = {"connected_record_reference"}
PROJECT_CREATION_SOURCE_REFERENCE_TARGET_KEYS = {
    "system",
    "objectId",
    "objectUrl",
    "recordUrlTemplate",
}
PROJECT_CREATION_COMPLETION_OUTPUT_KEY = "projectCreation"
PROJECT_CREATION_VARIABLE_FIELD_ALIASES = {
    "vc.fundStage": {"stage_focus"},
    "vc.fundSectors": {"sector_focus"},
    "vc.fundGeography": {"geography_focus"},
    "vc.fundThesis": {"investment_thesis"},
    "vc.firmName": {"firm_name"},
    "vc.fundName": {"fund_name"},
    "vc.originationEnabledSources": {"enabled_sources"},
    "vc.originationRunCadence": {"run_cadence"},
    "vc.originationDigestDestination": {"digest_channel"},
    "vc.originationSourceCostBudget": {"source_cost_budget"},
    "vc.originationPromotionThreshold": {"promotion_threshold"},
    "vc.originationManualReviewThreshold": {"manual_review_threshold"},
    "vc.originationCrmPipelineUrl": {"crm_pipeline_url"},
    "vc.originationDocumentWorkspaceUrl": {"document_workspace_url"},
}
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
    "run-investment-screen": ["investment_screen_scorecard_artifact_id"],
    "generate-diligence-questions": ["diligence_question_bank_artifact_id"],
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
    "affinity-deal-room-import": ["affinity_import_receipt_artifact_id"],
}
VC_ARTIFACT_INPUTS = {
    "screen-inbound-opportunity": ["pitch_deck_artifact_id"],
    "prepare-initial-call": ["pitch_deck_artifact_id"],
    "summarize-initial-call": ["meeting_record_artifact_ids"],
    "run-follow-up-evaluation": [
        "first_look_scorecard_artifact_id",
        "customer_insights_artifact_id",
    ],
    "run-investment-screen": ["pitch_deck_artifact_id"],
    "run-financial-dd": ["financial_source_artifact_ids"],
    "run-technical-dd": ["technical_source_artifact_ids"],
    "prepare-team-review-pack": [
        "commercial_dd_artifact_id",
        "financial_dd_artifact_id",
        "founder_evaluation_artifact_id",
        "technical_dd_artifact_id",
        "diligence_question_bank_artifact_id",
    ],
    "prepare-partner-review-pack": [
        "commercial_dd_artifact_id",
        "financial_dd_artifact_id",
        "founder_evaluation_artifact_id",
        "technical_dd_artifact_id",
        "diligence_question_bank_artifact_id",
        "team_review_pack_artifact_id",
    ],
    "create-ic-memo": [
        "commercial_dd_artifact_id",
        "financial_dd_artifact_id",
        "founder_evaluation_artifact_id",
        "technical_dd_artifact_id",
        "diligence_question_bank_artifact_id",
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


def load_vc_deal_room_lifecycle_states() -> set[str]:
    project_type = read_json(ROOT / "alludium" / "project-types" / "vc_deal_room.json")
    initial_version = project_type.get("initialVersion") or {}
    return set(require_string_list(
        initial_version.get("lifecycleStates"),
        "Project type vc_deal_room initialVersion.lifecycleStates",
    ))


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


def plugin_manifest_paths() -> list[Path]:
    paths = sorted(ROOT.glob(".*-plugin/plugin.json"))
    if not paths:
        fail("No plugin manifests found")
    return paths


def validate_plugin_manifest(path: Path) -> None:
    manifest = read_json(path)
    if manifest.get("name") != "vc":
        fail(f"{path.relative_to(ROOT)} name must be vc")
    if manifest.get("skills") != "./skills/":
        fail(f"{path.relative_to(ROOT)} skills path must be ./skills/")
    if manifest.get("mcpServers") != "./.mcp.json":
        fail(f"{path.relative_to(ROOT)} mcpServers path must be ./.mcp.json")


def validate_plugin_manifest_versions(pack_version: str, plugin_paths: list[Path]) -> None:
    for path in plugin_paths:
        manifest = read_json(path)
        if manifest.get("version") != pack_version:
            fail(
                f"{path.relative_to(ROOT)} version must match alludium/manifest.yaml "
                f"pack.version {pack_version}"
            )


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

    vc_deal_room_lifecycle_states = load_vc_deal_room_lifecycle_states()
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
        metadata = template.get("metadata") or {}
        if not isinstance(metadata, dict):
            fail(f"Agent template {template_id} metadata must be an object when declared")
        primary_deal_room_state = metadata.get("primaryDealRoomState")
        if (
            primary_deal_room_state is not None
            and primary_deal_room_state not in vc_deal_room_lifecycle_states
        ):
            fail(
                f"Agent template {template_id} primaryDealRoomState must be one of "
                f"{sorted(vc_deal_room_lifecycle_states)}"
            )

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


def validate_supported_project_types(
    value: Any,
    context: str,
    allowed_project_type_ids: set[str],
) -> list[str]:
    supported_project_types = require_string_list(value, context)
    if not supported_project_types:
        fail(f"{context} must declare at least one project type")
    if len(supported_project_types) != len(set(supported_project_types)):
        fail(f"{context} must not contain duplicate project types")
    unknown_project_types = sorted(set(supported_project_types) - allowed_project_type_ids)
    if unknown_project_types:
        fail(f"{context} references unknown project types: {unknown_project_types}")
    return supported_project_types


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


def validate_workspace_variables(manifest: dict[str, Any], project_type_ids: set[str]) -> set[str]:
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
        supported_project_types = variable.get("supportedProjectTypes")
        if not isinstance(supported_project_types, list) or not supported_project_types:
            fail(f"Workspace variable {variable_key} must declare supportedProjectTypes")
        invalid_project_types = [
            project_type
            for project_type in supported_project_types
            if not isinstance(project_type, str) or project_type not in project_type_ids
        ]
        if invalid_project_types:
            fail(
                f"Workspace variable {variable_key} has invalid supportedProjectTypes: "
                f"{sorted(invalid_project_types)}"
            )
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
    project_type_ids: set[str],
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
        validate_supported_project_types(
            recommendation.get("supportedProjectTypes"),
            f"Application recommendation {recommendation_id}.supportedProjectTypes",
            project_type_ids,
        )
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

        if (
            status == "available"
            and recommendation_id not in mcp_servers
            and recommendation_id not in APPLICATION_ONLY_AVAILABLE_EXTERNAL_IDS
        ):
            fail(
                f"Application recommendation {recommendation_id} is available but missing "
                "from .mcp.json"
            )


def require_mapping(value: Any, context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        fail(f"{context} must be an object")
    return value


def require_enum(value: Any, allowed: set[str], context: str) -> str:
    if value not in allowed:
        fail(f"{context} must be one of {sorted(allowed)}")
    return value


def load_task_template_supported_project_types_by_id() -> dict[str, list[str]]:
    task_project_types: dict[str, list[str]] = {}
    for path in (ROOT / "alludium" / "task-definition-templates").glob("**/*.yaml"):
        template = read_yaml(path)
        if not isinstance(template, dict):
            continue
        template_id = template.get("id")
        definition = template.get("definition") or {}
        definition_json = definition.get("definitionJson") or {}
        if not isinstance(template_id, str) or not isinstance(definition_json, dict):
            continue
        task_project_types[template_id] = require_string_list(
            definition_json.get("supportedProjectTypes"),
            f"Task template {template_id} definitionJson.supportedProjectTypes",
        )
    return task_project_types


def validate_recommendation_action(
    recommendation_id: str,
    recommendation_project_types: list[str],
    action: Any,
    task_template_ids: set[str],
    task_template_project_types: dict[str, list[str]],
    skill_ids: set[str],
) -> None:
    action_obj = require_mapping(action, f"Application recommendation {recommendation_id} action")
    action_kind = require_enum(
        action_obj.get("kind"),
        INTEGRATION_TASK_ACTION_KINDS,
        f"Application recommendation {recommendation_id} action.kind",
    )
    if not isinstance(action_obj.get("label"), str) or not action_obj["label"]:
        fail(f"Application recommendation {recommendation_id} action {action_kind} must declare label")

    task_template_id = action_obj.get("taskDefinitionTemplateId")
    if not isinstance(task_template_id, str) or not task_template_id:
        fail(
            f"Application recommendation {recommendation_id} action {action_kind} "
            "must declare taskDefinitionTemplateId"
        )
    if task_template_id not in task_template_ids:
        fail(
            f"Application recommendation {recommendation_id} action {action_kind} references "
            f"missing task template {task_template_id}"
        )

    action_project_types = validate_supported_project_types(
        action_obj.get("supportedProjectTypes"),
        f"Application recommendation {recommendation_id} action {action_kind}.supportedProjectTypes",
        set(recommendation_project_types),
    )
    supported_by_task = task_template_project_types.get(task_template_id)
    if supported_by_task is None:
        fail(
            f"Application recommendation {recommendation_id} action {action_kind} "
            f"references task template {task_template_id} without a project-type contract"
        )
    unsupported_by_task = sorted(set(action_project_types) - set(supported_by_task))
    if unsupported_by_task:
        fail(
            f"Application recommendation {recommendation_id} action {action_kind} "
            f"project types {unsupported_by_task} are not supported by task template "
            f"{task_template_id}"
        )

    skill_id = action_obj.get("skillId")
    if skill_id is not None and (not isinstance(skill_id, str) or not skill_id):
        fail(
            f"Application recommendation {recommendation_id} action {action_kind} "
            "skillId must be a non-empty string when declared"
        )
    if isinstance(skill_id, str) and skill_id not in skill_ids:
        fail(
            f"Application recommendation {recommendation_id} action {action_kind} references "
            f"missing skill {skill_id}"
        )

    expected_actions = EXPECTED_RECOMMENDATION_ACTIONS.get(recommendation_id)
    if expected_actions is None:
        return
    expected = expected_actions.get(action_kind)
    if expected is None:
        return
    expected_template_id = expected
    if task_template_id != expected_template_id:
        fail(
            f"Application recommendation {recommendation_id} action {action_kind} "
            f"must reference task template {expected_template_id}"
        )


def validate_recommendation_management_actions(
    recommendations: dict[str, Any],
    task_template_ids: set[str],
    skill_ids: set[str],
) -> None:
    if "integrationTaskAssociations" in recommendations:
        fail("Use recommendation-level entityRoles/actions; integrationTaskAssociations is not supported")

    found_expected_ids: set[str] = set()
    task_template_project_types = load_task_template_supported_project_types_by_id()
    for recommendation in recommendations.get("recommendations") or []:
        if not isinstance(recommendation, dict):
            continue
        recommendation_id = recommendation.get("externalId")
        if not isinstance(recommendation_id, str) or not recommendation_id:
            continue
        recommendation_project_types = require_string_list(
            recommendation.get("supportedProjectTypes"),
            f"Application recommendation {recommendation_id}.supportedProjectTypes",
        )

        entity_roles = require_string_list(
            recommendation.get("entityRoles"),
            f"Application recommendation {recommendation_id}.entityRoles",
        )
        for entity_role in entity_roles:
            require_enum(
                entity_role,
                INTEGRATION_ENTITY_ROLES,
                f"Application recommendation {recommendation_id}.entityRoles",
            )

        actions = recommendation.get("actions")
        if actions is None:
            continue
        if not isinstance(actions, list) or not actions:
            fail(f"Application recommendation {recommendation_id}.actions must be a non-empty list")
        if not entity_roles:
            fail(f"Application recommendation {recommendation_id} with actions must declare entityRoles")

        action_kinds: set[str] = set()
        for action in actions:
            validate_recommendation_action(
                recommendation_id,
                recommendation_project_types,
                action,
                task_template_ids,
                task_template_project_types,
                skill_ids,
            )
            action_kinds.add(action["kind"])

        expected_actions = EXPECTED_RECOMMENDATION_ACTIONS.get(recommendation_id)
        if expected_actions is None:
            continue
        found_expected_ids.add(recommendation_id)
        missing_action_kinds = sorted(set(expected_actions) - action_kinds)
        if missing_action_kinds:
            fail(
                f"Application recommendation {recommendation_id} is missing management actions: "
                f"{missing_action_kinds}"
            )

    missing_recommendations = sorted(set(EXPECTED_RECOMMENDATION_ACTIONS) - found_expected_ids)
    if missing_recommendations:
        fail(f"Missing recommendation-level management actions for {missing_recommendations}")


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


def validate_project_scope_instruction_language(
    template_id: str,
    slug: str,
    definition_json: dict[str, Any],
    supported_project_scopes: list[str],
) -> None:
    if DEFAULT_PROJECT_SCOPE in supported_project_scopes:
        return
    if PROJECT_MANAGEMENT_SCOPE not in supported_project_scopes:
        return

    instructions = definition_json.get("instructions") or {}
    if not isinstance(instructions, dict):
        return
    execution_instructions = instructions.get("executionInstructions")
    if not isinstance(execution_instructions, str):
        return
    if "project file artifact" in execution_instructions.lower():
        fail(
            f"Task template {template_id} ({slug}) is project_management scoped only and "
            "must not describe output artifacts as project file artifacts"
        )


@lru_cache(maxsize=1)
def load_project_setup_schedule_group_slugs_by_project_type() -> dict[str, set[str]]:
    grouped_slugs: dict[str, set[str]] = {}
    project_type_root = ROOT / "alludium" / "project-types"

    for path in project_type_root.glob("*.json"):
        if path.name == "catalog.v1.json":
            continue
        project_type = read_json(path)
        if not isinstance(project_type, dict):
            continue
        project_type_id = project_type.get("key")
        if not isinstance(project_type_id, str) or not project_type_id:
            continue
        project_setup = project_type.get("projectSetup")
        if not isinstance(project_setup, dict):
            grouped_slugs[project_type_id] = set()
            continue
        schedule_groups = project_setup.get("scheduleGroups")
        if not isinstance(schedule_groups, list):
            grouped_slugs[project_type_id] = set()
            continue
        slugs: set[str] = set()
        for group in schedule_groups:
            if isinstance(group, dict):
                slugs.update(require_string_list(
                    group.get("taskDefinitionSlugs"),
                    f"Project type {project_type_id} projectSetup.scheduleGroups.taskDefinitionSlugs",
                ))
        grouped_slugs[project_type_id] = slugs

    return grouped_slugs


def validate_task_scheduling_contract(
    template_id: str,
    slug: str,
    definition_json: dict[str, Any],
    supported_project_types: list[str],
) -> None:
    schedule_defaults = definition_json.get("scheduleDefaults")
    scheduling = definition_json.get("scheduling")

    if schedule_defaults is None and scheduling is None:
        return
    if not isinstance(schedule_defaults, dict):
        fail(f"Task template {template_id} definitionJson.scheduleDefaults must be an object")
    if not isinstance(scheduling, dict):
        fail(f"Task template {template_id} definitionJson.scheduling must be declared")

    if scheduling.get("schedulable") is not True:
        fail(f"Task template {template_id} definitionJson.scheduling.schedulable must be true")
    if scheduling.get("showInProjectSetup") is not True:
        fail(
            f"Task template {template_id} definitionJson.scheduling.showInProjectSetup must be true"
        )
    if scheduling.get("setupStep") not in TASK_SCHEDULING_SETUP_STEPS:
        fail(
            f"Task template {template_id} definitionJson.scheduling.setupStep must be one of "
            f"{sorted(TASK_SCHEDULING_SETUP_STEPS)}"
        )
    if scheduling.get("scheduleType") not in TASK_SCHEDULING_TYPES:
        fail(
            f"Task template {template_id} definitionJson.scheduling.scheduleType must be one of "
            f"{sorted(TASK_SCHEDULING_TYPES)}"
        )
    if scheduling.get("defaultScheduleRef") not in TASK_SCHEDULING_DEFAULT_REFS:
        fail(
            f"Task template {template_id} definitionJson.scheduling.defaultScheduleRef must "
            "point at scheduleDefaults"
        )

    for boolean_field in [
        "requiresHumanApprovalToEnable",
        "canCreateTestRun",
        "testRunCreatesVisibleTask",
        "dryRunFirst",
    ]:
        if not isinstance(scheduling.get(boolean_field), bool):
            fail(
                f"Task template {template_id} definitionJson.scheduling.{boolean_field} "
                "must be a boolean"
            )

    if scheduling.get("requiresHumanApprovalToEnable") is not True:
        fail(
            f"Task template {template_id} definitionJson.scheduling must require human approval"
        )
    if scheduling.get("testRunCreatesVisibleTask") is not True:
        fail(
            f"Task template {template_id} definitionJson.scheduling test runs must create "
            "visible tasks"
        )

    safety = scheduling.get("safety")
    if not isinstance(safety, dict):
        fail(f"Task template {template_id} definitionJson.scheduling.safety must be an object")
    if safety.get("externalWritesRequireApproval") is not True:
        fail(
            f"Task template {template_id} definitionJson.scheduling.safety must require "
            "approval for external writes"
        )

    schedule_groups_by_project_type = load_project_setup_schedule_group_slugs_by_project_type()
    missing_schedule_groups = sorted(
        project_type
        for project_type in supported_project_types
        if slug not in schedule_groups_by_project_type.get(project_type, set())
    )
    if missing_schedule_groups:
        fail(
            f"Task template {template_id} ({slug}) with setup scheduling must be declared in "
            f"projectSetup.scheduleGroups for {missing_schedule_groups}"
        )


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
    supported_project_scopes: list[str],
) -> None:
    if "vc_deal_room" not in supported_project_types:
        return

    if DEFAULT_PROJECT_SCOPE in supported_project_scopes:
        stage = definition_json.get("stage")
        if stage not in VC_DEAL_ROOM_LIFECYCLE_STAGES:
            fail(
                f"Task template {template_id} ({slug}) definitionJson.stage must be one of "
                f"{sorted(VC_DEAL_ROOM_LIFECYCLE_STAGES)} for vc_deal_room project_instance tasks"
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


def validate_task_template_document_refs(
    template_id: str,
    slug: str,
    definition_json: dict[str, Any],
    fields: dict[str, Any],
    document_ids: set[str],
    document_types_by_id: dict[str, str],
) -> None:
    output_fields = field_map(template_id, "output", fields.get("output"))
    document_refs = definition_json.get("documentRefs")
    if document_refs is None:
        document_refs = []
    if not isinstance(document_refs, list):
        fail(f"Task template {template_id} definitionJson.documentRefs must be a list")
    if document_refs:
        instructions = definition_json.get("instructions")
        if not isinstance(instructions, dict):
            fail(f"Task template {template_id} definitionJson.instructions must be an object")
        execution_instructions = instructions.get("executionInstructions")
        if not isinstance(execution_instructions, str) or "definitionJson.documentRefs" not in execution_instructions:
            fail(
                f"Task template {template_id} declares documentRefs but executionInstructions "
                "must tell the agent to use definitionJson.documentRefs"
            )

    ref_keys: set[tuple[str, str, str | None]] = set()
    output_ref_pairs: set[tuple[str, str]] = set()
    has_template_guidance = False
    requires_template_guidance = False
    for ref in document_refs:
        if not isinstance(ref, dict):
            fail(f"Task template {template_id} definitionJson.documentRefs entries must be objects")
        document_id = ref.get("documentId")
        if not isinstance(document_id, str) or not document_id:
            fail(f"Task template {template_id} documentRefs entries must declare documentId")
        if document_id not in document_ids:
            fail(f"Task template {template_id} references unknown document {document_id}")
        usage = ref.get("usage")
        if usage not in DOCUMENT_REF_USAGES:
            fail(
                f"Task template {template_id} documentRef {document_id} usage must be one of "
                f"{sorted(DOCUMENT_REF_USAGES)}"
            )
        document_type = document_types_by_id.get(document_id)
        allowed_document_types = DOCUMENT_REF_USAGE_DOCUMENT_TYPES.get(usage, set())
        if document_type not in allowed_document_types:
            fail(
                f"Task template {template_id} documentRef {document_id} usage {usage} "
                f"does not match documentType {document_type}; expected one of "
                f"{sorted(allowed_document_types)}"
            )
        if usage in TEMPLATE_USE_GUIDANCE_REQUIRED_USAGES:
            requires_template_guidance = True
        if document_id == TEMPLATE_USE_GUIDANCE_DOCUMENT_ID and usage == "operating_guidance":
            has_template_guidance = True
        output_field_key = ref.get("outputFieldKey")
        if output_field_key is not None and not isinstance(output_field_key, str):
            fail(f"Task template {template_id} documentRef {document_id} outputFieldKey must be a string")
        if output_field_key in DOCUMENT_REF_STRUCTURED_ARTIFACT_OUTPUT_FIELDS:
            fail(
                f"Task template {template_id} documentRef {document_id} references structured "
                f"artifact output field {output_field_key}; state, receipts, and task plans "
                "must not be modeled as document templates"
            )
        ref_key = (document_id, usage, output_field_key)
        if ref_key in ref_keys:
            fail(f"Task template {template_id} has duplicate documentRef {ref_key}")
        ref_keys.add(ref_key)
        if output_field_key is None:
            continue
        output_field = output_fields.get(output_field_key)
        if output_field is None:
            fail(
                f"Task template {template_id} documentRef {document_id} references missing "
                f"output field {output_field_key}"
            )
        if output_field.get("fieldType") != "file":
            fail(
                f"Task template {template_id} documentRef {document_id} output field "
                f"{output_field_key} must be a file field"
            )
        config = output_field.get("config")
        if not isinstance(config, dict):
            fail(f"Task template {template_id} output field {output_field_key} config must be an object")
        if config.get("documentRefId") != document_id:
            fail(
                f"Task template {template_id} output field {output_field_key} must set "
                f"config.documentRefId to {document_id}"
            )
        output_ref_pairs.add((output_field_key, document_id))

    for output_field_key, output_field in output_fields.items():
        config = output_field.get("config") or {}
        if not isinstance(config, dict):
            continue
        document_ref_id = config.get("documentRefId")
        if document_ref_id is None:
            continue
        if not isinstance(document_ref_id, str) or not document_ref_id:
            fail(f"Task template {template_id} output field {output_field_key} has invalid documentRefId")
        if (output_field_key, document_ref_id) not in output_ref_pairs:
            fail(
                f"Task template {template_id} output field {output_field_key} declares "
                f"documentRefId {document_ref_id} without matching definitionJson.documentRefs entry"
            )
    if requires_template_guidance and not has_template_guidance:
        fail(
            f"Task template {template_id} uses output/checklist document refs but does not reference "
            f"{TEMPLATE_USE_GUIDANCE_DOCUMENT_ID} as operating_guidance"
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


def validate_project_setup_contract(project_type_id: str, project_type: dict[str, Any]) -> None:
    project_setup = project_type.get("projectSetup")
    if not isinstance(project_setup, dict):
        fail(f"Project type {project_type_id} must declare projectSetup")

    required_evidence = require_string_list(
        project_setup.get("requiredEvidence"),
        f"Project type {project_type_id} projectSetup.requiredEvidence",
    )
    if not required_evidence:
        fail(f"Project type {project_type_id} projectSetup.requiredEvidence must not be empty")
    if len(required_evidence) != len(set(required_evidence)):
        fail(f"Project type {project_type_id} projectSetup.requiredEvidence has duplicates")

    setup_steps = require_mapping_list(
        project_setup.get("setupSteps"),
        f"Project type {project_type_id} projectSetup.setupSteps",
    )
    if not setup_steps:
        fail(f"Project type {project_type_id} projectSetup.setupSteps must not be empty")

    step_keys: list[str] = []
    required_step_evidence: list[str] = []
    for step in setup_steps:
        step_key = step.get("key")
        if not isinstance(step_key, str) or not step_key:
            fail(f"Project type {project_type_id} projectSetup.setupSteps entries must declare key")
        step_keys.append(step_key)
        for field_name in ["label", "purpose", "evidenceKey"]:
            if not isinstance(step.get(field_name), str) or not step.get(field_name):
                fail(
                    f"Project type {project_type_id} projectSetup.setupSteps.{step_key} "
                    f"must declare {field_name}"
                )
        if step.get("stepType") not in PROJECT_SETUP_STEP_TYPES:
            fail(
                f"Project type {project_type_id} projectSetup.setupSteps.{step_key}.stepType "
                f"must be one of {sorted(PROJECT_SETUP_STEP_TYPES)}"
            )
        if not isinstance(step.get("required"), bool):
            fail(
                f"Project type {project_type_id} projectSetup.setupSteps.{step_key}.required "
                "must be a boolean"
            )
        if step.get("required") is True:
            required_step_evidence.append(step["evidenceKey"])

        has_task_reference = any(
            isinstance(step.get(field_name), str) and step.get(field_name)
            for field_name in ["taskDefinitionSlug", "taskDefinitionTemplateId", "taskSelection"]
        )
        if not has_task_reference:
            fail(
                f"Project type {project_type_id} projectSetup.setupSteps.{step_key} "
                "must declare a task reference or taskSelection"
            )

    if len(step_keys) != len(set(step_keys)):
        fail(f"Project type {project_type_id} projectSetup.setupSteps has duplicate keys")
    if set(required_step_evidence) != set(required_evidence):
        fail(
            f"Project type {project_type_id} projectSetup.requiredEvidence must match required "
            f"setup step evidence keys: requiredEvidence={sorted(required_evidence)}, "
            f"requiredStepEvidence={sorted(required_step_evidence)}"
        )

    schedule_groups = require_mapping_list(
        project_setup.get("scheduleGroups"),
        f"Project type {project_type_id} projectSetup.scheduleGroups",
    )
    schedule_group_keys: list[str] = []
    task_contracts = load_task_template_contracts()
    for group in schedule_groups:
        group_key = group.get("key")
        if not isinstance(group_key, str) or not group_key:
            fail(f"Project type {project_type_id} projectSetup.scheduleGroups entries must declare key")
        schedule_group_keys.append(group_key)
        for field_name in ["label", "description"]:
            if not isinstance(group.get(field_name), str) or not group.get(field_name):
                fail(
                    f"Project type {project_type_id} projectSetup.scheduleGroups.{group_key} "
                    f"must declare {field_name}"
                )
        task_slugs = require_string_list(
            group.get("taskDefinitionSlugs"),
            f"Project type {project_type_id} projectSetup.scheduleGroups.{group_key}.taskDefinitionSlugs",
        )
        if not task_slugs:
            fail(
                f"Project type {project_type_id} projectSetup.scheduleGroups.{group_key} "
                "must list at least one taskDefinitionSlug"
            )
        for task_slug in task_slugs:
            contract = task_contracts.get(task_slug)
            if contract is None:
                fail(
                    f"Project type {project_type_id} projectSetup.scheduleGroups.{group_key} "
                    f"references unknown task {task_slug}"
                )
            if project_type_id not in contract.get("supportedProjectTypes", []):
                fail(
                    f"Project type {project_type_id} projectSetup.scheduleGroups.{group_key} "
                    f"references task {task_slug}, which does not support {project_type_id}"
                )
            scheduling = contract.get("scheduling")
            if not isinstance(scheduling, dict) or scheduling.get("schedulable") is not True:
                fail(
                    f"Project type {project_type_id} projectSetup.scheduleGroups.{group_key} "
                    f"references task {task_slug}, which is not schedulable"
                )
            if scheduling.get("showInProjectSetup") is not True:
                fail(
                    f"Project type {project_type_id} projectSetup.scheduleGroups.{group_key} "
                    f"references task {task_slug}, which is not shown in Project Setup"
                )
            if scheduling.get("setupStep") != "schedules":
                fail(
                    f"Project type {project_type_id} projectSetup.scheduleGroups.{group_key} "
                    f"references task {task_slug}, which is not a schedules-step task"
                )
        for field_name in ["defaultExpanded", "advanced"]:
            if not isinstance(group.get(field_name), bool):
                fail(
                    f"Project type {project_type_id} projectSetup.scheduleGroups.{group_key} "
                    f"must declare boolean {field_name}"
                )
    if len(schedule_group_keys) != len(set(schedule_group_keys)):
        fail(f"Project type {project_type_id} projectSetup.scheduleGroups has duplicate keys")

    def validate_source_evidence_keys(action_key: str, action: dict[str, Any]) -> list[str]:
        source_evidence_keys = require_string_list(
            action.get("sourceEvidenceKeys"),
            f"Project type {project_type_id} postApprovalActions.{action_key}.sourceEvidenceKeys",
        )
        if not source_evidence_keys:
            fail(
                f"Project type {project_type_id} postApprovalActions.{action_key}.sourceEvidenceKeys "
                "must not be empty"
            )
        unknown_evidence_roots = sorted(
            evidence_key.split(".", 1)[0]
            for evidence_key in source_evidence_keys
            if evidence_key.split(".", 1)[0] not in step_keys
        )
        if unknown_evidence_roots:
            fail(
                f"Project type {project_type_id} postApprovalActions.{action_key}.sourceEvidenceKeys "
                f"reference undeclared setup evidence roots: {unknown_evidence_roots}"
            )
        return source_evidence_keys

    def validate_enabled_platform_action(action_key: str, action: dict[str, Any]) -> None:
        if not isinstance(action.get("label"), str) or not action.get("label"):
            fail(f"Project type {project_type_id} enabled {action_key} must declare label")
        if not isinstance(action.get("target"), str) or not action.get("target"):
            fail(f"Project type {project_type_id} enabled {action_key} must declare target")
        validate_source_evidence_keys(action_key, action)
        if action.get("requiresReviewedUserApproval") is not True:
            fail(
                f"Project type {project_type_id} enabled {action_key} must require "
                "reviewed user approval"
            )
        if "dependsOn" in action:
            depends_on = require_string_list(
                action.get("dependsOn"),
                f"Project type {project_type_id} postApprovalActions.{action_key}.dependsOn",
            )
            unknown_dependencies = sorted(set(depends_on) - PROJECT_SETUP_POST_APPROVAL_ACTIONS)
            if unknown_dependencies:
                fail(
                    f"Project type {project_type_id} postApprovalActions.{action_key}.dependsOn "
                    f"references unknown actions: {unknown_dependencies}"
                )

    post_approval_actions = project_setup.get("postApprovalActions")
    if not isinstance(post_approval_actions, dict):
        fail(f"Project type {project_type_id} projectSetup.postApprovalActions must be declared")
    unknown_post_approval_actions = sorted(set(post_approval_actions) - PROJECT_SETUP_POST_APPROVAL_ACTIONS)
    if unknown_post_approval_actions:
        fail(
            f"Project type {project_type_id} projectSetup.postApprovalActions contains "
            f"unknown actions: {unknown_post_approval_actions}"
        )
    missing_post_approval_actions = sorted(PROJECT_SETUP_POST_APPROVAL_ACTIONS - set(post_approval_actions))
    if missing_post_approval_actions:
        fail(
            f"Project type {project_type_id} projectSetup.postApprovalActions must explicitly "
            f"declare actions: {missing_post_approval_actions}"
        )

    apply_variables = post_approval_actions.get("applyVariables")
    if not isinstance(apply_variables, dict):
        fail(f"Project type {project_type_id} projectSetup.postApprovalActions.applyVariables must be declared")
    if not isinstance(apply_variables.get("enabled"), bool):
        fail(f"Project type {project_type_id} applyVariables.enabled must be a boolean")
    if apply_variables.get("enabled") is True:
        validate_enabled_platform_action("applyVariables", apply_variables)
        if apply_variables.get("actionMode") != "platform_variable_application":
            fail(
                f"Project type {project_type_id} applyVariables.actionMode must be "
                "platform_variable_application"
            )
        if apply_variables.get("setupTasksMayPersistValues") is not False:
            fail(f"Project type {project_type_id} applyVariables.setupTasksMayPersistValues must be false")
    elif not isinstance(apply_variables.get("reason"), str) or not apply_variables.get("reason"):
        fail(f"Project type {project_type_id} disabled applyVariables must declare reason")

    import_projects = post_approval_actions.get("importProjects")
    if not isinstance(import_projects, dict):
        fail(
            f"Project type {project_type_id} projectSetup.postApprovalActions.importProjects "
            "must be declared"
        )
    if not isinstance(import_projects.get("enabled"), bool):
        fail(
            f"Project type {project_type_id} projectSetup.postApprovalActions.importProjects.enabled "
            "must be a boolean"
        )
    if import_projects.get("enabled") is True:
        if not isinstance(import_projects.get("label"), str) or not import_projects.get("label"):
            fail(f"Project type {project_type_id} enabled importProjects must declare label")
        if import_projects.get("targetProjectTypeKey") != project_type_id:
            fail(
                f"Project type {project_type_id} importProjects.targetProjectTypeKey must be "
                f"{project_type_id}"
            )
        validate_source_evidence_keys("importProjects", import_projects)
        project_import_task = import_projects.get("projectImportTask")
        if not isinstance(project_import_task, dict):
            fail(f"Project type {project_type_id} importProjects.projectImportTask must be declared")
        for field_name in ["taskDefinitionTemplateId", "taskDefinitionSlug", "inputField"]:
            if not isinstance(project_import_task.get(field_name), str) or not project_import_task.get(field_name):
                fail(
                    f"Project type {project_type_id} importProjects.projectImportTask "
                    f"must declare {field_name}"
                )
        task_slug = project_import_task["taskDefinitionSlug"]
        task_contract = task_contracts.get(task_slug)
        if task_contract is None:
            fail(f"Project type {project_type_id} importProjects references unknown task {task_slug}")
        if task_contract["id"] != project_import_task["taskDefinitionTemplateId"]:
            fail(
                f"Project type {project_type_id} importProjects references template id "
                f"{project_import_task['taskDefinitionTemplateId']}, but {task_slug} has id "
                f"{task_contract['id']}"
            )
        if project_type_id not in task_contract.get("supportedProjectTypes", []):
            fail(
                f"Project type {project_type_id} importProjects task {task_slug} "
                f"does not support {project_type_id}"
            )
        if DEFAULT_PROJECT_SCOPE not in task_contract.get("supportedProjectScopes", []):
            fail(
                f"Project type {project_type_id} importProjects task {task_slug} "
                f"must support {DEFAULT_PROJECT_SCOPE}"
            )
        input_field = project_import_task["inputField"]
        task_input_fields = task_contract["fields"]["input"]
        if input_field not in task_input_fields:
            fail(
                f"Project type {project_type_id} importProjects inputField {input_field} "
                f"is not an input field on {task_slug}"
            )
        if task_input_fields[input_field].get("required") is not True:
            fail(
                f"Project type {project_type_id} importProjects inputField {input_field} "
                f"must be required on {task_slug}"
            )
        payload_contract = project_import_task.get("payloadContract")
        if not isinstance(payload_contract, dict):
            fail(f"Project type {project_type_id} importProjects.projectImportTask must declare payloadContract")
        if not isinstance(payload_contract.get("version"), str) or not payload_contract.get("version"):
            fail(f"Project type {project_type_id} importProjects.payloadContract must declare version")
        for field_name in [
            "requiredTopLevelKeys",
            "requiredApprovalKeys",
            "requiredSourceKeys",
            "requiredSeedKeys",
            "requiredTargetProjectKeys",
        ]:
            if not require_string_list(
                payload_contract.get(field_name),
                f"Project type {project_type_id} importProjects.payloadContract.{field_name}",
            ):
                fail(
                    f"Project type {project_type_id} importProjects.payloadContract.{field_name} "
                    "must not be empty"
                )
        output_evidence_keys = require_string_list(
            project_import_task.get("outputEvidenceKeys"),
            f"Project type {project_type_id} importProjects.projectImportTask.outputEvidenceKeys",
        )
        if not output_evidence_keys:
            fail(f"Project type {project_type_id} importProjects.outputEvidenceKeys must not be empty")
        unknown_output_keys = sorted(
            set(output_evidence_keys) - set(task_contract["fields"]["output"].keys())
        )
        if unknown_output_keys:
            fail(
                f"Project type {project_type_id} importProjects.outputEvidenceKeys references "
                f"unknown task outputs: {unknown_output_keys}"
            )
        safety = import_projects.get("safety")
        if not isinstance(safety, dict):
            fail(f"Project type {project_type_id} importProjects.safety must be declared")
        expected_safety_values = {
            "requiresReviewedUserApproval": True,
            "setupTasksMayCreateProjects": False,
            "setupTasksMayImportRecords": False,
            "setupTasksMayEnableRecurringSync": False,
        }
        for field_name, expected_value in expected_safety_values.items():
            if safety.get(field_name) is not expected_value:
                fail(
                    f"Project type {project_type_id} importProjects.safety.{field_name} "
                    f"must be {expected_value}"
                )
    elif not isinstance(import_projects.get("reason"), str) or not import_projects.get("reason"):
        fail(f"Project type {project_type_id} disabled importProjects must declare reason")

    invite_collaborators = post_approval_actions.get("inviteCollaborators")
    if not isinstance(invite_collaborators, dict):
        fail(
            f"Project type {project_type_id} projectSetup.postApprovalActions.inviteCollaborators "
            "must be declared"
        )
    if not isinstance(invite_collaborators.get("enabled"), bool):
        fail(f"Project type {project_type_id} inviteCollaborators.enabled must be a boolean")
    if invite_collaborators.get("enabled") is True:
        validate_enabled_platform_action("inviteCollaborators", invite_collaborators)
        if "invite" not in step_keys:
            fail(
                f"Project type {project_type_id} inviteCollaborators is enabled without an invite "
                "setup step"
            )
        if invite_collaborators.get("actionMode") != "platform_project_membership":
            fail(
                f"Project type {project_type_id} inviteCollaborators.actionMode must be "
                "platform_project_membership"
            )
        if invite_collaborators.get("setupTasksMaySendInvites") is not False:
            fail(f"Project type {project_type_id} inviteCollaborators.setupTasksMaySendInvites must be false")
    elif not isinstance(invite_collaborators.get("reason"), str) or not invite_collaborators.get("reason"):
        fail(f"Project type {project_type_id} disabled inviteCollaborators must declare reason")

    enable_schedules = post_approval_actions.get("enableSchedules")
    if not isinstance(enable_schedules, dict):
        fail(f"Project type {project_type_id} projectSetup.postApprovalActions.enableSchedules must be declared")
    if not isinstance(enable_schedules.get("enabled"), bool):
        fail(f"Project type {project_type_id} enableSchedules.enabled must be a boolean")
    if enable_schedules.get("enabled") is True:
        validate_enabled_platform_action("enableSchedules", enable_schedules)
        if enable_schedules.get("scheduleGroupsRef") != "projectSetup.scheduleGroups":
            fail(
                f"Project type {project_type_id} enableSchedules.scheduleGroupsRef must be "
                "projectSetup.scheduleGroups"
            )
        if enable_schedules.get("defaultEnabled") is not False:
            fail(f"Project type {project_type_id} enableSchedules.defaultEnabled must be false")
        if enable_schedules.get("setupTasksMayEnableRecurringSync") is not False:
            fail(
                f"Project type {project_type_id} enableSchedules.setupTasksMayEnableRecurringSync "
                "must be false"
            )
    elif not isinstance(enable_schedules.get("reason"), str) or not enable_schedules.get("reason"):
        fail(f"Project type {project_type_id} disabled enableSchedules must declare reason")


def validate_project_creation_contract(
    project_type_id: str,
    project_type: dict[str, Any],
    field_keys: set[str],
    lifecycle_states: set[str],
) -> None:
    project_creation = project_type.get("projectCreation")
    if not isinstance(project_creation, dict):
        fail(f"Project type {project_type_id} must declare projectCreation")

    unknown_keys = sorted(set(project_creation) - PROJECT_CREATION_KEYS)
    if unknown_keys:
        fail(f"Project type {project_type_id} projectCreation contains unknown keys: {unknown_keys}")

    for field_name in ["launcherLabel", "starterId", "defaultState"]:
        if not isinstance(project_creation.get(field_name), str) or not project_creation.get(field_name):
            fail(f"Project type {project_type_id} projectCreation.{field_name} must be declared")

    starter_id = project_creation["starterId"]
    if PROJECT_CREATION_STARTER_ID_PATTERN.fullmatch(starter_id) is None:
        fail(
            f"Project type {project_type_id} projectCreation.starterId must be a stable "
            "lowercase slug"
        )

    aliases = require_string_list(
        project_creation.get("aliases"),
        f"Project type {project_type_id} projectCreation.aliases",
    )
    if len(aliases) != len(set(aliases)):
        fail(f"Project type {project_type_id} projectCreation.aliases has duplicates")

    all_creation_field_keys: list[str] = []
    for field_name in PROJECT_CREATION_FIELD_LISTS:
        keys = require_string_list(
            project_creation.get(field_name),
            f"Project type {project_type_id} projectCreation.{field_name}",
        )
        if len(keys) != len(set(keys)):
            fail(f"Project type {project_type_id} projectCreation.{field_name} has duplicates")
        unknown_field_keys = sorted(set(keys) - field_keys)
        if unknown_field_keys:
            fail(
                f"Project type {project_type_id} projectCreation.{field_name} "
                f"references unknown field keys: {unknown_field_keys}"
            )
        all_creation_field_keys.extend(keys)

    duplicate_creation_field_keys = sorted(
        key for key in set(all_creation_field_keys) if all_creation_field_keys.count(key) > 1
    )
    if duplicate_creation_field_keys:
        fail(
            f"Project type {project_type_id} projectCreation field lists overlap: "
            f"{duplicate_creation_field_keys}"
        )
    reserved_setup_field_keys = project_creation_reserved_field_keys_by_project_type().get(
        project_type_id,
        set(),
    )
    setup_fields_exposed_for_creation = sorted(
        set(all_creation_field_keys).intersection(reserved_setup_field_keys)
    )
    if setup_fields_exposed_for_creation:
        fail(
            f"Project type {project_type_id} projectCreation must not expose setup/workspace "
            f"variable fields: {setup_fields_exposed_for_creation}"
        )

    source_reference = project_creation.get("sourceReference")
    if source_reference is not None:
        if not isinstance(source_reference, dict):
            fail(f"Project type {project_type_id} projectCreation.sourceReference must be an object")
        for field_name in ["label", "connectionBindingKey"]:
            if not isinstance(source_reference.get(field_name), str) or not source_reference.get(field_name):
                fail(
                    f"Project type {project_type_id} projectCreation.sourceReference "
                    f"must declare {field_name}"
                )
        if source_reference.get("inputKind") not in PROJECT_CREATION_SOURCE_REFERENCE_INPUT_KINDS:
            fail(
                f"Project type {project_type_id} projectCreation.sourceReference.inputKind "
                f"must be one of {sorted(PROJECT_CREATION_SOURCE_REFERENCE_INPUT_KINDS)}"
            )
        target_field_keys = source_reference.get("targetFieldKeys")
        if not isinstance(target_field_keys, dict):
            fail(
                f"Project type {project_type_id} projectCreation.sourceReference."
                "targetFieldKeys must be declared"
            )
        missing_target_keys = sorted(
            PROJECT_CREATION_SOURCE_REFERENCE_TARGET_KEYS - set(target_field_keys)
        )
        unknown_target_keys = sorted(
            set(target_field_keys) - PROJECT_CREATION_SOURCE_REFERENCE_TARGET_KEYS
        )
        if missing_target_keys or unknown_target_keys:
            fail(
                f"Project type {project_type_id} projectCreation.sourceReference."
                f"targetFieldKeys mismatch: missing={missing_target_keys}, "
                f"unknown={unknown_target_keys}"
            )
        source_reference_field_keys: list[str] = []
        for target_key, field_key in target_field_keys.items():
            if not isinstance(field_key, str) or not field_key:
                fail(
                    f"Project type {project_type_id} projectCreation.sourceReference."
                    f"targetFieldKeys.{target_key} must be a field key"
                )
            if field_key not in field_keys:
                fail(
                    f"Project type {project_type_id} projectCreation.sourceReference."
                    f"targetFieldKeys.{target_key} references unknown field key {field_key}"
                )
            source_reference_field_keys.append(field_key)
        legacy_field_keys = require_string_list(
            source_reference.get("legacyFieldKeys"),
            f"Project type {project_type_id} projectCreation.sourceReference.legacyFieldKeys",
        )
        unknown_legacy_field_keys = sorted(set(legacy_field_keys) - field_keys)
        if unknown_legacy_field_keys:
            fail(
                f"Project type {project_type_id} projectCreation.sourceReference."
                f"legacyFieldKeys references unknown field keys: {unknown_legacy_field_keys}"
            )
        source_reference_field_keys.extend(legacy_field_keys)
        duplicated_source_reference_keys = sorted(
            key
            for key in set(source_reference_field_keys)
            if source_reference_field_keys.count(key) > 1
        )
        if duplicated_source_reference_keys:
            fail(
                f"Project type {project_type_id} projectCreation.sourceReference "
                f"contains duplicate field refs: {duplicated_source_reference_keys}"
            )
        exposed_source_reference_keys = sorted(
            set(source_reference_field_keys).intersection(all_creation_field_keys)
        )
        if exposed_source_reference_keys:
            fail(
                f"Project type {project_type_id} projectCreation.sourceReference fields "
                f"must not also be rendered as creation fields: {exposed_source_reference_keys}"
            )

    default_state = project_creation["defaultState"]
    if default_state not in lifecycle_states:
        fail(
            f"Project type {project_type_id} projectCreation.defaultState must be one of "
            f"{sorted(lifecycle_states)}"
        )

    guided_task = project_creation.get("guidedTask")
    if not isinstance(guided_task, dict):
        fail(f"Project type {project_type_id} projectCreation.guidedTask must be declared")
    for field_name in ["taskDefinitionTemplateId", "taskDefinitionSlug"]:
        if not isinstance(guided_task.get(field_name), str) or not guided_task.get(field_name):
            fail(
                f"Project type {project_type_id} projectCreation.guidedTask "
                f"must declare {field_name}"
            )
    task_contracts = load_task_template_contracts()
    task_slug = guided_task["taskDefinitionSlug"]
    task_contract = task_contracts.get(task_slug)
    if task_contract is None:
        fail(f"Project type {project_type_id} projectCreation references unknown task {task_slug}")
    if task_contract["id"] != guided_task["taskDefinitionTemplateId"]:
        fail(
            f"Project type {project_type_id} projectCreation references template id "
            f"{guided_task['taskDefinitionTemplateId']}, but {task_slug} has id "
            f"{task_contract['id']}"
        )
    if project_type_id not in task_contract.get("supportedProjectTypes", []):
        fail(
            f"Project type {project_type_id} projectCreation task {task_slug} "
            f"does not support {project_type_id}"
        )
    if DEFAULT_PROJECT_SCOPE not in task_contract.get("supportedProjectScopes", []):
        fail(
            f"Project type {project_type_id} projectCreation task {task_slug} "
            f"must support {DEFAULT_PROJECT_SCOPE}"
        )
    task_input_fields = task_contract["fields"]["input"]
    task_output_fields = task_contract["fields"]["output"]
    for field_key in require_string_list(
        project_creation.get("requiredFieldKeys"),
        f"Project type {project_type_id} projectCreation.requiredFieldKeys",
    ):
        if field_key not in task_input_fields and field_key not in task_output_fields:
            fail(
                f"Project type {project_type_id} projectCreation guided task {task_slug} "
                f"must collect or emit required creation field {field_key}"
            )
    completion_output = task_output_fields.get(PROJECT_CREATION_COMPLETION_OUTPUT_KEY)
    if completion_output is None:
        fail(
            f"Project type {project_type_id} projectCreation guided task {task_slug} "
            f"must declare output {PROJECT_CREATION_COMPLETION_OUTPUT_KEY}"
        )
    if completion_output.get("fieldType") != "json":
        fail(
            f"Project type {project_type_id} projectCreation guided task {task_slug} "
            f"output {PROJECT_CREATION_COMPLETION_OUTPUT_KEY} must use fieldType: json"
        )
    if completion_output.get("required") is not True:
        fail(
            f"Project type {project_type_id} projectCreation guided task {task_slug} "
            f"output {PROJECT_CREATION_COMPLETION_OUTPUT_KEY} must be required"
        )
    completion_config = completion_output.get("config")
    if not isinstance(completion_config, dict):
        fail(
            f"Project type {project_type_id} projectCreation guided task {task_slug} "
            f"output {PROJECT_CREATION_COMPLETION_OUTPUT_KEY} must declare config"
        )
    required_paths = require_string_list(
        completion_config.get("requiredPaths"),
        (
            f"Project type {project_type_id} projectCreation guided task {task_slug} "
            f"output {PROJECT_CREATION_COMPLETION_OUTPUT_KEY}.config.requiredPaths"
        ),
    )
    missing_required_paths = sorted(
        f"fieldValues.{field_key}"
        for field_key in project_creation["requiredFieldKeys"]
        if f"fieldValues.{field_key}" not in required_paths
    )
    if missing_required_paths:
        fail(
            f"Project type {project_type_id} projectCreation guided task {task_slug} "
            f"completion output is missing requiredPaths: {missing_required_paths}"
        )

    post_create = project_creation.get("postCreate")
    if not isinstance(post_create, dict):
        fail(f"Project type {project_type_id} projectCreation.postCreate must be declared")
    if set(post_create) != {"triggerInitialStateTasks"}:
        fail(
            f"Project type {project_type_id} projectCreation.postCreate must only declare "
            "triggerInitialStateTasks"
        )
    if not isinstance(post_create.get("triggerInitialStateTasks"), bool):
        fail(
            f"Project type {project_type_id} projectCreation.postCreate."
            "triggerInitialStateTasks must be a boolean"
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
    validate_project_setup_contract(expected_id, project_type)

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
    validate_project_creation_contract(
        expected_id,
        project_type,
        set(field_keys),
        set(lifecycle_states),
    )

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


def validate_document_markdown(
    document_root: Path,
    markdown_path: Path,
    catalog_entry: dict[str, Any],
) -> None:
    frontmatter = parse_frontmatter(markdown_path)
    relative_path = markdown_path.relative_to(document_root)
    markdown_text = markdown_path.read_text(encoding="utf-8")

    for field_name in ["id", "title", "documentType", "supportedProjectTypes"]:
        if field_name not in frontmatter:
            fail(f"Document {relative_path} frontmatter must declare {field_name}")
    for field_name in ["id", "title", "documentType"]:
        if frontmatter.get(field_name) != catalog_entry.get(field_name):
            fail(
                f"Document {relative_path} frontmatter {field_name} must match catalog entry "
                f"{catalog_entry.get('id')}"
            )
    supported_project_types = require_string_list(
        frontmatter.get("supportedProjectTypes"),
        f"Document {relative_path} frontmatter.supportedProjectTypes",
    )
    if supported_project_types != catalog_entry.get("supportedProjectTypes"):
        fail(
            f"Document {relative_path} frontmatter.supportedProjectTypes must match catalog entry "
            f"{catalog_entry.get('id')}"
        )
    if not isinstance(frontmatter.get("summary"), str) or not frontmatter.get("summary"):
        fail(f"Document {relative_path} frontmatter must declare summary")
    validate_markdown_tables(relative_path, markdown_text)
    validate_document_output_hygiene(relative_path, markdown_text)
    validate_document_quality_sections(relative_path, markdown_text, catalog_entry)


def validate_markdown_tables(relative_path: Path, markdown_text: str) -> None:
    table_block: list[tuple[int, str]] = []
    for line_number, line in enumerate(markdown_text.splitlines(), start=1):
        if line.startswith("|"):
            table_block.append((line_number, line))
            continue
        if table_block:
            validate_markdown_table_block(relative_path, table_block)
            table_block = []
    if table_block:
        validate_markdown_table_block(relative_path, table_block)


def validate_markdown_table_block(relative_path: Path, table_block: list[tuple[int, str]]) -> None:
    pipe_counts = {line.count("|") for _, line in table_block}
    if len(pipe_counts) > 1:
        first_line = table_block[0][0]
        fail(
            f"Document {relative_path}:{first_line} has inconsistent Markdown table columns: "
            f"{sorted(pipe_counts)}"
        )


def validate_document_output_hygiene(relative_path: Path, markdown_text: str) -> None:
    lowered = markdown_text.lower()
    for pattern in DOCUMENT_AUTHORING_LEAK_PATTERNS:
        if pattern in lowered:
            fail(f"Document {relative_path} contains authoring/prompt guidance leak: {pattern!r}")


def validate_document_quality_sections(
    relative_path: Path,
    markdown_text: str,
    catalog_entry: dict[str, Any],
) -> None:
    document_type = catalog_entry.get("documentType")
    reader_facing_quality_sections = [
        "## Approval Rule",
        "## Batch Rule",
        "## Boundary",
        "## Cadence",
        "## Decision",
        "## Escalation Rule",
        "## Standard",
        "## Usage",
    ]
    if document_type in {"template", "checklist"} and not any(
        heading in markdown_text for heading in reader_facing_quality_sections
    ):
        fail(f"Document {relative_path} must include a reader-facing quality or boundary section")
    if catalog_entry.get("id") in {
        "vc.document.investment_memo_template",
        "vc.document.diligence_report_template",
        "vc.document.review_pack_checklist",
        "vc.document.initial_call_brief_template",
        "vc.document.sourcing_digest_template",
        "vc.document.closing_checklist",
    } and "## Source Inputs" not in markdown_text:
        fail(f"Document {relative_path} must include a Source Inputs section")


def validate_documents(
    manifest: dict[str, Any],
    project_type_ids: set[str],
) -> tuple[dict[str, set[str]], dict[str, str]]:
    surface = manifest["surfaces"].get("documents")
    if not isinstance(surface, dict):
        fail("Manifest must declare surfaces.documents")
    surface_path = surface.get("path")
    if not isinstance(surface_path, str) or not surface_path:
        fail("surfaces.documents.path must be declared")
    if surface.get("status") != DOCUMENT_SURFACE_STATUS:
        fail(f"surfaces.documents.status must be {DOCUMENT_SURFACE_STATUS}")
    if surface.get("catalog") != "catalog.v1.json":
        fail("surfaces.documents.catalog must be catalog.v1.json")
    manifest_document_ids = surface.get("ids")
    if not isinstance(manifest_document_ids, list) or not all(
        isinstance(item, str) for item in manifest_document_ids
    ):
        fail("surfaces.documents.ids must be a list of strings")
    if len(manifest_document_ids) != len(set(manifest_document_ids)):
        fail("Duplicate document IDs in alludium/manifest.yaml")

    document_root = ROOT / surface_path
    resolved_document_root = document_root.resolve()
    try:
        resolved_document_root.relative_to(ROOT.resolve())
    except ValueError:
        fail(f"surfaces.documents.path must resolve inside the pack root: {surface_path}")
    if not document_root.is_dir():
        fail(f"surfaces.documents.path must reference an existing directory: {surface_path}")

    catalog_path = document_root / "catalog.v1.json"
    if not catalog_path.exists():
        fail(f"Missing document catalog: {catalog_path.relative_to(ROOT)}")
    catalog = read_json(catalog_path)
    if not isinstance(catalog, dict):
        fail(f"{catalog_path.relative_to(ROOT)} must be an object")
    if catalog.get("kind") != "document-catalog":
        fail(f"{catalog_path.relative_to(ROOT)} kind must be document-catalog")
    if catalog.get("apiVersion") != "alludium/v1alpha1":
        fail(f"{catalog_path.relative_to(ROOT)} apiVersion must be alludium/v1alpha1")

    catalog_entries = catalog.get("documents")
    if not isinstance(catalog_entries, list) or not catalog_entries:
        fail(f"{catalog_path.relative_to(ROOT)} documents must be a non-empty list")

    discovered_ids: list[str] = []
    discovered_paths: set[Path] = set()
    document_ids_by_project_type: dict[str, set[str]] = {
        project_type_id: set() for project_type_id in project_type_ids
    }
    document_types_by_id: dict[str, str] = {}
    task_slugs = set(load_task_template_contracts())
    for entry in catalog_entries:
        if not isinstance(entry, dict):
            fail("Document catalog entries must be objects")
        document_id = entry.get("id")
        relative_document_path = entry.get("path")
        if not isinstance(document_id, str) or not document_id:
            fail("Document catalog entries must declare id")
        if not isinstance(entry.get("title"), str) or not entry.get("title"):
            fail(f"Document catalog entry {document_id} must declare title")
        if not isinstance(entry.get("description"), str) or not entry.get("description"):
            fail(f"Document catalog entry {document_id} must declare description")
        if entry.get("documentType") not in DOCUMENT_TYPES:
            fail(f"Document catalog entry {document_id} has invalid documentType")
        document_types_by_id[document_id] = entry["documentType"]
        if entry.get("status") not in DOCUMENT_STATUSES:
            fail(f"Document catalog entry {document_id} has invalid status")
        if not isinstance(relative_document_path, str) or not relative_document_path:
            fail(f"Document catalog entry {document_id} must declare path")
        if not relative_document_path.endswith(".md"):
            fail(f"Document catalog entry {document_id} path must reference Markdown")

        supported_project_types = require_string_list(
            entry.get("supportedProjectTypes"),
            f"Document catalog entry {document_id}.supportedProjectTypes",
        )
        if not supported_project_types:
            fail(f"Document catalog entry {document_id} must declare supportedProjectTypes")
        unknown_project_types = sorted(set(supported_project_types) - project_type_ids)
        if unknown_project_types:
            fail(
                f"Document catalog entry {document_id} references unknown project types: "
                f"{unknown_project_types}"
            )
        if len(supported_project_types) != len(set(supported_project_types)):
            fail(f"Document catalog entry {document_id} has duplicate supportedProjectTypes")
        related_slugs = require_string_list(
            entry.get("relatedTaskDefinitionSlugs"),
            f"Document catalog entry {document_id}.relatedTaskDefinitionSlugs",
        )
        if len(related_slugs) != len(set(related_slugs)):
            fail(f"Document catalog entry {document_id} has duplicate relatedTaskDefinitionSlugs")
        unknown_related_slugs = sorted(set(related_slugs) - task_slugs)
        if unknown_related_slugs:
            fail(
                f"Document catalog entry {document_id} references unknown task slugs: "
                f"{unknown_related_slugs}"
            )

        document_path = document_root / relative_document_path
        resolved_document_path = document_path.resolve()
        try:
            resolved_document_path.relative_to(resolved_document_root)
        except ValueError:
            fail(f"Document catalog path escapes document surface: {relative_document_path}")
        if not document_path.exists():
            fail(f"Document catalog references missing file {relative_document_path}")
        discovered_paths.add(resolved_document_path)
        discovered_ids.append(document_id)
        validate_document_markdown(document_root, resolved_document_path, entry)
        for project_type_id in supported_project_types:
            document_ids_by_project_type[project_type_id].add(document_id)

    if len(discovered_ids) != len(set(discovered_ids)):
        fail("Duplicate document IDs in catalog files")
    if set(discovered_ids) != set(manifest_document_ids):
        fail(
            "Manifest document IDs do not match catalog files: "
            f"manifest_only={sorted(set(manifest_document_ids) - set(discovered_ids))}, "
            f"catalog_only={sorted(set(discovered_ids) - set(manifest_document_ids))}"
        )

    actual_markdown_paths = {path.resolve() for path in document_root.glob("**/*.md")}
    extra_markdown_paths = actual_markdown_paths - discovered_paths
    if extra_markdown_paths:
        fail(
            "Document Markdown files present on disk but missing from catalog: "
            f"{sorted(str(path.relative_to(document_root)) for path in extra_markdown_paths)}"
        )

    return document_ids_by_project_type, document_types_by_id


def validate_project_type_document_references(
    manifest: dict[str, Any],
    document_ids_by_project_type: dict[str, set[str]],
) -> None:
    project_type_root = ROOT / manifest["surfaces"]["projectTypes"]["path"]
    for project_type_id, expected_document_ids in document_ids_by_project_type.items():
        project_type_path = project_type_root / f"{project_type_id}.json"
        project_type = read_json(project_type_path)
        initial_version = project_type.get("initialVersion") or {}
        if not isinstance(initial_version, dict):
            fail(f"Project type {project_type_id} initialVersion must be an object")
        document_library = initial_version.get("documentLibrary")
        if not isinstance(document_library, dict):
            fail(f"Project type {project_type_id} initialVersion.documentLibrary must be declared")
        if document_library.get("catalogPath") != DOCUMENT_CATALOG_PATH:
            fail(
                f"Project type {project_type_id} documentLibrary.catalogPath must be "
                f"{DOCUMENT_CATALOG_PATH}"
            )
        document_ids = require_string_list(
            document_library.get("documentIds"),
            f"Project type {project_type_id} documentLibrary.documentIds",
        )
        if len(document_ids) != len(set(document_ids)):
            fail(f"Project type {project_type_id} documentLibrary.documentIds has duplicates")
        if set(document_ids) != expected_document_ids:
            fail(
                f"Project type {project_type_id} documentLibrary.documentIds must match "
                "document catalog supportedProjectTypes: "
                f"missing={sorted(expected_document_ids - set(document_ids))}, "
                f"extra={sorted(set(document_ids) - expected_document_ids)}"
            )


def validate_task_template_file(
    path: Path,
    expected_pack: dict[str, Any],
    skill_ids: set[str],
    agent_template_ids: set[str],
    project_type_ids: set[str],
    document_ids: set[str],
    document_types_by_id: dict[str, str],
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
    validate_project_scope_instruction_language(
        template_id,
        slug,
        definition_json,
        supported_project_scopes,
    )
    validate_task_template_reference_list(
        template_id,
        "supportedProjectTypes",
        supported_project_types,
        project_type_ids,
        "included project types",
    )
    validate_task_scheduling_contract(template_id, slug, definition_json, supported_project_types)

    fields = template.get("fields") or {}
    if not isinstance(fields, dict):
        fail(f"Task template {template_id} fields must be an object when declared")
    validate_task_template_document_refs(
        template_id,
        slug,
        definition_json,
        fields,
        document_ids,
        document_types_by_id,
    )
    validate_required_artifact_fields(template_id, slug, fields)
    validate_vc_deal_room_task_template_shape(
        template_id,
        slug,
        definition_json,
        fields,
        supported_project_types,
        supported_project_scopes,
    )

    pack_vertical_keys = expected_pack.get("verticalKeys") or []
    if expected_pack.get("availability") == "vertical" and not pack_vertical_keys:
        fail(f"Task template pack {expected_pack.get('id')} must declare verticalKeys")

    return template_id


def validate_integration_setup_task_templates(task_root: Path, template_ids: set[str]) -> None:
    for setup_template_id, expected in EXPECTED_SETUP_CHILD_TASKS.items():
        if setup_template_id not in template_ids:
            fail(f"Missing integration setup task template {setup_template_id}")

        setup_template: dict[str, Any] | None = None
        for path in task_root.glob("**/*.yaml"):
            candidate = read_yaml(path)
            if isinstance(candidate, dict) and candidate.get("id") == setup_template_id:
                setup_template = candidate
                break
        if setup_template is None:
            fail(f"Missing integration setup task template file for {setup_template_id}")

        definition = setup_template.get("definition")
        if not isinstance(definition, dict):
            fail(f"Integration setup task {setup_template_id} definition must be an object")
        if definition.get("allowSubtasks") is not True:
            fail(f"Integration setup task {setup_template_id} must allow subtasks")
        definition_json = definition.get("definitionJson")
        if not isinstance(definition_json, dict):
            fail(f"Integration setup task {setup_template_id} definitionJson must be an object")
        if definition_json.get("taskFamily") != "integration_setup":
            fail(f"Integration setup task {setup_template_id} taskFamily must be integration_setup")

        setup_contract = definition_json.get("integrationSetup")
        if not isinstance(setup_contract, dict):
            fail(f"Integration setup task {setup_template_id} must declare definitionJson.integrationSetup")
        if setup_contract.get("applicationExternalId") != expected["applicationExternalId"]:
            fail(
                f"Integration setup task {setup_template_id} applicationExternalId must be "
                f"{expected['applicationExternalId']}"
            )

        child_task_ids = setup_contract.get("childTaskDefinitionTemplateIds")
        if not isinstance(child_task_ids, dict):
            fail(
                f"Integration setup task {setup_template_id} must declare "
                "integrationSetup.childTaskDefinitionTemplateIds"
            )
        if child_task_ids != expected["childTaskDefinitionTemplateIds"]:
            fail(
                f"Integration setup task {setup_template_id} childTaskDefinitionTemplateIds must be "
                f"{expected['childTaskDefinitionTemplateIds']}"
            )
        for child_template_id in child_task_ids.values():
            if child_template_id not in template_ids:
                fail(
                    f"Integration setup task {setup_template_id} references missing child task "
                    f"{child_template_id}"
                )

        default_flow = setup_contract.get("defaultFlow")
        if not isinstance(default_flow, list) or not default_flow:
            fail(f"Integration setup task {setup_template_id} must declare integrationSetup.defaultFlow")
        flow_template_ids = {
            step.get("taskDefinitionTemplateId")
            for step in default_flow
            if isinstance(step, dict) and isinstance(step.get("taskDefinitionTemplateId"), str)
        }
        if flow_template_ids != set(child_task_ids.values()):
            fail(
                f"Integration setup task {setup_template_id} defaultFlow must reference exactly "
                "the declared child task templates"
            )


def validate_task_definition_templates(
    manifest: dict[str, Any],
    skill_ids: set[str],
    agent_template_ids: set[str],
    project_type_ids: set[str],
    document_ids: set[str],
    document_types_by_id: dict[str, str],
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
                    document_ids,
                    document_types_by_id,
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
    validate_integration_setup_task_templates(task_root, set(discovered_ids))

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
            "stage": definition_json.get("stage"),
            "scheduling": definition_json.get("scheduling"),
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


def option_values(options: Any) -> set[str]:
    values: set[str] = set()
    if not isinstance(options, list):
        return values
    for option in options:
        if isinstance(option, str) and option:
            values.add(option)
        elif isinstance(option, dict):
            value = option.get("value")
            if isinstance(value, str) and value:
                values.add(value)
    return values


def field_option_values(field: dict[str, Any]) -> set[str]:
    values = option_values(field.get("options"))
    config = field.get("config")
    if isinstance(config, dict):
        values.update(option_values(config.get("options")))
    return values


def camel_to_snake(value: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", value).lower()


@lru_cache(maxsize=1)
def project_creation_reserved_field_keys_by_project_type() -> dict[str, set[str]]:
    variables_path = ROOT / "alludium" / "workspace-variables.yaml"
    if not variables_path.exists():
        return {}
    surface = read_yaml(variables_path)
    if not isinstance(surface, dict):
        return {}
    reserved_by_project_type: dict[str, set[str]] = {}
    for variable in surface.get("workspaceVariables") or []:
        if not isinstance(variable, dict):
            continue
        namespace = variable.get("namespace")
        key = variable.get("key")
        if not isinstance(namespace, str) or not isinstance(key, str):
            continue
        variable_key = f"{namespace}.{key}"
        derived_field_key = camel_to_snake(key)
        if derived_field_key.startswith("origination_"):
            derived_field_key = derived_field_key.removeprefix("origination_")
        reserved_field_keys = {derived_field_key}
        reserved_field_keys.update(PROJECT_CREATION_VARIABLE_FIELD_ALIASES.get(variable_key, set()))
        for project_type_id in require_string_list(
            variable.get("supportedProjectTypes"),
            f"Workspace variable {variable_key}.supportedProjectTypes",
        ):
            reserved_by_project_type.setdefault(project_type_id, set()).update(reserved_field_keys)
    return reserved_by_project_type


def project_setup_import_task_slugs(project_type: dict[str, Any]) -> set[str]:
    project_setup = project_type.get("projectSetup")
    if not isinstance(project_setup, dict):
        return set()
    post_approval_actions = project_setup.get("postApprovalActions")
    if not isinstance(post_approval_actions, dict):
        return set()
    import_projects = post_approval_actions.get("importProjects")
    if not isinstance(import_projects, dict) or import_projects.get("enabled") is not True:
        return set()
    project_import_task = import_projects.get("projectImportTask")
    if not isinstance(project_import_task, dict):
        return set()
    task_slug = project_import_task.get("taskDefinitionSlug")
    return {task_slug} if isinstance(task_slug, str) and task_slug else set()


def validate_json_input_mapping_source(
    project_type_id: str,
    mapping_id: str,
    task_field: str,
    entry: dict[str, Any],
    task_input_field: dict[str, Any],
) -> None:
    if (
        task_input_field.get("fieldType") == "json"
        and entry.get("source") == "constant"
        and isinstance(entry.get("constantValue"), str)
    ):
        fail(
            f"Project type {project_type_id} mapping {mapping_id}.inputMappings.{task_field} "
            "must not satisfy a JSON input field with a string constant"
        )


def validate_project_enum_output_mapping(
    project_type_id: str,
    mapping_id: str,
    task_field: str,
    task_output_field: dict[str, Any],
    project_field: dict[str, Any],
) -> None:
    if project_field.get("kind") != "enum":
        return
    output_type = task_output_field.get("fieldType")
    if output_type != "select":
        fail(
            f"Project type {project_type_id} mapping {mapping_id}.outputMappings.{task_field} "
            "maps into an enum project field, so the task output must use fieldType: select"
        )
    project_options = field_option_values(project_field)
    output_options = field_option_values(task_output_field)
    if not output_options:
        fail(
            f"Project type {project_type_id} mapping {mapping_id}.outputMappings.{task_field} "
            "maps into an enum project field, so the task output must declare options"
        )
    unknown_options = sorted(output_options - project_options)
    if unknown_options:
        fail(
            f"Project type {project_type_id} mapping {mapping_id}.outputMappings.{task_field} "
            f"declares options not present on the target enum project field: {unknown_options}"
        )


def validate_project_task_mapping_contracts() -> None:
    project_type = read_json(ROOT / "alludium" / "project-types" / "vc_deal_room.json")
    initial_version = project_type.get("initialVersion") or {}
    project_type_id = project_type.get("key", "vc_deal_room")
    project_fields_by_key = {
        field["key"]: field
        for field in initial_version.get("fieldsSchema", [])
        if isinstance(field, dict) and isinstance(field.get("key"), str)
    }
    project_field_keys = set(project_fields_by_key)
    lifecycle_states = set(require_string_list(
        initial_version.get("lifecycleStates"),
        f"Project type {project_type_id} initialVersion.lifecycleStates",
    ))
    task_contracts = load_task_template_contracts()
    import_project_task_slugs = project_setup_import_task_slugs(project_type)
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

        mapped_input_fields: set[str] = set()
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
                    mapped_input_fields.add(task_field)
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
                    validate_json_input_mapping_source(
                        project_type_id,
                        mapping_id,
                        task_field,
                        entry,
                        task_contract["fields"]["input"][task_field],
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
                    if target == "project.field":
                        validate_project_enum_output_mapping(
                            project_type_id,
                            mapping_id,
                            task_field,
                            task_contract["fields"]["output"][task_field],
                            project_fields_by_key[target_path],
                        )
                    if "requiredForCompletion" in entry and not isinstance(entry["requiredForCompletion"], bool):
                        fail(
                            f"Project type {project_type_id} mapping {mapping_id}.outputMappings.{task_field} "
                            "requiredForCompletion must be a boolean"
                        )
                    if project_scope == DEFAULT_PROJECT_SCOPE:
                        mapped_outputs_by_slug.setdefault(slug, set()).add(task_field)

        if project_scope == DEFAULT_PROJECT_SCOPE:
            required_input_fields = {
                field_key
                for field_key, field in task_contract["fields"]["input"].items()
                if field.get("required") is True
            }
            missing_required_inputs = sorted(required_input_fields - mapped_input_fields)
            if missing_required_inputs and slug not in import_project_task_slugs:
                fail(
                    f"Project type {project_type_id} mapping {mapping_id} is missing "
                    f"required task input mappings: {missing_required_inputs}"
                )

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


ORIGINATION_STAGE_LIFECYCLE_STAGES = {
    "setup": {"draft", "configured", "needs_credentials"},
    "source": {"active"},
    "enrich": {"review_backlog"},
    "score": {"review_backlog"},
    "review": {"review_backlog"},
    "engage": {"review_backlog"},
    "promote": {"review_backlog"},
    "operate": {"active", "source_degraded", "paused", "migration_in_progress"},
}


def validate_origination_pipeline_task_mapping_contracts() -> None:
    project_type_id = "vc_origination_pipeline"
    project_type = read_json(ROOT / "alludium" / "project-types" / f"{project_type_id}.json")
    initial_version = project_type.get("initialVersion") or {}
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
    mappings = require_mapping_list(
        initial_version.get("projectTaskMappings"),
        f"Project type {project_type_id} initialVersion.projectTaskMappings",
    )
    if not mappings:
        fail(f"Project type {project_type_id} must declare projectTaskMappings")

    expected_project_instance_slugs = {
        slug
        for slug, contract in task_contracts.items()
        if project_type_id in contract.get("supportedProjectTypes", [])
        and DEFAULT_PROJECT_SCOPE in contract.get("supportedProjectScopes", [])
    }
    mapped_project_instance_slugs: set[str] = set()
    mapping_ids: list[str] = []

    for mapping in mappings:
        mapping_id = mapping.get("id")
        if not isinstance(mapping_id, str) or not mapping_id:
            fail(f"Project type {project_type_id} projectTaskMappings entries must declare id")
        mapping_ids.append(mapping_id)
        if "activationMode" in mapping:
            fail(
                f"Project type {project_type_id} mapping {mapping_id} must use "
                "activationPolicy, not activationMode"
            )

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
        if project_type_id not in task_contract.get("supportedProjectTypes", []):
            fail(f"Project type {project_type_id} mapping {mapping_id} task {slug} does not support {project_type_id}")

        project_scope = mapping.get("projectScope", DEFAULT_PROJECT_SCOPE)
        if project_scope not in PROJECT_SCOPES:
            fail(
                f"Project type {project_type_id} mapping {mapping_id} projectScope must be one of "
                f"{sorted(PROJECT_SCOPES)}"
            )
        if project_scope not in task_contract["supportedProjectScopes"]:
            fail(
                f"Project type {project_type_id} mapping {mapping_id} uses projectScope "
                f"{project_scope}, but task {slug} supports {task_contract['supportedProjectScopes']}"
            )
        if project_scope == DEFAULT_PROJECT_SCOPE:
            mapped_project_instance_slugs.add(slug)

        lifecycle_stage = mapping.get("lifecycleStage")
        if lifecycle_stage not in lifecycle_states:
            fail(
                f"Project type {project_type_id} mapping {mapping_id} references unknown "
                f"lifecycleStage {lifecycle_stage}"
            )
        stage = task_contract.get("stage")
        allowed_lifecycle_stages = ORIGINATION_STAGE_LIFECYCLE_STAGES.get(stage)
        if allowed_lifecycle_stages is not None and lifecycle_stage not in allowed_lifecycle_stages:
            fail(
                f"Project type {project_type_id} mapping {mapping_id} maps task stage {stage} "
                f"to lifecycleStage {lifecycle_stage}; expected one of "
                f"{sorted(allowed_lifecycle_stages)}"
            )

        if require_mapping_list(
            mapping.get("contextMappings"),
            f"Project type {project_type_id} mapping {mapping_id}.contextMappings",
        ):
            fail(f"Project type {project_type_id} mapping {mapping_id} must not declare contextMappings")

        mapped_input_fields: set[str] = set()
        for entry in require_mapping_list(
            mapping.get("inputMappings"),
            f"Project type {project_type_id} mapping {mapping_id}.inputMappings",
        ):
            task_field = entry.get("taskField")
            if not isinstance(task_field, str) or not task_field:
                fail(f"Project type {project_type_id} mapping {mapping_id}.inputMappings entries must declare taskField")
            if task_field not in task_contract["fields"]["input"]:
                fail(
                    f"Project type {project_type_id} mapping {mapping_id}.inputMappings.{task_field} "
                    "references an unknown task input field"
                )
            mapped_input_fields.add(task_field)
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

        required_input_fields = {
            field_key
            for field_key, field in task_contract["fields"]["input"].items()
            if field.get("required") is True
        }
        missing_required_inputs = sorted(required_input_fields - mapped_input_fields)
        if missing_required_inputs:
            fail(
                f"Project type {project_type_id} mapping {mapping_id} is missing "
                f"required task input mappings: {missing_required_inputs}"
            )

        for entry in require_mapping_list(
            mapping.get("outputMappings"),
            f"Project type {project_type_id} mapping {mapping_id}.outputMappings",
        ):
            task_field = entry.get("taskField")
            if not isinstance(task_field, str) or not task_field:
                fail(f"Project type {project_type_id} mapping {mapping_id}.outputMappings entries must declare taskField")
            if task_field not in task_contract["fields"]["output"]:
                fail(
                    f"Project type {project_type_id} mapping {mapping_id}.outputMappings.{task_field} "
                    "references an unknown task output field"
                )
            target = entry.get("target")
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
            output_field = task_contract["fields"]["output"][task_field]
            if output_field.get("fieldType") == "json":
                fail(
                    f"Project type {project_type_id} mapping {mapping_id}.outputMappings.{task_field} "
                    "must not map bulky JSON output into project data"
                )

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

    missing_project_instance_mappings = sorted(
        expected_project_instance_slugs - mapped_project_instance_slugs
    )
    if missing_project_instance_mappings:
        fail(
            f"Project type {project_type_id} is missing projectTaskMappings for "
            f"{missing_project_instance_mappings}"
        )

    for slug in expected_project_instance_slugs:
        for field_key, field in task_contracts[slug]["fields"]["output"].items():
            if (
                field.get("fieldType") == "json"
                and field_key != PROJECT_CREATION_COMPLETION_OUTPUT_KEY
            ):
                fail(
                    f"Project type {project_type_id} task {slug} output {field_key} "
                    "must be a file artifact or compact scalar, not json"
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
    plugin_paths = plugin_manifest_paths()
    for path in plugin_paths:
        validate_plugin_manifest(path)
    read_json(ROOT / ".mcp.json")

    manifest = read_yaml(ROOT / "alludium" / "manifest.yaml")
    if not isinstance(manifest, dict):
        fail("alludium/manifest.yaml must be an object")
    if manifest.get("boundaries", {}).get("secretsAllowed") is not False:
        fail("Manifest must declare boundaries.secretsAllowed: false")
    pack_version = manifest.get("pack", {}).get("version")
    if not isinstance(pack_version, str) or not pack_version:
        fail("Manifest must declare pack.version")
    validate_plugin_manifest_versions(pack_version, plugin_paths)

    skill_ids = validate_skills(manifest)
    validate_templates(manifest, skill_ids)
    agent_template_ids = set(manifest["surfaces"]["alludiumAgentTemplates"]["ids"])
    project_type_ids = validate_project_types(manifest)
    document_ids_by_project_type, document_types_by_id = validate_documents(manifest, project_type_ids)
    validate_project_type_document_references(manifest, document_ids_by_project_type)
    document_ids = set(manifest["surfaces"]["documents"]["ids"])
    validate_task_definition_templates(
        manifest,
        skill_ids,
        agent_template_ids,
        project_type_ids,
        document_ids,
        document_types_by_id,
    )
    validate_project_task_mapping_contracts()
    validate_origination_pipeline_task_mapping_contracts()
    recommendations_path = manifest["surfaces"]["alludiumMcpRecommendations"]["path"]
    if not (ROOT / recommendations_path).exists():
        fail(f"Missing Alludium MCP recommendations file: {recommendations_path}")
    recommendations = read_yaml(ROOT / recommendations_path)
    if not isinstance(recommendations, dict):
        fail(f"{recommendations_path} must be an object")
    validate_mcp_definitions(manifest, recommendations)
    validate_workspace_variables(manifest, project_type_ids)
    validate_application_recommendations(manifest, recommendations, project_type_ids)
    validate_recommendation_management_actions(
        recommendations,
        set(manifest["surfaces"]["taskDefinitionTemplates"]["ids"]),
        skill_ids,
    )
    validate_no_obvious_secrets()
    validate_no_public_readiness_leakage()

    print(
        "Validated vc pack: "
        f"{len(skill_ids)} skills, "
        f"{len(manifest['surfaces']['alludiumAgentTemplates']['ids'])} agent templates, "
        f"{len(manifest['surfaces']['taskDefinitionTemplates']['ids'])} task definition templates, "
        f"{len(project_type_ids)} project types, "
        f"{len(manifest['surfaces']['documents']['ids'])} documents"
    )


if __name__ == "__main__":
    main()
