---
id: vc.capture_investment_management_handoff
title: Capture Investment Management Handoff
slug: capture-investment-management-handoff
agent: vc-legal-compliance-desk
skills:
- citation-enforcement
- vc-task-and-next-step-generation
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/capture-investment-management-handoff.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Capture Investment Management Handoff

Capture the reviewed deal-structuring handoff needed to create an Investment Management project for formal diligence, contracts, and closing.

## Instructions

Capture the reviewed handoff from Deal Pipeline deal structuring into Investment Management. Confirm company identity, lead owner, IC or partner-review decision context, current term-sheet status, diligence source materials, legal/finance workstream readiness, and missing evidence. Cite material claims, separate assumptions from evidence, and do not create projects, send messages, mutate CRM records, move stages, or start legal/finance work without explicit human approval. When this task is used as a guided project creation task, complete with structured output `projectCreation.fieldValues.company_name` and include any confidently collected declared creation fields. Do not create the project; the platform finalizer owns deterministic project creation after task completion. Use `definitionJson.documentRefs` as the durable document reference contract. Apply each reference by usage: `style_guide` governs citations and claim language, and `operating_guidance` constrains process and approval boundaries.

## Missing Input Policy

Ask for company_name and at least one reviewed handoff source such as an IC decision, term-sheet review, deal-terms artifact, partner review, or counsel note.

## External Action Policy

Draft only unless a human explicitly approves project creation, external communications, CRM writes, Drive changes, legal/counsel actions, capital calls, or stage transitions.

## Completion Criteria

- Required identity and handoff evidence are captured or listed as explicit gaps.
- Formal diligence, contracts, and closing readiness are separated from assumptions.
- Next actions identify owner, dependency, and required human approval point.
- Guided project creation output includes `projectCreation.fieldValues.company_name`.

## Human Decision Points

- Approve creation of the Investment Management project.
- Approve legal, finance, counsel, CRM, Drive, task creation, stage movement, and external communication actions separately.

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `company_name` | Company Name | `string` | yes |
| `lead_partner` | Lead Partner | `string` | no |
| `handoff_source_artifact_ids` | Handoff Source Artifact IDs | `string` | no |
| `ic_decision_record_artifact_id` | IC Decision Record | `file` | yes |
| `term_sheet_review_artifact_id` | Term Sheet Review | `file` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `projectCreation` | Project Creation Payload | `json` | yes |
| `handoff_summary` | Handoff Summary | `richtext` | no |
| `missing_information` | Missing Information | `string` | no |
| `next_actions` | Next Actions | `json` | no |

## Document References

- `vc.document.evidence_citation_style_guide` (style_guide)
- `vc.document.template_use_guidance` (operating_guidance)

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/capture-investment-management-handoff.yaml`
- Alludium task ID: `vc.capture_investment_management_handoff`
- Task family: `investment_management_setup`
- Lifecycle stage: `formal_diligence`
- Recommended agent: `vc-legal-compliance-desk` (Alludium template `vc_legal_compliance_desk`)
- Supported project types:
  - `vc_investment_management`

## Required Skills

- `citation-enforcement`
- `vc-task-and-next-step-generation`
