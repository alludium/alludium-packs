---
id: vc-slack-sync-write
name: "VC Slack Sync Write"
description: >
  Draft approved Slack notifications and handoff messages for VC workflows,
  without broad posting or channel administration.
tags:
  - vc
  - slack
  - collaboration
  - sync-write
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: recommended
      required: false
      note: Approved writes may use `slack_v2-send-message-to-channel`, `slack_v2-reply-to-a-message`, `slack_v2-send-block-kit-message`, or `slack_v2-send-message-to-user-or-group`.
      gracefulDegradation: Draft message text and target metadata for human copy-and-send.
  routingHints:
    preferredSurface: skill
    notes:
      - Slack writes are limited to approved notifications and handoffs.
---

# VC Slack Sync Write

Use this skill to prepare Slack handoff drafts for review.

## Allowed Write Types

- Deal-room handoff notification to an approved channel
- IC prep or post-IC summary notification
- Reply draft in an approved deal thread
- Portfolio onboarding handoff after investment approval

## Required Inputs

- approved target channel, user, or thread
- exact message purpose
- message body or source artifact to summarize
- timing and owner approval

## Tool Guidance

Use write tools only after explicit approval:

- `slack_v2-send-message-to-channel`
- `slack_v2-reply-to-a-message`
- `slack_v2-send-block-kit-message`
- `slack_v2-send-message-to-user-or-group`

## Boundaries

- Do not use Slack for broad posting.
- Do not create, archive, invite, kick, delete, update profiles, or administer channels.
- Do not send founder-facing or external-party communications from this skill.
- Do not claim a message was sent unless a tool result confirms it.
