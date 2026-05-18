---
id: vc.generate_sourcing_digest
title: Generate Sourcing Digest
slug: generate-sourcing-digest
agent: vc-pipeline-autopilot
skills:
- vc-sourcing-digest-generation
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/generate-sourcing-digest.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Generate Sourcing Digest

Generate a daily or weekly origination digest with candidates, run receipts, degraded sources, and pending approvals.

## Instructions

Produce a reference-pipeline-style digest of new Meet/Watch and active candidates, source counts, run failures, budget/cost notes, and review actions. The default destination is a reviewable digest object; posting to Slack, ClickUp, email, or another external channel requires a separately approved write-capable task. Use `definitionJson.documentRefs` as the durable document reference contract; for refs with `outputFieldKey`, produce that output using the referenced pack document ID as the template or methodology source, and preserve the document ID alongside the output artifact.

## Missing Input Policy

Ask for run receipt, candidate batch, digest channel, audience, and whether this is daily, weekly, or monthly.

## External Action Policy

Draft digest only unless explicit channel-post approval is granted.

## Completion Criteria

- Digest groups candidates by action, urgency, source, and owner/review need.
- Run receipt, cost/budget notes, degraded-source warnings, and pending approvals are included.

## Human Decision Points

- None declared

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `digest_scope` | Digest Scope | `json` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `sourcing_digest_artifact_id` | Sourcing Digest Artifact | `file` | yes |
| `digest_status` | Digest Status | `string` | no |
| `sourcing_digest` | Sourcing Digest | `richtext` | no |

## Document References

- `vc.document.sourcing_digest_template` (output_template) -> `sourcing_digest_artifact_id`

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/generate-sourcing-digest.yaml`
- Alludium task ID: `vc.generate_sourcing_digest`
- Task family: `origination_digest`
- Lifecycle stage: `operate`
- Recommended agent: `vc-pipeline-autopilot` (Alludium template `vc_pipeline_autopilot`)
- Supported project types:
  - `vc_origination_pipeline`
- Supported project scopes:
  - `project_instance`

## Required Skills

- `vc-sourcing-digest-generation`
- `citation-enforcement`

## Planned Skills

- `vc-sourcing-digest-generation`
- `citation-enforcement`
