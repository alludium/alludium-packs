---
id: vc.apify_sync_read
title: Preview Apify Origination Results
slug: apify-sync-read
agent: vc-integration-operator
skills:
- vc-apify-sync-read
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-integrations/apify-sync-read.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Preview Apify Origination Results

## Objective

Preview selected Apify actor results before using them as VC origination source context.

## What To Do

Build a read preview only after discovery has selected approved actors, input scope, budget limits, and result limits. Process only selected sample results and return identity signals, source receipts, cost/run metadata when available, and suggested mapping into the origination source registry.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Selected Apify Scope.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Deliverable

- Produce a concise, reviewable task response that a human can act on.
- Also include a short human-readable summary covering: Apify Results Preview, Source Registry Mapping. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for selected actors, approved input scope, run/result limits, and discovered tool IDs before processing actor output.

## Guardrails

Read preview only. Do not enable scheduled runs, import candidates, write candidate records, score candidates, contact founders, update external systems, or create Deal Pipeline projects.

## Completion Criteria

- Preview rows include actor/source IDs, candidate identity signals, source receipts, and rejection reasons when available.
- Run IDs, dataset IDs, cost metadata, or missing metadata are named.
- Import, recurring monitoring, scoring, outreach, and promotion approvals remain separate from the preview.

## Human Review

- Approve sample results before candidate import or scoring.
- Approve source registry mappings and dedupe keys separately.
