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

This blueprint lists the project stages, mapped tasks, recommended agents, and task-referenced skills for this project type.

## Project Setup / General

| Task | Agent | Skills | Task ID |
| --- | --- | --- | --- |
| Project Source Choice | [VC Deal Room Setup Guide](../agents/vc-deal-room-setup-guide.md) | None declared | `alludium.project_source_choice` |
| Project Variable Review | [VC Deal Room Setup Guide](../agents/vc-deal-room-setup-guide.md) | None declared | `alludium.project_variable_review` |
| Project Schedule Review | [VC Deal Room Setup Guide](../agents/vc-deal-room-setup-guide.md) | None declared | `alludium.project_schedule_review` |
| Project Team Invite Review | [VC Deal Room Setup Guide](../agents/vc-deal-room-setup-guide.md) | None declared | `alludium.project_team_invite` |
| Project Source Setup | [VC Deal Room Setup Guide](../agents/vc-deal-room-setup-guide.md) | None declared | `alludium.project_source_setup` |
| [VC Pack Variable Discovery](../tasks/vc-pack-variable-discovery.md) | [VC Deal Room Setup Guide](../agents/vc-deal-room-setup-guide.md) | None declared | `vc.pack_variable_discovery` |
| [Set Up Affinity for VC Deal Rooms](../tasks/affinity-setup.md) | [VC Deal Room Setup Guide](../agents/vc-deal-room-setup-guide.md) | [`vc-affinity-discovery`](../skills/vc-affinity-discovery/SKILL.md)<br>[`vc-affinity-sync-read`](../skills/vc-affinity-sync-read/SKILL.md)<br>[`vc-affinity-sync-write`](../skills/vc-affinity-sync-write/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.affinity_setup` |
| [Preview Affinity Pipeline Import](../tasks/affinity-sync-read.md) | [Pipeline Autopilot](../agents/vc-pipeline-autopilot.md) | [`vc-affinity-sync-read`](../skills/vc-affinity-sync-read/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.affinity_sync_read` |

## Intake

| Task | Agent | Skills | Task ID |
| --- | --- | --- | --- |
| [Import Affinity Deal Room Seed](../tasks/affinity-deal-room-import.md) | [VC Deal Room Setup Guide](../agents/vc-deal-room-setup-guide.md) | [`vc-affinity-deal-room-import`](../skills/vc-affinity-deal-room-import/SKILL.md)<br>[`vc-affinity-sync-read`](../skills/vc-affinity-sync-read/SKILL.md)<br>[`deal-room-setup-and-source-ingestion`](../skills/deal-room-setup-and-source-ingestion/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.affinity_deal_room_import` |
| [Source Thesis Targets](../tasks/source-thesis-targets.md) | [Origination Scout](../agents/vc-origination-scout.md) | [`company-research-and-enrichment`](../skills/company-research-and-enrichment/SKILL.md)<br>[`founder-outreach-and-intro-paths`](../skills/founder-outreach-and-intro-paths/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.source_thesis_targets` |
| [Capture Opportunity Intake](../tasks/screen-inbound-opportunity.md) | [Dealflow Concierge](../agents/vc-dealflow-concierge.md) | [`deal-room-setup-and-source-ingestion`](../skills/deal-room-setup-and-source-ingestion/SKILL.md)<br>[`company-research-and-enrichment`](../skills/company-research-and-enrichment/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md)<br>[`pitch-deck-explainer`](../skills/pitch-deck-explainer/SKILL.md) | `vc.screen_inbound_opportunity` |

## Screening

| Task | Agent | Skills | Task ID |
| --- | --- | --- | --- |
| [Run Investment Fit Screen](../tasks/run-investment-screen.md) | [First Look Analyst](../agents/vc-first-look-analyst.md) | [`red-flags-scanner`](../skills/red-flags-scanner/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.run_investment_screen` |

## Evaluation

| Task | Agent | Skills | Task ID |
| --- | --- | --- | --- |
| [Request Founder Materials](../tasks/request-founder-materials.md) | [Dealflow Concierge](../agents/vc-dealflow-concierge.md) | [`citation-enforcement`](../skills/citation-enforcement/SKILL.md)<br>[`founder-materials-request`](../skills/founder-materials-request/SKILL.md) | `vc.request_founder_materials` |
| [Prepare Meeting](../tasks/prepare-initial-call.md) | [Meeting Operator](../agents/vc-meeting-operator.md) | [`meeting-prep-and-summary`](../skills/meeting-prep-and-summary/SKILL.md)<br>[`company-research-and-enrichment`](../skills/company-research-and-enrichment/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md)<br>[`pitch-deck-explainer`](../skills/pitch-deck-explainer/SKILL.md) | `vc.prepare_initial_call` |
| [Summarize Meeting Records](../tasks/summarize-initial-call.md) | [Meeting Operator](../agents/vc-meeting-operator.md) | [`meeting-prep-and-summary`](../skills/meeting-prep-and-summary/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md)<br>[`vc-task-and-next-step-generation`](../skills/vc-task-and-next-step-generation/SKILL.md) | `vc.summarize_initial_call` |
| [Run Opportunity Evaluation](../tasks/run-follow-up-evaluation.md) | [First Look Analyst](../agents/vc-first-look-analyst.md) | [`red-flags-scanner`](../skills/red-flags-scanner/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.run_follow_up_evaluation` |
| [Run Commercial Evaluation](../tasks/run-commercial-evaluation.md) | [First Look Analyst](../agents/vc-first-look-analyst.md) | [`commercial-evaluation-and-market-risk`](../skills/commercial-evaluation-and-market-risk/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.run_commercial_evaluation` |
| [Run Technical Evaluation](../tasks/run-technical-evaluation.md) | [First Look Analyst](../agents/vc-first-look-analyst.md) | [`technical-evaluation-and-product-risk`](../skills/technical-evaluation-and-product-risk/SKILL.md)<br>[`red-flags-scanner`](../skills/red-flags-scanner/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.run_technical_evaluation` |
| [Run Financial Evaluation](../tasks/run-financial-evaluation.md) | [First Look Analyst](../agents/vc-first-look-analyst.md) | [`financial-evaluation-and-financing-risk`](../skills/financial-evaluation-and-financing-risk/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.run_financial_evaluation` |
| [Run Team Evaluation](../tasks/run-team-evaluation.md) | [First Look Analyst](../agents/vc-first-look-analyst.md) | [`team-evaluation-and-founder-risk`](../skills/team-evaluation-and-founder-risk/SKILL.md)<br>[`red-flags-scanner`](../skills/red-flags-scanner/SKILL.md)<br>[`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.run_team_evaluation` |
| [Generate Diligence Questions](../tasks/generate-diligence-questions.md) | [First Look Analyst](../agents/vc-first-look-analyst.md) | [`citation-enforcement`](../skills/citation-enforcement/SKILL.md) | `vc.generate_diligence_questions` |

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
