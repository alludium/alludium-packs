---
id: vc.check_affinity_relationship_context
title: Check Affinity Relationship Context
slug: check-affinity-relationship-context
agent: vc-sourcing-operator
skills:
- vc-relationship-context-check
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/check-affinity-relationship-context.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Check Affinity Relationship Context

## Objective

Check whether sourcing candidates are already known in Affinity and capture relationship context without changing CRM records.

## What To Do

Mirror the reference pipeline's Affinity check by preferring exact domain match from enrichment or LinkedIn company data, then name fallback; treat a name-only match with no lists, notes, interactions, or owners as not found. Return lists, notes count, interaction flags, owner flags, deep link, and whether the company is known to the firm.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Relationship Check Scope.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Deliverable

- Create or update **Relationship Context Artifact** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.
- Also include a short human-readable summary covering: Known Candidate Count, Relationship Report. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for candidate batch, Affinity availability, approved lookup scope, and whether cached relationship state may be reused.

## Guardrails

Read-only relationship check. Do not create organizations, list entries, notes, field values, tasks, or outreach.

## Completion Criteria

- Each checked candidate has found/not-found, matched-by, known-in-CRM, list names, note counts, interaction flags, owner flags, and source receipt where available.
- False-positive name-only matches are explicitly rejected.
