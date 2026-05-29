---
id: vc.discover_linkedin_founder_candidates
title: Discover LinkedIn Founder Candidates
slug: discover-linkedin-founder-candidates
agent: vc-sourcing-operator
skills:
- vc-apify-linkedin-founder-discovery
- vc-source-registry-and-state-management
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/discover-linkedin-founder-candidates.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Discover LinkedIn Founder Candidates

## Objective

Find early UK/Ireland AI founder and company candidates through approved Apify LinkedIn actor tracks.

## What To Do

Use only approved Apify LinkedIn actor scopes. Mirror the reference pipeline's four-track model covering active AI founders, pedigree founders, exited or serial founders, and academic spinouts. Preserve per-query pagination/offsets, exhaustion locks, seen profile IDs, company URL slug dedupe, and quarantine rows without stable company identifiers. Treat LinkedIn people discovery as weekly by default because it is the expensive source.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: LinkedIn Discovery Scope.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Deliverable

- Create or update **LinkedIn Discovery Artifact** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.
- Also include a short human-readable summary covering: Discovery Report, Source Result Count, Source State Summary. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for actor allowlist, track selection, geography, result caps, query budget, dedupe-state availability, and whether this is a weekly full run or forced override.

## Guardrails

Discovery proposal only. Do not scrape unapproved profiles, bypass platform policy, import candidates, write CRM records, send outreach, or create Deal Pipelines.

## Completion Criteria

- Candidate preview includes track, founder profile URL, company name, company LinkedIn URL or stable key, founder role, geography evidence, score reasons, and source receipt.
- Source-state update includes seen profile IDs, company slugs, query offsets, exhaustion/rewind notes, and quarantine rows.
- Cost/run metadata or missing cost metadata is explicit.
