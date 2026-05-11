---
id: vc-sourcing-dedupe-and-novelty-check
name: "VC Sourcing Dedupe & Novelty Check"
description: >
  Determine whether sourced candidates are new, duplicate, known, or quarantined
  using source-specific keys, domains, company numbers, and CRM/context evidence.
tags:
  - vc
  - origination
  - dedupe
  - novelty
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: setup
      importance: recommended
      required: false
      owner: user
      ownerPath: Confirm the candidate registry or supplied prior-run state used for dedupe.
      confirmationRequired: true
      gracefulDegradation: Mark rows as `dedupe_unknown` and list keys that must be checked.
  routingHints:
    preferredSurface: skill
---

# VC Sourcing Dedupe & Novelty Check

Use this skill wherever candidate state might fork or duplicate.

## Key Priority

Use the strongest available key first:

- Companies House company number
- Company domain
- Company LinkedIn slug
- Founder LinkedIn profile id plus company slug
- GitHub repository id or full name
- X/Twitter tweet id plus author handle
- Reddit post id
- Manual-tip stable key
- Normalized company name plus geography only as a weak fallback

## Decisions

Return one of:

- `new`: no prior candidate or CRM signal found
- `duplicate`: same stable source or identity key exists
- `known_in_crm`: relationship system has credible evidence
- `weak_name_match`: possible but not enough evidence
- `quarantine`: no stable key or identity conflict
- `reject`: disqualified by source-specific rule

## False Positive Handling

Name-only matches are weak. If no list, note, interaction, owner, domain, LinkedIn URL, or source key supports the match, treat it as not found or weak rather than known.

## Boundaries

- Do not delete or merge records.
- Do not overwrite manual actions.
- Do not promote weak matches without human review.
