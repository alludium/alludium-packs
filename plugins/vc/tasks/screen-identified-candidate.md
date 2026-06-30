---
id: vc.screen_identified_candidate
title: Screen Identified Candidate
slug: screen-identified-candidate
agent: vc-sourcing-operator
skills:
- vc-sourcing-verdict-and-screening
- vc-sourcing-dedupe-and-novelty-check
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/screen-identified-candidate.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Screen Identified Candidate

## Objective

Run a lightweight first-pass fit screen on newly identified origination candidates before marking them of interest.

## What To Do

Screen newly identified candidates with the lightest useful evidence set: source receipt, normalized identity, stage/geography fit, obvious hard exclusions, basic AI/native software signal, founder signal, and duplicate/known-relationship status. This is not the full active-candidate screen; recommend only prioritize for outreach, watchlist, or pass, and list what must be enriched before outreach.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Identified Candidate Batch, First-Pass Screen Policy.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Sourcing Scoring Rubric](../alludium/documents/origination/sourcing-scoring-rubric.html): Use as the analysis method.
- [Origination Source Strategy Guide](../alludium/documents/origination/origination-source-strategy-guide.html): Use as the analysis method.
- [Dedupe And Novelty Policy](../alludium/documents/origination/dedupe-novelty-policy.html): Follow for process boundaries and review standards.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.html): Follow for process boundaries and review standards.

## Deliverable

- Create or update **Identified Screen Artifact** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.
- Also include a short human-readable summary covering: Outreach Ready Count, Watchlist Count, Pass Count, Identified Screen Report. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for the identified candidate batch, source receipts, thesis policy, hard exclusions, and dedupe state before screening.

## Guardrails

Screening recommendation only. Do not contact founders, write CRM/list records, send outreach, or create Deal Pipeline projects.

## Completion Criteria

- Every pass or watchlist recommendation names the evidence gap or exclusion rule.
- Outreach-ready recommendations include the next enrichment or outreach-prep evidence needed.
