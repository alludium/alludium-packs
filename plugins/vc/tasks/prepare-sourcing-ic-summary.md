---
id: vc.prepare_sourcing_ic_summary
title: Prepare Sourcing IC Summary
slug: prepare-sourcing-ic-summary
agent: vc-ic-prep-producer
skills:
- vc-origination-ic-summary-preparation
- citation-enforcement
---

<!-- Generated from alludium/task-definition-templates/vc-workflows/prepare-sourcing-ic-summary.yaml; do not edit directly. Run python plugins/vc/scripts/generate_markdown.py after changing the YAML source. -->

# Prepare Sourcing IC Summary

Prepare a lightweight IC-style summary for a reviewed origination candidate before Deal Room promotion.

## Instructions

Prepare a concise IC-style summary for Meet or Watch candidates using enriched candidate evidence, verdict, relationship context, portfolio-overlap result, source receipts, risks, and open questions. This replaces direct page-creation behavior from the reference implementation with a reviewable summary artifact.

## Missing Input Policy

Ask for candidate evidence, verdict, relationship context, overlap review, source receipts, and target audience.

## External Action Policy

Draft only. Do not create Notion pages, documents, external records, or Deal Rooms without explicit approval.

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

## Planned Skills

- `vc-origination-ic-summary-preparation`
- `citation-enforcement`
