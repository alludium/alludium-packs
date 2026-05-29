---
id: vc.review_portfolio_overlap
title: Review Portfolio Overlap
slug: review-portfolio-overlap
agent: vc-sourcing-operator
skills:
- vc-portfolio-overlap-review
- citation-enforcement
- vc-relationship-context-check
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/review-portfolio-overlap.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Review Portfolio Overlap

## Objective

Compare active sourcing candidates against portfolio companies and flag possible competitive overlap.

## What To Do

Mirror the reference pipeline's portfolio-overlap checker. Compare only active candidates such as Meet, IC-Summary, or Reach out against the current portfolio. Classify overlap as none, low, medium, or high using target customer, problem, and product category; sectoral overlap alone is not enough. Do not auto-pass candidates for overlap.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Portfolio Overlap Scope.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Deliverable

- Create or update **Portfolio Overlap Artifact** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.
- Also include a short human-readable summary covering: High Overlap Count, Overlap Report. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for active candidate batch, portfolio source or cache, freshness policy, and whether cached portfolio data may be reused.

## Guardrails

Review and annotate proposal only. Do not change candidate status, pass candidates, contact founders, or update external systems without separate approval.

## Completion Criteria

- Each checked candidate has severity, matching portfolio companies, reason, and receipt.
- Portfolio source freshness and cache age are named.
