---
id: vc.affinity_sync_read
title: Preview Affinity Pipeline Import
slug: affinity-sync-read
agent: vc-integration-operator
skills:
- vc-affinity-sync-read
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-integrations/affinity-sync-read.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Preview Affinity Pipeline Import

## Objective

Preview selected Affinity opportunity, company, person, note, and list-entry data before importing it into Deal Pipeline context.

## What To Do

Build a Deal Pipeline Affinity read-sync preview from the approved list/source and stage scope. Use affinity get list entries, affinity list opportunities, affinity get opportunity, affinity search companies, affinity get company, affinity search persons, affinity get person, and affinity list company notes only inside approved scope. Show proposed project, field, task, artifact, and setup-context mappings before import. Durable project creation and initial import belong to `affinity-deal-room-import` after reviewed user approval.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Selected Affinity Scope.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Deliverable

- Produce a concise, reviewable task response that a human can act on.
- Also include a short human-readable summary covering: Affinity Import Preview, Mapping Decisions. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for the selected Affinity source scope before creating a preview.

## Guardrails

Preview/import design only. Do not import records or enable recurring sync without explicit approval.

## Completion Criteria

- Preview rows include source IDs, target mappings, conflicts, and rejection reasons.
- Tool IDs used are named.
- Import approval remains separate from the preview and is executed through affinity-deal-room-import.

## Human Review

- Approve preview rows before import.
- Approve duplicate resolution and target mappings.
