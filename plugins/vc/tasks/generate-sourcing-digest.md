---
id: vc.generate_sourcing_digest
title: Generate Sourcing Digest
slug: generate-sourcing-digest
agent: vc-sourcing-operator
skills:
- vc-sourcing-digest-generation
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/generate-sourcing-digest.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Generate Sourcing Digest

## Objective

Generate a daily or weekly origination digest with candidates, run receipts, degraded sources, and pending approvals.

## What To Do

Produce a reference-pipeline-style digest of new Meet/Watch and active candidates, source counts, run failures, budget/cost notes, and review actions. The default destination is a reviewable digest object; posting to Slack, ClickUp, email, or another external channel requires a separately approved write-capable task.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Digest Scope.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Sourcing Digest Template](../alludium/documents/origination/sourcing-digest-template.md): Use as the starting structure for the deliverable; adapt it to the facts and avoid generic filler.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.md): Follow for process boundaries and review standards.

## Deliverable

- Create or update **Sourcing Digest Artifact** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.

## Missing Input Policy

Ask for run receipt, candidate batch, digest channel, audience, and whether this is daily, weekly, or monthly.

## Guardrails

Draft digest only unless explicit channel-post approval is granted.

## Completion Criteria

- Digest groups candidates by action, urgency, source, and owner/review need.
- Run receipt, cost/budget notes, degraded-source warnings, and pending approvals are included.
