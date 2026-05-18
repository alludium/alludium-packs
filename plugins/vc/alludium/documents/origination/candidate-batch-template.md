---
id: vc.document.candidate_batch_template
title: Candidate Batch Template
documentType: template
supportedProjectTypes:
  - vc_origination_pipeline
summary: Reusable batch review template for sourced candidates.
---

# Candidate Batch Template

## Batch Header

| Field | Content |
| --- | --- |
| Pipeline | Name and thesis |
| Batch period | Date range |
| Sources | Source keys used |
| Prepared by | Owner and date |
| Review objective | Score, enrich, promote, reject, or watch |

## Candidate Table

| Company | Domain | Source | Source URL | Thesis Tags | Initial Evidence | Dedupe Status | Relationship Context | Score | Confidence | Next Action | Owner | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  | New / existing / ambiguous / prior reject |  | Promote / review / watch / reject | High / Medium / Low | Meet / research / pass / hold |  |  |

## Batch Summary

| Metric | Count / Note |
| --- | --- |
| Candidates reviewed |  |
| Promote |  |
| Review |  |
| Watch |  |
| Reject |  |
| Ambiguous dedupe |  |

## Batch Rule

Treat a batch as a review artifact, not a source of truth. Promote durable facts into the candidate record, Deal Room, or CRM only after approval.
