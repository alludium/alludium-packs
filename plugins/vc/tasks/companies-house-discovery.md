---
id: vc.companies_house_discovery
title: Explore Companies House Public Register Scope
slug: companies-house-discovery
agent: vc-integration-operator
skills:
- vc-companies-house-sourcing
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-integrations/companies-house-discovery.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Explore Companies House Public Register Scope

## Objective

Discover public Companies House search URLs, result limits, and page-preview scope before selected VC origination reads.

## What To Do

Use the connected `firecrawl-mcp-hosted` application to inspect only approved public Companies House pages. Construct public search URLs from approved terms and filters, such as `/search/companies?q=<term>` for broad company search and `/advanced-search/get-results?companyNameIncludes=<term>` for table-like advanced results. Prefer HTML or structured extraction when available so company names, company numbers, statuses, addresses, result ranks, and direct `/company/<number>` links can be captured with source receipts.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Discovery Goal.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Deliverable

- Produce a concise, reviewable task response that a human can act on.
- Also include a short human-readable summary covering: Companies House Discovery Report, Source Scope Questions. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for Firecrawl availability, selected search terms, result limits, approved public URL patterns, or a supplied inventory when live extraction is unavailable.

## Guardrails

Discovery only. Do not call authenticated Companies House APIs, import companies, process candidate queues, persist source state, score candidates, update external systems, or create Deal Pipeline projects.

## Completion Criteria

- Approved public Companies House search URLs and source-scope decisions are listed.
- Firecrawl availability and any missing extraction-tool gap are explicit.
- User choices needed before sync read are explicit.

## Human Review

- Choose keyword, company-name, result-limit, and optional advanced-search scope before sync read.
- Approve sample-result processing separately.
