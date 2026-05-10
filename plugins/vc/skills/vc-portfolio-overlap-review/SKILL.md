---
id: vc-portfolio-overlap-review
name: "VC Portfolio Overlap Review"
description: >
  Compare active sourcing candidates against portfolio companies and classify
  competitive overlap without automatically passing or blocking candidates.
tags:
  - vc
  - origination
  - portfolio
  - overlap
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: setup
      importance: recommended
      required: false
      owner: user
      ownerPath: Provide or authorize the current portfolio list and freshness policy.
      confirmationRequired: true
      gracefulDegradation: Produce overlap-unknown output and list missing portfolio data.
  routingHints:
    preferredSurface: skill
---

# VC Portfolio Overlap Review

Use this skill for active candidates that are likely to advance.

## Compare On

Compare the candidate to portfolio companies by:

- Target customer
- Problem solved
- Product category
- Workflow or buying center
- Differentiated technical approach
- Geography only when relevant

Sector alone is not enough for a conflict.

## Severity

Return one of:

- `none`: no meaningful overlap
- `low`: broad thematic overlap only
- `medium`: adjacent workflow, buyer, or product category
- `high`: direct customer/problem/product conflict needing partner review

## Output

Return severity, matching portfolio companies, evidence, confidence, freshness of portfolio source, and recommended review owner.

## Boundaries

- Do not auto-pass candidates.
- Do not contact portfolio companies.
- Do not write to CRM or candidate records without approval.
