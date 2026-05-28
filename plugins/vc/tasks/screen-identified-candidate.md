---
id: vc.screen_identified_candidates
title: Screen Identified Candidate
slug: screen-identified-candidate
agent: vc-sourcing-operator
skills:
- vc-sourcing-verdict-and-screening
- vc-sourcing-dedupe-and-novelty-check
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/screen-identified-candidate.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Screen Identified Candidate

Run a lightweight first-pass fit screen on newly identified origination candidates before marking them of interest.

## Instructions

Screen newly identified candidates with the lightest useful evidence set: source receipt, normalized identity, stage/geography fit, obvious hard exclusions, basic AI/native software signal, founder signal, and duplicate/known-relationship status. This is not the full active-candidate screen; recommend only prioritize for outreach, watchlist, or pass, and list what must be enriched before outreach. Use `definitionJson.documentRefs` as the durable document reference contract. Apply each reference by usage: `output_template` sets the output skeleton, `methodology` supplies scoring or analysis logic, `checklist` must be completed with status, evidence, and owner, `style_guide` governs citations and claim language, and `operating_guidance` or `policy` constrains process and approval boundaries. For refs with `outputFieldKey`, produce that output from the referenced pack document and preserve the document ID alongside the output artifact.

## Missing Input Policy

Ask for the identified candidate batch, source receipts, thesis policy, hard exclusions, and dedupe state before screening.

## External Action Policy

Screening recommendation only. Do not contact founders, write CRM/list records, send outreach, or create Deal Pipeline projects.

## Completion Criteria

- Every pass or watchlist recommendation names the evidence gap or exclusion rule.
- Outreach-ready recommendations include the next enrichment or outreach-prep evidence needed.

## Human Decision Points

- None declared

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `identified_candidate_batch` | Identified Candidate Batch | `json` | yes |
| `first_pass_screen_policy` | First-Pass Screen Policy | `json` | no |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `identified_screen_artifact_id` | Identified Screen Artifact | `file` | yes |
| `outreach_ready_count` | Outreach Ready Count | `number` | no |
| `watchlist_count` | Watchlist Count | `number` | no |
| `pass_count` | Pass Count | `number` | no |
| `identified_screen_report` | Identified Screen Report | `richtext` | no |

## Document References

- `vc.document.sourcing_scoring_rubric` (methodology) -> `identified_screen_artifact_id`
- `vc.document.origination_source_strategy_guide` (methodology)
- `vc.document.dedupe_novelty_policy` (policy)
- `vc.document.template_use_guidance` (operating_guidance)

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/screen-identified-candidate.yaml`
- Alludium task ID: `vc.screen_identified_candidates`
- Task family: `origination_screening`
- Lifecycle stage: `review`
- Recommended agent: `vc-sourcing-operator` (Alludium template `vc_sourcing_operator`)
- Supported project types:
  - `vc_origination_pipeline`
- Supported project scopes:
  - `project_instance`

## Required Skills

- `vc-sourcing-verdict-and-screening`
- `vc-sourcing-dedupe-and-novelty-check`
- `citation-enforcement`
