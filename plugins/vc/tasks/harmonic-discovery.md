---
id: vc.harmonic_discovery
title: Explore Harmonic Source Scopes
slug: harmonic-discovery
agent: vc-integration-operator
skills:
- vc-harmonic-discovery
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-integrations/harmonic-discovery.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Explore Harmonic Source Scopes

## Objective

Discover Harmonic saved searches, daily searches, and source scope before selected VC sourcing context reads.

## What To Do

Use the connected `harmonic-mcp-oauth` application only after tool discovery has produced live tool rows. The current local platform catalog has the Harmonic OAuth application and connection template but no trusted Harmonic tool external IDs, so report missing tool discovery explicitly if no tools are available. When tools are discovered, enumerate saved searches, daily searches, or comparable source scopes and ask the user to choose the sourcing scope before any read-sync task.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Discovery Goal.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Deliverable

- Produce a concise, reviewable task response that a human can act on.
- Also include a short human-readable summary covering: Harmonic Discovery Report, Source Scope Questions. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

If Harmonic is not authorized or has no discovered tools, report the setup gap and ask for authorization/tool discovery or a supplied saved-search inventory.

## Guardrails

Discovery only. Do not process company results, mark search results as seen, update saved searches, export contacts, enrich records, or write back to Harmonic.

## Completion Criteria

- Available Harmonic saved searches or source scopes are listed when tools exist.
- The report explicitly states whether trusted Harmonic tool IDs were discovered.
- User choices needed before result processing are explicit.

## Human Review

- Choose saved search, daily search, or source scope before sync read.
- Approve whether net-new result processing is in scope.
