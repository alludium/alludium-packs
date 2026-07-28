---
projectType: vc_origination_pipeline
title: Origination Pipeline Blueprint
source: alludium/project-types/vc_origination_pipeline.json
---

> **GENERATED FILE**
> Source: `alludium/project-types/vc_origination_pipeline.json`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Origination Pipeline Blueprint

The fund-level origination control plane for shared source connections, thesis and review policy, budgets, cross-line Inbox and digest, and creation of first-class Sourcing Lines.

This blueprint lists setup, support, and workflow-stage tasks with the recommended agents, task-referenced skills, document references, and integration surfaces for this project type. General and support sections are included only when they contain cross-cutting tasks that are not already mapped to a workflow stage.

## Setup

Project-type setup and configuration tasks used before normal project execution.

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| [Configure Origination Pipeline](../tasks/configure-origination-pipeline.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [Origination Pipeline Orchestration](../skills/origination-pipeline-orchestration/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | [Origination Pipeline Operating SOP](../alludium/documents/origination/origination-pipeline-sop.md) (operating_guidance)<br>[Origination Source Strategy Guide](../alludium/documents/origination/origination-source-strategy-guide.md) (methodology)<br>[Source Registry Template](../alludium/documents/origination/source-registry-template.md) (operating_guidance)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | None declared |
| [VC Pack Variable Discovery](../tasks/vc-pack-variable-discovery.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | None declared | None declared | None declared |
| [Set Up Apify for Origination](../tasks/apify-setup.md) | [Integration Operator](../agents/vc-integration-operator.md) | [VC Apify Discovery](../skills/vc-apify-discovery/SKILL.md)<br>[VC Apify Sync Read](../skills/vc-apify-sync-read/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | None declared | `apify-actors-mcp` |
| [Configure Companies House Public Register Preview](../tasks/companies-house-setup.md) | [Integration Operator](../agents/vc-integration-operator.md) | [VC Companies House Sourcing](../skills/vc-companies-house-sourcing/SKILL.md)<br>[VC Companies House Sync Read](../skills/vc-companies-house-sync-read/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | None declared | `firecrawl-mcp-hosted` |

## Integration Support

Connector discovery, preview, and read-only integration support tasks used to configure or inspect source surfaces without making them part of the VC workflow.

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| [Explore Apify Origination Sources](../tasks/apify-discovery.md) | [Integration Operator](../agents/vc-integration-operator.md) | [VC Apify Discovery](../skills/vc-apify-discovery/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | None declared | `apify-actors-mcp` |
| [Explore Companies House Public Register Scope](../tasks/companies-house-discovery.md) | [Integration Operator](../agents/vc-integration-operator.md) | [VC Companies House Sourcing](../skills/vc-companies-house-sourcing/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | None declared | `firecrawl-mcp-hosted` |
| [Preview Apify Origination Results](../tasks/apify-sync-read.md) | [Integration Operator](../agents/vc-integration-operator.md) | [VC Apify Sync Read](../skills/vc-apify-sync-read/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | None declared | `apify-actors-mcp` |
| [Preview Companies House Public Register Results](../tasks/companies-house-sync-read.md) | [Integration Operator](../agents/vc-integration-operator.md) | [VC Companies House Sync Read](../skills/vc-companies-house-sync-read/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | None declared | `firecrawl-mcp-hosted` |

## Pipeline Management

VC-specific operating and management tasks that support pipeline health, source operations, or review artifacts outside the candidate workflow.

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| [Prepare Lead Gen Packet](../tasks/prepare-lead-gen-packet.md) | [Origination Scout](../agents/vc-origination-scout.md) | [Company Research & Enrichment](../skills/company-research-and-enrichment/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | [Lead Generation Packet Template](../alludium/documents/deal-room/lead-generation-packet-template.md) (output_template, to `lead_generation_packet_artifact_id`)<br>[Origination Source Strategy Guide](../alludium/documents/origination/origination-source-strategy-guide.md) (methodology)<br>[Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.md) (style_guide)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | `alludium-platform`<br>`harmonic-mcp-oauth`<br>`affinity-mcp-server`<br>`exa-mcp-hosted`<br>`brave-search-mcp`<br>`serpapi-mcp`<br>`firecrawl-mcp-hosted`<br>`dealroom-mcp`<br>`linkedin` |

## Draft

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| None mapped | None declared | None declared | None declared | None declared |

## Configured

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| None mapped | None declared | None declared | None declared | None declared |

## Active

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| [Generate Sourcing Digest](../tasks/generate-sourcing-digest.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC Sourcing Digest Generation](../skills/vc-sourcing-digest-generation/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | [Sourcing Digest Template](../alludium/documents/origination/sourcing-digest-template.md) (output_template, to `sourcing_digest_artifact_id`)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | None declared |

## Degraded

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| [Review Source Errors and Spend](../tasks/review-source-errors-and-spend.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC Source Error & Spend Audit](../skills/vc-source-error-and-spend-audit/SKILL.md)<br>[VC Source Registry & State Management](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | [Source Health Review Checklist](../alludium/documents/origination/source-health-review-checklist.md) (output_template, to `source_health_artifact_id`)<br>[Paid Source Spend Audit Checklist](../alludium/documents/origination/paid-source-spend-audit-checklist.md) (checklist)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | None declared |

## Paused

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| None mapped | None declared | None declared | None declared | None declared |

## Archived

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| None mapped | None declared | None declared | None declared | None declared |
