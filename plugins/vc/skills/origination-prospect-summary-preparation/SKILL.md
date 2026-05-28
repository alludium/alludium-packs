---
id: origination-prospect-summary-preparation
name: "Origination Prospect Summary Preparation"
description: >
  Prepare a concise prospect-level sourcing summary for prioritized origination
  candidates without creating pages or promoting to a Deal Pipeline automatically.
tags:
  - vc
  - origination
  - prospect-summary
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
  routingHints:
    preferredSurface: skill
---

# Origination Prospect Summary Preparation

Use this skill for prioritized candidates that need a concise sourcing summary before outreach, founder follow-up, or Deal Pipeline promotion.

## Inputs

Use enriched candidate data, verdict output, relationship context, source receipts, website evidence, and open questions.

## Prospect Summary

Include:

- Company and founder identity
- What they do
- Why now
- Thesis fit
- Founder signal
- Market/customer signal
- Evidence quality
- Known relationship context
- Risks and unknowns
- Recommended next step

Scope the output to exactly one prospect/candidate. Portfolio-wide or batch-level summaries belong in sourcing digests.

## Boundaries

- Do not create Notion pages or documents without approval.
- Do not label the output as an IC memo or IC-ready recommendation.
- Do not promote into a Deal Pipeline.
- Do not overwrite candidate status.
