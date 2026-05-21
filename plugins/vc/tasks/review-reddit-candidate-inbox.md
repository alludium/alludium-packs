---
id: vc.review_reddit_candidate_inbox
title: Review Reddit Candidate Inbox
slug: review-reddit-candidate-inbox
agent: vc-origination-scout
skills:
- vc-reddit-inbox-approval
- vc-sourcing-dedupe-and-novelty-check
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/review-reddit-candidate-inbox.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Review Reddit Candidate Inbox

Review Reddit discovery inbox rows and prepare approved candidates for enrichment.

## Instructions

Review public Reddit candidate inbox rows before they enter the main candidate flow. Approve only rows with first-person builder/founder evidence, durable company or product identity, and thesis-relevant signal. Prepare approved rows for enrichment; keep uncertain rows in review and reject noise with reasons.

## Missing Input Policy

Ask for Reddit inbox rows, raw source receipts, approval policy, and dedupe state.

## External Action Policy

Approval proposal only unless explicit write approval is granted. Do not mark rows pushed, comment, message users, or sync externally.

## Completion Criteria

- Approved, rejected, and needs-review rows are separated with reasons and receipts.
- Approved rows include dedupe keys and enrichment-ready fields.

## Human Decision Points

- None declared

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `reddit_inbox_scope` | Reddit Inbox Scope | `json` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `reddit_inbox_review_artifact_id` | Reddit Inbox Review Artifact | `file` | yes |
| `approved_candidate_count` | Approved Candidate Count | `number` | no |
| `needs_review_count` | Needs Review Count | `number` | no |
| `review_report` | Review Report | `richtext` | no |

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/review-reddit-candidate-inbox.yaml`
- Alludium task ID: `vc.review_reddit_candidate_inbox`
- Task family: `origination_reddit_approval`
- Lifecycle stage: `review`
- Recommended agent: `vc-origination-scout` (Alludium template `vc_origination_scout`)
- Supported project types:
  - `vc_origination_pipeline`
- Supported project scopes:
  - `project_instance`

## Required Skills

- `vc-reddit-inbox-approval`
- `vc-sourcing-dedupe-and-novelty-check`
- `citation-enforcement`
