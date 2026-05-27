---
id: vc-notion-sync-read
name: "VC Notion Sync Read"
description: >
  Preview selected Notion page, block, property, and database context for VC
  Deal Pipeline tasks without broad workspace ingestion.
tags:
  - vc
  - notion
  - workspace-docs
  - sync-read
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: required
      required: true
      note: Use `notion-retrieve-page`, `notion-retrieve-block`, `notion-retrieve-page-property-item`, `notion-retrieve-database-schema`, `notion-retrieve-database-content`, and `notion-query-database` only inside approved scope.
      gracefulDegradation: Ask for copied Notion excerpts or exported pages/databases.
  routingHints:
    preferredSurface: skill
    notes:
      - Read sync is selected-context only; do not ingest broad workspaces.
---

# VC Notion Sync Read

Use this skill after Notion discovery has selected the allowed page, database, block, or row scope.

## Required Inputs

- Notion discovery report
- Approved page, database, block, or row scope
- Deal, project, or task context that explains why Notion context is needed
- Sensitivity exclusions

## Tool Plan

1. Use `notion-retrieve-page` for approved page metadata.
2. Use `notion-retrieve-block` for approved block content.
3. Use `notion-retrieve-page-property-item` for approved page properties.
4. Use `notion-retrieve-database-schema`, `notion-retrieve-database-content`, and `notion-query-database` only for selected databases and filters.

## Preview Output

Return:

- page, block, database, or row IDs used
- summarized content with source provenance
- suggested target: Deal Pipeline setup context, task context, artifact input, or human reference
- excluded content and reason
- duplicate or sensitivity caveats

## Boundaries

- Do not read unapproved pages, databases, blocks, or rows.
- Do not attach or import without preview approval.
- Do not create, update, append, delete, duplicate, upload, or comment in Notion.
- Do not treat Notion notes as final investment evidence without corroboration.
