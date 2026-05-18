---
id: vc.prepare_portfolio_onboarding
title: Prepare Portfolio Onboarding
slug: prepare-portfolio-onboarding
agent: vc-legal-compliance-desk
skills:
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/prepare-portfolio-onboarding.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Prepare Portfolio Onboarding

Prepare Portfolio Onboarding for one venture-capital opportunity with evidence capture, human review gates, and next-action recommendations.

## Instructions

Prepare the portfolio handoff with board setup notes, reporting cadence, 100-day plan, milestones, support request intake, and owner assignments. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Use the required input file artifacts `ic_decision_record_artifact_id`, `closing_checklist_artifact_id`, and `conditions_precedent_verification_artifact_id` as source artifacts for the portfolio onboarding plan. Create or update a durable project file artifact named Portfolio Onboarding Plan and attach it to the required output field `portfolio_onboarding_plan_artifact_id`. Use `definitionJson.documentRefs` as the durable document reference contract. Apply each reference by usage: `output_template` sets the output skeleton, `methodology` supplies scoring or analysis logic, `checklist` must be completed with status, evidence, and owner, `style_guide` governs citations and claim language, and `operating_guidance` or `policy` constrains process and approval boundaries. For refs with `outputFieldKey`, produce that output from the referenced pack document and preserve the document ID alongside the output artifact.

## Missing Input Policy

Ask for missing required inputs before producing investment-stage recommendations.

## External Action Policy

Draft only unless a human explicitly approves the send, CRM write, Drive change, project creation, child task creation, or stage transition.

## Completion Criteria

- Required input gaps are resolved or listed as assumptions/open questions.
- Material conclusions include source links or are labeled as human judgment calls.
- Next actions identify owner, dependency, and required human approval point.

## Human Decision Points

- Approve investment-stage movement, pass/follow-up recommendations, and final task completion.
- Approve external communications, CRM writes, Drive/project creation, legal/counsel actions, and founder-facing requests.

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `ic_decision_record_artifact_id` | IC Decision Record | `file` | yes |
| `closing_checklist_artifact_id` | Closing Checklist | `file` | yes |
| `conditions_precedent_verification_artifact_id` | Conditions Precedent Verification | `file` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `portfolio_onboarding_plan_artifact_id` | Portfolio Onboarding Plan | `file` | yes |
| `board_setup_notes` | Board Setup Notes | `richtext` | no |
| `reporting_cadence` | Reporting Cadence | `string` | no |
| `hundred_day_plan` | Hundred Day Plan | `string` | no |
| `milestones` | Milestones | `json` | no |
| `support_request_intake` | Support Request Intake | `string` | no |
| `owner_assignments` | Owner Assignments | `string` | no |
| `summary` | Summary | `richtext` | no |
| `recommendation` | Recommendation | `string` | no |
| `source_links` | Source Links | `string` | no |
| `assumptions` | Assumptions | `string` | no |
| `evidence_quality` | Evidence Quality | `json` | no |
| `open_questions` | Open Questions | `json` | no |
| `risks` | Risks | `json` | no |
| `human_decision_points` | Human Decision Points | `string` | no |
| `next_actions` | Next Actions | `json` | no |

## Document References

- `vc.document.portfolio_onboarding_plan_template` (output_template) -> `portfolio_onboarding_plan_artifact_id`
- `vc.document.template_use_guidance` (operating_guidance)

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/prepare-portfolio-onboarding.yaml`
- Alludium task ID: `vc.prepare_portfolio_onboarding`
- Task family: `onboarding`
- Lifecycle stage: `closing`
- Recommended agent: `vc-legal-compliance-desk` (Alludium template `vc_legal_compliance_desk`)
- Supported project types:
  - `vc_deal_room`

## Required Skills

- `citation-enforcement`

## Planned Skills

- `portfolio-onboarding-and-100-day-plan`
- `citation-enforcement`
