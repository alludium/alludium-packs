---
id: vc-linkedin-query-spend-audit
name: "VC LinkedIn Query Spend Audit"
description: >
  Review LinkedIn Apify query yield, pages paid, cost per surfaced company,
  exhaustion state, and manual prune/review recommendations.
tags:
  - vc
  - origination
  - apify
  - spend-audit
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: setup
      importance: recommended
      required: false
      owner: user
      ownerPath: Provide run receipts, query offset state, and candidate yield state for the audit window.
      confirmationRequired: true
      gracefulDegradation: Produce a missing-data audit checklist.
  routingHints:
    preferredSurface: skill
---

# VC LinkedIn Query Spend Audit

Use this skill to reduce Apify spend by reviewing LinkedIn query yield.

## Audit Metrics

For each query or track, report:

- Track and query text
- Pages or result batches paid for
- Profiles/results paid for
- Estimated or known spend
- Companies surfaced
- Cost per company
- Last run date
- Seen-rate or duplicate-rate signals
- Exhaustion lock state
- Recommendation: `KEEP`, `REVIEW`, or `PRUNE`

## Recommendation Rules

Suggest `PRUNE` for high spend with no surfaced companies, repeated exhaustion, or very high cost per company.

Suggest `REVIEW` for mediocre yield, stale queries, or ambiguous geography/product fit.

Suggest `KEEP` for low cost and consistent qualified yield.

## Boundaries

- Read-only audit.
- Do not edit query lists or actor inputs.
- Do not change budgets or schedules automatically.
