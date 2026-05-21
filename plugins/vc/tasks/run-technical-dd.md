---
id: vc.run_technical_dd
title: Run Technical DD
slug: run-technical-dd
agent: vc-diligence-analyst
skills:
- team-and-hiring-assessment
- red-flags-scanner
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/run-technical-dd.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Run Technical DD

Run Technical DD for one venture-capital opportunity with evidence capture, human review gates, and next-action recommendations.

## Instructions

Run technical diligence covering architecture, product, engineering team, IP and licensing, AI/ML risks, scalability, security, and technical scorecard from the supplied technical source artifact list and approved access references. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Create or update a durable project file artifact named Technical DD Report and attach it to the required output field `technical_dd_artifact_id`. Use `definitionJson.documentRefs` as the durable document reference contract. Apply each reference by usage: `output_template` sets the output skeleton, `methodology` supplies scoring or analysis logic, `checklist` must be completed with status, evidence, and owner, `style_guide` governs citations and claim language, and `operating_guidance` or `policy` constrains process and approval boundaries. For refs with `outputFieldKey`, produce that output from the referenced pack document and preserve the document ID alongside the output artifact.

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
| `technical_source_artifact_ids` | Technical Source Artifact IDs | `string` | yes |
| `repo_or_code_access` | Repo Or Code Access | `string` | yes |
| `product_roadmap` | Product Roadmap | `string` | no |
| `ip_patent_materials` | Ip Patent Materials | `string` | no |
| `engineering_team_materials` | Engineering Team Materials | `string` | no |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `technical_dd_artifact_id` | Technical DD Report | `file` | yes |
| `architecture_product_summary` | Architecture Product Summary | `richtext` | no |
| `technical_team_assessment` | Technical Team Assessment | `string` | no |
| `oss_licensing_ip_checks` | Oss Licensing Ip Checks | `string` | no |
| `ai_ml_risk_assessment` | Ai Ml Risk Assessment | `string` | no |
| `scalability_security_concerns` | Scalability Security Concerns | `string` | no |
| `technical_scorecard` | Technical Scorecard | `string` | no |
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

- `vc.document.diligence_report_template` (output_template) -> `technical_dd_artifact_id`
- `vc.document.evidence_citation_style_guide` (style_guide)
- `vc.document.template_use_guidance` (operating_guidance)

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/run-technical-dd.yaml`
- Alludium task ID: `vc.run_technical_dd`
- Task family: `diligence`
- Lifecycle stage: `formal_diligence`
- Recommended agent: `vc-diligence-analyst` (Alludium template `vc_diligence_analyst`)
- Supported project types:
  - `vc_deal_room`

## Required Skills

- `team-and-hiring-assessment`
- `red-flags-scanner`
- `citation-enforcement`

## Planned Skills

- `technical-diligence-workstream`
- `team-and-hiring-assessment`
- `red-flags-scanner`
- `citation-enforcement`
