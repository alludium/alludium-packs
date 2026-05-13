---
id: vc.discover_companies_house_candidates
title: Discover Companies House Candidates
slug: discover-companies-house-candidates
agent: vc-origination-scout
skills:
- vc-companies-house-sourcing
- vc-source-registry-and-state-management
- citation-enforcement
---

# Discover Companies House Candidates

Discover UK company candidates from approved Companies House public-register pages using reference-pipeline scoring and dedupe patterns.

## Instructions

Discover candidate companies from approved public Companies House search/result pages. Mirror the reference pipeline's two-window intent for recent incorporations and mature/fundraising-age companies. Prioritize active UK companies with software, data, R&D, biotech, AI, robotics, or deep-tech signals; reject mass-registration addresses, service/consultancy language, outside-geography signals, corporate officers, and weak name/location/founder evidence. Use company number as the primary dedupe key.

## Missing Input Policy

Ask for selected public URL patterns, geography/stage/sector scope, result limits, allowed SIC or keyword filters, and Firecrawl availability before extraction.

## External Action Policy

Read preview and candidate proposal only. Do not call the Companies House API, import candidates, score final verdicts, enable recurring monitoring, write CRM rows, or create Deal Rooms.

## Completion Criteria

- Candidate preview includes company number, name, status, incorporation date, visible SIC/nature text, address locality, founder/officer hints when visible, source URL, and extraction timestamp.
- Rejection reasons and dedupe decisions are listed.
- Source-state update records company-number keys and selected search windows.

## Human Decision Points

- None declared

## Inputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `companies_house_discovery_scope` | Companies House Discovery Scope | `json` | yes |

## Outputs

| Key | Name | Type | Required |
| --- | --- | --- | --- |
| `companies_house_discovery_artifact_id` | Companies House Discovery Artifact | `file` | yes |
| `discovery_report` | Discovery Report | `richtext` | no |
| `source_result_count` | Source Result Count | `number` | no |
| `source_state_summary` | Source State Summary | `string` | no |

## Routing

- Source template: `alludium/task-definition-templates/vc-workflows/discover-companies-house-candidates.yaml`
- Alludium task ID: `vc.discover_companies_house_candidates`
- Task family: `origination_source_discovery`
- Lifecycle stage: `source`
- Recommended agent: `vc-origination-scout` (Alludium template `vc_origination_scout`)
- Supported project types:
  - `vc_origination_pipeline`
- Supported project scopes:
  - `project_instance`

## Required Skills

- `vc-companies-house-sourcing`
- `vc-source-registry-and-state-management`
- `citation-enforcement`

## Planned Skills

- `vc-companies-house-sourcing`
- `vc-source-registry-and-state-management`
- `citation-enforcement`
