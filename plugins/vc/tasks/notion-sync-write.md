---
id: vc.notion_sync_write
title: Draft Notion Update Proposals
slug: notion-sync-write
agent: vc-integration-operator
skills:
- vc-notion-sync-write
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-integrations/notion-sync-write.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Draft Notion Update Proposals

## Objective

Draft reviewable Notion page, database, or comment proposals from VC task outputs without performing broad workspace mutation.

## What To Do

Draft Notion update proposals only. Each proposal must include the target page, database, block, or row ID, before/after summary when known, proposed content, source evidence, owner approval, and a clear statement that no Notion write has been performed. Reference available write surfaces such as `notion-create-comment`, `notion-append-block`, `notion-update-page`, or `notion-update-database` only as later approved execution candidates; this task must not execute them.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Notion Write Source.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Deliverable

- Produce a concise, reviewable task response that a human can act on.
- Also include a short human-readable summary covering: Notion Update Proposals. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for the source artifact, target Notion object, proposed content, and approval owner before drafting.

## Guardrails

Draft only. Do not create pages, create databases, update pages, update databases, append blocks, delete blocks, duplicate pages, upload files, or create comments.

## Completion Criteria

- Every proposal is evidence-backed and approval-gated.
- The output clearly states no Notion writes were performed.
- Broad page/database mutation remains outside this task unless a separate explicit approval workflow exists.

## Human Review

- Approve exact target object and proposed content before any future execution.
- Approve whether a Notion write is appropriate at all for the workflow.
