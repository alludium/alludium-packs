---
id: vc.slack_sync_write
title: Draft Slack Handoff Notifications
slug: slack-sync-write
agent: vc-integration-operator
skills:
- vc-slack-sync-write
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-integrations/slack-sync-write.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Draft Slack Handoff Notifications

## Objective

Draft approved Slack handoff notifications for VC workflows without broad posting.

## What To Do

Draft Slack notification or handoff messages for an approved channel, user, or thread. Approved execution tools may include `slack_v2-send-message-to-channel`, `slack_v2-reply-to-a-message`, `slack_v2-send-block-kit-message`, or `slack_v2-send-message-to-user-or-group`, but this task must not send unless a later approved runtime path executes the tool.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Handoff Source.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Deliverable

- Produce a concise, reviewable task response that a human can act on.
- Also include a short human-readable summary covering: Slack Handoff Draft. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for the target, message purpose, source artifact, timing, and approver before drafting.

## Guardrails

Draft only. Do not post, reply, create channels, archive channels, delete messages, update profiles, or administer Slack.

## Completion Criteria

- Draft includes target, body, source context, timing, and approver.
- Output states no Slack message was sent.

## Human Review

- Approve exact message content and target before send.
