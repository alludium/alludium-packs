---
id: vc.track_term_sheet_negotiation
title: Track Term Sheet Negotiation
slug: track-term-sheet-negotiation
agent: vc-legal-compliance-desk
skills:
- term-sheet-negotiation-brief
- deal-terms-analysis
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/track-term-sheet-negotiation.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Track Term Sheet Negotiation

Organize open term-sheet issues, give/get options, counsel questions, and approval points without negotiating or approving legal language.

## Instructions

Prepare an internal negotiation brief from the current term sheet, open terms, IC constraints, founder comments or redlines, counsel notes, cap table context, and deal terms analysis. Separate business tradeoffs from counsel review, identify give/get options, and list approval points. Cite material claims, separate assumptions from evidence, and do not provide legal advice, negotiate terms, send terms, approve legal language, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Create or update a durable project file artifact named Term Sheet Negotiation Brief and attach it to the required output field `negotiation_brief_artifact_id`. Use `definitionJson.documentRefs` as the durable document reference contract. Apply each reference by usage: `output_template` sets the output skeleton, `methodology` supplies scoring or analysis logic, `checklist` must be completed with status, evidence, and owner, `style_guide` governs citations and claim language, and `operating_guidance` or `policy` constrains process and approval boundaries. For refs with `outputFieldKey`, produce that output from the referenced pack document and preserve the document ID alongside the output artifact.

## Missing Input Policy

Ask for the current term sheet, open terms, and IC constraints before producing a negotiation brief.

## External Action Policy

Draft only unless a human explicitly approves the send, CRM write, Drive change, project creation, child task creation, or stage transition.

## Completion Criteria

- Required input gaps are resolved or listed as assumptions/open questions.
- Open terms distinguish business tradeoffs from counsel questions.
- Approval points identify owner, dependency, and required human approval point.

## Human Decision Points

- Approve all negotiation positions, founder-facing messages, legal language, and stage movement.
- Approve external communications, CRM writes, Drive/project creation, legal/counsel actions, and founder-facing requests.

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `term_sheet_artifact_id` | Term Sheet Artifact | `file` | yes |
| `current_open_terms` | Current Open Terms | `json` | yes |
| `ic_constraints` | IC Constraints | `richtext` | yes |
| `founder_comments_or_redline` | Founder Comments Or Redline | `richtext` | no |
| `counsel_notes` | Counsel Notes | `richtext` | no |
| `cap_table_artifact_id` | Cap Table | `file` | no |
| `deal_terms_analysis_artifact_id` | Deal Terms Analysis | `file` | no |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `negotiation_brief_artifact_id` | Negotiation Brief | `file` | yes |
| `open_terms_table` | Open Terms Table | `json` | no |
| `give_get_options` | Give/Get Options | `json` | no |
| `legal_escalations` | Legal Escalations | `json` | no |
| `approval_required` | Approval Required | `string` | no |
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

- `vc.document.term_sheet_negotiation_brief_template` (output_template) -> `negotiation_brief_artifact_id`
- `vc.document.evidence_citation_style_guide` (style_guide)
- `vc.document.template_use_guidance` (operating_guidance)

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/track-term-sheet-negotiation.yaml`
- Alludium task ID: `vc.track_term_sheet_negotiation`
- Task family: `deal_structuring`
- Lifecycle stage: `deal_structuring`
- Recommended agent: `vc-legal-compliance-desk` (Alludium template `vc_legal_compliance_desk`)
- Supported project types:
  - `vc_deal_room`

## Required Skills

- `term-sheet-negotiation-brief`
- `deal-terms-analysis`
- `citation-enforcement`
