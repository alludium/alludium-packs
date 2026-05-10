---
id: vc-origination-pipeline-orchestration
name: "VC Origination Pipeline Orchestration"
description: >
  Configure a VC origination pipeline's thesis, source registry, cadence intent,
  budget policy, review thresholds, and setup-task plan without running sourcing
  automations.
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

# VC Origination Pipeline Orchestration

Use this skill to configure the standing VC origination pipeline before any sourcing run exists.

## Required Inputs

- Pipeline thesis and target geography, stage, and sector focus
- Selected source systems and source-scope policy
- Cadence intent, digest destination, budget policy, and review thresholds
- Credential-readiness evidence for selected integrations

## Configuration Output

Return:

- `configuration_summary`: thesis, sources, cadence intent, budget policy, and unresolved decisions
- `source_registry`: selected sources, scope notes, actor or query allowlists, and credential state
- `review_policy`: promotion threshold, manual-review threshold, approval requirements, and excluded actions
- `child_task_plan`: setup tasks to create next, with the reason each task is needed

## Boundaries

- Do not run sourcing.
- Do not score candidates.
- Do not create candidate records.
- Do not enable schedules or recurring jobs.
- Do not write to external systems.
- Do not send outreach or create Deal Room projects.
