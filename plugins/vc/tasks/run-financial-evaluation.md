---
id: vc.run_financial_evaluation
title: Run Financial Evaluation
slug: run-financial-evaluation
agent: vc-first-look-analyst
skills:
- financial-evaluation-and-financing-risk
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/run-financial-evaluation.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Run Financial Evaluation

Run an evaluation-stage financial and financing workstream for one venture-capital opportunity, identifying model evidence, financing risk, and next proof needed before formal diligence.

## Instructions

Run a financial evaluation covering business model, forecast plausibility, revenue quality, burn, runway, use of funds, valuation, ownership, financing path, and financial gating risk. Use this as evaluation-stage work, not formal financial diligence, accounting advice, tax advice, or legal advice. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Create or update a durable project file artifact named Financial Evaluation and attach it to the required output field `financial_evaluation_artifact_id`. Use `definitionJson.documentRefs` as the durable document reference contract. Apply each reference by usage: `output_template` sets the output skeleton, `methodology` supplies scoring or analysis logic, `checklist` must be completed with status, evidence, and owner, `style_guide` governs citations and claim language, and `operating_guidance` or `policy` constrains process and approval boundaries. For refs with `outputFieldKey`, produce that output from the referenced pack document and preserve the document ID alongside the output artifact.

## Missing Input Policy

Ask for the company name and at least one relevant source such as a deck, screen, model extract, burn/runway context, valuation or cap-table context, revenue evidence, pricing notes, or use-of-funds narrative before producing the evaluation.

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
| `follow_up_evaluation_artifact_id` | Opportunity Evaluation | `file` | no |
| `opportunity_evidence_artifact_ids` | Opportunity Evidence Artifacts | `json` | no |
| `financial_or_financing_evidence` | Financial Or Financing Evidence | `json` | no |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `financial_evaluation_artifact_id` | Financial Evaluation | `file` | yes |
| `main_financial_hypothesis` | Main Financial Hypothesis | `richtext` | no |
| `financial_gating_risk` | Financial Gating Risk | `richtext` | no |
| `next_financial_proof_needed` | Next Financial Proof Needed | `richtext` | no |

## Document References

- `vc.document.financial_evaluation_template` (output_template) -> `financial_evaluation_artifact_id`
- `vc.document.evaluation_workstream_guide` (methodology)
- `vc.document.financial_evaluation_guide` (methodology)
- `vc.document.opportunity_evaluation_framework` (methodology)
- `vc.document.evidence_citation_style_guide` (style_guide)
- `vc.document.template_use_guidance` (operating_guidance)

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/run-financial-evaluation.yaml`
- Alludium task ID: `vc.run_financial_evaluation`
- Task family: `evaluation`
- Lifecycle stage: `evaluation`
- Recommended agent: `vc-first-look-analyst` (Alludium template `vc_first_look_analyst`)
- Supported project types:
  - `vc_deal_room`

## Required Skills

- `financial-evaluation-and-financing-risk`
- `citation-enforcement`

## Workspace-Configured Methodology Skills

- `traction-and-saas-unit-economics`: Use only for SaaS deals or workspaces that select this metric pack.
