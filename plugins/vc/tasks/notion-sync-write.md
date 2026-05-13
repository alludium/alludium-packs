---
id: vc.notion_sync_write
title: Draft Notion Update Proposals
slug: notion-sync-write
agent: vc-pipeline-autopilot
skills:
- vc-notion-sync-write
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-integrations/notion-sync-write.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Draft Notion Update Proposals

Draft reviewable Notion page, database, or comment proposals from VC task outputs without performing broad workspace mutation.

## Instructions

Draft Notion update proposals only. Each proposal must include the target page, database, block, or row ID, before/after summary when known, proposed content, source evidence, owner approval, and a clear statement that no Notion write has been performed. Reference available write surfaces such as `notion-create-comment`, `notion-append-block`, `notion-update-page`, or `notion-update-database` only as later approved execution candidates; this task must not execute them.

## Missing Input Policy

Ask for the source artifact, target Notion object, proposed content, and approval owner before drafting.

## External Action Policy

Draft only. Do not create pages, create databases, update pages, update databases, append blocks, delete blocks, duplicate pages, upload files, or create comments.

## Completion Criteria

- Every proposal is evidence-backed and approval-gated.
- The output clearly states no Notion writes were performed.
- Broad page/database mutation remains outside this task unless a separate explicit approval workflow exists.

## Human Decision Points

- Approve exact target object and proposed content before any future execution.
- Approve whether a Notion write is appropriate at all for the workflow.

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `notion_write_source` | Notion Write Source | `json` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `notion_update_proposals` | Notion Update Proposals | `richtext` | no |

## Routing

- Source template: `alludium/task-definition-templates/vc-integrations/notion-sync-write.yaml`
- Alludium task ID: `vc.notion_sync_write`
- Task family: `integration_sync_write`
- Recommended agent: `vc-pipeline-autopilot` (Alludium template `vc_pipeline_autopilot`)
- Supported project types:
  - `vc_deal_room`
- Supported project scopes:
  - `project_management`

## Required Skills

- `vc-notion-sync-write`
- `citation-enforcement`

## Planned Skills

- `vc-notion-sync-write`
- `citation-enforcement`
