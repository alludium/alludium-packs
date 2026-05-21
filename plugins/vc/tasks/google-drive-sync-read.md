---
id: vc.google_drive_sync_read
title: Preview Google Drive Context
slug: google-drive-sync-read
agent: vc-pipeline-autopilot
skills:
- vc-google-drive-sync-read
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-integrations/google-drive-sync-read.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Preview Google Drive Context

Preview selected Google Drive file, folder, and document context before attaching or importing it into VC Deal Room tasks.

## Instructions

Build a read preview from the approved Google Drive source scope. Use `google_drive-list-files`, `google_drive-get-file-by-id`, `google_drive-download-file`, `google_drive-list-comments`, and `google_drive-get-comment` only for selected folders or files. Summarize proposed target mapping as Deal Room setup context, task context, artifact input, or human reference before any attachment or import.

## Missing Input Policy

Ask for approved shared drive, folder, or file scope before reading contents or comments.

## External Action Policy

Read preview only. Do not attach, import, create, upload, copy, share, move, delete, trash, update, or change permissions without a separate approval path.

## Completion Criteria

- Preview names source file/folder IDs, MIME types, owners or timestamps when available, and sensitivity caveats.
- Proposed target mappings and rejected files are explicit.
- Attachment or import approval remains separate from the preview.

## Human Decision Points

- Approve selected files, folders, and comments before attaching them to project or task context.
- Approve duplicate handling and target mapping.

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `selected_google_drive_scope` | Selected Google Drive Scope | `json` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `google_drive_context_preview` | Google Drive Context Preview | `richtext` | no |
| `target_context_mapping` | Target Context Mapping | `json` | no |

## Routing

- Source template: `alludium/task-definition-templates/vc-integrations/google-drive-sync-read.yaml`
- Alludium task ID: `vc.google_drive_sync_read`
- Task family: `integration_sync_read`
- Recommended agent: `vc-pipeline-autopilot` (Alludium template `vc_pipeline_autopilot`)
- Supported project types:
  - `vc_deal_room`
- Supported project scopes:
  - `project_management`

## Required Skills

- `vc-google-drive-sync-read`
- `citation-enforcement`
