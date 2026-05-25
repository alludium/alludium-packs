---
id: vc.run_commercial_evaluation
title: Run Commercial Evaluation
slug: run-commercial-evaluation
agent: vc-evaluation-analyst
skills:
- commercial-evaluation-and-market-risk
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/run-commercial-evaluation.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Run Commercial Evaluation

Run an evaluation-stage commercial workstream for one venture-capital opportunity, identifying market/customer evidence, GTM risk, and next proof needed before formal diligence.

## Instructions

Run a commercial evaluation covering customer segment, pain urgency, budget, pricing, GTM path, competition, lightweight market sizing, and commercial gating risk. Use this as evaluation-stage work, not formal commercial diligence. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Create or update a durable project file artifact named Commercial Evaluation and attach it to the required output field `commercial_evaluation_artifact_id`. Use `definitionJson.documentRefs` as the durable document reference contract. Apply each reference by usage: `output_template` sets the output skeleton, `methodology` supplies scoring or analysis logic, `checklist` must be completed with status, evidence, and owner, `style_guide` governs citations and claim language, and `operating_guidance` or `policy` constrains process and approval boundaries. For refs with `outputFieldKey`, produce that output from the referenced pack document and preserve the document ID alongside the output artifact.

## Missing Input Policy

Ask for the company name and at least one relevant source such as a deck, screen, call notes, customer evidence, pricing context, GTM notes, pipeline evidence, or market source before producing the evaluation.

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
| `customer_or_market_evidence` | Customer Or Market Evidence | `json` | no |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `commercial_evaluation_artifact_id` | Commercial Evaluation | `file` | yes |
| `main_commercial_hypothesis` | Main Commercial Hypothesis | `richtext` | no |
| `commercial_gating_risk` | Commercial Gating Risk | `richtext` | no |
| `next_commercial_proof_needed` | Next Commercial Proof Needed | `richtext` | no |

## Document References

- `vc.document.commercial_evaluation_template` (output_template) -> `commercial_evaluation_artifact_id`
- `vc.document.evaluation_workstream_guide` (methodology)
- `vc.document.commercial_evaluation_guide` (methodology)
- `vc.document.opportunity_evaluation_framework` (methodology)
- `vc.document.evidence_citation_style_guide` (style_guide)
- `vc.document.template_use_guidance` (operating_guidance)

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/run-commercial-evaluation.yaml`
- Alludium task ID: `vc.run_commercial_evaluation`
- Task family: `evaluation`
- Lifecycle stage: `evaluation`
- Recommended agent: `vc-evaluation-analyst` (Alludium template `vc_evaluation_analyst`)
- Supported project types:
  - `vc_deal_room`

## Required Skills

- `commercial-evaluation-and-market-risk`
- `citation-enforcement`

## Workspace-Configured Methodology Skills

- `market-map-building`: Use only when the workspace explicitly configures this market mapping method.
