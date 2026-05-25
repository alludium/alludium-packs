---
id: vc.prepare_team_review_pack
title: Prepare Team Review Pack
slug: prepare-team-review-pack
agent: vc-diligence-analyst
skills:
- ic-memo-assembly
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/prepare-team-review-pack.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Prepare Team Review Pack

Prepare Team Review Pack for one venture-capital opportunity with evidence capture, human review gates, and next-action recommendations.

## Instructions

Assemble the Team Review pack from evaluation-stage workstream outputs, the diligence question bank, available formal diligence outputs, evidence summary, founder risks, and stage-gate recommendation. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Use required evaluation input file artifacts `commercial_evaluation_artifact_id`, `technical_evaluation_artifact_id`, `financial_evaluation_artifact_id`, `team_evaluation_artifact_id`, and `diligence_question_bank_artifact_id` as the decision-review source set. Use formal diligence artifacts `commercial_dd_artifact_id`, `financial_dd_artifact_id`, `founder_evaluation_artifact_id`, and `technical_dd_artifact_id` when present, but do not block evaluation-stage review on them. Create or update a durable project file artifact named Team Review Pack and attach it to the required output field `team_review_pack_artifact_id`. Use `definitionJson.documentRefs` as the durable document reference contract. Apply each reference by usage: `output_template` sets the output skeleton, `methodology` supplies scoring or analysis logic, `checklist` must be completed with status, evidence, and owner, `style_guide` governs citations and claim language, and `operating_guidance` or `policy` constrains process and approval boundaries. For refs with `outputFieldKey`, produce that output from the referenced pack document and preserve the document ID alongside the output artifact.

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
| `commercial_evaluation_artifact_id` | Commercial Evaluation | `file` | yes |
| `technical_evaluation_artifact_id` | Technical Evaluation | `file` | yes |
| `financial_evaluation_artifact_id` | Financial Evaluation | `file` | yes |
| `team_evaluation_artifact_id` | Team Evaluation | `file` | yes |
| `diligence_question_bank_artifact_id` | Structured Diligence Question Bank | `file` | yes |
| `commercial_dd_artifact_id` | Commercial DD Report | `file` | no |
| `financial_dd_artifact_id` | Financial DD Report | `file` | no |
| `founder_evaluation_artifact_id` | Founder Evaluation | `file` | no |
| `technical_dd_artifact_id` | Technical DD Report | `file` | no |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `team_review_pack_artifact_id` | Team Review Pack | `file` | yes |
| `company_snapshot` | Company Snapshot | `json` | no |
| `evidence_summary` | Evidence Summary | `richtext` | no |
| `screening_and_diligence_summary` | Initial Screening And Diligence Summary | `richtext` | no |
| `founder_risk_summary` | Founder Risk Summary | `richtext` | no |
| `stage_gate_recommendation` | Stage Gate Recommendation | `string` | no |
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

- `vc.document.review_pack_checklist` (output_template) -> `team_review_pack_artifact_id`
- `vc.document.opportunity_evaluation_framework` (methodology)
- `vc.document.evaluation_workstream_guide` (methodology)
- `vc.document.formal_diligence_workstream_guide` (methodology)
- `vc.document.formal_diligence_checklist` (checklist)
- `vc.document.evidence_citation_style_guide` (style_guide)
- `vc.document.template_use_guidance` (operating_guidance)

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/prepare-team-review-pack.yaml`
- Alludium task ID: `vc.prepare_team_review_pack`
- Task family: `diligence`
- Lifecycle stage: `decision_review`
- Recommended agent: `vc-diligence-analyst` (Alludium template `vc_diligence_analyst`)
- Supported project types:
  - `vc_deal_room`

## Required Skills

- `ic-memo-assembly`
- `citation-enforcement`

## Workspace-Configured Methodology Skills

- `investment-diligence-question-framework`: Use only when the workspace explicitly configures this diligence framework.
