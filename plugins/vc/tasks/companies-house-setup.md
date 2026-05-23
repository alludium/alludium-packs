---
id: vc.companies_house_setup
title: Configure Companies House Public Register Preview
slug: companies-house-setup
agent: vc-integration-operator
skills:
- vc-companies-house-sourcing
- vc-companies-house-sync-read
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-integrations/companies-house-setup.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Configure Companies House Public Register Preview

Configure Firecrawl-backed public Companies House search and company-page previews for a VC origination pipeline.

## Instructions

Confirm that Companies House public register preview is a selected origination source, then coordinate Firecrawl readiness, search terms, allowed public URLs, result limits, and reviewed read-preview setup. Use public search URLs such as `https://find-and-update.company-information.service.gov.uk/search/companies?q=<term>` and `https://find-and-update.company-information.service.gov.uk/advanced-search/get-results?companyNameIncludes=<term>` as the approved source surface. Create child tasks from the declared integrationSetup flow only when the user chooses that step. Keep imports, recurring monitoring, candidate scoring, CRM writes, outreach, and Deal Room promotion disabled unless a later human approval explicitly creates that task.

## Missing Input Policy

If Firecrawl is not available or no source scope is selected, keep setup incomplete and ask for Firecrawl availability, search terms, result limits, selected public register URLs, or source-scope decisions.

## External Action Policy

Setup orchestration only. Do not call the Companies House API, import companies, enable recurring sync, write candidate records, update external systems, or create Deal Room projects from this setup task.

## Completion Criteria

- Firecrawl availability is connected or the missing extraction-tool gap is recorded.
- Search terms, public URL patterns, result limits, and source scope are recorded, or unanswered decisions are explicit.
- Read-preview policy is recorded without enabling imports, recurring sync, scoring, or writes.
- The accepted extraction scope states whether Firecrawl access is personal, project-shared, or workspace-shared.

## Human Decision Points

- Choose whether Firecrawl access is personal, project-shared, or workspace-shared.
- Choose search terms, approved public Companies House URLs, result limits, and candidate filter scope.
- Approve any read-preview, import, recurring monitoring, or write task separately.

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `setup_goal` | Setup Goal | `string` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `setup_summary` | Setup Summary | `richtext` | no |
| `accepted_connection_scope` | Accepted Connection Scope | `string` | no |
| `child_task_plan` | Child Task Plan | `json` | no |
| `sync_policy` | Sync Policy | `json` | no |

## Routing

- Source template: `alludium/task-definition-templates/vc-integrations/companies-house-setup.yaml`
- Alludium task ID: `vc.companies_house_setup`
- Task family: `integration_setup`
- Recommended agent: `vc-integration-operator` (Alludium template `vc_integration_operator`)
- Supported project types:
  - `vc_origination_pipeline`
- Supported project scopes:
  - `project_management`

## Required Skills

- `vc-companies-house-sourcing`
- `vc-companies-house-sync-read`
- `citation-enforcement`
