---
id: vc.configure_origination_pipeline
title: Configure Origination Pipeline
slug: configure-origination-pipeline
agent: vc-sourcing-operator
skills:
- origination-pipeline-orchestration
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/configure-origination-pipeline.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Configure Origination Pipeline

## Objective

Capture thesis, source selection, cadence intent, budget policy, review thresholds, and integration-readiness requirements for a VC origination pipeline.

## What To Do

Guide the user through initial origination pipeline configuration. Capture the required pipeline name, thesis, source choices, cadence intent, digest destination, budget, review policy, promotion threshold, manual-review threshold, credential gaps, and child setup tasks needed for selected sources. Create setup child tasks only for selected integrations whose setup templates exist. Capture pipeline name, include source registry and review policy when captured, and include confidentiality level only when confidently captured. Do not run sourcing, score candidates, create candidate records, enable schedules, write to external systems, send outreach, create Deal Pipelines, or create the Origination Pipeline project; the platform finalizer owns deterministic project creation after task completion.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Pipeline Name, Configuration Goal, Current Pipeline Context.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Origination Pipeline Operating SOP](../alludium/documents/origination/origination-pipeline-sop.md): Follow for process boundaries and review standards.
- [Origination Source Strategy Guide](../alludium/documents/origination/origination-source-strategy-guide.md): Use as the analysis method.
- [Source Registry Template](../alludium/documents/origination/source-registry-template.md): Follow for process boundaries and review standards.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.md): Follow for process boundaries and review standards.

## Deliverable

- Produce a concise, reviewable task response that a human can act on.
- Also include a short human-readable summary covering: Configuration Summary, Source Registry, Review Policy, Child Task Plan, Project Creation Field Values. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Keep setup incomplete when thesis, enabled sources, review policy, budget policy, or required credential decisions are missing. Ask targeted task questions rather than inventing configuration.

## Guardrails

Configuration only. No external reads beyond connection-readiness checks, no scheduled runs, no imports, no external writes, no outreach, and no Deal Pipeline creation.

## Completion Criteria

- pipeline name is captured for guided project creation finalization.
- Thesis, source selection, run cadence intent, budget policy, review policy, and thresholds are captured or explicitly marked unresolved.
- Required setup child tasks for selected Apify and Companies House sources are proposed without executing source reads.
- Credential gaps and approved connection scopes are listed.
- The output distinguishes configuration intent from active automation.
- Guided project creation captures pipeline name and captured runtime project fields such as source registry and review policy.

## Human Review

- Choose enabled source systems and approved source scope.
- Confirm budget and cadence intent before any later scheduled-run work.
- Approve child setup tasks separately for each integration.
