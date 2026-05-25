---
id: vc.harmonic_sync_read
title: Preview Harmonic Search Results
slug: harmonic-sync-read
agent: vc-integration-operator
skills:
- vc-harmonic-sync-read
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-integrations/harmonic-sync-read.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Preview Harmonic Search Results

Preview selected Harmonic company or saved-search results before using them as VC sourcing or screening context.

## Instructions

Build a Harmonic read preview only after discovery has selected a saved search, daily search, company, or result scope and live tool IDs are known. The current local platform catalog has no trusted Harmonic tool rows, so treat live reads as blocked until tool discovery after authorization succeeds. When tools exist, process only selected company/search results and propose target mapping as sourcing context, task context, watchlist candidates, or Deal Room setup context.

## Missing Input Policy

Ask for selected Harmonic source scope and discovered tool IDs before processing search results.

## External Action Policy

Read preview only. Do not create Deal Rooms, import companies, mark net-new results as seen, update saved searches, export contacts, or write back to Harmonic.

## Completion Criteria

- Preview rows include Harmonic source IDs, company/person identity signals, relevance notes, and rejection reasons when available.
- Tool IDs used or missing are named.
- Import, watchlist creation, or recurring monitoring approval remains separate from the preview.

## Human Decision Points

- Approve result rows before importing or attaching context.
- Approve dedupe decisions and target mappings.

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `selected_harmonic_scope` | Selected Harmonic Scope | `json` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `harmonic_results_preview` | Harmonic Results Preview | `richtext` | no |
| `target_context_mapping` | Target Context Mapping | `json` | no |

## Routing

- Source template: `alludium/task-definition-templates/vc-integrations/harmonic-sync-read.yaml`
- Alludium task ID: `vc.harmonic_sync_read`
- Task family: `integration_sync_read`
- Recommended agent: `vc-integration-operator` (Alludium template `vc_integration_operator`)
- Supported project types:
  - `vc_deal_room`
- Supported project scopes:
  - `project_management`

## Required Skills

- `vc-harmonic-sync-read`
- `citation-enforcement`
