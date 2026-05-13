---
id: vc.companies_house_discovery
title: Explore Companies House Public Register Scope
slug: companies-house-discovery
agent: vc-origination-scout
skills:
- vc-companies-house-sourcing
- citation-enforcement
---

<!-- Generated from alludium/task-definition-templates/vc-integrations/companies-house-discovery.yaml; do not edit directly. Run python plugins/vc/scripts/generate_markdown.py after changing the YAML source. -->

# Explore Companies House Public Register Scope

Discover public Companies House search URLs, result limits, and page-preview scope before selected VC origination reads.

## Instructions

Use the connected `firecrawl-mcp-hosted` application to inspect only approved public Companies House pages. Construct public search URLs from approved terms and filters, such as `/search/companies?q=<term>` for broad company search and `/advanced-search/get-results?companyNameIncludes=<term>` for table-like advanced results. Prefer HTML or structured extraction when available so company names, company numbers, statuses, addresses, result ranks, and direct `/company/<number>` links can be captured with source receipts.

## Missing Input Policy

Ask for Firecrawl availability, selected search terms, result limits, approved public URL patterns, or a supplied inventory when live extraction is unavailable.

## External Action Policy

Discovery only. Do not call authenticated Companies House APIs, import companies, process candidate queues, persist source state, score candidates, update external systems, or create Deal Room projects.

## Completion Criteria

- Approved public Companies House search URLs and source-scope decisions are listed.
- Firecrawl availability and any missing extraction-tool gap are explicit.
- User choices needed before sync read are explicit.

## Human Decision Points

- Choose keyword, company-name, result-limit, and optional advanced-search scope before sync read.
- Approve sample-result processing separately.

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `discovery_goal` | Discovery Goal | `string` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `companies_house_discovery_report` | Companies House Discovery Report | `richtext` | no |
| `source_scope_questions` | Source Scope Questions | `json` | no |

## Routing

- Source template: `alludium/task-definition-templates/vc-integrations/companies-house-discovery.yaml`
- Alludium task ID: `vc.companies_house_discovery`
- Task family: `integration_discovery`
- Recommended agent: `vc-origination-scout` (Alludium template `vc_origination_scout`)
- Supported project types:
  - `vc_origination_pipeline`
- Supported project scopes:
  - `project_management`

## Required Skills

- `vc-companies-house-sourcing`
- `citation-enforcement`

## Planned Skills

- `vc-companies-house-sourcing`
- `citation-enforcement`
