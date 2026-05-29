---
id: vc.apify_discovery
title: Explore Apify Origination Sources
slug: apify-discovery
agent: vc-integration-operator
skills:
- vc-apify-discovery
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-integrations/apify-discovery.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Explore Apify Origination Sources

## Objective

Discover approved Apify actors, input schemas, source scope, and run-cost guardrails before any VC origination read preview.

## What To Do

Use the connected `apify-actors-mcp` application only after authorization and tool discovery. Enumerate approved actors, input requirements, estimated cost controls, and safe sample-read options. If live tools are not available, produce the missing-tool discovery checklist and ask for an approved actor inventory instead of inventing actor IDs.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Discovery Goal.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Deliverable

- Produce a concise, reviewable task response that a human can act on.
- Also include a short human-readable summary covering: Apify Discovery Report, Source Scope Questions. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for authorization, actor allowlist, source policy, or supplied actor inventory when live discovery is unavailable.

## Guardrails

Discovery only. Do not start actor runs, import candidates, persist candidate state, score candidates, contact founders, update external systems, or create Deal Pipeline projects.

## Completion Criteria

- Available or supplied Apify actors are listed with source purpose and read-preview requirements.
- Tool discovery status and any missing authorization are explicit.
- User choices needed before sync read are explicit.

## Human Review

- Choose approved actors and source policy before sync read.
- Approve sample-run budget and result scope separately.
