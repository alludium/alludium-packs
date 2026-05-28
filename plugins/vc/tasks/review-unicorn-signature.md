---
id: vc.review_unicorn_signature
title: Review Unicorn Signature
slug: review-unicorn-signature
agent: vc-sourcing-operator
skills:
- vc-sourcing-verdict-and-screening
- origination-prospect-summary-preparation
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/review-unicorn-signature.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Review Unicorn Signature

Stress-test strong origination candidates for venture-scale shape before prospect-summary preparation.

## Instructions

Stress-test candidates that survived deal-fit and active screening for genuine venture-scale shape before creating a prospect summary. Classify the candidate as genuine, strong, on-pattern, or off-shape, and recommend whether to proceed to prospect summary, watchlist, or pass. Use market/category context only to support the classification; do not fabricate market size or traction. Use `definitionJson.documentRefs` as the durable document reference contract. Apply each reference by usage: `output_template` sets the output skeleton, `methodology` supplies scoring or analysis logic, `checklist` must be completed with status, evidence, and owner, `style_guide` governs citations and claim language, and `operating_guidance` or `policy` constrains process and approval boundaries. For refs with `outputFieldKey`, produce that output from the referenced pack document and preserve the document ID alongside the output artifact.

## Missing Input Policy

Ask for deal-fit and active-screen artifacts, category context, candidate evidence, and allowed next states before reviewing.

## External Action Policy

Review only. Do not demote protected manual decisions, write external systems, send outreach, or create Deal Pipeline projects without explicit approval.

## Completion Criteria

- Classification is one of genuine, strong, on-pattern, or off-shape.
- Recommendation states whether to proceed to prospect summary, watchlist, or pass.
- Evidence gaps and validation questions are listed.

## Human Decision Points

- None declared

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `unicorn_signature_scope` | Unicorn Signature Scope | `json` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `unicorn_signature_artifact_id` | Unicorn Signature Artifact | `file` | yes |
| `unicorn_signature_recommendation` | Unicorn Signature Recommendation | `string` | no |
| `unicorn_signature_report` | Unicorn Signature Report | `richtext` | no |

## Document References

- `vc.document.sourcing_scoring_rubric` (methodology) -> `unicorn_signature_artifact_id`
- `vc.document.sourcing_ic_summary_template` (operating_guidance)
- `vc.document.template_use_guidance` (operating_guidance)

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/review-unicorn-signature.yaml`
- Alludium task ID: `vc.review_unicorn_signature`
- Task family: `origination_unicorn_signature`
- Lifecycle stage: `review`
- Recommended agent: `vc-sourcing-operator` (Alludium template `vc_sourcing_operator`)
- Supported project types:
  - `vc_origination_pipeline`
- Supported project scopes:
  - `project_instance`

## Required Skills

- `vc-sourcing-verdict-and-screening`
- `origination-prospect-summary-preparation`
- `citation-enforcement`
