---
id: vc.audit_linkedin_query_spend
title: Audit LinkedIn Query Spend
slug: audit-linkedin-query-spend
agent: vc-pipeline-autopilot
skills:
- vc-linkedin-query-spend-audit
- vc-source-registry-and-state-management
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/audit-linkedin-query-spend.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Audit LinkedIn Query Spend

Produce a read-only Apify LinkedIn query yield and cost audit with manual KEEP/REVIEW/PRUNE recommendations.

## Instructions

Mirror the reference pipeline's read-only LinkedIn query audit. Compare query/track run depth, pages or result batches paid, candidate yield, duplicate or seen rate, exhaustion state, estimated cost, and cost per surfaced company. Recommend KEEP, REVIEW, or PRUNE for manual query-list maintenance. Use `definitionJson.documentRefs` as the durable document reference contract; for refs with `outputFieldKey`, produce that output using the referenced pack document ID as the template or methodology source, and preserve the document ID alongside the output artifact.

## Missing Input Policy

Ask for Apify run receipts, query offset state, candidate yield state, and cost assumptions.

## External Action Policy

Read-only audit. Do not edit query lists, actor inputs, budgets, or schedules.

## Completion Criteria

- Audit table includes query, track, spend/yield metrics, exhaustion notes, recommendation, and confidence.
- Paid source spend status is one of within_budget, near_limit, over_limit, or unknown.
- Prune/review recommendations are clearly manual follow-ups.

## Human Decision Points

- None declared

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `spend_audit_scope` | Spend Audit Scope | `json` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `linkedin_spend_audit_artifact_id` | LinkedIn Spend Audit Artifact | `file` | yes |
| `paid_source_spend_status` | Paid Source Spend Status | `string` | no |
| `audit_report` | Audit Report | `richtext` | no |

## Document References

- `vc.document.paid_source_spend_audit_checklist` (output_template) -> `linkedin_spend_audit_artifact_id`

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/audit-linkedin-query-spend.yaml`
- Alludium task ID: `vc.audit_linkedin_query_spend`
- Task family: `origination_spend_audit`
- Lifecycle stage: `operate`
- Recommended agent: `vc-pipeline-autopilot` (Alludium template `vc_pipeline_autopilot`)
- Supported project types:
  - `vc_origination_pipeline`
- Supported project scopes:
  - `project_instance`

## Required Skills

- `vc-linkedin-query-spend-audit`
- `vc-source-registry-and-state-management`
- `citation-enforcement`

## Planned Skills

- `vc-linkedin-query-spend-audit`
- `vc-source-registry-and-state-management`
- `citation-enforcement`
