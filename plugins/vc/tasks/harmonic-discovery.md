---
id: vc.harmonic_discovery
title: Explore Harmonic Source Scopes
slug: harmonic-discovery
agent: vc-origination-scout
skills:
- vc-harmonic-discovery
- citation-enforcement
---

<!-- Generated from alludium/task-definition-templates/vc-integrations/harmonic-discovery.yaml; do not edit directly. Run python plugins/vc/scripts/generate_markdown.py after changing the YAML source. -->

# Explore Harmonic Source Scopes

Discover Harmonic saved searches, daily searches, and source scope before selected VC sourcing context reads.

## Instructions

Use the connected `harmonic-mcp-oauth` application only after tool discovery has produced live tool rows. The current local platform catalog has the Harmonic OAuth application and connection template but no trusted Harmonic tool external IDs, so report missing tool discovery explicitly if no tools are available. When tools are discovered, enumerate saved searches, daily searches, or comparable source scopes and ask the user to choose the sourcing scope before any read-sync task.

## Missing Input Policy

If Harmonic is not authorized or has no discovered tools, report the setup gap and ask for authorization/tool discovery or a supplied saved-search inventory.

## External Action Policy

Discovery only. Do not process company results, mark search results as seen, update saved searches, export contacts, enrich records, or write back to Harmonic.

## Completion Criteria

- Available Harmonic saved searches or source scopes are listed when tools exist.
- The report explicitly states whether trusted Harmonic tool IDs were discovered.
- User choices needed before result processing are explicit.

## Human Decision Points

- Choose saved search, daily search, or source scope before sync read.
- Approve whether net-new result processing is in scope.

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `discovery_goal` | Discovery Goal | `string` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `harmonic_discovery_report` | Harmonic Discovery Report | `richtext` | no |
| `source_scope_questions` | Source Scope Questions | `json` | no |

## Routing

- Source template: `alludium/task-definition-templates/vc-integrations/harmonic-discovery.yaml`
- Alludium task ID: `vc.harmonic_discovery`
- Task family: `integration_discovery`
- Recommended agent: `vc-origination-scout` (Alludium template `vc_origination_scout`)
- Supported project types:
  - `vc_deal_room`
- Supported project scopes:
  - `project_management`

## Required Skills

- `vc-harmonic-discovery`
- `citation-enforcement`

## Planned Skills

- `vc-harmonic-discovery`
- `citation-enforcement`
