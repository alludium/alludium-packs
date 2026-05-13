---
id: vc.discover_linkedin_founders
title: Discover LinkedIn Founder Candidates
slug: discover-linkedin-founders
agent: vc-origination-scout
skills:
- vc-apify-linkedin-founder-discovery
- vc-source-registry-and-state-management
- citation-enforcement
---

<!-- Generated from alludium/task-definition-templates/vc-workflows/discover-linkedin-founders.yaml; do not edit directly. Run python plugins/vc/scripts/generate_markdown.py after changing the YAML source. -->

# Discover LinkedIn Founder Candidates

Find early UK/Ireland AI founder and company candidates through approved Apify LinkedIn actor tracks.

## Instructions

Use only approved Apify LinkedIn actor scopes. Mirror the reference pipeline's four-track model covering active AI founders, pedigree founders, exited or serial founders, and academic spinouts. Preserve per-query pagination/offsets, exhaustion locks, seen profile IDs, company URL slug dedupe, and quarantine rows without stable company identifiers. Treat LinkedIn people discovery as weekly by default because it is the expensive source.

## Missing Input Policy

Ask for actor allowlist, track selection, geography, result caps, query budget, dedupe-state availability, and whether this is a weekly full run or forced override.

## External Action Policy

Discovery proposal only. Do not scrape unapproved profiles, bypass platform policy, import candidates, write CRM records, send outreach, or create Deal Rooms.

## Completion Criteria

- Candidate preview includes track, founder profile URL, company name, company LinkedIn URL or stable key, founder role, geography evidence, score reasons, and source receipt.
- Source-state update includes seen profile IDs, company slugs, query offsets, exhaustion/rewind notes, and quarantine rows.
- Cost/run metadata or missing cost metadata is explicit.

## Human Decision Points

- None declared

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `linkedin_discovery_scope` | LinkedIn Discovery Scope | `json` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `linkedin_discovery_artifact_id` | LinkedIn Discovery Artifact | `file` | yes |
| `discovery_report` | Discovery Report | `richtext` | no |
| `source_result_count` | Source Result Count | `number` | no |
| `source_state_summary` | Source State Summary | `string` | no |

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/discover-linkedin-founders.yaml`
- Alludium task ID: `vc.discover_linkedin_founders`
- Task family: `origination_source_discovery`
- Lifecycle stage: `source`
- Recommended agent: `vc-origination-scout` (Alludium template `vc_origination_scout`)
- Supported project types:
  - `vc_origination_pipeline`
- Supported project scopes:
  - `project_instance`

## Required Skills

- `vc-apify-linkedin-founder-discovery`
- `vc-source-registry-and-state-management`
- `citation-enforcement`

## Planned Skills

- `vc-apify-linkedin-founder-discovery`
- `vc-source-registry-and-state-management`
- `citation-enforcement`
