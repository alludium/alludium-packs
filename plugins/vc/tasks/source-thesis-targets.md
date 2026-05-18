---
id: vc.source_thesis_targets
title: Source Thesis Targets
slug: source-thesis-targets
agent: vc-origination-scout
skills:
- company-research-and-enrichment
- founder-outreach-and-intro-paths
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/source-thesis-targets.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Source Thesis Targets

Source Thesis Targets for one venture-capital opportunity with evidence capture, human review gates, and next-action recommendations.

## Instructions

Research thesis-aligned companies for the requested thesis area, geography, stage focus, and market filters; return target companies, fit rationale, source links, warm intro paths, and confidence notes. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Use workspace-configured scoring frameworks, CRM providers, stage names, and deal-type metric packs; do not assume a specific fund, CRM, or SaaS default unless the workspace configuration explicitly selects it. Create or update a durable project file artifact named Thesis Target List and attach it to the required output field `thesis_target_list_artifact_id`. Use `definitionJson.documentRefs` as the durable document reference contract. Apply each reference by usage: `output_template` sets the output skeleton, `methodology` supplies scoring or analysis logic, `checklist` must be completed with status, evidence, and owner, `style_guide` governs citations and claim language, and `operating_guidance` or `policy` constrains process and approval boundaries. For refs with `outputFieldKey`, produce that output from the referenced pack document and preserve the document ID alongside the output artifact.

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
| `thesis_area` | Thesis Area | `string` | yes |
| `geography` | Geography | `string` | yes |
| `stage_focus` | Stage Focus | `string` | no |
| `market_filters` | Market Filters | `json` | no |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `thesis_target_list_artifact_id` | Thesis Target List | `file` | yes |
| `target_company_list` | Target Company List | `json` | no |
| `fit_rationale` | Fit Rationale | `string` | no |
| `source_links` | Source Links | `string` | no |
| `warm_intro_paths` | Warm Intro Paths | `string` | no |
| `confidence_notes` | Confidence Notes | `richtext` | no |
| `summary` | Summary | `richtext` | no |
| `recommendation` | Recommendation | `string` | no |
| `assumptions` | Assumptions | `string` | no |
| `evidence_quality` | Evidence Quality | `json` | no |
| `open_questions` | Open Questions | `json` | no |
| `risks` | Risks | `json` | no |
| `human_decision_points` | Human Decision Points | `string` | no |
| `next_actions` | Next Actions | `json` | no |

## Document References

- `vc.document.thesis_target_list_template` (output_template) -> `thesis_target_list_artifact_id`
- `vc.document.evidence_citation_style_guide` (style_guide)
- `vc.document.template_use_guidance` (operating_guidance)

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/source-thesis-targets.yaml`
- Alludium task ID: `vc.source_thesis_targets`
- Task family: `pipeline`
- Lifecycle stage: `assessment`
- Recommended agent: `vc-origination-scout` (Alludium template `vc_origination_scout`)
- Supported project types:
  - `vc_deal_room`

## Required Skills

- `company-research-and-enrichment`
- `founder-outreach-and-intro-paths`
- `citation-enforcement`

## Planned Skills

- `company-research-and-enrichment`
- `founder-outreach-and-intro-paths`
- `citation-enforcement`

## Workspace-Configured Methodology Skills

- `market-map-building`: Use only when the workspace explicitly configures this market mapping method.
