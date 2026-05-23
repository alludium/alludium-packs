---
id: vc.google_drive_sync_write
title: Draft Google Drive File Proposals
slug: google-drive-sync-write
agent: vc-integration-operator
skills:
- vc-google-drive-sync-write
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-integrations/google-drive-sync-write.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Draft Google Drive File Proposals

Draft reviewable Google Drive file or comment proposals from VC task outputs without performing broad Drive mutations.

## Instructions

Draft Google Drive proposals only. Each proposal must include the target folder or file ID, intended action, source evidence, owner approval, and a clear statement that no Drive write has been performed. Reference available write surfaces such as `google_drive-add-comment`, `google_drive-reply-to-comment`, `google_drive-create-file-from-text`, or `google_drive-upload-file` only as later approved execution candidates; this task must not execute them.

## Missing Input Policy

Ask for the source artifact, target Drive location, proposed file/comment content, and approval owner before drafting.

## External Action Policy

Draft only. Do not create files, upload files, create folders, copy files, share files, move files, delete files, trash files, update metadata, resolve access proposals, or change permissions.

## Completion Criteria

- Every proposal is evidence-backed and approval-gated.
- The output clearly states no Google Drive writes were performed.
- Any broad file, sharing, deletion, move, or permission request is rejected or routed to a separate human-admin process.

## Human Decision Points

- Approve exact target, file/comment content, and action before any future execution.
- Approve whether a Drive write is appropriate at all for the workflow.

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `drive_write_source` | Drive Write Source | `json` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `google_drive_write_proposals` | Google Drive Write Proposals | `richtext` | no |

## Routing

- Source template: `alludium/task-definition-templates/vc-integrations/google-drive-sync-write.yaml`
- Alludium task ID: `vc.google_drive_sync_write`
- Task family: `integration_sync_write`
- Recommended agent: `vc-integration-operator` (Alludium template `vc_integration_operator`)
- Supported project types:
  - `vc_deal_room`
- Supported project scopes:
  - `project_management`

## Required Skills

- `vc-google-drive-sync-write`
- `citation-enforcement`
