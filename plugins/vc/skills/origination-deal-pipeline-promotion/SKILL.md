---
id: origination-deal-pipeline-promotion
name: "Origination Deal Pipeline Promotion"
description: >
  Prepare a human-reviewed promotion package that can create or update a VC Deal
  Pipeline from an approved first-class Origination Candidate.
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
      ownerPath: Confirm promotion threshold, owner, and target Deal Pipeline creation/update policy.
      confirmationRequired: true
      gracefulDegradation: Produce a promotion-readiness checklist only.
  routingHints:
    preferredSurface: skill
---

# Origination Deal Pipeline Promotion

Use this skill only after a candidate has human approval for promotion.

## Promotion Package

Include:

- Company and founder identity
- Source family and original receipts
- Enrichment summary
- Relationship context
- Verdict and active screen summary
- Portfolio overlap result
- Outreach/contact state
- Recommended Deal Pipeline fields
- Recommended initial lifecycle state
- Suggested next tasks
- Open questions and risks

## Approval Boundary

The default output is a promotion package. Creating or updating a Deal Pipeline project is a separate explicit platform action.

When a new Deal Pipeline is approved, create it atomically with an incoming `vc.origination_candidate_promoted_to_deal` relationship from the Origination Candidate. Use `project-relationship.create` only when both projects already exist. Preserve the candidate project ID in compatibility fields during rollout, but treat the native relationship as authoritative.

## Boundaries

- Do not create or update projects without approval.
- Do not sync CRM or document systems without approval.
- Do not send notifications or outreach automatically.
