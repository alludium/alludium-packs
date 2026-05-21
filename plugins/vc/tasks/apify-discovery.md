---
id: vc.apify_discovery
title: Explore Apify Origination Sources
slug: apify-discovery
agent: vc-origination-scout
skills:
- vc-apify-discovery
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-integrations/apify-discovery.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Explore Apify Origination Sources

Discover approved Apify actors, input schemas, source scope, and run-cost guardrails before any VC origination read preview.

## Instructions

Use the connected `apify-actors-mcp` application only after authorization and tool discovery. Enumerate approved actors, input requirements, estimated cost controls, and safe sample-read options. If live tools are not available, produce the missing-tool discovery checklist and ask for an approved actor inventory instead of inventing actor IDs.

## Missing Input Policy

Ask for authorization, actor allowlist, source policy, or supplied actor inventory when live discovery is unavailable.

## External Action Policy

Discovery only. Do not start actor runs, import candidates, persist candidate state, score candidates, contact founders, update external systems, or create Deal Room projects.

## Completion Criteria

- Available or supplied Apify actors are listed with source purpose and read-preview requirements.
- Tool discovery status and any missing authorization are explicit.
- User choices needed before sync read are explicit.

## Human Decision Points

- Choose approved actors and source policy before sync read.
- Approve sample-run budget and result scope separately.

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `discovery_goal` | Discovery Goal | `string` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `apify_discovery_report` | Apify Discovery Report | `richtext` | no |
| `source_scope_questions` | Source Scope Questions | `json` | no |

## Routing

- Source template: `alludium/task-definition-templates/vc-integrations/apify-discovery.yaml`
- Alludium task ID: `vc.apify_discovery`
- Task family: `integration_discovery`
- Recommended agent: `vc-origination-scout` (Alludium template `vc_origination_scout`)
- Supported project types:
  - `vc_origination_pipeline`
- Supported project scopes:
  - `project_management`

## Required Skills

- `vc-apify-discovery`
- `citation-enforcement`
