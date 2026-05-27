---
id: vc.review_investment_documents
title: Review Investment Documents
slug: review-investment-documents
agent: vc-legal-compliance-desk
skills:
- legal-diligence-coordination
- closing-coordination-and-cp-tracking
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/review-investment-documents.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Review Investment Documents

Coordinate post-term-sheet investment document review, disclosure-letter issues, counsel questions, and closing readiness notes without providing legal advice.

## Instructions

Coordinate investment document review by mapping document provisions back to the term sheet review, disclosure letter, counsel notes, board minutes, and cap table context. Identify open document issues, counsel questions, and closing readiness notes without interpreting legal sufficiency. Cite material claims, separate assumptions from evidence, and do not provide legal advice, sign off documents, send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Create or update a durable project file artifact named Investment Document Review and attach it to the required output field `investment_document_review_artifact_id`. Use `definitionJson.documentRefs` as the durable document reference contract. Apply each reference by usage: `output_template` sets the output skeleton, `methodology` supplies scoring or analysis logic, `checklist` must be completed with status, evidence, and owner, `style_guide` governs citations and claim language, and `operating_guidance` or `policy` constrains process and approval boundaries. For refs with `outputFieldKey`, produce that output from the referenced pack document and preserve the document ID alongside the output artifact.

## Missing Input Policy

Ask for investment document artifacts and term sheet review before producing document-readiness notes.

## External Action Policy

Draft only unless a human explicitly approves the send, CRM write, Drive change, project creation, child task creation, or stage transition.

## Completion Criteria

- Required input gaps are resolved or listed as assumptions/open questions.
- Term-to-document mapping distinguishes business mismatches from counsel questions.
- Closing readiness notes identify owner, dependency, and required human approval point.

## Human Decision Points

- Approve legal conclusions, document sufficiency, signing readiness, counsel/founder communications, and stage movement.
- Approve external communications, CRM writes, Drive/project creation, legal/counsel actions, and founder-facing requests.

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `investment_document_artifact_ids` | Investment Document Artifact IDs | `string` | yes |
| `term_sheet_review_artifact_id` | Term Sheet Review | `file` | yes |
| `negotiation_brief_artifact_id` | Negotiation Brief | `file` | no |
| `legal_diligence_artifact_id` | Legal Diligence | `file` | no |
| `disclosure_letter_artifact_id` | Disclosure Letter | `file` | no |
| `counsel_notes` | Counsel Notes | `richtext` | no |
| `cap_table_artifact_id` | Cap Table | `file` | no |
| `board_minutes_artifact_id` | Board Minutes | `file` | no |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `investment_document_review_artifact_id` | Investment Document Review | `file` | yes |
| `term_to_document_mapping` | Term To Document Mapping | `json` | no |
| `open_document_issues` | Open Document Issues | `json` | no |
| `counsel_questions` | Counsel Questions | `json` | no |
| `closing_readiness_notes` | Closing Readiness Notes | `richtext` | no |
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

- `vc.document.investment_document_review_template` (output_template) -> `investment_document_review_artifact_id`
- `vc.document.legal_diligence_guide` (methodology)
- `vc.document.evidence_citation_style_guide` (style_guide)
- `vc.document.template_use_guidance` (operating_guidance)

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/review-investment-documents.yaml`
- Alludium task ID: `vc.review_investment_documents`
- Task family: `contracts`
- Lifecycle stage: `contracts`
- Recommended agent: `vc-legal-compliance-desk` (Alludium template `vc_legal_compliance_desk`)
- Supported project types:
  - `vc_investment_management`

## Required Skills

- `legal-diligence-coordination`
- `closing-coordination-and-cp-tracking`
- `citation-enforcement`
