---
id: vc.configure_sourcing_line
title: Configure Sourcing Line
slug: configure-sourcing-line
agent: vc-sourcing-line-manager
skills:
- origination-pipeline-orchestration
- vc-source-registry-and-state-management
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/configure-sourcing-line.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Configure Sourcing Line

## Objective

Turn a sourcing hypothesis into a paused, measurable Fund-specific line with approved sources, screen, cadence, review policy, and outreach boundaries.

## What To Do

Resolve fund id by exact stable-ID equality against one active record in `vc.funds`, then use only that Fund mandate. Shape one measurable sourcing experiment: registered sources, query or screen, evidence requirements, cadence, timezone, cursor/window, result limit, budget, Inbox threshold, review policy, outreach boundary, success measures, review date, and retirement condition. Do not require an Origination Pipeline hub or copy hub registry, counts, health caches, or digest configuration into the line. Leave schedules disabled until separately approved. After the user explicitly approves the complete configuration, call `project.update` for the task's exact Sourcing Line project with typed field values for line hypothesis, source keys, screen definition, cadence policy, review policy, outreach policy, success metrics, result limit, budget limit, timezone, review date, retirement condition, and inbox threshold. Do not mutate on missing inputs, rejected approval, or a failed update. Re-read the exact project with `project.getAgentContext` and complete only when every approved value is persisted; the task output alone is not project state. Use `definitionJson.documentRefs` as the durable document reference contract. Apply each reference by usage: output template sets the output skeleton, methodology supplies analysis logic, checklist must be completed with status, evidence, and owner, style guide governs citations and claim language, and operating guidance or policy constrains process and approval boundaries.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Line Name, Fund ID, Starter Template Key.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Source Registry Template](../alludium/documents/origination/source-registry-template.html): Follow for process boundaries and review standards.
- [Origination Source Strategy Guide](../alludium/documents/origination/origination-source-strategy-guide.html): Use as the analysis method.

## Deliverable

- Produce a concise, reviewable task response that a human can act on.
- Also include a short human-readable summary covering: Line Hypothesis, Registered Source Keys, Query And Screen, Cadence Policy, Review And Inbox Policy, Outreach Policy, Success Metrics, Result Limit, and other task-specific status fields. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Keep setup incomplete until an active Fund, line hypothesis, source mix, screen, cadence, budget posture, review policy, and outreach boundary are explicit.

## Guardrails

Configuration only. Do not read paid sources, enable schedules, create candidates, write external systems, or send outreach.

## Completion Criteria

- fund_id matches exactly one active vc.funds record and only its mandate is used.
- The line has one coherent, testable learning question.
- Sources, cadence, result limits, budget, review threshold, and retirement condition are explicit.
- Outreach is disabled or approval-gated.

## Human Review

- Approve the Fund-specific source mix and screen.
- Approve paid-source budget and result limits.
- Approve any later schedule enablement or outreach separately.
