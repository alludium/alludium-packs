---
id: vc.run_deal_fit_analysis
title: Run Deal Fit Analysis
slug: run-deal-fit-analysis
agent: vc-sourcing-operator
skills:
- vc-sourcing-verdict-and-screening
- investment-screening-framework
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/run-deal-fit-analysis.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Run Deal Fit Analysis

## Objective

Score active origination candidates against the firm's deal-fit pillars before deeper screening.

## What To Do

Mirror the reference pipeline deal-fit step by scoring active candidates against the configured fit pillars before the heavier screen. Use enriched evidence, relationship context, portfolio-overlap results, and the current thesis policy. Return a fit score or band, reasoning, evidence gaps, and recommended next state.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Deal Fit Scope.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Sourcing Scoring Rubric](../alludium/documents/origination/sourcing-scoring-rubric.html): Use as the analysis method.
- [Investment Screening Framework](../alludium/documents/shared/investment-screening-framework.html): Use as the analysis method.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.html): Follow for process boundaries and review standards.

## Deliverable

- Create or update **Deal Fit Artifact** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.
- Also include a short human-readable summary covering: Deal Fit Ready Count, Deal Fit Report. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for enriched candidates, thesis policy, scoring pillars, portfolio overlap, relationship context, and approved write mode before analysis.

## Guardrails

Analysis only unless explicit write approval is granted. Do not send outreach, update protected manual decisions, or create Deal Pipeline projects.

## Completion Criteria

- Each candidate has a deal-fit score or band, cited reasoning, evidence gaps, and recommended next state.
- Portfolio overlap and relationship context are reflected when available.
