---
id: vc-sourcing-candidate-enrichment
name: "VC Sourcing Candidate Enrichment"
description: >
  Normalize and enrich origination candidates with low-cost public evidence,
  website context, founder/company profiles, and receipts before verdict scoring.
tags:
  - vc
  - origination
  - enrichment
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: recommended
      required: false
      note: Use available web search, Firecrawl, Apify search actors, CRM, or supplied exports according to the approved source registry.
      gracefulDegradation: Normalize supplied candidate rows and list enrichment gaps.
  routingHints:
    preferredSurface: skill
    notes:
      - Enrichment is separate from final Meet/Watch/Pass verdicting.
---

# VC Sourcing Candidate Enrichment

Use this skill after discovery and before scoring.

## Enrichment Order

1. Normalize identity: company name, website/domain, company number, LinkedIn company URL, founder names, founder LinkedIn URLs.
2. Reuse trusted URLs from the source row before searching again.
3. Search for official website, founder profile, company LinkedIn page, GitHub/product docs, and relevant press.
4. Extract first-party website evidence when available.
5. Attach receipts to every material claim.

## Output Fields

For each candidate return:

- Stable source key and source family
- Normalized company and founder identity
- Website/domain
- Company LinkedIn URL and founder LinkedIn URLs
- Company number, repo id, tweet id, post id, or actor row key where applicable
- Website/product summary
- AI/B2B/stage/geography/founder evidence
- Missing data flags
- Source receipts

## Boundaries

- Do not make final Meet/Watch/Pass decisions.
- Do not pay for expensive scraping unless approved by source budget.
- Do not write to CRM, Notion, Slack, or Deal Pipeline projects.
- Do not contact founders.
