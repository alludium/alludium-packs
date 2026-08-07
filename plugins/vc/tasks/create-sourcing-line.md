---
id: vc.create_sourcing_line
title: Create Sourcing Line
slug: create-sourcing-line
agent: vc-sourcing-line-manager
skills:
- origination-pipeline-orchestration
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/create-sourcing-line.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Create Sourcing Line

## Objective

Create a minimal Fund-specific Sourcing Line so its configuration continues in the line's canonical chat.

## What To Do

Capture a human-readable line name and require fund id to exactly match one active record in the canonical `vc.funds` collection. Emit `projectCreation.createRequest` with only those required field values. Do not require or create an Origination Pipeline hub relationship. The platform finalizer creates the draft Sourcing Line, then opens its canonical chat. Defer the hypothesis, sources, screen, cadence, review policy, and outreach policy to `configure-sourcing-line`.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Line Name, Fund ID.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Deliverable

- Produce a concise, reviewable task response that a human can act on.
- Also include a short human-readable summary covering: Project Creation Request. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for a short line name and an active configured Fund. Keep creation incomplete when fund_id is missing, unknown, or inactive.

## Guardrails

Create only the draft project. Do not run sources, enable schedules, create candidates, spend money, write external systems, or send outreach.

## Completion Criteria

- Line name is known.
- fund_id exactly matches one active vc.funds record.
- Draft project creation is proposed without a mandatory hub relationship.

## Human Review

- Confirm the line name and Fund.
