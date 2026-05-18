---
id: vc.configure_origination_pipeline
title: Configure VC Origination Pipeline
slug: configure-origination-pipeline
agent: vc-pipeline-autopilot
skills:
- vc-origination-pipeline-orchestration
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/configure-origination-pipeline.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Configure VC Origination Pipeline

Capture thesis, source selection, cadence intent, budget policy, review thresholds, and integration-readiness requirements for a VC origination pipeline.

## Instructions

Guide the user through initial origination pipeline configuration. Capture thesis, source choices, cadence intent, digest destination, budget, review policy, promotion threshold, manual-review threshold, credential gaps, and child setup tasks needed for selected sources. Create setup child tasks only for selected integrations whose setup templates exist. Do not run sourcing, score candidates, create candidate records, enable schedules, write to external systems, send outreach, or promote candidates to Deal Rooms.

## Missing Input Policy

Keep setup incomplete when thesis, enabled sources, review policy, budget policy, or required credential decisions are missing. Ask targeted task questions rather than inventing configuration.

## External Action Policy

Configuration only. No external reads beyond connection-readiness checks, no scheduled runs, no imports, no external writes, no outreach, and no Deal Room creation.

## Completion Criteria

- Thesis, source selection, run cadence intent, budget policy, review policy, and thresholds are captured or explicitly marked unresolved.
- Required setup child tasks for selected Apify and Companies House sources are proposed without executing source reads.
- Credential gaps and approved connection scopes are listed.
- The output distinguishes configuration intent from active automation.

## Human Decision Points

- Choose enabled source systems and approved source scope.
- Confirm budget and cadence intent before any later scheduled-run work.
- Approve child setup tasks separately for each integration.

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `configuration_goal` | Configuration Goal | `string` | yes |
| `current_pipeline_context` | Current Pipeline Context | `json` | no |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `configuration_summary` | Configuration Summary | `richtext` | no |
| `source_registry` | Source Registry | `richtext` | no |
| `review_policy` | Review Policy | `richtext` | no |
| `child_task_plan_artifact_id` | Child Task Plan Artifact | `file` | yes |

## Document References

- `vc.document.origination_pipeline_sop` (operating_guidance)
- `vc.document.source_registry_template` (output_template) -> `child_task_plan_artifact_id`

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/configure-origination-pipeline.yaml`
- Alludium task ID: `vc.configure_origination_pipeline`
- Task family: `origination_pipeline_setup`
- Lifecycle stage: `setup`
- Recommended agent: `vc-pipeline-autopilot` (Alludium template `vc_pipeline_autopilot`)
- Supported project types:
  - `vc_origination_pipeline`
- Supported project scopes:
  - `project_instance`

## Required Skills

- `vc-origination-pipeline-orchestration`
- `citation-enforcement`

## Planned Skills

- `vc-origination-pipeline-orchestration`
- `citation-enforcement`
