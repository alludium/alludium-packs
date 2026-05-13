---
id: vc.discover_reddit_builder_signals
title: Discover Reddit Builder Signals
slug: discover-reddit-builder-signals
agent: vc-origination-scout
skills:
- vc-reddit-builder-signal-discovery
- vc-source-registry-and-state-management
- citation-enforcement
---

# Discover Reddit Builder Signals

Discover public Reddit builder posts that may indicate early AI startup candidates.

## Instructions

Mirror the reference pipeline's Reddit approach against approved public communities and terms. Look for first-person build, launch, beta, pre-seed, early-user, AI/LLM, and B2B signals. Reject advice questions, job posts, hiring posts, rants, freelancing income posts, pure academic posts without product signal, and non-self posts. Preserve post ID as the dedupe key.

## Missing Input Policy

Ask for approved subreddits, query terms, lookback window, minimum score, rate-limit policy, and seen post state.

## External Action Policy

Public read and inbox proposal only. Do not comment, message, import into the main candidate queue, or sync externally without separate approval.

## Completion Criteria

- Candidate preview includes Reddit URL, subreddit, author, extracted company/product, website if visible, UK signal, score reasons, and source receipt.
- Source-state update includes seen post IDs and rejected/noise counts.

## Human Decision Points

- None declared

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `reddit_discovery_scope` | Reddit Discovery Scope | `json` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `reddit_discovery_artifact_id` | Reddit Discovery Artifact | `file` | yes |
| `discovery_report` | Discovery Report | `richtext` | no |
| `source_result_count` | Source Result Count | `number` | no |
| `source_state_summary` | Source State Summary | `string` | no |

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/discover-reddit-builder-signals.yaml`
- Alludium task ID: `vc.discover_reddit_builder_signals`
- Task family: `origination_source_discovery`
- Lifecycle stage: `source`
- Recommended agent: `vc-origination-scout` (Alludium template `vc_origination_scout`)
- Supported project types:
  - `vc_origination_pipeline`
- Supported project scopes:
  - `project_instance`

## Required Skills

- `vc-reddit-builder-signal-discovery`
- `vc-source-registry-and-state-management`
- `citation-enforcement`

## Planned Skills

- `vc-reddit-builder-signal-discovery`
- `vc-source-registry-and-state-management`
- `citation-enforcement`
