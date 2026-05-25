---
id: vc.discover_github_builder_signals
title: Discover GitHub Builder Signals
slug: discover-github-builder-signals
agent: vc-sourcing-operator
skills:
- vc-github-builder-signal-discovery
- vc-source-registry-and-state-management
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/discover-github-builder-signals.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Discover GitHub Builder Signals

Discover UK/Ireland technical-founder and AI repository signals using the reference pipeline's two-pass GitHub model.

## Instructions

Mirror the reference pipeline's two-pass GitHub approach. Pass 1 searches users by UK/Ireland city/location and reviews their recently-created repositories. Pass 2 searches AI/LLM/agentic repository topics and descriptions, then checks owner profile location and README/product evidence. Score UK signal, B2B/enterprise language, AI keyword depth, serious topics, stars-per-day traction, homepage/contact signals, README pricing/CTA, and founder profile evidence.

## Missing Input Policy

Ask for GitHub access, lookback window, approved topics/keywords, location scope, rate-limit policy, and seen repo/user state.

## External Action Policy

Public/source read only. Do not open issues, star repos, contact maintainers, import candidates, or sync external records without a separate approved task.

## Completion Criteria

- Candidate preview includes repository URL, owner, created date, stars, topics, language, founder/location evidence, score reasons, and source receipt.
- Source-state update includes full_name or repo ID dedupe, seen repo IDs, seen user logins, and rate-limit notes.

## Human Decision Points

- None declared

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `github_discovery_scope` | GitHub Discovery Scope | `json` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `github_discovery_artifact_id` | GitHub Discovery Artifact | `file` | yes |
| `discovery_report` | Discovery Report | `richtext` | no |
| `source_result_count` | Source Result Count | `number` | no |
| `source_state_summary` | Source State Summary | `string` | no |

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/discover-github-builder-signals.yaml`
- Alludium task ID: `vc.discover_github_builder_signals`
- Task family: `origination_source_discovery`
- Lifecycle stage: `source`
- Recommended agent: `vc-sourcing-operator` (Alludium template `vc_sourcing_operator`)
- Supported project types:
  - `vc_origination_pipeline`
- Supported project scopes:
  - `project_instance`

## Required Skills

- `vc-github-builder-signal-discovery`
- `vc-source-registry-and-state-management`
- `citation-enforcement`
