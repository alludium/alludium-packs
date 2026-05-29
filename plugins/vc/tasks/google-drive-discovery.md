---
id: vc.google_drive_discovery
title: Explore Google Drive Sources
slug: google-drive-discovery
agent: vc-integration-operator
skills:
- vc-google-drive-discovery
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-integrations/google-drive-discovery.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Explore Google Drive Sources

## Objective

Discover Google Drive shared drive, folder, and file scope before selected Deal Pipeline context reads.

## What To Do

Use the connected google drive application to confirm account context with `google_drive-get-current-user`, enumerate shared drives with `google_drive-search-shared-drives`, and inspect candidate folders/files with `google_drive-list-files`, `google_drive-find-folder`, `google_drive-find-file`, `google_drive-get-folder-id-for-path`, and `google_drive-get-file-by-id` inside obvious VC source areas only. Ask the user to choose the shared drive, folder, file, or source-scope boundary before any read-sync task.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Discovery Goal.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Deliverable

- Produce a concise, reviewable task response that a human can act on.
- Also include a short human-readable summary covering: Google Drive Discovery Report, Source Scope Questions. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

If Google Drive is not authorized, ask for authorization or a supplied folder/file inventory.

## Guardrails

Discovery only. Do not download file contents, create files, create folders, share files, move files, delete files, trash files, update metadata, resolve access proposals, or change permissions.

## Completion Criteria

- Candidate shared drives, folders, files, and source scopes are listed with stable IDs when available.
- Tool IDs used or missing are named.
- User choices needed before file or folder preview are explicit.

## Human Review

- Choose shared drive, folder, or file scope before sync read.
- Approve whether comments, folder listings, or file content previews are in scope.
- Approve any later import or attachment separately.
