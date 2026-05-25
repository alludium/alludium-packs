---
id: vc.record_ic_decision
title: Record IC Decision
slug: record-ic-decision
agent: vc-ic-prep-producer
skills:
- citation-enforcement
- ic-risk-checklist-and-decision-log
- vc-task-and-next-step-generation
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/record-ic-decision.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Record IC Decision

Record IC Decision for one venture-capital opportunity with evidence capture, human review gates, and next-action recommendations.

## Instructions

Record the IC decision outcome, vote or consensus summary, dissent and objections, conditions, post-IC action items, and stage transition recommendation. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Use the required input file artifacts `investment_memo_artifact_id` and `ic_agenda_artifact_id` as the IC decision record subjects, alongside the transcript or notes. Create or update a durable project file artifact named IC Decision Record and attach it to the required output field `ic_decision_record_artifact_id`. Use `definitionJson.documentRefs` as the durable document reference contract. Apply each reference by usage: `output_template` sets the output skeleton, `methodology` supplies scoring or analysis logic, `checklist` must be completed with status, evidence, and owner, `style_guide` governs citations and claim language, and `operating_guidance` or `policy` constrains process and approval boundaries. For refs with `outputFieldKey`, produce that output from the referenced pack document and preserve the document ID alongside the output artifact.

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
| `ic_agenda_artifact_id` | IC Agenda | `file` | yes |
| `ic_transcript_or_notes` | Ic Transcript Or Notes | `richtext` | yes |
| `decision_options` | Decision Options | `string` | yes |
| `conditions_discussed` | Conditions Discussed | `json` | no |
| `attendees` | Attendees | `string` | no |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `ic_decision_record_artifact_id` | IC Decision Record | `file` | yes |
| `decision_outcome` | Decision Outcome | `string` | no |
| `vote_or_consensus_summary` | Vote Or Consensus Summary | `richtext` | no |
| `dissent_and_objections` | Dissent And Objections | `string` | no |
| `conditions` | Conditions | `json` | no |
| `post_ic_action_items` | Post Ic Action Items | `string` | no |
| `stage_transition_recommendation` | Stage Transition Recommendation | `string` | no |
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

- `vc.document.ic_decision_record_template` (output_template) -> `ic_decision_record_artifact_id`
- `vc.document.evidence_citation_style_guide` (style_guide)
- `vc.document.template_use_guidance` (operating_guidance)

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/record-ic-decision.yaml`
- Alludium task ID: `vc.record_ic_decision`
- Task family: `ic`
- Lifecycle stage: `decision_review`
- Recommended agent: `vc-ic-prep-producer` (Alludium template `vc_ic_prep_producer`)
- Supported project types:
  - `vc_deal_room`

## Required Skills

- `citation-enforcement`
- `ic-risk-checklist-and-decision-log`
- `vc-task-and-next-step-generation`
