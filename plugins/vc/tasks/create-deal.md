---
id: vc.create_deal_pipeline_project
title: Create Deal
slug: create-deal
agent: vc-dealflow-concierge
skills:
- deal-pipeline-setup-and-source-ingestion
- company-research-and-enrichment
- citation-enforcement
- pitch-deck-explainer
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/create-deal.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Create Deal

Gather enough structured context from chat, inbox material, CRM references, source notes, domains, decks, or origination handoffs to create one Deal Pipeline project.

## Instructions

Guide the user through creating a Deal Pipeline project from whatever context is available: an inbox request, intro note, CRM/source record link, company domain, pitch deck, founder material, source thread, or origination promotion package. Ask only for the missing details needed to confidently identify the company and preserve source context. Complete with structured output `projectCreation.fieldValues.company_name`; include domain, source, founder, pitch-deck, source-reference, confidentiality, and other declared Deal Pipeline creation fields only when confidently collected. Do not create the project, run intake, screen the opportunity, create child tasks, move stages, mutate CRM records, send messages, or write external files; the platform finalizer owns deterministic project creation after task completion. Use `definitionJson.documentRefs` as the durable document reference contract. Apply each reference by usage: `style_guide` governs citations and claim language, and `operating_guidance` constrains process and approval boundaries.

## Missing Input Policy

Ask for company_name or enough evidence to infer it, plus at least one source note, source artifact, source record, pitch deck, company domain, source thread, or origination handoff before completing project creation.

## External Action Policy

Guided creation only. No CRM writes, external sends, Drive changes, project creation, child task creation, stage transitions, or screening work.

## Completion Criteria

- `projectCreation.fieldValues.company_name` is captured for guided project creation finalization.
- Available source context is preserved as declared Deal Pipeline creation fields or summarized as creation notes.
- Missing enrichment or screening inputs are listed for the post-create intake task rather than blocking creation unnecessarily.
- The output distinguishes project-creation facts from later intake, enrichment, and screening judgments.

## Human Decision Points

- Confirm the target company identity when source material is ambiguous.
- Confirm whether incomplete context is sufficient to create the project and let intake continue after creation.

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `company_name` | Company Name | `string` | no |
| `freeform_deal_context` | Deal Context | `richtext` | no |
| `company_domain` | Company Domain | `string` | no |
| `source_object_url` | Source Record URL | `string` | no |
| `source_thread_url` | Source Thread URL | `string` | no |
| `pitch_deck_artifact_id` | Pitch Deck Artifact | `file` | no |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `projectCreation` | Project Creation Field Values | `json` | yes |
| `creation_summary` | Creation Summary | `richtext` | no |
| `missing_creation_context` | Missing Creation Context | `string` | no |

## Document References

- `vc.document.deal_room_sop` (operating_guidance)
- `vc.document.evidence_citation_style_guide` (style_guide)
- `vc.document.template_use_guidance` (operating_guidance)

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/create-deal.yaml`
- Alludium task ID: `vc.create_deal_pipeline_project`
- Task family: `deal_pipeline_project_creation`
- Lifecycle stage: `setup`
- Recommended agent: `vc-dealflow-concierge` (Alludium template `vc_dealflow_concierge`)
- Supported project types:
  - `vc_deal_room`
- Supported project scopes:
  - `project_instance`

## Required Skills

- `deal-pipeline-setup-and-source-ingestion`
- `company-research-and-enrichment`
- `citation-enforcement`
- `pitch-deck-explainer`
