---
id: vc.notion_sync_read
title: Preview Notion Context
slug: notion-sync-read
agent: vc-integration-operator
skills:
- vc-notion-sync-read
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-integrations/notion-sync-read.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Preview Notion Context

## Objective

Preview selected Notion page, block, property, and database content before attaching it to Deal Pipeline tasks.

## What To Do

Build a Notion read preview from the approved page or database scope. Use `notion-retrieve-page`, `notion-retrieve-block`, `notion-retrieve-page-property-item`, `notion-retrieve-database-schema`, `notion-retrieve-database-content`, and `notion-query-database` only inside the selected scope. Summarize proposed target mapping as Deal Pipeline setup context, task context, artifact input, or human reference before any attachment or import.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Selected Notion Scope.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Deliverable

- Produce a concise, reviewable task response that a human can act on.
- Also include a short human-readable summary covering: Notion Context Preview, Target Context Mapping. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for approved page or database scope before reading content.

## Guardrails

Read preview only. Do not attach, import, create pages, create databases, update pages, update databases, append blocks, delete blocks, duplicate pages, upload files, or create comments without a separate approval path.

## Completion Criteria

- Preview names source page, block, database, or row IDs and sensitivity caveats.
- Relevant content is summarized with source provenance.
- Attachment or import approval remains separate from the preview.

## Human Review

- Approve selected page, block, database, and row context before attaching it to project or task state.
- Approve duplicate handling and target mapping.
