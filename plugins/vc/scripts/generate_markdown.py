#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml


THIS_FILE = Path(__file__).resolve()
PACK_ROOT = THIS_FILE.parents[1]
AGENT_TEMPLATE_ROOT = PACK_ROOT / "alludium" / "agent-templates"
TASK_TEMPLATE_ROOT = PACK_ROOT / "alludium" / "task-definition-templates"
PROJECT_TYPE_ROOT = PACK_ROOT / "alludium" / "project-types"
AGENT_OUTPUT_ROOT = PACK_ROOT / "agents"
TASK_OUTPUT_ROOT = PACK_ROOT / "tasks"
BLUEPRINT_OUTPUT_ROOT = PACK_ROOT / "project-blueprints"
MANIFEST_PATH = PACK_ROOT / "alludium" / "manifest.yaml"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def read_yaml(path: Path) -> dict[str, Any]:
    try:
        parsed = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - defensive CLI guard
        fail(f"Failed to parse YAML {path.relative_to(PACK_ROOT)}: {exc}")
    if not isinstance(parsed, dict):
        fail(f"{path.relative_to(PACK_ROOT)} must be a YAML object")
    return parsed


def read_json(path: Path) -> dict[str, Any]:
    try:
        parsed = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - defensive CLI guard
        fail(f"Failed to parse JSON {path.relative_to(PACK_ROOT)}: {exc}")
    if not isinstance(parsed, dict):
        fail(f"{path.relative_to(PACK_ROOT)} must be a JSON object")
    return parsed


def yaml_frontmatter(data: dict[str, Any]) -> str:
    dumped = yaml.safe_dump(
        data,
        allow_unicode=False,
        default_flow_style=False,
        sort_keys=False,
        width=120,
    ).strip()
    return f"---\n{dumped}\n---\n\n"


def generated_notice(source_path: Path) -> str:
    return (
        "> **GENERATED FILE**\n"
        f"> Source: `{source_path.relative_to(PACK_ROOT)}`\n"
        "> Do not edit directly. Change the YAML source and run "
        "`python plugins/vc/scripts/generate_markdown.py`.\n\n"
    )


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if not slug:
        fail(f"Cannot derive slug from {value!r}")
    return slug


def require_string(value: Any, context: str) -> str:
    if not isinstance(value, str) or not value.strip():
        fail(f"{context} must be a non-empty string")
    return value


def require_mapping(value: Any, context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        fail(f"{context} must be an object")
    return value


def optional_string(value: Any, fallback: str) -> str:
    if isinstance(value, str) and value.strip():
        return value
    return fallback


def string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str) and item]


def bullet_list(values: list[str]) -> str:
    if not values:
        return "- None declared\n"
    return "".join(f"- `{value}`\n" for value in values)


def plain_bullet_list(values: list[str]) -> str:
    if not values:
        return "- None declared\n"
    return "".join(f"- {value}\n" for value in values)


def markdown_escape(value: Any) -> str:
    text = str(value) if value is not None else ""
    return text.replace("|", "\\|").replace("\n", " ").strip()


def title_from_key(value: str) -> str:
    return value.replace("_", " ").replace("-", " ").title()


def field_table(fields: list[dict[str, Any]]) -> str:
    if not fields:
        return "None declared.\n"
    lines = ["| Key | Name | Type | Required |", "| --- | --- | --- | --- |"]
    for field in fields:
        key = field.get("key", "")
        name = field.get("name", "")
        field_type = field.get("fieldType", "")
        required = "yes" if field.get("required") is True else "no"
        lines.append(f"| `{key}` | {name} | `{field_type}` | {required} |")
    return "\n".join(lines) + "\n"


def task_link(slug: str, title: str | None = None) -> str:
    label = markdown_escape(title or title_from_key(slug))
    return f"[{label}](../tasks/{slug}.md)"


def agent_link(agent_id: str | None, agent_names: dict[str, str]) -> str:
    if not agent_id:
        return "None declared"
    label = markdown_escape(agent_names.get(agent_id, title_from_key(agent_id)))
    return f"[{label}](../agents/{slugify(agent_id)}.md)"


def skill_links(skills: list[str]) -> str:
    if not skills:
        return "None declared"
    return "<br>".join(
        f"[`{markdown_escape(skill)}`](../skills/{skill}/SKILL.md)" for skill in skills
    )


def action_list(actions: list[dict[str, Any]]) -> str:
    if not actions:
        return "- None declared\n"
    lines: list[str] = []
    for action in actions:
        title = action.get("Title") or action.get("title") or "Untitled action"
        message = action.get("Message") or action.get("message") or ""
        if message:
            lines.append(f"- **{title}**: {message}\n")
        else:
            lines.append(f"- **{title}**\n")
    return "".join(lines)


def document_ref_list(refs: Any) -> str:
    if not isinstance(refs, list) or not refs:
        return "- None declared\n"
    lines: list[str] = []
    for ref in refs:
        if not isinstance(ref, dict):
            continue
        document_id = ref.get("documentId")
        usage = ref.get("usage")
        if not isinstance(document_id, str) or not document_id:
            continue
        suffix = ""
        if isinstance(usage, str) and usage:
            suffix += f" ({usage})"
        output_field_key = ref.get("outputFieldKey")
        if isinstance(output_field_key, str) and output_field_key:
            suffix += f" -> `{output_field_key}`"
        lines.append(f"- `{document_id}`{suffix}\n")
    return "".join(lines) if lines else "- None declared\n"


def skill_ids_from_agent(template: dict[str, Any]) -> list[str]:
    skills = template.get("skills")
    if not isinstance(skills, list):
        return []
    ids: list[str] = []
    for skill in skills:
        if isinstance(skill, dict) and isinstance(skill.get("externalId"), str):
            ids.append(skill["externalId"])
    return ids


def skill_lines_with_activation(template: dict[str, Any]) -> str:
    skills = template.get("skills")
    if not isinstance(skills, list):
        return "- None declared\n"
    lines: list[str] = []
    for skill in skills:
        if not isinstance(skill, dict):
            continue
        external_id = skill.get("externalId")
        activation = skill.get("activationMode")
        if isinstance(external_id, str) and isinstance(activation, str):
            lines.append(f"- `{external_id}` ({activation})\n")
        elif isinstance(external_id, str):
            lines.append(f"- `{external_id}`\n")
    return "".join(lines) if lines else "- None declared\n"


def mcp_lines(template: dict[str, Any]) -> str:
    servers = template.get("mcpServers")
    if not isinstance(servers, dict):
        return "- None declared\n"
    lines: list[str] = []
    for server_name, server in servers.items():
        tools: list[str] = []
        if isinstance(server, dict) and isinstance(server.get("tools"), list):
            for tool in server["tools"]:
                if isinstance(tool, dict) and isinstance(tool.get("name"), str):
                    tools.append(tool["name"])
        tool_text = ", ".join(f"`{tool}`" for tool in tools)
        lines.append(f"- `{server_name}`")
        if tool_text:
            lines[-1] += f": {tool_text}"
        lines[-1] += "\n"
    return "".join(lines)


def model_alias(llm: Any) -> str | None:
    if not isinstance(llm, dict):
        return None
    model = llm.get("model")
    if not isinstance(model, str):
        return None
    normalized = model.lower()
    if "opus" in normalized:
        return "opus"
    if "sonnet" in normalized:
        return "sonnet"
    if "haiku" in normalized:
        return "haiku"
    return None


def render_agent(path: Path) -> tuple[Path, str]:
    template = read_yaml(path)
    source_id = require_string(template.get("id"), f"{path.name}.id")
    name = require_string(template.get("name"), f"{path.name}.name")
    description = require_string(template.get("description"), f"{path.name}.description")
    prompt = template.get("prompt")
    if not isinstance(prompt, dict):
        fail(f"{path.relative_to(PACK_ROOT)} prompt must be an object")
    prompt_template = require_string(prompt.get("template"), f"{path.name}.prompt.template")
    agent_name = slugify(source_id)

    frontmatter: dict[str, Any] = {
        "name": agent_name,
        "description": description,
    }
    alias = model_alias(template.get("llm"))
    if alias is not None:
        frontmatter["model"] = alias
    skills = skill_ids_from_agent(template)
    if skills:
        frontmatter["skills"] = skills

    metadata = template.get("metadata") if isinstance(template.get("metadata"), dict) else {}
    variables = prompt.get("variables") if isinstance(prompt.get("variables"), list) else []
    actions = template.get("actions") if isinstance(template.get("actions"), list) else []
    greeting = template.get("greeting") if isinstance(template.get("greeting"), str) else ""

    body = yaml_frontmatter(frontmatter)
    body += generated_notice(path)
    body += prompt_template.strip() + "\n\n"
    body += "## Alludium Source\n\n"
    body += f"- Source template: `alludium/agent-templates/{path.name}`\n"
    body += f"- Alludium template ID: `{source_id}`\n"
    body += f"- Display name: {name}\n"
    body += f"- Version: `{template.get('version', 'unknown')}`\n"
    if isinstance(metadata.get("primaryStage"), str):
        body += f"- Primary stage: {metadata['primaryStage']}\n"
    if isinstance(metadata.get("primaryDealRoomState"), str):
        body += f"- Primary Deal Room state: `{metadata['primaryDealRoomState']}`\n"
    supported_tasks = string_list(metadata.get("supportedTaskDefinitions"))
    if supported_tasks:
        body += "- Supported task definitions:\n"
        body += "".join(f"  - `{task}`\n" for task in supported_tasks)
    installed_tasks = string_list(metadata.get("installedTaskTemplateIds"))
    if installed_tasks:
        body += "- Installed task templates:\n"
        body += "".join(f"  - `{task}`\n" for task in installed_tasks)

    body += "\n## Skills\n\n"
    body += skill_lines_with_activation(template)
    body += "\n## MCP And Tool Context\n\n"
    body += mcp_lines(template)
    body += "\n## Suggested Actions\n\n"
    body += action_list(actions)

    if variables:
        body += "\n## Prompt Variables\n\n"
        for variable in variables:
            if not isinstance(variable, dict):
                continue
            key = variable.get("key")
            if not isinstance(key, str):
                continue
            label = variable.get("label") if isinstance(variable.get("label"), str) else key
            body += f"- `{key}`: {label}"
            binding = variable.get("binding")
            if isinstance(binding, dict) and isinstance(binding.get("path"), str):
                body += f" (workspace binding `{binding['path']}`)"
            body += "\n"

    if greeting.strip():
        body += "\n## Greeting\n\n"
        body += greeting.strip() + "\n"

    return AGENT_OUTPUT_ROOT / f"{agent_name}.md", body


def render_task(path: Path) -> tuple[Path, str]:
    template = read_yaml(path)
    template_id = require_string(template.get("id"), f"{path.name}.id")
    title = require_string(template.get("title"), f"{path.name}.title")
    definition = template.get("definition")
    if not isinstance(definition, dict):
        fail(f"{path.relative_to(PACK_ROOT)} definition must be an object")
    slug = require_string(definition.get("slug"), f"{path.name}.definition.slug")
    description = require_string(definition.get("description"), f"{path.name}.definition.description")
    definition_json = definition.get("definitionJson")
    if not isinstance(definition_json, dict):
        fail(f"{path.relative_to(PACK_ROOT)} definition.definitionJson must be an object")
    instructions = definition_json.get("instructions")
    if not isinstance(instructions, dict):
        fail(f"{path.relative_to(PACK_ROOT)} definition.definitionJson.instructions must be an object")

    execution = require_string(instructions.get("executionInstructions"), f"{path.name}.executionInstructions")
    missing_input = optional_string(
        instructions.get("missingInputPolicy"),
        "No separate missing-input policy is declared. Follow the execution instructions and ask only when needed.",
    )
    external_action = optional_string(
        instructions.get("externalActionPolicy"),
        "No separate external-action policy is declared. Do not take external or persistent actions unless the task instructions explicitly allow them.",
    )
    completion = instructions.get("completionCriteria")
    if not isinstance(completion, list):
        fail(f"{path.relative_to(PACK_ROOT)} completionCriteria must be a list")

    fields = template.get("fields") if isinstance(template.get("fields"), dict) else {}
    input_fields = fields.get("input") if isinstance(fields.get("input"), list) else []
    context_fields = fields.get("context") if isinstance(fields.get("context"), list) else []
    output_fields = fields.get("output") if isinstance(fields.get("output"), list) else []
    input_dicts = [field for field in input_fields if isinstance(field, dict)]
    context_dicts = [field for field in context_fields if isinstance(field, dict)]
    output_dicts = [field for field in output_fields if isinstance(field, dict)]

    recommended_agent = definition_json.get("recommendedAgentTemplate")
    recommended_agent_name = slugify(recommended_agent) if isinstance(recommended_agent, str) else None
    planned_agent = definition_json.get("plannedRecommendedAgentTemplate")
    planned_agent_name = slugify(planned_agent) if isinstance(planned_agent, str) else None
    required_skills = string_list(definition_json.get("requiredSkills"))
    planned_skills = string_list(definition_json.get("plannedRequiredSkills"))
    human_decisions = string_list(definition_json.get("humanDecisionPoints"))
    project_types = string_list(definition_json.get("supportedProjectTypes"))
    project_scopes = string_list(definition_json.get("supportedProjectScopes"))

    frontmatter: dict[str, Any] = {
        "id": template_id,
        "title": title,
        "slug": slug,
    }
    if recommended_agent_name is not None:
        frontmatter["agent"] = recommended_agent_name
    if required_skills:
        frontmatter["skills"] = required_skills

    body = yaml_frontmatter(frontmatter)
    body += generated_notice(path)
    body += f"# {title}\n\n"
    body += f"{description}\n\n"
    body += "## Instructions\n\n"
    body += execution.strip() + "\n\n"
    body += "## Missing Input Policy\n\n"
    body += missing_input.strip() + "\n\n"
    body += "## External Action Policy\n\n"
    body += external_action.strip() + "\n\n"
    body += "## Completion Criteria\n\n"
    body += plain_bullet_list([str(item) for item in completion if isinstance(item, str)])
    body += "\n## Human Decision Points\n\n"
    body += plain_bullet_list(human_decisions)
    body += "\n## Inputs\n\n"
    body += field_table(input_dicts)
    if context_dicts:
        body += "\n## Context Fields\n\n"
        body += field_table(context_dicts)
    body += "\n## Outputs\n\n"
    body += field_table(output_dicts)
    document_refs = definition_json.get("documentRefs")
    if isinstance(document_refs, list) and document_refs:
        body += "\n## Document References\n\n"
        body += document_ref_list(document_refs)
    body += "\n## Routing\n\n"
    body += f"- Source template: `alludium/task-definition-templates/{path.relative_to(TASK_TEMPLATE_ROOT)}`\n"
    body += f"- Alludium task ID: `{template_id}`\n"
    body += f"- Task family: `{definition_json.get('taskFamily', 'unknown')}`\n"
    if isinstance(definition_json.get("stage"), str):
        body += f"- Lifecycle stage: `{definition_json['stage']}`\n"
    if recommended_agent_name is not None:
        body += f"- Recommended agent: `{recommended_agent_name}`"
        if isinstance(recommended_agent, str):
            body += f" (Alludium template `{recommended_agent}`)"
        body += "\n"
    if planned_agent_name is not None and planned_agent_name != recommended_agent_name:
        body += f"- Planned recommended agent: `{planned_agent_name}`"
        if isinstance(planned_agent, str):
            body += f" (Alludium template `{planned_agent}`)"
        body += "\n"
    body += "- Supported project types:\n"
    body += "".join(f"  - `{value}`\n" for value in project_types) if project_types else "  - None declared\n"
    if project_scopes:
        body += "- Supported project scopes:\n"
        body += "".join(f"  - `{value}`\n" for value in project_scopes)
    body += "\n## Required Skills\n\n"
    body += bullet_list(required_skills)
    if planned_skills:
        body += "\n## Planned Skills\n\n"
        body += bullet_list(planned_skills)

    methodology_skills = definition_json.get("workspaceConfiguredMethodologySkills")
    if isinstance(methodology_skills, list) and methodology_skills:
        body += "\n## Workspace-Configured Methodology Skills\n\n"
        for skill in methodology_skills:
            if isinstance(skill, dict) and isinstance(skill.get("skill"), str):
                note = skill.get("note")
                body += f"- `{skill['skill']}`"
                if isinstance(note, str) and note:
                    body += f": {note}"
                body += "\n"
            elif isinstance(skill, str):
                body += f"- `{skill}`\n"

    return TASK_OUTPUT_ROOT / f"{slug}.md", body


def load_task_templates() -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    by_slug: dict[str, dict[str, Any]] = {}
    by_id: dict[str, dict[str, Any]] = {}
    for path in sorted(TASK_TEMPLATE_ROOT.glob("*/*.yaml")):
        template = read_yaml(path)
        template_id = require_string(template.get("id"), f"{path.relative_to(PACK_ROOT)}.id")
        definition = require_mapping(template.get("definition"), f"{path.relative_to(PACK_ROOT)}.definition")
        slug = require_string(definition.get("slug"), f"{path.relative_to(PACK_ROOT)}.definition.slug")
        entry = {
            "path": path,
            "id": template_id,
            "slug": slug,
            "title": require_string(template.get("title"), f"{path.relative_to(PACK_ROOT)}.title"),
            "definitionJson": require_mapping(
                definition.get("definitionJson"),
                f"{path.relative_to(PACK_ROOT)}.definition.definitionJson",
            ),
        }
        if slug in by_slug:
            fail(f"Duplicate task definition slug in YAML: {slug}")
        if template_id in by_id:
            fail(f"Duplicate task definition ID in YAML: {template_id}")
        by_slug[slug] = entry
        by_id[template_id] = entry
    return by_slug, by_id


def load_agent_names() -> dict[str, str]:
    names: dict[str, str] = {}
    for path in sorted(AGENT_TEMPLATE_ROOT.glob("*.yaml")):
        template = read_yaml(path)
        agent_id = require_string(template.get("id"), f"{path.relative_to(PACK_ROOT)}.id")
        names[agent_id] = require_string(template.get("name"), f"{path.relative_to(PACK_ROOT)}.name")
    return names


def blueprint_task_row(
    slug: str,
    task_by_slug: dict[str, dict[str, Any]],
    agent_names: dict[str, str],
    fallback_agent_id: str | None = None,
) -> str:
    task = task_by_slug.get(slug)
    if task is None:
        return (
            f"| `{markdown_escape(slug)}` | {agent_link(fallback_agent_id, agent_names)} | "
            "None declared | Pack task not found; likely platform-owned setup task. |\n"
        )
    definition_json = task["definitionJson"]
    agent_id = definition_json.get("recommendedAgentTemplate")
    if not isinstance(agent_id, str):
        agent_id = definition_json.get("plannedRecommendedAgentTemplate")
    if not isinstance(agent_id, str):
        agent_id = fallback_agent_id
    skills = string_list(definition_json.get("requiredSkills"))
    return (
        f"| {task_link(slug, task['title'])} | {agent_link(agent_id, agent_names)} | "
        f"{skill_links(skills)} | `{markdown_escape(task['id'])}` |\n"
    )


def collect_setup_task_slugs(project_type: dict[str, Any]) -> list[tuple[str, str | None]]:
    setup = project_type.get("projectSetup")
    if not isinstance(setup, dict):
        return []
    fallback_agent = setup.get("recommendedSetupAgent")
    if not isinstance(fallback_agent, str):
        fallback_agent = None

    collected: list[tuple[str, str | None]] = []

    def add_slug(value: Any, agent_id: str | None = fallback_agent) -> None:
        if isinstance(value, str) and value and (value, agent_id) not in collected:
            collected.append((value, agent_id))

    for step in setup.get("setupSteps", []):
        if isinstance(step, dict):
            add_slug(step.get("taskDefinitionSlug"))

    for key in ["defaultChildTask", "variableDiscoveryTask"]:
        item = setup.get(key)
        if isinstance(item, dict):
            add_slug(item.get("taskDefinitionSlug"))

    for task in setup.get("sourceSetupTasks", []):
        if isinstance(task, dict):
            add_slug(task.get("taskDefinitionSlug"))

    for group in setup.get("scheduleGroups", []):
        if not isinstance(group, dict):
            continue
        slugs = group.get("taskDefinitionSlugs")
        if isinstance(slugs, list):
            for slug in slugs:
                add_slug(slug, None)

    return collected


def render_blueprint(
    project_type_path: Path,
    task_by_slug: dict[str, dict[str, Any]],
    agent_names: dict[str, str],
) -> tuple[Path, str]:
    project_type = read_json(project_type_path)
    project_key = require_string(project_type.get("key"), f"{project_type_path.name}.key")
    project_name = require_string(project_type.get("name"), f"{project_type_path.name}.name")
    description = require_string(project_type.get("description"), f"{project_type_path.name}.description")
    initial_version = require_mapping(project_type.get("initialVersion"), f"{project_type_path.name}.initialVersion")

    frontmatter = {
        "projectType": project_key,
        "title": f"{project_name} Blueprint",
        "source": str(project_type_path.relative_to(PACK_ROOT)),
    }
    body = yaml_frontmatter(frontmatter)
    body += generated_notice(project_type_path)
    body += f"# {project_name} Blueprint\n\n"
    body += f"{description}\n\n"
    body += "This blueprint lists the project stages, mapped tasks, recommended agents, and task-referenced skills for this project type.\n\n"
    body += "## Project Setup / General\n\n"
    body += "| Task | Agent | Skills | Task ID |\n| --- | --- | --- | --- |\n"
    setup_rows = [
        blueprint_task_row(slug, task_by_slug, agent_names, fallback_agent)
        for slug, fallback_agent in collect_setup_task_slugs(project_type)
    ]
    body += "".join(setup_rows) if setup_rows else "| None mapped | None declared | None declared |  |\n"

    mappings = initial_version.get("projectTaskMappings")
    if not isinstance(mappings, list):
        mappings = []
    mappings_by_stage: dict[str, list[str]] = {}
    for mapping in mappings:
        if not isinstance(mapping, dict):
            continue
        slug = mapping.get("taskDefinitionSlug")
        if not isinstance(slug, str) or not slug:
            continue
        stage = mapping.get("lifecycleStage")
        if not isinstance(stage, str) or not stage:
            task = task_by_slug.get(slug)
            definition_json = task.get("definitionJson") if isinstance(task, dict) else {}
            stage = definition_json.get("stage") if isinstance(definition_json, dict) else None
        if not isinstance(stage, str) or not stage:
            stage = "general"
        mappings_by_stage.setdefault(stage, []).append(slug)

    lifecycle_states = initial_version.get("lifecycleStates")
    stage_order = [state for state in lifecycle_states if isinstance(state, str)] if isinstance(lifecycle_states, list) else []
    for stage in sorted(mappings_by_stage):
        if stage not in stage_order and stage != "general":
            stage_order.append(stage)
    if "general" in mappings_by_stage:
        stage_order.insert(0, "general")

    for stage in stage_order:
        body += f"\n## {title_from_key(stage)}\n\n"
        body += "| Task | Agent | Skills | Task ID |\n| --- | --- | --- | --- |\n"
        rows = [
            blueprint_task_row(slug, task_by_slug, agent_names)
            for slug in mappings_by_stage.get(stage, [])
        ]
        body += "".join(rows) if rows else "| None mapped | None declared | None declared |  |\n"

    return BLUEPRINT_OUTPUT_ROOT / f"{slugify(project_key)}.md", body


def read_manifest() -> dict[str, Any]:
    return read_yaml(MANIFEST_PATH)


def add_expected_output(
    outputs: dict[Path, str],
    sources: dict[Path, Path],
    output_path: Path,
    body: str,
    source_path: Path,
) -> None:
    existing_source = sources.get(output_path)
    if existing_source is not None:
        fail(
            "Generated Markdown filename collision: "
            f"{source_path.relative_to(PACK_ROOT)} and "
            f"{existing_source.relative_to(PACK_ROOT)} both map to "
            f"{output_path.relative_to(PACK_ROOT)}"
        )
    outputs[output_path] = body
    sources[output_path] = source_path


def expected_outputs() -> dict[Path, str]:
    manifest = read_manifest()
    surfaces = require_mapping(manifest.get("surfaces"), "alludium/manifest.yaml surfaces")
    agent_templates_surface = require_mapping(
        surfaces.get("alludiumAgentTemplates"),
        "alludium/manifest.yaml surfaces.alludiumAgentTemplates",
    )
    task_templates_surface = require_mapping(
        surfaces.get("taskDefinitionTemplates"),
        "alludium/manifest.yaml surfaces.taskDefinitionTemplates",
    )
    project_types_surface = require_mapping(
        surfaces.get("projectTypes"),
        "alludium/manifest.yaml surfaces.projectTypes",
    )
    agent_template_ids = agent_templates_surface.get("ids")
    if not isinstance(agent_template_ids, list):
        fail("alludium/manifest.yaml surfaces.alludiumAgentTemplates.ids must be a list")
    task_template_ids = task_templates_surface.get("ids")
    if not isinstance(task_template_ids, list):
        fail("alludium/manifest.yaml surfaces.taskDefinitionTemplates.ids must be a list")
    project_type_ids = project_types_surface.get("ids")
    if not isinstance(project_type_ids, list):
        fail("alludium/manifest.yaml surfaces.projectTypes.ids must be a list")

    outputs: dict[Path, str] = {}
    sources: dict[Path, Path] = {}

    discovered_agent_paths = {path.name for path in AGENT_TEMPLATE_ROOT.glob("*.yaml")}
    declared_agent_paths: set[str] = set()
    for template_id in agent_template_ids:
        if not isinstance(template_id, str) or not template_id:
            fail("alludium/manifest.yaml agent template IDs must be non-empty strings")
        declared_agent_paths.add(f"{template_id}.yaml")
        path = AGENT_TEMPLATE_ROOT / f"{template_id}.yaml"
        if not path.exists():
            fail(f"Manifest agent template missing YAML: {template_id}")
        output_path, body = render_agent(path)
        add_expected_output(outputs, sources, output_path, body, path)

    extra_agent_paths = sorted(discovered_agent_paths - declared_agent_paths)
    if extra_agent_paths:
        fail(f"Agent template YAML present on disk but missing from manifest: {extra_agent_paths}")

    discovered_task_paths_by_id: dict[str, Path] = {}
    for path in sorted(TASK_TEMPLATE_ROOT.glob("*/*.yaml")):
        template = read_yaml(path)
        template_id = require_string(template.get("id"), f"{path.relative_to(PACK_ROOT)}.id")
        if template_id in discovered_task_paths_by_id:
            fail(
                "Duplicate task template ID in YAML: "
                f"{template_id} appears in "
                f"{discovered_task_paths_by_id[template_id].relative_to(PACK_ROOT)} and "
                f"{path.relative_to(PACK_ROOT)}"
            )
        discovered_task_paths_by_id[template_id] = path

    declared_task_ids: set[str] = set()
    for template_id in task_template_ids:
        if not isinstance(template_id, str) or not template_id:
            fail("alludium/manifest.yaml task template IDs must be non-empty strings")
        declared_task_ids.add(template_id)
        path = discovered_task_paths_by_id.get(template_id)
        if path is None:
            fail(f"Manifest task template missing YAML: {template_id}")
        output_path, body = render_task(path)
        add_expected_output(outputs, sources, output_path, body, path)

    extra_task_ids = sorted(set(discovered_task_paths_by_id) - declared_task_ids)
    if extra_task_ids:
        fail(f"Task template YAML present on disk but missing from manifest: {extra_task_ids}")

    task_by_slug, _task_by_id = load_task_templates()
    agent_names = load_agent_names()
    discovered_project_paths = {
        path.name for path in PROJECT_TYPE_ROOT.glob("*.json") if path.name != "catalog.v1.json"
    }
    declared_project_paths: set[str] = set()
    for project_type_id in project_type_ids:
        if not isinstance(project_type_id, str) or not project_type_id:
            fail("alludium/manifest.yaml project type IDs must be non-empty strings")
        declared_project_paths.add(f"{project_type_id}.json")
        path = PROJECT_TYPE_ROOT / f"{project_type_id}.json"
        if not path.exists():
            fail(f"Manifest project type missing JSON: {project_type_id}")
        output_path, body = render_blueprint(path, task_by_slug, agent_names)
        add_expected_output(outputs, sources, output_path, body, path)

    extra_project_paths = sorted(discovered_project_paths - declared_project_paths)
    if extra_project_paths:
        fail(f"Project type JSON present on disk but missing from manifest: {extra_project_paths}")

    return outputs


def write_outputs(outputs: dict[Path, str]) -> None:
    for directory in [AGENT_OUTPUT_ROOT, TASK_OUTPUT_ROOT, BLUEPRINT_OUTPUT_ROOT]:
        directory.mkdir(parents=True, exist_ok=True)
    expected_paths = set(outputs)
    actual_paths = (
        set(AGENT_OUTPUT_ROOT.glob("*.md"))
        | set(TASK_OUTPUT_ROOT.glob("*.md"))
        | set(BLUEPRINT_OUTPUT_ROOT.glob("*.md"))
    )
    for path in sorted(actual_paths - expected_paths):
        path.unlink()
    for path, body in outputs.items():
        path.write_text(body, encoding="utf-8")


def check_outputs(outputs: dict[Path, str]) -> None:
    failures: list[str] = []
    expected_paths = set(outputs)
    actual_paths = (
        set(AGENT_OUTPUT_ROOT.glob("*.md"))
        | set(TASK_OUTPUT_ROOT.glob("*.md"))
        | set(BLUEPRINT_OUTPUT_ROOT.glob("*.md"))
    )
    for path in sorted(expected_paths):
        if not path.exists():
            failures.append(f"Missing generated file: {path.relative_to(PACK_ROOT)}")
            continue
        current = path.read_text(encoding="utf-8")
        if current != outputs[path]:
            failures.append(f"Stale generated file: {path.relative_to(PACK_ROOT)}")
    for path in sorted(actual_paths - expected_paths):
        failures.append(f"Unexpected generated file: {path.relative_to(PACK_ROOT)}")
    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        fail("Generated Markdown is stale. Run python plugins/vc/scripts/generate_markdown.py")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate plugin Markdown from Alludium YAML surfaces.")
    parser.add_argument("--check", action="store_true", help="Verify generated Markdown is up to date.")
    args = parser.parse_args()

    outputs = expected_outputs()
    if args.check:
        check_outputs(outputs)
        print(f"Generated Markdown is up to date: {len(outputs)} files")
        return

    write_outputs(outputs)
    print(
        "Generated Markdown: "
        f"{len(list(AGENT_TEMPLATE_ROOT.glob('*.yaml')))} agents, "
        f"{len(list(TASK_TEMPLATE_ROOT.glob('*/*.yaml')))} tasks, "
        f"{len([path for path in PROJECT_TYPE_ROOT.glob('*.json') if path.name != 'catalog.v1.json'])} project blueprints"
    )


if __name__ == "__main__":
    main()
