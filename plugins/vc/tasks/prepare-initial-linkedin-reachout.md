---
id: vc.prepare_initial_linkedin_reachout
title: Prepare Initial LinkedIn Reachout
slug: prepare-initial-linkedin-reachout
agent: vc-sourcing-operator
skills:
- vc-outreach-draft-queue
- founder-outreach-and-intro-paths
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/prepare-initial-linkedin-reachout.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Prepare Initial LinkedIn Reachout

Draft the first LinkedIn message after a candidate has been approved for outbound engagement.

## Instructions

Draft the first LinkedIn reachout for approved of-interest candidates or connected founders. Use concrete candidate evidence, founder context, and the approved thesis angle. Keep the message short, specific, and question-led. Do not mark the reachout as sent, update CRM stages, or contact the founder without explicit human approval. Use `definitionJson.documentRefs` as the durable document reference contract. Apply each reference by usage: `output_template` sets the output skeleton, `methodology` supplies scoring or analysis logic, `checklist` must be completed with status, evidence, and owner, `style_guide` governs citations and claim language, and `operating_guidance` or `policy` constrains process and approval boundaries. For refs with `outputFieldKey`, produce that output from the referenced pack document and preserve the document ID alongside the output artifact.

## Missing Input Policy

Ask for the approved candidate, founder LinkedIn URL, connection state, thesis angle, source evidence, and outreach tone policy before drafting.

## External Action Policy

Draft only. Sending LinkedIn messages, updating CRM stages, and changing outbound status require explicit human approval.

## Completion Criteria

- Draft includes founder, company, profile URL, message text, evidence hook, owner, and skip reason where applicable.
- Message is concise, specific, and anchored to cited candidate evidence.
- Send and CRM mutation boundaries are explicit.

## Human Decision Points

- None declared

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `initial_reachout_scope` | Initial Reachout Scope | `json` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `initial_linkedin_reachout_artifact_id` | Initial LinkedIn Reachout Artifact | `file` | yes |
| `initial_reachout_draft_count` | Initial Reachout Draft Count | `number` | no |
| `initial_reachout_summary` | Initial Reachout Summary | `richtext` | no |

## Document References

- `vc.document.outreach_queue_template` (output_template) -> `initial_linkedin_reachout_artifact_id`
- `vc.document.origination_source_strategy_guide` (methodology)
- `vc.document.template_use_guidance` (operating_guidance)

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/prepare-initial-linkedin-reachout.yaml`
- Alludium task ID: `vc.prepare_initial_linkedin_reachout`
- Task family: `origination_outreach_drafts`
- Lifecycle stage: `initial_reachout_linkedin`
- Recommended agent: `vc-sourcing-operator` (Alludium template `vc_sourcing_operator`)
- Supported project types:
  - `vc_origination_pipeline`
- Supported project scopes:
  - `project_instance`

## Required Skills

- `vc-outreach-draft-queue`
- `founder-outreach-and-intro-paths`
- `citation-enforcement`
