---
id: vc-google-drive-discovery
name: "VC Google Drive Discovery"
description: >
  Discover Google Drive shared drive, folder, and file scope before previewing
  founder materials, diligence files, memos, or meeting-note context.
tags:
  - vc
  - google-drive
  - documents
  - discovery
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: required
      required: true
      note: Use the connected Google Drive application `google_drive`; expected discovery tools are `google_drive-get-current-user`, `google_drive-search-shared-drives`, `google_drive-list-files`, `google_drive-find-folder`, `google_drive-find-file`, `google_drive-get-folder-id-for-path`, and `google_drive-get-file-by-id`.
      gracefulDegradation: Ask for Google Drive authorization or a supplied folder/file inventory.
  routingHints:
    preferredSurface: skill
    notes:
      - Discovery chooses source scope and must not download, attach, import, or mutate files.
---

# VC Google Drive Discovery

Use this skill to identify the Drive source scope for VC materials before any content preview or import.

## Required Inputs

- Authorized `google_drive` connection or a supplied folder/file inventory
- Intended workflow, such as founder materials intake, diligence source review, IC memo preparation, or meeting-note handoff
- Known shared drive, folder, file, company, or deal names
- Any sensitive or excluded folders

## Tool Plan

Use Google Drive tools in this order when available:

1. Use `google_drive-get-current-user` to confirm the active account context.
2. Use `google_drive-search-shared-drives` to list candidate shared drives.
3. Use `google_drive-list-files`, `google_drive-find-folder`, and `google_drive-find-file` to inspect candidate source areas.
4. Use `google_drive-get-folder-id-for-path` and `google_drive-get-file-by-id` only to resolve selected folders or files.

## Discovery Output

Return:

- `workspace_identity`: authorized account or shared-drive context
- `candidate_source_scopes`: shared drives, folders, files, or search scopes with stable IDs
- `excluded_sources`: folders/files that should stay out of scope
- `recommended_scope`: the narrowest folder/file/source scope for the workflow
- `scope_questions`: user choices needed before sync read

## Boundaries

- Do not download file contents during discovery.
- Do not attach, import, create, upload, copy, move, delete, trash, share, update, or permission-change files.
- Do not include broad shared drives or whole workspaces without explicit user selection.
