---
id: vc.slack_setup
title: Set Up Slack for Deal Pipelines
slug: slack-setup
agent: vc-integration-operator
skills:
- vc-slack-discovery
- vc-slack-sync-read
- vc-slack-sync-write
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-integrations/slack-setup.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Set Up Slack for Deal Pipelines

Coordinate Slack connection readiness, channel discovery, read-preview policy, and optional notification proposal scope for Deal Pipeline setup.

## Instructions

Confirm that Slack is a selected collaboration source, check connection readiness, then coordinate workspace/channel discovery and reviewed read-preview setup. Create child tasks from the declared integrationSetup flow only when the user chooses that step. Keep message reads, posting, channel creation, recurring sync, and notification drafts disabled unless a later human approval explicitly creates that task.

## Missing Input Policy

If Slack is not authorized or no channel/thread scope is selected, keep setup incomplete and ask for connection authorization, a supplied channel list, or the source-scope decision needed for discovery.

## External Action Policy

Setup orchestration only. Do not read broad channel history, post messages, create channels, enable recurring sync, or create Deal Pipeline projects from this setup task.

## Completion Criteria

- Connection readiness or missing-authorization evidence is recorded.
- Candidate channel/thread scope is complete or the unanswered scope questions are explicit.
- Read-preview and optional notification-proposal policies are recorded without enabling external writes.
- The accepted connection scope states whether access is personal, project-shared, or workspace-shared.

## Human Decision Points

- Choose whether the Slack connection is personal, project-shared, or workspace-shared.
- Choose the workspace, channel, and thread scope.
- Approve any read-preview, notification, recurring sync, or post task separately.

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

- Source template: `alludium/task-definition-templates/vc-integrations/slack-setup.yaml`
- Alludium task ID: `vc.slack_setup`
- Task family: `integration_setup`
- Recommended agent: `vc-integration-operator` (Alludium template `vc_integration_operator`)
- Supported project types:
  - `vc_deal_room`
- Supported project scopes:
  - `project_management`

## Required Skills

- `vc-slack-discovery`
- `vc-slack-sync-read`
- `vc-slack-sync-write`
- `citation-enforcement`
