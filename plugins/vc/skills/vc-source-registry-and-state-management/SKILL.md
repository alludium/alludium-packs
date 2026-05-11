---
id: vc-source-registry-and-state-management
name: "VC Source Registry & State Management"
description: >
  Maintain origination source scope, dedupe keys, pagination state, run receipts,
  candidate action preservation, and degraded-source notes across VC sourcing tasks.
tags:
  - vc
  - origination
  - state
  - dedupe
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: setup
      importance: recommended
      required: false
      owner: user
      ownerPath: Confirm where source state is stored for this project and which fields are protected from automatic overwrite.
      confirmationRequired: true
      gracefulDegradation: Produce a state update proposal without persisting it.
  routingHints:
    preferredSurface: skill
    notes:
      - This skill defines state contracts; persistence depends on an approved platform or workspace write surface.
---

# VC Source Registry & State Management

Use this skill whenever an origination task reads, updates, or proposes changes to source state.

## State Model

Track source state by source key:

- `companies_house`: company numbers, search windows, query URLs, last extraction time
- `linkedin_people`: actor id, track, query, offset, seen profile ids, seen company slugs, exhaustion lock, quarantine rows
- `x_twitter`: actor id, query, seen tweet ids, author handles, last run window
- `github`: seen repository ids or full names, seen user logins, rate-limit notes
- `reddit`: seen post ids, subreddit/query windows, inbox approval state
- `manual_tip`: submitter, supplied identity fields, stable manual-tip key

## Preservation Rules

- Never overwrite human decisions unless the task has explicit write approval and the field is not protected.
- Treat `Pass`, `IC-Summary`, and `Reach out` style actions as protected.
- Treat manual status/contact progress as protected.
- Distinguish dry-run state proposals from approved state writes.

## Run Receipts

Every source task should return:

- Source name and approved scope used
- Query, actor, URL, or API surface used
- Result limit, run time, and lookback window
- Cost metadata when available, or `cost_unknown`
- Counts for new, duplicate, rejected, quarantined, errored, and skipped rows
- Pagination, exhaustion, rewind, and rate-limit notes

## Boundaries

- Do not create schedules.
- Do not write external records without explicit task approval.
- Do not infer that a candidate is new unless dedupe keys have been checked.
- Do not drop quarantine rows silently.
