---
id: vc.configure_sourcing_line
title: Configure Sourcing Line
slug: configure-sourcing-line
agent: vc-sourcing-operator
skills:
- origination-pipeline-orchestration
- vc-source-registry-and-state-management
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/configure-sourcing-line.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Configure Sourcing Line

## Objective

Turn a sourcing hypothesis into a paused, measurable sourcing-line project with approved sources, screen, cadence, review policy, and outreach boundaries.

## What To Do

Use the dedicated Sourcing Line chat to shape one sourcing experiment. A sourcing line is registered source(s) x query or screen x cadence x review policy x outreach policy, not a provider connection. Start from an optional starter configuration, then capture the hypothesis, source keys, connection assumptions, exclusions, evidence requirements, cadence, timezone, cursor/window, result limit, budget, Inbox threshold, review owner, outreach mode, success metrics, review date, and retirement condition. Verify the native `vc.origination_pipeline_contains_sourcing_line` relationship or propose `project-relationship.create` when the hub and line already exist but are not linked. Update the draft line configuration only after human approval and leave schedules disabled. Use `definitionJson.documentRefs` as the durable document reference contract.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Line Name, Origination Pipeline Project ID, Starter Template Key, Configuration Goal.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Sourcing Line Template Catalog](../alludium/documents/origination/sourcing-line-template-catalog.md): Use as the analysis method.
- [Source Registry Template](../alludium/documents/origination/source-registry-template.md): Follow for process boundaries and review standards.
- [Origination Pipeline Operating SOP](../alludium/documents/origination/origination-pipeline-sop.md): Follow for process boundaries and review standards.

## Deliverable

- Produce a concise, reviewable task response that a human can act on.
- Also include a short human-readable summary covering: Line Definition, Pipeline Relationship Key, Line Hypothesis, Registered Source Keys, Query And Screen, Cadence Policy, Review And Inbox Policy, Outreach Policy, and other task-specific status fields. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Keep setup incomplete until the line hypothesis, parent pipeline project ID, source mix, screen, cadence, budget posture, review policy, and outreach boundary are explicit.

## Guardrails

Configuration only. Do not read paid sources, enable schedules, create candidates, write external systems, or send outreach.

## Completion Criteria

- The line has one coherent, testable learning question.
- Source keys refer to the parent pipeline source registry and do not embed credentials.
- Cadence, result limits, budget, review threshold, and retirement condition are explicit.
- Outreach is disabled or approval-gated and never represented as an automatic send.
- Approved configuration fields are ready to persist before the draft line moves to paused.

## Human Review

- Approve the source mix and query or screen.
- Approve paid-source budget and result limits.
- Approve any later schedule enablement or outreach experiment separately.
