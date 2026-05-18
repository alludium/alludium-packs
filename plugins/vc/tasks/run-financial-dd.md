---
id: vc.run_financial_dd
title: Run Financial DD
slug: run-financial-dd
agent: vc-diligence-analyst
skills:
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/run-financial-dd.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Run Financial DD

Run Financial DD for one venture-capital opportunity with evidence capture, human review gates, and next-action recommendations.

## Instructions

Run financial diligence covering historicals, burn and runway, cap table, business-model economics, forecast stress test, use of funds, and financial risks from the supplied financial source artifact list. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Use workspace-configured scoring frameworks, CRM providers, stage names, and deal-type metric packs; do not assume a specific fund, CRM, or SaaS default unless the workspace configuration explicitly selects it. Create or update durable project file artifacts named Financial DD Report and Unit Economics Analysis, and attach them to the required output fields `financial_dd_artifact_id` and `unit_economics_artifact_id`. Use `definitionJson.documentRefs` as the durable document reference contract. Apply each reference by usage: `output_template` sets the output skeleton, `methodology` supplies scoring or analysis logic, `checklist` must be completed with status, evidence, and owner, `style_guide` governs citations and claim language, and `operating_guidance` or `policy` constrains process and approval boundaries. For refs with `outputFieldKey`, produce that output from the referenced pack document and preserve the document ID alongside the output artifact.

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
| `financial_source_artifact_ids` | Financial Source Artifact IDs | `string` | yes |
| `business_model` | Business Model | `string` | no |
| `cap_table` | Cap Table | `string` | no |
| `bank_statement_evidence` | Bank Statement Evidence | `json` | no |
| `use_of_funds_plan` | Use Of Funds Plan | `string` | no |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `financial_dd_artifact_id` | Financial DD Report | `file` | yes |
| `unit_economics_artifact_id` | Unit Economics Analysis | `file` | yes |
| `historicals_summary` | Historicals Summary | `richtext` | no |
| `burn_runway_analysis` | Burn Runway Analysis | `string` | no |
| `cap_table_summary` | Cap Table Summary | `richtext` | no |
| `business_model_economics` | Business Model Economics | `string` | no |
| `forecast_stress_test` | Forecast Stress Test | `string` | no |
| `use_of_funds_assessment` | Use Of Funds Assessment | `string` | no |
| `financial_risks` | Financial Risks | `json` | no |
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

- `vc.document.diligence_report_template` (output_template) -> `financial_dd_artifact_id`
- `vc.document.diligence_report_template` (output_template) -> `unit_economics_artifact_id`
- `vc.document.evidence_citation_style_guide` (style_guide)
- `vc.document.template_use_guidance` (operating_guidance)

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/run-financial-dd.yaml`
- Alludium task ID: `vc.run_financial_dd`
- Task family: `diligence`
- Lifecycle stage: `diligence`
- Recommended agent: `vc-diligence-analyst` (Alludium template `vc_diligence_analyst`)
- Supported project types:
  - `vc_deal_room`

## Required Skills

- `citation-enforcement`

## Planned Skills

- `financial-diligence-workstream`
- `citation-enforcement`

## Workspace-Configured Methodology Skills

- `traction-and-saas-unit-economics`: Use only for SaaS deals or workspaces that select this metric pack.
