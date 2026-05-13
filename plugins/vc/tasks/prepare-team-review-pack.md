---
id: vc.prepare_team_review_pack
title: Prepare Team Review Pack
slug: prepare-team-review-pack
agent: vc-diligence-analyst
skills:
- ic-memo-assembly
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/prepare-team-review-pack.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Prepare Team Review Pack

Prepare Team Review Pack for one venture-capital opportunity with evidence capture, human review gates, and next-action recommendations.

## Instructions

Assemble the Team Review pack from prior stage outputs, evidence summary, 10-Factor and 82-Factor summaries, founder risks, and stage-gate recommendation. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Use workspace-configured scoring frameworks, CRM providers, stage names, and deal-type metric packs; do not assume a specific fund, CRM, or SaaS default unless the workspace configuration explicitly selects it. Use the required input file artifacts `commercial_dd_artifact_id`, `financial_dd_artifact_id`, `founder_evaluation_artifact_id`, `technical_dd_artifact_id`, and `eighty_two_factor_questions_artifact_id` as the review subjects for the team review pack. Create or update a durable project file artifact named Team Review Pack and attach it to the required output field `team_review_pack_artifact_id`.

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
| `commercial_dd_artifact_id` | Commercial DD Report | `file` | yes |
| `financial_dd_artifact_id` | Financial DD Report | `file` | yes |
| `founder_evaluation_artifact_id` | Founder Evaluation | `file` | yes |
| `technical_dd_artifact_id` | Technical DD Report | `file` | yes |
| `eighty_two_factor_questions_artifact_id` | 82-Factor Question Set | `file` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `team_review_pack_artifact_id` | Team Review Pack | `file` | yes |
| `company_snapshot` | Company Snapshot | `json` | no |
| `evidence_summary` | Evidence Summary | `richtext` | no |
| `ten_and_82_factor_summary` | Ten And 82 Factor Summary | `richtext` | no |
| `founder_risk_summary` | Founder Risk Summary | `richtext` | no |
| `stage_gate_recommendation` | Stage Gate Recommendation | `string` | no |
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

- Source template: `alludium/task-definition-templates/vc-workflows/prepare-team-review-pack.yaml`
- Alludium task ID: `vc.prepare_team_review_pack`
- Task family: `diligence`
- Lifecycle stage: `review`
- Recommended agent: `vc-diligence-analyst` (Alludium template `vc_diligence_analyst`)
- Supported project types:
  - `vc_deal_room`

## Required Skills

- `ic-memo-assembly`
- `citation-enforcement`

## Planned Skills

- `ic-memo-assembly`
- `citation-enforcement`

## Workspace-Configured Methodology Skills

- `82-factor-diligence-question-generation`: Use only when the workspace explicitly configures this diligence framework.
