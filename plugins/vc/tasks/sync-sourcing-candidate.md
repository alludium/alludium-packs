---
id: vc.sync_sourcing_candidate
title: Sync Sourcing Candidate
slug: sync-sourcing-candidate
agent: vc-sourcing-operator
skills:
- vc-source-registry-and-state-management
- vc-sourcing-dedupe-and-novelty-check
- citation-enforcement
- vc-notion-sync-write
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/sync-sourcing-candidate.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Sync Sourcing Candidate

## Objective

Prepare or apply reviewed candidate state sync while preserving manual workflow decisions.

## What To Do

Mirror the reference pipeline's sync safety. Upsert by stable source key and preserve manual Action/Status-style decisions unless the current value is empty or explicitly auto-set. Distinguish dry-run sync plan from approved write. If syncing to a review table, include columns equivalent to Action, Urgency, Fit, Confidence, funding/HQ concerns, relationship context, source track, reasons, receipts, and analyst notes.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Sync Scope.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Deliverable

- Create or update **Sync Plan Artifact** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.
- Also include a short human-readable summary covering: Sync Status, Sync Report. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for target system, write approval, candidate batch, dedupe key policy, protected manual fields, and dry-run/real-run mode.

## Guardrails

Default is dry-run proposal. Do not write to Notion, CRM, Slack, ClickUp, or any external system without explicit human approval in this task.

## Completion Criteria

- Sync plan or write receipt lists created, updated, skipped, protected, rejected, and failed rows.
- Manual fields protected from overwrite are named.
- Dedupe/upsert keys and source receipts are recorded.
