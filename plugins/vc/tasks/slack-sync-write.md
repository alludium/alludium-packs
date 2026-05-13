---
id: vc.slack_sync_write
title: Draft Slack Handoff Notifications
slug: slack-sync-write
agent: vc-pipeline-autopilot
skills:
- vc-slack-sync-write
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-integrations/slack-sync-write.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Draft Slack Handoff Notifications

Draft approved Slack handoff notifications for VC workflows without broad posting.

## Instructions

Draft Slack notification or handoff messages for an approved channel, user, or thread. Approved execution tools may include `slack_v2-send-message-to-channel`, `slack_v2-reply-to-a-message`, `slack_v2-send-block-kit-message`, or `slack_v2-send-message-to-user-or-group`, but this task must not send unless a later approved runtime path executes the tool.

## Missing Input Policy

Ask for the target, message purpose, source artifact, timing, and approver before drafting.

## External Action Policy

Draft only. Do not post, reply, create channels, archive channels, delete messages, update profiles, or administer Slack.

## Completion Criteria

- Draft includes target, body, source context, timing, and approver.
- Output states no Slack message was sent.

## Human Decision Points

- Approve exact message content and target before send.

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `handoff_source` | Handoff Source | `json` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `slack_handoff_draft` | Slack Handoff Draft | `richtext` | no |

## Routing

- Source template: `alludium/task-definition-templates/vc-integrations/slack-sync-write.yaml`
- Alludium task ID: `vc.slack_sync_write`
- Task family: `integration_sync_write`
- Recommended agent: `vc-pipeline-autopilot` (Alludium template `vc_pipeline_autopilot`)
- Supported project types:
  - `vc_deal_room`
- Supported project scopes:
  - `project_management`

## Required Skills

- `vc-slack-sync-write`
- `citation-enforcement`

## Planned Skills

- `vc-slack-sync-write`
- `citation-enforcement`
