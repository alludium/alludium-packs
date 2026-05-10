---
id: vc-companies-house-sync-read
name: "VC Companies House Sync Read"
description: >
  Preview selected public Companies House search results and company pages for
  VC origination with receipts and source-registry mapping recommendations.
tags:
  - vc
  - companies-house
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
      applicationExternalId: firecrawl-mcp-hosted
      note: Use the connected Firecrawl application `firecrawl-mcp-hosted` only for approved public Companies House pages.
      gracefulDegradation: Produce a preview plan from supplied public register records and ask for Firecrawl availability.
  routingHints:
    preferredSurface: skill
    notes:
      - Sync-read is source preview only; candidate import is out of scope.
---

# VC Companies House Public Register Sync Read

Use this skill to preview selected Companies House public register records for a VC origination pipeline.

## Required Inputs

- Selected public search URLs from discovery
- Approved result limits and selected company profile URLs
- Known filters, company numbers, or supplied result sample

## Preview Output

Return:

- `companies_house_results_preview`: selected company rows with company number, name, status, incorporation date, company type, visible SIC/nature-of-business text, source URL, scrape timestamp, and result rank
- `source_registry_mapping`: proposed source keys, dedupe keys, and unresolved mapping questions
- `source_receipts`: search URLs, company profile URLs, scrape timestamps, extraction method, and missing metadata when available
- `rejection_reasons`: why rows should not become candidates yet

## Boundaries

- Do not call the Companies House API.
- Do not scrape outside `find-and-update.company-information.service.gov.uk`.
- Do not import candidates.
- Do not score companies.
- Do not enable recurring monitoring.
- Do not write candidate state, CRM records, or external notes.
- Do not create Deal Room projects.
