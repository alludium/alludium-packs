---
id: vc.slack_sync_read
title: Preview Slack Deal Context
slug: slack-sync-read
agent: vc-integration-operator
skills:
- vc-slack-sync-read
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-integrations/slack-sync-read.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Preview Slack Deal Context

## Objective

Preview selected Slack channel, thread, message, and file context for Deal Pipeline tasks.

## What To Do

Use `slack_v2-find-message`, `slack_v2-list-replies`, `slack_v2-list-files`, and `slack_v2-get-file` only inside the approved channel/thread scope. Summarize selected context and propose whether it belongs as knowledge context, artifact context, task context, or setup context.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Selected Slack Scope.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Deliverable

- Produce a concise, reviewable task response that a human can act on.
- Also include a short human-readable summary covering: Slack Context Preview, Target Context Mapping. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for approved channel/thread scope before reading Slack messages.

## Guardrails

Read preview only. Do not ingest broad history, post, reply, delete, or update messages.

## Completion Criteria

- Message/thread IDs and channel IDs are listed.
- Relevant context is summarized with timestamps and sensitivity caveats.
- Broad channel ingestion remains out of scope.

## Human Review

- Approve selected context before attaching it to project/task state.
