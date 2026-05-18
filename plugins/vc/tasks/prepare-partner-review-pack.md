---
id: vc.prepare_partner_review_pack
title: Prepare Partner Review Pack
slug: prepare-partner-review-pack
agent: vc-diligence-analyst
skills:
- ic-memo-assembly
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/prepare-partner-review-pack.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Prepare Partner Review Pack

Prepare Partner Review Pack for one venture-capital opportunity with evidence capture, human review gates, and next-action recommendations.

## Instructions

Prepare the Partner Review pack with investment thesis, strategic fit, proposed DD scope, workstream owners, key risks, and decision ask. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Use workspace-configured scoring frameworks, CRM providers, stage names, and deal-type metric packs; do not assume a specific fund, CRM, or SaaS default unless the workspace configuration explicitly selects it. Use the required input file artifacts `commercial_dd_artifact_id`, `financial_dd_artifact_id`, `founder_evaluation_artifact_id`, `technical_dd_artifact_id`, and `diligence_question_bank_artifact_id` as the review subjects for the partner review pack. Use the required input file artifact `team_review_pack_artifact_id` as the team review pack being escalated to partner review. Create or update a durable project file artifact named Partner Review Pack and attach it to the required output field `partner_review_pack_artifact_id`. Use `definitionJson.documentRefs` as the durable document reference contract. Apply each reference by usage: `output_template` sets the output skeleton, `methodology` supplies scoring or analysis logic, `checklist` must be completed with status, evidence, and owner, `style_guide` governs citations and claim language, and `operating_guidance` or `policy` constrains process and approval boundaries. For refs with `outputFieldKey`, produce that output from the referenced pack document and preserve the document ID alongside the output artifact.

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
| `team_review_pack_artifact_id` | Team Review Pack | `file` | yes |
| `commercial_dd_artifact_id` | Commercial DD Report | `file` | yes |
| `financial_dd_artifact_id` | Financial DD Report | `file` | yes |
| `founder_evaluation_artifact_id` | Founder Evaluation | `file` | yes |
| `technical_dd_artifact_id` | Technical DD Report | `file` | yes |
| `diligence_question_bank_artifact_id` | Structured Diligence Question Bank | `file` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `partner_review_pack_artifact_id` | Partner Review Pack | `file` | yes |
| `investment_thesis_summary` | Investment Thesis Summary | `richtext` | no |
| `strategic_fit` | Strategic Fit | `string` | no |
| `proposed_dd_scope` | Proposed Dd Scope | `string` | no |
| `workstream_owners` | Workstream Owners | `json` | no |
| `key_risks` | Key Risks | `json` | no |
| `decision_ask` | Decision Ask | `string` | no |
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

- `vc.document.review_pack_checklist` (output_template) -> `partner_review_pack_artifact_id`
- `vc.document.evidence_citation_style_guide` (style_guide)
- `vc.document.template_use_guidance` (operating_guidance)

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/prepare-partner-review-pack.yaml`
- Alludium task ID: `vc.prepare_partner_review_pack`
- Task family: `diligence`
- Lifecycle stage: `review`
- Recommended agent: `vc-diligence-analyst` (Alludium template `vc_diligence_analyst`)
- Supported project types:
  - `vc_deal_room`

## Required Skills

- `ic-memo-assembly`
- `citation-enforcement`

## Planned Skills

- `ic-memo-assembly`
- `citation-enforcement`

## Workspace-Configured Methodology Skills

- `market-map-building`: Use only when the workspace explicitly configures this market mapping method.
