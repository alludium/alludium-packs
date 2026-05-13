---
id: vc.run_commercial_dd
title: Run Commercial DD
slug: run-commercial-dd
agent: vc-diligence-analyst
skills:
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/run-commercial-dd.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Run Commercial DD

Run Commercial DD for one venture-capital opportunity with evidence capture, human review gates, and next-action recommendations.

## Instructions

Run commercial diligence covering market sizing, competition, customer references where applicable, business-model-appropriate traction and economics, GTM/pricing where applicable, and commercial risks. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Use workspace-configured scoring frameworks, CRM providers, stage names, and deal-type metric packs; do not assume a specific fund, CRM, or SaaS default unless the workspace configuration explicitly selects it. Create or update durable project file artifacts named Commercial DD Report, Market Analysis, and Customer Reference Summary, and attach them to the required output fields `commercial_dd_artifact_id`, `market_analysis_artifact_id`, and `customer_reference_summary_artifact_id`.

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
| `company_name` | Company Name | `string` | yes |
| `business_model` | Business Model | `string` | no |
| `customer_or_user_evidence` | Customer Or User Evidence | `json` | no |
| `go_to_market_evidence` | Go To Market Evidence | `string` | no |
| `pricing_or_revenue_evidence` | Pricing Or Revenue Evidence | `string` | no |
| `market_sources` | Market Sources | `json` | no |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `commercial_dd_artifact_id` | Commercial DD Report | `file` | yes |
| `market_analysis_artifact_id` | Market Analysis | `file` | yes |
| `customer_reference_summary_artifact_id` | Customer Reference Summary | `file` | yes |
| `tam_sam_som_assessment` | Tam Sam Som Assessment | `string` | no |
| `competitive_landscape` | Competitive Landscape | `string` | no |
| `customer_reference_plan` | Customer Reference Plan | `string` | no |
| `reference_summaries` | Reference Summaries | `string` | no |
| `retention_or_repeat_usage_notes` | Retention Or Repeat Usage Notes | `richtext` | no |
| `gtm_and_business_model_assessment` | GTM And Business Model Assessment | `string` | no |
| `commercial_risks` | Commercial Risks | `json` | no |
| `summary` | Summary | `richtext` | no |
| `recommendation` | Recommendation | `string` | no |
| `source_links` | Source Links | `string` | no |
| `assumptions` | Assumptions | `string` | no |
| `evidence_quality` | Evidence Quality | `json` | no |
| `open_questions` | Open Questions | `json` | no |
| `risks` | Risks | `json` | no |
| `human_decision_points` | Human Decision Points | `string` | no |
| `next_actions` | Next Actions | `json` | no |

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/run-commercial-dd.yaml`
- Alludium task ID: `vc.run_commercial_dd`
- Task family: `diligence`
- Lifecycle stage: `diligence`
- Recommended agent: `vc-diligence-analyst` (Alludium template `vc_diligence_analyst`)
- Supported project types:
  - `vc_deal_room`

## Required Skills

- `citation-enforcement`

## Planned Skills

- `commercial-diligence-workstream`
- `citation-enforcement`

## Workspace-Configured Methodology Skills

- `market-map-building`: Use only when the workspace explicitly configures this market mapping method.
- `traction-and-saas-unit-economics`: Use only for SaaS deals or workspaces that select this metric pack.
