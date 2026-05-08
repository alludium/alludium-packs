---
id: vc-google-drive-sync-write
name: "VC Google Drive Sync Write"
description: >
  Draft Google Drive file or comment proposals for VC workflows without broad
  file creation, sharing, deletion, moving, or permission changes.
tags:
  - vc
  - google-drive
  - documents
  - sync-write
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: recommended
      required: false
      note: Later approved execution candidates may include `google_drive-add-comment`, `google_drive-reply-to-comment`, `google_drive-create-file-from-text`, or `google_drive-upload-file`; this skill drafts proposals only.
      gracefulDegradation: Produce file/comment proposals for human copy-and-apply review.
  routingHints:
    preferredSurface: skill
    notes:
      - This skill drafts proposals. It does not mutate Google Drive.
---

# VC Google Drive Sync Write

Use this skill to turn approved Alludium outputs into reviewable Google Drive proposals.

## Allowed Proposal Types

- Comment draft on an approved diligence file
- File draft for a memo, source summary, or handoff in an approved folder
- Upload proposal for a generated artifact when the target folder and owner are explicit
- Folder-placement recommendation for human review

## Required Evidence

Every proposal must include:

- target folder or file ID
- proposed title, body, comment, or upload source
- source artifact, task output, meeting note, or human decision that supports it
- approval owner and audit note
- explicit statement that no Drive write has been performed

## Tool Guidance

Available write surfaces include `google_drive-add-comment`, `google_drive-reply-to-comment`, `google_drive-create-file-from-text`, and `google_drive-upload-file`, but use them only in a later approved runtime workflow. This skill does not execute writes.

## Boundaries

- Do not create files, upload files, create folders, copy files, move files, delete files, trash files, share files, resolve access proposals, update metadata, or change permissions.
- Do not propose broad file operations.
- Do not claim Drive was updated unless a tool result confirms it in a separate approved workflow.
