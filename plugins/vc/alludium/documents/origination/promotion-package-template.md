---
id: vc.document.promotion_package_template
title: Promotion Package Template
documentType: template
supportedProjectTypes:
  - vc_origination_pipeline
summary: Reusable package for promoting a sourced candidate to Deal Room review.
---

# Promotion Package Template

## Promotion Header

| Field | Content |
| --- | --- |
| Candidate | Company name, domain, source ID |
| Pipeline | Origination pipeline and thesis |
| Recommended action | Create Deal Room / update existing Deal Room / hold |
| Proposed Deal Room owner | Name or role |
| Approval status | Pending / approved / rejected |

## Promotion Case

| Area | Summary | Evidence |
| --- | --- | --- |
| Company snapshot | Product, customer, stage, geography |  |
| Source path | How the candidate surfaced |  |
| Thesis fit | Why it fits the fund |  |
| Screening result | Score and rationale |  |
| Novelty / dedupe | New, existing, ambiguous, prior reject |  |
| Relationship context | Warm intro, known contact, no path |  |
| Risks and unknowns | Top open issues |  |

## Downstream Setup

| Field | Recommendation |
| --- | --- |
| Suggested next task | Initial call, founder materials, investment screen, or pass note |
| Initial artifacts to attach | Candidate batch, source receipts, screen, relationship check |
| Required approval | Human approver and date |

## Approval Rule

Promotion should create or update a downstream opportunity only after a human approves the package and confirms the intended Deal Room boundary.
