---
id: vc-notion-discovery
name: "VC Notion Discovery"
description: >
  Discover Notion workspace, page, and database scope before previewing VC
  operating docs, memos, knowledge bases, or lightweight deal-tracking content.
tags:
  - vc
  - notion
  - workspace-docs
  - discovery
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: required
      required: true
      note: Use the connected Notion application `notion`; expected discovery tools are `notion-get-current-user`, `notion-search`, and `notion-retrieve-database-schema`.
      gracefulDegradation: Ask for Notion authorization or a supplied page/database inventory.
  routingHints:
    preferredSurface: skill
    notes:
      - Discovery chooses page/database scope and must not read broad content or mutate Notion.
---

# VC Notion Discovery

Use this skill to identify the Notion scope relevant to a VC workflow.

## Required Inputs

- Authorized `notion` connection or a supplied page/database inventory
- Intended workflow, such as deal tracking, memo preparation, knowledge-base handoff, or diligence source review
- Known page, database, company, deal, or workspace names
- Sensitive or excluded pages/databases

## Tool Plan

1. Use `notion-get-current-user` to confirm account context.
2. Use `notion-search` to find candidate pages and databases.
3. Use `notion-retrieve-database-schema` only for selected candidate databases.

## Discovery Output

Return:

- workspace identity
- candidate pages and databases with IDs
- database property summaries for selected candidates
- excluded pages/databases and why
- recommended page/database scope
- questions for the user to approve before sync read

## Boundaries

- Do not read broad page or database content during discovery.
- Do not create, update, append, delete, duplicate, upload, or comment in Notion.
- Do not treat every Notion database as deal pipeline without user confirmation.
