---
id: vc.prepare_initial_linkedin_reachout
title: Prepare Initial LinkedIn Reachout
slug: prepare-initial-linkedin-reachout
agent: vc-sourcing-operator
skills:
- vc-outreach-draft-queue
- founder-outreach-and-intro-paths
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/prepare-initial-linkedin-reachout.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Prepare Initial LinkedIn Reachout

## Objective

Draft the first LinkedIn message after a candidate has been approved for outbound engagement.

## What To Do

Draft the first LinkedIn reachout for approved of-interest candidates or connected founders. Use concrete candidate evidence, founder context, and the approved thesis angle. Keep the message short, specific, and question-led. Do not mark the reachout as sent, update CRM stages, or contact the founder without explicit human approval.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Initial Reachout Scope.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Outreach Queue Template](../alludium/documents/origination/outreach-queue-template.md): Use as the starting structure for the deliverable; adapt it to the facts and avoid generic filler.
- [Origination Source Strategy Guide](../alludium/documents/origination/origination-source-strategy-guide.md): Use as the analysis method.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.md): Follow for process boundaries and review standards.

## Deliverable

- Create or update **Initial LinkedIn Reachout Artifact** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.
- Also include a short human-readable summary covering: Initial Reachout Draft Count, Initial Reachout Summary. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for the approved candidate, founder LinkedIn URL, connection state, thesis angle, source evidence, and outreach tone policy before drafting.

## Guardrails

Draft only. Sending LinkedIn messages, updating CRM stages, and changing outbound status require explicit human approval.

## Completion Criteria

- Draft includes founder, company, profile URL, message text, evidence hook, owner, and skip reason where applicable.
- Message is concise, specific, and anchored to cited candidate evidence.
- Send and CRM mutation boundaries are explicit.
