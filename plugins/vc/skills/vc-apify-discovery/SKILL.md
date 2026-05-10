---
id: vc-apify-discovery
name: "VC Apify Discovery"
description: >
  Discover approved Apify actor and source scope for VC origination without
  launching scheduled sourcing runs or importing candidates.
tags:
  - vc
  - apify
  - discovery
  - origination
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: required
      required: true
      note: Use the connected Apify application `apify-actors-mcp` after authorization and tool discovery.
      gracefulDegradation: Report missing Apify tool discovery and ask for an approved actor inventory.
  routingHints:
    preferredSurface: skill
    notes:
      - Discovery ends with source choices and does not process candidate queues.
---

# VC Apify Discovery

Use this skill to identify approved Apify actors and source scope for VC origination setup.

## Required Inputs

- Authorized `apify-actors-mcp` connection or a supplied actor inventory
- Approved actor/source policy, including whether LinkedIn, X, or other actors are allowed
- Intended query or source filters and sample-read limits

## Discovery Output

Return:

- `tool_discovery_status`: discovered, missing, or blocked
- `available_actors`: approved actors with source purpose and input requirements
- `source_scope_ids`: actor IDs, dataset IDs, saved inputs, or supplied source references when available
- `cost_controls`: run budget, result limit, and retry policy questions
- `scope_questions`: user choices needed before sync read

## Boundaries

- Do not start actor runs unless a later read-preview task explicitly approves a sample run.
- Do not import candidates.
- Do not persist candidate state.
- Do not enable schedules.
- Do not contact founders or write to external systems.
