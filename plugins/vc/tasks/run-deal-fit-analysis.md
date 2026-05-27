---
id: vc.run_deal_fit_analysis
title: Run Deal Fit Analysis
slug: run-deal-fit-analysis
agent: vc-sourcing-operator
skills:
- vc-sourcing-verdict-and-screening
- investment-screening-framework
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/run-deal-fit-analysis.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Run Deal Fit Analysis

Score active origination candidates against the firm's deal-fit pillars before deeper screening.

## Instructions

Mirror the reference pipeline deal-fit step by scoring active candidates against the configured fit pillars before the heavier screen. Use enriched evidence, relationship context, portfolio-overlap results, and the current thesis policy. Return a fit score or band, reasoning, evidence gaps, and recommended next state. Use `definitionJson.documentRefs` as the durable document reference contract. Apply each reference by usage: `output_template` sets the output skeleton, `methodology` supplies scoring or analysis logic, `checklist` must be completed with status, evidence, and owner, `style_guide` governs citations and claim language, and `operating_guidance` or `policy` constrains process and approval boundaries. For refs with `outputFieldKey`, produce that output from the referenced pack document and preserve the document ID alongside the output artifact.

## Missing Input Policy

Ask for enriched candidates, thesis policy, scoring pillars, portfolio overlap, relationship context, and approved write mode before analysis.

## External Action Policy

Analysis only unless explicit write approval is granted. Do not send outreach, update protected manual decisions, or create Deal Pipeline projects.

## Completion Criteria

- Each candidate has a deal-fit score or band, cited reasoning, evidence gaps, and recommended next state.
- Portfolio overlap and relationship context are reflected when available.

## Human Decision Points

- None declared

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `deal_fit_scope` | Deal Fit Scope | `json` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `deal_fit_artifact_id` | Deal Fit Artifact | `file` | yes |
| `deal_fit_ready_count` | Deal Fit Ready Count | `number` | no |
| `deal_fit_report` | Deal Fit Report | `richtext` | no |

## Document References

- `vc.document.sourcing_scoring_rubric` (methodology) -> `deal_fit_artifact_id`
- `vc.document.investment_screening_framework` (methodology)
- `vc.document.template_use_guidance` (operating_guidance)

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/run-deal-fit-analysis.yaml`
- Alludium task ID: `vc.run_deal_fit_analysis`
- Task family: `origination_deal_fit`
- Lifecycle stage: `review`
- Recommended agent: `vc-sourcing-operator` (Alludium template `vc_sourcing_operator`)
- Supported project types:
  - `vc_origination_pipeline`
- Supported project scopes:
  - `project_instance`

## Required Skills

- `vc-sourcing-verdict-and-screening`
- `investment-screening-framework`
- `citation-enforcement`
