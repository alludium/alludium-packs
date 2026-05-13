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

<!-- Generated from alludium/task-definition-templates/vc-workflows/source-thesis-targets.yaml; do not edit directly. Run python plugins/vc/scripts/generate_markdown.py after changing the YAML source. -->

# Source Thesis Targets

Source Thesis Targets for one venture-capital opportunity with evidence capture, human review gates, and next-action recommendations.

## Instructions

Research thesis-aligned companies for the requested thesis area, geography, stage focus, and market filters; return target companies, fit rationale, source links, warm intro paths, and confidence notes. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Use workspace-configured scoring frameworks, CRM providers, stage names, and deal-type metric packs; do not assume a specific fund, CRM, or SaaS default unless the workspace configuration explicitly selects it. Create or update a durable project file artifact named Thesis Target List and attach it to the required output field `thesis_target_list_artifact_id`.

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
