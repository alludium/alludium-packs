---
id: vc.affinity_discovery
title: Explore Affinity Lists and Stages
slug: affinity-discovery
agent: vc-integration-operator
skills:
- vc-affinity-discovery
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-integrations/affinity-discovery.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Explore Affinity Lists and Stages

## Objective

Discover Affinity list, stage, field, and object-count scope before Deal Pipeline import or sync.

## What To Do

Use the connected `affinity-mcp-server` application to enumerate Affinity lists, stages/status fields, key CRM fields, and object counts. Expected tools include affinity list opportunities, affinity get opportunity, affinity get list entries, affinity get field values, and affinity get field value changes when discovered. Ask the user to choose the list/source and active stages before any import or sync-read task.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Discovery Goal.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Deliverable

- Produce a concise, reviewable task response that a human can act on.
- Also include a short human-readable summary covering: Affinity Discovery Report, Scope Questions. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

If Affinity has no authorized connection or no discovered tools, report the setup gap and ask for connection authorization or an exported snapshot.

## Guardrails

Read-only discovery. Do not import, sync, update CRM fields, write notes, move stages, or create tasks.

## Completion Criteria

- Candidate Affinity lists/sources and stages are listed with counts when available.
- The report names the Affinity tool IDs used or missing.
- User choices needed before import are explicit.

## Human Review

- Choose the Affinity list/source scope.
- Choose which stages count as active pipeline.
- Approve any later import or recurring sync separately.
