---
id: vc.audit_linkedin_query_spend
title: Audit LinkedIn Query Spend
slug: audit-linkedin-query-spend
agent: vc-sourcing-operator
skills:
- vc-linkedin-query-spend-audit
- vc-source-registry-and-state-management
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/audit-linkedin-query-spend.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Audit LinkedIn Query Spend

## Objective

Produce a read-only Apify LinkedIn query yield and cost audit with manual KEEP/REVIEW/PRUNE recommendations.

## What To Do

Mirror the reference pipeline's read-only LinkedIn query audit. Compare query/track run depth, pages or result batches paid, candidate yield, duplicate or seen rate, exhaustion state, estimated cost, and cost per surfaced company. Recommend KEEP, REVIEW, or PRUNE for manual query-list maintenance.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Spend Audit Scope.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Paid Source Spend Audit Checklist](../alludium/documents/origination/paid-source-spend-audit-checklist.html): Use as the starting structure for the deliverable; adapt it to the facts and avoid generic filler.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.html): Follow for process boundaries and review standards.

## Deliverable

- Create or update **LinkedIn Spend Audit Artifact** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.
- Also include a short human-readable summary covering: Paid Source Spend Status. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for Apify run receipts, query offset state, candidate yield state, and cost assumptions.

## Guardrails

Read-only audit. Do not edit query lists, actor inputs, budgets, or schedules.

## Completion Criteria

- Audit table includes query, track, spend/yield metrics, exhaustion notes, recommendation, and confidence.
- Paid source spend status is one of within_budget, near_limit, over_limit, or unknown.
- Prune/review recommendations are clearly manual follow-ups.
