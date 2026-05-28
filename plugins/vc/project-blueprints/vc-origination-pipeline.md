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

This blueprint lists setup, support, and workflow-stage tasks with the recommended agents, task-referenced skills, document references, and integration surfaces for this project type. General and support sections are included only when they contain cross-cutting tasks that are not already mapped to a workflow stage.

## Setup

Project-type setup and configuration tasks used before normal project execution.

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| [Configure Origination Pipeline](../tasks/configure-origination-pipeline.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [Origination Pipeline Orchestration](../skills/origination-pipeline-orchestration/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | [Origination Pipeline Operating SOP](../alludium/documents/origination/origination-pipeline-sop.md) (operating_guidance)<br>[Origination Source Strategy Guide](../alludium/documents/origination/origination-source-strategy-guide.md) (methodology)<br>[Source Registry Template](../alludium/documents/origination/source-registry-template.md) (operating_guidance)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | None declared |
| [VC Pack Variable Discovery](../tasks/vc-pack-variable-discovery.md) | [Origination Scout](../agents/vc-origination-scout.md) | None declared | None declared | `alludium-platform`<br>`harmonic-mcp-oauth`<br>`affinity-mcp-server`<br>`exa-mcp-hosted`<br>`brave-search-mcp`<br>`serpapi-mcp`<br>`firecrawl-mcp-hosted`<br>`dealroom-mcp`<br>`linkedin` |
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
| [Review Source Errors and Spend](../tasks/review-source-errors-and-spend.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC Source Error & Spend Audit](../skills/vc-source-error-and-spend-audit/SKILL.md)<br>[VC Source Registry & State Management](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | [Source Health Review Checklist](../alludium/documents/origination/source-health-review-checklist.md) (output_template, to `source_health_artifact_id`)<br>[Paid Source Spend Audit Checklist](../alludium/documents/origination/paid-source-spend-audit-checklist.md) (checklist)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | None declared |
| [Prepare Lead Gen Packet](../tasks/prepare-lead-gen-packet.md) | [Origination Scout](../agents/vc-origination-scout.md) | [Company Research & Enrichment](../skills/company-research-and-enrichment/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | [Lead Generation Packet Template](../alludium/documents/deal-room/lead-generation-packet-template.md) (output_template, to `lead_generation_packet_artifact_id`)<br>[Origination Source Strategy Guide](../alludium/documents/origination/origination-source-strategy-guide.md) (methodology)<br>[Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.md) (style_guide)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | `alludium-platform`<br>`harmonic-mcp-oauth`<br>`affinity-mcp-server`<br>`exa-mcp-hosted`<br>`brave-search-mcp`<br>`serpapi-mcp`<br>`firecrawl-mcp-hosted`<br>`dealroom-mcp`<br>`linkedin` |

## Source

Run approved sourcing routes and produce raw candidate batches.

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| [Run VC Sourcing Pipeline](../tasks/run-vc-sourcing-pipeline.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [Origination Pipeline Orchestration](../skills/origination-pipeline-orchestration/SKILL.md)<br>[VC Source Registry & State Management](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | [Candidate Batch Template](../alludium/documents/origination/candidate-batch-template.md) (output_template, to `candidate_batch_artifact_id`)<br>[Origination Pipeline Operating SOP](../alludium/documents/origination/origination-pipeline-sop.md) (operating_guidance)<br>[Origination Source Strategy Guide](../alludium/documents/origination/origination-source-strategy-guide.md) (methodology)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | None declared |
| [Discover Companies House Candidates](../tasks/discover-companies-house-candidates.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC Companies House Sourcing](../skills/vc-companies-house-sourcing/SKILL.md)<br>[VC Source Registry & State Management](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | None declared | None declared |
| [Discover LinkedIn Founder Candidates](../tasks/discover-linkedin-founder-candidates.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC Apify LinkedIn Founder Discovery](../skills/vc-apify-linkedin-founder-discovery/SKILL.md)<br>[VC Source Registry & State Management](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | None declared | None declared |
| [Discover X Founder Signals](../tasks/discover-x-founder-signals.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC Apify X Founder Discovery](../skills/vc-apify-x-founder-discovery/SKILL.md)<br>[VC Source Registry & State Management](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | None declared | None declared |
| [Discover GitHub Builder Signals](../tasks/discover-github-builder-signals.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC GitHub Builder Signal Discovery](../skills/vc-github-builder-signal-discovery/SKILL.md)<br>[VC Source Registry & State Management](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | None declared | None declared |
| [Discover Reddit Builder Signals](../tasks/discover-reddit-builder-signals.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC Reddit Builder Signal Discovery](../skills/vc-reddit-builder-signal-discovery/SKILL.md)<br>[VC Source Registry & State Management](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | None declared | None declared |
| [Generate Sourcing Digest](../tasks/generate-sourcing-digest.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC Sourcing Digest Generation](../skills/vc-sourcing-digest-generation/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | [Sourcing Digest Template](../alludium/documents/origination/sourcing-digest-template.md) (output_template, to `sourcing_digest_artifact_id`)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | None declared |
| [Audit LinkedIn Query Spend](../tasks/audit-linkedin-query-spend.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC LinkedIn Query Spend Audit](../skills/vc-linkedin-query-spend-audit/SKILL.md)<br>[VC Source Registry & State Management](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | [Paid Source Spend Audit Checklist](../alludium/documents/origination/paid-source-spend-audit-checklist.md) (output_template, to `linkedin_spend_audit_artifact_id`)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | None declared |
| [Source Thesis Targets](../tasks/source-thesis-targets.md) | [Origination Scout](../agents/vc-origination-scout.md) | [Company Research & Enrichment](../skills/company-research-and-enrichment/SKILL.md)<br>[Founder Outreach & Intro Paths](../skills/founder-outreach-and-intro-paths/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | [Thesis Target List Template](../alludium/documents/deal-room/thesis-target-list-template.md) (output_template, to `thesis_target_list_artifact_id`)<br>[Origination Source Strategy Guide](../alludium/documents/origination/origination-source-strategy-guide.md) (methodology)<br>[Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.md) (style_guide)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | `alludium-platform`<br>`harmonic-mcp-oauth`<br>`affinity-mcp-server`<br>`exa-mcp-hosted`<br>`brave-search-mcp`<br>`serpapi-mcp`<br>`firecrawl-mcp-hosted`<br>`dealroom-mcp`<br>`linkedin` |

## Identify

Normalize raw leads into candidate records with stable identity and dedupe context.

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| [Review Reddit Candidate Inbox](../tasks/review-reddit-candidate-inbox.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC Reddit Inbox Approval](../skills/vc-reddit-inbox-approval/SKILL.md)<br>[VC Sourcing Dedupe & Novelty Check](../skills/vc-sourcing-dedupe-and-novelty-check/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | None declared | None declared |
| [Ingest Manual Sourcing Tip](../tasks/ingest-manual-sourcing-tip.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC Manual Tip Ingestion](../skills/vc-manual-tip-ingestion/SKILL.md)<br>[VC Sourcing Dedupe & Novelty Check](../skills/vc-sourcing-dedupe-and-novelty-check/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | None declared | None declared |
| [Sync Sourcing Candidate](../tasks/sync-sourcing-candidate.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC Source Registry & State Management](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[VC Sourcing Dedupe & Novelty Check](../skills/vc-sourcing-dedupe-and-novelty-check/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md)<br>[VC Notion Sync Write](../skills/vc-notion-sync-write/SKILL.md) | None declared | None declared |

## Enrich

Add web, founder, relationship, CRM, and evidence context before judgment.

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| [Enrich Sourcing Candidate](../tasks/enrich-sourcing-candidate.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC Sourcing Candidate Enrichment](../skills/vc-sourcing-candidate-enrichment/SKILL.md)<br>[VC Sourcing Dedupe & Novelty Check](../skills/vc-sourcing-dedupe-and-novelty-check/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | None declared | None declared |
| [Check Affinity Relationship Context](../tasks/check-affinity-relationship-context.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC Relationship Context Check](../skills/vc-relationship-context-check/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | None declared | None declared |

## Initial Screen

Apply a lightweight thesis, stage, geography, and hard-exclusion screen.

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| [Score Sourcing Candidate](../tasks/score-sourcing-candidate.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC Sourcing Verdict & Screening](../skills/vc-sourcing-verdict-and-screening/SKILL.md)<br>[VC Sourcing Dedupe & Novelty Check](../skills/vc-sourcing-dedupe-and-novelty-check/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | [Sourcing Scoring Rubric](../alludium/documents/origination/sourcing-scoring-rubric.md) (methodology, to `scoring_artifact_id`)<br>[Origination Source Strategy Guide](../alludium/documents/origination/origination-source-strategy-guide.md) (methodology)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | None declared |
| [Screen Identified Candidate](../tasks/screen-identified-candidate.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC Sourcing Verdict & Screening](../skills/vc-sourcing-verdict-and-screening/SKILL.md)<br>[VC Sourcing Dedupe & Novelty Check](../skills/vc-sourcing-dedupe-and-novelty-check/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | [Sourcing Scoring Rubric](../alludium/documents/origination/sourcing-scoring-rubric.md) (methodology, to `identified_screen_artifact_id`)<br>[Origination Source Strategy Guide](../alludium/documents/origination/origination-source-strategy-guide.md) (methodology)<br>[Dedupe And Novelty Policy](../alludium/documents/origination/dedupe-novelty-policy.md) (policy)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | None declared |

## Prioritize

Rank and stress-test screened candidates for active outreach.

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| [Review Portfolio Overlap](../tasks/review-portfolio-overlap.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC Portfolio Overlap Review](../skills/vc-portfolio-overlap-review/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md)<br>[VC Relationship Context Check](../skills/vc-relationship-context-check/SKILL.md) | None declared | None declared |
| [Run Deal Fit Analysis](../tasks/run-deal-fit-analysis.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC Sourcing Verdict & Screening](../skills/vc-sourcing-verdict-and-screening/SKILL.md)<br>[Investment Screening Framework](../skills/investment-screening-framework/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | [Sourcing Scoring Rubric](../alludium/documents/origination/sourcing-scoring-rubric.md) (methodology, to `deal_fit_artifact_id`)<br>[Investment Screening Framework](../alludium/documents/shared/investment-screening-framework.md) (methodology)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | None declared |
| [Screen Active Sourcing Candidate](../tasks/screen-active-sourcing-candidate.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC Sourcing Verdict & Screening](../skills/vc-sourcing-verdict-and-screening/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md)<br>[Investment Screening Framework](../skills/investment-screening-framework/SKILL.md) | [Sourcing Scoring Rubric](../alludium/documents/origination/sourcing-scoring-rubric.md) (methodology, to `screening_artifact_id`)<br>[Origination Source Strategy Guide](../alludium/documents/origination/origination-source-strategy-guide.md) (methodology)<br>[Dedupe And Novelty Policy](../alludium/documents/origination/dedupe-novelty-policy.md) (policy)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | None declared |
| [Review Unicorn Signature](../tasks/review-unicorn-signature.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC Sourcing Verdict & Screening](../skills/vc-sourcing-verdict-and-screening/SKILL.md)<br>[Origination Prospect Summary Preparation](../skills/origination-prospect-summary-preparation/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | [Sourcing Scoring Rubric](../alludium/documents/origination/sourcing-scoring-rubric.md) (methodology, to `unicorn_signature_artifact_id`)<br>[Prospect Summary Template](../alludium/documents/origination/sourcing-ic-summary-template.md) (operating_guidance)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | None declared |

## Outreach Prep

Prepare prospect summaries and approved outreach queues before contact attempts.

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| [Prepare Prospect Summary](../tasks/prepare-prospect-summary.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [Origination Prospect Summary Preparation](../skills/origination-prospect-summary-preparation/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | [Prospect Summary Template](../alludium/documents/origination/sourcing-ic-summary-template.md) (output_template, to `prospect_summary_artifact_id`)<br>[Origination Source Strategy Guide](../alludium/documents/origination/origination-source-strategy-guide.md) (methodology)<br>[Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.md) (style_guide)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | None declared |
| [Prepare Outreach Draft Queue](../tasks/prepare-outreach-draft-queue.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC Outreach Draft Queue](../skills/vc-outreach-draft-queue/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md)<br>[Founder Outreach & Intro Paths](../skills/founder-outreach-and-intro-paths/SKILL.md) | [Outreach Queue Template](../alludium/documents/origination/outreach-queue-template.md) (output_template, to `outreach_queue_artifact_id`)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | None declared |

## Contact Attempts

Track human-approved outreach attempts across LinkedIn, email, warm intros, or other channels.

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| [Record LinkedIn Connection Attempt](../tasks/record-linkedin-connection-attempt.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC Outreach Draft Queue](../skills/vc-outreach-draft-queue/SKILL.md)<br>[Founder Outreach & Intro Paths](../skills/founder-outreach-and-intro-paths/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | [Outreach Queue Template](../alludium/documents/origination/outreach-queue-template.md) (output_template, to `connection_record_artifact_id`)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | None declared |
| [Prepare Initial LinkedIn Reachout](../tasks/prepare-initial-linkedin-reachout.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC Outreach Draft Queue](../skills/vc-outreach-draft-queue/SKILL.md)<br>[Founder Outreach & Intro Paths](../skills/founder-outreach-and-intro-paths/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | [Outreach Queue Template](../alludium/documents/origination/outreach-queue-template.md) (output_template, to `initial_linkedin_reachout_artifact_id`)<br>[Origination Source Strategy Guide](../alludium/documents/origination/origination-source-strategy-guide.md) (methodology)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | None declared |
| [Prepare Second Reachout Email](../tasks/prepare-second-reachout-email.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC Outreach Draft Queue](../skills/vc-outreach-draft-queue/SKILL.md)<br>[Founder Outreach & Intro Paths](../skills/founder-outreach-and-intro-paths/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | [Outreach Queue Template](../alludium/documents/origination/outreach-queue-template.md) (output_template, to `second_reachout_email_artifact_id`)<br>[Origination Source Strategy Guide](../alludium/documents/origination/origination-source-strategy-guide.md) (methodology)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | None declared |

## Founder Engagement Screen

Re-screen after founder response, connection, or direct relationship context adds new evidence.

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| [Screen Founder-Connected Candidate](../tasks/screen-founder-connected-candidate.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [VC Sourcing Verdict & Screening](../skills/vc-sourcing-verdict-and-screening/SKILL.md)<br>[VC Outreach Draft Queue](../skills/vc-outreach-draft-queue/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md)<br>[Investment Screening Framework](../skills/investment-screening-framework/SKILL.md) | [Sourcing Scoring Rubric](../alludium/documents/origination/sourcing-scoring-rubric.md) (methodology, to `founder_connected_screen_artifact_id`)<br>[Outreach Queue Template](../alludium/documents/origination/outreach-queue-template.md) (output_template)<br>[Origination Source Strategy Guide](../alludium/documents/origination/origination-source-strategy-guide.md) (methodology)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | None declared |
| [Review Outreach Outcome](../tasks/review-outreach-outcome.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [Origination Deal Pipeline Promotion](../skills/origination-deal-pipeline-promotion/SKILL.md)<br>[VC Outreach Draft Queue](../skills/vc-outreach-draft-queue/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | [Promotion Package Template](../alludium/documents/origination/promotion-package-template.md) (output_template, to `outreach_outcome_artifact_id`)<br>[Origination Source Strategy Guide](../alludium/documents/origination/origination-source-strategy-guide.md) (methodology)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | None declared |

## Added To Deal Pipeline

Candidate has engaged and is handed into a Deal Pipeline project with an approved promotion package.

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| [Promote Candidate to Deal Pipeline](../tasks/promote-candidate-to-deal-pipeline.md) | [Sourcing Operator](../agents/vc-sourcing-operator.md) | [Origination Deal Pipeline Promotion](../skills/origination-deal-pipeline-promotion/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md)<br>[Deal Pipeline Setup & Source Ingestion](../skills/deal-pipeline-setup-and-source-ingestion/SKILL.md) | [Promotion Package Template](../alludium/documents/origination/promotion-package-template.md) (output_template, to `promotion_package_artifact_id`)<br>[Origination Source Strategy Guide](../alludium/documents/origination/origination-source-strategy-guide.md) (methodology)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | None declared |

## No Response

Candidate has not responded after the approved contact sequence.

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| None mapped | None declared | None declared | None declared | None declared |

## Pass

Terminal no-fit or not-now outcome with cited rationale.

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| None mapped | None declared | None declared | None declared | None declared |

## Watchlist

Hold candidates worth revisiting but not active for outreach now.

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| None mapped | None declared | None declared | None declared | None declared |
