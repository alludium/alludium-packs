---
id: vc-apify-linkedin-founder-discovery
name: "VC Apify LinkedIn Founder Discovery"
description: >
  Use approved Apify LinkedIn people-search actors to discover early AI founder
  candidates with reference-pipeline track, budget, pagination, and dedupe discipline.
tags:
  - vc
  - origination
  - apify
  - linkedin
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: required
      required: true
      applicationExternalId: apify-actors-mcp
      note: Use only workspace-approved Apify LinkedIn actor scopes and result limits.
      gracefulDegradation: Produce query and actor-run plan without executing Apify.
  routingHints:
    preferredSurface: skill
    notes:
      - LinkedIn people discovery is weekly by default because it is the expensive source.
---

# VC Apify LinkedIn Founder Discovery

Use this skill for LinkedIn people discovery through Apify, not for general LinkedIn research.

## Track Model

Mirror these four tracks:

- Track A: active AI founders
- Track B: pedigree founders from strong technical, research, or company backgrounds
- Track C: exited, repeat, or serial founders
- Track D: academic spinouts and research-commercialization founders

## Query Handling

For each track, keep:

- Query text and actor input
- Offset or pagination cursor
- Run id, dataset id, and cost metadata when available
- Seen profile ids
- Seen company LinkedIn slugs
- Exhaustion lock with expiry when a query is depleted
- Quarantine rows when no stable company key exists

Use an explicit forced-run override before running outside the weekly cadence.

## Candidate Filter

Prefer candidates with:

- Founder, co-founder, CEO, CTO, or product-builder role evidence
- UK or Ireland location signal
- AI, ML, LLM, agent, data, robotics, or deep-tech signal
- Company identity stable enough for dedupe
- Product or company page evidence

Reject or quarantine:

- No stable person or company identifier
- Recruiters, investors, media, agencies, consultants, or corporate roles
- Vague AI interest with no company/product signal
- Geography mismatch unless the thesis explicitly allows it

## Output

Return candidate rows with track, query, founder URL, company name, company URL or stable key, role evidence, location evidence, score reasons, rejection/quarantine reason, and receipt.

## Boundaries

- Do not bypass platform or provider policy.
- Do not run unapproved actors.
- Do not contact founders.
- Do not write CRM rows or create Deal Pipelines.
