---
id: vc.discover_x_founder_signals
title: Discover X Founder Signals
slug: discover-x-founder-signals
agent: vc-sourcing-operator
skills:
- vc-apify-x-founder-discovery
- vc-source-registry-and-state-management
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/discover-x-founder-signals.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Discover X Founder Signals

## Objective

Find public founder/product/building signals on X through approved Apify tweet-search actors.

## What To Do

Use approved X/Twitter actor scope only. Mirror the reference pipeline's target pattern for build-in-public, first-person launch/building language, AI/LLM/product terms, UK/Ireland location signals, B2B/enterprise hints, product URLs, engagement, and founder-author evidence. Reject media, VC, newsletter, aggregator, and third-party news accounts.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: X Discovery Scope.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Deliverable

- Create or update **X Founder Discovery Artifact** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.
- Also include a short human-readable summary covering: Discovery Report, Source Result Count, Source State Summary. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for approved search terms, lookback window, budget/result cap, actor authorization, and seen-tweet state before discovery.

## Guardrails

Public-signal read and candidate proposal only. Do not engage authors, import candidates, sync to external systems, or create Deal Pipelines.

## Completion Criteria

- Candidate preview includes tweet URL, author handle, founder/company identity, product URL, location signal, score reasons, and source receipt.
- Source-state update includes seen tweet IDs and rejected/noise counts.
- Cost/run metadata or missing cost metadata is explicit.
