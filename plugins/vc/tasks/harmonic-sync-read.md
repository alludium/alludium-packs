---
id: vc.harmonic_sync_read
title: Preview Harmonic Search Results
slug: harmonic-sync-read
agent: vc-integration-operator
skills:
- vc-harmonic-sync-read
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-integrations/harmonic-sync-read.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Preview Harmonic Search Results

## Objective

Preview selected Harmonic company or saved-search results before using them as VC sourcing or screening context.

## What To Do

Build a Harmonic read preview only after discovery has selected a saved search, daily search, company, or result scope and live tool IDs are known. The current local platform catalog has no trusted Harmonic tool rows, so treat live reads as blocked until tool discovery after authorization succeeds. When tools exist, process only selected company/search results and propose target mapping as sourcing context, task context, watchlist candidates, or Deal Pipeline setup context.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Selected Harmonic Scope.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Deliverable

- Produce a concise, reviewable task response that a human can act on.
- Also include a short human-readable summary covering: Harmonic Results Preview, Target Context Mapping. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for selected Harmonic source scope and discovered tool IDs before processing search results.

## Guardrails

Read preview only. Do not create Deal Pipelines, import companies, mark net-new results as seen, update saved searches, export contacts, or write back to Harmonic.

## Completion Criteria

- Preview rows include Harmonic source IDs, company/person identity signals, relevance notes, and rejection reasons when available.
- Tool IDs used or missing are named.
- Import, watchlist creation, or recurring monitoring approval remains separate from the preview.

## Human Review

- Approve result rows before importing or attaching context.
- Approve dedupe decisions and target mappings.
