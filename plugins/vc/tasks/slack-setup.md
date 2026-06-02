---
id: vc.slack_setup
title: Set Up Slack for Deal Pipelines
slug: slack-setup
agent: vc-integration-operator
skills:
- vc-slack-discovery
- vc-slack-sync-read
- vc-slack-sync-write
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-integrations/slack-setup.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Set Up Slack for Deal Pipelines

## Objective

Coordinate Slack connection readiness, channel discovery, read-preview policy, and optional notification proposal scope for Deal Pipeline setup.

## What To Do

Confirm that Slack is a selected collaboration source, check connection readiness, then coordinate workspace/channel discovery and reviewed read-preview setup. Create child tasks from the declared integrationSetup flow only when the user chooses that step. Keep message reads, posting, channel creation, recurring sync, and notification drafts disabled unless a later human approval explicitly creates that task.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Setup Goal.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Deliverable

- Produce a concise, reviewable task response that a human can act on.
- Also include a short human-readable summary covering: Setup Summary, Accepted Connection Scope, Child Task Plan, Sync Policy. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

If Slack is not authorized or no channel/thread scope is selected, keep setup incomplete and ask for connection authorization, a supplied channel list, or the source-scope decision needed for discovery.

## Guardrails

Setup orchestration only. Do not read broad channel history, post messages, create channels, enable recurring sync, or create Deal Pipeline projects from this setup task.

## Completion Criteria

- Connection readiness or missing-authorization evidence is recorded.
- Candidate channel/thread scope is complete or the unanswered scope questions are explicit.
- Read-preview and optional notification-proposal policies are recorded without enabling external writes.
- The accepted connection scope states whether access is personal, project-shared, or workspace-shared.

## Human Review

- Choose whether the Slack connection is personal, project-shared, or workspace-shared.
- Choose the workspace, channel, and thread scope.
- Approve any read-preview, notification, recurring sync, or post task separately.
