---
id: vc.prepare_ic_agenda
title: Prepare IC Agenda
slug: prepare-ic-agenda
agent: vc-ic-prep-producer
skills:
- meeting-prep-and-summary
- citation-enforcement
- ic-risk-checklist-and-decision-log
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/prepare-ic-agenda.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Prepare IC Agenda

Prepare IC Agenda for one venture-capital opportunity with evidence capture, human review gates, and next-action recommendations.

## Instructions

Prepare the IC agenda, pack checklist, key debate topics, follow-up questions, and pre-read requirements. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Use the required input file artifact `investment_memo_artifact_id` as the source memo when preparing the IC agenda. Create or update a durable project file artifact named IC Agenda and attach it to the required output field `ic_agenda_artifact_id`. Use `definitionJson.documentRefs` as the durable document reference contract. Apply each reference by usage: `output_template` sets the output skeleton, `methodology` supplies scoring or analysis logic, `checklist` must be completed with status, evidence, and owner, `style_guide` governs citations and claim language, and `operating_guidance` or `policy` constrains process and approval boundaries. For refs with `outputFieldKey`, produce that output from the referenced pack document and preserve the document ID alongside the output artifact.

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
| `investment_memo_artifact_id` | Investment Memo | `file` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `ic_agenda_artifact_id` | IC Agenda | `file` | yes |
| `agenda` | Agenda | `richtext` | no |
| `pack_checklist` | Pack Checklist | `json` | no |
| `key_debate_topics` | Key Debate Topics | `string` | no |
| `follow_up_questions` | Follow Up Questions | `json` | no |
| `pre_read_requirements` | Pre Read Requirements | `json` | no |
| `summary` | Summary | `richtext` | no |
| `recommendation` | Recommendation | `string` | no |
| `source_links` | Source Links | `string` | no |
| `assumptions` | Assumptions | `string` | no |
| `evidence_quality` | Evidence Quality | `json` | no |
| `open_questions` | Open Questions | `json` | no |
| `risks` | Risks | `json` | no |
| `human_decision_points` | Human Decision Points | `string` | no |
| `next_actions` | Next Actions | `json` | no |

## Document References

- `vc.document.ic_agenda_template` (output_template) -> `ic_agenda_artifact_id`
- `vc.document.template_use_guidance` (operating_guidance)

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/prepare-ic-agenda.yaml`
- Alludium task ID: `vc.prepare_ic_agenda`
- Task family: `ic`
- Lifecycle stage: `decision_review`
- Recommended agent: `vc-ic-prep-producer` (Alludium template `vc_ic_prep_producer`)
- Supported project types:
  - `vc_deal_room`

## Required Skills

- `meeting-prep-and-summary`
- `citation-enforcement`
- `ic-risk-checklist-and-decision-log`
