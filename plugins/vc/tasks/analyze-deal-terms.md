---
id: vc.analyze_deal_terms
title: Analyze Deal Terms
slug: analyze-deal-terms
agent: vc-legal-compliance-desk
skills:
- deal-terms-analysis
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/analyze-deal-terms.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Analyze Deal Terms

Analyze proposed venture deal economics, ownership, dilution, ESOP, and commercial open terms without providing legal advice or approving terms.

## Instructions

Analyze the proposed investment amount, valuation, round size, cap table, ownership target, ESOP, co-investors, and reserve policy as commercial deal economics. Model ownership, dilution, valuation sensitivity, and open commercial terms only from supplied evidence. Cite material claims, separate assumptions from evidence, and do not provide legal advice, negotiate terms, approve terms, send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Create or update a durable project file artifact named Deal Terms Analysis and attach it to the required output field `deal_terms_analysis_artifact_id`. Use `definitionJson.documentRefs` as the durable document reference contract. Apply each reference by usage: `output_template` sets the output skeleton, `methodology` supplies scoring or analysis logic, `checklist` must be completed with status, evidence, and owner, `style_guide` governs citations and claim language, and `operating_guidance` or `policy` constrains process and approval boundaries. For refs with `outputFieldKey`, produce that output from the referenced pack document and preserve the document ID alongside the output artifact.

## Missing Input Policy

Ask for missing required economics inputs before producing ownership, valuation, or reserve conclusions.

## External Action Policy

Draft only unless a human explicitly approves the send, CRM write, Drive change, project creation, child task creation, or stage transition.

## Completion Criteria

- Required input gaps are resolved or listed as assumptions/open questions.
- Material economics conclusions include source links or are labeled as human judgment calls.
- Open terms and IC questions identify owner, dependency, and required human approval point.

## Human Decision Points

- Approve valuation, ownership, ESOP, reserve, term-sheet, and investment-stage recommendations.
- Approve external communications, CRM writes, Drive/project creation, legal/counsel actions, and founder-facing requests.

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `proposed_investment_amount` | Proposed Investment Amount | `string` | yes |
| `valuation` | Valuation | `string` | yes |
| `round_size` | Round Size | `string` | yes |
| `cap_table_artifact_id` | Cap Table | `file` | yes |
| `esop` | ESOP | `string` | no |
| `co_investors` | Co-investors | `json` | no |
| `ownership_target` | Ownership Target | `string` | no |
| `follow_on_reserve_policy` | Follow-on Reserve Policy | `richtext` | no |
| `deal_terms_snapshot` | Deal Terms Snapshot | `json` | no |
| `financial_forecast_artifact_id` | Financial Forecast | `file` | no |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `deal_terms_analysis_artifact_id` | Deal Terms Analysis | `file` | yes |
| `ownership_model_summary` | Ownership Model Summary | `richtext` | no |
| `valuation_sensitivity` | Valuation Sensitivity | `json` | no |
| `open_commercial_terms` | Open Commercial Terms | `json` | no |
| `ic_questions` | IC Questions | `json` | no |
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

- `vc.document.deal_terms_analysis_template` (output_template) -> `deal_terms_analysis_artifact_id`
- `vc.document.evidence_citation_style_guide` (style_guide)
- `vc.document.template_use_guidance` (operating_guidance)

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/analyze-deal-terms.yaml`
- Alludium task ID: `vc.analyze_deal_terms`
- Task family: `deal_structuring`
- Lifecycle stage: `deal_structuring`
- Recommended agent: `vc-legal-compliance-desk` (Alludium template `vc_legal_compliance_desk`)
- Supported project types:
  - `vc_deal_room`

## Required Skills

- `deal-terms-analysis`
- `citation-enforcement`
