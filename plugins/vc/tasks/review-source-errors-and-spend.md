---
id: vc.review_source_errors_and_spend
title: Review Source Errors and Spend
slug: review-source-errors-and-spend
agent: vc-pipeline-autopilot
skills:
- vc-source-error-and-spend-audit
- vc-source-registry-and-state-management
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/review-source-errors-and-spend.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Review Source Errors and Spend

Review degraded source runs, cost warnings, retry safety, and required human actions.

## Instructions

Review run receipts and degraded-source notes from the latest origination pass. Classify missing credentials, auth expiry, provider failure, rate limits, budget caps, exhausted queries, schema drift, no-yield sources, and blocked writes. Recommend retry, setup, query pruning, schedule pause, or human review. Use `definitionJson.documentRefs` as the durable document reference contract. Apply each reference by usage: `output_template` sets the output skeleton, `methodology` supplies scoring or analysis logic, `checklist` must be completed with status, evidence, and owner, `style_guide` governs citations and claim language, and `operating_guidance` or `policy` constrains process and approval boundaries. For refs with `outputFieldKey`, produce that output from the referenced pack document and preserve the document ID alongside the output artifact.

## Missing Input Policy

Ask for recent run receipts, source state, budget policy, provider status notes, and retry policy.

## External Action Policy

Review only. Do not retry paid runs, change budgets, disable schedules, or update credentials.

## Completion Criteria

- Each issue includes source, severity, impact, retry safety, owner, and next action.
- Source health status is one of healthy, degraded, needs_credentials, budget_blocked, or unknown.
- Paid retry and schedule-change approvals are explicit.

## Human Decision Points

- None declared

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `source_health_scope` | Source Health Scope | `json` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `source_health_artifact_id` | Source Health Artifact | `file` | yes |
| `source_health_status` | Source Health Status | `string` | no |
| `source_error_count` | Source Error Count | `number` | no |
| `source_health_report` | Source Health Report | `richtext` | no |

## Document References

- `vc.document.source_health_review_checklist` (output_template) -> `source_health_artifact_id`
- `vc.document.paid_source_spend_audit_checklist` (checklist)
- `vc.document.template_use_guidance` (operating_guidance)

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/review-source-errors-and-spend.yaml`
- Alludium task ID: `vc.review_source_errors_and_spend`
- Task family: `origination_source_health`
- Lifecycle stage: `operate`
- Recommended agent: `vc-pipeline-autopilot` (Alludium template `vc_pipeline_autopilot`)
- Supported project types:
  - `vc_origination_pipeline`
- Supported project scopes:
  - `project_instance`

## Required Skills

- `vc-source-error-and-spend-audit`
- `vc-source-registry-and-state-management`
- `citation-enforcement`

## Planned Skills

- `vc-source-error-and-spend-audit`
- `vc-source-registry-and-state-management`
- `citation-enforcement`
