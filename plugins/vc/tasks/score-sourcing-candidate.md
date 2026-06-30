---
id: vc.score_sourcing_candidate
title: Score Sourcing Candidate
slug: score-sourcing-candidate
agent: vc-sourcing-operator
skills:
- vc-sourcing-verdict-and-screening
- vc-sourcing-dedupe-and-novelty-check
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/score-sourcing-candidate.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Score Sourcing Candidate

## Objective

Produce Meet/Watch/Pass verdicts and urgency scores for enriched origination candidates.

## What To Do

Mirror the reference pipeline's verdict contract. Score from already-enriched data, separate evidence from inference, and return Meet, Watch, or Pass plus urgency. Apply hard stage safety by passing companies with Series A+ funding or more than 20 employees when reliable LinkedIn company data is present. Run the second-pass verdict only for Meet/Watch rows with fresh LinkedIn company data so paid scraping and model cost stay bounded.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Enriched Candidate Batch, Scoring Policy.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Sourcing Scoring Rubric](../alludium/documents/origination/sourcing-scoring-rubric.html): Use as the analysis method.
- [Origination Source Strategy Guide](../alludium/documents/origination/origination-source-strategy-guide.html): Use as the analysis method.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.html): Follow for process boundaries and review standards.

## Deliverable

- Create or update **Scoring Artifact** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.
- Also include a short human-readable summary covering: Meet Candidate Count, Watch Candidate Count, Promotion Ready Count, Scoring Report. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for enriched candidates, thesis, geography/stage policy, relationship context, LinkedIn company data availability, and scoring thresholds before scoring.

## Guardrails

Scoring only. Do not sync external records, change manual decisions, send outreach, or create Deal Pipelines.

## Completion Criteria

- Each scored candidate has action, urgency, thesis fit, confidence, funding status, HQ/geography concern, frontier-pedigree evidence, reasons, and receipts.
- Auto-pass decisions name the specific rule and evidence.
- Second-pass rows are limited to candidates with fresh LinkedIn company data.
