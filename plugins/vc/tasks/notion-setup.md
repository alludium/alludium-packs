---
id: vc.notion_setup
title: Set Up Notion for VC Deal Rooms
slug: notion-setup
agent: vc-pipeline-autopilot
skills:
- vc-notion-discovery
- vc-notion-sync-read
- vc-notion-sync-write
- citation-enforcement
---

# Set Up Notion for VC Deal Rooms

Coordinate Notion connection readiness, page/database discovery, read-preview policy, and optional update-proposal scope for VC Deal Room setup.

## Instructions

Confirm that Notion is a selected workspace/document source, check connection readiness, then coordinate page/database discovery and reviewed read-preview setup. Create child tasks from the declared integrationSetup flow only when the user chooses that step. Keep database imports, recurring sync, page writes, and update proposals disabled unless a later human approval explicitly creates that task.

## Missing Input Policy

If Notion is not authorized or no page/database scope is selected, keep setup incomplete and ask for connection authorization, a supplied workspace map, or the source-scope decision needed for discovery.

## External Action Policy

Setup orchestration only. Do not import databases, write pages, change permissions, enable recurring sync, or create Deal Room projects from this setup task.

## Completion Criteria

- Connection readiness or missing-authorization evidence is recorded.
- Candidate page/database scope is complete or the unanswered scope questions are explicit.
- Read-preview and optional update-proposal policies are recorded without enabling external writes.
- The accepted connection scope states whether access is personal, project-shared, or workspace-shared.

## Human Decision Points

- Choose whether the Notion connection is personal, project-shared, or workspace-shared.
- Choose the page, database, or workspace scope.
- Approve any read-preview, import, recurring sync, or write task separately.

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `setup_goal` | Setup Goal | `string` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `setup_summary` | Setup Summary | `richtext` | no |
| `accepted_connection_scope` | Accepted Connection Scope | `string` | no |
| `child_task_plan` | Child Task Plan | `json` | no |
| `sync_policy` | Sync Policy | `json` | no |

## Routing

- Source template: `alludium/task-definition-templates/vc-integrations/notion-setup.yaml`
- Alludium task ID: `vc.notion_setup`
- Task family: `integration_setup`
- Recommended agent: `vc-pipeline-autopilot` (Alludium template `vc_pipeline_autopilot`)
- Supported project types:
  - `vc_deal_room`
- Supported project scopes:
  - `project_management`

## Required Skills

- `vc-notion-discovery`
- `vc-notion-sync-read`
- `vc-notion-sync-write`
- `citation-enforcement`

## Planned Skills

- `vc-notion-discovery`
- `vc-notion-sync-read`
- `vc-notion-sync-write`
- `citation-enforcement`
