---
id: origination-pipeline-orchestration
name: "Origination Pipeline Orchestration"
description: >
  Configure and operate one Fund-specific VC Sourcing Line's hypothesis, source
  registry, cadence intent, budget policy, review thresholds, and reviewed run plan.
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
      ownerPath: Confirm the line's Fund, source choices, cadence intent, budget policy, and credential boundaries.
      confirmationRequired: true
      gracefulDegradation: Produce an unresolved setup checklist only.
  routingHints:
    preferredSurface: skill
    notes:
      - Configuration records intent and readiness; it does not activate scheduled sourcing.
---

# Sourcing Line Orchestration

Use this skill for one Sourcing Line: one Fund-specific, measurable sourcing experiment with its own hypothesis, sources, screen, cadence, receipts, costs, and retirement condition. Do not assume a standing singleton pipeline, a cross-line digest, or an Origination Hub.

## Required Inputs

- Exact Sourcing Line project and its active canonical Fund record
- Line hypothesis and target geography, stage, and sector focus
- Selected source systems and line-scoped source policy
- Cadence intent, result limit, budget policy, review thresholds, and retirement condition
- Credential-readiness evidence for selected integrations

## Configuration Output

Return:

- `configuration_summary`: Fund, line hypothesis, sources, cadence intent, budget policy, success measures, retirement condition, and unresolved decisions
- `source_registry`: selected sources, scope notes, actor or query allowlists, and credential state
- `review_policy`: promotion threshold, manual-review threshold, approval requirements, and excluded actions
- `child_task_plan`: setup tasks to create next, with the reason each task is needed

For a reviewed run, keep every child task, receipt, artifact, candidate relationship, source-health result, and cost on this exact Sourcing Line. Do not combine evidence from another line merely because the lines share a Fund or source.

Workspace summaries are explicitly on demand. When requested, aggregate only the readable Sourcing Lines and Candidates supplied by the workspace projection, state scope and freshness, and preserve Fund and observation-window distinctions. Do not create a mandatory cross-line schedule or digest destination.

## Boundaries

- Do not run a source outside the reviewed line task and its approved bounded child tasks.
- Do not score or create Candidates in the orchestration step; route those actions to their reviewed tasks.
- Do not enable schedules or recurring jobs.
- Do not write to external systems.
- Do not send outreach or create Deal Pipeline projects.
- Do not create or rely on a singleton Origination Pipeline or cross-line digest.
