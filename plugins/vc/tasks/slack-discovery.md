---
id: vc.slack_discovery
title: Explore Slack Channels for VC Context
slug: slack-discovery
agent: vc-integration-operator
skills:
- vc-slack-discovery
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-integrations/slack-discovery.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Explore Slack Channels for VC Context

## Objective

Discover Slack workspace and channel scope before selected VC context reads or handoff notifications.

## What To Do

Use the connected slack v2 application to confirm workspace context with `slack_v2-get-current-user` and enumerate channels with `slack_v2-list-channels`. Classify channel purpose as deal intake, deal-specific discussion, IC prep, portfolio handoff, operations, broad/general, sensitive/excluded, or unknown.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Discovery Goal.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Deliverable

- Produce a concise, reviewable task response that a human can act on.
- Also include a short human-readable summary covering: Slack Discovery Report, Channel Scope Questions. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

If Slack is not authorized, ask for authorization or a supplied channel list.

## Guardrails

Discovery only. Do not read messages, post, reply, create channels, or change channel settings.

## Completion Criteria

- Candidate channels are classified with confidence.
- User choices needed before message/thread reads are explicit.

## Human Review

- Approve included channels or threads before sync read.
- Approve any notification targets separately.
