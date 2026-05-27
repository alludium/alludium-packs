---
id: vc.discover_x_founder_signals
title: Discover X Founder Signals
slug: discover-x-founder-signals
agent: vc-sourcing-operator
skills:
- vc-apify-x-founder-discovery
- vc-source-registry-and-state-management
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/discover-x-founder-signals.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Discover X Founder Signals

Find public founder/product/building signals on X through approved Apify tweet-search actors.

## Instructions

Use approved X/Twitter actor scope only. Mirror the reference pipeline's target pattern for build-in-public, first-person launch/building language, AI/LLM/product terms, UK/Ireland location signals, B2B/enterprise hints, product URLs, engagement, and founder-author evidence. Reject media, VC, newsletter, aggregator, and third-party news accounts.

## Missing Input Policy

Ask for approved search terms, lookback window, budget/result cap, actor authorization, and seen-tweet state before discovery.

## External Action Policy

Public-signal read and candidate proposal only. Do not engage authors, import candidates, sync to external systems, or create Deal Pipelines.

## Completion Criteria

- Candidate preview includes tweet URL, author handle, founder/company identity, product URL, location signal, score reasons, and source receipt.
- Source-state update includes seen tweet IDs and rejected/noise counts.
- Cost/run metadata or missing cost metadata is explicit.

## Human Decision Points

- None declared

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `x_discovery_scope` | X Discovery Scope | `json` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `x_founder_discovery_artifact_id` | X Founder Discovery Artifact | `file` | yes |
| `discovery_report` | Discovery Report | `richtext` | no |
| `source_result_count` | Source Result Count | `number` | no |
| `source_state_summary` | Source State Summary | `string` | no |

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/discover-x-founder-signals.yaml`
- Alludium task ID: `vc.discover_x_founder_signals`
- Task family: `origination_source_discovery`
- Lifecycle stage: `source`
- Recommended agent: `vc-sourcing-operator` (Alludium template `vc_sourcing_operator`)
- Supported project types:
  - `vc_origination_pipeline`
- Supported project scopes:
  - `project_instance`

## Required Skills

- `vc-apify-x-founder-discovery`
- `vc-source-registry-and-state-management`
- `citation-enforcement`
