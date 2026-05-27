---
id: vc.enrich_sourcing_candidates
title: Enrich Sourcing Candidates
slug: enrich-sourcing-candidates
agent: vc-sourcing-operator
skills:
- vc-sourcing-candidate-enrichment
- vc-sourcing-dedupe-and-novelty-check
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/enrich-sourcing-candidates.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Enrich Sourcing Candidates

Normalize and enrich candidate records with web, LinkedIn, founder, website, and evidence context before scoring.

## Instructions

Enrich only candidates above the configured source-specific floor. Preserve the reference pipeline separation between cheap enrichment and LLM verdict by first gathering search results, website, company LinkedIn URL, founder LinkedIn URLs, founder profile evidence, and receipts; do not make final Meet/Watch/Pass judgments in this task. For LinkedIn-sourced rows, reuse pre-verified founder/company LinkedIn URLs rather than re-searching them.

## Missing Input Policy

Ask for candidate batch, enrichment budget, approved search/extraction tools, dedupe state, and minimum source score before enriching.

## External Action Policy

Read/enrich only. Do not write CRM rows, create Notion pages, score final verdicts, contact founders, or create Deal Pipelines.

## Completion Criteria

- Enriched candidates include normalized identity, source key, website, company LinkedIn, founder LinkedIn evidence, search snippets, receipts, and missing-data flags.
- Dedupe decisions include company-number, LinkedIn slug, domain, name, repo, post, or tweet keys as applicable.
- Errors and skipped rows are listed with retry guidance.

## Human Decision Points

- None declared

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `candidate_batch` | Candidate Batch | `json` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `enrichment_artifact_id` | Enrichment Artifact | `file` | yes |
| `enriched_candidate_count` | Enriched Candidate Count | `number` | no |
| `enrichment_status` | Enrichment Status | `string` | no |
| `enrichment_report` | Enrichment Report | `richtext` | no |

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/enrich-sourcing-candidates.yaml`
- Alludium task ID: `vc.enrich_sourcing_candidates`
- Task family: `origination_enrichment`
- Lifecycle stage: `enrich`
- Recommended agent: `vc-sourcing-operator` (Alludium template `vc_sourcing_operator`)
- Supported project types:
  - `vc_origination_pipeline`
- Supported project scopes:
  - `project_instance`

## Required Skills

- `vc-sourcing-candidate-enrichment`
- `vc-sourcing-dedupe-and-novelty-check`
- `citation-enforcement`
