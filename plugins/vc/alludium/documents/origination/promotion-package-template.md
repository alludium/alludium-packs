---
id: vc.document.promotion_package_template
title: Promotion Package Template
documentType: template
supportedProjectTypes:
  - vc_origination_pipeline
summary: Reusable package for promoting a sourced candidate to Deal Pipeline review.
---

# Promotion Package Template

## Promotion Header

| Field | Content |
| --- | --- |
| Candidate | Company name, domain, source ID |
| Pipeline | Origination pipeline and thesis |
| Recommended action | Create Deal Pipeline / update existing Deal Pipeline / hold |
| Proposed Deal Pipeline owner | Name or role |
| Approval status | Pending / approved / rejected |

## Promotion Case

| Area | Summary | Evidence |
| --- | --- | --- |
| Company snapshot | Product, customer, stage, geography |  |
| Source path | How the candidate surfaced |  |
| Source quality | Source family, freshness, owner, relationship path, and evidence quality |  |
| Thesis fit | Why it fits the fund |  |
| Screening result | Score and rationale |  |
| Novelty / dedupe | New, existing, ambiguous, prior reject |  |
| Relationship context | Warm intro, known contact, no path |  |
| Risks and unknowns | Top open issues |  |
| Suggested Deal Pipeline posture | Intake, screening, evaluation, watch, or pass recommendation |  |

## Downstream Setup

| Field | Recommendation |
| --- | --- |
| Suggested next task | Initial call, founder materials, investment screen, or pass note |
| Initial artifacts to attach | Candidate batch, source receipts, screen, relationship check |
| Required approval | Human approver and date |

## Approval Rule

Promotion should create or update a downstream opportunity only after a human approves the package and confirms the intended Deal Pipeline boundary.
