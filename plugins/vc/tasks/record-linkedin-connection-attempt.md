---
id: vc.record_linkedin_connection_attempt
title: Record LinkedIn Connection Attempt
slug: record-linkedin-connection-attempt
agent: vc-sourcing-operator
skills:
- vc-outreach-draft-queue
- founder-outreach-and-intro-paths
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/record-linkedin-connection-attempt.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Record LinkedIn Connection Attempt

Capture a human-approved LinkedIn connection attempt and update the outbound state without sending messages automatically.

## Instructions

Record only a connection attempt that a human has already approved or sent. Capture the founder profile, sent note, sent-at date, source candidate, destination CRM/list state, and any manual owner notes. Mirror the reference outbound pattern: the task may prepare an update plan for the outreach state, but it must not send a LinkedIn request, mutate CRM records, or mark outreach as sent without explicit human approval. Use `definitionJson.documentRefs` as the durable document reference contract. Apply each reference by usage: `output_template` sets the output skeleton, `methodology` supplies scoring or analysis logic, `checklist` must be completed with status, evidence, and owner, `style_guide` governs citations and claim language, and `operating_guidance` or `policy` constrains process and approval boundaries. For refs with `outputFieldKey`, produce that output from the referenced pack document and preserve the document ID alongside the output artifact.

## Missing Input Policy

Ask for the approved outreach target, LinkedIn profile URL, connection note, sent/approval status, owner, and destination system before recording.

## External Action Policy

Record and propose state updates only. Sending LinkedIn requests, setting CRM stages, or changing external status requires explicit human approval.

## Completion Criteria

- Connection attempt record includes target, founder profile URL, note, date, owner, and source candidate reference.
- Recommended next state distinguishes pending connection from ready-for-initial-LinkedIn-reachout.
- External writes and message sending remain explicitly human-controlled.

## Human Decision Points

- None declared

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `connection_attempt` | Connection Attempt | `json` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `connection_record_artifact_id` | Connection Record Artifact | `file` | yes |
| `outbound_status` | Outbound Status | `string` | no |
| `connection_record_summary` | Connection Record Summary | `richtext` | no |

## Document References

- `vc.document.outreach_queue_template` (output_template) -> `connection_record_artifact_id`
- `vc.document.template_use_guidance` (operating_guidance)

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/record-linkedin-connection-attempt.yaml`
- Alludium task ID: `vc.record_linkedin_connection_attempt`
- Task family: `origination_outbound_state`
- Lifecycle stage: `connecting_on_linkedin`
- Recommended agent: `vc-sourcing-operator` (Alludium template `vc_sourcing_operator`)
- Supported project types:
  - `vc_origination_pipeline`
- Supported project scopes:
  - `project_instance`

## Required Skills

- `vc-outreach-draft-queue`
- `founder-outreach-and-intro-paths`
- `citation-enforcement`
