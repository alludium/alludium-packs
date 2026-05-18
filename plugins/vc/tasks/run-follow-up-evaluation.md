---
id: vc.run_follow_up_evaluation
title: Run Follow-Up Evaluation
slug: run-follow-up-evaluation
agent: vc-first-look-analyst
skills:
- red-flags-scanner
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/run-follow-up-evaluation.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Run Follow-Up Evaluation

Run Follow-Up Evaluation for one venture-capital opportunity with evidence capture, human review gates, and next-action recommendations.

## Instructions

Build the follow-up evaluation workspace with document requests, competitive landscape, early risks, and readiness recommendation. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Use workspace-configured scoring frameworks, CRM providers, stage names, and deal-type metric packs; do not assume a specific fund, CRM, or SaaS default unless the workspace configuration explicitly selects it. Create or update a durable project file artifact named Follow-Up Evaluation and attach it to the required output field `follow_up_evaluation_artifact_id`. Use `definitionJson.documentRefs` as the durable document reference contract; for refs with `outputFieldKey`, produce that output using the referenced pack document ID as the template or methodology source, and preserve the document ID alongside the output artifact.

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
| `first_look_scorecard_artifact_id` | First-Look Scorecard | `file` | yes |
| `customer_insights_artifact_id` | Customer Insights Summary | `file` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `follow_up_evaluation_artifact_id` | Follow-Up Evaluation | `file` | yes |

## Document References

- `vc.document.follow_up_evaluation_template` (output_template) -> `follow_up_evaluation_artifact_id`
- `vc.document.evidence_citation_style_guide` (style_guide)

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/run-follow-up-evaluation.yaml`
- Alludium task ID: `vc.run_follow_up_evaluation`
- Task family: `diligence`
- Lifecycle stage: `assessment`
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

- `82-factor-diligence-question-generation`: Use only when the workspace explicitly configures this diligence framework.
- `market-map-building`: Use only when the workspace explicitly configures this market mapping method.
