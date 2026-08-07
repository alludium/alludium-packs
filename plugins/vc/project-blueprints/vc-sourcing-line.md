---
projectType: vc_sourcing_line
title: Sourcing Line Blueprint
source: alludium/project-types/vc_sourcing_line.json
---

> **GENERATED FILE**
> Source: `alludium/project-types/vc_sourcing_line.json`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Sourcing Line Blueprint

A fund-specific, measurable origination experiment with its own sources, screen, cadence, evidence receipts, review policy, and learning history.

This blueprint lists setup, support, and workflow-stage tasks with the recommended agents, task-referenced skills, document references, and integration surfaces for this project type. General and support sections are included only when they contain cross-cutting tasks that are not already mapped to a workflow stage.

## Setup

Project-type setup and configuration tasks used before normal project execution.

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| [Configure Sourcing Line](../tasks/configure-sourcing-line.md) | [Sourcing Line Manager](../agents/vc-sourcing-line-manager.md) | [Origination Pipeline Orchestration](../skills/origination-pipeline-orchestration/SKILL.md)<br>[VC Source Registry & State Management](../skills/vc-source-registry-and-state-management/SKILL.md) | [Source Registry Template](../alludium/documents/origination/source-registry-template.html) (operating_guidance)<br>[Origination Source Strategy Guide](../alludium/documents/origination/origination-source-strategy-guide.html) (methodology) | `alludium-platform` |
| [Create Sourcing Line](../tasks/create-sourcing-line.md) | [Sourcing Line Manager](../agents/vc-sourcing-line-manager.md) | [Origination Pipeline Orchestration](../skills/origination-pipeline-orchestration/SKILL.md) | None declared | `alludium-platform` |
| [VC Pack Variable Discovery](../tasks/vc-pack-variable-discovery.md) | [Sourcing Line Manager](../agents/vc-sourcing-line-manager.md) | None declared | None declared | `alludium-platform` |

## Integration Support

Connector discovery, preview, and read-only integration support tasks used to configure or inspect source surfaces without making them part of the VC workflow.

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| [Configure Companies House Public Register Preview](../tasks/companies-house-setup.md) | [Integration Operator](../agents/vc-integration-operator.md) | [VC Companies House Sourcing](../skills/vc-companies-house-sourcing/SKILL.md)<br>[VC Companies House Sync Read](../skills/vc-companies-house-sync-read/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | None declared | `firecrawl-mcp-hosted` |
| [Explore Apify Origination Sources](../tasks/apify-discovery.md) | [Integration Operator](../agents/vc-integration-operator.md) | [VC Apify Discovery](../skills/vc-apify-discovery/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | None declared | `apify-actors-mcp` |
| [Explore Companies House Public Register Scope](../tasks/companies-house-discovery.md) | [Integration Operator](../agents/vc-integration-operator.md) | [VC Companies House Sourcing](../skills/vc-companies-house-sourcing/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | None declared | `firecrawl-mcp-hosted` |
| [Preview Apify Origination Results](../tasks/apify-sync-read.md) | [Integration Operator](../agents/vc-integration-operator.md) | [VC Apify Sync Read](../skills/vc-apify-sync-read/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | None declared | `apify-actors-mcp` |
| [Preview Companies House Public Register Results](../tasks/companies-house-sync-read.md) | [Integration Operator](../agents/vc-integration-operator.md) | [VC Companies House Sync Read](../skills/vc-companies-house-sync-read/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | None declared | `firecrawl-mcp-hosted` |
| [Set Up Apify for Origination](../tasks/apify-setup.md) | [Integration Operator](../agents/vc-integration-operator.md) | [VC Apify Discovery](../skills/vc-apify-discovery/SKILL.md)<br>[VC Apify Sync Read](../skills/vc-apify-sync-read/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | None declared | `apify-actors-mcp` |

## Pipeline Management

VC-specific operating and management tasks that support pipeline health, source operations, or review artifacts outside the candidate workflow.

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| [Prepare Lead Gen Packet](../tasks/prepare-lead-gen-packet.md) | [Origination Scout](../agents/vc-origination-scout.md) | [Company Research & Enrichment](../skills/company-research-and-enrichment/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | [Lead Generation Packet Template](../alludium/documents/deal-room/lead-generation-packet-template.html) (output_template, to `lead_generation_packet_artifact_id`)<br>[Origination Source Strategy Guide](../alludium/documents/origination/origination-source-strategy-guide.html) (methodology)<br>[Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.html) (style_guide)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.html) (operating_guidance) | `alludium-platform`<br>`harmonic-mcp-oauth`<br>`affinity-mcp-server`<br>`exa-mcp-hosted`<br>`brave-search-mcp`<br>`serpapi-mcp`<br>`firecrawl-mcp-hosted`<br>`dealroom-mcp`<br>`linkedin` |

## Draft

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| None mapped | None declared | None declared | None declared | None declared |

## Ready

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| None mapped | None declared | None declared | None declared | None declared |

## Active

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| [Link Existing Origination Candidate](../tasks/link-existing-origination-candidate.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC Sourcing Dedupe & Novelty Check](../skills/vc-sourcing-dedupe-and-novelty-check/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | [Dedupe And Novelty Policy](../alludium/documents/origination/dedupe-novelty-policy.html) (policy) | `alludium-platform`<br>`affinity-mcp-server` |
| [Run VC Sourcing Pipeline](../tasks/run-vc-sourcing-pipeline.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [Origination Pipeline Orchestration](../skills/origination-pipeline-orchestration/SKILL.md)<br>[VC Source Registry & State Management](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | [Candidate Batch Template](../alludium/documents/origination/candidate-batch-template.html) (output_template, to `candidate_batch_artifact_id`)<br>[Origination Operating SOP](../alludium/documents/origination/origination-pipeline-sop.html) (operating_guidance)<br>[Origination Source Strategy Guide](../alludium/documents/origination/origination-source-strategy-guide.html) (methodology)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.html) (operating_guidance) | `alludium-platform`<br>`affinity-mcp-server` |
| [Discover Companies House Candidates](../tasks/discover-companies-house-candidates.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC Companies House Sourcing](../skills/vc-companies-house-sourcing/SKILL.md)<br>[VC Source Registry & State Management](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | None declared | `alludium-platform`<br>`affinity-mcp-server` |
| [Discover LinkedIn Founder Candidates](../tasks/discover-linkedin-founder-candidates.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC Apify LinkedIn Founder Discovery](../skills/vc-apify-linkedin-founder-discovery/SKILL.md)<br>[VC Source Registry & State Management](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | None declared | `alludium-platform`<br>`affinity-mcp-server` |
| [Discover X Founder Signals](../tasks/discover-x-founder-signals.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC Apify X Founder Discovery](../skills/vc-apify-x-founder-discovery/SKILL.md)<br>[VC Source Registry & State Management](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | None declared | `alludium-platform`<br>`affinity-mcp-server` |
| [Discover GitHub Builder Signals](../tasks/discover-github-builder-signals.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC GitHub Builder Signal Discovery](../skills/vc-github-builder-signal-discovery/SKILL.md)<br>[VC Source Registry & State Management](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | None declared | `alludium-platform`<br>`affinity-mcp-server` |
| [Discover Reddit Builder Signals](../tasks/discover-reddit-builder-signals.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC Reddit Builder Signal Discovery](../skills/vc-reddit-builder-signal-discovery/SKILL.md)<br>[VC Source Registry & State Management](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | None declared | `alludium-platform`<br>`affinity-mcp-server` |
| [Ingest Manual Sourcing Tip](../tasks/ingest-manual-sourcing-tip.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC Manual Tip Ingestion](../skills/vc-manual-tip-ingestion/SKILL.md)<br>[VC Sourcing Dedupe & Novelty Check](../skills/vc-sourcing-dedupe-and-novelty-check/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | None declared | `alludium-platform`<br>`affinity-mcp-server` |
| [Review Reddit Candidate Inbox](../tasks/review-reddit-candidate-inbox.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC Reddit Inbox Approval](../skills/vc-reddit-inbox-approval/SKILL.md)<br>[VC Sourcing Dedupe & Novelty Check](../skills/vc-sourcing-dedupe-and-novelty-check/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | None declared | `alludium-platform`<br>`affinity-mcp-server` |
| [Audit LinkedIn Query Spend](../tasks/audit-linkedin-query-spend.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC LinkedIn Query Spend Audit](../skills/vc-linkedin-query-spend-audit/SKILL.md)<br>[VC Source Registry & State Management](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | [Paid Source Spend Audit Checklist](../alludium/documents/origination/paid-source-spend-audit-checklist.html) (output_template, to `linkedin_spend_audit_artifact_id`)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.html) (operating_guidance) | `alludium-platform`<br>`affinity-mcp-server` |
| [Source Thesis Targets](../tasks/source-thesis-targets.md) | [Origination Scout](../agents/vc-origination-scout.md) | [Company Research & Enrichment](../skills/company-research-and-enrichment/SKILL.md)<br>[Founder Outreach & Intro Paths](../skills/founder-outreach-and-intro-paths/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | [Thesis Target List Template](../alludium/documents/deal-room/thesis-target-list-template.html) (output_template, to `thesis_target_list_artifact_id`)<br>[Origination Source Strategy Guide](../alludium/documents/origination/origination-source-strategy-guide.html) (methodology)<br>[Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.html) (style_guide)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.html) (operating_guidance) | `alludium-platform`<br>`harmonic-mcp-oauth`<br>`affinity-mcp-server`<br>`exa-mcp-hosted`<br>`brave-search-mcp`<br>`serpapi-mcp`<br>`firecrawl-mcp-hosted`<br>`dealroom-mcp`<br>`linkedin` |

## Degraded

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| [Review Source Errors and Spend](../tasks/review-source-errors-and-spend.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC Source Error & Spend Audit](../skills/vc-source-error-and-spend-audit/SKILL.md)<br>[VC Source Registry & State Management](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | [Source Health Review Checklist](../alludium/documents/origination/source-health-review-checklist.html) (output_template, to `source_health_artifact_id`)<br>[Paid Source Spend Audit Checklist](../alludium/documents/origination/paid-source-spend-audit-checklist.html) (checklist)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.html) (operating_guidance) | `alludium-platform`<br>`affinity-mcp-server` |

## Paused

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| None mapped | None declared | None declared | None declared | None declared |

## Retired

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| None mapped | None declared | None declared | None declared | None declared |

## Archived

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| None mapped | None declared | None declared | None declared | None declared |
