---
id: vc.generate_diligence_questions
title: Generate Diligence Questions
slug: generate-diligence-questions
agent: vc-evaluation-analyst
skills:
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/generate-diligence-questions.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Generate Diligence Questions

Generate a structured investment diligence question bank for one venture-capital opportunity with evidence capture, human review gates, and next-action recommendations.

## Instructions

Generate prioritized investment diligence questions with rationale, source gap, owner, and urgency. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Use workspace-configured scoring frameworks, CRM providers, stage names, and deal-type metric packs; do not assume a specific fund, CRM, or SaaS default unless the workspace configuration explicitly selects it. Create or update a durable project file artifact named Structured Diligence Question Bank and attach it to the required output field `diligence_question_bank_artifact_id`. Use `definitionJson.documentRefs` as the durable document reference contract. Apply each reference by usage: `output_template` sets the output skeleton, `methodology` supplies scoring or analysis logic, `checklist` must be completed with status, evidence, and owner, `style_guide` governs citations and claim language, and `operating_guidance` or `policy` constrains process and approval boundaries. For refs with `outputFieldKey`, produce that output from the referenced pack document and preserve the document ID alongside the output artifact.

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
| `known_claims` | Known Claims | `string` | yes |
| `existing_answers` | Existing Answers | `string` | no |
| `priority_workstreams` | Priority Workstreams | `string` | no |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `diligence_question_bank_artifact_id` | Structured Diligence Question Bank | `file` | yes |
| `question_set` | Question Set | `string` | no |
| `rationale` | Rationale | `string` | no |
| `source_gap` | Source Gap | `string` | no |
| `owner` | Owner | `string` | no |
| `urgency` | Urgency | `string` | no |
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

- `vc.document.investment_diligence_question_framework` (methodology) -> `diligence_question_bank_artifact_id`
- `vc.document.opportunity_evaluation_framework` (methodology)
- `vc.document.evaluation_workstream_guide` (methodology)
- `vc.document.commercial_evaluation_guide` (methodology)
- `vc.document.technical_evaluation_guide` (methodology)
- `vc.document.financial_evaluation_guide` (methodology)
- `vc.document.formal_diligence_workstream_guide` (methodology)
- `vc.document.formal_diligence_checklist` (checklist)
- `vc.document.legal_diligence_guide` (methodology)
- `vc.document.evidence_citation_style_guide` (style_guide)
- `vc.document.template_use_guidance` (operating_guidance)

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/generate-diligence-questions.yaml`
- Alludium task ID: `vc.generate_diligence_questions`
- Task family: `diligence`
- Lifecycle stage: `evaluation`
- Recommended agent: `vc-evaluation-analyst` (Alludium template `vc_evaluation_analyst`)
- Supported project types:
  - `vc_deal_room`

## Required Skills

- `citation-enforcement`

## Workspace-Configured Methodology Skills

- `investment-diligence-question-framework`: Use only when the workspace explicitly configures this diligence framework.
