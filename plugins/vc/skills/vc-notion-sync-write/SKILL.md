---
id: vc-notion-sync-write
name: "VC Notion Sync Write"
description: >
  Draft Notion page, database, block, or comment update proposals for VC
  workflows without performing broad workspace mutation.
tags:
  - vc
  - notion
  - workspace-docs
  - sync-write
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: recommended
      required: false
      note: Later approved execution candidates may include `notion-create-comment`, `notion-append-block`, `notion-update-page`, or `notion-update-database`; this skill drafts proposals only.
      gracefulDegradation: Produce before/after proposals for human copy-and-apply review.
  routingHints:
    preferredSurface: skill
    notes:
      - This skill drafts proposals. It does not mutate Notion.
---

# VC Notion Sync Write

Use this skill to turn approved Alludium outputs into reviewable Notion update proposals.

## Allowed Proposal Types

- Comment draft on an approved page
- Page-property update proposal with before/after values
- Block or section draft for a selected page
- Database row update proposal for a selected database item

## Required Evidence

Every proposal must include:

- target page, database, block, or row ID
- current value or current context when known
- proposed value, block text, or comment text
- source artifact, task output, meeting note, or human decision that supports it
- approval owner and audit note
- explicit statement that no Notion write has been performed

## Tool Guidance

Available write surfaces include `notion-create-comment`, `notion-append-block`, `notion-update-page`, and `notion-update-database`, but use them only in a later approved runtime workflow. This skill does not execute writes.

## Boundaries

- Do not create pages, create databases, update pages, update databases, append blocks, delete blocks, duplicate pages, upload files, or create comments.
- Do not propose broad page/database mutation or workspace restructuring.
- Do not claim Notion was updated unless a tool result confirms it in a separate approved workflow.
