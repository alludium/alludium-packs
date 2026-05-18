---
id: vc.create_ic_memo
title: Create IC Memo
slug: create-ic-memo
agent: vc-ic-prep-producer
skills:
- ic-memo-assembly
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/create-ic-memo.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Create IC Memo

Create IC Memo for one venture-capital opportunity with evidence capture, human review gates, and next-action recommendations.

## Instructions

Assemble the IC memo and pack checklist from stage outputs, DD summaries, founder risks, term-sheet inputs, source artifacts, unresolved risks, assumptions, and citation coverage. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Use the required diligence input file artifacts `commercial_dd_artifact_id`, `financial_dd_artifact_id`, `founder_evaluation_artifact_id`, `technical_dd_artifact_id`, and `diligence_question_bank_artifact_id` as source artifacts for the IC memo. Create or update a durable project file artifact named Investment Memo and attach it to the required output field `investment_memo_artifact_id`. Use the required input file artifacts `team_review_pack_artifact_id` and `partner_review_pack_artifact_id` as the review-pack sources for the IC memo.

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
| `team_review_pack_artifact_id` | Team Review Pack | `file` | yes |
| `partner_review_pack_artifact_id` | Partner Review Pack | `file` | yes |
| `commercial_dd_artifact_id` | Commercial DD Report | `file` | yes |
| `financial_dd_artifact_id` | Financial DD Report | `file` | yes |
| `founder_evaluation_artifact_id` | Founder Evaluation | `file` | yes |
| `technical_dd_artifact_id` | Technical DD Report | `file` | yes |
| `diligence_question_bank_artifact_id` | Structured Diligence Question Bank | `file` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `investment_memo_artifact_id` | Investment Memo | `file` | yes |
| `investment_memo` | Investment Memo | `richtext` | no |
| `ic_pack_checklist` | Ic Pack Checklist | `json` | no |
| `decision_ask` | Decision Ask | `string` | no |
| `unresolved_risks` | Unresolved Risks | `json` | no |
| `assumptions` | Assumptions | `string` | no |
| `citation_coverage` | Citation Coverage | `string` | no |
| `summary` | Summary | `richtext` | no |
| `recommendation` | Recommendation | `string` | no |
| `source_links` | Source Links | `string` | no |
| `evidence_quality` | Evidence Quality | `json` | no |
| `open_questions` | Open Questions | `json` | no |
| `risks` | Risks | `json` | no |
| `human_decision_points` | Human Decision Points | `string` | no |
| `next_actions` | Next Actions | `json` | no |

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/create-ic-memo.yaml`
- Alludium task ID: `vc.create_ic_memo`
- Task family: `ic`
- Lifecycle stage: `review`
- Recommended agent: `vc-ic-prep-producer` (Alludium template `vc_ic_prep_producer`)
- Supported project types:
  - `vc_deal_room`

## Required Skills

- `ic-memo-assembly`
- `citation-enforcement`

## Planned Skills

- `ic-memo-assembly`
- `citation-enforcement`
- `ic-risk-checklist-and-decision-log`
