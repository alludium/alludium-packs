---
id: vc-slack-sync-read
name: "VC Slack Sync Read"
description: >
  Preview selected Slack channel, thread, message, and file context for VC
  deal-room tasks without broad workspace ingestion.
tags:
  - vc
  - slack
  - collaboration
  - sync-read
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: required
      required: true
      note: Use `slack_v2-find-message`, `slack_v2-list-replies`, `slack_v2-list-files`, and `slack_v2-get-file` only for approved channel/thread scope.
      gracefulDegradation: Ask for copied Slack excerpts or approved thread links.
  routingHints:
    preferredSurface: skill
    notes:
      - Read sync is selected-context only; do not ingest broad channel history.
---

# VC Slack Sync Read

Use this skill after Slack discovery has selected allowed channels or threads.

## Required Inputs

- Slack discovery report
- Approved workspace/channel/thread scope
- Deal, project, or task context that explains why Slack context is needed
- Sensitivity exclusions

## Tool Plan

1. Use `slack_v2-find-message` for targeted message lookup inside approved scope.
2. Use `slack_v2-list-replies` for approved threads.
3. Use `slack_v2-list-files` and `slack_v2-get-file` only when file context is explicitly allowed.

## Preview Output

Return:

- message/thread IDs and channel IDs used
- summarized context with timestamps and participants
- relevance to the VC deal-room task
- suggested target: knowledge source, artifact, task context, or setup context
- excluded content and reason

## Boundaries

- Do not read unapproved channels or unrelated history.
- Do not treat Slack conversation as final investment evidence without corroboration.
- Do not post or reply.
- Do not retain sensitive context beyond the approved task scope.
