---
id: vc.companies_house_sync_read
title: Preview Companies House Public Register Results
slug: companies-house-sync-read
agent: vc-origination-scout
skills:
- vc-companies-house-sync-read
- citation-enforcement
---

# Preview Companies House Public Register Results

Preview selected Companies House public search results and company profile pages before using them as VC origination source context.

## Instructions

Build a read preview only after discovery has selected public search URLs, result limits, and page-preview scope. Use Firecrawl to scrape approved Companies House search result pages and selected `/company/<number>` public profile pages. Return company identity signals, company number, status, incorporation date, company type, registered office locality when visible, SIC or nature-of-business text when visible, direct source URLs, scrape timestamp, result rank, and suggested source-registry mapping.

## Missing Input Policy

Ask for selected public search URLs, result limits, selected company numbers, and Firecrawl availability before processing company pages.

## External Action Policy

Read preview only. Do not call authenticated Companies House APIs, import companies, enable recurring monitoring, score candidates, write candidate records, update external systems, or create Deal Room projects.

## Completion Criteria

- Preview rows include company number, name, status, selected source signals, source receipts, result rank, and rejection reasons when available.
- Firecrawl result metadata, source URLs, scrape timestamps, or missing metadata are named.
- Import, recurring monitoring, scoring, and promotion approvals remain separate from the preview.

## Human Decision Points

- Approve result rows before candidate import or scoring.
- Approve source registry mappings and dedupe keys separately.

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `selected_companies_house_scope` | Selected Companies House Scope | `json` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `companies_house_results_preview` | Companies House Results Preview | `richtext` | no |
| `source_registry_mapping` | Source Registry Mapping | `json` | no |

## Routing

- Source template: `alludium/task-definition-templates/vc-integrations/companies-house-sync-read.yaml`
- Alludium task ID: `vc.companies_house_sync_read`
- Task family: `integration_sync_read`
- Recommended agent: `vc-origination-scout` (Alludium template `vc_origination_scout`)
- Supported project types:
  - `vc_origination_pipeline`
- Supported project scopes:
  - `project_management`

## Required Skills

- `vc-companies-house-sync-read`
- `citation-enforcement`

## Planned Skills

- `vc-companies-house-sync-read`
- `citation-enforcement`
