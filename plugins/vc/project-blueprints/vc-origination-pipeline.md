---
projectType: vc_origination_pipeline
title: VC Origination Pipeline Blueprint
source: alludium/project-types/vc_origination_pipeline.json
---

> **GENERATED FILE**
> Source: `alludium/project-types/vc_origination_pipeline.json`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# VC Origination Pipeline Blueprint

Project context for a standing venture sourcing pipeline that configures source coverage, credential readiness, review policy, and promotion thresholds before recurring sourcing work is enabled.

This blueprint lists the project stages, mapped tasks, recommended agents, and task-referenced skills for this project type.

## Project Setup / General

| Task | Agent | Skills | Task ID |
| --- | --- | --- | --- |
| Project Source Choice | [Origination Scout](../agents/vc-origination-scout.md) | None declared | `alludium.project_source_choice` |
| Project Variable Review | [Origination Scout](../agents/vc-origination-scout.md) | None declared | `alludium.project_variable_review` |
| Project Schedule Review | [Origination Scout](../agents/vc-origination-scout.md) | None declared | `alludium.project_schedule_review` |
| Project Source Setup | [Origination Scout](../agents/vc-origination-scout.md) | None declared | `alludium.project_source_setup` |
| [VC Pack Variable Discovery](../tasks/vc-pack-variable-discovery.md) | [Origination Scout](../agents/vc-origination-scout.md) | None declared | `vc.pack_variable_discovery` |
| [Set Up Apify for VC Origination](../tasks/apify-setup.md) | [Pipeline Autopilot](../agents/vc-pipeline-autopilot.md) | [`vc-apify-discovery`](../skills/vc-apify-discovery/SKILL.md)<br>[`vc-apify-sync-read`](../skills/vc-apify-sync-read/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.apify_setup` |
| [Configure Companies House Public Register Preview](../tasks/companies-house-setup.md) | [Pipeline Autopilot](../agents/vc-pipeline-autopilot.md) | [`vc-companies-house-sourcing`](../skills/vc-companies-house-sourcing/SKILL.md)<br>[`vc-companies-house-sync-read`](../skills/vc-companies-house-sync-read/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.companies_house_setup` |
| [Run VC Sourcing Pipeline](../tasks/run-sourcing-pipeline.md) | [Pipeline Autopilot](../agents/vc-pipeline-autopilot.md) | [`vc-origination-pipeline-orchestration`](../skills/vc-origination-pipeline-orchestration/SKILL.md)<br>[`vc-source-registry-and-state-management`](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.run_sourcing_pipeline` |
| [Generate Sourcing Digest](../tasks/generate-sourcing-digest.md) | [Pipeline Autopilot](../agents/vc-pipeline-autopilot.md) | [`vc-sourcing-digest-generation`](../skills/vc-sourcing-digest-generation/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.generate_sourcing_digest` |
| [Review Source Errors and Spend](../tasks/review-source-errors-and-spend.md) | [Pipeline Autopilot](../agents/vc-pipeline-autopilot.md) | [`vc-source-error-and-spend-audit`](../skills/vc-source-error-and-spend-audit/SKILL.md)<br>[`vc-source-registry-and-state-management`](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.review_source_errors_and_spend` |
| [Discover Companies House Candidates](../tasks/discover-companies-house-candidates.md) | [Origination Scout](../agents/vc-origination-scout.md) | [`vc-companies-house-sourcing`](../skills/vc-companies-house-sourcing/SKILL.md)<br>[`vc-source-registry-and-state-management`](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.discover_companies_house_candidates` |
| [Discover X Founder Signals](../tasks/discover-x-founder-signals.md) | [Origination Scout](../agents/vc-origination-scout.md) | [`vc-apify-x-founder-discovery`](../skills/vc-apify-x-founder-discovery/SKILL.md)<br>[`vc-source-registry-and-state-management`](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.discover_x_founder_signals` |
| [Discover GitHub Builder Signals](../tasks/discover-github-builder-signals.md) | [Origination Scout](../agents/vc-origination-scout.md) | [`vc-github-builder-signal-discovery`](../skills/vc-github-builder-signal-discovery/SKILL.md)<br>[`vc-source-registry-and-state-management`](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.discover_github_builder_signals` |
| [Discover LinkedIn Founder Candidates](../tasks/discover-linkedin-founders.md) | [Origination Scout](../agents/vc-origination-scout.md) | [`vc-apify-linkedin-founder-discovery`](../skills/vc-apify-linkedin-founder-discovery/SKILL.md)<br>[`vc-source-registry-and-state-management`](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.discover_linkedin_founders` |
| [Discover Reddit Builder Signals](../tasks/discover-reddit-builder-signals.md) | [Origination Scout](../agents/vc-origination-scout.md) | [`vc-reddit-builder-signal-discovery`](../skills/vc-reddit-builder-signal-discovery/SKILL.md)<br>[`vc-source-registry-and-state-management`](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.discover_reddit_builder_signals` |
| [Review Portfolio Overlap](../tasks/review-portfolio-overlap.md) | [First Look Analyst](../agents/vc-first-look-analyst.md) | [`vc-portfolio-overlap-review`](../skills/vc-portfolio-overlap-review/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md)<br>[`vc-relationship-context-check`](../skills/vc-relationship-context-check/SKILL.md) | `vc.review_portfolio_overlap` |
| [Screen Active Sourcing Candidates](../tasks/screen-active-sourcing-candidates.md) | [First Look Analyst](../agents/vc-first-look-analyst.md) | [`vc-sourcing-verdict-and-screening`](../skills/vc-sourcing-verdict-and-screening/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md)<br>[`investment-screening-framework`](../skills/investment-screening-framework/SKILL.md) | `vc.screen_active_sourcing_candidates` |
| [Prepare Outreach Draft Queue](../tasks/prepare-outreach-draft-queue.md) | [Dealflow Concierge](../agents/vc-dealflow-concierge.md) | [`vc-outreach-draft-queue`](../skills/vc-outreach-draft-queue/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md)<br>[`founder-outreach-and-intro-paths`](../skills/founder-outreach-and-intro-paths/SKILL.md) | `vc.prepare_outreach_draft_queue` |
| [Audit LinkedIn Query Spend](../tasks/audit-linkedin-query-spend.md) | [Pipeline Autopilot](../agents/vc-pipeline-autopilot.md) | [`vc-linkedin-query-spend-audit`](../skills/vc-linkedin-query-spend-audit/SKILL.md)<br>[`vc-source-registry-and-state-management`](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.audit_linkedin_query_spend` |

## Draft

| Task | Agent | Skills | Task ID |
| --- | --- | --- | --- |
| [Configure VC Origination Pipeline](../tasks/configure-origination-pipeline.md) | [Pipeline Autopilot](../agents/vc-pipeline-autopilot.md) | [`vc-origination-pipeline-orchestration`](../skills/vc-origination-pipeline-orchestration/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.configure_origination_pipeline` |

## Configured

| Task | Agent | Skills | Task ID |
| --- | --- | --- | --- |
| None mapped | None declared | None declared |  |

## Active

| Task | Agent | Skills | Task ID |
| --- | --- | --- | --- |
| [Run VC Sourcing Pipeline](../tasks/run-sourcing-pipeline.md) | [Pipeline Autopilot](../agents/vc-pipeline-autopilot.md) | [`vc-origination-pipeline-orchestration`](../skills/vc-origination-pipeline-orchestration/SKILL.md)<br>[`vc-source-registry-and-state-management`](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.run_sourcing_pipeline` |
| [Discover Companies House Candidates](../tasks/discover-companies-house-candidates.md) | [Origination Scout](../agents/vc-origination-scout.md) | [`vc-companies-house-sourcing`](../skills/vc-companies-house-sourcing/SKILL.md)<br>[`vc-source-registry-and-state-management`](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.discover_companies_house_candidates` |
| [Discover LinkedIn Founder Candidates](../tasks/discover-linkedin-founders.md) | [Origination Scout](../agents/vc-origination-scout.md) | [`vc-apify-linkedin-founder-discovery`](../skills/vc-apify-linkedin-founder-discovery/SKILL.md)<br>[`vc-source-registry-and-state-management`](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.discover_linkedin_founders` |
| [Discover X Founder Signals](../tasks/discover-x-founder-signals.md) | [Origination Scout](../agents/vc-origination-scout.md) | [`vc-apify-x-founder-discovery`](../skills/vc-apify-x-founder-discovery/SKILL.md)<br>[`vc-source-registry-and-state-management`](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.discover_x_founder_signals` |
| [Discover GitHub Builder Signals](../tasks/discover-github-builder-signals.md) | [Origination Scout](../agents/vc-origination-scout.md) | [`vc-github-builder-signal-discovery`](../skills/vc-github-builder-signal-discovery/SKILL.md)<br>[`vc-source-registry-and-state-management`](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.discover_github_builder_signals` |
| [Discover Reddit Builder Signals](../tasks/discover-reddit-builder-signals.md) | [Origination Scout](../agents/vc-origination-scout.md) | [`vc-reddit-builder-signal-discovery`](../skills/vc-reddit-builder-signal-discovery/SKILL.md)<br>[`vc-source-registry-and-state-management`](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.discover_reddit_builder_signals` |
| [Ingest Manual Sourcing Tip](../tasks/ingest-manual-sourcing-tip.md) | [Origination Scout](../agents/vc-origination-scout.md) | [`vc-manual-tip-ingestion`](../skills/vc-manual-tip-ingestion/SKILL.md)<br>[`vc-sourcing-dedupe-and-novelty-check`](../skills/vc-sourcing-dedupe-and-novelty-check/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.ingest_manual_sourcing_tip` |
| [Generate Sourcing Digest](../tasks/generate-sourcing-digest.md) | [Pipeline Autopilot](../agents/vc-pipeline-autopilot.md) | [`vc-sourcing-digest-generation`](../skills/vc-sourcing-digest-generation/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.generate_sourcing_digest` |
| [Audit LinkedIn Query Spend](../tasks/audit-linkedin-query-spend.md) | [Pipeline Autopilot](../agents/vc-pipeline-autopilot.md) | [`vc-linkedin-query-spend-audit`](../skills/vc-linkedin-query-spend-audit/SKILL.md)<br>[`vc-source-registry-and-state-management`](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.audit_linkedin_query_spend` |

## Needs Credentials

| Task | Agent | Skills | Task ID |
| --- | --- | --- | --- |
| [Set Up Apify for VC Origination](../tasks/apify-setup.md) | [Pipeline Autopilot](../agents/vc-pipeline-autopilot.md) | [`vc-apify-discovery`](../skills/vc-apify-discovery/SKILL.md)<br>[`vc-apify-sync-read`](../skills/vc-apify-sync-read/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.apify_setup` |
| [Configure Companies House Public Register Preview](../tasks/companies-house-setup.md) | [Pipeline Autopilot](../agents/vc-pipeline-autopilot.md) | [`vc-companies-house-sourcing`](../skills/vc-companies-house-sourcing/SKILL.md)<br>[`vc-companies-house-sync-read`](../skills/vc-companies-house-sync-read/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.companies_house_setup` |

## Source Degraded

| Task | Agent | Skills | Task ID |
| --- | --- | --- | --- |
| [Review Source Errors and Spend](../tasks/review-source-errors-and-spend.md) | [Pipeline Autopilot](../agents/vc-pipeline-autopilot.md) | [`vc-source-error-and-spend-audit`](../skills/vc-source-error-and-spend-audit/SKILL.md)<br>[`vc-source-registry-and-state-management`](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.review_source_errors_and_spend` |

## Review Backlog

| Task | Agent | Skills | Task ID |
| --- | --- | --- | --- |
| [Review Reddit Candidate Inbox](../tasks/review-reddit-candidate-inbox.md) | [Origination Scout](../agents/vc-origination-scout.md) | [`vc-reddit-inbox-approval`](../skills/vc-reddit-inbox-approval/SKILL.md)<br>[`vc-sourcing-dedupe-and-novelty-check`](../skills/vc-sourcing-dedupe-and-novelty-check/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.review_reddit_candidate_inbox` |
| [Enrich Sourcing Candidates](../tasks/enrich-sourcing-candidates.md) | [Origination Scout](../agents/vc-origination-scout.md) | [`vc-sourcing-candidate-enrichment`](../skills/vc-sourcing-candidate-enrichment/SKILL.md)<br>[`vc-sourcing-dedupe-and-novelty-check`](../skills/vc-sourcing-dedupe-and-novelty-check/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.enrich_sourcing_candidates` |
| [Check Affinity Relationship Context](../tasks/check-affinity-relationships.md) | [Origination Scout](../agents/vc-origination-scout.md) | [`vc-relationship-context-check`](../skills/vc-relationship-context-check/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.check_affinity_relationships` |
| [Score Sourcing Candidates](../tasks/score-sourcing-candidates.md) | [First Look Analyst](../agents/vc-first-look-analyst.md) | [`vc-sourcing-verdict-and-screening`](../skills/vc-sourcing-verdict-and-screening/SKILL.md)<br>[`vc-sourcing-dedupe-and-novelty-check`](../skills/vc-sourcing-dedupe-and-novelty-check/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.score_sourcing_candidates` |
| [Sync Sourcing Candidates](../tasks/sync-sourcing-candidates.md) | [Dealflow Concierge](../agents/vc-dealflow-concierge.md) | [`vc-source-registry-and-state-management`](../skills/vc-source-registry-and-state-management/SKILL.md)<br>[`vc-sourcing-dedupe-and-novelty-check`](../skills/vc-sourcing-dedupe-and-novelty-check/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md)<br>[`vc-notion-sync-write`](../skills/vc-notion-sync-write/SKILL.md) | `vc.sync_sourcing_candidates` |
| [Review Portfolio Overlap](../tasks/review-portfolio-overlap.md) | [First Look Analyst](../agents/vc-first-look-analyst.md) | [`vc-portfolio-overlap-review`](../skills/vc-portfolio-overlap-review/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md)<br>[`vc-relationship-context-check`](../skills/vc-relationship-context-check/SKILL.md) | `vc.review_portfolio_overlap` |
| [Screen Active Sourcing Candidates](../tasks/screen-active-sourcing-candidates.md) | [First Look Analyst](../agents/vc-first-look-analyst.md) | [`vc-sourcing-verdict-and-screening`](../skills/vc-sourcing-verdict-and-screening/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md)<br>[`investment-screening-framework`](../skills/investment-screening-framework/SKILL.md) | `vc.screen_active_sourcing_candidates` |
| [Prepare Sourcing IC Summary](../tasks/prepare-sourcing-ic-summary.md) | [IC Prep Producer](../agents/vc-ic-prep-producer.md) | [`vc-origination-ic-summary-preparation`](../skills/vc-origination-ic-summary-preparation/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.prepare_sourcing_ic_summary` |
| [Prepare Outreach Draft Queue](../tasks/prepare-outreach-draft-queue.md) | [Dealflow Concierge](../agents/vc-dealflow-concierge.md) | [`vc-outreach-draft-queue`](../skills/vc-outreach-draft-queue/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md)<br>[`founder-outreach-and-intro-paths`](../skills/founder-outreach-and-intro-paths/SKILL.md) | `vc.prepare_outreach_draft_queue` |
| [Promote Candidate to Deal Room](../tasks/promote-candidate-to-deal-room.md) | [Dealflow Concierge](../agents/vc-dealflow-concierge.md) | [`vc-origination-deal-room-promotion`](../skills/vc-origination-deal-room-promotion/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md)<br>[`deal-room-setup-and-source-ingestion`](../skills/deal-room-setup-and-source-ingestion/SKILL.md) | `vc.promote_candidate_to_deal_room` |

## Paused

| Task | Agent | Skills | Task ID |
| --- | --- | --- | --- |
| None mapped | None declared | None declared |  |

## Migration In Progress

| Task | Agent | Skills | Task ID |
| --- | --- | --- | --- |
| None mapped | None declared | None declared |  |

## Archived

| Task | Agent | Skills | Task ID |
| --- | --- | --- | --- |
| None mapped | None declared | None declared |  |
