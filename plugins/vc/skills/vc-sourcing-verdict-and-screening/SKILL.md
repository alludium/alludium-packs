---
id: vc-sourcing-verdict-and-screening
name: "VC Sourcing Verdict & Screening"
description: >
  Score enriched origination candidates into Meet, Watch, or Pass with urgency,
  evidence quality, hard stage safety, and active-candidate screening outcomes.
tags:
  - vc
  - origination
  - scoring
  - screening
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
  routingHints:
    preferredSurface: skill
    notes:
      - This skill recommends actions; external sync or promotion happens in separate approved tasks.
---

# VC Sourcing Verdict & Screening

Use this skill after candidate enrichment and relationship checks.

## Verdict Contract

Return:

- `action`: `Meet`, `Watch`, or `Pass`
- `urgency`: high, medium, low, or none
- `fit`: concise thesis-fit rationale
- `confidence`: high, medium, low
- `funding_status`
- `hq_or_geography_concern`
- `founder_or_frontier_pedigree_evidence`
- `reasons`
- `receipts`

## Hard Safety Rules

Pass when reliable evidence shows:

- Series A or later funding, unless the thesis explicitly allows later-stage companies
- More than 20 employees, unless the thesis explicitly allows that size
- Outside geography with no allowed exception
- Agency, consultancy, media, investor, or service-provider positioning where product startup evidence is absent

Only apply the Series A/headcount safety rule when the LinkedIn company or another reliable company-size/funding source is fresh enough to trust.

## Two-Pass LinkedIn Company Pattern

First pass scores from cheap enrichment.

For Meet/Watch rows only, run or consume approved LinkedIn company-page enrichment, then rescore rows with fresh company headcount/funding evidence.

## Active Candidate Screen

For active candidates, return `PROCEED_TO_IC`, `DIG_FURTHER`, or `PASS`. Do not downgrade protected manual actions.

## Boundaries

- Do not sync records.
- Do not overwrite human decisions.
- Do not create Deal Pipelines.
- Do not send outreach.
