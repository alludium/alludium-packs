---
id: vc.ingest_manual_sourcing_tip
title: Ingest Manual Sourcing Tip
slug: ingest-manual-sourcing-tip
agent: vc-sourcing-operator
skills:
- vc-manual-tip-ingestion
- vc-sourcing-dedupe-and-novelty-check
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/ingest-manual-sourcing-tip.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Ingest Manual Sourcing Tip

## Objective

Normalize a manually submitted company or founder lead into the origination candidate model.

## What To Do

Mirror the reference pipeline's manual-tip ingestion by normalizing supplied company, founder, website, LinkedIn, note, and source context into the candidate schema, assigning a stable manual-tip key, setting source and discovery mode, and sending the candidate through enrichment and scoring rather than directly promoting it.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Manual Tip.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Deliverable

- Create or update **Manual Tip Ingestion Artifact** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.
- Also include a short human-readable summary covering: Normalized Candidate Key, Ingestion Report. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for company or founder identity, source of tip, website or profile URL, submitter, and confidence if missing.

## Guardrails

Internal candidate normalization only. Do not contact founders, write CRM records, or create Deal Pipelines.

## Completion Criteria

- Manual tip candidate has stable key, source, submitter/source receipt, identity fields, dedupe decision, and next-step recommendation.
