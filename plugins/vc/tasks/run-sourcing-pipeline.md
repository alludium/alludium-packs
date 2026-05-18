---
id: vc.run_sourcing_pipeline
title: Run VC Sourcing Pipeline
slug: run-sourcing-pipeline
agent: vc-pipeline-autopilot
skills:
- vc-origination-pipeline-orchestration
- vc-source-registry-and-state-management
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/run-sourcing-pipeline.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Run VC Sourcing Pipeline

Orchestrate one VC origination sourcing pass across approved sources with source-state receipts, cost gates, and human approval boundaries.

## Instructions

Run only approved origination sources and preserve the reference workflow order across Companies House recent and mature windows, GitHub builder signals, X/Twitter builder signals, cheap enrichment, Affinity relationship check, first verdict, LinkedIn company enrichment only for Meet or Watch, second verdict for fresh LinkedIn company data, sync proposal, portfolio-overlap review, screen, outreach drafts, and digest. LinkedIn people discovery is weekly by default or explicit override only. Create child tasks for the enabled steps; keep each child within its own source/action boundary. Use `definitionJson.documentRefs` as the durable document reference contract; for refs with `outputFieldKey`, produce that output using the referenced pack document ID as the template or methodology source, and preserve the document ID alongside the output artifact.

## Missing Input Policy

Ask for enabled source registry, cadence policy, budget cap, result limits, review thresholds, and credential readiness before running. If paid-source budget is missing, run only no-cost previews or produce a dry-run plan.

## External Action Policy

Read, score, draft, and propose only unless a child task has explicit human approval for the specific write. Do not send outreach, silently update CRM/manual decisions, or create Deal Room projects.

## Completion Criteria

- Run receipt lists enabled sources, skipped sources, cadence mode, result limits, cost metadata or missing cost metadata, and degraded-source notes.
- Run status is one of dry_run, completed, partial, blocked, or failed.
- Candidate counts are split by source, new, duplicate, rejected, enriched, Meet, Watch, Pass, screened, outreach-drafted, and promotion-ready where available.
- Source-state update includes dedupe keys, pagination/offset notes, seen IDs, and unresolved state-store gaps.
- Follow-up child tasks and human approvals are listed without performing unapproved writes.

## Human Decision Points

- Approve enabling or changing a recurring schedule.
- Approve paid-source actor runs and source-specific result limits.
- Approve sync writes, outreach sending, or Deal Room promotion in separate tasks.

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `sourcing_run_scope` | Sourcing Run Scope | `json` | yes |
| `run_mode` | Run Mode | `string` | no |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `sourcing_run_summary` | Sourcing Run Summary | `richtext` | no |
| `run_status` | Run Status | `string` | no |
| `new_candidates_count` | New Candidates Count | `number` | no |
| `promotion_ready_count` | Promotion Ready Count | `number` | no |
| `run_completed_at` | Run Completed At | `date` | no |
| `run_receipt_artifact_id` | Run Receipt Artifact | `file` | yes |
| `candidate_batch_artifact_id` | Candidate Batch Artifact | `file` | yes |
| `source_state_artifact_id` | Source State Artifact | `file` | yes |
| `child_task_plan` | Child Task Plan | `richtext` | yes |

## Document References

- `vc.document.candidate_batch_template` (output_template) -> `candidate_batch_artifact_id`
- `vc.document.origination_pipeline_sop` (operating_guidance)

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/run-sourcing-pipeline.yaml`
- Alludium task ID: `vc.run_sourcing_pipeline`
- Task family: `origination_pipeline_run`
- Lifecycle stage: `source`
- Recommended agent: `vc-pipeline-autopilot` (Alludium template `vc_pipeline_autopilot`)
- Supported project types:
  - `vc_origination_pipeline`
- Supported project scopes:
  - `project_instance`

## Required Skills

- `vc-origination-pipeline-orchestration`
- `vc-source-registry-and-state-management`
- `citation-enforcement`

## Planned Skills

- `vc-origination-pipeline-orchestration`
- `vc-source-registry-and-state-management`
- `citation-enforcement`
