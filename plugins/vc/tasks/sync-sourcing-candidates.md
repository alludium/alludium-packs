---
id: vc.sync_sourcing_candidates
title: Sync Sourcing Candidates
slug: sync-sourcing-candidates
agent: vc-dealflow-concierge
skills:
- vc-source-registry-and-state-management
- vc-sourcing-dedupe-and-novelty-check
- citation-enforcement
---

# Sync Sourcing Candidates

Prepare or apply reviewed candidate state sync while preserving manual workflow decisions.

## Instructions

Mirror the reference pipeline's sync safety. Upsert by stable source key and preserve manual Action/Status-style decisions unless the current value is empty or explicitly auto-set. Distinguish dry-run sync plan from approved write. If syncing to a review table, include columns equivalent to Action, Urgency, Fit, Confidence, funding/HQ concerns, relationship context, source track, reasons, receipts, and analyst notes.

## Missing Input Policy

Ask for target system, write approval, candidate batch, dedupe key policy, protected manual fields, and dry-run/real-run mode.

## External Action Policy

Default is dry-run proposal. Do not write to Notion, CRM, Slack, ClickUp, or any external system without explicit human approval in this task.

## Completion Criteria

- Sync plan or write receipt lists created, updated, skipped, protected, rejected, and failed rows.
- Manual fields protected from overwrite are named.
- Dedupe/upsert keys and source receipts are recorded.

## Human Decision Points

- None declared

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `sync_scope` | Sync Scope | `json` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `sync_plan_artifact_id` | Sync Plan Artifact | `file` | yes |
| `sync_status` | Sync Status | `string` | no |
| `sync_report` | Sync Report | `richtext` | no |

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/sync-sourcing-candidates.yaml`
- Alludium task ID: `vc.sync_sourcing_candidates`
- Task family: `origination_candidate_sync`
- Lifecycle stage: `review`
- Recommended agent: `vc-dealflow-concierge` (Alludium template `vc_dealflow_concierge`)
- Supported project types:
  - `vc_origination_pipeline`
- Supported project scopes:
  - `project_instance`

## Required Skills

- `vc-source-registry-and-state-management`
- `vc-sourcing-dedupe-and-novelty-check`
- `citation-enforcement`

## Planned Skills

- `vc-source-registry-and-state-management`
- `vc-sourcing-dedupe-and-novelty-check`
- `vc-notion-sync-write`
- `citation-enforcement`
