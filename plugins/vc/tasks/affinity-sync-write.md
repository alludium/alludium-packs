---
id: vc.affinity_sync_write
title: Draft Affinity Write-Back Proposals
slug: affinity-sync-write
agent: vc-integration-operator
skills:
- vc-affinity-sync-write
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-integrations/affinity-sync-write.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Draft Affinity Write-Back Proposals

Draft reviewable Affinity note, field, and stage update proposals from VC task outputs.

## Instructions

Draft Affinity write-back proposals only. Each proposal must include the target Affinity object, before value, proposed after value or note text, source evidence, approving owner, and audit note. Reference `affinity_add_note` only as an approved execution tool if it is discovered and the runtime approval model is present.

## Missing Input Policy

Ask for the source artifact, target Affinity record, and approval owner before drafting a write-back proposal.

## External Action Policy

Draft only. Do not write notes, update fields, move stages, or change list entries.

## Completion Criteria

- Every proposal is evidence-backed and approval-gated.
- The output clearly states no Affinity writes were performed.

## Human Decision Points

- Approve exact write target and content.
- Approve CRM field or stage changes outside this task.

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `write_back_source` | Write-Back Source | `json` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `affinity_write_back_proposals` | Affinity Write-Back Proposals | `richtext` | no |

## Routing

- Source template: `alludium/task-definition-templates/vc-integrations/affinity-sync-write.yaml`
- Alludium task ID: `vc.affinity_sync_write`
- Task family: `integration_sync_write`
- Recommended agent: `vc-integration-operator` (Alludium template `vc_integration_operator`)
- Supported project types:
  - `vc_deal_room`
- Supported project scopes:
  - `project_management`

## Required Skills

- `vc-affinity-sync-write`
- `citation-enforcement`
