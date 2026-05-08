---
id: vc-affinity-sync-read
name: "VC Affinity Sync Read"
description: >
  Design and preview read/import sync from a selected Affinity list or pipeline
  scope into VC Deal Room projects, fields, tasks, and artifacts.
tags:
  - vc
  - affinity
  - crm
  - sync-read
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: required
      required: true
      note: Use `affinity_search_companies`, `affinity_get_company`, `affinity_list_company_notes`, `affinity_search_persons`, `affinity_get_person`, `affinity_list_opportunities`, `affinity_get_opportunity`, and `affinity_get_list_entries` when discovered.
      gracefulDegradation: Draft a preview/import contract from the discovery artifact and mark all live reads blocked.
  routingHints:
    preferredSurface: skill
    notes:
      - Sync read is preview/import oriented; recurring sync is out of scope until approved separately.
---

# VC Affinity Sync Read

Use this skill after Affinity discovery has selected the list/source and stage scope.

## Required Inputs

- Affinity discovery report
- Selected list or source scope
- Selected stages/statuses considered active pipeline
- Target mapping preference: create/update Deal Room projects, project fields, tasks, artifacts, or setup context

## Tool Plan

Use Affinity tools only within the approved scope:

1. Use `affinity_get_list_entries` or `affinity_list_opportunities` to create the scoped preview set.
2. Use `affinity_get_opportunity` for opportunity-level fields.
3. Use `affinity_search_companies` and `affinity_get_company` for company identity resolution.
4. Use `affinity_search_persons` and `affinity_get_person` for founder/contact context.
5. Use `affinity_list_company_notes` only when notes are explicitly in scope.

## Preview Contract

Return a preview before import:

- source ID, source URL, company/opportunity identity, current stage, owner, source/referrer, last activity
- proposed Alludium target object and field mapping
- conflicts, duplicates, missing required fields, and records rejected from import
- provenance for each imported field

## Boundaries

- Do not import without preview approval.
- Do not treat Affinity as authoritative for investment judgment.
- Do not create or update Affinity records.
- Do not enable recurring sync from this task.
