---
id: vc.affinity_setup
title: Set Up Affinity for Deal Pipelines
slug: affinity-setup
agent: vc-integration-operator
skills:
- vc-affinity-discovery
- vc-affinity-sync-read
- vc-affinity-sync-write
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-integrations/affinity-setup.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Set Up Affinity for Deal Pipelines

Coordinate Affinity connection readiness, list discovery, read-preview policy, and optional write-back proposal scope for Deal Pipeline setup.

## Instructions

Confirm that Affinity is the selected CRM path from the task integration setup context, then lead the setup through read-only discovery in short phases. Phase 1 is source scope; make the lightest read-only Affinity call needed to confirm connection readiness, list available lists or pipelines, call task-management.askTaskQuestions with exactly one required select question using presentation.control=cards and presentation.layout=stack, map the answer to setupEvidence.selectedSourceScope with responseMappings, and stop. Do not inspect a list, fetch records, or continue discovery before the source-scope answer is recorded. Phase 2 is stage mapping; retrieve the recorded source-scope answer from task context if needed, inspect only the selected source, propose source-stage to Deal Pipeline stage mappings with exactly one required inputType=mapping question, map the answer to setupEvidence.acceptedStageMapping, and stop. Phase 3 is seed selection; retrieve the accepted mapping from task context if needed, fetch one bounded visible set of recent deals from the selected scope, then ask exactly one required inputType=multiselect card question with presentation.allowSelectAll=true, presentation.selectAllLabel="Select all visible deals", presentation.layout=stack, and a defer option. Use the first safe bounded result you can inspect; do not loop over broad list-entry calls trying to perfect the data. If the source returns too many records or sparse fields, present the first visible bounded candidate set with the fields available and say that later import/sync tasks can refine filtering. Map the answer to setupEvidence.seedSelection and stop. Present no more than 100 records in one question; "all" means all visible records in that question. If the task-question tool rejects the option count, reduce the visible candidate set before retrying and keep the same presentation fields. Phase 4 is final review; call task-management.getTaskDetail and read the recorded questionResponses before summarizing. Summarize the selected source, accepted mapping, selected visible seed deals or defer decision, and sync-readiness notes exactly as recorded; do not say all visible deals were selected unless the recorded seed answer selected every visible deal option. Ask the user to use Complete step if the summary is correct. Do not call task-management.completeTask, task-management.completeHumanTask, or any completion tool yourself. Do not call user-agent-deployment.getAgentSetupStatus for this task; that reports the assigned agent deployment, not the pack integration requirement. Create child tasks from the declared integrationSetup flow only when the user chooses that step. Keep all import, recurring sync, CRM writes, note creation, and stage movement disabled unless a later human approval explicitly creates that task.

## Missing Input Policy

If Affinity is not authorized or no source scope is selected, keep setup incomplete, ask the user to authorize Affinity or provide an exported list/stage snapshot, and stop. Do not complete this task while connection evidence or required task questions are unresolved.

## External Action Policy

Setup orchestration only. Do not import records, enable recurring sync, update CRM fields, write notes, move stages, or create Deal Pipeline projects from this setup task.

## Completion Criteria

- Affinity connection evidence is connected, or a user-approved exported snapshot fallback is recorded in task context.
- Required task questions for connection sharing scope and discovery scope are answered.
- The selected Affinity list or pipeline has been inspected in read-only mode.
- Source stages or swimlanes have been mapped to Deal Pipeline stages, or the user explicitly chose to defer mapping.
- A bounded visible deal set has been presented and the user selected visible seed deals, selected all visible deals, or explicitly chose to defer seed selection.
- Read-preview and optional write-proposal policies are recorded without enabling external writes.
- The accepted connection scope states whether access is personal, project-shared, or workspace-shared.
- The agent has summarized the reviewed evidence and asked the user to complete the task; the agent has not completed it.

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
| `selected_source_scope` | Selected Source Scope | `json` | no |
| `accepted_stage_mapping` | Accepted Stage Mapping | `json` | no |
| `seed_selection` | Seed Selection | `json` | no |
| `sync_policy` | Sync Policy | `json` | no |

## Routing

- Source template: `alludium/task-definition-templates/vc-integrations/affinity-setup.yaml`
- Alludium task ID: `vc.affinity_setup`
- Task family: `integration_setup`
- Recommended agent: `vc-integration-operator` (Alludium template `vc_integration_operator`)
- Supported project types:
  - `vc_deal_room`
- Supported project scopes:
  - `project_management`

## Required Skills

- `vc-affinity-discovery`
- `vc-affinity-sync-read`
- `vc-affinity-sync-write`
- `citation-enforcement`
