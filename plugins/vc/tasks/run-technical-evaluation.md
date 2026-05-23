---
id: vc.run_technical_evaluation
title: Run Technical Evaluation
slug: run-technical-evaluation
agent: vc-first-look-analyst
skills:
- technical-evaluation-and-product-risk
- red-flags-scanner
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/run-technical-evaluation.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Run Technical Evaluation

Run an evaluation-stage technical and product workstream for one venture-capital opportunity, identifying product evidence, technical risk, and next proof needed before formal diligence.

## Instructions

Run a technical evaluation covering product depth, architecture plausibility, technical edge, IP or data defensibility, roadmap realism, technical team coverage, and technical gating risk. Use this as evaluation-stage work, not formal technical diligence, code review, security review, expert validation, or IP clearance. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Create or update a durable project file artifact named Technical Evaluation and attach it to the required output field `technical_evaluation_artifact_id`. Use `definitionJson.documentRefs` as the durable document reference contract. Apply each reference by usage: `output_template` sets the output skeleton, `methodology` supplies scoring or analysis logic, `checklist` must be completed with status, evidence, and owner, `style_guide` governs citations and claim language, and `operating_guidance` or `policy` constrains process and approval boundaries. For refs with `outputFieldKey`, produce that output from the referenced pack document and preserve the document ID alongside the output artifact.

## Missing Input Policy

Ask for the company name and at least one relevant source such as a deck, product demo notes, product materials, architecture claims, roadmap, IP/data narrative, or technical team context before producing the evaluation.

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
| `product_or_technical_evidence` | Product Or Technical Evidence | `json` | no |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `technical_evaluation_artifact_id` | Technical Evaluation | `file` | yes |
| `main_technical_hypothesis` | Main Technical Hypothesis | `richtext` | no |
| `technical_gating_risk` | Technical Gating Risk | `richtext` | no |
| `next_technical_proof_needed` | Next Technical Proof Needed | `richtext` | no |

## Document References

- `vc.document.technical_evaluation_template` (output_template) -> `technical_evaluation_artifact_id`
- `vc.document.evaluation_workstream_guide` (methodology)
- `vc.document.technical_evaluation_guide` (methodology)
- `vc.document.opportunity_evaluation_framework` (methodology)
- `vc.document.evidence_citation_style_guide` (style_guide)
- `vc.document.template_use_guidance` (operating_guidance)

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/run-technical-evaluation.yaml`
- Alludium task ID: `vc.run_technical_evaluation`
- Task family: `evaluation`
- Lifecycle stage: `evaluation`
- Recommended agent: `vc-first-look-analyst` (Alludium template `vc_first_look_analyst`)
- Supported project types:
  - `vc_deal_room`

## Required Skills

- `technical-evaluation-and-product-risk`
- `red-flags-scanner`
- `citation-enforcement`
