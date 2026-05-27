---
projectType: vc_origination_pipeline
title: Origination Pipeline Blueprint
source: alludium/project-types/vc_origination_pipeline.json
---

> **GENERATED FILE**
> Source: `alludium/project-types/vc_origination_pipeline.json`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Origination Pipeline Blueprint

Project context for a standing venture sourcing pipeline that configures source coverage, credential readiness, review policy, and promotion thresholds before recurring sourcing work is enabled.

This blueprint lists setup, general, management, and lifecycle-stage tasks with the recommended agents, task-referenced skills, document references, and integration surfaces for this project type. Setup, General, and Management are blueprint categories rather than lifecycle states.

## Setup

Project-type setup and configuration tasks used before normal project execution.

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| Project Source Choice | [Origination Scout](../agents/vc-origination-scout.md) | None declared | None declared | None declared |
| Project Variable Review | [Origination Scout](../agents/vc-origination-scout.md) | None declared | None declared | None declared |
| Project Schedule Review | [Origination Scout](../agents/vc-origination-scout.md) | None declared | None declared | None declared |
| Project Source Setup | [Origination Scout](../agents/vc-origination-scout.md) | None declared | None declared | None declared |
| [VC Pack Variable Discovery](../tasks/vc-pack-variable-discovery.md) | [Origination Scout](../agents/vc-origination-scout.md) | None declared | None declared | `alludium-platform`<br>`harmonic-mcp-oauth`<br>`affinity-mcp-server`<br>`exa-mcp-hosted`<br>`brave-search-mcp`<br>`serpapi-mcp`<br>`firecrawl-mcp-hosted`<br>`dealroom-mcp`<br>`linkedin` |
| [Set Up Apify for Origination](../tasks/apify-setup.md) | [Integration Operator](../agents/vc-integration-operator.md) | [`vc-apify-discovery`](../skills/vc-apify-discovery/SKILL.md)<br>[`vc-apify-sync-read`](../skills/vc-apify-sync-read/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | None declared | `apify-actors-mcp` |
| [Configure Companies House Public Register Preview](../tasks/companies-house-setup.md) | [Integration Operator](../agents/vc-integration-operator.md) | [`vc-companies-house-sourcing`](../skills/vc-companies-house-sourcing/SKILL.md)<br>[`vc-companies-house-sync-read`](../skills/vc-companies-house-sync-read/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | None declared | `firecrawl-mcp-hosted` |

## General

Reusable project-instance tasks that can be useful across multiple lifecycle stages.

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| None mapped | None declared | None declared | None declared | None declared |

## Management

Project-management tasks that operate across a project suite, source pipeline, or recurring sync/reporting flow.

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| [Run VC Sourcing Pipeline](../tasks/run-sourcing-pipeline.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [`vc-origination-pipeline-orchestration`](../skills/vc-origination-pipeline-orchestration/SKILL.md)<br>[`vc-source-registry-and-state-management`](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | [`vc.document.candidate_batch_template`](../alludium/documents/origination/candidate-batch-template.md) (output_template, to `candidate_batch_artifact_id`)<br>[`vc.document.origination_pipeline_sop`](../alludium/documents/origination/origination-pipeline-sop.md) (operating_guidance)<br>[`vc.document.origination_source_strategy_guide`](../alludium/documents/origination/origination-source-strategy-guide.md) (methodology)<br>[`vc.document.template_use_guidance`](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | None declared |
| [Generate Sourcing Digest](../tasks/generate-sourcing-digest.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [`vc-sourcing-digest-generation`](../skills/vc-sourcing-digest-generation/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | [`vc.document.sourcing_digest_template`](../alludium/documents/origination/sourcing-digest-template.md) (output_template, to `sourcing_digest_artifact_id`)<br>[`vc.document.template_use_guidance`](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | None declared |
| [Review Source Errors and Spend](../tasks/review-source-errors-and-spend.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [`vc-source-error-and-spend-audit`](../skills/vc-source-error-and-spend-audit/SKILL.md)<br>[`vc-source-registry-and-state-management`](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | [`vc.document.source_health_review_checklist`](../alludium/documents/origination/source-health-review-checklist.md) (output_template, to `source_health_artifact_id`)<br>[`vc.document.paid_source_spend_audit_checklist`](../alludium/documents/origination/paid-source-spend-audit-checklist.md) (checklist)<br>[`vc.document.template_use_guidance`](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | None declared |
| [Discover Companies House Candidates](../tasks/discover-companies-house-candidates.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [`vc-companies-house-sourcing`](../skills/vc-companies-house-sourcing/SKILL.md)<br>[`vc-source-registry-and-state-management`](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | None declared | None declared |
| [Discover X Founder Signals](../tasks/discover-x-founder-signals.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [`vc-apify-x-founder-discovery`](../skills/vc-apify-x-founder-discovery/SKILL.md)<br>[`vc-source-registry-and-state-management`](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | None declared | None declared |
| [Discover GitHub Builder Signals](../tasks/discover-github-builder-signals.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [`vc-github-builder-signal-discovery`](../skills/vc-github-builder-signal-discovery/SKILL.md)<br>[`vc-source-registry-and-state-management`](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | None declared | None declared |
| [Discover LinkedIn Founder Candidates](../tasks/discover-linkedin-founders.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [`vc-apify-linkedin-founder-discovery`](../skills/vc-apify-linkedin-founder-discovery/SKILL.md)<br>[`vc-source-registry-and-state-management`](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | None declared | None declared |
| [Discover Reddit Builder Signals](../tasks/discover-reddit-builder-signals.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [`vc-reddit-builder-signal-discovery`](../skills/vc-reddit-builder-signal-discovery/SKILL.md)<br>[`vc-source-registry-and-state-management`](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | None declared | None declared |
| [Review Portfolio Overlap](../tasks/review-portfolio-overlap.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [`vc-portfolio-overlap-review`](../skills/vc-portfolio-overlap-review/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md)<br>[`vc-relationship-context-check`](../skills/vc-relationship-context-check/SKILL.md) | None declared | None declared |
| [Screen Identified Candidates](../tasks/screen-identified-candidates.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [`vc-sourcing-verdict-and-screening`](../skills/vc-sourcing-verdict-and-screening/SKILL.md)<br>[`vc-sourcing-dedupe-and-novelty-check`](../skills/vc-sourcing-dedupe-and-novelty-check/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | [`vc.document.sourcing_scoring_rubric`](../alludium/documents/origination/sourcing-scoring-rubric.md) (methodology, to `identified_screen_artifact_id`)<br>[`vc.document.origination_source_strategy_guide`](../alludium/documents/origination/origination-source-strategy-guide.md) (methodology)<br>[`vc.document.dedupe_novelty_policy`](../alludium/documents/origination/dedupe-novelty-policy.md) (policy)<br>[`vc.document.template_use_guidance`](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | None declared |
| [Run Deal Fit Analysis](../tasks/run-deal-fit-analysis.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [`vc-sourcing-verdict-and-screening`](../skills/vc-sourcing-verdict-and-screening/SKILL.md)<br>[`investment-screening-framework`](../skills/investment-screening-framework/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | [`vc.document.sourcing_scoring_rubric`](../alludium/documents/origination/sourcing-scoring-rubric.md) (methodology, to `deal_fit_artifact_id`)<br>[`vc.document.investment_screening_framework`](../alludium/documents/shared/investment-screening-framework.md) (methodology)<br>[`vc.document.template_use_guidance`](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | None declared |
| [Screen Active Sourcing Candidates](../tasks/screen-active-sourcing-candidates.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [`vc-sourcing-verdict-and-screening`](../skills/vc-sourcing-verdict-and-screening/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md)<br>[`investment-screening-framework`](../skills/investment-screening-framework/SKILL.md) | [`vc.document.sourcing_scoring_rubric`](../alludium/documents/origination/sourcing-scoring-rubric.md) (methodology, to `screening_artifact_id`)<br>[`vc.document.origination_source_strategy_guide`](../alludium/documents/origination/origination-source-strategy-guide.md) (methodology)<br>[`vc.document.dedupe_novelty_policy`](../alludium/documents/origination/dedupe-novelty-policy.md) (policy)<br>[`vc.document.template_use_guidance`](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | None declared |
| [Review Unicorn Signature](../tasks/review-unicorn-signature.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [`vc-sourcing-verdict-and-screening`](../skills/vc-sourcing-verdict-and-screening/SKILL.md)<br>[`vc-origination-ic-summary-preparation`](../skills/vc-origination-ic-summary-preparation/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | [`vc.document.sourcing_scoring_rubric`](../alludium/documents/origination/sourcing-scoring-rubric.md) (methodology, to `unicorn_signature_artifact_id`)<br>[`vc.document.sourcing_ic_summary_template`](../alludium/documents/origination/sourcing-ic-summary-template.md) (operating_guidance)<br>[`vc.document.template_use_guidance`](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | None declared |
| [Screen Founder-Connected Candidates](../tasks/screen-founder-connected-candidates.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [`vc-sourcing-verdict-and-screening`](../skills/vc-sourcing-verdict-and-screening/SKILL.md)<br>[`vc-outreach-draft-queue`](../skills/vc-outreach-draft-queue/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md)<br>[`investment-screening-framework`](../skills/investment-screening-framework/SKILL.md) | [`vc.document.sourcing_scoring_rubric`](../alludium/documents/origination/sourcing-scoring-rubric.md) (methodology, to `founder_connected_screen_artifact_id`)<br>[`vc.document.outreach_queue_template`](../alludium/documents/origination/outreach-queue-template.md) (output_template)<br>[`vc.document.origination_source_strategy_guide`](../alludium/documents/origination/origination-source-strategy-guide.md) (methodology)<br>[`vc.document.template_use_guidance`](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | None declared |
| [Prepare Outreach Draft Queue](../tasks/prepare-outreach-draft-queue.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [`vc-outreach-draft-queue`](../skills/vc-outreach-draft-queue/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md)<br>[`founder-outreach-and-intro-paths`](../skills/founder-outreach-and-intro-paths/SKILL.md) | [`vc.document.outreach_queue_template`](../alludium/documents/origination/outreach-queue-template.md) (output_template, to `outreach_queue_artifact_id`)<br>[`vc.document.template_use_guidance`](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | None declared |
| [Audit LinkedIn Query Spend](../tasks/audit-linkedin-query-spend.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [`vc-linkedin-query-spend-audit`](../skills/vc-linkedin-query-spend-audit/SKILL.md)<br>[`vc-source-registry-and-state-management`](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | [`vc.document.paid_source_spend_audit_checklist`](../alludium/documents/origination/paid-source-spend-audit-checklist.md) (output_template, to `linkedin_spend_audit_artifact_id`)<br>[`vc.document.template_use_guidance`](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | None declared |
| [Explore Apify Origination Sources](../tasks/apify-discovery.md) | [Integration Operator](../agents/vc-integration-operator.md) | [`vc-apify-discovery`](../skills/vc-apify-discovery/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | None declared | None declared |
| [Explore Companies House Public Register Scope](../tasks/companies-house-discovery.md) | [Integration Operator](../agents/vc-integration-operator.md) | [`vc-companies-house-sourcing`](../skills/vc-companies-house-sourcing/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | None declared | None declared |
| [Prepare Lead Gen Packet](../tasks/prepare-lead-gen-packet.md) | [Origination Scout](../agents/vc-origination-scout.md) | [`company-research-and-enrichment`](../skills/company-research-and-enrichment/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | [`vc.document.lead_generation_packet_template`](../alludium/documents/deal-room/lead-generation-packet-template.md) (output_template, to `lead_generation_packet_artifact_id`)<br>[`vc.document.origination_source_strategy_guide`](../alludium/documents/origination/origination-source-strategy-guide.md) (methodology)<br>[`vc.document.evidence_citation_style_guide`](../alludium/documents/shared/evidence-citation-style-guide.md) (style_guide)<br>[`vc.document.template_use_guidance`](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | `alludium-platform`<br>`harmonic-mcp-oauth`<br>`affinity-mcp-server`<br>`exa-mcp-hosted`<br>`brave-search-mcp`<br>`serpapi-mcp`<br>`firecrawl-mcp-hosted`<br>`dealroom-mcp`<br>`linkedin` |
| [Preview Apify Origination Results](../tasks/apify-sync-read.md) | [Integration Operator](../agents/vc-integration-operator.md) | [`vc-apify-sync-read`](../skills/vc-apify-sync-read/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | None declared | None declared |
| [Preview Companies House Public Register Results](../tasks/companies-house-sync-read.md) | [Integration Operator](../agents/vc-integration-operator.md) | [`vc-companies-house-sync-read`](../skills/vc-companies-house-sync-read/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | None declared | None declared |

## Draft

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| [Configure Origination Pipeline](../tasks/configure-origination-pipeline.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [`vc-origination-pipeline-orchestration`](../skills/vc-origination-pipeline-orchestration/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | [`vc.document.origination_pipeline_sop`](../alludium/documents/origination/origination-pipeline-sop.md) (operating_guidance)<br>[`vc.document.origination_source_strategy_guide`](../alludium/documents/origination/origination-source-strategy-guide.md) (methodology)<br>[`vc.document.source_registry_template`](../alludium/documents/origination/source-registry-template.md) (operating_guidance)<br>[`vc.document.template_use_guidance`](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | None declared |

## Configured

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| None mapped | None declared | None declared | None declared | None declared |

## Active

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| [Run VC Sourcing Pipeline](../tasks/run-sourcing-pipeline.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [`vc-origination-pipeline-orchestration`](../skills/vc-origination-pipeline-orchestration/SKILL.md)<br>[`vc-source-registry-and-state-management`](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | [`vc.document.candidate_batch_template`](../alludium/documents/origination/candidate-batch-template.md) (output_template, to `candidate_batch_artifact_id`)<br>[`vc.document.origination_pipeline_sop`](../alludium/documents/origination/origination-pipeline-sop.md) (operating_guidance)<br>[`vc.document.origination_source_strategy_guide`](../alludium/documents/origination/origination-source-strategy-guide.md) (methodology)<br>[`vc.document.template_use_guidance`](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | None declared |
| [Generate Sourcing Digest](../tasks/generate-sourcing-digest.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [`vc-sourcing-digest-generation`](../skills/vc-sourcing-digest-generation/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | [`vc.document.sourcing_digest_template`](../alludium/documents/origination/sourcing-digest-template.md) (output_template, to `sourcing_digest_artifact_id`)<br>[`vc.document.template_use_guidance`](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | None declared |
| [Audit LinkedIn Query Spend](../tasks/audit-linkedin-query-spend.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [`vc-linkedin-query-spend-audit`](../skills/vc-linkedin-query-spend-audit/SKILL.md)<br>[`vc-source-registry-and-state-management`](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | [`vc.document.paid_source_spend_audit_checklist`](../alludium/documents/origination/paid-source-spend-audit-checklist.md) (output_template, to `linkedin_spend_audit_artifact_id`)<br>[`vc.document.template_use_guidance`](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | None declared |
| [Source Thesis Targets](../tasks/source-thesis-targets.md) | [Origination Scout](../agents/vc-origination-scout.md) | [`company-research-and-enrichment`](../skills/company-research-and-enrichment/SKILL.md)<br>[`founder-outreach-and-intro-paths`](../skills/founder-outreach-and-intro-paths/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | [`vc.document.thesis_target_list_template`](../alludium/documents/deal-room/thesis-target-list-template.md) (output_template, to `thesis_target_list_artifact_id`)<br>[`vc.document.origination_source_strategy_guide`](../alludium/documents/origination/origination-source-strategy-guide.md) (methodology)<br>[`vc.document.evidence_citation_style_guide`](../alludium/documents/shared/evidence-citation-style-guide.md) (style_guide)<br>[`vc.document.template_use_guidance`](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | `alludium-platform`<br>`harmonic-mcp-oauth`<br>`affinity-mcp-server`<br>`exa-mcp-hosted`<br>`brave-search-mcp`<br>`serpapi-mcp`<br>`firecrawl-mcp-hosted`<br>`dealroom-mcp`<br>`linkedin` |

## Needs Credentials

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| None mapped | None declared | None declared | None declared | None declared |

## Source Degraded

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| [Review Source Errors and Spend](../tasks/review-source-errors-and-spend.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [`vc-source-error-and-spend-audit`](../skills/vc-source-error-and-spend-audit/SKILL.md)<br>[`vc-source-registry-and-state-management`](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | [`vc.document.source_health_review_checklist`](../alludium/documents/origination/source-health-review-checklist.md) (output_template, to `source_health_artifact_id`)<br>[`vc.document.paid_source_spend_audit_checklist`](../alludium/documents/origination/paid-source-spend-audit-checklist.md) (checklist)<br>[`vc.document.template_use_guidance`](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | None declared |

## Review Backlog

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| None mapped | None declared | None declared | None declared | None declared |

## Identified

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| [Discover Companies House Candidates](../tasks/discover-companies-house-candidates.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [`vc-companies-house-sourcing`](../skills/vc-companies-house-sourcing/SKILL.md)<br>[`vc-source-registry-and-state-management`](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | None declared | None declared |
| [Discover LinkedIn Founder Candidates](../tasks/discover-linkedin-founders.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [`vc-apify-linkedin-founder-discovery`](../skills/vc-apify-linkedin-founder-discovery/SKILL.md)<br>[`vc-source-registry-and-state-management`](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | None declared | None declared |
| [Discover X Founder Signals](../tasks/discover-x-founder-signals.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [`vc-apify-x-founder-discovery`](../skills/vc-apify-x-founder-discovery/SKILL.md)<br>[`vc-source-registry-and-state-management`](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | None declared | None declared |
| [Discover GitHub Builder Signals](../tasks/discover-github-builder-signals.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [`vc-github-builder-signal-discovery`](../skills/vc-github-builder-signal-discovery/SKILL.md)<br>[`vc-source-registry-and-state-management`](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | None declared | None declared |
| [Discover Reddit Builder Signals](../tasks/discover-reddit-builder-signals.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [`vc-reddit-builder-signal-discovery`](../skills/vc-reddit-builder-signal-discovery/SKILL.md)<br>[`vc-source-registry-and-state-management`](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | None declared | None declared |
| [Review Reddit Candidate Inbox](../tasks/review-reddit-candidate-inbox.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [`vc-reddit-inbox-approval`](../skills/vc-reddit-inbox-approval/SKILL.md)<br>[`vc-sourcing-dedupe-and-novelty-check`](../skills/vc-sourcing-dedupe-and-novelty-check/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | None declared | None declared |
| [Ingest Manual Sourcing Tip](../tasks/ingest-manual-sourcing-tip.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [`vc-manual-tip-ingestion`](../skills/vc-manual-tip-ingestion/SKILL.md)<br>[`vc-sourcing-dedupe-and-novelty-check`](../skills/vc-sourcing-dedupe-and-novelty-check/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | None declared | None declared |
| [Enrich Sourcing Candidates](../tasks/enrich-sourcing-candidates.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [`vc-sourcing-candidate-enrichment`](../skills/vc-sourcing-candidate-enrichment/SKILL.md)<br>[`vc-sourcing-dedupe-and-novelty-check`](../skills/vc-sourcing-dedupe-and-novelty-check/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | None declared | None declared |
| [Check Affinity Relationship Context](../tasks/check-affinity-relationships.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [`vc-relationship-context-check`](../skills/vc-relationship-context-check/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | None declared | None declared |

## Screened

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| [Score Sourcing Candidates](../tasks/score-sourcing-candidates.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [`vc-sourcing-verdict-and-screening`](../skills/vc-sourcing-verdict-and-screening/SKILL.md)<br>[`vc-sourcing-dedupe-and-novelty-check`](../skills/vc-sourcing-dedupe-and-novelty-check/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | [`vc.document.sourcing_scoring_rubric`](../alludium/documents/origination/sourcing-scoring-rubric.md) (methodology, to `scoring_artifact_id`)<br>[`vc.document.origination_source_strategy_guide`](../alludium/documents/origination/origination-source-strategy-guide.md) (methodology)<br>[`vc.document.template_use_guidance`](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | None declared |
| [Screen Identified Candidates](../tasks/screen-identified-candidates.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [`vc-sourcing-verdict-and-screening`](../skills/vc-sourcing-verdict-and-screening/SKILL.md)<br>[`vc-sourcing-dedupe-and-novelty-check`](../skills/vc-sourcing-dedupe-and-novelty-check/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | [`vc.document.sourcing_scoring_rubric`](../alludium/documents/origination/sourcing-scoring-rubric.md) (methodology, to `identified_screen_artifact_id`)<br>[`vc.document.origination_source_strategy_guide`](../alludium/documents/origination/origination-source-strategy-guide.md) (methodology)<br>[`vc.document.dedupe_novelty_policy`](../alludium/documents/origination/dedupe-novelty-policy.md) (policy)<br>[`vc.document.template_use_guidance`](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | None declared |
| [Sync Sourcing Candidates](../tasks/sync-sourcing-candidates.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [`vc-source-registry-and-state-management`](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[`vc-sourcing-dedupe-and-novelty-check`](../skills/vc-sourcing-dedupe-and-novelty-check/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md)<br>[`vc-notion-sync-write`](../skills/vc-notion-sync-write/SKILL.md) | None declared | None declared |
| [Review Portfolio Overlap](../tasks/review-portfolio-overlap.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [`vc-portfolio-overlap-review`](../skills/vc-portfolio-overlap-review/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md)<br>[`vc-relationship-context-check`](../skills/vc-relationship-context-check/SKILL.md) | None declared | None declared |
| [Run Deal Fit Analysis](../tasks/run-deal-fit-analysis.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [`vc-sourcing-verdict-and-screening`](../skills/vc-sourcing-verdict-and-screening/SKILL.md)<br>[`investment-screening-framework`](../skills/investment-screening-framework/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | [`vc.document.sourcing_scoring_rubric`](../alludium/documents/origination/sourcing-scoring-rubric.md) (methodology, to `deal_fit_artifact_id`)<br>[`vc.document.investment_screening_framework`](../alludium/documents/shared/investment-screening-framework.md) (methodology)<br>[`vc.document.template_use_guidance`](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | None declared |
| [Screen Active Sourcing Candidates](../tasks/screen-active-sourcing-candidates.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [`vc-sourcing-verdict-and-screening`](../skills/vc-sourcing-verdict-and-screening/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md)<br>[`investment-screening-framework`](../skills/investment-screening-framework/SKILL.md) | [`vc.document.sourcing_scoring_rubric`](../alludium/documents/origination/sourcing-scoring-rubric.md) (methodology, to `screening_artifact_id`)<br>[`vc.document.origination_source_strategy_guide`](../alludium/documents/origination/origination-source-strategy-guide.md) (methodology)<br>[`vc.document.dedupe_novelty_policy`](../alludium/documents/origination/dedupe-novelty-policy.md) (policy)<br>[`vc.document.template_use_guidance`](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | None declared |
| [Review Unicorn Signature](../tasks/review-unicorn-signature.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [`vc-sourcing-verdict-and-screening`](../skills/vc-sourcing-verdict-and-screening/SKILL.md)<br>[`vc-origination-ic-summary-preparation`](../skills/vc-origination-ic-summary-preparation/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | [`vc.document.sourcing_scoring_rubric`](../alludium/documents/origination/sourcing-scoring-rubric.md) (methodology, to `unicorn_signature_artifact_id`)<br>[`vc.document.sourcing_ic_summary_template`](../alludium/documents/origination/sourcing-ic-summary-template.md) (operating_guidance)<br>[`vc.document.template_use_guidance`](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | None declared |

## Of Interest

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| [Prepare Sourcing IC Summary](../tasks/prepare-sourcing-ic-summary.md) | [IC Prep Producer](../agents/vc-ic-prep-producer.md) | [`vc-origination-ic-summary-preparation`](../skills/vc-origination-ic-summary-preparation/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | [`vc.document.sourcing_ic_summary_template`](../alludium/documents/origination/sourcing-ic-summary-template.md) (output_template, to `ic_summary_artifact_id`)<br>[`vc.document.origination_source_strategy_guide`](../alludium/documents/origination/origination-source-strategy-guide.md) (methodology)<br>[`vc.document.evidence_citation_style_guide`](../alludium/documents/shared/evidence-citation-style-guide.md) (style_guide)<br>[`vc.document.template_use_guidance`](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | `alludium-platform`<br>`exa-mcp-hosted`<br>`brave-search-mcp`<br>`serpapi-mcp`<br>`dealroom-mcp`<br>`google_drive` |
| [Prepare Outreach Draft Queue](../tasks/prepare-outreach-draft-queue.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [`vc-outreach-draft-queue`](../skills/vc-outreach-draft-queue/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md)<br>[`founder-outreach-and-intro-paths`](../skills/founder-outreach-and-intro-paths/SKILL.md) | [`vc.document.outreach_queue_template`](../alludium/documents/origination/outreach-queue-template.md) (output_template, to `outreach_queue_artifact_id`)<br>[`vc.document.template_use_guidance`](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | None declared |

## Connecting On Linkedin

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| [Record LinkedIn Connection Attempt](../tasks/record-linkedin-connection-attempt.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [`vc-outreach-draft-queue`](../skills/vc-outreach-draft-queue/SKILL.md)<br>[`founder-outreach-and-intro-paths`](../skills/founder-outreach-and-intro-paths/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | [`vc.document.outreach_queue_template`](../alludium/documents/origination/outreach-queue-template.md) (output_template, to `connection_record_artifact_id`)<br>[`vc.document.template_use_guidance`](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | None declared |

## Founder Connected

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| [Screen Founder-Connected Candidates](../tasks/screen-founder-connected-candidates.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [`vc-sourcing-verdict-and-screening`](../skills/vc-sourcing-verdict-and-screening/SKILL.md)<br>[`vc-outreach-draft-queue`](../skills/vc-outreach-draft-queue/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md)<br>[`investment-screening-framework`](../skills/investment-screening-framework/SKILL.md) | [`vc.document.sourcing_scoring_rubric`](../alludium/documents/origination/sourcing-scoring-rubric.md) (methodology, to `founder_connected_screen_artifact_id`)<br>[`vc.document.outreach_queue_template`](../alludium/documents/origination/outreach-queue-template.md) (output_template)<br>[`vc.document.origination_source_strategy_guide`](../alludium/documents/origination/origination-source-strategy-guide.md) (methodology)<br>[`vc.document.template_use_guidance`](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | None declared |

## Initial Reachout Linkedin

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| [Prepare Initial LinkedIn Reachout](../tasks/prepare-initial-linkedin-reachout.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [`vc-outreach-draft-queue`](../skills/vc-outreach-draft-queue/SKILL.md)<br>[`founder-outreach-and-intro-paths`](../skills/founder-outreach-and-intro-paths/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | [`vc.document.outreach_queue_template`](../alludium/documents/origination/outreach-queue-template.md) (output_template, to `initial_linkedin_reachout_artifact_id`)<br>[`vc.document.origination_source_strategy_guide`](../alludium/documents/origination/origination-source-strategy-guide.md) (methodology)<br>[`vc.document.template_use_guidance`](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | None declared |

## Second Reachout Email

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| [Prepare Second Reachout Email](../tasks/prepare-second-reachout-email.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [`vc-outreach-draft-queue`](../skills/vc-outreach-draft-queue/SKILL.md)<br>[`founder-outreach-and-intro-paths`](../skills/founder-outreach-and-intro-paths/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | [`vc.document.outreach_queue_template`](../alludium/documents/origination/outreach-queue-template.md) (output_template, to `second_reachout_email_artifact_id`)<br>[`vc.document.origination_source_strategy_guide`](../alludium/documents/origination/origination-source-strategy-guide.md) (methodology)<br>[`vc.document.template_use_guidance`](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | None declared |
| [Review Outreach Outcome](../tasks/review-outreach-outcome.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [`vc-origination-deal-room-promotion`](../skills/vc-origination-deal-room-promotion/SKILL.md)<br>[`vc-outreach-draft-queue`](../skills/vc-outreach-draft-queue/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | [`vc.document.promotion_package_template`](../alludium/documents/origination/promotion-package-template.md) (output_template, to `outreach_outcome_artifact_id`)<br>[`vc.document.origination_source_strategy_guide`](../alludium/documents/origination/origination-source-strategy-guide.md) (methodology)<br>[`vc.document.template_use_guidance`](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | None declared |

## No Response

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| None mapped | None declared | None declared | None declared | None declared |

## Engaged Added To Deal Funnel

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| [Promote Candidate to Deal Pipeline](../tasks/promote-candidate-to-deal-room.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [`vc-origination-deal-room-promotion`](../skills/vc-origination-deal-room-promotion/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md)<br>[`deal-room-setup-and-source-ingestion`](../skills/deal-room-setup-and-source-ingestion/SKILL.md) | [`vc.document.promotion_package_template`](../alludium/documents/origination/promotion-package-template.md) (output_template, to `promotion_package_artifact_id`)<br>[`vc.document.origination_source_strategy_guide`](../alludium/documents/origination/origination-source-strategy-guide.md) (methodology)<br>[`vc.document.template_use_guidance`](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | None declared |

## Pass

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| None mapped | None declared | None declared | None declared | None declared |

## Watchlist

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| None mapped | None declared | None declared | None declared | None declared |

## Paused

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| None mapped | None declared | None declared | None declared | None declared |

## Migration In Progress

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| None mapped | None declared | None declared | None declared | None declared |

## Archived

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| None mapped | None declared | None declared | None declared | None declared |
