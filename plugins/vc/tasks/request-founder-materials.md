---
id: vc.request_founder_materials
title: Request Founder Materials
slug: request-founder-materials
agent: vc-dealflow-concierge
skills:
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/request-founder-materials.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Request Founder Materials

Request Founder Materials for one venture-capital opportunity with evidence capture, human review gates, and next-action recommendations.

## Instructions

Prepare the missing-materials checklist, founder-friendly request draft, share instructions, and due-date recommendation for human approval before sending. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Create or update a durable project file artifact named Founder Materials Request and attach it to the required output field `founder_materials_request_artifact_id`. Use `definitionJson.documentRefs` as the durable document reference contract. Apply each reference by usage: `output_template` sets the output skeleton, `methodology` supplies scoring or analysis logic, `checklist` must be completed with status, evidence, and owner, `style_guide` governs citations and claim language, and `operating_guidance` or `policy` constrains process and approval boundaries. For refs with `outputFieldKey`, produce that output from the referenced pack document and preserve the document ID alongside the output artifact.

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
| `company_name` | Company Name | `string` | yes |
| `missing_materials` | Missing Materials | `string` | yes |
| `founder_contact` | Founder Contact | `string` | no |
| `due_date` | Due Date | `string` | no |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `founder_materials_request_artifact_id` | Founder Materials Request | `file` | yes |
| `materials_request_checklist` | Materials Request Checklist | `json` | no |
| `draft_external_message` | Draft External Message | `richtext` | no |
| `share_instructions` | Share Instructions | `string` | no |
| `due_date_recommendation` | Due Date Recommendation | `string` | no |
| `approval_required` | Approval Required | `string` | no |
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

- `vc.document.founder_materials_request_template` (output_template) -> `founder_materials_request_artifact_id`
- `vc.document.file_naming_source_index_sop` (operating_guidance)
- `vc.document.template_use_guidance` (operating_guidance)

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/request-founder-materials.yaml`
- Alludium task ID: `vc.request_founder_materials`
- Task family: `deal_room`
- Lifecycle stage: `evaluation`
- Recommended agent: `vc-dealflow-concierge` (Alludium template `vc_dealflow_concierge`)
- Supported project types:
  - `vc_deal_room`

## Required Skills

- `citation-enforcement`

## Planned Skills

- `founder-materials-request`
- `citation-enforcement`
