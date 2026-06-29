---
id: vc.review_term_sheet
title: Review Term Sheet
slug: review-term-sheet
agent: vc-legal-compliance-desk
skills:
- red-flags-scanner
- citation-enforcement
- closing-coordination-and-cp-tracking
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/review-term-sheet.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Review Term Sheet

## Objective

Review Term Sheet for one venture-capital opportunity with evidence capture, human review gates, and next-action recommendations.

## What To Do

Review the term sheet for business deviations, red flags, and counsel review questions without providing legal advice. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Create or update a polished Word-ready document named Term Sheet Review as a standalone safe static HTML artifact using the Artifact Create Text Artifact tool (`artifact.createTextArtifact`), a `.html` filename, and `mimeType: "text/html"`; do not use the Project Instantiate Template tool, `project.instantiateTemplate`, or `project_instantiateTemplate`, and do not create a `.md`/`text/markdown` artifact for this rendered output; then attach it to the required output field term sheet review artifact.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Term Sheet Artifact, Deal Terms, Standard Terms Reference, Counsel Notes, Deal Terms Analysis.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Term Sheet Review Template](../alludium/documents/deal-room/term-sheet-review-template.md): Use as the starting structure for the deliverable; adapt it to the facts and avoid generic filler.
- [Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.md): Follow for citations, claim language, assumptions, and evidence quality.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.md): Follow for process boundaries and review standards.

## Deliverable

- Create or update **Term Sheet Review** as a standalone safe HTML artifact. Use `.html`, `mimeType: "text/html"`, and complete static HTML suitable for the platform safe previewer.

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
