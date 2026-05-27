---
id: vc.prepare_sourcing_ic_summary
title: Prepare Sourcing IC Summary
slug: prepare-sourcing-ic-summary
agent: vc-ic-prep-producer
skills:
- vc-origination-ic-summary-preparation
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/prepare-sourcing-ic-summary.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Prepare Sourcing IC Summary

Prepare a lightweight IC-style summary for a reviewed origination candidate before Deal Pipeline promotion.

## Instructions

Prepare a concise IC-style summary for Meet or Watch candidates using enriched candidate evidence, verdict, relationship context, portfolio-overlap result, source receipts, risks, and open questions. This replaces direct page-creation behavior from the reference implementation with a reviewable summary artifact. Use `definitionJson.documentRefs` as the durable document reference contract. Apply each reference by usage: `output_template` sets the output skeleton, `methodology` supplies scoring or analysis logic, `checklist` must be completed with status, evidence, and owner, `style_guide` governs citations and claim language, and `operating_guidance` or `policy` constrains process and approval boundaries. For refs with `outputFieldKey`, produce that output from the referenced pack document and preserve the document ID alongside the output artifact.

## Missing Input Policy

Ask for candidate evidence, verdict, relationship context, overlap review, source receipts, and target audience.

## External Action Policy

Draft only. Do not create Notion pages, documents, external records, or Deal Pipelines without explicit approval.

## Completion Criteria

- Summary includes identity, product, thesis fit, founder signal, market/customer signal, relationship context, risks, unknowns, evidence quality, and recommended next step.

## Human Decision Points

- None declared

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `ic_summary_candidate` | IC Summary Candidate | `json` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `ic_summary_artifact_id` | IC Summary Artifact | `file` | yes |
| `ic_summary_status` | IC Summary Status | `string` | no |
| `ic_summary` | IC Summary | `richtext` | no |

## Document References

- `vc.document.sourcing_ic_summary_template` (output_template) -> `ic_summary_artifact_id`
- `vc.document.origination_source_strategy_guide` (methodology)
- `vc.document.evidence_citation_style_guide` (style_guide)
- `vc.document.template_use_guidance` (operating_guidance)

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/prepare-sourcing-ic-summary.yaml`
- Alludium task ID: `vc.prepare_sourcing_ic_summary`
- Task family: `origination_ic_summary`
- Lifecycle stage: `review`
- Recommended agent: `vc-ic-prep-producer` (Alludium template `vc_ic_prep_producer`)
- Supported project types:
  - `vc_origination_pipeline`
- Supported project scopes:
  - `project_instance`

## Required Skills

- `vc-origination-ic-summary-preparation`
- `citation-enforcement`
