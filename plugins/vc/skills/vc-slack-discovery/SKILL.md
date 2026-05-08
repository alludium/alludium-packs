---
id: vc-slack-discovery
name: "VC Slack Discovery"
description: >
  Discover Slack workspace and channel scope for VC deal-room context,
  notifications, and handoffs before reading messages or proposing writes.
tags:
  - vc
  - slack
  - collaboration
  - discovery
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: required
      required: true
      note: Use the connected Slack application `slack_v2`; expected discovery tools are `slack_v2-get-current-user` and `slack_v2-list-channels`.
      gracefulDegradation: Ask for Slack authorization or a supplied channel list.
  routingHints:
    preferredSurface: skill
    notes:
      - Discovery classifies channels and asks for scope approval before reading messages.
---

# VC Slack Discovery

Use this skill to decide which Slack surfaces, if any, should be available to VC workflows.

## Required Inputs

- Authorized `slack_v2` connection or a supplied channel inventory
- Intended workflow: deal intake, IC prep, portfolio handoff, operations, or notifications
- Known sensitive or excluded channels

## Tool Plan

1. Use `slack_v2-get-current-user` to confirm the active workspace and authorized user context.
2. Use `slack_v2-list-channels` to list candidate public/private channels visible to the connection.
3. Classify channels from name, topic, purpose, and user-supplied context.

## Channel Classifications

Use these labels:

- deal intake
- deal-specific discussion
- IC prep or IC decisions
- portfolio handoff
- operations
- broad/general
- sensitive/excluded
- unknown

## Discovery Output

Return:

- workspace identity
- channel inventory with classification and confidence
- recommended included channels
- excluded channels and why
- questions for the user to approve channel/thread scope

## Boundaries

- Do not read message history during discovery.
- Do not post, reply, create channels, or change channel settings.
- Do not include broad/general channels without explicit user selection.
