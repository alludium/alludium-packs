---
projectType: vc_deal_pipeline
title: VC Deal Pipeline Blueprint
source: alludium/project-types/vc_deal_pipeline.json
---

> **GENERATED FILE**
> Source: `alludium/project-types/vc_deal_pipeline.json`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# VC Deal Pipeline Blueprint

A simplified, evidence-led VC Deal Pipeline with stage-independent living documents from screening through term-sheet review.

This blueprint lists setup, support, and workflow-stage tasks with the recommended agents, task-referenced skills, document references, and integration surfaces for this project type. General and support sections are included only when they contain cross-cutting tasks that are not already mapped to a workflow stage.

## Setup

Project-type setup and configuration tasks used before normal project execution.

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| [Create Pipeline Deal](../tasks/create-pipeline-deal.md) | [Deal Manager](../agents/vc-deal-pipeline-manager.md) | [Company Research & Enrichment](../skills/company-research-and-enrichment/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | [Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.html) (style_guide) | `alludium-platform` |
| [VC Pack Variable Discovery](../tasks/vc-pack-variable-discovery.md) | [Deal Manager](../agents/vc-deal-pipeline-manager.md) | None declared | None declared | `alludium-platform` |

## General

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| [Generate or Refresh Screening Report](../tasks/generate-refresh-screening-report.md) | [Deal Analyst](../agents/vc-deal-analyst.md) | [Generate or Refresh Living Report](../skills/generate-or-refresh-living-report/SKILL.md)<br>[Investment Screening Framework](../skills/investment-screening-framework/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | [Deal Pipeline Screening Criteria](../alludium/documents/deal-pipeline/screening-criteria.html) (methodology)<br>[Deal Pipeline Screening Report Template](../alludium/documents/deal-pipeline/screening-report-template.html) (output_template, to `screening_report_artifact_id`)<br>[Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.html) (style_guide)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.html) (operating_guidance) | `alludium-platform`<br>`harmonic-mcp-oauth`<br>`affinity-mcp-server`<br>`exa-mcp-hosted` |
| [Generate or Refresh Evaluation Report](../tasks/generate-refresh-evaluation-report.md) | [Deal Analyst](../agents/vc-deal-analyst.md) | [Generate or Refresh Living Report](../skills/generate-or-refresh-living-report/SKILL.md)<br>[Investment Diligence Question Framework](../skills/investment-diligence-question-framework/SKILL.md)<br>[Market Map Building](../skills/market-map-building/SKILL.md)<br>[Commercial Evaluation & Market Risk](../skills/commercial-evaluation-and-market-risk/SKILL.md)<br>[Technical Evaluation & Product Risk](../skills/technical-evaluation-and-product-risk/SKILL.md)<br>[Financial Evaluation & Financing Risk](../skills/financial-evaluation-and-financing-risk/SKILL.md)<br>[Team Evaluation & Founder Risk](../skills/team-evaluation-and-founder-risk/SKILL.md)<br>[Red Flags Scanner](../skills/red-flags-scanner/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | [Deal Pipeline Evaluation Criteria](../alludium/documents/deal-pipeline/evaluation-criteria.html) (methodology)<br>[Deal Pipeline Evaluation Report Template](../alludium/documents/deal-pipeline/evaluation-report-template.html) (output_template, to `evaluation_report_artifact_id`)<br>[Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.html) (style_guide)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.html) (operating_guidance) | `alludium-platform`<br>`harmonic-mcp-oauth`<br>`affinity-mcp-server`<br>`exa-mcp-hosted` |
| [Prepare or Refresh IC Memo](../tasks/prepare-refresh-ic-memo.md) | [Deal Analyst](../agents/vc-deal-analyst.md) | [Generate or Refresh Living Report](../skills/generate-or-refresh-living-report/SKILL.md)<br>[IC Memo Assembly](../skills/ic-memo-assembly/SKILL.md)<br>[IC Risk Checklist & Decision Log](../skills/ic-risk-checklist-and-decision-log/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | [Deal Pipeline IC Criteria and Guidance](../alludium/documents/deal-pipeline/ic-criteria.html) (methodology)<br>[Deal Pipeline IC Memo Template](../alludium/documents/deal-pipeline/ic-memo-template.html) (output_template, to `ic_memo_artifact_id`)<br>[Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.html) (style_guide)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.html) (operating_guidance) | `alludium-platform`<br>`harmonic-mcp-oauth`<br>`affinity-mcp-server`<br>`exa-mcp-hosted` |
| [Review or Refresh Term Sheet](../tasks/review-refresh-term-sheet.md) | [Deal Analyst](../agents/vc-deal-analyst.md) | [Generate or Refresh Living Report](../skills/generate-or-refresh-living-report/SKILL.md)<br>[Deal Terms Analysis](../skills/deal-terms-analysis/SKILL.md)<br>[Term Sheet Negotiation Brief](../skills/term-sheet-negotiation-brief/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | [Deal Pipeline Term Sheet Review Policy](../alludium/documents/deal-pipeline/term-sheet-review-policy.html) (policy)<br>[Deal Pipeline Term Sheet Review Template](../alludium/documents/deal-pipeline/term-sheet-review-template.html) (output_template, to `term_sheet_review_artifact_id`)<br>[Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.html) (style_guide)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.html) (operating_guidance) | `alludium-platform`<br>`harmonic-mcp-oauth`<br>`affinity-mcp-server`<br>`exa-mcp-hosted` |

## Screening

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| None mapped | None declared | None declared | None declared | None declared |

## Evaluation

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| None mapped | None declared | None declared | None declared | None declared |

## Decision

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| None mapped | None declared | None declared | None declared | None declared |

## Term Sheet

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| None mapped | None declared | None declared | None declared | None declared |

## Passed

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| None mapped | None declared | None declared | None declared | None declared |

## Promoted To Investment Execution

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| None mapped | None declared | None declared | None declared | None declared |

## Archived

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| None mapped | None declared | None declared | None declared | None declared |
