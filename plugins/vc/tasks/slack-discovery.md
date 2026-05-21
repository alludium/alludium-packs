---
id: vc.slack_discovery
title: Explore Slack Channels for VC Context
slug: slack-discovery
agent: vc-pipeline-autopilot
skills:
- vc-slack-discovery
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-integrations/slack-discovery.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Explore Slack Channels for VC Context

Discover Slack workspace and channel scope before selected VC context reads or handoff notifications.

## Instructions

Use the connected `slack_v2` application to confirm workspace context with `slack_v2-get-current-user` and enumerate channels with `slack_v2-list-channels`. Classify channel purpose as deal intake, deal-specific discussion, IC prep, portfolio handoff, operations, broad/general, sensitive/excluded, or unknown.

## Missing Input Policy

If Slack is not authorized, ask for authorization or a supplied channel list.

## External Action Policy

Discovery only. Do not read messages, post, reply, create channels, or change channel settings.

## Completion Criteria

- Candidate channels are classified with confidence.
- User choices needed before message/thread reads are explicit.

## Human Decision Points

- Approve included channels or threads before sync read.
- Approve any notification targets separately.

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `discovery_goal` | Discovery Goal | `string` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `slack_discovery_report` | Slack Discovery Report | `richtext` | no |
| `channel_scope_questions` | Channel Scope Questions | `json` | no |

## Routing

- Source template: `alludium/task-definition-templates/vc-integrations/slack-discovery.yaml`
- Alludium task ID: `vc.slack_discovery`
- Task family: `integration_discovery`
- Recommended agent: `vc-pipeline-autopilot` (Alludium template `vc_pipeline_autopilot`)
- Supported project types:
  - `vc_deal_room`
- Supported project scopes:
  - `project_management`

## Required Skills

- `vc-slack-discovery`
- `citation-enforcement`
