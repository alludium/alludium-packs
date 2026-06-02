---
id: vc.notion_setup
title: Set Up Notion for Deal Pipelines
slug: notion-setup
agent: vc-integration-operator
skills:
- vc-notion-discovery
- vc-notion-sync-read
- vc-notion-sync-write
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-integrations/notion-setup.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Set Up Notion for Deal Pipelines

## Objective

Coordinate Notion connection readiness, page/database discovery, read-preview policy, and optional update-proposal scope for Deal Pipeline setup.

## What To Do

Confirm that Notion is a selected workspace/document source, check connection readiness, then coordinate page/database discovery and reviewed read-preview setup. Create child tasks from the declared integrationSetup flow only when the user chooses that step. Keep database imports, recurring sync, page writes, and update proposals disabled unless a later human approval explicitly creates that task.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Setup Goal.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Deliverable

- Produce a concise, reviewable task response that a human can act on.
- Also include a short human-readable summary covering: Setup Summary, Accepted Connection Scope, Child Task Plan, Sync Policy. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

If Notion is not authorized or no page/database scope is selected, keep setup incomplete and ask for connection authorization, a supplied workspace map, or the source-scope decision needed for discovery.

## Guardrails

Setup orchestration only. Do not import databases, write pages, change permissions, enable recurring sync, or create Deal Pipeline projects from this setup task.

## Completion Criteria

- Connection readiness or missing-authorization evidence is recorded.
- Candidate page/database scope is complete or the unanswered scope questions are explicit.
- Read-preview and optional update-proposal policies are recorded without enabling external writes.
- The accepted connection scope states whether access is personal, project-shared, or workspace-shared.

## Human Review

- Choose whether the Notion connection is personal, project-shared, or workspace-shared.
- Choose the page, database, or workspace scope.
- Approve any read-preview, import, recurring sync, or write task separately.
