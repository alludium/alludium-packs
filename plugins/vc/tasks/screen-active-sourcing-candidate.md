---
id: vc.screen_active_sourcing_candidate
title: Screen Active Sourcing Candidate
slug: screen-active-sourcing-candidate
agent: vc-sourcing-operator
skills:
- vc-sourcing-verdict-and-screening
- citation-enforcement
- investment-screening-framework
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/screen-active-sourcing-candidate.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Screen Active Sourcing Candidate

## Objective

Run an origination-specific thesis screen on active Meet, IC-Summary, or Reach out candidates.

## What To Do

Screen active origination candidates using the reference pipeline's fast thesis filter rather than the downstream Deal Pipeline first-look task. Assess stage, geography, enterprise software, AI-native depth, named buyer, moat, and founder balance. Return PROCEED_TO_IC, DIG_FURTHER, or PASS and map those to review actions without downgrading protected manual decisions.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Screening Scope.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Sourcing Scoring Rubric](../alludium/documents/origination/sourcing-scoring-rubric.md): Use as the analysis method.
- [Origination Source Strategy Guide](../alludium/documents/origination/origination-source-strategy-guide.md): Use as the analysis method.
- [Dedupe And Novelty Policy](../alludium/documents/origination/dedupe-novelty-policy.md): Follow for process boundaries and review standards.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.md): Follow for process boundaries and review standards.

## Deliverable

- Create or update **Screening Artifact** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.
- Also include a short human-readable summary covering: Promotion Ready Count, Screening Report. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for active candidate batch, current manual actions, thesis policy, protected-action list, and approved write mode before screening.

## Guardrails

Screening recommendation only unless explicit write approval is granted. Never downgrade protected manual decisions such as IC-Summary or Pass.

## Completion Criteria

- Each screened candidate has thesis pillar statuses, key signals, verdict, verdict reason, protected-action handling, and receipts.
- Manual decision preservation is explicit.
