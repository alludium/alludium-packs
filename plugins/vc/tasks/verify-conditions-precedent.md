---
id: vc.verify_conditions_precedent
title: Verify Conditions Precedent
slug: verify-conditions-precedent
agent: vc-legal-compliance-desk
skills:
- citation-enforcement
---

# Verify Conditions Precedent

Verify Conditions Precedent for one venture-capital opportunity with evidence capture, human review gates, and next-action recommendations.

## Instructions

Map conditions precedent to available closing evidence, identify missing items and blocker severity, and prepare counsel review recommendation and signing readiness. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Use the required input file artifact `closing_checklist_artifact_id` as the closing checklist subject, and use `closing_source_artifact_ids` for legal documents, counsel notes, CP lists, signed documents, and evidence files. Create or update a durable project file artifact named Conditions Precedent Verification and attach it to the required output field `conditions_precedent_verification_artifact_id`.

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
| `closing_checklist_artifact_id` | Closing Checklist | `file` | yes |
| `closing_source_artifact_ids` | Closing Source Artifact IDs | `string` | yes |
| `counsel_requirements` | Counsel Requirements | `json` | no |
| `closing_status` | Closing Status | `string` | no |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `conditions_precedent_verification_artifact_id` | Conditions Precedent Verification | `file` | yes |
| `cp_evidence_mapping` | Cp Evidence Mapping | `json` | no |
| `missing_items` | Missing Items | `string` | no |
| `blocker_severity` | Blocker Severity | `string` | no |
| `counsel_review_recommendation` | Counsel Review Recommendation | `string` | no |
| `signing_readiness` | Signing Readiness | `string` | no |
| `summary` | Summary | `richtext` | no |
| `recommendation` | Recommendation | `string` | no |
| `source_links` | Source Links | `string` | no |
| `assumptions` | Assumptions | `string` | no |
| `evidence_quality` | Evidence Quality | `json` | no |
| `open_questions` | Open Questions | `json` | no |
| `risks` | Risks | `json` | no |
| `human_decision_points` | Human Decision Points | `string` | no |
| `next_actions` | Next Actions | `json` | no |

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/verify-conditions-precedent.yaml`
- Alludium task ID: `vc.verify_conditions_precedent`
- Task family: `closing`
- Lifecycle stage: `closing`
- Recommended agent: `vc-legal-compliance-desk` (Alludium template `vc_legal_compliance_desk`)
- Supported project types:
  - `vc_deal_room`

## Required Skills

- `citation-enforcement`

## Planned Skills

- `closing-coordination-and-cp-tracking`
- `citation-enforcement`
