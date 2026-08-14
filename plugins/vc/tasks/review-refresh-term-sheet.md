---
id: vc.review_refresh_term_sheet
title: Review or Refresh Term Sheet
slug: review-refresh-term-sheet
agent: vc-deal-analyst
skills:
- generate-or-refresh-living-report
- deal-terms-analysis
- term-sheet-negotiation-brief
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/review-refresh-term-sheet.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Review or Refresh Term Sheet

## Objective

Review or refresh the living Term Sheet Review for one Deal at any active stage, comparing the prior source when available.

## What To Do

Apply `generate-or-refresh-living-report` to discover the current project-linked evidence corpus, include the mapped current and previous term sheets, Evaluation Report, IC Memo and any additive focus artifacts, compare the prior evidence basis when refreshing, and preserve the report lifecycle. Use `definitionJson.documentRefs` as the durable policy, template, style, and operating-guidance contract. Review the current term sheet against the Term Sheet Review Policy. Cover economics, liquidation, dilution, governance and control, founder obligations, exit rights, conditions, and process. When previous term sheet artifact is supplied, compare it directly with the current source and explain every material change. State implications for the Evaluation Report, IC Memo, conditions, and reapproval. Identify counsel questions, do not present legal advice, render from the Term Sheet Review Template, and return the resulting artifact ID as term sheet review artifact.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Company Name, Current Term Sheet, Previous Term Sheet, Evaluation Report, IC Memo, Focus Artifact IDs, Existing Term Sheet Review.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Deal Pipeline Term Sheet Review Policy](../alludium/documents/deal-pipeline/term-sheet-review-policy.html): Follow for process boundaries and review standards.
- [Deal Pipeline Term Sheet Review Template](../alludium/documents/deal-pipeline/term-sheet-review-template.html): Use as the starting structure for the deliverable; adapt it to the facts and avoid generic filler.
- [Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.html): Follow for citations, claim language, assumptions, and evidence quality.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.html): Follow for process boundaries and review standards.

## Deliverable

- Create or update **Term Sheet Review** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.

## Missing Input Policy

Require a readable current term sheet; treat a missing prior version as no comparison baseline, not as no change.

## Guardrails

Do not negotiate, send messages, make legal conclusions, record a decision, create tasks or projects, or move stage.

## Completion Criteria

- The current source is cited and the prior source is compared when supplied.
- Material deviations, red lines, implications, and counsel questions are explicit.
- The shared living-report lifecycle and evidence-basis manifest contract is satisfied.
- The resulting ID is saved to term sheet review artifact.

## Human Review

- Approve negotiation posture, legal instructions, reapproval, and any investment decision separately.
