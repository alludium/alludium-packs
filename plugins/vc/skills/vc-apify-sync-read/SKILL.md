---
id: vc-apify-sync-read
name: "VC Apify Sync Read"
description: >
  Preview selected Apify actor results for VC origination with source receipts,
  identity signals, and source-registry mapping recommendations.
tags:
  - vc
  - apify
  - sync-read
  - origination
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: required
      required: true
      note: Use the connected Apify application `apify-actors-mcp` only for approved sample reads.
      gracefulDegradation: Produce a preview plan from supplied actor metadata and ask for authorization.
  routingHints:
    preferredSurface: skill
    notes:
      - Sync-read is a reviewed preview, not candidate import or scheduling.
---

# VC Apify Sync Read

Use this skill to preview selected Apify actor output for a VC origination pipeline.

## Required Inputs

- Selected actor scope from discovery
- Approved sample-read limits and budget policy
- Known input filters, dataset IDs, or supplied result sample

## Preview Output

Return:

- `apify_results_preview`: selected result rows with source receipts, identity signals, and confidence notes
- `source_registry_mapping`: proposed source keys, dedupe keys, actor metadata, and unresolved mapping questions
- `run_receipts`: run IDs, dataset IDs, cost metadata, and missing metadata when available
- `rejection_reasons`: why rows should not become candidates yet

## Boundaries

- Do not import candidates.
- Do not score candidates.
- Do not enable recurring actor runs.
- Do not write candidate state or CRM records.
- Do not send outreach or create Deal Pipeline projects.
