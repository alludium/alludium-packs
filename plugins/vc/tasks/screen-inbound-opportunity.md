---
id: vc.screen_inbound_opportunity
title: Capture Opportunity Intake
slug: screen-inbound-opportunity
agent: vc-dealflow-concierge
skills:
- deal-room-setup-and-source-ingestion
- company-research-and-enrichment
- citation-enforcement
- pitch-deck-explainer
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/screen-inbound-opportunity.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Capture Opportunity Intake

Capture source context, known fields, missing information, and guided project-creation values for one venture-capital opportunity before formal screening.

## Instructions

Capture the inbound or promoted opportunity's source context, known project fields, missing setup information, source index, and recommended next task before formal screening. Use a pitch deck, intro note, source thread, CRM/source record, or other supplied material when available, but do not require a pitch deck when another source explains the opportunity. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Create or update a durable project file artifact named Opportunity Intake Summary and attach it to the required output field `opportunity_intake_artifact_id`. When this task is used as a guided project creation task, complete with structured output `projectCreation.fieldValues.company_name`, include `projectCreation.fieldValues.pitch_deck_artifact_id` when a pitch deck is available, and include only other declared VC Deal Room creation fields that were confidently collected. Do not create the project; the platform finalizer owns deterministic project creation after task completion. Use `definitionJson.documentRefs` as the durable document reference contract. Apply each reference by usage: `output_template` sets the output skeleton, `methodology` supplies scoring or analysis logic, `checklist` must be completed with status, evidence, and owner, `style_guide` governs citations and claim language, and `operating_guidance` or `policy` constrains process and approval boundaries. For refs with `outputFieldKey`, produce that output from the referenced pack document and preserve the document ID alongside the output artifact.

## Missing Input Policy

Ask for company_name plus at least one source note, source artifact, source record, pitch deck, or source thread before completing intake.

## External Action Policy

Draft only unless a human explicitly approves the send, CRM write, Drive change, project creation, child task creation, or stage transition.

## Completion Criteria

- Required input gaps are resolved or listed as assumptions/open questions.
- Material conclusions include source links or are labeled as human judgment calls.
- Next actions identify owner, dependency, and required human approval point.
- Guided project creation output includes `projectCreation.fieldValues.company_name` and any confidently collected declared creation fields.

## Human Decision Points

- Approve investment-stage movement, pass/follow-up recommendations, and final task completion.
- Approve external communications, CRM writes, Drive/project creation, legal/counsel actions, and founder-facing requests.

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `company_name` | Company Name | `string` | yes |
| `pitch_deck_artifact_id` | Pitch Deck Artifact | `file` | no |
| `referrer` | Referrer | `string` | no |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `opportunity_intake_artifact_id` | Opportunity Intake Summary | `file` | yes |
| `fit_recommendation` | Intake Recommendation | `string` | no |
| `initial_investment_screen_summary` | Intake Summary | `richtext` | no |
| `missing_information` | Missing Information | `string` | no |
| `red_flags` | Early Red Flags | `string` | no |
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
| `projectCreation` | Project Creation Field Values | `json` | yes |

## Document References

- `vc.document.deal_room_sop` (operating_guidance)
- `vc.document.evidence_citation_style_guide` (style_guide)
- `vc.document.template_use_guidance` (operating_guidance)

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/screen-inbound-opportunity.yaml`
- Alludium task ID: `vc.screen_inbound_opportunity`
- Task family: `intake`
- Lifecycle stage: `intake`
- Recommended agent: `vc-dealflow-concierge` (Alludium template `vc_dealflow_concierge`)
- Supported project types:
  - `vc_deal_room`

## Required Skills

- `deal-room-setup-and-source-ingestion`
- `company-research-and-enrichment`
- `citation-enforcement`
- `pitch-deck-explainer`
