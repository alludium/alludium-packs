---
id: vc.prepare_lead_gen_packet
title: Prepare Lead Gen Packet
slug: prepare-lead-gen-packet
agent: vc-origination-scout
skills:
- company-research-and-enrichment
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/prepare-lead-gen-packet.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Prepare Lead Gen Packet

Prepare Lead Gen Packet for one venture-capital opportunity with evidence capture, human review gates, and next-action recommendations.

## Instructions

Prepare the lead-generation meeting packet from candidate companies and thesis context; include per-company snapshots, discussion points, and proposed next actions. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Use workspace-configured scoring frameworks, CRM providers, stage names, and deal-type metric packs; do not assume a specific fund, CRM, or SaaS default unless the workspace configuration explicitly selects it. Create or update a durable management task file artifact named Lead Generation Packet and attach it to the required output field `lead_generation_packet_artifact_id`; do not assume this project-management scoped output is indexed onto a single Deal Room project. Use `definitionJson.documentRefs` as the durable document reference contract. Apply each reference by usage: `output_template` sets the output skeleton, `methodology` supplies scoring or analysis logic, `checklist` must be completed with status, evidence, and owner, `style_guide` governs citations and claim language, and `operating_guidance` or `policy` constrains process and approval boundaries. For refs with `outputFieldKey`, produce that output from the referenced pack document and preserve the document ID alongside the output artifact.

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
| `candidate_companies` | Candidate Companies | `json` | yes |
| `meeting_date` | Meeting Date | `string` | yes |
| `thesis_context` | Thesis Context | `richtext` | no |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `lead_generation_packet_artifact_id` | Lead Generation Packet | `file` | yes |
| `lead_gen_packet` | Lead Gen Packet | `json` | no |
| `per_company_snapshots` | Per Company Snapshots | `json` | no |
| `discussion_points` | Discussion Points | `string` | no |
| `proposed_next_actions` | Proposed Next Actions | `json` | no |
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

- `vc.document.lead_generation_packet_template` (output_template) -> `lead_generation_packet_artifact_id`
- `vc.document.evidence_citation_style_guide` (style_guide)
- `vc.document.template_use_guidance` (operating_guidance)

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/prepare-lead-gen-packet.yaml`
- Alludium task ID: `vc.prepare_lead_gen_packet`
- Task family: `pipeline`
- Lifecycle stage: `assessment`
- Recommended agent: `vc-origination-scout` (Alludium template `vc_origination_scout`)
- Supported project types:
  - `vc_deal_room`
- Supported project scopes:
  - `project_management`

## Required Skills

- `company-research-and-enrichment`
- `citation-enforcement`

## Planned Skills

- `company-research-and-enrichment`
- `citation-enforcement`

## Workspace-Configured Methodology Skills

- `market-map-building`: Use only when the workspace explicitly configures this market mapping method.
- `investment-screening-framework`: Use only when the workspace explicitly configures this screening framework.
