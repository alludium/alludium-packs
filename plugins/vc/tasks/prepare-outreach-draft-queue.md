---
id: vc.prepare_outreach_draft_queue
title: Prepare Outreach Draft Queue
slug: prepare-outreach-draft-queue
agent: vc-sourcing-operator
skills:
- vc-outreach-draft-queue
- citation-enforcement
- founder-outreach-and-intro-paths
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/prepare-outreach-draft-queue.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Prepare Outreach Draft Queue

## Objective

Draft founder outreach notes for active candidates while leaving send decisions to humans.

## What To Do

Mirror the reference pipeline's outreach draft policy. Draft only for candidates with active actions such as Meet, IC-Summary, or Reach out, no manual Status/contact progress, and a founder LinkedIn URL. Produce short, specific, question-led LinkedIn connection notes tied to evidence. Skip weak hooks instead of fabricating personalization.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Outreach Scope.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Outreach Queue Template](../alludium/documents/origination/outreach-queue-template.md): Use as the starting structure for the deliverable; adapt it to the facts and avoid generic filler.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.md): Follow for process boundaries and review standards.

## Deliverable

- Create or update **Outreach Queue Artifact** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.
- Also include a short human-readable summary covering: Outreach Draft Count, Outreach Report. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for active candidate batch, founder profile URL, eligible actions, manual-contact status, outreach tone policy, and destination for drafts.

## Guardrails

Draft only. Do not send messages, insert browser-extension notes, mark outreach as sent, or update external systems without explicit human approval.

## Completion Criteria

- Draft queue includes founder, profile URL, note, angle, strength, skip reason, and source evidence.
- Notes are short, question-led, specific, and free of unsupported praise or editorializing.
- Send remains a human action.
