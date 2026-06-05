---
id: vc.prepare_deal_flow_agenda
title: Prepare Deal Flow Agenda
slug: prepare-deal-flow-agenda
agent: vc-pipeline-autopilot
skills:
- citation-enforcement
- vc-task-and-next-step-generation
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/prepare-deal-flow-agenda.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Prepare Deal Flow Agenda

## Objective

Prepare Deal Flow Agenda for one venture-capital opportunity with evidence capture, human review gates, and next-action recommendations.

## What To Do

Prepare the deal-flow agenda from the pipeline snapshot; identify stale deals, new deals, stage-change candidates, and the seven-day action plan. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Use workspace-configured scoring frameworks, CRM providers, stage names, and deal-type metric packs; do not assume a specific fund, CRM, or SaaS default unless the workspace configuration explicitly selects it.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Pipeline Snapshot, Meeting Date, Stale Deal Threshold.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Deliverable

- Produce a concise, reviewable task response that a human can act on.
- Also include a short human-readable summary covering: Agenda, Stale Deal List, New Deal List, Stage Change Candidates, Seven Day Action Plan. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for missing required inputs before producing investment-stage recommendations.

## Guardrails

Draft only unless a human explicitly approves the send, CRM write, Drive change, project creation, child task creation, or stage transition.

## Completion Criteria

- Required input gaps are resolved or listed as assumptions/open questions.
- Material conclusions include source links or are labeled as human judgment calls.
- Next actions identify owner, dependency, and required human approval point.

## Human Review

- Approve investment-stage movement, pass/follow-up recommendations, and final task completion.
- Approve external communications, CRM writes, Drive/project creation, legal/counsel actions, and founder-facing requests.

## Workspace Methodology

- Use the workspace-configured Pipeline Health And Crm Hygiene methodology when applicable: Use only when the workspace CRM/stage model matches the skill assumptions.
