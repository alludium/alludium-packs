---
id: vc.manage_closing_checklist
title: Manage Closing Checklist
slug: manage-closing-checklist
agent: vc-legal-compliance-desk
skills:
- citation-enforcement
- closing-coordination-and-cp-tracking
- vc-task-and-next-step-generation
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/manage-closing-checklist.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Manage Closing Checklist

Manage Closing Checklist for one venture-capital opportunity with evidence capture, human review gates, and next-action recommendations.

## Instructions

Track closing workplan owners, due dates, blockers, daily status, and onboarding readiness for human close-readiness review. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Use the required input file artifacts `ic_decision_record_artifact_id` and `term_sheet_review_artifact_id` as the decision and terms sources, and use `closing_source_artifact_ids` for legal documents, workplans, counsel notes, CP lists, signed documents, and evidence files. Create or update a durable project file artifact named Closing Checklist and attach it to the required output field `closing_checklist_artifact_id`. Use `definitionJson.documentRefs` as the durable document reference contract. Apply each reference by usage: `output_template` sets the output skeleton, `methodology` supplies scoring or analysis logic, `checklist` must be completed with status, evidence, and owner, `style_guide` governs citations and claim language, and `operating_guidance` or `policy` constrains process and approval boundaries. For refs with `outputFieldKey`, produce that output from the referenced pack document and preserve the document ID alongside the output artifact.

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
| `ic_decision_record_artifact_id` | IC Decision Record | `file` | yes |
| `term_sheet_review_artifact_id` | Term Sheet Review | `file` | yes |
| `closing_source_artifact_ids` | Closing Source Artifact IDs | `string` | yes |
| `legal_document_status` | Legal Document Status | `string` | yes |
| `legal_diligence_artifact_id` | Legal Diligence | `file` | no |
| `investment_document_review_artifact_id` | Investment Document Review | `file` | no |
| `owners` | Owners | `json` | no |
| `deadlines` | Deadlines | `json` | no |
| `blockers` | Blockers | `json` | no |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `closing_checklist_artifact_id` | Closing Checklist | `file` | yes |
| `closing_status` | Closing Status | `string` | no |
| `owner_due_date_table` | Owner Due Date Table | `string` | no |
| `blockers` | Blockers | `json` | no |
| `daily_status_summary` | Daily Status Summary | `richtext` | no |
| `onboarding_readiness` | Onboarding Readiness | `string` | no |
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

- `vc.document.closing_checklist` (output_template) -> `closing_checklist_artifact_id`
- `vc.document.legal_diligence_guide` (methodology)
- `vc.document.template_use_guidance` (operating_guidance)

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/manage-closing-checklist.yaml`
- Alludium task ID: `vc.manage_closing_checklist`
- Task family: `closing`
- Lifecycle stage: `closing`
- Recommended agent: `vc-legal-compliance-desk` (Alludium template `vc_legal_compliance_desk`)
- Supported project types:
  - `vc_deal_room`

## Required Skills

- `citation-enforcement`
- `closing-coordination-and-cp-tracking`
- `vc-task-and-next-step-generation`
