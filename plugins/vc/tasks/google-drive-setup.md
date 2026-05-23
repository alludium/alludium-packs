---
id: vc.google_drive_setup
title: Set Up Google Drive for VC Deal Rooms
slug: google-drive-setup
agent: vc-integration-operator
skills:
- vc-google-drive-discovery
- vc-google-drive-sync-read
- vc-google-drive-sync-write
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-integrations/google-drive-setup.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Set Up Google Drive for VC Deal Rooms

Coordinate Google Drive connection readiness, folder discovery, read-preview policy, and optional file proposal scope for VC Deal Room setup.

## Instructions

Confirm that Google Drive is a selected document source, check connection readiness, then coordinate folder/file discovery and reviewed read-preview setup. Create child tasks from the declared integrationSetup flow only when the user chooses that step. Keep file creation, import, broad indexing, recurring sync, sharing changes, and Drive writes disabled unless a later human approval explicitly creates that task.

## Missing Input Policy

If Google Drive is not authorized or no folder/file scope is selected, keep setup incomplete and ask for connection authorization, shared-drive context, or the source-scope decision needed for discovery.

## External Action Policy

Setup orchestration only. Do not import files, change sharing, create folders, write documents, enable recurring sync, or create Deal Room projects from this setup task.

## Completion Criteria

- Connection readiness or missing-authorization evidence is recorded.
- Candidate folder/file scope is complete or the unanswered scope questions are explicit.
- Read-preview and optional file-proposal policies are recorded without enabling external writes.
- The accepted connection scope states whether access is personal, project-shared, or workspace-shared.

## Human Decision Points

- Choose whether the Google Drive connection is personal, project-shared, or workspace-shared.
- Choose the shared drive, folder, or file scope.
- Approve any read-preview, import, recurring sync, or write task separately.

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

- Source template: `alludium/task-definition-templates/vc-integrations/google-drive-setup.yaml`
- Alludium task ID: `vc.google_drive_setup`
- Task family: `integration_setup`
- Recommended agent: `vc-integration-operator` (Alludium template `vc_integration_operator`)
- Supported project types:
  - `vc_deal_room`
- Supported project scopes:
  - `project_management`

## Required Skills

- `vc-google-drive-discovery`
- `vc-google-drive-sync-read`
- `vc-google-drive-sync-write`
- `citation-enforcement`
