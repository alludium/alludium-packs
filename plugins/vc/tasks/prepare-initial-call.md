---
id: vc.prepare_initial_call
title: Prepare Meeting
slug: prepare-initial-call
agent: vc-meeting-operator
skills:
- meeting-prep-and-summary
- company-research-and-enrichment
- citation-enforcement
- pitch-deck-explainer
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/prepare-initial-call.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Prepare Meeting

Prepare a founder, management, advisor, customer, expert, partner, IC, legal, or closing meeting for one venture-capital opportunity with evidence capture, human review gates, and next-action recommendations.

## Instructions

Prepare the meeting brief, relationship context, concise company and evidence summary, stage-relevant agenda, risk prompts, and questions by topic for the requested meeting type. Use the pitch deck, prior task artifacts, meeting goal, calendar context, CRM context, or other supplied source material when available, but do not require a pitch deck when another evidence source is sufficient. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Use workspace-configured scoring frameworks, CRM providers, stage names, and deal-type metric packs; do not assume a specific fund, CRM, or SaaS default unless the workspace configuration explicitly selects it. Create or update a durable project file artifact named Meeting Brief and attach it to the required output field `initial_call_brief_artifact_id`. Use `definitionJson.documentRefs` as the durable document reference contract. Apply each reference by usage: `output_template` sets the output skeleton, `methodology` supplies scoring or analysis logic, `checklist` must be completed with status, evidence, and owner, `style_guide` governs citations and claim language, and `operating_guidance` or `policy` constrains process and approval boundaries. For refs with `outputFieldKey`, produce that output from the referenced pack document and preserve the document ID alongside the output artifact.

## Missing Input Policy

Ask for the meeting type, meeting goal, and missing source material before producing the meeting brief when they are not clear from project context.

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
| `founder_names` | Founder Names | `string` | no |
| `meeting_datetime` | Meeting Datetime | `string` | no |
| `deal_room_url` | Deal Pipeline Url | `string` | no |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `initial_call_brief_artifact_id` | Meeting Brief | `file` | yes |
| `pre_call_brief` | Meeting Brief | `richtext` | no |
| `founder_company_summary` | Founder Company Summary | `richtext` | no |
| `competitor_funding_activity` | Competitor Funding Activity | `string` | no |
| `starter_investment_screen_scorecard` | Stage-Relevant Scorecard Notes | `string` | no |
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
- `vc.document.template_use_guidance` (operating_guidance)

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/prepare-initial-call.yaml`
- Alludium task ID: `vc.prepare_initial_call`
- Task family: `meeting`
- Lifecycle stage: `evaluation`
- Recommended agent: `vc-meeting-operator` (Alludium template `vc_meeting_operator`)
- Supported project types:
  - `vc_deal_room`

## Required Skills

- `meeting-prep-and-summary`
- `company-research-and-enrichment`
- `citation-enforcement`
- `pitch-deck-explainer`

## Workspace-Configured Methodology Skills

- `investment-screening-framework`: Use only when the workspace explicitly configures this screening framework.
