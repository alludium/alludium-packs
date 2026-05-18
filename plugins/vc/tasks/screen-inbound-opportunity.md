---
id: vc.screen_inbound_opportunity
title: Screen Inbound Opportunity
slug: screen-inbound-opportunity
agent: vc-dealflow-concierge
skills:
- company-research-and-enrichment
- red-flags-scanner
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/screen-inbound-opportunity.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Screen Inbound Opportunity

Screen Inbound Opportunity for one venture-capital opportunity with evidence capture, human review gates, and next-action recommendations.

## Instructions

Screen the inbound company against fund thesis and available deck or intro context; return fit recommendation, initial screening summary, gaps, red flags, pass feedback draft, and next actions. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Use workspace-configured scoring frameworks, CRM providers, stage names, and deal-type metric packs; do not assume a specific fund, CRM, or SaaS default unless the workspace configuration explicitly selects it. Create or update a durable project file artifact named First Look Scorecard and attach it to the required output field `first_look_scorecard_artifact_id`. Use `definitionJson.documentRefs` as the durable document reference contract; for refs with `outputFieldKey`, produce that output using the referenced pack document ID as the template or methodology source, and preserve the document ID alongside the output artifact.

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
| `referrer` | Referrer | `string` | no |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `first_look_scorecard_artifact_id` | First Look Scorecard | `file` | yes |
| `fit_recommendation` | Fit Recommendation | `string` | no |
| `initial_investment_screen_summary` | Initial Investment Screen Summary | `richtext` | no |
| `missing_information` | Missing Information | `string` | no |
| `red_flags` | Red Flags | `string` | no |
| `pass_feedback_draft` | Pass Feedback Draft | `string` | no |
| `next_actions` | Next Actions | `json` | no |
| `summary` | Summary | `richtext` | no |
| `recommendation` | Recommendation | `string` | no |
| `source_links` | Source Links | `string` | no |
| `assumptions` | Assumptions | `string` | no |
| `evidence_quality` | Evidence Quality | `json` | no |
| `open_questions` | Open Questions | `json` | no |
| `risks` | Risks | `json` | no |
| `human_decision_points` | Human Decision Points | `string` | no |

## Document References

- `vc.document.investment_screening_framework` (methodology) -> `first_look_scorecard_artifact_id`
- `vc.document.evidence_citation_style_guide` (style_guide)

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/screen-inbound-opportunity.yaml`
- Alludium task ID: `vc.screen_inbound_opportunity`
- Task family: `screening`
- Lifecycle stage: `assessment`
- Recommended agent: `vc-dealflow-concierge` (Alludium template `vc_dealflow_concierge`)
- Supported project types:
  - `vc_deal_room`

## Required Skills

- `company-research-and-enrichment`
- `red-flags-scanner`
- `citation-enforcement`

## Planned Skills

- `pitch-deck-explainer`
- `company-research-and-enrichment`
- `red-flags-scanner`
- `citation-enforcement`

## Workspace-Configured Methodology Skills

- `investment-screening-framework`: Use only when the workspace explicitly configures this screening framework.
