---
id: vc.prepare_ic_agenda
title: Prepare IC Agenda
slug: prepare-ic-agenda
agent: vc-ic-prep-producer
skills:
- meeting-prep-and-summary
- citation-enforcement
- ic-risk-checklist-and-decision-log
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/prepare-ic-agenda.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Prepare IC Agenda

## Objective

Prepare IC Agenda for one venture-capital opportunity with evidence capture, human review gates, and next-action recommendations.

## What To Do

Prepare the IC agenda, pack checklist, key debate topics, follow-up questions, and pre-read requirements. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Use the required input file artifact investment memo artifact as the source memo when preparing the IC agenda. Create or update a polished Word-ready document named IC Agenda as a standalone safe static HTML artifact using the Artifact Create Text Artifact tool (`artifact.createTextArtifact`), a `.html` filename, and `mimeType: "text/html"`; do not use `project.instantiateTemplate` or create a `.md`/`text/markdown` artifact for this rendered output; then attach it to the required output field ic agenda artifact.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Investment Memo.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [IC Agenda Template](../alludium/documents/deal-room/ic-agenda-template.md): Use as the starting structure for the deliverable; adapt it to the facts and avoid generic filler.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.md): Follow for process boundaries and review standards.

## Deliverable

- Create or update **IC Agenda** as a standalone safe HTML artifact. Use `.html`, `mimeType: "text/html"`, and complete static HTML suitable for the platform safe previewer.

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
