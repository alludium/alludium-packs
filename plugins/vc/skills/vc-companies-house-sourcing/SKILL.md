---
id: vc-companies-house-sourcing
name: "VC Companies House Sourcing"
description: >
  Discover public Companies House search scope through Firecrawl-backed page
  extraction without importing candidates or enabling recurring monitoring.
tags:
  - vc
  - companies-house
  - discovery
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
      note: Use the connected Firecrawl application `firecrawl-mcp-hosted` to scrape approved public Companies House search and company pages.
      gracefulDegradation: Report missing Firecrawl availability and ask for approved public URLs or a supplied source-scope inventory.
  routingHints:
    preferredSurface: skill
    notes:
      - Discovery chooses filters and source surfaces before any read preview.
---

# VC Companies House Public Register Sourcing

Use this skill to identify Companies House public register source scope for VC origination without a native Companies House connector.

## Required Inputs

- Firecrawl availability or supplied Companies House public register pages
- Approved search terms, company-name filters, result limits, and public URL patterns
- Result limit and review policy

## Public URL Patterns

Use only the public Companies House register surfaces:

- Broad company search: `https://find-and-update.company-information.service.gov.uk/search/companies?q=<term>`
- Advanced company results: `https://find-and-update.company-information.service.gov.uk/advanced-search/get-results?companyNameIncludes=<term>`
- Company profile: `https://find-and-update.company-information.service.gov.uk/company/<company_number>`

## Discovery Output

Return:

- `tool_discovery_status`: Firecrawl available, missing, or blocked
- `approved_search_urls`: exact public Companies House URLs to scrape next
- `source_scope`: selected terms, result limits, and extraction scope
- `scope_questions`: user choices needed before sync read

## Boundaries

- Do not call the Companies House API.
- Do not scrape outside `find-and-update.company-information.service.gov.uk`.
- Do not import companies.
- Do not persist candidate state.
- Do not enable recurring monitoring.
- Do not score candidates.
- Do not write to external systems or create Deal Pipeline projects.
