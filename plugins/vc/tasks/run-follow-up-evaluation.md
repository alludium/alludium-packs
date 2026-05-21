---
id: vc.run_follow_up_evaluation
title: Run Opportunity Evaluation
slug: run-follow-up-evaluation
agent: vc-first-look-analyst
skills:
- red-flags-scanner
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/run-follow-up-evaluation.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Run Opportunity Evaluation

Run a deeper opportunity evaluation after screening for one venture-capital opportunity with evidence capture, human review gates, and next-action recommendations.

## Instructions

Build an opportunity evaluation from the investment fit screen, meeting records, founder materials, customer evidence, market sources, technical sources, financial sources, and existing questions. Produce a deeper evaluation scorecard, key claims register, critical unknowns, initial diligence recommendations, and recommended decision path. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Use workspace-configured scoring frameworks, CRM providers, stage names, and deal-type metric packs; do not assume a specific fund, CRM, or SaaS default unless the workspace configuration explicitly selects it. Create or update a durable project file artifact named Opportunity Evaluation and attach it to the required output field `follow_up_evaluation_artifact_id`. Use `definitionJson.documentRefs` as the durable document reference contract. Apply each reference by usage: `output_template` sets the output skeleton, `methodology` supplies scoring or analysis logic, `checklist` must be completed with status, evidence, and owner, `style_guide` governs citations and claim language, and `operating_guidance` or `policy` constrains process and approval boundaries. For refs with `outputFieldKey`, produce that output from the referenced pack document and preserve the document ID alongside the output artifact.

## Missing Input Policy

Ask for the investment screen and at least one meeting, founder-material, customer, market, technical, or financial evidence source before producing the evaluation.

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
| `investment_screen_scorecard_artifact_id` | Investment Fit Screen Scorecard | `file` | yes |
| `customer_insights_artifact_id` | Meeting Records Summary | `file` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `follow_up_evaluation_artifact_id` | Opportunity Evaluation | `file` | yes |

## Document References

- `vc.document.follow_up_evaluation_template` (output_template) -> `follow_up_evaluation_artifact_id`
- `vc.document.evidence_citation_style_guide` (style_guide)
- `vc.document.template_use_guidance` (operating_guidance)

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/run-follow-up-evaluation.yaml`
- Alludium task ID: `vc.run_follow_up_evaluation`
- Task family: `evaluation`
- Lifecycle stage: `evaluation`
- Recommended agent: `vc-first-look-analyst` (Alludium template `vc_first_look_analyst`)
- Supported project types:
  - `vc_deal_room`

## Required Skills

- `red-flags-scanner`
- `citation-enforcement`

## Planned Skills

- `red-flags-scanner`
- `citation-enforcement`

## Workspace-Configured Methodology Skills

- `investment-diligence-question-framework`: Use only when the workspace explicitly configures this diligence framework.
- `market-map-building`: Use only when the workspace explicitly configures this market mapping method.
