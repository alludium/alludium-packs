---
id: vc.configure_origination_pipeline
title: Configure Origination Pipeline
slug: configure-origination-pipeline
agent: vc-sourcing-operator
skills:
- vc-origination-pipeline-orchestration
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/configure-origination-pipeline.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Configure Origination Pipeline

Capture thesis, source selection, cadence intent, budget policy, review thresholds, and integration-readiness requirements for a VC origination pipeline.

## Instructions

Guide the user through initial origination pipeline configuration. Capture the required `pipeline_name`, thesis, source choices, cadence intent, digest destination, budget, review policy, promotion threshold, manual-review threshold, credential gaps, and child setup tasks needed for selected sources. Create setup child tasks only for selected integrations whose setup templates exist. Complete with structured output `projectCreation.fieldValues.pipeline_name`, include `projectCreation.fieldValues.source_registry` and `projectCreation.fieldValues.review_policy` when captured, and include `projectCreation.fieldValues.confidentiality_level` only when confidently captured. Do not run sourcing, score candidates, create candidate records, enable schedules, write to external systems, send outreach, create Deal Pipelines, or create the Origination Pipeline project; the platform finalizer owns deterministic project creation after task completion. Use `definitionJson.documentRefs` as the durable document reference contract. Apply each reference by usage: `output_template` sets the output skeleton, `methodology` supplies scoring or analysis logic, `checklist` must be completed with status, evidence, and owner, `style_guide` governs citations and claim language, and `operating_guidance` or `policy` constrains process and approval boundaries. For refs with `outputFieldKey`, produce that output from the referenced pack document and preserve the document ID alongside the output artifact.

## Missing Input Policy

Keep setup incomplete when thesis, enabled sources, review policy, budget policy, or required credential decisions are missing. Ask targeted task questions rather than inventing configuration.

## External Action Policy

Configuration only. No external reads beyond connection-readiness checks, no scheduled runs, no imports, no external writes, no outreach, and no Deal Pipeline creation.

## Completion Criteria

- `pipeline_name` is captured for guided project creation finalization.
- Thesis, source selection, run cadence intent, budget policy, review policy, and thresholds are captured or explicitly marked unresolved.
- Required setup child tasks for selected Apify and Companies House sources are proposed without executing source reads.
- Credential gaps and approved connection scopes are listed.
- The output distinguishes configuration intent from active automation.
- Guided project creation output includes `projectCreation.fieldValues.pipeline_name` and captured runtime project fields such as `source_registry` and `review_policy`.

## Human Decision Points

- Choose enabled source systems and approved source scope.
- Confirm budget and cadence intent before any later scheduled-run work.
- Approve child setup tasks separately for each integration.

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `pipeline_name` | Pipeline Name | `string` | yes |
| `configuration_goal` | Configuration Goal | `string` | no |
| `current_pipeline_context` | Current Pipeline Context | `json` | no |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `configuration_summary` | Configuration Summary | `richtext` | no |
| `source_registry` | Source Registry | `richtext` | no |
| `review_policy` | Review Policy | `richtext` | no |
| `child_task_plan` | Child Task Plan | `richtext` | yes |
| `projectCreation` | Project Creation Field Values | `json` | yes |

## Document References

- `vc.document.origination_pipeline_sop` (operating_guidance)
- `vc.document.origination_source_strategy_guide` (methodology)
- `vc.document.source_registry_template` (operating_guidance)
- `vc.document.template_use_guidance` (operating_guidance)

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/configure-origination-pipeline.yaml`
- Alludium task ID: `vc.configure_origination_pipeline`
- Task family: `origination_pipeline_setup`
- Lifecycle stage: `setup`
- Recommended agent: `vc-sourcing-operator` (Alludium template `vc_sourcing_operator`)
- Supported project types:
  - `vc_origination_pipeline`
- Supported project scopes:
  - `project_instance`

## Required Skills

- `vc-origination-pipeline-orchestration`
- `citation-enforcement`
