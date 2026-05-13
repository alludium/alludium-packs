---
id: vc.google_drive_discovery
title: Explore Google Drive Sources
slug: google-drive-discovery
agent: vc-pipeline-autopilot
skills:
- vc-google-drive-discovery
- citation-enforcement
---

# Explore Google Drive Sources

Discover Google Drive shared drive, folder, and file scope before selected VC Deal Room context reads.

## Instructions

Use the connected `google_drive` application to confirm account context with `google_drive-get-current-user`, enumerate shared drives with `google_drive-search-shared-drives`, and inspect candidate folders/files with `google_drive-list-files`, `google_drive-find-folder`, `google_drive-find-file`, `google_drive-get-folder-id-for-path`, and `google_drive-get-file-by-id` inside obvious VC source areas only. Ask the user to choose the shared drive, folder, file, or source-scope boundary before any read-sync task.

## Missing Input Policy

If Google Drive is not authorized, ask for authorization or a supplied folder/file inventory.

## External Action Policy

Discovery only. Do not download file contents, create files, create folders, share files, move files, delete files, trash files, update metadata, resolve access proposals, or change permissions.

## Completion Criteria

- Candidate shared drives, folders, files, and source scopes are listed with stable IDs when available.
- Tool IDs used or missing are named.
- User choices needed before file or folder preview are explicit.

## Human Decision Points

- Choose shared drive, folder, or file scope before sync read.
- Approve whether comments, folder listings, or file content previews are in scope.
- Approve any later import or attachment separately.

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `discovery_goal` | Discovery Goal | `string` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `google_drive_discovery_report` | Google Drive Discovery Report | `richtext` | no |
| `source_scope_questions` | Source Scope Questions | `json` | no |

## Routing

- Source template: `alludium/task-definition-templates/vc-integrations/google-drive-discovery.yaml`
- Alludium task ID: `vc.google_drive_discovery`
- Task family: `integration_discovery`
- Recommended agent: `vc-pipeline-autopilot` (Alludium template `vc_pipeline_autopilot`)
- Supported project types:
  - `vc_deal_room`
- Supported project scopes:
  - `project_management`

## Required Skills

- `vc-google-drive-discovery`
- `citation-enforcement`

## Planned Skills

- `vc-google-drive-discovery`
- `citation-enforcement`
