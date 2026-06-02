---
id: vc.apify_setup
title: Set Up Apify for Origination
slug: apify-setup
agent: vc-integration-operator
skills:
- vc-apify-discovery
- vc-apify-sync-read
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-integrations/apify-setup.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Set Up Apify for Origination

## Objective

Coordinate Apify connection readiness, actor allowlist, discovery scope, and read-preview policy for a VC origination pipeline.

## What To Do

Confirm that Apify is a selected origination source, then coordinate connection readiness, actor allowlist, run budget, and reviewed discovery scope. Create child tasks from the declared integrationSetup flow only when the user chooses that step. Keep imports, scheduled actor runs, candidate scoring, CRM writes, outreach, and Deal Pipeline promotion disabled unless a later human approval explicitly creates that task.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Setup Goal.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Deliverable

- Produce a concise, reviewable task response that a human can act on.
- Also include a short human-readable summary covering: Setup Summary, Accepted Connection Scope, Child Task Plan, Sync Policy. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

If Apify is not authorized, no actor allowlist is approved, or no source scope is selected, keep setup incomplete and ask for authorization, approved actors, budget policy, or source-scope decisions.

## Guardrails

Setup orchestration only. Do not run scheduled sourcing, import candidates, write candidate state, contact founders, update external systems, or create Deal Pipeline projects from this setup task.

## Completion Criteria

- Apify connection evidence is connected or the missing authorization/tool-discovery gap is recorded.
- Actor allowlist and source-scope decisions are recorded, or unanswered decisions are explicit.
- Read-preview, run-budget, and cost-control policies are recorded without enabling scheduled runs or writes.
- The accepted connection scope states whether access is personal, project-shared, or workspace-shared.

## Human Review

- Choose whether the Apify connection is personal, project-shared, or workspace-shared.
- Approve actor allowlist and source policy for LinkedIn, X, or other actors.
- Approve any read-preview, scheduled run, import, or write task separately.
