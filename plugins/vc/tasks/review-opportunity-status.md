---
id: vc.review_opportunity_status
title: Review Opportunity Status
slug: review-opportunity-status
agent: vc-pipeline-autopilot
skills:
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/review-opportunity-status.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Review Opportunity Status

Review the current status of one venture-capital opportunity and suggest missing inputs, stage movement, and next tasks without producing a formal investment evaluation document.

## Instructions

Review the supplied stage snapshot and current Deal Room state, identify missing inputs, recommend stage movement, and list next task suggestions using the workspace configured stage graph; do not create tasks automatically. This is a status/control helper, not a formal investment evaluation memo. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Use workspace-configured scoring frameworks, CRM providers, stage names, and deal-type metric packs; do not assume a specific fund, CRM, or SaaS default unless the workspace configuration explicitly selects it.

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
| `company_name` | Company Name | `string` | yes |
| `investment_stage` | Investment Stage | `string` | yes |
| `stage_snapshot` | Stage Snapshot | `richtext` | yes |
| `relevant_artifact_ids` | Relevant Artifact IDs | `string` | no |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `stage_summary` | Stage Summary | `richtext` | no |
| `missing_inputs` | Missing Inputs | `string` | no |
| `stage_transition_recommendation` | Stage Transition Recommendation | `string` | no |
| `next_task_suggestions` | Next Task Suggestions | `string` | no |
| `source_links` | Source Links | `string` | no |
| `summary` | Summary | `richtext` | no |
| `recommendation` | Recommendation | `string` | no |
| `assumptions` | Assumptions | `string` | no |
| `evidence_quality` | Evidence Quality | `json` | no |
| `open_questions` | Open Questions | `json` | no |
| `risks` | Risks | `json` | no |
| `human_decision_points` | Human Decision Points | `string` | no |
| `next_actions` | Next Actions | `json` | no |

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/review-opportunity-status.yaml`
- Alludium task ID: `vc.review_opportunity_status`
- Task family: `pipeline`
- Lifecycle stage: `assessment`
- Recommended agent: `vc-pipeline-autopilot` (Alludium template `vc_pipeline_autopilot`)
- Supported project types:
  - `vc_deal_room`

## Required Skills

- `citation-enforcement`

## Planned Skills

- `vc-task-and-next-step-generation`
- `citation-enforcement`

## Workspace-Configured Methodology Skills

- `pipeline-health-and-crm-hygiene`: Use only when the workspace CRM/stage model matches the skill assumptions.
