---
id: vc.review_term_sheet
title: Review Term Sheet
slug: review-term-sheet
agent: vc-legal-compliance-desk
skills:
- red-flags-scanner
- citation-enforcement
---

# Review Term Sheet

Review Term Sheet for one venture-capital opportunity with evidence capture, human review gates, and next-action recommendations.

## Instructions

Review the term sheet for business deviations, red flags, and counsel review questions without providing legal advice. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Create or update a durable project file artifact named Term Sheet Review and attach it to the required output field `term_sheet_review_artifact_id`.

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
| `term_sheet_artifact_id` | Term Sheet Artifact | `file` | yes |
| `deal_terms` | Deal Terms | `json` | yes |
| `standard_terms_reference` | Standard Terms Reference | `json` | no |
| `counsel_notes` | Counsel Notes | `richtext` | no |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `term_sheet_review_artifact_id` | Term Sheet Review | `file` | yes |
| `term_summary` | Term Summary | `richtext` | no |
| `deviation_table` | Deviation Table | `string` | no |
| `review_focus` | Review Focus | `multiselect` | no |
| `deal_room_url` | Deal Room URL | `string` | no |
| `recommendation` | Recommendation | `select` | no |
| `review_notes` | Review Notes | `richtext` | no |
| `red_flags` | Red Flags | `string` | no |
| `counsel_review_questions` | Counsel Review Questions | `json` | no |
| `approval_required` | Approval Required | `string` | no |
| `summary` | Summary | `richtext` | no |
| `source_links` | Source Links | `string` | no |
| `assumptions` | Assumptions | `string` | no |
| `evidence_quality` | Evidence Quality | `json` | no |
| `open_questions` | Open Questions | `json` | no |
| `risks` | Risks | `json` | no |
| `human_decision_points` | Human Decision Points | `string` | no |
| `next_actions` | Next Actions | `json` | no |

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/review-term-sheet.yaml`
- Alludium task ID: `vc.review_term_sheet`
- Task family: `closing`
- Lifecycle stage: `term_sheet`
- Recommended agent: `vc-legal-compliance-desk` (Alludium template `vc_legal_compliance_desk`)
- Supported project types:
  - `vc_deal_room`

## Required Skills

- `red-flags-scanner`
- `citation-enforcement`

## Planned Skills

- `closing-coordination-and-cp-tracking`
- `red-flags-scanner`
- `citation-enforcement`
