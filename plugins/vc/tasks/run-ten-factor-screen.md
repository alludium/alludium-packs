---
id: vc.run_ten_factor_screen
title: Run 10-Factor Screen
slug: run-ten-factor-screen
agent: vc-first-look-analyst
skills:
- red-flags-scanner
- citation-enforcement
---

# Run 10-Factor Screen

Run 10-Factor Screen for one venture-capital opportunity with evidence capture, human review gates, and next-action recommendations.

## Instructions

Score each 10-Factor criterion with rationale, source links, unknowns, and human-review prompts before recommending continue or pass. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Use workspace-configured scoring frameworks, CRM providers, stage names, and deal-type metric packs; do not assume a specific fund, CRM, or SaaS default unless the workspace configuration explicitly selects it. Create or update a durable project file artifact named Ten Factor Scorecard and attach it to the required output field `ten_factor_scorecard_artifact_id`.

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
| `pitch_deck_artifact_id` | Pitch Deck Artifact | `file` | yes |
| `meeting_notes` | Meeting Notes | `richtext` | no |
| `source_links` | Source Links | `string` | no |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `ten_factor_scorecard_artifact_id` | Ten Factor Scorecard | `file` | yes |
| `factor_scores` | Factor Scores | `json` | no |
| `overall_recommendation` | Overall Recommendation | `string` | no |
| `source_links` | Source Links | `string` | no |
| `unknowns` | Unknowns | `string` | no |
| `human_review_prompts` | Human Review Prompts | `string` | no |
| `summary` | Summary | `richtext` | no |
| `recommendation` | Recommendation | `string` | no |
| `assumptions` | Assumptions | `string` | no |
| `evidence_quality` | Evidence Quality | `json` | no |
| `open_questions` | Open Questions | `json` | no |
| `risks` | Risks | `json` | no |
| `human_decision_points` | Human Decision Points | `string` | no |
| `next_actions` | Next Actions | `json` | no |

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/run-ten-factor-screen.yaml`
- Alludium task ID: `vc.run_ten_factor_screen`
- Task family: `screening`
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

- `ten-factor-evaluation`: Use only when the workspace explicitly configures this screening framework.
