---
id: vc.screen_founder_connected_candidates
title: Screen Founder-Connected Candidate
slug: screen-founder-connected-candidates
agent: vc-sourcing-operator
skills:
- vc-sourcing-verdict-and-screening
- vc-outreach-draft-queue
- citation-enforcement
- investment-screening-framework
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/screen-founder-connected-candidates.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Screen Founder-Connected Candidate

Re-screen candidates after a founder connection adds direct context, before continuing outbound or promotion.

## Instructions

Re-screen candidates only after a founder connection, reply, or direct relationship signal adds new context beyond the first-pass screen. Compare founder-provided context, current enrichment, relationship warmth, thesis fit, portfolio overlap, deal-fit score where available, and remaining evidence gaps. Recommend continue outbound, watchlist, pass, or engaged-ready-for-Deal-Pipeline handoff. Do not treat connection acceptance alone as investment fit. Use `definitionJson.documentRefs` as the durable document reference contract. Apply each reference by usage: `output_template` sets the output skeleton, `methodology` supplies scoring or analysis logic, `checklist` must be completed with status, evidence, and owner, `style_guide` governs citations and claim language, and `operating_guidance` or `policy` constrains process and approval boundaries. For refs with `outputFieldKey`, produce that output from the referenced pack document and preserve the document ID alongside the output artifact.

## Missing Input Policy

Ask for the connection record, founder reply/context, latest enrichment and screen artifacts, portfolio overlap, deal-fit context if available, and allowed next states before screening.

## External Action Policy

Recommendation and draft-prep only. Do not send messages, update CRM/list stages, or create Deal Pipeline projects without explicit human approval.

## Completion Criteria

- Recommendation distinguishes new founder-context evidence from earlier sourced evidence.
- Continue, pass, watchlist, or engaged handoff recommendation is explicit and cited.
- If outreach should continue, the next message angle and unresolved validation questions are listed.

## Human Decision Points

- None declared

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `founder_connection_context` | Founder Connection Context | `json` | yes |
| `prior_screen_artifacts` | Prior Screen Artifacts | `file[]` | no |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `founder_connected_screen_artifact_id` | Founder Connected Screen Artifact | `file` | yes |
| `founder_connected_screen_recommendation` | Founder Connected Screen Recommendation | `string` | no |
| `founder_connected_screen_report` | Founder Connected Screen Report | `richtext` | no |

## Document References

- `vc.document.sourcing_scoring_rubric` (methodology) -> `founder_connected_screen_artifact_id`
- `vc.document.outreach_queue_template` (output_template)
- `vc.document.origination_source_strategy_guide` (methodology)
- `vc.document.template_use_guidance` (operating_guidance)

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/screen-founder-connected-candidates.yaml`
- Alludium task ID: `vc.screen_founder_connected_candidates`
- Task family: `origination_founder_connected_screening`
- Lifecycle stage: `engage`
- Recommended agent: `vc-sourcing-operator` (Alludium template `vc_sourcing_operator`)
- Supported project types:
  - `vc_origination_pipeline`
- Supported project scopes:
  - `project_instance`

## Required Skills

- `vc-sourcing-verdict-and-screening`
- `vc-outreach-draft-queue`
- `citation-enforcement`
- `investment-screening-framework`
