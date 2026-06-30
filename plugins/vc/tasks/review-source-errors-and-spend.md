---
id: vc.review_source_errors_and_spend
title: Review Source Errors and Spend
slug: review-source-errors-and-spend
agent: vc-sourcing-operator
skills:
- vc-source-error-and-spend-audit
- vc-source-registry-and-state-management
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/review-source-errors-and-spend.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Review Source Errors and Spend

## Objective

Review degraded source runs, cost warnings, retry safety, and required human actions.

## What To Do

Review run receipts and degraded-source notes from the latest origination pass. Classify missing credentials, auth expiry, provider failure, rate limits, budget caps, exhausted queries, schema drift, no-yield sources, and blocked writes. Recommend retry, setup, query pruning, schedule pause, or human review.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Source Health Scope.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Source Health Review Checklist](../alludium/documents/origination/source-health-review-checklist.html): Use as the starting structure for the deliverable; adapt it to the facts and avoid generic filler.
- [Paid Source Spend Audit Checklist](../alludium/documents/origination/paid-source-spend-audit-checklist.html): Complete as a checklist with status, evidence, owner, and open items.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.html): Follow for process boundaries and review standards.

## Deliverable

- Create or update **Source Health Artifact** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.
- Also include a short human-readable summary covering: Source Health Status. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for recent run receipts, source state, budget policy, provider status notes, and retry policy.

## Guardrails

Review only. Do not retry paid runs, change budgets, disable schedules, or update credentials.

## Completion Criteria

- Each issue includes source, severity, impact, retry safety, owner, and next action.
- Source health status is one of healthy, degraded, needs_credentials, budget_blocked, or unknown.
- Paid retry and schedule-change approvals are explicit.
