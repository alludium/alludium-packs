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

## Objective

Draft reviewable Google Drive file or comment proposals from VC task outputs without performing broad Drive mutations.

## What To Do

Draft Google Drive proposals only. Each proposal must include the target folder or file ID, intended action, source evidence, owner approval, and a clear statement that no Drive write has been performed. Reference available write surfaces such as `google_drive-add-comment`, `google_drive-reply-to-comment`, `google_drive-create-file-from-text`, or `google_drive-upload-file` only as later approved execution candidates; this task must not execute them.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Drive Write Source.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Deliverable

- Produce a concise, reviewable task response that a human can act on.
- Also include a short human-readable summary covering: Google Drive Write Proposals. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for the source artifact, target Drive location, proposed file/comment content, and approval owner before drafting.

## Guardrails

Draft only. Do not create files, upload files, create folders, copy files, share files, move files, delete files, trash files, update metadata, resolve access proposals, or change permissions.

## Completion Criteria

- Every proposal is evidence-backed and approval-gated.
- The output clearly states no Google Drive writes were performed.
- Any broad file, sharing, deletion, move, or permission request is rejected or routed to a separate human-admin process.

## Human Review

- Approve exact target, file/comment content, and action before any future execution.
- Approve whether a Drive write is appropriate at all for the workflow.
