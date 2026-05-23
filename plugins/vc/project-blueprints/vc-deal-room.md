---
projectType: vc_deal_room
title: VC Deal Room Blueprint
source: alludium/project-types/vc_deal_room.json
---

> **GENERATED FILE**
> Source: `alludium/project-types/vc_deal_room.json`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# VC Deal Room Blueprint

Project context for one venture investment opportunity from sourcing through portfolio handoff.

This blueprint lists setup, general, management, and lifecycle-stage tasks with the recommended agents and task-referenced skills for this project type. Setup, General, and Management are blueprint categories rather than lifecycle states.

## Setup

Project-type setup and configuration tasks used before normal project execution.

| Task | Agent | Skills | Task ID |
| --- | --- | --- | --- |
| Project Source Choice | [VC Deal Room Setup Guide](../agents/vc-deal-room-setup-guide.md) | None declared | `alludium.project_source_choice` |
| Project Variable Review | [VC Deal Room Setup Guide](../agents/vc-deal-room-setup-guide.md) | None declared | `alludium.project_variable_review` |
| Project Schedule Review | [VC Deal Room Setup Guide](../agents/vc-deal-room-setup-guide.md) | None declared | `alludium.project_schedule_review` |
| Project Team Invite Review | [VC Deal Room Setup Guide](../agents/vc-deal-room-setup-guide.md) | None declared | `alludium.project_team_invite` |
| Project Source Setup | [VC Deal Room Setup Guide](../agents/vc-deal-room-setup-guide.md) | None declared | `alludium.project_source_setup` |
| [VC Pack Variable Discovery](../tasks/vc-pack-variable-discovery.md) | [VC Deal Room Setup Guide](../agents/vc-deal-room-setup-guide.md) | None declared | `vc.pack_variable_discovery` |
| [Set Up Affinity for VC Deal Rooms](../tasks/affinity-setup.md) | [Integration Operator](../agents/vc-integration-operator.md) | [`vc-affinity-discovery`](../skills/vc-affinity-discovery/SKILL.md)<br>[`vc-affinity-sync-read`](../skills/vc-affinity-sync-read/SKILL.md)<br>[`vc-affinity-sync-write`](../skills/vc-affinity-sync-write/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.affinity_setup` |

## General

Reusable project-instance tasks that can be useful across multiple lifecycle stages.

| Task | Agent | Skills | Task ID |
| --- | --- | --- | --- |
| [Prepare Meeting](../tasks/prepare-initial-call.md) | [Meeting Operator](../agents/vc-meeting-operator.md) | [`meeting-prep-and-summary`](../skills/meeting-prep-and-summary/SKILL.md)<br>[`company-research-and-enrichment`](../skills/company-research-and-enrichment/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md)<br>[`pitch-deck-explainer`](../skills/pitch-deck-explainer/SKILL.md) | `vc.prepare_initial_call` |
| [Request Founder Materials](../tasks/request-founder-materials.md) | [Dealflow Concierge](../agents/vc-dealflow-concierge.md) | [`citation-enforcement`](../skills/citation-enforcement/SKILL.md)<br>[`founder-materials-request`](../skills/founder-materials-request/SKILL.md) | `vc.request_founder_materials` |
| [Summarize Meeting Records](../tasks/summarize-initial-call.md) | [Meeting Operator](../agents/vc-meeting-operator.md) | [`meeting-prep-and-summary`](../skills/meeting-prep-and-summary/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md)<br>[`vc-task-and-next-step-generation`](../skills/vc-task-and-next-step-generation/SKILL.md) | `vc.summarize_initial_call` |
| [Review Opportunity Status](../tasks/review-opportunity-status.md) | [Pipeline Autopilot](../agents/vc-pipeline-autopilot.md) | [`citation-enforcement`](../skills/citation-enforcement/SKILL.md)<br>[`vc-task-and-next-step-generation`](../skills/vc-task-and-next-step-generation/SKILL.md) | `vc.review_opportunity_status` |

## Management

Project-management tasks that operate across a project suite, source pipeline, or recurring sync/reporting flow.

| Task | Agent | Skills | Task ID |
| --- | --- | --- | --- |
| [Preview Affinity Pipeline Import](../tasks/affinity-sync-read.md) | [Integration Operator](../agents/vc-integration-operator.md) | [`vc-affinity-sync-read`](../skills/vc-affinity-sync-read/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.affinity_sync_read` |
| [Draft Affinity Write-Back Proposals](../tasks/affinity-sync-write.md) | [Integration Operator](../agents/vc-integration-operator.md) | [`vc-affinity-sync-write`](../skills/vc-affinity-sync-write/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.affinity_sync_write` |
| [Draft Google Drive File Proposals](../tasks/google-drive-sync-write.md) | [Integration Operator](../agents/vc-integration-operator.md) | [`vc-google-drive-sync-write`](../skills/vc-google-drive-sync-write/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.google_drive_sync_write` |
| [Draft Notion Update Proposals](../tasks/notion-sync-write.md) | [Integration Operator](../agents/vc-integration-operator.md) | [`vc-notion-sync-write`](../skills/vc-notion-sync-write/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.notion_sync_write` |
| [Draft Slack Handoff Notifications](../tasks/slack-sync-write.md) | [Integration Operator](../agents/vc-integration-operator.md) | [`vc-slack-sync-write`](../skills/vc-slack-sync-write/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.slack_sync_write` |
| [Explore Affinity Lists and Stages](../tasks/affinity-discovery.md) | [Integration Operator](../agents/vc-integration-operator.md) | [`vc-affinity-discovery`](../skills/vc-affinity-discovery/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.affinity_discovery` |
| [Explore Google Drive Sources](../tasks/google-drive-discovery.md) | [Integration Operator](../agents/vc-integration-operator.md) | [`vc-google-drive-discovery`](../skills/vc-google-drive-discovery/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.google_drive_discovery` |
| [Explore Harmonic Source Scopes](../tasks/harmonic-discovery.md) | [Integration Operator](../agents/vc-integration-operator.md) | [`vc-harmonic-discovery`](../skills/vc-harmonic-discovery/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.harmonic_discovery` |
| [Explore Notion Pages and Databases](../tasks/notion-discovery.md) | [Integration Operator](../agents/vc-integration-operator.md) | [`vc-notion-discovery`](../skills/vc-notion-discovery/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.notion_discovery` |
| [Explore Slack Channels for VC Context](../tasks/slack-discovery.md) | [Integration Operator](../agents/vc-integration-operator.md) | [`vc-slack-discovery`](../skills/vc-slack-discovery/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.slack_discovery` |
| [Prepare Deal Flow Agenda](../tasks/prepare-deal-flow-agenda.md) | [Pipeline Autopilot](../agents/vc-pipeline-autopilot.md) | [`citation-enforcement`](../skills/citation-enforcement/SKILL.md)<br>[`vc-task-and-next-step-generation`](../skills/vc-task-and-next-step-generation/SKILL.md) | `vc.prepare_deal_flow_agenda` |
| [Prepare Lead Gen Packet](../tasks/prepare-lead-gen-packet.md) | [Origination Scout](../agents/vc-origination-scout.md) | [`company-research-and-enrichment`](../skills/company-research-and-enrichment/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.prepare_lead_gen_packet` |
| [Preview Google Drive Context](../tasks/google-drive-sync-read.md) | [Integration Operator](../agents/vc-integration-operator.md) | [`vc-google-drive-sync-read`](../skills/vc-google-drive-sync-read/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.google_drive_sync_read` |
| [Preview Harmonic Search Results](../tasks/harmonic-sync-read.md) | [Integration Operator](../agents/vc-integration-operator.md) | [`vc-harmonic-sync-read`](../skills/vc-harmonic-sync-read/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.harmonic_sync_read` |
| [Preview Notion Context](../tasks/notion-sync-read.md) | [Integration Operator](../agents/vc-integration-operator.md) | [`vc-notion-sync-read`](../skills/vc-notion-sync-read/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.notion_sync_read` |
| [Preview Slack Deal Context](../tasks/slack-sync-read.md) | [Integration Operator](../agents/vc-integration-operator.md) | [`vc-slack-sync-read`](../skills/vc-slack-sync-read/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.slack_sync_read` |
| [Set Up Google Drive for VC Deal Rooms](../tasks/google-drive-setup.md) | [Integration Operator](../agents/vc-integration-operator.md) | [`vc-google-drive-discovery`](../skills/vc-google-drive-discovery/SKILL.md)<br>[`vc-google-drive-sync-read`](../skills/vc-google-drive-sync-read/SKILL.md)<br>[`vc-google-drive-sync-write`](../skills/vc-google-drive-sync-write/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.google_drive_setup` |
| [Set Up Harmonic for VC Deal Rooms](../tasks/harmonic-setup.md) | [Integration Operator](../agents/vc-integration-operator.md) | [`vc-harmonic-discovery`](../skills/vc-harmonic-discovery/SKILL.md)<br>[`vc-harmonic-sync-read`](../skills/vc-harmonic-sync-read/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.harmonic_setup` |
| [Set Up Notion for VC Deal Rooms](../tasks/notion-setup.md) | [Integration Operator](../agents/vc-integration-operator.md) | [`vc-notion-discovery`](../skills/vc-notion-discovery/SKILL.md)<br>[`vc-notion-sync-read`](../skills/vc-notion-sync-read/SKILL.md)<br>[`vc-notion-sync-write`](../skills/vc-notion-sync-write/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.notion_setup` |
| [Set Up Slack for VC Deal Rooms](../tasks/slack-setup.md) | [Integration Operator](../agents/vc-integration-operator.md) | [`vc-slack-discovery`](../skills/vc-slack-discovery/SKILL.md)<br>[`vc-slack-sync-read`](../skills/vc-slack-sync-read/SKILL.md)<br>[`vc-slack-sync-write`](../skills/vc-slack-sync-write/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.slack_setup` |

## Intake

| Task | Agent | Skills | Task ID |
| --- | --- | --- | --- |
| [Import Affinity Deal Room Seed](../tasks/affinity-deal-room-import.md) | [VC Deal Room Setup Guide](../agents/vc-deal-room-setup-guide.md) | [`vc-affinity-deal-room-import`](../skills/vc-affinity-deal-room-import/SKILL.md)<br>[`vc-affinity-sync-read`](../skills/vc-affinity-sync-read/SKILL.md)<br>[`deal-room-setup-and-source-ingestion`](../skills/deal-room-setup-and-source-ingestion/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.affinity_deal_room_import` |
| [Source Thesis Targets](../tasks/source-thesis-targets.md) | [Origination Scout](../agents/vc-origination-scout.md) | [`company-research-and-enrichment`](../skills/company-research-and-enrichment/SKILL.md)<br>[`founder-outreach-and-intro-paths`](../skills/founder-outreach-and-intro-paths/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.source_thesis_targets` |
| [Capture Opportunity Intake](../tasks/screen-inbound-opportunity.md) | [Dealflow Concierge](../agents/vc-dealflow-concierge.md) | [`deal-room-setup-and-source-ingestion`](../skills/deal-room-setup-and-source-ingestion/SKILL.md)<br>[`company-research-and-enrichment`](../skills/company-research-and-enrichment/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md)<br>[`pitch-deck-explainer`](../skills/pitch-deck-explainer/SKILL.md) | `vc.screen_inbound_opportunity` |

## Screening

| Task | Agent | Skills | Task ID |
| --- | --- | --- | --- |
| [Run Investment Fit Screen](../tasks/run-investment-screen.md) | [First Look Analyst](../agents/vc-first-look-analyst.md) | [`investment-screening-framework`](../skills/investment-screening-framework/SKILL.md)<br>[`red-flags-scanner`](../skills/red-flags-scanner/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.run_investment_screen` |

## Evaluation

| Task | Agent | Skills | Task ID |
| --- | --- | --- | --- |
| [Run Opportunity Evaluation](../tasks/run-follow-up-evaluation.md) | [Evaluation Analyst](../agents/vc-evaluation-analyst.md) | [`investment-diligence-question-framework`](../skills/investment-diligence-question-framework/SKILL.md)<br>[`red-flags-scanner`](../skills/red-flags-scanner/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.run_follow_up_evaluation` |
| [Run Commercial Evaluation](../tasks/run-commercial-evaluation.md) | [Evaluation Analyst](../agents/vc-evaluation-analyst.md) | [`commercial-evaluation-and-market-risk`](../skills/commercial-evaluation-and-market-risk/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.run_commercial_evaluation` |
| [Run Technical Evaluation](../tasks/run-technical-evaluation.md) | [Evaluation Analyst](../agents/vc-evaluation-analyst.md) | [`technical-evaluation-and-product-risk`](../skills/technical-evaluation-and-product-risk/SKILL.md)<br>[`red-flags-scanner`](../skills/red-flags-scanner/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.run_technical_evaluation` |
| [Run Financial Evaluation](../tasks/run-financial-evaluation.md) | [Evaluation Analyst](../agents/vc-evaluation-analyst.md) | [`financial-evaluation-and-financing-risk`](../skills/financial-evaluation-and-financing-risk/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.run_financial_evaluation` |
| [Run Team Evaluation](../tasks/run-team-evaluation.md) | [Evaluation Analyst](../agents/vc-evaluation-analyst.md) | [`team-evaluation-and-founder-risk`](../skills/team-evaluation-and-founder-risk/SKILL.md)<br>[`red-flags-scanner`](../skills/red-flags-scanner/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.run_team_evaluation` |
| [Generate Diligence Questions](../tasks/generate-diligence-questions.md) | [Evaluation Analyst](../agents/vc-evaluation-analyst.md) | [`investment-diligence-question-framework`](../skills/investment-diligence-question-framework/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.generate_diligence_questions` |

## Decision Review

| Task | Agent | Skills | Task ID |
| --- | --- | --- | --- |
| [Prepare Team Review Pack](../tasks/prepare-team-review-pack.md) | [Diligence Analyst](../agents/vc-diligence-analyst.md) | [`ic-memo-assembly`](../skills/ic-memo-assembly/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.prepare_team_review_pack` |
| [Prepare Partner Review Pack](../tasks/prepare-partner-review-pack.md) | [Diligence Analyst](../agents/vc-diligence-analyst.md) | [`ic-memo-assembly`](../skills/ic-memo-assembly/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.prepare_partner_review_pack` |
| [Create IC Memo](../tasks/create-ic-memo.md) | [IC Prep Producer](../agents/vc-ic-prep-producer.md) | [`ic-memo-assembly`](../skills/ic-memo-assembly/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md)<br>[`ic-risk-checklist-and-decision-log`](../skills/ic-risk-checklist-and-decision-log/SKILL.md) | `vc.create_ic_memo` |
| [Prepare IC Agenda](../tasks/prepare-ic-agenda.md) | [IC Prep Producer](../agents/vc-ic-prep-producer.md) | [`meeting-prep-and-summary`](../skills/meeting-prep-and-summary/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md)<br>[`ic-risk-checklist-and-decision-log`](../skills/ic-risk-checklist-and-decision-log/SKILL.md) | `vc.prepare_ic_agenda` |
| [Review IC Memo](../tasks/review-ic-memo.md) | [IC Prep Producer](../agents/vc-ic-prep-producer.md) | [`citation-enforcement`](../skills/citation-enforcement/SKILL.md)<br>[`ic-memo-assembly`](../skills/ic-memo-assembly/SKILL.md)<br>[`ic-risk-checklist-and-decision-log`](../skills/ic-risk-checklist-and-decision-log/SKILL.md) | `vc.review_ic_memo` |
| [Record IC Decision](../tasks/record-ic-decision.md) | [IC Prep Producer](../agents/vc-ic-prep-producer.md) | [`citation-enforcement`](../skills/citation-enforcement/SKILL.md)<br>[`ic-risk-checklist-and-decision-log`](../skills/ic-risk-checklist-and-decision-log/SKILL.md)<br>[`vc-task-and-next-step-generation`](../skills/vc-task-and-next-step-generation/SKILL.md) | `vc.record_ic_decision` |

## Deal Structuring

| Task | Agent | Skills | Task ID |
| --- | --- | --- | --- |
| [Analyze Deal Terms](../tasks/analyze-deal-terms.md) | [Legal & Compliance Desk](../agents/vc-legal-compliance-desk.md) | [`deal-terms-analysis`](../skills/deal-terms-analysis/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.analyze_deal_terms` |
| [Track Term Sheet Negotiation](../tasks/track-term-sheet-negotiation.md) | [Legal & Compliance Desk](../agents/vc-legal-compliance-desk.md) | [`term-sheet-negotiation-brief`](../skills/term-sheet-negotiation-brief/SKILL.md)<br>[`deal-terms-analysis`](../skills/deal-terms-analysis/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.track_term_sheet_negotiation` |
| [Review Term Sheet](../tasks/review-term-sheet.md) | [Legal & Compliance Desk](../agents/vc-legal-compliance-desk.md) | [`red-flags-scanner`](../skills/red-flags-scanner/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md)<br>[`closing-coordination-and-cp-tracking`](../skills/closing-coordination-and-cp-tracking/SKILL.md) | `vc.review_term_sheet` |

## Formal Diligence

| Task | Agent | Skills | Task ID |
| --- | --- | --- | --- |
| [Run Commercial DD](../tasks/run-commercial-dd.md) | [Diligence Analyst](../agents/vc-diligence-analyst.md) | [`citation-enforcement`](../skills/citation-enforcement/SKILL.md)<br>[`commercial-diligence-workstream`](../skills/commercial-diligence-workstream/SKILL.md) | `vc.run_commercial_dd` |
| [Run Financial DD](../tasks/run-financial-dd.md) | [Diligence Analyst](../agents/vc-diligence-analyst.md) | [`citation-enforcement`](../skills/citation-enforcement/SKILL.md)<br>[`financial-diligence-workstream`](../skills/financial-diligence-workstream/SKILL.md) | `vc.run_financial_dd` |
| [Run Founder Evaluation](../tasks/run-founder-evaluation.md) | [Diligence Analyst](../agents/vc-diligence-analyst.md) | [`team-and-hiring-assessment`](../skills/team-and-hiring-assessment/SKILL.md)<br>[`red-flags-scanner`](../skills/red-flags-scanner/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md)<br>[`founder-evaluation-and-reference-checking`](../skills/founder-evaluation-and-reference-checking/SKILL.md) | `vc.run_founder_evaluation` |
| [Run Technical DD](../tasks/run-technical-dd.md) | [Diligence Analyst](../agents/vc-diligence-analyst.md) | [`team-and-hiring-assessment`](../skills/team-and-hiring-assessment/SKILL.md)<br>[`red-flags-scanner`](../skills/red-flags-scanner/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md)<br>[`technical-diligence-workstream`](../skills/technical-diligence-workstream/SKILL.md) | `vc.run_technical_dd` |
| [Run Legal Diligence](../tasks/run-legal-diligence.md) | [Legal & Compliance Desk](../agents/vc-legal-compliance-desk.md) | [`legal-diligence-coordination`](../skills/legal-diligence-coordination/SKILL.md)<br>[`red-flags-scanner`](../skills/red-flags-scanner/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.run_legal_diligence` |

## Contracts

| Task | Agent | Skills | Task ID |
| --- | --- | --- | --- |
| [Review Investment Documents](../tasks/review-investment-documents.md) | [Legal & Compliance Desk](../agents/vc-legal-compliance-desk.md) | [`legal-diligence-coordination`](../skills/legal-diligence-coordination/SKILL.md)<br>[`closing-coordination-and-cp-tracking`](../skills/closing-coordination-and-cp-tracking/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.review_investment_documents` |

## Closing

| Task | Agent | Skills | Task ID |
| --- | --- | --- | --- |
| [Manage Closing Checklist](../tasks/manage-closing-checklist.md) | [Legal & Compliance Desk](../agents/vc-legal-compliance-desk.md) | [`citation-enforcement`](../skills/citation-enforcement/SKILL.md)<br>[`closing-coordination-and-cp-tracking`](../skills/closing-coordination-and-cp-tracking/SKILL.md)<br>[`vc-task-and-next-step-generation`](../skills/vc-task-and-next-step-generation/SKILL.md) | `vc.manage_closing_checklist` |
| [Verify Conditions Precedent](../tasks/verify-conditions-precedent.md) | [Legal & Compliance Desk](../agents/vc-legal-compliance-desk.md) | [`citation-enforcement`](../skills/citation-enforcement/SKILL.md)<br>[`closing-coordination-and-cp-tracking`](../skills/closing-coordination-and-cp-tracking/SKILL.md) | `vc.verify_conditions_precedent` |
| [Coordinate Capital Call And Completion](../tasks/coordinate-capital-call-and-completion.md) | [Legal & Compliance Desk](../agents/vc-legal-compliance-desk.md) | [`closing-coordination-and-cp-tracking`](../skills/closing-coordination-and-cp-tracking/SKILL.md)<br>[`vc-task-and-next-step-generation`](../skills/vc-task-and-next-step-generation/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.coordinate_capital_call_and_completion` |
| [Prepare Portfolio Onboarding](../tasks/prepare-portfolio-onboarding.md) | [Legal & Compliance Desk](../agents/vc-legal-compliance-desk.md) | [`citation-enforcement`](../skills/citation-enforcement/SKILL.md)<br>[`portfolio-onboarding-and-100-day-plan`](../skills/portfolio-onboarding-and-100-day-plan/SKILL.md) | `vc.prepare_portfolio_onboarding` |

## Watchlist

| Task | Agent | Skills | Task ID |
| --- | --- | --- | --- |
| None mapped | None declared | None declared |  |

## Invested

| Task | Agent | Skills | Task ID |
| --- | --- | --- | --- |
| None mapped | None declared | None declared |  |

## Passed

| Task | Agent | Skills | Task ID |
| --- | --- | --- | --- |
| None mapped | None declared | None declared |  |

## Archived

| Task | Agent | Skills | Task ID |
| --- | --- | --- | --- |
| None mapped | None declared | None declared |  |
