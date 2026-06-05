---
id: vc.prepare_second_reachout_email
title: Prepare Second Reachout Email
slug: prepare-second-reachout-email
agent: vc-sourcing-operator
skills:
- vc-outreach-draft-queue
- founder-outreach-and-intro-paths
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/prepare-second-reachout-email.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Prepare Second Reachout Email

## Objective

Draft a second-touch email for candidates with LinkedIn outreach sent and no response after the configured wait period.

## What To Do

Draft a second-touch email only for candidates with a recorded LinkedIn reachout, no reply, and an approved wait period. Use one concrete hook and a simple call request. Treat the email as a draft artifact only; do not send email, set outreach status, or mutate external CRM/list stages without explicit human approval.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Second Reachout Scope.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Outreach Queue Template](../alludium/documents/origination/outreach-queue-template.md): Use as the starting structure for the deliverable; adapt it to the facts and avoid generic filler.
- [Origination Source Strategy Guide](../alludium/documents/origination/origination-source-strategy-guide.md): Use as the analysis method.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.md): Follow for process boundaries and review standards.

## Deliverable

- Create or update **Second Reachout Email Artifact** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.
- Also include a short human-readable summary covering: Second Reachout Draft Count. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for the prior LinkedIn reachout record, no-response date/window, founder email or email-finding policy, candidate evidence, and approved sender before drafting.

## Guardrails

Draft only. Sending email, updating Outreach Status, and moving CRM stages require explicit human approval.

## Completion Criteria

- Email draft includes subject, body, evidence hook, recipient, prior-reachout reference, and no-response timing.
- Draft explains whether the candidate should remain active, move to no-response, watchlist, pass, or engaged outcome review.
- No external send or status mutation occurs without explicit approval.
