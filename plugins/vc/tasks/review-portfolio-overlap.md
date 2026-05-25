---
id: vc.review_portfolio_overlap
title: Review Portfolio Overlap
slug: review-portfolio-overlap
agent: vc-sourcing-operator
skills:
- vc-portfolio-overlap-review
- citation-enforcement
- vc-relationship-context-check
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/review-portfolio-overlap.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Review Portfolio Overlap

Compare active sourcing candidates against portfolio companies and flag possible competitive overlap.

## Instructions

Mirror the reference pipeline's portfolio-overlap checker. Compare only active candidates such as Meet, IC-Summary, or Reach out against the current portfolio. Classify overlap as none, low, medium, or high using target customer, problem, and product category; sectoral overlap alone is not enough. Do not auto-pass candidates for overlap.

## Missing Input Policy

Ask for active candidate batch, portfolio source or cache, freshness policy, and whether cached portfolio data may be reused.

## External Action Policy

Review and annotate proposal only. Do not change candidate status, pass candidates, contact founders, or update external systems without separate approval.

## Completion Criteria

- Each checked candidate has severity, matching portfolio companies, reason, and receipt.
- Portfolio source freshness and cache age are named.

## Human Decision Points

- None declared

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `portfolio_overlap_scope` | Portfolio Overlap Scope | `json` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `portfolio_overlap_artifact_id` | Portfolio Overlap Artifact | `file` | yes |
| `high_overlap_count` | High Overlap Count | `number` | no |
| `overlap_report` | Overlap Report | `richtext` | no |

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/review-portfolio-overlap.yaml`
- Alludium task ID: `vc.review_portfolio_overlap`
- Task family: `origination_portfolio_overlap`
- Lifecycle stage: `review`
- Recommended agent: `vc-sourcing-operator` (Alludium template `vc_sourcing_operator`)
- Supported project types:
  - `vc_origination_pipeline`
- Supported project scopes:
  - `project_instance`

## Required Skills

- `vc-portfolio-overlap-review`
- `citation-enforcement`
- `vc-relationship-context-check`
