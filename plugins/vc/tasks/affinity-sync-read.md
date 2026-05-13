---
id: vc.affinity_sync_read
title: Preview Affinity Pipeline Import
slug: affinity-sync-read
agent: vc-pipeline-autopilot
skills:
- vc-affinity-sync-read
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-integrations/affinity-sync-read.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Preview Affinity Pipeline Import

Preview selected Affinity opportunity, company, person, note, and list-entry data before importing it into VC Deal Room context.

## Instructions

Build an Affinity read-sync preview from the approved list/source and stage scope. Use `affinity_get_list_entries`, `affinity_list_opportunities`, `affinity_get_opportunity`, `affinity_search_companies`, `affinity_get_company`, `affinity_search_persons`, `affinity_get_person`, and `affinity_list_company_notes` only inside approved scope. Show proposed project, field, task, artifact, and setup-context mappings before import.

## Missing Input Policy

Ask for the selected Affinity source scope before creating a preview.

## External Action Policy

Preview/import design only. Do not import records or enable recurring sync without explicit approval.

## Completion Criteria

- Preview rows include source IDs, target mappings, conflicts, and rejection reasons.
- Tool IDs used are named.
- Import approval remains separate from the preview.

## Human Decision Points

- Approve preview rows before import.
- Approve duplicate resolution and target mappings.

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `selected_affinity_scope` | Selected Affinity Scope | `json` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `affinity_import_preview` | Affinity Import Preview | `richtext` | no |
| `mapping_decisions` | Mapping Decisions | `json` | no |

## Routing

- Source template: `alludium/task-definition-templates/vc-integrations/affinity-sync-read.yaml`
- Alludium task ID: `vc.affinity_sync_read`
- Task family: `integration_sync_read`
- Recommended agent: `vc-pipeline-autopilot` (Alludium template `vc_pipeline_autopilot`)
- Supported project types:
  - `vc_deal_room`
- Supported project scopes:
  - `project_management`

## Required Skills

- `vc-affinity-sync-read`
- `citation-enforcement`

## Planned Skills

- `vc-affinity-sync-read`
- `citation-enforcement`
