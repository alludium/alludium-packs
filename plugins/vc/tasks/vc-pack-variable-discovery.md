---
id: vc.pack_variable_discovery
title: VC Pack Variable Discovery
slug: vc-pack-variable-discovery
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/pack-variable-discovery.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# VC Pack Variable Discovery

Best-effort, review-only discovery for VC Pack Setup variables and invite suggestions.

## Instructions

Use only the task input, task context, and safe workspace/onboarding context provided to this task to suggest values for the declared VC setup variables. Return best-effort answers keyed by namespace.key and include a concise rationale for each answer when evidence exists. Also suggest likely internal invite candidates only when the provided context contains safe email, calendar, company, or workspace signals. Do not browse external systems, sample CRM data, create projects, send invites, connect apps, persist workspace facts, or write to external systems. Finish by calling task-management.completeTask with output containing summary, variable_answers, and invite_candidates. The parent Pack Setup task remains the only review and persistence surface.

## Missing Input Policy

No separate missing-input policy is declared. Follow the execution instructions and ask only when needed.

## External Action Policy

No separate external-action policy is declared. Do not take external or persistent actions unless the task instructions explicitly allow them.

## Completion Criteria

- Produce a concise summary of which setup variables could be inferred.
- Include variable_answers as an object keyed by namespace.key.
- Include invite_candidates as an array only when safe context supports them.
- Mark uncertain or missing answers as review-needed instead of inventing facts.
- Do not claim persistence or activation has occurred.

## Human Decision Points

- None declared

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `declared_variables` | Declared Variables | `json` | yes |
| `current_answers` | Current Answers | `json` | no |
| `workspace_context` | Workspace Context | `json` | no |

## Context Fields

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `pack_setup` | Pack Setup Context | `json` | no |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `summary` | Summary | `richtext` | no |
| `variable_answers` | Variable Answers | `json` | no |
| `invite_candidates` | Invite Candidates | `json` | no |

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/pack-variable-discovery.yaml`
- Alludium task ID: `vc.pack_variable_discovery`
- Task family: `pack_setup`
- Lifecycle stage: `setup`
- Supported project types:
  - None declared

## Required Skills

- None declared

## Planned Skills

- None declared
