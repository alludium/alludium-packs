---
id: vc.harmonic_setup
title: Set Up Harmonic for VC Deal Rooms
slug: harmonic-setup
agent: vc-pipeline-autopilot
skills:
- vc-harmonic-discovery
- vc-harmonic-sync-read
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-integrations/harmonic-setup.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Set Up Harmonic for VC Deal Rooms

Coordinate Harmonic connection readiness, saved-search discovery, and read-preview policy for VC Deal Room setup.

## Instructions

Confirm that Harmonic is a selected company-intelligence source, check connection readiness, then coordinate saved-search/source discovery and reviewed read-preview setup. Create child tasks from the declared integrationSetup flow only when the user chooses that step. Keep imports, watchlist creation, recurring sync, and external writes disabled unless a later human approval explicitly creates that task.

## Missing Input Policy

If Harmonic is not authorized, has no discovered tools, or no saved-search/source scope is selected, keep setup incomplete and ask for authorization, tool discovery, a supplied inventory, or the source-scope decision needed for discovery.

## External Action Policy

Setup orchestration only. Do not import companies or people, create watchlists, enable recurring sync, write to Harmonic, or create Deal Room projects from this setup task.

## Completion Criteria

- Connection readiness or missing-authorization/tool-discovery evidence is recorded.
- Candidate saved-search/source scope is complete or the unanswered scope questions are explicit.
- Read-preview policy is recorded without enabling import, recurring sync, or writes.
- The accepted connection scope states whether access is personal, project-shared, or workspace-shared.

## Human Decision Points

- Choose whether the Harmonic connection is personal, project-shared, or workspace-shared.
- Choose the saved search, daily search, company, or source scope.
- Approve any read-preview, import, watchlist, or recurring sync task separately.

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

- Source template: `alludium/task-definition-templates/vc-integrations/harmonic-setup.yaml`
- Alludium task ID: `vc.harmonic_setup`
- Task family: `integration_setup`
- Recommended agent: `vc-pipeline-autopilot` (Alludium template `vc_pipeline_autopilot`)
- Supported project types:
  - `vc_deal_room`
- Supported project scopes:
  - `project_management`

## Required Skills

- `vc-harmonic-discovery`
- `vc-harmonic-sync-read`
- `citation-enforcement`
