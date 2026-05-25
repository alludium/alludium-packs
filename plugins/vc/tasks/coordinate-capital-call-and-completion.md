---
id: vc.coordinate_capital_call_and_completion
title: Coordinate Capital Call And Completion
slug: coordinate-capital-call-and-completion
agent: vc-legal-compliance-desk
skills:
- closing-coordination-and-cp-tracking
- vc-task-and-next-step-generation
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/coordinate-capital-call-and-completion.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Coordinate Capital Call And Completion

Track final closing administration, capital call status, funds transfer readiness, share-certificate receipt, and portfolio handoff triggers without initiating banking or legal completion actions.

## Instructions

Track the final administrative closing sequence from conditions precedent verification, closing checklist, transaction bible, administrator status, capital call status, funds transfer status, and share certificate status. Produce completion status, readiness notes, blockers, and portfolio handoff trigger recommendations. Cite material claims, separate assumptions from evidence, and do not initiate banking, administrator instructions, legal completion actions, external messages, CRM writes, folder/project creation, child task creation, or stage movement without explicit human approval. Create or update a durable project file artifact named Completion Tracker and attach it to the required output field `completion_tracker_artifact_id`. Use `definitionJson.documentRefs` as the durable document reference contract. Apply each reference by usage: `output_template` sets the output skeleton, `methodology` supplies scoring or analysis logic, `checklist` must be completed with status, evidence, and owner, `style_guide` governs citations and claim language, and `operating_guidance` or `policy` constrains process and approval boundaries. For refs with `outputFieldKey`, produce that output from the referenced pack document and preserve the document ID alongside the output artifact.

## Missing Input Policy

Ask for CP verification, closing checklist, and transaction bible before producing completion readiness.

## External Action Policy

Draft only unless a human explicitly approves the send, CRM write, Drive change, project creation, child task creation, stage transition, administrator instruction, or banking action.

## Completion Criteria

- Required input gaps are resolved or listed as assumptions/open questions.
- Completion tracker separates evidence-backed status from human/counsel/finance signoff.
- Handoff trigger identifies owner, dependency, and required human approval point.

## Human Decision Points

- Approve banking actions, administrator instructions, completion status, portfolio handoff, and stage movement.
- Approve external communications, CRM writes, Drive/project creation, legal/counsel actions, and founder-facing requests.

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `conditions_precedent_verification_artifact_id` | Conditions Precedent Verification | `file` | yes |
| `closing_checklist_artifact_id` | Closing Checklist | `file` | yes |
| `transaction_bible_artifact_id` | Transaction Bible | `file` | yes |
| `administrator_contact` | Administrator Contact | `string` | no |
| `capital_call_status` | Capital Call Status | `string` | no |
| `funds_transfer_status` | Funds Transfer Status | `string` | no |
| `share_certificate_status` | Share Certificate Status | `string` | no |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `completion_tracker_artifact_id` | Completion Tracker | `file` | yes |
| `capital_call_status_summary` | Capital Call Status Summary | `richtext` | no |
| `funds_transfer_readiness` | Funds Transfer Readiness | `string` | no |
| `share_certificate_receipt_status` | Share Certificate Receipt Status | `string` | no |
| `portfolio_handoff_trigger` | Portfolio Handoff Trigger | `string` | no |
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

- `vc.document.completion_tracker_template` (output_template) -> `completion_tracker_artifact_id`
- `vc.document.evidence_citation_style_guide` (style_guide)
- `vc.document.template_use_guidance` (operating_guidance)

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/coordinate-capital-call-and-completion.yaml`
- Alludium task ID: `vc.coordinate_capital_call_and_completion`
- Task family: `closing`
- Lifecycle stage: `closing`
- Recommended agent: `vc-legal-compliance-desk` (Alludium template `vc_legal_compliance_desk`)
- Supported project types:
  - `vc_deal_room`

## Required Skills

- `closing-coordination-and-cp-tracking`
- `vc-task-and-next-step-generation`
- `citation-enforcement`
