---
id: vc.apify_sync_read
title: Preview Apify Origination Results
slug: apify-sync-read
agent: vc-integration-operator
skills:
- vc-apify-sync-read
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-integrations/apify-sync-read.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Preview Apify Origination Results

Preview selected Apify actor results before using them as VC origination source context.

## Instructions

Build a read preview only after discovery has selected approved actors, input scope, budget limits, and result limits. Process only selected sample results and return identity signals, source receipts, cost/run metadata when available, and suggested mapping into the origination source registry.

## Missing Input Policy

Ask for selected actors, approved input scope, run/result limits, and discovered tool IDs before processing actor output.

## External Action Policy

Read preview only. Do not enable scheduled runs, import candidates, write candidate records, score candidates, contact founders, update external systems, or create Deal Pipeline projects.

## Completion Criteria

- Preview rows include actor/source IDs, candidate identity signals, source receipts, and rejection reasons when available.
- Run IDs, dataset IDs, cost metadata, or missing metadata are named.
- Import, recurring monitoring, scoring, outreach, and promotion approvals remain separate from the preview.

## Human Decision Points

- Approve sample results before candidate import or scoring.
- Approve source registry mappings and dedupe keys separately.

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `selected_apify_scope` | Selected Apify Scope | `json` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `apify_results_preview` | Apify Results Preview | `richtext` | no |
| `source_registry_mapping` | Source Registry Mapping | `json` | no |

## Routing

- Source template: `alludium/task-definition-templates/vc-integrations/apify-sync-read.yaml`
- Alludium task ID: `vc.apify_sync_read`
- Task family: `integration_sync_read`
- Recommended agent: `vc-integration-operator` (Alludium template `vc_integration_operator`)
- Supported project types:
  - `vc_origination_pipeline`
- Supported project scopes:
  - `project_management`

## Required Skills

- `vc-apify-sync-read`
- `citation-enforcement`
