---
id: vc.score_sourcing_candidates
title: Score Sourcing Candidates
slug: score-sourcing-candidates
agent: vc-sourcing-operator
skills:
- vc-sourcing-verdict-and-screening
- vc-sourcing-dedupe-and-novelty-check
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/score-sourcing-candidates.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Score Sourcing Candidates

Produce Meet/Watch/Pass verdicts and urgency scores for enriched origination candidates.

## Instructions

Mirror the reference pipeline's verdict contract. Score from already-enriched data, separate evidence from inference, and return Meet, Watch, or Pass plus urgency. Apply hard stage safety by passing companies with Series A+ funding or more than 20 employees when reliable LinkedIn company data is present. Run the second-pass verdict only for Meet/Watch rows with fresh LinkedIn company data so paid scraping and model cost stay bounded. Use `definitionJson.documentRefs` as the durable document reference contract. Apply each reference by usage: `output_template` sets the output skeleton, `methodology` supplies scoring or analysis logic, `checklist` must be completed with status, evidence, and owner, `style_guide` governs citations and claim language, and `operating_guidance` or `policy` constrains process and approval boundaries. For refs with `outputFieldKey`, produce that output from the referenced pack document and preserve the document ID alongside the output artifact.

## Missing Input Policy

Ask for enriched candidates, thesis, geography/stage policy, relationship context, LinkedIn company data availability, and scoring thresholds before scoring.

## External Action Policy

Scoring only. Do not sync external records, change manual decisions, send outreach, or create Deal Pipelines.

## Completion Criteria

- Each scored candidate has action, urgency, thesis fit, confidence, funding status, HQ/geography concern, frontier-pedigree evidence, reasons, and receipts.
- Auto-pass decisions name the specific rule and evidence.
- Second-pass rows are limited to candidates with fresh LinkedIn company data.

## Human Decision Points

- None declared

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `enriched_candidate_batch` | Enriched Candidate Batch | `json` | yes |
| `scoring_policy` | Scoring Policy | `json` | no |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `scoring_artifact_id` | Scoring Artifact | `file` | yes |
| `meet_candidate_count` | Meet Candidate Count | `number` | no |
| `watch_candidate_count` | Watch Candidate Count | `number` | no |
| `promotion_ready_count` | Promotion Ready Count | `number` | no |
| `scoring_report` | Scoring Report | `richtext` | no |

## Document References

- `vc.document.sourcing_scoring_rubric` (methodology) -> `scoring_artifact_id`
- `vc.document.origination_source_strategy_guide` (methodology)
- `vc.document.template_use_guidance` (operating_guidance)

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/score-sourcing-candidates.yaml`
- Alludium task ID: `vc.score_sourcing_candidates`
- Task family: `origination_scoring`
- Lifecycle stage: `score`
- Recommended agent: `vc-sourcing-operator` (Alludium template `vc_sourcing_operator`)
- Supported project types:
  - `vc_origination_pipeline`
- Supported project scopes:
  - `project_instance`

## Required Skills

- `vc-sourcing-verdict-and-screening`
- `vc-sourcing-dedupe-and-novelty-check`
- `citation-enforcement`
