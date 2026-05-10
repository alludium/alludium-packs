---
id: vc-reddit-inbox-approval
name: "VC Reddit Inbox Approval"
description: >
  Review Reddit discovery inbox rows and prepare approved candidates for the
  main origination flow without silently importing or syncing them.
tags:
  - vc
  - origination
  - reddit
  - approval
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
  routingHints:
    preferredSurface: skill
---

# VC Reddit Inbox Approval

Use this skill after Reddit discovery has produced an inbox/proposal batch.

## Approval Review

For each row, confirm:

- First-person founder or builder signal
- Company/product identity
- Website, demo, GitHub, or other durable follow-up link
- AI/B2B/startup relevance
- Geography signal or accepted exception
- Not a job post, advice request, agency pitch, rant, or pure news item

## Output

Return approved rows, rejected rows, dedupe keys, next enrichment task input, and any rows needing more human review.

## Boundaries

- Do not mark inbox rows pushed unless an approved write task is active.
- Do not import directly into the main candidate queue without approval.
- Do not comment or message Reddit users.
