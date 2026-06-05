---
id: vc.capture_investment_management_handoff
title: Capture Investment Management Handoff
slug: capture-investment-management-handoff
agent: vc-legal-compliance-desk
skills:
- citation-enforcement
- vc-task-and-next-step-generation
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/capture-investment-management-handoff.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Capture Investment Management Handoff

## Objective

Capture the reviewed deal-structuring handoff needed to create an Investment Management project for formal diligence, contracts, and closing.

## What To Do

Capture the reviewed handoff from Deal Pipeline deal structuring into Investment Management. Confirm company identity, lead owner, IC or partner-review decision context, current term-sheet status, diligence source materials, legal/finance workstream readiness, and missing evidence. Cite material claims, separate assumptions from evidence, and do not create projects, send messages, mutate CRM records, move stages, or start legal/finance work without explicit human approval. When this task is used as a guided project creation task, complete with structured output company name and include any confidently collected declared creation fields. Do not create the project; the platform finalizer owns deterministic project creation after task completion.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Company Name, Lead Partner, Handoff Source Artifact IDs, IC Decision Record, Term Sheet Review.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.md): Follow for citations, claim language, assumptions, and evidence quality.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.md): Follow for process boundaries and review standards.

## Deliverable

- Produce a concise, reviewable task response that a human can act on.
- Also include a short human-readable summary covering: Project Creation Payload, Handoff Summary, Missing Information. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for company name and at least one reviewed handoff source such as an IC decision, term-sheet review, deal-terms artifact, partner review, or counsel note.

## Guardrails

Draft only unless a human explicitly approves project creation, external communications, CRM writes, Drive changes, legal/counsel actions, capital calls, or stage transitions.

## Completion Criteria

- Required identity and handoff evidence are captured or listed as explicit gaps.
- Formal diligence, contracts, and closing readiness are separated from assumptions.
- Next actions identify owner, dependency, and required human approval point.
- Guided project creation captures company name.

## Human Review

- Approve creation of the Investment Management project.
- Approve legal, finance, counsel, CRM, Drive, task creation, stage movement, and external communication actions separately.
