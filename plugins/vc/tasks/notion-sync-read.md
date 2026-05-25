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

Preview selected Notion page, block, property, and database content before attaching it to VC Deal Room tasks.

## Instructions

Build a Notion read preview from the approved page or database scope. Use `notion-retrieve-page`, `notion-retrieve-block`, `notion-retrieve-page-property-item`, `notion-retrieve-database-schema`, `notion-retrieve-database-content`, and `notion-query-database` only inside the selected scope. Summarize proposed target mapping as Deal Room setup context, task context, artifact input, or human reference before any attachment or import.

## Missing Input Policy

Ask for approved page or database scope before reading content.

## External Action Policy

Read preview only. Do not attach, import, create pages, create databases, update pages, update databases, append blocks, delete blocks, duplicate pages, upload files, or create comments without a separate approval path.

## Completion Criteria

- Preview names source page, block, database, or row IDs and sensitivity caveats.
- Relevant content is summarized with source provenance.
- Attachment or import approval remains separate from the preview.

## Human Decision Points

- Approve selected page, block, database, and row context before attaching it to project or task state.
- Approve duplicate handling and target mapping.

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `selected_notion_scope` | Selected Notion Scope | `json` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `notion_context_preview` | Notion Context Preview | `richtext` | no |
| `target_context_mapping` | Target Context Mapping | `json` | no |

## Routing

- Source template: `alludium/task-definition-templates/vc-integrations/notion-sync-read.yaml`
- Alludium task ID: `vc.notion_sync_read`
- Task family: `integration_sync_read`
- Recommended agent: `vc-integration-operator` (Alludium template `vc_integration_operator`)
- Supported project types:
  - `vc_deal_room`
- Supported project scopes:
  - `project_management`

## Required Skills

- `vc-notion-sync-read`
- `citation-enforcement`
