---
id: vc-source-error-and-spend-audit
name: "VC Source Error & Spend Audit"
description: >
  Review origination source failures, degraded connectors, rate limits, missing
  credentials, cost warnings, and retry recommendations.
tags:
  - vc
  - origination
  - source-health
  - audit
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
  routingHints:
    preferredSurface: skill
---

# VC Source Error & Spend Audit

Use this skill after sourcing runs or when the pipeline is degraded.

## Review

Classify each issue:

- Missing credential
- Authorization expired
- Rate limited
- Provider unavailable
- Query exhausted
- Budget cap reached
- Extraction/schema drift
- Repeated duplicate/no-yield source
- External write blocked

## Output

Return issue, source, severity, first seen, last seen, affected tasks, candidate impact, retry safety, recommended owner, and required human approval.

## Boundaries

- Do not retry paid runs automatically.
- Do not increase budgets automatically.
- Do not enable or disable schedules without approval.
