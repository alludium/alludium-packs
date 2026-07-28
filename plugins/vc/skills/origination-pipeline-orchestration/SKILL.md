---
id: origination-pipeline-orchestration
name: "Origination Pipeline Orchestration"
description: >
  Configure the fund-level Origination Pipeline control plane and shape first-class
  Sourcing Line experiments without running sourcing automations.
tags:
  - vc
  - origination
  - setup
  - orchestration
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: setup
      importance: required
      required: true
      owner: user
      ownerPath: Confirm source choices, cadence intent, budget policy, and credential boundaries.
      confirmationRequired: true
      gracefulDegradation: Produce an unresolved setup checklist only.
  routingHints:
    preferredSurface: skill
    notes:
      - Configuration records intent and readiness; it does not activate scheduled sourcing.
---

# Origination Pipeline Orchestration

Use this skill to configure the fund-level Origination Pipeline and to shape Sourcing Line experiments before any sourcing run exists.

## Required Inputs

- Pipeline thesis and target geography, stage, and sector focus
- Selected source systems and source-scope policy
- Shared digest destination, aggregate budget policy, and review thresholds
- Credential-readiness evidence for selected integrations
- For a line: one hypothesis, registered source keys, query/screen, cadence, Inbox policy, outreach boundary, success metrics, and retirement condition

## Configuration Output

Return:

- `configuration_summary`: thesis, sources, cadence intent, budget policy, and unresolved decisions
- `source_registry`: reusable sources, approved connection scopes, actor allowlists, and credential state; do not embed line queries or cadence
- `review_policy`: promotion threshold, manual-review threshold, approval requirements, and excluded actions
- `child_task_plan`: setup tasks to create next, with the reason each task is needed
- Sourcing Line proposal: template key, hypothesis, source mix, screen, cadence, review/outreach policy, metrics, and required approvals

## Boundaries

- Do not run sourcing.
- Do not score candidates.
- Do not create candidate records.
- Do not collapse a sourcing experiment into a provider row in the shared source registry.
- Do not enable schedules or recurring jobs.
- Do not write to external systems.
- Do not send outreach or create Deal Pipeline projects.
