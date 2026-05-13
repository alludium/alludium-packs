---
id: vc.apify_setup
title: Set Up Apify for VC Origination
slug: apify-setup
agent: vc-pipeline-autopilot
skills:
- vc-apify-discovery
- vc-apify-sync-read
- citation-enforcement
---

<!-- Generated from alludium/task-definition-templates/vc-integrations/apify-setup.yaml; do not edit directly. Run python plugins/vc/scripts/generate_markdown.py after changing the YAML source. -->

# Set Up Apify for VC Origination

Coordinate Apify connection readiness, actor allowlist, discovery scope, and read-preview policy for a VC origination pipeline.

## Instructions

Confirm that Apify is a selected origination source, then coordinate connection readiness, actor allowlist, run budget, and reviewed discovery scope. Create child tasks from the declared integrationSetup flow only when the user chooses that step. Keep imports, scheduled actor runs, candidate scoring, CRM writes, outreach, and Deal Room promotion disabled unless a later human approval explicitly creates that task.

## Missing Input Policy

If Apify is not authorized, no actor allowlist is approved, or no source scope is selected, keep setup incomplete and ask for authorization, approved actors, budget policy, or source-scope decisions.

## External Action Policy

Setup orchestration only. Do not run scheduled sourcing, import candidates, write candidate state, contact founders, update external systems, or create Deal Room projects from this setup task.

## Completion Criteria

- Apify connection evidence is connected or the missing authorization/tool-discovery gap is recorded.
- Actor allowlist and source-scope decisions are recorded, or unanswered decisions are explicit.
- Read-preview, run-budget, and cost-control policies are recorded without enabling scheduled runs or writes.
- The accepted connection scope states whether access is personal, project-shared, or workspace-shared.

## Human Decision Points

- Choose whether the Apify connection is personal, project-shared, or workspace-shared.
- Approve actor allowlist and source policy for LinkedIn, X, or other actors.
- Approve any read-preview, scheduled run, import, or write task separately.

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

- Source template: `alludium/task-definition-templates/vc-integrations/apify-setup.yaml`
- Alludium task ID: `vc.apify_setup`
- Task family: `integration_setup`
- Recommended agent: `vc-pipeline-autopilot` (Alludium template `vc_pipeline_autopilot`)
- Supported project types:
  - `vc_origination_pipeline`
- Supported project scopes:
  - `project_management`

## Required Skills

- `vc-apify-discovery`
- `vc-apify-sync-read`
- `citation-enforcement`

## Planned Skills

- `vc-apify-discovery`
- `vc-apify-sync-read`
- `citation-enforcement`
