---
id: vc.check_affinity_relationships
title: Check Affinity Relationship Context
slug: check-affinity-relationships
agent: vc-origination-scout
skills:
- vc-relationship-context-check
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/check-affinity-relationships.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Check Affinity Relationship Context

Check whether sourcing candidates are already known in Affinity and capture relationship context without changing CRM records.

## Instructions

Mirror the reference pipeline's Affinity check by preferring exact domain match from enrichment or LinkedIn company data, then name fallback; treat a name-only match with no lists, notes, interactions, or owners as not found. Return lists, notes count, interaction flags, owner flags, deep link, and whether the company is known to the firm.

## Missing Input Policy

Ask for candidate batch, Affinity availability, approved lookup scope, and whether cached relationship state may be reused.

## External Action Policy

Read-only relationship check. Do not create organizations, list entries, notes, field values, tasks, or outreach.

## Completion Criteria

- Each checked candidate has found/not-found, matched-by, known-in-CRM, list names, note counts, interaction flags, owner flags, and source receipt where available.
- False-positive name-only matches are explicitly rejected.

## Human Decision Points

- None declared

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `relationship_check_scope` | Relationship Check Scope | `json` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `relationship_context_artifact_id` | Relationship Context Artifact | `file` | yes |
| `known_candidate_count` | Known Candidate Count | `number` | no |
| `relationship_report` | Relationship Report | `richtext` | no |

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/check-affinity-relationships.yaml`
- Alludium task ID: `vc.check_affinity_relationships`
- Task family: `origination_relationship_check`
- Lifecycle stage: `enrich`
- Recommended agent: `vc-origination-scout` (Alludium template `vc_origination_scout`)
- Supported project types:
  - `vc_origination_pipeline`
- Supported project scopes:
  - `project_instance`

## Required Skills

- `vc-relationship-context-check`
- `citation-enforcement`

## Planned Skills

- `vc-relationship-context-check`
- `citation-enforcement`
