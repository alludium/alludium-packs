---
id: vc.summarize_initial_call
title: Summarize Meeting Records
slug: summarize-initial-call
agent: vc-meeting-operator
skills:
- meeting-prep-and-summary
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/summarize-initial-call.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Summarize Meeting Records

Summarize or ingest meeting records for one venture-capital opportunity with evidence capture, human review gates, and next-action recommendations.

## Instructions

Summarize or ingest the available meeting records for this opportunity, including transcript artifacts, meeting-summary artifacts, recording exports, notes, or meeting-source links represented in the supplied artifact list. Extract claims and gaps, capture action items, draft a CRM-neutral update, and recommend pass or follow-up. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Use workspace-configured scoring frameworks, CRM providers, stage names, and deal-type metric packs; do not assume a specific fund, CRM, or SaaS default unless the workspace configuration explicitly selects it. Create or update a durable project file artifact named Customer Insights Summary and attach it to the required output field `customer_insights_artifact_id`. Use `definitionJson.documentRefs` as the durable document reference contract. Apply each reference by usage: `output_template` sets the output skeleton, `methodology` supplies scoring or analysis logic, `checklist` must be completed with status, evidence, and owner, `style_guide` governs citations and claim language, and `operating_guidance` or `policy` constrains process and approval boundaries. For refs with `outputFieldKey`, produce that output from the referenced pack document and preserve the document ID alongside the output artifact.

## Missing Input Policy

Require meeting_record_artifact_ids and company_name before producing the call summary. Use meeting_notes as optional supporting context when provided.

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
| `meeting_record_artifact_ids` | Meeting Record Artifact IDs | `string` | yes |
| `meeting_notes` | Meeting Notes | `richtext` | no |
| `company_name` | Company Name | `string` | yes |
| `deal_room_url` | Deal Room Url | `string` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `customer_insights_artifact_id` | Customer Insights Summary | `file` | yes |
| `transcript_summary` | Transcript Summary | `richtext` | no |
| `claims_register` | Claims Register | `string` | no |
| `contradictions_or_gaps` | Contradictions Or Gaps | `string` | no |
| `action_items` | Action Items | `string` | no |
| `draft_crm_update` | Draft CRM Update | `string` | no |
| `pass_follow_up_recommendation` | Pass Follow Up Recommendation | `string` | no |
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

- `vc.document.customer_insights_summary_template` (output_template) -> `customer_insights_artifact_id`
- `vc.document.evidence_citation_style_guide` (style_guide)
- `vc.document.template_use_guidance` (operating_guidance)

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/summarize-initial-call.yaml`
- Alludium task ID: `vc.summarize_initial_call`
- Task family: `meeting`
- Lifecycle stage: `assessment`
- Recommended agent: `vc-meeting-operator` (Alludium template `vc_meeting_operator`)
- Supported project types:
  - `vc_deal_room`

## Required Skills

- `meeting-prep-and-summary`
- `citation-enforcement`

## Planned Skills

- `meeting-prep-and-summary`
- `vc-task-and-next-step-generation`
- `citation-enforcement`

## Workspace-Configured Methodology Skills

- `investment-screening-framework`: Use only when the workspace explicitly configures this screening framework.
