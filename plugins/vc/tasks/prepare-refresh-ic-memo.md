---
id: vc.prepare_refresh_ic_memo
title: Prepare or Refresh IC Memo
slug: prepare-refresh-ic-memo
agent: vc-deal-analyst
skills:
- generate-or-refresh-living-report
- ic-memo-assembly
- ic-risk-checklist-and-decision-log
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/prepare-refresh-ic-memo.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Prepare or Refresh IC Memo

## Objective

Prepare or refresh the deliberative IC Memo for one Deal at any active stage without recording the human decision.

## What To Do

Apply `generate-or-refresh-living-report` to discover the current project-linked evidence corpus, include the mapped Evaluation Report, prior Decision Records, Term Sheet Review and any additive focus artifacts, compare the prior evidence basis when refreshing, and preserve the report lifecycle. Use `definitionJson.documentRefs` as the durable criteria, template, style, and operating-guidance contract. Prepare a decision-ready IC Memo that states the decision ask, recommendation, core thesis, evidence, risks, sensitivities, dissent, unresolved questions, and changes since the prior IC round. Render from the IC Memo Template and return the resulting artifact ID as ic memo artifact. The memo is deliberative and must not state or persist the human outcome.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Company Name, Confirmed Fund ID, Focus Artifact IDs, Evaluation Report, Prior Decision Record IDs, Term Sheet Review, Existing IC Memo.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Deal Pipeline IC Criteria and Guidance](../alludium/documents/deal-pipeline/ic-criteria.html): Use as the analysis method.
- [Deal Pipeline IC Memo Template](../alludium/documents/deal-pipeline/ic-memo-template.html): Use as the starting structure for the deliverable; adapt it to the facts and avoid generic filler.
- [Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.html): Follow for citations, claim language, assumptions, and evidence quality.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.html): Follow for process boundaries and review standards.

## Deliverable

- Create or update **IC Memo** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.

## Missing Input Policy

Ask for a readable Evaluation Report when no equivalent evaluation evidence is available; otherwise mark gaps explicitly.

## Guardrails

Do not record a Decision Record, send messages, mutate CRM, create tasks or projects, or move stage.

## Completion Criteria

- The memo is a cited deliberative synthesis with an explicit ask and recommendation.
- It does not represent the recommendation as the committee decision.
- The shared living-report lifecycle and evidence-basis manifest contract is satisfied.
- The resulting ID is saved to ic memo artifact.

## Human Review

- The committee confirms any decision separately; the Deal Manager records a new Decision Record only after explicit confirmation.
