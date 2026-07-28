---
id: vc.create_sourcing_line
title: Create Sourcing Line
slug: create-sourcing-line
agent: vc-sourcing-operator
skills:
- origination-pipeline-orchestration
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/create-sourcing-line.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Create Sourcing Line

## Objective

Create the minimal draft Sourcing Line and its native relationship so configuration continues in the line's canonical chat.

## What To Do

Capture only a human-readable line name and the current Origination Pipeline project ID. Emit `projectCreation.createRequest` with the required field values and `relationships: [{ direction: "incoming", relatedProjectId: origination_pipeline_project_id, relationshipTypeKey: "vc.origination_pipeline_contains_sourcing_line", metadata: { creationSource: "create-sourcing-line" } }]`. The platform finalizer must atomically create the draft Sourcing Line and relationship, then open the new project canonical chat. Do not collect the line hypothesis, source mix, screen, cadence, review policy, or outreach policy here; the dedicated line chat and `configure-sourcing-line` task own that proposal.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Line Name, Origination Pipeline Project ID.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Deliverable

- Produce a concise, reviewable task response that a human can act on.
- Also include a short human-readable summary covering: Pipeline Relationship Key, Project Creation Request. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask only for a short line name when it cannot be inferred. The current Origination Pipeline project ID is mandatory.

## Guardrails

Create only the draft project and native project relationship. Do not run sources, enable schedules, create candidates, spend money, write external systems, or send outreach.

## Completion Criteria

- Line name and parent Origination Pipeline project ID are known.
- Atomic draft creation and incoming relationship are proposed.
- Configuration is explicitly deferred to the line's canonical chat.

## Human Review

- Confirm the draft line name.
