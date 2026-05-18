---
id: vc.prepare_outreach_draft_queue
title: Prepare Outreach Draft Queue
slug: prepare-outreach-draft-queue
agent: vc-dealflow-concierge
skills:
- vc-outreach-draft-queue
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/prepare-outreach-draft-queue.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Prepare Outreach Draft Queue

Draft founder outreach notes for active candidates while leaving send decisions to humans.

## Instructions

Mirror the reference pipeline's outreach draft policy. Draft only for candidates with active actions such as Meet, IC-Summary, or Reach out, no manual Status/contact progress, and a founder LinkedIn URL. Produce short, specific, question-led LinkedIn connection notes tied to evidence. Skip weak hooks instead of fabricating personalization.

## Missing Input Policy

Ask for active candidate batch, founder profile URL, eligible actions, manual-contact status, outreach tone policy, and destination for drafts.

## External Action Policy

Draft only. Do not send messages, insert browser-extension notes, mark outreach as sent, or update external systems without explicit human approval.

## Completion Criteria

- Draft queue includes founder, profile URL, note, angle, strength, skip reason, and source evidence.
- Notes are short, question-led, specific, and free of unsupported praise or editorializing.
- Send remains a human action.

## Human Decision Points

- None declared

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `outreach_scope` | Outreach Scope | `json` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `outreach_queue_artifact_id` | Outreach Queue Artifact | `file` | yes |
| `outreach_draft_count` | Outreach Draft Count | `number` | no |
| `outreach_report` | Outreach Report | `richtext` | no |

## Document References

- `vc.document.outreach_queue_template` (output_template) -> `outreach_queue_artifact_id`

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/prepare-outreach-draft-queue.yaml`
- Alludium task ID: `vc.prepare_outreach_draft_queue`
- Task family: `origination_outreach_drafts`
- Lifecycle stage: `engage`
- Recommended agent: `vc-dealflow-concierge` (Alludium template `vc_dealflow_concierge`)
- Supported project types:
  - `vc_origination_pipeline`
- Supported project scopes:
  - `project_instance`

## Required Skills

- `vc-outreach-draft-queue`
- `citation-enforcement`

## Planned Skills

- `vc-outreach-draft-queue`
- `founder-outreach-and-intro-paths`
- `citation-enforcement`
