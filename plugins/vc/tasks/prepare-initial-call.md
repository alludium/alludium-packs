---
id: vc.prepare_initial_call
title: Prepare Initial Call
slug: prepare-initial-call
agent: vc-meeting-operator
skills:
- meeting-prep-and-summary
- company-research-and-enrichment
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/prepare-initial-call.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Prepare Initial Call

Prepare Initial Call for one venture-capital opportunity with evidence capture, human review gates, and next-action recommendations.

## Instructions

Prepare the first-call brief, founder and company summary, competitor and funding activity, starter Initial investment screen scorecard, and questions by topic. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Use workspace-configured scoring frameworks, CRM providers, stage names, and deal-type metric packs; do not assume a specific fund, CRM, or SaaS default unless the workspace configuration explicitly selects it. Create or update a durable project file artifact named Initial Call Brief and attach it to the required output field `initial_call_brief_artifact_id`. Use `definitionJson.documentRefs` as the durable document reference contract; for refs with `outputFieldKey`, produce that output using the referenced pack document ID as the template or methodology source, and preserve the document ID alongside the output artifact.

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
| `founder_names` | Founder Names | `string` | no |
| `meeting_datetime` | Meeting Datetime | `string` | no |
| `deal_room_url` | Deal Room Url | `string` | no |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `initial_call_brief_artifact_id` | Initial Call Brief | `file` | yes |
| `pre_call_brief` | Pre Call Brief | `richtext` | no |
| `founder_company_summary` | Founder Company Summary | `richtext` | no |
| `competitor_funding_activity` | Competitor Funding Activity | `string` | no |
| `starter_investment_screen_scorecard` | Starter Investment Screen Scorecard | `string` | no |
| `questions_by_topic` | Questions By Topic | `json` | no |
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

- `vc.document.initial_call_brief_template` (output_template) -> `initial_call_brief_artifact_id`
- `vc.document.evidence_citation_style_guide` (style_guide)

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/prepare-initial-call.yaml`
- Alludium task ID: `vc.prepare_initial_call`
- Task family: `meeting`
- Lifecycle stage: `assessment`
- Recommended agent: `vc-meeting-operator` (Alludium template `vc_meeting_operator`)
- Supported project types:
  - `vc_deal_room`

## Required Skills

- `meeting-prep-and-summary`
- `company-research-and-enrichment`
- `citation-enforcement`

## Planned Skills

- `meeting-prep-and-summary`
- `company-research-and-enrichment`
- `pitch-deck-explainer`
- `citation-enforcement`

## Workspace-Configured Methodology Skills

- `ten-factor-evaluation`: Use only when the workspace explicitly configures this screening framework.
