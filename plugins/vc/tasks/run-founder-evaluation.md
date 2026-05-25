---
id: vc.run_founder_evaluation
title: Run Founder Evaluation
slug: run-founder-evaluation
agent: vc-diligence-analyst
skills:
- team-and-hiring-assessment
- red-flags-scanner
- citation-enforcement
- founder-evaluation-and-reference-checking
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/run-founder-evaluation.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Run Founder Evaluation

Run Founder Evaluation for one venture-capital opportunity with evidence capture, human review gates, and next-action recommendations.

## Instructions

Prepare founder dossier, reference plan, reference summaries when available, founder risk assessment, stop signals, and human-only judgment prompts. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Create or update a durable project file artifact named Founder Evaluation and attach it to the required output field `founder_evaluation_artifact_id`. Use `definitionJson.documentRefs` as the durable document reference contract. Apply each reference by usage: `output_template` sets the output skeleton, `methodology` supplies scoring or analysis logic, `checklist` must be completed with status, evidence, and owner, `style_guide` governs citations and claim language, and `operating_guidance` or `policy` constrains process and approval boundaries. For refs with `outputFieldKey`, produce that output from the referenced pack document and preserve the document ID alongside the output artifact.

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
| `founder_names` | Founder Names | `string` | yes |
| `linkedin_profiles` | Linkedin Profiles | `string` | yes |
| `reference_inputs` | Reference Inputs | `string` | no |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `founder_evaluation_artifact_id` | Founder Evaluation | `file` | yes |
| `founder_dossier` | Founder Dossier | `string` | no |
| `reference_plan` | Reference Plan | `string` | no |
| `reference_summaries` | Reference Summaries | `string` | no |
| `founder_risk_assessment` | Founder Risk Assessment | `string` | no |
| `human_only_judgment_prompts` | Human Only Judgment Prompts | `string` | no |
| `stop_signals` | Stop Signals | `string` | no |
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

- `vc.document.diligence_report_template` (output_template) -> `founder_evaluation_artifact_id`
- `vc.document.formal_diligence_workstream_guide` (methodology)
- `vc.document.formal_diligence_checklist` (checklist)
- `vc.document.evidence_citation_style_guide` (style_guide)
- `vc.document.template_use_guidance` (operating_guidance)

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/run-founder-evaluation.yaml`
- Alludium task ID: `vc.run_founder_evaluation`
- Task family: `diligence`
- Lifecycle stage: `formal_diligence`
- Recommended agent: `vc-diligence-analyst` (Alludium template `vc_diligence_analyst`)
- Supported project types:
  - `vc_deal_room`

## Required Skills

- `team-and-hiring-assessment`
- `red-flags-scanner`
- `citation-enforcement`
- `founder-evaluation-and-reference-checking`
