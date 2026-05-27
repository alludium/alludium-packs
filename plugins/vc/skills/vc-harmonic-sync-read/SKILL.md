---
id: vc-harmonic-sync-read
name: "VC Harmonic Sync Read"
description: >
  Preview selected Harmonic company, founder, or saved-search results for VC
  sourcing and screening context before import or watchlist action.
tags:
  - vc
  - harmonic
  - company-intelligence
  - sync-read
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: required
      required: true
      note: Use `harmonic-mcp-oauth` only after OAuth authorization and tool discovery. The current local platform catalog has no trusted Harmonic tool external IDs.
      gracefulDegradation: Draft the preview contract from supplied exports and mark live reads blocked until tool discovery exists.
  routingHints:
    preferredSurface: skill
    notes:
      - Read sync previews selected search results only; import, watchlist creation, and recurring monitoring require separate approval.
---

# VC Harmonic Sync Read

Use this skill after Harmonic discovery has selected a saved search, daily search, company, person, or result scope and confirmed live tool discovery.

## Required Inputs

- Harmonic discovery report
- Selected source scope and discovered tool IDs, or a supplied export
- Target mapping preference: sourcing context, task context, watchlist candidates, or Deal Pipeline setup context
- Dedupe and rejection criteria

## Tool Plan

If no Harmonic tools are discovered, report live reads as blocked. Do not guess tool IDs.

When tools exist, use only the selected source scope:

1. Fetch selected company or person result rows.
2. Capture stable Harmonic source IDs and available source URLs.
3. Summarize company/founder identity, stage, geography, sector, traction, funding, and relevance signals when present.
4. Propose target mapping and dedupe decisions before import or watchlist action.

## Preview Output

Return:

- source IDs and source URLs when available
- company/person identity signals and matching keys
- relevant sourcing or screening context
- proposed target mapping
- duplicate, rejected, or low-confidence rows
- tool discovery status and tool IDs used or missing

## Boundaries

- Do not import companies or create Deal Pipelines without preview approval.
- Do not mark net-new results as seen.
- Do not update saved searches, export contacts, or write back to Harmonic.
- Do not enable recurring monitoring from this task.
