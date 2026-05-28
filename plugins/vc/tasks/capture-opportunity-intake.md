---
id: vc.screen_inbound_opportunity
title: Capture Opportunity Intake
slug: capture-opportunity-intake
agent: vc-dealflow-concierge
skills:
- deal-pipeline-setup-and-source-ingestion
- company-research-and-enrichment
- citation-enforcement
- pitch-deck-explainer
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/capture-opportunity-intake.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Capture Opportunity Intake

Hydrate and assess a created Deal Pipeline from available source context before formal screening.

## Instructions

Hydrate the created Deal Pipeline from the best available source context: CRM/source record, company domain, pitch deck, intro note, source thread, founder material, origination promotion package, or other supplied evidence. Capture known project fields, source index, missing information, evidence quality, and recommended readiness for formal screening. Do not require a pitch deck when another source explains the opportunity. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Create or update a durable project file artifact named Opportunity Intake Summary and attach it to the required output field `opportunity_intake_artifact_id`. Use `definitionJson.documentRefs` as the durable document reference contract. Apply each reference by usage: `output_template` sets the output skeleton, `methodology` supplies scoring or analysis logic, `checklist` must be completed with status, evidence, and owner, `style_guide` governs citations and claim language, and `operating_guidance` or `policy` constrains process and approval boundaries. For refs with `outputFieldKey`, produce that output from the referenced pack document and preserve the document ID alongside the output artifact.

## Missing Input Policy

Ask for the minimum missing context needed to identify the company and cite at least one source. If company identity and one credible source are present, complete intake and list missing enrichment or screening inputs instead of blocking.

## External Action Policy

Draft only unless a human explicitly approves the send, CRM write, Drive change, child task creation, or stage transition.

## Completion Criteria

- Required input gaps are resolved or listed as assumptions/open questions.
- Material conclusions include source links or are labeled as human judgment calls.
- Next actions identify owner, dependency, and required human approval point.
- Intake recommendation clearly states whether the project is ready for screening, needs more context, should be watched, or should be passed.

## Human Decision Points

- Approve investment-stage movement, pass/follow-up recommendations, and final task completion.
- Approve external communications, CRM writes, Drive/project creation, legal/counsel actions, and founder-facing requests.

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `company_name` | Company Name | `string` | yes |
| `pitch_deck_artifact_id` | Pitch Deck Artifact | `file` | no |
| `company_domain` | Company Domain | `string` | no |
| `source_system` | Source System | `string` | no |
| `source_object_url` | Source Object URL | `string` | no |
| `source_thread_url` | Source Thread URL | `string` | no |
| `source_thread_artifact_id` | Source Thread Artifact | `file` | no |
| `source_material_artifact_ids` | Source Material Artifacts | `string` | no |
| `founder_materials_artifact_ids` | Founder Materials Artifacts | `string` | no |
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

## Document References

- `vc.document.deal_room_sop` (operating_guidance)
- `vc.document.evidence_citation_style_guide` (style_guide)
- `vc.document.template_use_guidance` (operating_guidance)

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/capture-opportunity-intake.yaml`
- Alludium task ID: `vc.screen_inbound_opportunity`
- Task family: `intake`
- Lifecycle stage: `intake`
- Recommended agent: `vc-dealflow-concierge` (Alludium template `vc_dealflow_concierge`)
- Supported project types:
  - `vc_deal_room`

## Required Skills

- `deal-pipeline-setup-and-source-ingestion`
- `company-research-and-enrichment`
- `citation-enforcement`
- `pitch-deck-explainer`
