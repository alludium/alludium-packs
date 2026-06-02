---
id: vc.harmonic_setup
title: Set Up Harmonic for Deal Pipelines
slug: harmonic-setup
agent: vc-integration-operator
skills:
- vc-harmonic-discovery
- vc-harmonic-sync-read
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-integrations/harmonic-setup.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Set Up Harmonic for Deal Pipelines

## Objective

Coordinate Harmonic connection readiness, saved-search discovery, and read-preview policy for Deal Pipeline setup.

## What To Do

Confirm that Harmonic is a selected company-intelligence source, check connection readiness, then coordinate saved-search/source discovery and reviewed read-preview setup. Create child tasks from the declared integrationSetup flow only when the user chooses that step. Keep imports, watchlist creation, recurring sync, and external writes disabled unless a later human approval explicitly creates that task.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Setup Goal.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Deliverable

- Produce a concise, reviewable task response that a human can act on.
- Also include a short human-readable summary covering: Setup Summary, Accepted Connection Scope, Child Task Plan, Sync Policy. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

If Harmonic is not authorized, has no discovered tools, or no saved-search/source scope is selected, keep setup incomplete and ask for authorization, tool discovery, a supplied inventory, or the source-scope decision needed for discovery.

## Guardrails

Setup orchestration only. Do not import companies or people, create watchlists, enable recurring sync, write to Harmonic, or create Deal Pipeline projects from this setup task.

## Completion Criteria

- Connection readiness or missing-authorization/tool-discovery evidence is recorded.
- Candidate saved-search/source scope is complete or the unanswered scope questions are explicit.
- Read-preview policy is recorded without enabling import, recurring sync, or writes.
- The accepted connection scope states whether access is personal, project-shared, or workspace-shared.

## Human Review

- Choose whether the Harmonic connection is personal, project-shared, or workspace-shared.
- Choose the saved search, daily search, company, or source scope.
- Approve any read-preview, import, watchlist, or recurring sync task separately.
