---
id: vc.google_drive_setup
title: Set Up Google Drive for Deal Pipelines
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

# Set Up Google Drive for Deal Pipelines

## Objective

Coordinate Google Drive connection readiness, folder discovery, read-preview policy, and optional file proposal scope for Deal Pipeline setup.

## What To Do

Confirm that Google Drive is a selected document source, check connection readiness, then coordinate folder/file discovery and reviewed read-preview setup. Create child tasks from the declared integrationSetup flow only when the user chooses that step. Keep file creation, import, broad indexing, recurring sync, sharing changes, and Drive writes disabled unless a later human approval explicitly creates that task.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Setup Goal.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Deliverable

- Produce a concise, reviewable task response that a human can act on.
- Also include a short human-readable summary covering: Setup Summary, Accepted Connection Scope, Child Task Plan, Sync Policy. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

If Google Drive is not authorized or no folder/file scope is selected, keep setup incomplete and ask for connection authorization, shared-drive context, or the source-scope decision needed for discovery.

## Guardrails

Setup orchestration only. Do not import files, change sharing, create folders, write documents, enable recurring sync, or create Deal Pipeline projects from this setup task.

## Completion Criteria

- Connection readiness or missing-authorization evidence is recorded.
- Candidate folder/file scope is complete or the unanswered scope questions are explicit.
- Read-preview and optional file-proposal policies are recorded without enabling external writes.
- The accepted connection scope states whether access is personal, project-shared, or workspace-shared.

## Human Review

- Choose whether the Google Drive connection is personal, project-shared, or workspace-shared.
- Choose the shared drive, folder, or file scope.
- Approve any read-preview, import, recurring sync, or write task separately.
