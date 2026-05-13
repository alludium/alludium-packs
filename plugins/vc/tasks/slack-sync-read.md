---
id: vc.slack_sync_read
title: Preview Slack Deal Context
slug: slack-sync-read
agent: vc-pipeline-autopilot
skills:
- vc-slack-sync-read
- citation-enforcement
---

# Preview Slack Deal Context

Preview selected Slack channel, thread, message, and file context for VC Deal Room tasks.

## Instructions

Use `slack_v2-find-message`, `slack_v2-list-replies`, `slack_v2-list-files`, and `slack_v2-get-file` only inside the approved channel/thread scope. Summarize selected context and propose whether it belongs as knowledge context, artifact context, task context, or setup context.

## Missing Input Policy

Ask for approved channel/thread scope before reading Slack messages.

## External Action Policy

Read preview only. Do not ingest broad history, post, reply, delete, or update messages.

## Completion Criteria

- Message/thread IDs and channel IDs are listed.
- Relevant context is summarized with timestamps and sensitivity caveats.
- Broad channel ingestion remains out of scope.

## Human Decision Points

- Approve selected context before attaching it to project/task state.

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `selected_slack_scope` | Selected Slack Scope | `json` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `slack_context_preview` | Slack Context Preview | `richtext` | no |
| `target_context_mapping` | Target Context Mapping | `json` | no |

## Routing

- Source template: `alludium/task-definition-templates/vc-integrations/slack-sync-read.yaml`
- Alludium task ID: `vc.slack_sync_read`
- Task family: `integration_sync_read`
- Recommended agent: `vc-pipeline-autopilot` (Alludium template `vc_pipeline_autopilot`)
- Supported project types:
  - `vc_deal_room`
- Supported project scopes:
  - `project_management`

## Required Skills

- `vc-slack-sync-read`
- `citation-enforcement`

## Planned Skills

- `vc-slack-sync-read`
- `citation-enforcement`
