---
id: vc.run_legal_diligence
title: Run Legal Diligence
slug: run-legal-diligence
agent: vc-legal-compliance-desk
skills:
- legal-diligence-coordination
- red-flags-scanner
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/run-legal-diligence.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Run Legal Diligence

Coordinate legal diligence document indexing, issue tracking, counsel questions, and showstopper-risk review support without providing legal advice.

## Instructions

Coordinate legal diligence by indexing legal source artifacts, tracking issues, drafting counsel questions, and surfacing showstopper risks for human review. Separate factual document gaps from legal conclusions. Cite material claims, separate assumptions from evidence, and do not provide legal advice, clear legal risks, approve legal sufficiency, send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Create or update a durable project file artifact named Legal Diligence Tracker and attach it to the required output field `legal_diligence_artifact_id`. Use `definitionJson.documentRefs` as the durable document reference contract. Apply each reference by usage: `output_template` sets the output skeleton, `methodology` supplies scoring or analysis logic, `checklist` must be completed with status, evidence, and owner, `style_guide` governs citations and claim language, and `operating_guidance` or `policy` constrains process and approval boundaries. For refs with `outputFieldKey`, produce that output from the referenced pack document and preserve the document ID alongside the output artifact.

## Missing Input Policy

Ask for legal source artifacts and company name before producing a legal diligence tracker.

## External Action Policy

Draft only unless a human explicitly approves the send, CRM write, Drive change, project creation, child task creation, or stage transition.

## Completion Criteria

- Required input gaps are resolved or listed as assumptions/open questions.
- Issue register separates factual gaps from counsel/human legal judgments.
- Counsel questions identify owner, dependency, and required human approval point.

## Human Decision Points

- Approve legal conclusions, counsel communications, founder requests, showstopper classification, and stage movement.
- Approve external communications, CRM writes, Drive/project creation, legal/counsel actions, and founder-facing requests.

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `legal_source_artifact_ids` | Legal Source Artifact IDs | `string` | yes |
| `company_name` | Company Name | `string` | yes |
| `counsel_requirements` | Counsel Requirements | `json` | no |
| `ip_artifact_ids` | IP Artifact IDs | `string` | no |
| `corporate_structure_artifact_id` | Corporate Structure Artifact | `file` | no |
| `employment_contract_artifact_ids` | Employment Contract Artifact IDs | `string` | no |
| `litigation_search_artifact_ids` | Litigation Search Artifact IDs | `string` | no |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `legal_diligence_artifact_id` | Legal Diligence Tracker | `file` | yes |
| `legal_document_index` | Legal Document Index | `json` | no |
| `issue_register` | Issue Register | `json` | no |
| `counsel_questions` | Counsel Questions | `json` | no |
| `showstopper_risks` | Showstopper Risks | `json` | no |
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

- `vc.document.legal_diligence_tracker_template` (output_template) -> `legal_diligence_artifact_id`
- `vc.document.legal_diligence_guide` (methodology)
- `vc.document.formal_diligence_workstream_guide` (methodology)
- `vc.document.formal_diligence_checklist` (checklist)
- `vc.document.evidence_citation_style_guide` (style_guide)
- `vc.document.template_use_guidance` (operating_guidance)

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/run-legal-diligence.yaml`
- Alludium task ID: `vc.run_legal_diligence`
- Task family: `diligence`
- Lifecycle stage: `formal_diligence`
- Recommended agent: `vc-legal-compliance-desk` (Alludium template `vc_legal_compliance_desk`)
- Supported project types:
  - `vc_investment_management`

## Required Skills

- `legal-diligence-coordination`
- `red-flags-scanner`
- `citation-enforcement`
