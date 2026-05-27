---
id: vc.prepare_second_reachout_email
title: Prepare Second Reachout Email
slug: prepare-second-reachout-email
agent: vc-sourcing-operator
skills:
- vc-outreach-draft-queue
- founder-outreach-and-intro-paths
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/prepare-second-reachout-email.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Prepare Second Reachout Email

Draft a second-touch email for candidates with LinkedIn outreach sent and no response after the configured wait period.

## Instructions

Draft a second-touch email only for candidates with a recorded LinkedIn reachout, no reply, and an approved wait period. Use one concrete hook and a simple call request. Treat the email as a draft artifact only; do not send email, set outreach status, or mutate external CRM/list stages without explicit human approval. Use `definitionJson.documentRefs` as the durable document reference contract. Apply each reference by usage: `output_template` sets the output skeleton, `methodology` supplies scoring or analysis logic, `checklist` must be completed with status, evidence, and owner, `style_guide` governs citations and claim language, and `operating_guidance` or `policy` constrains process and approval boundaries. For refs with `outputFieldKey`, produce that output from the referenced pack document and preserve the document ID alongside the output artifact.

## Missing Input Policy

Ask for the prior LinkedIn reachout record, no-response date/window, founder email or email-finding policy, candidate evidence, and approved sender before drafting.

## External Action Policy

Draft only. Sending email, updating Outreach Status, and moving CRM stages require explicit human approval.

## Completion Criteria

- Email draft includes subject, body, evidence hook, recipient, prior-reachout reference, and no-response timing.
- Draft explains whether the candidate should remain active, move to no-response, watchlist, pass, or engaged outcome review.
- No external send or status mutation occurs without explicit approval.

## Human Decision Points

- None declared

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `second_reachout_scope` | Second Reachout Scope | `json` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `second_reachout_email_artifact_id` | Second Reachout Email Artifact | `file` | yes |
| `second_reachout_draft_count` | Second Reachout Draft Count | `number` | no |
| `second_reachout_summary` | Second Reachout Summary | `richtext` | no |

## Document References

- `vc.document.outreach_queue_template` (output_template) -> `second_reachout_email_artifact_id`
- `vc.document.origination_source_strategy_guide` (methodology)
- `vc.document.template_use_guidance` (operating_guidance)

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/prepare-second-reachout-email.yaml`
- Alludium task ID: `vc.prepare_second_reachout_email`
- Task family: `origination_outreach_drafts`
- Lifecycle stage: `second_reachout_email`
- Recommended agent: `vc-sourcing-operator` (Alludium template `vc_sourcing_operator`)
- Supported project types:
  - `vc_origination_pipeline`
- Supported project scopes:
  - `project_instance`

## Required Skills

- `vc-outreach-draft-queue`
- `founder-outreach-and-intro-paths`
- `citation-enforcement`
