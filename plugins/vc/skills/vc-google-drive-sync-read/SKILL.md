---
id: vc-google-drive-sync-read
name: "VC Google Drive Sync Read"
description: >
  Preview selected Google Drive file, folder, document, and comment context for
  Deal Pipeline tasks before any attachment or import.
tags:
  - vc
  - google-drive
  - documents
  - sync-read
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: required
      required: true
      note: Use `google_drive-list-files`, `google_drive-get-file-by-id`, `google_drive-download-file`, `google_drive-list-comments`, and `google_drive-get-comment` only inside approved folder/file scope.
      gracefulDegradation: Ask for supplied files, excerpts, or exported documents.
  routingHints:
    preferredSurface: skill
    notes:
      - Read sync is a preview and mapping step; attachment or import requires separate approval.
---

# VC Google Drive Sync Read

Use this skill after Google Drive discovery has selected the approved shared drive, folder, file, or source scope.

## Required Inputs

- Google Drive discovery report
- Approved folder, file, or source scope
- Deal, project, or task context that explains why the Drive content is needed
- Sensitivity exclusions and target mapping preference

## Tool Plan

Use Google Drive tools only within approved scope:

1. Use `google_drive-list-files` to enumerate selected folder contents.
2. Use `google_drive-get-file-by-id` to inspect metadata for selected files.
3. Use `google_drive-download-file` only for explicitly approved files.
4. Use `google_drive-list-comments` and `google_drive-get-comment` only when comments are in scope.

## Preview Output

Return:

- source file/folder IDs, names, MIME types, timestamps, and owners when available
- summarized context with provenance
- suggested target: Deal Pipeline setup context, task context, artifact input, or human reference
- rejected files and reasons
- duplicate or sensitivity caveats

## Boundaries

- Do not attach or import without preview approval.
- Do not read outside the approved folder/file scope.
- Do not create, upload, copy, move, delete, trash, share, update, or permission-change files.
- Do not treat Drive documents as final investment evidence without corroboration.
