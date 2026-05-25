---
id: vc.prepare_deal_flow_agenda
title: Prepare Deal Flow Agenda
slug: prepare-deal-flow-agenda
agent: vc-pipeline-autopilot
skills:
- citation-enforcement
- vc-task-and-next-step-generation
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/prepare-deal-flow-agenda.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Prepare Deal Flow Agenda

Prepare Deal Flow Agenda for one venture-capital opportunity with evidence capture, human review gates, and next-action recommendations.

## Instructions

Prepare the deal-flow agenda from the pipeline snapshot; identify stale deals, new deals, stage-change candidates, and the seven-day action plan. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Use workspace-configured scoring frameworks, CRM providers, stage names, and deal-type metric packs; do not assume a specific fund, CRM, or SaaS default unless the workspace configuration explicitly selects it.

## Missing Input Policy

Ask for missing required inputs before producing investment-stage recommendations.

## External Action Policy

Draft only unless a human explicitly approves the send, CRM write, Drive change, project creation, child task creation, or stage transition.

## Completion Criteria

- Required input gaps are resolved or listed as assumptions/open questions.
- Material conclusions include source links or are labeled as human judgment calls.
- Next actions identify owner, dependency, and required human approval point.

## Human Decision Points

- Approve investment-stage movement, pass/follow-up recommendations, and final task completion.
- Approve external communications, CRM writes, Drive/project creation, legal/counsel actions, and founder-facing requests.

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `pipeline_snapshot` | Pipeline Snapshot | `json` | yes |
| `meeting_date` | Meeting Date | `string` | yes |
| `stale_deal_threshold` | Stale Deal Threshold | `string` | no |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `agenda` | Agenda | `richtext` | no |
| `stale_deal_list` | Stale Deal List | `json` | no |
| `new_deal_list` | New Deal List | `json` | no |
| `stage_change_candidates` | Stage Change Candidates | `string` | no |
| `seven_day_action_plan` | Seven Day Action Plan | `string` | no |
| `summary` | Summary | `richtext` | no |
| `recommendation` | Recommendation | `string` | no |
| `source_links` | Source Links | `string` | no |
| `assumptions` | Assumptions | `string` | no |
| `evidence_quality` | Evidence Quality | `json` | no |
| `open_questions` | Open Questions | `json` | no |
| `risks` | Risks | `json` | no |
| `human_decision_points` | Human Decision Points | `string` | no |
| `next_actions` | Next Actions | `json` | no |

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/prepare-deal-flow-agenda.yaml`
- Alludium task ID: `vc.prepare_deal_flow_agenda`
- Task family: `pipeline`
- Lifecycle stage: `evaluation`
- Recommended agent: `vc-pipeline-autopilot` (Alludium template `vc_pipeline_autopilot`)
- Supported project types:
  - `vc_deal_room`
- Supported project scopes:
  - `project_management`

## Required Skills

- `citation-enforcement`
- `vc-task-and-next-step-generation`

## Workspace-Configured Methodology Skills

- `pipeline-health-and-crm-hygiene`: Use only when the workspace CRM/stage model matches the skill assumptions.
