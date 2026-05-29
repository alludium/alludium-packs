---
id: vc.companies_house_sync_read
title: Preview Companies House Public Register Results
slug: companies-house-sync-read
agent: vc-integration-operator
skills:
- vc-companies-house-sync-read
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-integrations/companies-house-sync-read.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Preview Companies House Public Register Results

## Objective

Preview selected Companies House public search results and company profile pages before using them as VC origination source context.

## What To Do

Build a read preview only after discovery has selected public search URLs, result limits, and page-preview scope. Use Firecrawl to scrape approved Companies House search result pages and selected `/company/<number>` public profile pages. Return company identity signals, company number, status, incorporation date, company type, registered office locality when visible, SIC or nature-of-business text when visible, direct source URLs, scrape timestamp, result rank, and suggested source-registry mapping.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Selected Companies House Scope.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Deliverable

- Produce a concise, reviewable task response that a human can act on.
- Also include a short human-readable summary covering: Companies House Results Preview, Source Registry Mapping. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for selected public search URLs, result limits, selected company numbers, and Firecrawl availability before processing company pages.

## Guardrails

Read preview only. Do not call authenticated Companies House APIs, import companies, enable recurring monitoring, score candidates, write candidate records, update external systems, or create Deal Pipeline projects.

## Completion Criteria

- Preview rows include company number, name, status, selected source signals, source receipts, result rank, and rejection reasons when available.
- Firecrawl result metadata, source URLs, scrape timestamps, or missing metadata are named.
- Import, recurring monitoring, scoring, and promotion approvals remain separate from the preview.

## Human Review

- Approve result rows before candidate import or scoring.
- Approve source registry mappings and dedupe keys separately.
