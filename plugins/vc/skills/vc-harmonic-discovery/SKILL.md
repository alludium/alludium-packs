---
id: vc-harmonic-discovery
name: "VC Harmonic Discovery"
description: >
  Discover Harmonic saved search, daily search, or source scope before processing
  company and founder intelligence for VC sourcing.
tags:
  - vc
  - harmonic
  - company-intelligence
  - discovery
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: required
      required: true
      note: Use the connected Harmonic application `harmonic-mcp-oauth` after OAuth authorization and tool discovery. The current local platform catalog has no trusted Harmonic tool external IDs.
      gracefulDegradation: Report that Harmonic has no discovered tool rows and ask for authorization/tool discovery or a supplied saved-search inventory.
  routingHints:
    preferredSurface: skill
    notes:
      - Discovery verifies whether live Harmonic tools exist before naming or using any tool ID.
---

# VC Harmonic Discovery

Use this skill to identify Harmonic source scope for VC sourcing workflows.

## Required Inputs

- Authorized `harmonic-mcp-oauth` connection with discovered tool rows, or a supplied saved-search inventory
- Intended workflow, such as thesis sourcing, daily search review, market-map expansion, or first-look screening
- Known saved search, daily search, geography, sector, stage, or company filters

## Tool Plan

First verify whether the Harmonic application has live discovered tools. In the current local platform catalog, `harmonic-mcp-oauth` exists as a `DIRECT_REMOTE` OAuth application but has zero tool rows, so specific tool IDs cannot be trusted yet.

When tool discovery later succeeds:

1. Enumerate available saved searches, daily searches, or comparable source scopes.
2. Capture stable source IDs and available result counts.
3. Ask the user to choose the source scope before processing company or person results.

## Discovery Output

Return:

- `tool_discovery_status`: discovered, missing, or blocked
- `available_source_scopes`: saved searches, daily searches, or equivalent source scopes when available
- `source_scope_ids`: stable source IDs when available
- `recommended_scope`: the selected search/source to process next
- `scope_questions`: user choices needed before sync read

## Boundaries

- Do not process company or person result payloads during discovery.
- Do not mark net-new results as seen.
- Do not update saved searches, export contacts, or write back to Harmonic.
- Do not invent Harmonic tool IDs when the platform has not discovered them.
