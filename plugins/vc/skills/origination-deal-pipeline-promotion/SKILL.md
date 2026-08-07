---
id: origination-deal-pipeline-promotion
name: "Origination Deal Pipeline Promotion"
description: >
  Prepare a human-reviewed, explicitly Fund-routed promotion package that can
  create a VC Deal from an approved origination candidate while preserving
  multi-line provenance.
tags:
  - vc
  - origination
  - deal-room
  - promotion
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: setup
      importance: recommended
      required: false
      owner: user
      ownerPath: Confirm promotion threshold, owner, exact active target Fund, and Deal creation policy.
      confirmationRequired: true
      gracefulDegradation: Produce a promotion-readiness checklist only.
  routingHints:
    preferredSurface: skill
---

# Origination Deal Pipeline Promotion

Use this skill only after a candidate has human approval for promotion.

## Fund Selection

- Resolve the user-selected `fund_id` by exact stable-ID equality against one active record in canonical `vc.funds`.
- Treat Fund selection as a separate human decision at promotion. Never inherit it from the primary, latest, or majority Sourcing Line, even when every contributing line currently uses the same Fund.
- If the selected Fund is missing, unknown, or inactive, stop at a promotion-readiness checklist and ask the user to choose an active Fund.
- Carry the exact confirmed `fund_id` into the reviewed Deal creation package. Never blend Fund mandates.

## Promotion Package

Include:

- Company and founder identity
- Every contributing Sourcing Line, source family, stable source key, and original receipt
- Enrichment summary
- Relationship context
- Verdict and active screen summary
- Portfolio overlap result
- Outreach/contact state
- Recommended Deal Pipeline fields
- Explicitly selected target `fund_id`
- Recommended initial lifecycle state
- Suggested next tasks
- Open questions and risks

## Approval Boundary

The default output is a promotion package. Creating a Deal is a separate explicit platform action. Promotion must retain the Candidate project, its source receipts, and every line relationship for auditability.

## Boundaries

- Do not create or update projects without approval.
- Do not sync CRM or document systems without approval.
- Do not send notifications or outreach automatically.
