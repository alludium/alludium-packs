---
id: vc.enrich_sourcing_candidate
title: Enrich Sourcing Candidate
slug: enrich-sourcing-candidate
agent: vc-sourcing-operator
skills:
- vc-sourcing-candidate-enrichment
- vc-sourcing-dedupe-and-novelty-check
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/enrich-sourcing-candidate.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Enrich Sourcing Candidate

## Objective

Normalize and enrich candidate records with web, LinkedIn, founder, website, and evidence context before scoring.

## What To Do

Enrich only candidates above the configured source-specific floor. Preserve the reference pipeline separation between cheap enrichment and LLM verdict by first gathering search results, website, company LinkedIn URL, founder LinkedIn URLs, founder profile evidence, and receipts; do not make final Meet/Watch/Pass judgments in this task. For LinkedIn-sourced rows, reuse pre-verified founder/company LinkedIn URLs rather than re-searching them.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Candidate Batch.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Deliverable

- Create or update **Enrichment Artifact** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.
- Also include a short human-readable summary covering: Enriched Candidate Count, Enrichment Status, Enrichment Report. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for candidate batch, enrichment budget, approved search/extraction tools, dedupe state, and minimum source score before enriching.

## Guardrails

Read/enrich only. Do not write CRM rows, create Notion pages, score final verdicts, contact founders, or create Deal Pipelines.

## Completion Criteria

- Enriched candidates include normalized identity, source key, website, company LinkedIn, founder LinkedIn evidence, search snippets, receipts, and missing-data flags.
- Dedupe decisions include company-number, LinkedIn slug, domain, name, repo, post, or tweet keys as applicable.
- Errors and skipped rows are listed with retry guidance.
