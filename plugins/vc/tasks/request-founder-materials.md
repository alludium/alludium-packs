---
id: vc.request_founder_materials
title: Request Founder Materials
slug: request-founder-materials
agent: vc-dealflow-concierge
skills:
- citation-enforcement
- founder-materials-request
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/request-founder-materials.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Request Founder Materials

## Objective

Request Founder Materials for one venture-capital opportunity with evidence capture, human review gates, and next-action recommendations.

## What To Do

Prepare the missing-materials checklist, founder-friendly request draft, share instructions, and due-date recommendation for human approval before sending. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Create or update a polished Word-ready document named Founder Materials Request as a standalone safe static HTML artifact using `artifact_createTextArtifact`, a `.html` filename, and `mimeType: "text/html"`; then attach it to the required output field founder materials request artifact.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Company Name, Missing Materials, Founder Contact, Due Date.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Founder Materials Request Template](../alludium/documents/deal-room/founder-materials-request-template.md): Use as the starting structure for the deliverable; adapt it to the facts and avoid generic filler.
- [File Naming And Source Index SOP](../alludium/documents/shared/file-naming-source-index-sop.md): Follow for process boundaries and review standards.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.md): Follow for process boundaries and review standards.

## Deliverable

- Create or update **Founder Materials Request** as a standalone safe HTML artifact. Use `.html`, `mimeType: "text/html"`, and complete static HTML suitable for the platform safe previewer.

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
