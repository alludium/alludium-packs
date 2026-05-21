---
id: vc.ingest_manual_sourcing_tip
title: Ingest Manual Sourcing Tip
slug: ingest-manual-sourcing-tip
agent: vc-origination-scout
skills:
- vc-manual-tip-ingestion
- vc-sourcing-dedupe-and-novelty-check
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/ingest-manual-sourcing-tip.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Ingest Manual Sourcing Tip

Normalize a manually submitted company or founder lead into the origination candidate model.

## Instructions

Mirror the reference pipeline's manual-tip ingestion by normalizing supplied company, founder, website, LinkedIn, note, and source context into the candidate schema, assigning a stable manual-tip key, setting source and discovery mode, and sending the candidate through enrichment and scoring rather than directly promoting it.

## Missing Input Policy

Ask for company or founder identity, source of tip, website or profile URL, submitter, and confidence if missing.

## External Action Policy

Internal candidate normalization only. Do not contact founders, write CRM records, or create Deal Rooms.

## Completion Criteria

- Manual tip candidate has stable key, source, submitter/source receipt, identity fields, dedupe decision, and next-step recommendation.

## Human Decision Points

- None declared

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `manual_tip` | Manual Tip | `json` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `manual_tip_ingestion_artifact_id` | Manual Tip Ingestion Artifact | `file` | yes |
| `normalized_candidate_key` | Normalized Candidate Key | `string` | no |
| `ingestion_report` | Ingestion Report | `richtext` | no |

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/ingest-manual-sourcing-tip.yaml`
- Alludium task ID: `vc.ingest_manual_sourcing_tip`
- Task family: `origination_manual_tip`
- Lifecycle stage: `source`
- Recommended agent: `vc-origination-scout` (Alludium template `vc_origination_scout`)
- Supported project types:
  - `vc_origination_pipeline`
- Supported project scopes:
  - `project_instance`

## Required Skills

- `vc-manual-tip-ingestion`
- `vc-sourcing-dedupe-and-novelty-check`
- `citation-enforcement`
