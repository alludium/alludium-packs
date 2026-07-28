---
id: vc.document.candidate_batch_template
title: Candidate Batch Template
documentType: template
supportedProjectTypes:
  - vc_sourcing_line
  - vc_origination_candidate
summary: Reusable batch review template for sourced candidates.
---

# Candidate Batch Template

## Batch Header

| Field | Content |
| --- | --- |
| Origination Pipeline | Parent project ID and name |
| Sourcing Line | Project ID, name, hypothesis, and screen version |
| Batch period | Date range |
| Sources | Registered source keys and run receipt IDs |
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

Treat a batch as a review artifact, not a source of truth. Promote durable facts into the candidate record, Deal Pipeline, or CRM only after approval.
