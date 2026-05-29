---
id: vc.review_reddit_candidate_inbox
title: Review Reddit Candidate Inbox
slug: review-reddit-candidate-inbox
agent: vc-sourcing-operator
skills:
- vc-reddit-inbox-approval
- vc-sourcing-dedupe-and-novelty-check
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/review-reddit-candidate-inbox.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Review Reddit Candidate Inbox

## Objective

Review Reddit discovery inbox rows and prepare approved candidates for enrichment.

## What To Do

Review public Reddit candidate inbox rows before they enter the main candidate flow. Approve only rows with first-person builder/founder evidence, durable company or product identity, and thesis-relevant signal. Prepare approved rows for enrichment; keep uncertain rows in review and reject noise with reasons.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Reddit Inbox Scope.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Deliverable

- Create or update **Reddit Inbox Review Artifact** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.
- Also include a short human-readable summary covering: Approved Candidate Count, Needs Review Count, Review Report. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for Reddit inbox rows, raw source receipts, approval policy, and dedupe state.

## Guardrails

Approval proposal only unless explicit write approval is granted. Do not mark rows pushed, comment, message users, or sync externally.

## Completion Criteria

- Approved, rejected, and needs-review rows are separated with reasons and receipts.
- Approved rows include dedupe keys and enrichment-ready fields.
