---
id: vc-origination-ic-summary-preparation
name: "Origination IC Summary Preparation"
description: >
  Prepare a lightweight IC-style summary for Meet or Watch origination candidates
  without creating pages or promoting to a Deal Pipeline automatically.
tags:
  - vc
  - origination
  - ic-summary
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
  routingHints:
    preferredSurface: skill
---

# Origination IC Summary Preparation

Use this skill for Meet or Watch candidates that need a concise partner-review artifact before Deal Pipeline promotion.

## Inputs

Use enriched candidate data, verdict output, relationship context, source receipts, website evidence, and open questions.

## Summary

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

## Boundaries

- Do not create Notion pages or documents without approval.
- Do not promote into a Deal Pipeline.
- Do not overwrite candidate status.
