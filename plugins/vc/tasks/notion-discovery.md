---
id: vc.notion_discovery
title: Explore Notion Pages and Databases
slug: notion-discovery
agent: vc-pipeline-autopilot
skills:
- vc-notion-discovery
- citation-enforcement
---

# Explore Notion Pages and Databases

Discover Notion page, database, and workspace scope before selected VC Deal Room context reads.

## Instructions

Use the connected `notion` application to confirm account context with `notion-get-current-user`, search accessible pages and databases with `notion-search`, and inspect candidate database shape with `notion-retrieve-database-schema` when selected. Ask the user to choose the page or database scope before any read-sync task.

## Missing Input Policy

If Notion is not authorized, ask for authorization or a supplied page/database inventory.

## External Action Policy

Discovery only. Do not read broad page contents, create pages, create databases, update pages, update databases, append blocks, delete blocks, duplicate pages, upload files, or create comments.

## Completion Criteria

- Candidate pages, databases, owners, and scope signals are listed with IDs when available.
- Tool IDs used or missing are named.
- User choices needed before page or database preview are explicit.

## Human Decision Points

- Choose page or database scope before sync read.
- Approve whether properties, blocks, or database rows are in scope.
- Approve any later import or attachment separately.

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `discovery_goal` | Discovery Goal | `string` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `notion_discovery_report` | Notion Discovery Report | `richtext` | no |
| `scope_questions` | Scope Questions | `json` | no |

## Routing

- Source template: `alludium/task-definition-templates/vc-integrations/notion-discovery.yaml`
- Alludium task ID: `vc.notion_discovery`
- Task family: `integration_discovery`
- Recommended agent: `vc-pipeline-autopilot` (Alludium template `vc_pipeline_autopilot`)
- Supported project types:
  - `vc_deal_room`
- Supported project scopes:
  - `project_management`

## Required Skills

- `vc-notion-discovery`
- `citation-enforcement`

## Planned Skills

- `vc-notion-discovery`
- `citation-enforcement`
