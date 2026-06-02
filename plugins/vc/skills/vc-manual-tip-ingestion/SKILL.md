---
id: vc-manual-tip-ingestion
name: "VC Manual Tip Ingestion"
description: >
  Normalize manually submitted founder or company leads into the origination
  candidate model with stable keys, dedupe checks, and enrichment handoff.
tags:
  - vc
  - origination
  - manual-tip
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
  routingHints:
    preferredSurface: skill
---

# VC Manual Tip Ingestion

Use this skill when a user supplies a candidate manually.

## Required Fields

Capture what is available:

- Company name
- Founder name
- Website or domain
- LinkedIn company or founder URL
- Source of tip and submitter
- Note or reason for interest
- Date received
- Confidence or uncertainty

## Normalization

Create a stable manual-tip key from the strongest identity fields. Then run dedupe before enrichment.

Do not promote directly from a manual tip. The lead should flow through enrichment, relationship check, scoring, and human review.

## Output

Return normalized candidate, stable key, source receipt, dedupe decision, missing fields, and recommended next task.

## Boundaries

- Do not contact founders.
- Do not create Deal Pipelines.
- Do not write CRM records without approval.
