---
id: vc.review_outreach_outcome
title: Review Outreach Outcome
slug: review-outreach-outcome
agent: vc-sourcing-operator
skills:
- vc-origination-deal-room-promotion
- vc-outreach-draft-queue
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/review-outreach-outcome.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Review Outreach Outcome

Classify outbound outcomes after LinkedIn and email attempts into no response, engaged, pass, or watchlist.

## Instructions

Review the latest outreach state, response evidence, CRM/list context, and candidate screening artifacts. Recommend one outcome: no response, engaged and ready to add to the Deal Pipeline, pass, or watchlist. If engaged, prepare the promotion handoff context but do not create a Deal Pipeline or mutate CRM/list stages without explicit human approval. Use `definitionJson.documentRefs` as the durable document reference contract. Apply each reference by usage: `output_template` sets the output skeleton, `methodology` supplies scoring or analysis logic, `checklist` must be completed with status, evidence, and owner, `style_guide` governs citations and claim language, and `operating_guidance` or `policy` constrains process and approval boundaries. For refs with `outputFieldKey`, produce that output from the referenced pack document and preserve the document ID alongside the output artifact.

## Missing Input Policy

Ask for outreach history, response evidence, latest screening artifact, owner decision policy, and target system before classifying.

## External Action Policy

Review and recommendation only. Deal Pipeline creation, CRM stage changes, pass/watchlist updates, and notifications require explicit human approval.

## Completion Criteria

- Outcome recommendation is one of no_response, engaged_added_to_deal_funnel, pass, or watchlist.
- Recommendation cites outreach evidence, response state, and screening rationale.
- Engaged outcomes include promotion readiness and unresolved blockers.

## Human Decision Points

- None declared

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `outreach_state` | Outreach State | `json` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `outreach_outcome_artifact_id` | Outreach Outcome Artifact | `file` | yes |
| `recommended_terminal_state` | Recommended Terminal State | `string` | yes |
| `outreach_outcome_summary` | Outreach Outcome Summary | `richtext` | no |

## Document References

- `vc.document.promotion_package_template` (output_template) -> `outreach_outcome_artifact_id`
- `vc.document.origination_source_strategy_guide` (methodology)
- `vc.document.template_use_guidance` (operating_guidance)

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/review-outreach-outcome.yaml`
- Alludium task ID: `vc.review_outreach_outcome`
- Task family: `origination_outbound_state`
- Lifecycle stage: `outbound_outcome`
- Recommended agent: `vc-sourcing-operator` (Alludium template `vc_sourcing_operator`)
- Supported project types:
  - `vc_origination_pipeline`
- Supported project scopes:
  - `project_instance`

## Required Skills

- `vc-origination-deal-room-promotion`
- `vc-outreach-draft-queue`
- `citation-enforcement`
