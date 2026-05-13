---
id: vc.promote_candidate_to_deal_room
title: Promote Candidate to Deal Room
slug: promote-candidate-to-deal-room
agent: vc-dealflow-concierge
skills:
- vc-origination-deal-room-promotion
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/promote-candidate-to-deal-room.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Promote Candidate to Deal Room

Prepare a reviewed promotion package for creating or updating a VC Deal Room from an approved origination candidate.

## Instructions

Promote only human-approved candidates. Prepare a Deal Room creation/update package with company identity, founder evidence, source receipts, enrichment/verdict/screen summaries, relationship context, outreach state, and open questions. Do not create or update the Deal Room unless the platform action is explicitly approved.

## Missing Input Policy

Ask for approved candidate, target Deal Room policy, promotion threshold evidence, owner, and required source artifacts.

## External Action Policy

Promotion package by default. Deal Room creation/update, CRM changes, document creation, and notifications require separate explicit approval.

## Completion Criteria

- Promotion package includes source receipts, candidate evidence, recommended initial Deal Room state, required tasks, owner, and unresolved risks.
- Human approval boundary for project creation/update is explicit.

## Human Decision Points

- None declared

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `promotion_candidate` | Promotion Candidate | `json` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `promotion_package_artifact_id` | Promotion Package Artifact | `file` | yes |
| `promoted_candidate_key` | Promoted Candidate Key | `string` | no |
| `promotion_summary` | Promotion Summary | `richtext` | no |

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/promote-candidate-to-deal-room.yaml`
- Alludium task ID: `vc.promote_candidate_to_deal_room`
- Task family: `origination_promotion`
- Lifecycle stage: `promote`
- Recommended agent: `vc-dealflow-concierge` (Alludium template `vc_dealflow_concierge`)
- Supported project types:
  - `vc_origination_pipeline`
- Supported project scopes:
  - `project_instance`

## Required Skills

- `vc-origination-deal-room-promotion`
- `citation-enforcement`

## Planned Skills

- `vc-origination-deal-room-promotion`
- `deal-room-setup-and-source-ingestion`
- `citation-enforcement`
