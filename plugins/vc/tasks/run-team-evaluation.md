---
id: vc.run_team_evaluation
title: Run Team Evaluation
slug: run-team-evaluation
agent: vc-evaluation-analyst
skills:
- team-evaluation-and-founder-risk
- red-flags-scanner
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/run-team-evaluation.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Run Team Evaluation

Run an evaluation-stage team and founder workstream for one venture-capital opportunity, identifying founder evidence, role gaps, team risk, and next proof needed before formal diligence.

## Instructions

Run a team evaluation covering founder-market fit, role coverage, relevant experience, execution evidence, integrity or consistency signals, hiring gaps, adviser or board quality, reference needs, and team gating risk. Use this as evaluation-stage work, not formal founder diligence, completed reference checking, or background checking. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Create or update a durable project file artifact named Team Evaluation and attach it to the required output field `team_evaluation_artifact_id`. Use `definitionJson.documentRefs` as the durable document reference contract. Apply each reference by usage: `output_template` sets the output skeleton, `methodology` supplies scoring or analysis logic, `checklist` must be completed with status, evidence, and owner, `style_guide` governs citations and claim language, and `operating_guidance` or `policy` constrains process and approval boundaries. For refs with `outputFieldKey`, produce that output from the referenced pack document and preserve the document ID alongside the output artifact.

## Missing Input Policy

Ask for the company name and at least one relevant source such as founder names, founder materials, public profiles, meeting notes, team page, hiring plan, relationship context, or reference notes before producing the evaluation.

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
| `team_or_founder_evidence` | Team Or Founder Evidence | `json` | no |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `team_evaluation_artifact_id` | Team Evaluation | `file` | yes |
| `main_team_hypothesis` | Main Team Hypothesis | `richtext` | no |
| `team_gating_risk` | Team Gating Risk | `richtext` | no |
| `next_team_proof_needed` | Next Team Proof Needed | `richtext` | no |

## Document References

- `vc.document.team_evaluation_template` (output_template) -> `team_evaluation_artifact_id`
- `vc.document.evaluation_workstream_guide` (methodology)
- `vc.document.opportunity_evaluation_framework` (methodology)
- `vc.document.evidence_citation_style_guide` (style_guide)
- `vc.document.template_use_guidance` (operating_guidance)

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/run-team-evaluation.yaml`
- Alludium task ID: `vc.run_team_evaluation`
- Task family: `evaluation`
- Lifecycle stage: `evaluation`
- Recommended agent: `vc-evaluation-analyst` (Alludium template `vc_evaluation_analyst`)
- Supported project types:
  - `vc_deal_room`

## Required Skills

- `team-evaluation-and-founder-risk`
- `red-flags-scanner`
- `citation-enforcement`
