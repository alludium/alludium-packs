---
id: vc.record_linkedin_connection_attempt
title: Record LinkedIn Connection Attempt
slug: record-linkedin-connection-attempt
agent: vc-sourcing-operator
skills:
- vc-outreach-draft-queue
- founder-outreach-and-intro-paths
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/record-linkedin-connection-attempt.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Record LinkedIn Connection Attempt

## Objective

Capture a human-approved LinkedIn connection attempt and update the outbound state without sending messages automatically.

## What To Do

Record only a connection attempt that a human has already approved or sent. Capture the founder profile, sent note, sent-at date, source candidate, destination CRM/list state, and any manual owner notes. Mirror the reference outbound pattern: the task may prepare an update plan for the outreach state, but it must not send a LinkedIn request, mutate CRM records, or mark outreach as sent without explicit human approval.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Connection Attempt.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Outreach Queue Template](../alludium/documents/origination/outreach-queue-template.md): Use as the starting structure for the deliverable; adapt it to the facts and avoid generic filler.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.md): Follow for process boundaries and review standards.

## Deliverable

- Create or update **Connection Record Artifact** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.
- Also include a short human-readable summary covering: Outbound Status, Connection Record Summary. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for the approved outreach target, LinkedIn profile URL, connection note, sent/approval status, owner, and destination system before recording.

## Guardrails

Record and propose state updates only. Sending LinkedIn requests, setting CRM stages, or changing external status requires explicit human approval.

## Completion Criteria

- Connection attempt record includes target, founder profile URL, note, date, owner, and source candidate reference.
- Recommended next state distinguishes pending connection from ready-for-initial-LinkedIn-reachout.
- External writes and message sending remain explicitly human-controlled.
