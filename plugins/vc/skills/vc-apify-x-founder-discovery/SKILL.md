---
id: vc-apify-x-founder-discovery
name: "VC Apify X Founder Discovery"
description: >
  Use approved Apify X/Twitter search actors to find first-person build,
  launch, AI, and B2B founder signals with noise filtering and receipts.
tags:
  - vc
  - origination
  - apify
  - x
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: required
      required: true
      applicationExternalId: apify-actors-mcp
      note: Use only approved X/Twitter actor scope, query terms, lookback windows, and result caps.
      gracefulDegradation: Produce a query plan and ask for authorized Apify access.
  routingHints:
    preferredSurface: skill
    notes:
      - This is public-signal discovery only; engagement and outreach are separate tasks.
---

# VC Apify X Founder Discovery

Use this skill to find public founder and product-launch signals on X/Twitter through approved Apify actors.

## Positive Signals

Score candidates up for:

- First-person building, launching, beta, fundraising, customer, or hiring language
- AI, ML, LLM, agent, automation, data, infrastructure, or developer-tool terms
- B2B, enterprise, workflow, integration, compliance, security, or ROI language
- UK or Ireland profile, bio, post, website, or company signal
- Product website, waitlist, demo, or customer call-to-action
- Credible engagement from relevant builders or buyers

## Noise Rejection

Reject:

- Media, VC, newsletter, aggregator, job-board, agency, or consultant accounts
- Third-party news about a company where no founder/source identity is present
- Pure opinion posts with no product or company signal
- Crypto/spam/giveaway patterns unless the thesis explicitly allows them

## State

Track seen tweet ids, author handles, query terms, lookback windows, run ids, and rejected/noise counts.

## Output

Return tweet URL, author handle, founder or company identity, product URL, location signal, source query, score reasons, dedupe key, rejection reason, and receipt.

## Boundaries

- Do not reply, like, follow, DM, or otherwise engage.
- Do not import or sync candidates without a separate approved task.
- Do not create Deal Pipelines.
