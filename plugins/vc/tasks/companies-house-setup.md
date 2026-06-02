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

## Objective

Configure Firecrawl-backed public Companies House search and company-page previews for a VC origination pipeline.

## What To Do

Confirm that Companies House public register preview is a selected origination source, then coordinate Firecrawl readiness, search terms, allowed public URLs, result limits, and reviewed read-preview setup. Use public search URLs such as `https://find-and-update.company-information.service.gov.uk/search/companies?q=<term>` and `https://find-and-update.company-information.service.gov.uk/advanced-search/get-results?companyNameIncludes=<term>` as the approved source surface. Create child tasks from the declared integrationSetup flow only when the user chooses that step. Keep imports, recurring monitoring, candidate scoring, CRM writes, outreach, and Deal Pipeline promotion disabled unless a later human approval explicitly creates that task.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Setup Goal.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Deliverable

- Produce a concise, reviewable task response that a human can act on.
- Also include a short human-readable summary covering: Setup Summary, Accepted Connection Scope, Child Task Plan, Sync Policy. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

If Firecrawl is not available or no source scope is selected, keep setup incomplete and ask for Firecrawl availability, search terms, result limits, selected public register URLs, or source-scope decisions.

## Guardrails

Setup orchestration only. Do not call the Companies House API, import companies, enable recurring sync, write candidate records, update external systems, or create Deal Pipeline projects from this setup task.

## Completion Criteria

- Firecrawl availability is connected or the missing extraction-tool gap is recorded.
- Search terms, public URL patterns, result limits, and source scope are recorded, or unanswered decisions are explicit.
- Read-preview policy is recorded without enabling imports, recurring sync, scoring, or writes.
- The accepted extraction scope states whether Firecrawl access is personal, project-shared, or workspace-shared.

## Human Review

- Choose whether Firecrawl access is personal, project-shared, or workspace-shared.
- Choose search terms, approved public Companies House URLs, result limits, and candidate filter scope.
- Approve any read-preview, import, recurring monitoring, or write task separately.
