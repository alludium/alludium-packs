---
id: vc.google_drive_sync_read
title: Preview Google Drive Context
slug: google-drive-sync-read
agent: vc-integration-operator
skills:
- vc-google-drive-sync-read
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-integrations/google-drive-sync-read.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Preview Google Drive Context

## Objective

Preview selected Google Drive file, folder, and document context before attaching or importing it into Deal Pipeline tasks.

## What To Do

Build a read preview from the approved Google Drive source scope. Use `google_drive-list-files`, `google_drive-get-file-by-id`, `google_drive-download-file`, `google_drive-list-comments`, and `google_drive-get-comment` only for selected folders or files. Summarize proposed target mapping as Deal Pipeline setup context, task context, artifact input, or human reference before any attachment or import.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Selected Google Drive Scope.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Deliverable

- Produce a concise, reviewable task response that a human can act on.
- Also include a short human-readable summary covering: Google Drive Context Preview, Target Context Mapping. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for approved shared drive, folder, or file scope before reading contents or comments.

## Guardrails

Read preview only. Do not attach, import, create, upload, copy, share, move, delete, trash, update, or change permissions without a separate approval path.

## Completion Criteria

- Preview names source file/folder IDs, MIME types, owners or timestamps when available, and sensitivity caveats.
- Proposed target mappings and rejected files are explicit.
- Attachment or import approval remains separate from the preview.

## Human Review

- Approve selected files, folders, and comments before attaching them to project or task context.
- Approve duplicate handling and target mapping.
