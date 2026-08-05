---
id: vc.review_outreach_outcome
title: Review Outreach Outcome
slug: review-outreach-outcome
agent: vc-sourcing-operator
skills:
- origination-deal-pipeline-promotion
- vc-outreach-draft-queue
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/review-outreach-outcome.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Review Outreach Outcome

## Objective

Classify outbound outcomes after LinkedIn and email attempts into no response, engaged, pass, or watchlist.

## What To Do

Review the latest outreach state, response evidence, CRM/list context, and candidate screening artifacts. Recommend one outcome: no response, engaged and ready to add to the Deal Pipeline, pass, or watchlist. If engaged, prepare the promotion handoff context but do not create a Deal Pipeline or mutate CRM/list stages without explicit human approval.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Outreach State.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Promotion Package Template](../alludium/documents/origination/promotion-package-template.html): Use as the starting structure for the deliverable; adapt it to the facts and avoid generic filler.
- [Origination Source Strategy Guide](../alludium/documents/origination/origination-source-strategy-guide.html): Use as the analysis method.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.html): Follow for process boundaries and review standards.

## Deliverable

- Create or update **Outreach Outcome Artifact** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.
- Also include a short human-readable summary covering: Recommended Terminal State. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for outreach history, response evidence, latest screening artifact, owner decision policy, and target system before classifying.

## Guardrails

Review and recommendation only. Deal Pipeline creation, CRM stage changes, pass/watchlist updates, and notifications require explicit human approval.

## Completion Criteria

- Outcome recommendation is one of no_response, engaged_added_to_deal_funnel, pass, or watchlist.
- Recommendation cites outreach evidence, response state, and screening rationale.
- Engaged outcomes include promotion readiness and unresolved blockers.
