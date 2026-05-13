---
id: vc.generate_82_factor_questions
title: Generate 82-Factor Questions
slug: generate-82-factor-questions
agent: vc-first-look-analyst
skills:
- citation-enforcement
---

# Generate 82-Factor Questions

Generate 82-Factor Questions for one venture-capital opportunity with evidence capture, human review gates, and next-action recommendations.

## Instructions

Generate prioritized 82-Factor diligence questions with rationale, source gap, owner, and urgency. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Use workspace-configured scoring frameworks, CRM providers, stage names, and deal-type metric packs; do not assume a specific fund, CRM, or SaaS default unless the workspace configuration explicitly selects it. Create or update a durable project file artifact named 82-Factor Question Set and attach it to the required output field `eighty_two_factor_questions_artifact_id`.

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
| `known_claims` | Known Claims | `string` | yes |
| `existing_answers` | Existing Answers | `string` | no |
| `priority_workstreams` | Priority Workstreams | `string` | no |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `eighty_two_factor_questions_artifact_id` | 82-Factor Question Set | `file` | yes |
| `question_set` | Question Set | `string` | no |
| `rationale` | Rationale | `string` | no |
| `source_gap` | Source Gap | `string` | no |
| `owner` | Owner | `string` | no |
| `urgency` | Urgency | `string` | no |
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

- Source template: `alludium/task-definition-templates/vc-workflows/generate-82-factor-questions.yaml`
- Alludium task ID: `vc.generate_82_factor_questions`
- Task family: `diligence`
- Lifecycle stage: `diligence`
- Recommended agent: `vc-first-look-analyst` (Alludium template `vc_first_look_analyst`)
- Supported project types:
  - `vc_deal_room`

## Required Skills

- `citation-enforcement`

## Planned Skills

- `citation-enforcement`

## Workspace-Configured Methodology Skills

- `82-factor-diligence-question-generation`: Use only when the workspace explicitly configures this diligence framework.
