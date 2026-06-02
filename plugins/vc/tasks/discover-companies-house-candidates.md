---
id: vc.discover_companies_house_candidates
title: Discover Companies House Candidates
slug: discover-companies-house-candidates
agent: vc-sourcing-operator
skills:
- vc-companies-house-sourcing
- vc-source-registry-and-state-management
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/discover-companies-house-candidates.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Discover Companies House Candidates

## Objective

Discover UK company candidates from approved Companies House public-register pages using reference-pipeline scoring and dedupe patterns.

## What To Do

Discover candidate companies from approved public Companies House search/result pages. Mirror the reference pipeline's two-window intent for recent incorporations and mature/fundraising-age companies. Prioritize active UK companies with software, data, R&D, biotech, AI, robotics, or deep-tech signals; reject mass-registration addresses, service/consultancy language, outside-geography signals, corporate officers, and weak name/location/founder evidence. Use company number as the primary dedupe key.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Companies House Discovery Scope.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Deliverable

- Create or update **Companies House Discovery Artifact** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.
- Also include a short human-readable summary covering: Discovery Report, Source Result Count, Source State Summary. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for selected public URL patterns, geography/stage/sector scope, result limits, allowed SIC or keyword filters, and Firecrawl availability before extraction.

## Guardrails

Read preview and candidate proposal only. Do not call the Companies House API, import candidates, score final verdicts, enable recurring monitoring, write CRM rows, or create Deal Pipelines.

## Completion Criteria

- Candidate preview includes company number, name, status, incorporation date, visible SIC/nature text, address locality, founder/officer hints when visible, source URL, and extraction timestamp.
- Rejection reasons and dedupe decisions are listed.
- Source-state update records company-number keys and selected search windows.
