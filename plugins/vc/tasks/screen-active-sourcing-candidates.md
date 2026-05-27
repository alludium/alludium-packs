---
id: vc.screen_active_sourcing_candidates
title: Screen Active Sourcing Candidate
slug: screen-active-sourcing-candidates
agent: vc-sourcing-operator
skills:
- vc-sourcing-verdict-and-screening
- citation-enforcement
- investment-screening-framework
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/screen-active-sourcing-candidates.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Screen Active Sourcing Candidate

Run an origination-specific thesis screen on active Meet, IC-Summary, or Reach out candidates.

## Instructions

Screen active origination candidates using the reference pipeline's fast thesis filter rather than the downstream Deal Pipeline first-look task. Assess stage, geography, enterprise software, AI-native depth, named buyer, moat, and founder balance. Return PROCEED_TO_IC, DIG_FURTHER, or PASS and map those to review actions without downgrading protected manual decisions. Use `definitionJson.documentRefs` as the durable document reference contract. Apply each reference by usage: `output_template` sets the output skeleton, `methodology` supplies scoring or analysis logic, `checklist` must be completed with status, evidence, and owner, `style_guide` governs citations and claim language, and `operating_guidance` or `policy` constrains process and approval boundaries. For refs with `outputFieldKey`, produce that output from the referenced pack document and preserve the document ID alongside the output artifact.

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

## Document References

- `vc.document.sourcing_scoring_rubric` (methodology) -> `screening_artifact_id`
- `vc.document.origination_source_strategy_guide` (methodology)
- `vc.document.dedupe_novelty_policy` (policy)
- `vc.document.template_use_guidance` (operating_guidance)

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/screen-active-sourcing-candidates.yaml`
- Alludium task ID: `vc.screen_active_sourcing_candidates`
- Task family: `origination_screening`
- Lifecycle stage: `review`
- Recommended agent: `vc-sourcing-operator` (Alludium template `vc_sourcing_operator`)
- Supported project types:
  - `vc_origination_pipeline`
- Supported project scopes:
  - `project_instance`

## Required Skills

- `vc-sourcing-verdict-and-screening`
- `citation-enforcement`
- `investment-screening-framework`
