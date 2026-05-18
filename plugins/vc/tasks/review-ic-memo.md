---
id: vc.review_ic_memo
title: Review IC Memo
slug: review-ic-memo
agent: vc-ic-prep-producer
skills:
- citation-enforcement
- ic-memo-assembly
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/review-ic-memo.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Review IC Memo

Review IC Memo for one venture-capital opportunity with evidence capture, human review gates, and next-action recommendations.

## Instructions

Review the IC memo and pack for findings, citation gaps, assumption gaps, unresolved risks, decision readiness, and required changes. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Use the required input file artifacts `investment_memo_artifact_id` and `ic_agenda_artifact_id` as the memo and agenda under review; do not substitute a task slug, UI label, or pasted memo text for artifact-backed files. Create or update a durable project file artifact named IC Memo Review and attach it to the required output field `ic_memo_review_artifact_id`. Use `definitionJson.documentRefs` as the durable document reference contract. Apply each reference by usage: `output_template` sets the output skeleton, `methodology` supplies scoring or analysis logic, `checklist` must be completed with status, evidence, and owner, `style_guide` governs citations and claim language, and `operating_guidance` or `policy` constrains process and approval boundaries. For refs with `outputFieldKey`, produce that output from the referenced pack document and preserve the document ID alongside the output artifact.

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
| `investment_memo_artifact_id` | Investment Memo | `file` | yes |
| `ic_agenda_artifact_id` | IC Agenda | `file` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `ic_memo_review_artifact_id` | IC Memo Review | `file` | yes |
| `review_summary` | Review Summary | `richtext` | no |
| `review_findings` | Review Findings | `string` | no |
| `citation_gaps` | Citation Gaps | `string` | no |
| `assumption_gaps` | Assumption Gaps | `string` | no |
| `unresolved_risks` | Unresolved Risks | `json` | no |
| `decision_readiness` | Decision Readiness | `string` | no |
| `required_changes` | Required Changes | `string` | no |
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

- `vc.document.ic_memo_review_template` (output_template) -> `ic_memo_review_artifact_id`
- `vc.document.evidence_citation_style_guide` (style_guide)
- `vc.document.template_use_guidance` (operating_guidance)

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/review-ic-memo.yaml`
- Alludium task ID: `vc.review_ic_memo`
- Task family: `ic`
- Lifecycle stage: `review`
- Recommended agent: `vc-ic-prep-producer` (Alludium template `vc_ic_prep_producer`)
- Supported project types:
  - `vc_deal_room`

## Required Skills

- `citation-enforcement`
- `ic-memo-assembly`

## Planned Skills

- `citation-enforcement`
- `ic-risk-checklist-and-decision-log`
- `ic-memo-assembly`
