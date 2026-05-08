---
id: vc-affinity-discovery
name: "VC Affinity Discovery"
description: >
  Discover Affinity CRM lists, stages, field structure, and pipeline object counts
  before proposing any VC Deal Room import or sync.
tags:
  - vc
  - affinity
  - crm
  - discovery
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: required
      required: true
      note: Use the connected Affinity application `affinity-mcp-server`; expected tool IDs include `affinity_list_opportunities`, `affinity_get_opportunity`, `affinity_get_list_entries`, `affinity_get_field_values`, and `affinity_get_field_value_changes` when discovered.
      gracefulDegradation: If Affinity tools are not discovered yet, ask for an authorized Affinity connection or an exported list/stage snapshot.
    - kind: setup
      importance: required
      required: true
      owner: user
      ownerPath: Authorize Affinity and choose list/stage scope before import or sync.
      confirmationRequired: true
      gracefulDegradation: Produce a discovery checklist only.
  routingHints:
    preferredSurface: skill
    notes:
      - Discovery is read-only and must end with scope choices, not import.
---

# VC Affinity Discovery

Use this skill to understand the firm's Affinity pipeline shape before any data is imported into Alludium.

## Required Inputs

- Authorized `affinity-mcp-server` connection or an exported Affinity snapshot
- Intended VC workflow, such as deal-room setup, pipeline hygiene, or weekly deal-flow review
- Any known list names, stage names, or owner fields the firm already uses

## Tool Plan

Use the discovered Affinity tools in this order when available:

1. Use `affinity_list_opportunities` to identify opportunity coverage and stage/status shape.
2. Use `affinity_get_list_entries` to inspect candidate lists and sample list entries.
3. Use `affinity_get_opportunity` on a small approved sample to understand opportunity fields.
4. Use `affinity_get_field_values` and `affinity_get_field_value_changes` to identify stage, owner, source, last activity, and VC-specific fields.

If the live Affinity application has no tool rows yet, report that tool discovery must run after connection authorization.

## Discovery Output

Return:

- `available_lists`: candidate Affinity lists or source scopes
- `stage_model`: stage/status fields and observed values
- `object_counts`: counts by list, stage, and object type when available
- `field_inventory`: important fields, owners, source/referrer fields, and date fields
- `sample_records_reviewed`: minimal approved samples only
- `recommended_scope`: the list/source and stages that should be considered for VC Deal Room setup
- `scope_questions`: user choices needed before read sync or import

## Boundaries

- Do not import records.
- Do not write notes, fields, stages, or list entries.
- Do not assume every Affinity list is deal pipeline.
- Ask the user to choose the list/source scope before any sync-read task runs.
