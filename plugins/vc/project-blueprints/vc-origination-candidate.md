---
projectType: vc_origination_candidate
title: Origination Candidate Blueprint
source: alludium/project-types/vc_origination_candidate.json
---

> **GENERATED FILE**
> Source: `alludium/project-types/vc_origination_candidate.json`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Origination Candidate Blueprint

A first-class pre-deal company record that consolidates multi-line provenance, evidence, screening, relationship context, outreach state, and reviewed Deal Pipeline promotion.

This blueprint lists setup, support, and workflow-stage tasks with the recommended agents, task-referenced skills, document references, and integration surfaces for this project type. General and support sections are included only when they contain cross-cutting tasks that are not already mapped to a workflow stage.

## Setup

Project-type setup and configuration tasks used before normal project execution.

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| [Register Origination Candidate](../tasks/register-origination-candidate.md) | [Candidate Manager](../agents/vc-origination-candidate-manager.md) | [VC Sourcing Dedupe & Novelty Check](../skills/vc-sourcing-dedupe-and-novelty-check/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | [Candidate Batch Template](../alludium/documents/origination/candidate-batch-template.html) (operating_guidance)<br>[Dedupe And Novelty Policy](../alludium/documents/origination/dedupe-novelty-policy.html) (policy) | `alludium-platform`<br>`affinity-mcp-server`<br>`harmonic-mcp-oauth`<br>`exa-mcp-hosted` |
| [VC Pack Variable Discovery](../tasks/vc-pack-variable-discovery.md) | [Candidate Manager](../agents/vc-origination-candidate-manager.md) | None declared | None declared | `alludium-platform`<br>`affinity-mcp-server`<br>`harmonic-mcp-oauth`<br>`exa-mcp-hosted` |

## Identified

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| [Screen Identified Candidate](../tasks/screen-identified-candidate.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC Sourcing Verdict & Screening](../skills/vc-sourcing-verdict-and-screening/SKILL.md)<br>[VC Sourcing Dedupe & Novelty Check](../skills/vc-sourcing-dedupe-and-novelty-check/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | [Sourcing Scoring Rubric](../alludium/documents/origination/sourcing-scoring-rubric.html) (methodology, to `identified_screen_artifact_id`)<br>[Origination Source Strategy Guide](../alludium/documents/origination/origination-source-strategy-guide.html) (methodology)<br>[Dedupe And Novelty Policy](../alludium/documents/origination/dedupe-novelty-policy.html) (policy)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.html) (operating_guidance) | `alludium-platform`<br>`affinity-mcp-server` |

## Enriched

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| [Enrich Sourcing Candidate](../tasks/enrich-sourcing-candidate.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC Sourcing Candidate Enrichment](../skills/vc-sourcing-candidate-enrichment/SKILL.md)<br>[VC Sourcing Dedupe & Novelty Check](../skills/vc-sourcing-dedupe-and-novelty-check/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | None declared | `alludium-platform`<br>`affinity-mcp-server` |
| [Check Affinity Relationship Context](../tasks/check-affinity-relationship-context.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC Relationship Context Check](../skills/vc-relationship-context-check/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | None declared | `alludium-platform`<br>`affinity-mcp-server` |

## Qualified

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| [Score Sourcing Candidate](../tasks/score-sourcing-candidate.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC Sourcing Verdict & Screening](../skills/vc-sourcing-verdict-and-screening/SKILL.md)<br>[VC Sourcing Dedupe & Novelty Check](../skills/vc-sourcing-dedupe-and-novelty-check/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | [Sourcing Scoring Rubric](../alludium/documents/origination/sourcing-scoring-rubric.html) (methodology, to `scoring_artifact_id`)<br>[Origination Source Strategy Guide](../alludium/documents/origination/origination-source-strategy-guide.html) (methodology)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.html) (operating_guidance) | `alludium-platform`<br>`affinity-mcp-server` |
| [Sync Sourcing Candidate](../tasks/sync-sourcing-candidate.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC Source Registry & State Management](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[VC Sourcing Dedupe & Novelty Check](../skills/vc-sourcing-dedupe-and-novelty-check/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md)<br>[VC Notion Sync Write](../skills/vc-notion-sync-write/SKILL.md) | None declared | `alludium-platform`<br>`affinity-mcp-server` |
| [Review Portfolio Overlap](../tasks/review-portfolio-overlap.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC Portfolio Overlap Review](../skills/vc-portfolio-overlap-review/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md)<br>[VC Relationship Context Check](../skills/vc-relationship-context-check/SKILL.md) | None declared | `alludium-platform`<br>`affinity-mcp-server` |
| [Run Deal Fit Analysis](../tasks/run-deal-fit-analysis.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC Sourcing Verdict & Screening](../skills/vc-sourcing-verdict-and-screening/SKILL.md)<br>[Investment Screening Framework](../skills/investment-screening-framework/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | [Sourcing Scoring Rubric](../alludium/documents/origination/sourcing-scoring-rubric.html) (methodology, to `deal_fit_artifact_id`)<br>[Investment Screening Framework](../alludium/documents/shared/investment-screening-framework.html) (methodology)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.html) (operating_guidance) | `alludium-platform`<br>`affinity-mcp-server` |
| [Screen Active Sourcing Candidate](../tasks/screen-active-sourcing-candidate.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC Sourcing Verdict & Screening](../skills/vc-sourcing-verdict-and-screening/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md)<br>[Investment Screening Framework](../skills/investment-screening-framework/SKILL.md) | [Sourcing Scoring Rubric](../alludium/documents/origination/sourcing-scoring-rubric.html) (methodology, to `screening_artifact_id`)<br>[Origination Source Strategy Guide](../alludium/documents/origination/origination-source-strategy-guide.html) (methodology)<br>[Dedupe And Novelty Policy](../alludium/documents/origination/dedupe-novelty-policy.html) (policy)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.html) (operating_guidance) | `alludium-platform`<br>`affinity-mcp-server` |
| [Review Unicorn Signature](../tasks/review-unicorn-signature.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC Sourcing Verdict & Screening](../skills/vc-sourcing-verdict-and-screening/SKILL.md)<br>[Origination Prospect Summary Preparation](../skills/origination-prospect-summary-preparation/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | [Sourcing Scoring Rubric](../alludium/documents/origination/sourcing-scoring-rubric.html) (methodology, to `unicorn_signature_artifact_id`)<br>[Prospect Summary Template](../alludium/documents/origination/sourcing-ic-summary-template.html) (operating_guidance)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.html) (operating_guidance) | `alludium-platform`<br>`affinity-mcp-server` |
| [Prepare Prospect Summary](../tasks/prepare-prospect-summary.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [Origination Prospect Summary Preparation](../skills/origination-prospect-summary-preparation/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | [Prospect Summary Template](../alludium/documents/origination/sourcing-ic-summary-template.html) (output_template, to `prospect_summary_artifact_id`)<br>[Origination Source Strategy Guide](../alludium/documents/origination/origination-source-strategy-guide.html) (methodology)<br>[Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.html) (style_guide)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.html) (operating_guidance) | `alludium-platform`<br>`affinity-mcp-server` |

## Outreach Ready

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| [Prepare Outreach Draft Queue](../tasks/prepare-outreach-draft-queue.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC Outreach Draft Queue](../skills/vc-outreach-draft-queue/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md)<br>[Founder Outreach & Intro Paths](../skills/founder-outreach-and-intro-paths/SKILL.md) | [Outreach Queue Template](../alludium/documents/origination/outreach-queue-template.html) (output_template, to `outreach_queue_artifact_id`)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.html) (operating_guidance) | `alludium-platform`<br>`affinity-mcp-server` |
| [Prepare Initial LinkedIn Reachout](../tasks/prepare-initial-linkedin-reachout.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC Outreach Draft Queue](../skills/vc-outreach-draft-queue/SKILL.md)<br>[Founder Outreach & Intro Paths](../skills/founder-outreach-and-intro-paths/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | [Outreach Queue Template](../alludium/documents/origination/outreach-queue-template.html) (output_template, to `initial_linkedin_reachout_artifact_id`)<br>[Origination Source Strategy Guide](../alludium/documents/origination/origination-source-strategy-guide.html) (methodology)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.html) (operating_guidance) | `alludium-platform`<br>`affinity-mcp-server` |

## Contacted

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| [Record LinkedIn Connection Attempt](../tasks/record-linkedin-connection-attempt.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC Outreach Draft Queue](../skills/vc-outreach-draft-queue/SKILL.md)<br>[Founder Outreach & Intro Paths](../skills/founder-outreach-and-intro-paths/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | [Outreach Queue Template](../alludium/documents/origination/outreach-queue-template.html) (output_template, to `connection_record_artifact_id`)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.html) (operating_guidance) | `alludium-platform`<br>`affinity-mcp-server` |
| [Prepare Second Reachout Email](../tasks/prepare-second-reachout-email.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC Outreach Draft Queue](../skills/vc-outreach-draft-queue/SKILL.md)<br>[Founder Outreach & Intro Paths](../skills/founder-outreach-and-intro-paths/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | [Outreach Queue Template](../alludium/documents/origination/outreach-queue-template.html) (output_template, to `second_reachout_email_artifact_id`)<br>[Origination Source Strategy Guide](../alludium/documents/origination/origination-source-strategy-guide.html) (methodology)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.html) (operating_guidance) | `alludium-platform`<br>`affinity-mcp-server` |

## Engaged

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| [Screen Founder-Connected Candidate](../tasks/screen-founder-connected-candidate.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC Sourcing Verdict & Screening](../skills/vc-sourcing-verdict-and-screening/SKILL.md)<br>[VC Outreach Draft Queue](../skills/vc-outreach-draft-queue/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md)<br>[Investment Screening Framework](../skills/investment-screening-framework/SKILL.md) | [Sourcing Scoring Rubric](../alludium/documents/origination/sourcing-scoring-rubric.html) (methodology, to `founder_connected_screen_artifact_id`)<br>[Outreach Queue Template](../alludium/documents/origination/outreach-queue-template.html) (output_template)<br>[Origination Source Strategy Guide](../alludium/documents/origination/origination-source-strategy-guide.html) (methodology)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.html) (operating_guidance) | `alludium-platform`<br>`affinity-mcp-server` |
| [Review Outreach Outcome](../tasks/review-outreach-outcome.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [Origination Deal Pipeline Promotion](../skills/origination-deal-pipeline-promotion/SKILL.md)<br>[VC Outreach Draft Queue](../skills/vc-outreach-draft-queue/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | [Promotion Package Template](../alludium/documents/origination/promotion-package-template.html) (output_template, to `outreach_outcome_artifact_id`)<br>[Origination Source Strategy Guide](../alludium/documents/origination/origination-source-strategy-guide.html) (methodology)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.html) (operating_guidance) | `alludium-platform`<br>`affinity-mcp-server` |

## Watchlist

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| None mapped | None declared | None declared | None declared | None declared |

## Passed

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| None mapped | None declared | None declared | None declared | None declared |

## Promotion Ready

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| [Promote Candidate to Deal Pipeline](../tasks/promote-candidate-to-deal-pipeline.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [Origination Deal Pipeline Promotion](../skills/origination-deal-pipeline-promotion/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md)<br>[Deal Pipeline Setup & Source Ingestion](../skills/deal-pipeline-setup-and-source-ingestion/SKILL.md) | [Promotion Package Template](../alludium/documents/origination/promotion-package-template.html) (output_template, to `promotion_package_artifact_id`)<br>[Origination Source Strategy Guide](../alludium/documents/origination/origination-source-strategy-guide.html) (methodology)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.html) (operating_guidance) | `alludium-platform`<br>`affinity-mcp-server` |

## Promoted

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| None mapped | None declared | None declared | None declared | None declared |

## Archived

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| None mapped | None declared | None declared | None declared | None declared |
