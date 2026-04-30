---
id: vc-task-and-next-step-generation
name: VC Task & Next-Step Generation
description: >
  Convert VC deal context, meeting notes, pipeline state, IC decisions, or closing
  blockers into owner-assigned next steps. Use this skill when producing action
  items, CRM update suggestions, stage-move recommendations, diligence follow-ups,
  or task-system drafts. It proposes actions; it does not create tasks, mutate CRM,
  or send messages without an approved workflow.
tags:
  - vc
  - tasks
  - next-steps
  - pipeline
  - operations
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: recommended
      required: false
      note: Next-step generation is strongest with meeting notes, CRM/deal-system state, prior task outputs, and task/project-system context. Provider-specific tool IDs are intentionally omitted because actions may be managed in different systems.
      gracefulDegradation: Produce suggested actions from provided context only.
    - kind: setup
      importance: recommended
      required: false
      owner: user
      ownerPath: Provide deal context, owner names, deadlines, and connected task/CRM surfaces before claiming actionable system updates.
      confirmationRequired: true
      gracefulDegradation: Return a human-review action list.
  routingHints:
    preferredSurface: skill
    notes:
      - Use this for suggestions and drafts; writes require explicit approval and connected tools.
---

# VC Task & Next-Step Generation

Turn deal evidence into specific, owner-assigned next steps.

## Minimum Inputs

- deal or company name
- current stage or workflow
- source context: meeting notes, transcript, CRM state, IC decision, DD output, or closing checklist
- human owner or ownership rules if known

## Process

1. Extract commitments, blockers, missing inputs, decisions, and follow-up requests.
2. Convert each into one concrete action with owner, due date, dependency, and source.
3. Separate internal actions from founder/external requests.
4. Identify CRM or task-system updates as suggestions, not completed mutations.
5. Group actions by urgency and stage gate.

## Output Contract

Return:

- `next_actions`: owner, action, due date, source, dependency, status
- `external_requests`: founder/counterparty asks that need message approval
- `crm_update_suggestions`: before/after field or note suggestions with evidence
- `task_system_drafts`: task titles/descriptions if a task system is connected
- `stage_transition_recommendation`: when supported by the evidence
- `approval_required`: sends, CRM writes, task creation, stage changes

## Tool Guidance

Use CRM/deal systems, meeting transcript providers, email/calendar context, and
task systems when connected. Examples include Affinity, Salesforce, HubSpot,
Granola, Otter, Fireflies, Gmail, Outlook, Asana, ClickUp, Monday, Jira, Linear,
Trello, and Notion.

## Related Skills

- Use `pipeline-health-and-crm-hygiene` when the primary job is pipeline triage,
  CRM/deal-system hygiene, stale-deal review, or stage movement.
- Use this skill when the primary job is turning meeting, IC, diligence, or
  closing context into owner/date/action drafts.

## Boundaries

- Do not create tasks or mutate CRM without explicit approval.
- Do not assign an external party as owner of an internal task.
- Do not infer dates when none are present; use `TBD` and ask.
- Do not move investment stages; recommend and require human confirmation.
