---
id: vc.track_term_sheet_negotiation
title: Track Term Sheet Negotiation
slug: track-term-sheet-negotiation
agent: vc-legal-compliance-desk
skills:
- term-sheet-negotiation-brief
- deal-terms-analysis
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/track-term-sheet-negotiation.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Track Term Sheet Negotiation

## Objective

Organize open term-sheet issues, give/get options, counsel questions, and approval points without negotiating or approving legal language.

## What To Do

Prepare an internal negotiation brief from the current term sheet, open terms, IC constraints, founder comments or redlines, counsel notes, cap table context, and deal terms analysis. Separate business tradeoffs from counsel review, identify give/get options, and list approval points. Cite material claims, separate assumptions from evidence, and do not provide legal advice, negotiate terms, send terms, approve legal language, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Create or update a polished Word-ready document named Term Sheet Negotiation Brief as a standalone safe static HTML artifact using the Artifact Create Text Artifact tool (`artifact.createTextArtifact`), a `.html` filename, and `mimeType: "text/html"`; do not use the Project Instantiate Template tool, `project.instantiateTemplate`, or `project_instantiateTemplate`, and do not create a `.md`/`text/markdown` artifact for this rendered output; then attach it to the required output field negotiation brief artifact. Use `definitionJson.documentRefs` only as source guidance for rendered outputs. Read referenced templates, methodologies, checklists, style guides, operating guidance, and policies, but convert the referenced Markdown/template sections into semantic standalone HTML for `artifact.createTextArtifact`: keep the required first summary section from the task or template, preserve decision-critical section order, omit unsupported boilerplate, and resolve conflicts in favor of the shared HTML contract plus task-specific heading requirements. For refs with `outputFieldKey`, save the `artifact.createTextArtifact` result to that output field and preserve the document ID alongside the output artifact.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Term Sheet Artifact, Current Open Terms, IC Constraints, Founder Comments Or Redline, Counsel Notes, Cap Table, Deal Terms Analysis.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Term Sheet Negotiation Brief Template](../alludium/documents/deal-room/term-sheet-negotiation-brief-template.html): Use as the starting structure for the deliverable; adapt it to the facts and avoid generic filler.
- [Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.md): Follow for citations, claim language, assumptions, and evidence quality.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.md): Follow for process boundaries and review standards.

## Deliverable

- Create or update **Negotiation Brief** as a standalone safe HTML artifact. Use `.html`, `mimeType: "text/html"`, and complete static HTML suitable for the platform safe previewer.

## Missing Input Policy

Ask for the current term sheet, open terms, and IC constraints before producing a negotiation brief.

## Guardrails

Draft only unless a human explicitly approves the send, CRM write, Drive change, project creation, child task creation, or stage transition.

## Completion Criteria

- Required input gaps are resolved or listed as assumptions/open questions.
- Open terms distinguish business tradeoffs from counsel questions.
- Approval points identify owner, dependency, and required human approval point.

## Human Review

- Approve all negotiation positions, founder-facing messages, legal language, and stage movement.
- Approve external communications, CRM writes, Drive/project creation, legal/counsel actions, and founder-facing requests.
