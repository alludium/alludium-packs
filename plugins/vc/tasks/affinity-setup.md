---
id: vc.affinity_setup
title: Set Up Affinity for VC Deal Rooms
slug: affinity-setup
agent: vc-pipeline-autopilot
skills:
- vc-affinity-discovery
- vc-affinity-sync-read
- vc-affinity-sync-write
- citation-enforcement
---

# Set Up Affinity for VC Deal Rooms

Coordinate Affinity connection readiness, list discovery, read-preview policy, and optional write-back proposal scope for VC Deal Room setup.

## Instructions

Confirm that Affinity is the selected CRM path from the task integration setup context, then guide the user through connection readiness, connection sharing scope, and reviewed discovery scope. Use task-management.askTaskQuestion or task-management.askTaskQuestions for missing decisions. Do not call user-agent-deployment.getAgentSetupStatus for this task; that reports the assigned agent deployment, not the pack integration requirement. Create child tasks from the declared integrationSetup flow only when the user chooses that step. Keep all import, recurring sync, CRM writes, note creation, and stage movement disabled unless a later human approval explicitly creates that task.

## Missing Input Policy

If Affinity is not authorized or no source scope is selected, keep setup incomplete, ask the user to authorize Affinity or provide an exported list/stage snapshot, and stop. Do not complete this task while connection evidence or required task questions are unresolved.

## External Action Policy

Setup orchestration only. Do not import records, enable recurring sync, update CRM fields, write notes, move stages, or create Deal Room projects from this setup task.

## Completion Criteria

- Affinity connection evidence is connected, or a user-approved exported snapshot fallback is recorded in task context.
- Required task questions for connection sharing scope and discovery scope are answered.
- Read-preview and optional write-proposal policies are recorded without enabling external writes.
- The accepted connection scope states whether access is personal, project-shared, or workspace-shared.

## Human Decision Points

- Choose whether the Affinity connection is personal, project-shared, or workspace-shared.
- Choose the Affinity list/source and active stage scope.
- Approve any read-preview, import, recurring sync, or write-back task separately.

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `setup_goal` | Setup Goal | `string` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `setup_summary` | Setup Summary | `richtext` | no |
| `accepted_connection_scope` | Accepted Connection Scope | `string` | no |
| `child_task_plan` | Child Task Plan | `json` | no |
| `sync_policy` | Sync Policy | `json` | no |

## Routing

- Source template: `alludium/task-definition-templates/vc-integrations/affinity-setup.yaml`
- Alludium task ID: `vc.affinity_setup`
- Task family: `integration_setup`
- Recommended agent: `vc-pipeline-autopilot` (Alludium template `vc_pipeline_autopilot`)
- Supported project types:
  - `vc_deal_room`
- Supported project scopes:
  - `project_management`

## Required Skills

- `vc-affinity-discovery`
- `vc-affinity-sync-read`
- `vc-affinity-sync-write`
- `citation-enforcement`

## Planned Skills

- `vc-affinity-discovery`
- `vc-affinity-sync-read`
- `vc-affinity-sync-write`
- `citation-enforcement`
