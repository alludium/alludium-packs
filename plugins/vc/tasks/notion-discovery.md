---
id: vc.notion_discovery
title: Explore Notion Pages and Databases
slug: notion-discovery
agent: vc-integration-operator
skills:
- vc-notion-discovery
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-integrations/notion-discovery.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Explore Notion Pages and Databases

## Objective

Discover Notion page, database, and workspace scope before selected Deal Pipeline context reads.

## What To Do

Use the connected notion application to confirm account context with `notion-get-current-user`, search accessible pages and databases with `notion-search`, and inspect candidate database shape with `notion-retrieve-database-schema` when selected. Ask the user to choose the page or database scope before any read-sync task.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Discovery Goal.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Deliverable

- Produce a concise, reviewable task response that a human can act on.
- Also include a short human-readable summary covering: Notion Discovery Report, Scope Questions. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

If Notion is not authorized, ask for authorization or a supplied page/database inventory.

## Guardrails

Discovery only. Do not read broad page contents, create pages, create databases, update pages, update databases, append blocks, delete blocks, duplicate pages, upload files, or create comments.

## Completion Criteria

- Candidate pages, databases, owners, and scope signals are listed with IDs when available.
- Tool IDs used or missing are named.
- User choices needed before page or database preview are explicit.

## Human Review

- Choose page or database scope before sync read.
- Approve whether properties, blocks, or database rows are in scope.
- Approve any later import or attachment separately.
