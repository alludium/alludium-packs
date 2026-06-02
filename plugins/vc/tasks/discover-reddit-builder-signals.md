---
id: vc.discover_reddit_builder_signals
title: Discover Reddit Builder Signals
slug: discover-reddit-builder-signals
agent: vc-sourcing-operator
skills:
- vc-reddit-builder-signal-discovery
- vc-source-registry-and-state-management
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/discover-reddit-builder-signals.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Discover Reddit Builder Signals

## Objective

Discover public Reddit builder posts that may indicate early AI startup candidates.

## What To Do

Mirror the reference pipeline's Reddit approach against approved public communities and terms. Look for first-person build, launch, beta, pre-seed, early-user, AI/LLM, and B2B signals. Reject advice questions, job posts, hiring posts, rants, freelancing income posts, pure academic posts without product signal, and non-self posts. Preserve post ID as the dedupe key.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Reddit Discovery Scope.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Deliverable

- Create or update **Reddit Discovery Artifact** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.
- Also include a short human-readable summary covering: Discovery Report, Source Result Count, Source State Summary. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for approved subreddits, query terms, lookback window, minimum score, rate-limit policy, and seen post state.

## Guardrails

Public read and inbox proposal only. Do not comment, message, import into the main candidate queue, or sync externally without separate approval.

## Completion Criteria

- Candidate preview includes Reddit URL, subreddit, author, extracted company/product, website if visible, UK signal, score reasons, and source receipt.
- Source-state update includes seen post IDs and rejected/noise counts.
