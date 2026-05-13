---
id: vc.screen_active_sourcing_candidates
title: Screen Active Sourcing Candidates
slug: screen-active-sourcing-candidates
agent: vc-first-look-analyst
skills:
- vc-sourcing-verdict-and-screening
- citation-enforcement
---

# Screen Active Sourcing Candidates

Run an origination-specific thesis screen on active Meet, IC-Summary, or Reach out candidates.

## Instructions

Screen active origination candidates using the reference pipeline's fast thesis filter rather than the downstream Deal Room first-look task. Assess stage, geography, enterprise software, AI-native depth, named buyer, moat, and founder balance. Return PROCEED_TO_IC, DIG_FURTHER, or PASS and map those to review actions without downgrading protected manual decisions.

## Missing Input Policy

Ask for active candidate batch, current manual actions, thesis policy, protected-action list, and approved write mode before screening.

## External Action Policy

Screening recommendation only unless explicit write approval is granted. Never downgrade protected manual decisions such as IC-Summary or Pass.

## Completion Criteria

- Each screened candidate has thesis pillar statuses, key signals, verdict, verdict reason, protected-action handling, and receipts.
- Manual decision preservation is explicit.

## Human Decision Points

- None declared

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `screening_scope` | Screening Scope | `json` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `screening_artifact_id` | Screening Artifact | `file` | yes |
| `promotion_ready_count` | Promotion Ready Count | `number` | no |
| `screening_report` | Screening Report | `richtext` | no |

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/screen-active-sourcing-candidates.yaml`
- Alludium task ID: `vc.screen_active_sourcing_candidates`
- Task family: `origination_screening`
- Lifecycle stage: `review`
- Recommended agent: `vc-first-look-analyst` (Alludium template `vc_first_look_analyst`)
- Supported project types:
  - `vc_origination_pipeline`
- Supported project scopes:
  - `project_instance`

## Required Skills

- `vc-sourcing-verdict-and-screening`
- `citation-enforcement`

## Planned Skills

- `vc-sourcing-verdict-and-screening`
- `ten-factor-evaluation`
- `citation-enforcement`
