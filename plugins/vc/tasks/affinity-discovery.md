---
id: vc.affinity_discovery
title: Explore Affinity Lists and Stages
slug: affinity-discovery
agent: vc-pipeline-autopilot
skills:
- vc-affinity-discovery
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-integrations/affinity-discovery.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Explore Affinity Lists and Stages

Discover Affinity list, stage, field, and object-count scope before VC Deal Room import or sync.

## Instructions

Use the connected `affinity-mcp-server` application to enumerate Affinity lists, stages/status fields, key CRM fields, and object counts. Expected tools include `affinity_list_opportunities`, `affinity_get_opportunity`, `affinity_get_list_entries`, `affinity_get_field_values`, and `affinity_get_field_value_changes` when discovered. Ask the user to choose the list/source and active stages before any import or sync-read task.

## Missing Input Policy

If Affinity has no authorized connection or no discovered tools, report the setup gap and ask for connection authorization or an exported snapshot.

## External Action Policy

Read-only discovery. Do not import, sync, update CRM fields, write notes, move stages, or create tasks.

## Completion Criteria

- Candidate Affinity lists/sources and stages are listed with counts when available.
- The report names the Affinity tool IDs used or missing.
- User choices needed before import are explicit.

## Human Decision Points

- Choose the Affinity list/source scope.
- Choose which stages count as active pipeline.
- Approve any later import or recurring sync separately.

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `discovery_goal` | Discovery Goal | `string` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `affinity_discovery_report` | Affinity Discovery Report | `richtext` | no |
| `scope_questions` | Scope Questions | `json` | no |

## Routing

- Source template: `alludium/task-definition-templates/vc-integrations/affinity-discovery.yaml`
- Alludium task ID: `vc.affinity_discovery`
- Task family: `integration_discovery`
- Recommended agent: `vc-pipeline-autopilot` (Alludium template `vc_pipeline_autopilot`)
- Supported project types:
  - `vc_deal_room`
- Supported project scopes:
  - `project_management`

## Required Skills

- `vc-affinity-discovery`
- `citation-enforcement`

## Planned Skills

- `vc-affinity-discovery`
- `citation-enforcement`
