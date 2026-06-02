---
id: vc.document.dedupe_novelty_policy
title: Dedupe And Novelty Policy
documentType: policy
supportedProjectTypes:
  - vc_origination_pipeline
summary: Policy for candidate dedupe, novelty, and promotion eligibility.
---

# Dedupe And Novelty Policy

## Match Signals

| Signal | Match Strength | Notes |
| --- | --- | --- |
| Company domain | Strong | Normalize redirects and alternate domains |
| Legal name and aliases | Strong / medium | Watch for subsidiaries and stealth names |
| Founder names | Medium | Useful when company identity is thin |
| CRM record URLs | Strong | Prefer durable CRM IDs where available |
| Source object IDs | Strong within one source | Do not assume cross-source uniqueness |
| Existing Deal Pipeline fields | Strong | Check current and archived opportunities |
| Prior rejected or watched candidates | Medium / strong | Requires partner review before override |
| Relationship context | Medium | Relationship alone does not prove same company |

## Outcomes

| Outcome | Meaning | Allowed Action |
| --- | --- | --- |
| New | No meaningful match found | Continue screening or promotion package |
| Existing opportunity | Candidate maps to current Deal Pipeline | Attach evidence to existing opportunity recommendation |
| Existing pipeline candidate | Candidate already exists upstream | Update candidate batch or source registry |
| Prior reject or watch | Candidate was previously rejected or watched | Require partner review before promotion |
| Ambiguous | Competing matches remain plausible | Hold promotion and list matches |

## Standard

Novelty is a decision input, not a guarantee. When uncertain, mark ambiguous and include the competing matches.
