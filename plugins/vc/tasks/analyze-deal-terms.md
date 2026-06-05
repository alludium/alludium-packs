---
id: vc.analyze_deal_terms
title: Analyze Deal Terms
slug: analyze-deal-terms
agent: vc-legal-compliance-desk
skills:
- deal-terms-analysis
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/analyze-deal-terms.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Analyze Deal Terms

## Objective

Analyze proposed venture deal economics, ownership, dilution, ESOP, and commercial open terms without providing legal advice or approving terms.

## What To Do

Analyze the proposed investment amount, valuation, round size, cap table, ownership target, ESOP, co-investors, and reserve policy as commercial deal economics. Model ownership, dilution, valuation sensitivity, and open commercial terms only from supplied evidence. Cite material claims, separate assumptions from evidence, and do not provide legal advice, negotiate terms, approve terms, send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Create or update a polished Word-ready document named Deal Terms Analysis.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Proposed Investment Amount, Valuation, Round Size, Cap Table, ESOP, Co-investors, Ownership Target, Follow-on Reserve Policy, Deal Terms Snapshot, Financial Forecast.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Deal Terms Analysis Template](../alludium/documents/deal-room/deal-terms-analysis-template.md): Use as the starting structure for the deliverable; adapt it to the facts and avoid generic filler.
- [Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.md): Follow for citations, claim language, assumptions, and evidence quality.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.md): Follow for process boundaries and review standards.

## Deliverable

- Create or update **Deal Terms Analysis** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.
- Also include a short human-readable summary covering: Open Commercial Terms. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for missing required economics inputs before producing ownership, valuation, or reserve conclusions.

## Guardrails

Draft only unless a human explicitly approves the send, CRM write, Drive change, project creation, child task creation, or stage transition.

## Completion Criteria

- Required input gaps are resolved or listed as assumptions/open questions.
- Material economics conclusions include source links or are labeled as human judgment calls.
- Open terms and IC questions identify owner, dependency, and required human approval point.

## Human Review

- Approve valuation, ownership, ESOP, reserve, term-sheet, and investment-stage recommendations.
- Approve external communications, CRM writes, Drive/project creation, legal/counsel actions, and founder-facing requests.
