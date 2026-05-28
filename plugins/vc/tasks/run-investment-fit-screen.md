---
id: vc.run_investment_screen
title: Run Investment Fit Screen
slug: run-investment-fit-screen
agent: vc-first-look-analyst
skills:
- investment-screening-framework
- red-flags-scanner
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/run-investment-fit-screen.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Run Investment Fit Screen

Run a fast investment fit screen for one venture-capital opportunity using configured criteria, available evidence, human review gates, and next-action recommendations.

## Instructions

Score each configured investment-fit criterion with rationale, source links, unknowns, red flags, and human-review prompts before recommending continue, watch, or pass. Use a pitch deck, source material, source thread, opportunity intake artifact, meeting notes, or source links as evidence; do not require a pitch deck when another source is sufficient. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Use workspace-configured scoring frameworks, CRM providers, stage names, and deal-type metric packs; do not assume a specific fund, CRM, or SaaS default unless the workspace configuration explicitly selects it. Create or update a durable project file artifact named Investment Fit Screen Scorecard and attach it to the required output field `investment_screen_scorecard_artifact_id`. Use `definitionJson.documentRefs` as the durable document reference contract. Apply each reference by usage: `output_template` sets the output skeleton, `methodology` supplies scoring or analysis logic, `checklist` must be completed with status, evidence, and owner, `style_guide` governs citations and claim language, and `operating_guidance` or `policy` constrains process and approval boundaries. For refs with `outputFieldKey`, produce that output from the referenced pack document and preserve the document ID alongside the output artifact.

## Missing Input Policy

Ask for at least one evidence source before producing an investment fit recommendation.

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
| `pitch_deck_artifact_id` | Pitch Deck Artifact | `file` | no |
| `meeting_notes` | Meeting Notes | `richtext` | no |
| `source_links` | Source Links | `string` | no |
| `opportunity_intake_artifact_id` | Opportunity Intake Summary | `file` | no |
| `source_material_artifact_ids` | Source Material Artifact IDs | `string` | no |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `investment_screen_scorecard_artifact_id` | Investment Fit Screen Scorecard | `file` | yes |
| `factor_scores` | Criterion Scores | `json` | no |
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

## Document References

- `vc.document.investment_screening_framework` (methodology) -> `investment_screen_scorecard_artifact_id`
- `vc.document.evidence_citation_style_guide` (style_guide)
- `vc.document.template_use_guidance` (operating_guidance)

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/run-investment-fit-screen.yaml`
- Alludium task ID: `vc.run_investment_screen`
- Task family: `screening`
- Lifecycle stage: `screening`
- Recommended agent: `vc-first-look-analyst` (Alludium template `vc_first_look_analyst`)
- Supported project types:
  - `vc_deal_room`

## Required Skills

- `investment-screening-framework`
- `red-flags-scanner`
- `citation-enforcement`

## Workspace-Configured Methodology Skills

- `investment-screening-framework`: Use only when the workspace explicitly configures this screening framework.
