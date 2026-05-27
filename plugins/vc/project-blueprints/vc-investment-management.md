---
projectType: vc_investment_management
title: Investment Management Blueprint
source: alludium/project-types/vc_investment_management.json
---

> **GENERATED FILE**
> Source: `alludium/project-types/vc_investment_management.json`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Investment Management Blueprint

Project context for formal diligence, investment contracts, closing, completion, and portfolio handoff after a deal has moved beyond deal structuring.

This blueprint lists setup, support, and workflow-stage tasks with the recommended agents, task-referenced skills, document references, and integration surfaces for this project type. General and support sections are included only when they contain cross-cutting tasks that are not already mapped to a workflow stage.

## Setup

Project-type setup and configuration tasks used before normal project execution.

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| [Capture Investment Management Handoff](../tasks/capture-investment-management-handoff.md) | [Legal & Compliance Desk](../agents/vc-legal-compliance-desk.md) | [Citation Enforcement](../skills/citation-enforcement/SKILL.md)<br>[VC Task & Next-Step Generation](../skills/vc-task-and-next-step-generation/SKILL.md) | [Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.md) (style_guide)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | `alludium-platform`<br>`affinity-mcp-server`<br>`exa-mcp-hosted`<br>`brave-search-mcp`<br>`dealroom-mcp`<br>`google_drive` |
| [VC Pack Variable Discovery](../tasks/vc-pack-variable-discovery.md) | [Legal & Compliance Desk](../agents/vc-legal-compliance-desk.md) | None declared | None declared | `alludium-platform`<br>`affinity-mcp-server`<br>`exa-mcp-hosted`<br>`brave-search-mcp`<br>`dealroom-mcp`<br>`google_drive` |

## Formal Diligence

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| [Run Commercial DD](../tasks/run-commercial-dd.md) | [Diligence Analyst](../agents/vc-diligence-analyst.md) | [Citation Enforcement](../skills/citation-enforcement/SKILL.md)<br>[Commercial Diligence Workstream](../skills/commercial-diligence-workstream/SKILL.md) | [Diligence Report Template](../alludium/documents/deal-room/diligence-report-template.md) (output_template, to `commercial_dd_artifact_id`)<br>[Formal Diligence Workstream Guide](../alludium/documents/deal-room/formal-diligence-workstream-guide.md) (methodology)<br>[Formal Diligence Checklist](../alludium/documents/deal-room/formal-diligence-checklist.md) (checklist)<br>[Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.md) (style_guide)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | `alludium-platform`<br>`harmonic-mcp-oauth`<br>`affinity-mcp-server`<br>`exa-mcp-hosted`<br>`brave-search-mcp`<br>`serpapi-mcp`<br>`firecrawl-mcp-hosted`<br>`dealroom-mcp` |
| [Run Financial DD](../tasks/run-financial-dd.md) | [Diligence Analyst](../agents/vc-diligence-analyst.md) | [Citation Enforcement](../skills/citation-enforcement/SKILL.md)<br>[Financial Diligence Workstream](../skills/financial-diligence-workstream/SKILL.md) | [Diligence Report Template](../alludium/documents/deal-room/diligence-report-template.md) (output_template, to `financial_dd_artifact_id`)<br>[Formal Diligence Workstream Guide](../alludium/documents/deal-room/formal-diligence-workstream-guide.md) (methodology)<br>[Formal Diligence Checklist](../alludium/documents/deal-room/formal-diligence-checklist.md) (checklist)<br>[Diligence Report Template](../alludium/documents/deal-room/diligence-report-template.md) (output_template, to `unit_economics_artifact_id`)<br>[Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.md) (style_guide)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | `alludium-platform`<br>`harmonic-mcp-oauth`<br>`affinity-mcp-server`<br>`exa-mcp-hosted`<br>`brave-search-mcp`<br>`serpapi-mcp`<br>`firecrawl-mcp-hosted`<br>`dealroom-mcp` |
| [Run Founder Evaluation](../tasks/run-founder-evaluation.md) | [Diligence Analyst](../agents/vc-diligence-analyst.md) | [Team & Hiring Assessment](../skills/team-and-hiring-assessment/SKILL.md)<br>[Red Flags Scanner](../skills/red-flags-scanner/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md)<br>[Founder Evaluation & Reference Checking](../skills/founder-evaluation-and-reference-checking/SKILL.md) | [Diligence Report Template](../alludium/documents/deal-room/diligence-report-template.md) (output_template, to `founder_evaluation_artifact_id`)<br>[Formal Diligence Workstream Guide](../alludium/documents/deal-room/formal-diligence-workstream-guide.md) (methodology)<br>[Formal Diligence Checklist](../alludium/documents/deal-room/formal-diligence-checklist.md) (checklist)<br>[Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.md) (style_guide)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | `alludium-platform`<br>`harmonic-mcp-oauth`<br>`affinity-mcp-server`<br>`exa-mcp-hosted`<br>`brave-search-mcp`<br>`serpapi-mcp`<br>`firecrawl-mcp-hosted`<br>`dealroom-mcp` |
| [Run Technical DD](../tasks/run-technical-dd.md) | [Diligence Analyst](../agents/vc-diligence-analyst.md) | [Team & Hiring Assessment](../skills/team-and-hiring-assessment/SKILL.md)<br>[Red Flags Scanner](../skills/red-flags-scanner/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md)<br>[Technical Diligence Workstream](../skills/technical-diligence-workstream/SKILL.md) | [Diligence Report Template](../alludium/documents/deal-room/diligence-report-template.md) (output_template, to `technical_dd_artifact_id`)<br>[Formal Diligence Workstream Guide](../alludium/documents/deal-room/formal-diligence-workstream-guide.md) (methodology)<br>[Formal Diligence Checklist](../alludium/documents/deal-room/formal-diligence-checklist.md) (checklist)<br>[Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.md) (style_guide)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | `alludium-platform`<br>`harmonic-mcp-oauth`<br>`affinity-mcp-server`<br>`exa-mcp-hosted`<br>`brave-search-mcp`<br>`serpapi-mcp`<br>`firecrawl-mcp-hosted`<br>`dealroom-mcp` |
| [Run Legal Diligence](../tasks/run-legal-diligence.md) | [Legal & Compliance Desk](../agents/vc-legal-compliance-desk.md) | [Legal Diligence Coordination](../skills/legal-diligence-coordination/SKILL.md)<br>[Red Flags Scanner](../skills/red-flags-scanner/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | [Legal Diligence Tracker Template](../alludium/documents/deal-room/legal-diligence-tracker-template.md) (output_template, to `legal_diligence_artifact_id`)<br>[Legal Diligence Guide](../alludium/documents/deal-room/legal-diligence-guide.md) (methodology)<br>[Formal Diligence Workstream Guide](../alludium/documents/deal-room/formal-diligence-workstream-guide.md) (methodology)<br>[Formal Diligence Checklist](../alludium/documents/deal-room/formal-diligence-checklist.md) (checklist)<br>[Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.md) (style_guide)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | `alludium-platform`<br>`affinity-mcp-server`<br>`exa-mcp-hosted`<br>`brave-search-mcp`<br>`dealroom-mcp`<br>`google_drive` |

## Contracts

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| [Review Investment Documents](../tasks/review-investment-documents.md) | [Legal & Compliance Desk](../agents/vc-legal-compliance-desk.md) | [Legal Diligence Coordination](../skills/legal-diligence-coordination/SKILL.md)<br>[Closing Coordination & CP Tracking](../skills/closing-coordination-and-cp-tracking/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | [Investment Document Review Template](../alludium/documents/deal-room/investment-document-review-template.md) (output_template, to `investment_document_review_artifact_id`)<br>[Legal Diligence Guide](../alludium/documents/deal-room/legal-diligence-guide.md) (methodology)<br>[Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.md) (style_guide)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | `alludium-platform`<br>`affinity-mcp-server`<br>`exa-mcp-hosted`<br>`brave-search-mcp`<br>`dealroom-mcp`<br>`google_drive` |

## Closing

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| [Manage Closing Checklist](../tasks/manage-closing-checklist.md) | [Legal & Compliance Desk](../agents/vc-legal-compliance-desk.md) | [Citation Enforcement](../skills/citation-enforcement/SKILL.md)<br>[Closing Coordination & CP Tracking](../skills/closing-coordination-and-cp-tracking/SKILL.md)<br>[VC Task & Next-Step Generation](../skills/vc-task-and-next-step-generation/SKILL.md) | [Closing Checklist](../alludium/documents/deal-room/closing-checklist.md) (output_template, to `closing_checklist_artifact_id`)<br>[Legal Diligence Guide](../alludium/documents/deal-room/legal-diligence-guide.md) (methodology)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | `alludium-platform`<br>`affinity-mcp-server`<br>`exa-mcp-hosted`<br>`brave-search-mcp`<br>`dealroom-mcp`<br>`google_drive` |
| [Verify Conditions Precedent](../tasks/verify-conditions-precedent.md) | [Legal & Compliance Desk](../agents/vc-legal-compliance-desk.md) | [Citation Enforcement](../skills/citation-enforcement/SKILL.md)<br>[Closing Coordination & CP Tracking](../skills/closing-coordination-and-cp-tracking/SKILL.md) | [Conditions Precedent Tracker Template](../alludium/documents/deal-room/conditions-precedent-tracker-template.md) (output_template, to `conditions_precedent_verification_artifact_id`)<br>[Legal Diligence Guide](../alludium/documents/deal-room/legal-diligence-guide.md) (methodology)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | `alludium-platform`<br>`affinity-mcp-server`<br>`exa-mcp-hosted`<br>`brave-search-mcp`<br>`dealroom-mcp`<br>`google_drive` |
| [Coordinate Capital Call And Completion](../tasks/coordinate-capital-call-and-completion.md) | [Legal & Compliance Desk](../agents/vc-legal-compliance-desk.md) | [Closing Coordination & CP Tracking](../skills/closing-coordination-and-cp-tracking/SKILL.md)<br>[VC Task & Next-Step Generation](../skills/vc-task-and-next-step-generation/SKILL.md)<br>[Citation Enforcement](../skills/citation-enforcement/SKILL.md) | [Completion Tracker Template](../alludium/documents/deal-room/completion-tracker-template.md) (output_template, to `completion_tracker_artifact_id`)<br>[Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.md) (style_guide)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | `alludium-platform`<br>`affinity-mcp-server`<br>`exa-mcp-hosted`<br>`brave-search-mcp`<br>`dealroom-mcp`<br>`google_drive` |
| [Prepare Portfolio Onboarding](../tasks/prepare-portfolio-onboarding.md) | [Legal & Compliance Desk](../agents/vc-legal-compliance-desk.md) | [Citation Enforcement](../skills/citation-enforcement/SKILL.md)<br>[Portfolio Onboarding & 100-Day Plan](../skills/portfolio-onboarding-and-100-day-plan/SKILL.md) | [Portfolio Onboarding Plan Template](../alludium/documents/deal-room/portfolio-onboarding-plan-template.md) (output_template, to `portfolio_onboarding_plan_artifact_id`)<br>[Template Use Guidance](../alludium/documents/shared/template-use-guidance.md) (operating_guidance) | `alludium-platform`<br>`affinity-mcp-server`<br>`exa-mcp-hosted`<br>`brave-search-mcp`<br>`dealroom-mcp`<br>`google_drive` |

## Invested

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| None mapped | None declared | None declared | None declared | None declared |

## Passed

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| None mapped | None declared | None declared | None declared | None declared |

## Archived

| Task | Agent | Skills | Documents | Integrations |
| --- | --- | --- | --- | --- |
| None mapped | None declared | None declared | None declared | None declared |
