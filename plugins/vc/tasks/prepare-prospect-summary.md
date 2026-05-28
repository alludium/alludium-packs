---
id: vc.prepare_sourcing_ic_summary
title: Prepare Prospect Summary
slug: prepare-prospect-summary
agent: vc-sourcing-operator
skills:
- origination-prospect-summary-preparation
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/prepare-prospect-summary.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Prepare Prospect Summary

Prepare a concise prospect-level sourcing summary for one prioritized origination candidate before outreach or promotion.

## Instructions

Prepare a concise prospect summary for one prioritized candidate using enriched candidate evidence, verdict, relationship context, portfolio-overlap result, source receipts, risks, and open questions. This is a sourcing and outreach-prep artifact, not an IC memo or IC-ready recommendation. Use `definitionJson.documentRefs` as the durable document reference contract. Apply each reference by usage: `output_template` sets the output skeleton, `methodology` supplies scoring or analysis logic, `checklist` must be completed with status, evidence, and owner, `style_guide` governs citations and claim language, and `operating_guidance` or `policy` constrains process and approval boundaries. For refs with `outputFieldKey`, produce that output from the referenced pack document and preserve the document ID alongside the output artifact.

## Missing Input Policy

Ask for candidate evidence, verdict, relationship context, overlap review, source receipts, outreach audience, and the intended next action.

## External Action Policy

Draft only. Do not create Notion pages, documents, external records, or Deal Pipelines without explicit approval.

## Completion Criteria

- Summary covers exactly one prospect/candidate.
- Summary includes identity, product, thesis fit, founder signal, market/customer signal, relationship context, risks, unknowns, evidence quality, and recommended next step.

## Human Decision Points

- None declared

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `prospect_summary_candidate` | Prospect Summary Candidate | `json` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `prospect_summary_artifact_id` | Prospect Summary Artifact | `file` | yes |
| `prospect_summary_status` | Prospect Summary Status | `string` | no |
| `prospect_summary` | Prospect Summary | `richtext` | no |

## Document References

- `vc.document.sourcing_ic_summary_template` (output_template) -> `prospect_summary_artifact_id`
- `vc.document.origination_source_strategy_guide` (methodology)
- `vc.document.evidence_citation_style_guide` (style_guide)
- `vc.document.template_use_guidance` (operating_guidance)

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/prepare-prospect-summary.yaml`
- Alludium task ID: `vc.prepare_sourcing_ic_summary`
- Task family: `origination_prospect_summary`
- Lifecycle stage: `review`
- Recommended agent: `vc-sourcing-operator` (Alludium template `vc_sourcing_operator`)
- Supported project types:
  - `vc_origination_pipeline`
- Supported project scopes:
  - `project_instance`

## Required Skills

- `origination-prospect-summary-preparation`
- `citation-enforcement`
