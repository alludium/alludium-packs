---
id: vc-reddit-builder-signal-discovery
name: "VC Reddit Builder Signal Discovery"
description: >
  Discover public Reddit builder posts that may indicate early AI startup
  candidates, keeping them in an approval inbox until reviewed.
tags:
  - vc
  - origination
  - reddit
  - discovery
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: recommended
      required: false
      note: Use public Reddit JSON, web search, or supplied post exports within approved communities and terms.
      gracefulDegradation: Produce subreddit/query plan and ask for source access or supplied exports.
  routingHints:
    preferredSurface: skill
    notes:
      - Reddit rows stay in an inbox/proposal state until a human approves promotion into the main candidate queue.
---

# VC Reddit Builder Signal Discovery

Use this skill for public Reddit sourcing, especially early product launches and builder updates.

## Positive Signals

Prefer first-person posts that include:

- Building, launched, beta, waitlist, users, customers, revenue, pre-seed, or fundraising language
- AI, LLM, agent, automation, data, SaaS, workflow, developer-tool, or B2B language
- Website, demo, waitlist, GitHub, founder profile, or product name
- UK or Ireland signal when visible

## Rejections

Reject:

- Advice requests with no company/product
- Job, hiring, freelance, rant, or course-promotion posts
- News or third-party commentary
- Pure academic/research posts without commercialization signal
- Posts where author/company identity cannot be carried forward

## State

Track subreddit, query, post id, author, score/comments, lookback window, seen ids, rejected/noise counts, and inbox approval state.

## Output

Return Reddit URL, subreddit, author, extracted company/product, website if visible, geography signal, score reasons, rejection reason, dedupe key, and receipt.

## Boundaries

- Do not comment or message users.
- Do not deanonymize users beyond public post/profile evidence.
- Do not import into the main candidate queue without human approval.
