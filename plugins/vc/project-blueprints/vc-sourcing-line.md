---
projectType: vc_sourcing_line
title: Sourcing Line Blueprint
source: alludium/project-types/vc_sourcing_line.json
---

> **GENERATED FILE**
> Source: `alludium/project-types/vc_sourcing_line.json`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Sourcing Line Blueprint

A first-class, measurable origination experiment with its own chat, source mix, screen, cadence, review policy, outreach boundary, schedules, receipts, and performance history.

This blueprint lists setup, support, and workflow-stage tasks with the recommended agents, task-referenced skills, document references, and integration surfaces for this project type. General and support sections are included only when they contain cross-cutting tasks that are not already mapped to a workflow stage.

## Setup

Project-type setup and configuration tasks used before normal project execution.

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| [Configure Sourcing Line](../tasks/configure-sourcing-line.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [Origination Pipeline Orchestration](../skills/origination-pipeline-orchestration/SKILL.md)<br>[VC Source Registry & State Management](../skills/vc-source-registry-and-state-management/SKILL.md) | [Sourcing Line Template Catalog](../alludium/documents/origination/sourcing-line-template-catalog.md) (methodology)<br>[Source Registry Template](../alludium/documents/origination/source-registry-template.md) (operating_guidance)<br>[Origination Pipeline Operating SOP](../alludium/documents/origination/origination-pipeline-sop.md) (operating_guidance) | None declared |
| [Create Sourcing Line](../tasks/create-sourcing-line.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [Origination Pipeline Orchestration](../skills/origination-pipeline-orchestration/SKILL.md) | None declared | None declared |
| [VC Pack Variable Discovery](../tasks/vc-pack-variable-discovery.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | None declared | None declared | None declared |

## Integration Support

Connector discovery, preview, and read-only integration support tasks used to configure or inspect source surfaces without making them part of the VC workflow.

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| [Explore Apify Origination Sources](../tasks/apify-discovery.md) | [Integration Operator](../agents/vc-integration-operator.md) | [VC Apify Discovery](../skills/vc-apify-discovery/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | None declared | `apify-actors-mcp` |
| [Preview Apify Origination Results](../tasks/apify-sync-read.md) | [Integration Operator](../agents/vc-integration-operator.md) | [VC Apify Sync Read](../skills/vc-apify-sync-read/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | None declared | `apify-actors-mcp` |
| [Set Up Apify for Origination](../tasks/apify-setup.md) | [Integration Operator](../agents/vc-integration-operator.md) | [VC Apify Discovery](../skills/vc-apify-discovery/SKILL.md)<br>[VC Apify Sync Read](../skills/vc-apify-sync-read/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | None declared | `apify-actors-mcp` |

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
| [Run Sourcing Line](../tasks/run-vc-sourcing-pipeline.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [Origination Pipeline Orchestration](../skills/origination-pipeline-orchestration/SKILL.md)<br>[VC Source Registry & State Management](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | [Candidate Batch Template](../alludium/documents/origination/candidate-batch-template.md) (output_template, to `candidate_batch_artifact_id`)<br>[Origination Pipeline Operating SOP](../alludium/documents/origination/origination-pipeline-sop.md) (operating_guidance)<br>[Origination Source Strategy Guide](../alludium/documents/origination/origination-source-strategy-guide.md) (methodology)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | None declared |

## Degraded

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| [Review Source Errors and Spend](../tasks/review-source-errors-and-spend.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC Source Error & Spend Audit](../skills/vc-source-error-and-spend-audit/SKILL.md)<br>[VC Source Registry & State Management](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | [Source Health Review Checklist](../alludium/documents/origination/source-health-review-checklist.md) (output_template, to `source_health_artifact_id`)<br>[Paid Source Spend Audit Checklist](../alludium/documents/origination/paid-source-spend-audit-checklist.md) (checklist)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | None declared |

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
