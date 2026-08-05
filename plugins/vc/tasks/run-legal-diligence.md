---
id: vc.run_legal_diligence
title: Run Legal Diligence
slug: run-legal-diligence
agent: vc-legal-compliance-desk
skills:
- legal-diligence-coordination
- red-flags-scanner
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/run-legal-diligence.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Run Legal Diligence

## Objective

Coordinate legal diligence document indexing, issue tracking, counsel questions, and showstopper-risk review support without providing legal advice.

## What To Do

Coordinate legal diligence by indexing legal source artifacts, tracking issues, drafting counsel questions, and surfacing showstopper risks for human review. Separate factual document gaps from legal conclusions. Cite material claims, separate assumptions from evidence, and do not provide legal advice, clear legal risks, approve legal sufficiency, send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Create or update a polished Word-ready document named Legal Diligence Tracker.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Legal Source Artifact IDs, Company Name, Counsel Requirements, IP Artifact IDs, Corporate Structure Artifact, Employment Contract Artifact IDs, Litigation Search Artifact IDs.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Legal Diligence Tracker Template](../alludium/documents/deal-room/legal-diligence-tracker-template.html): Use as the starting structure for the deliverable; adapt it to the facts and avoid generic filler.
- [Legal Diligence Guide](../alludium/documents/deal-room/legal-diligence-guide.html): Use as the analysis method.
- [Formal Diligence Workstream Guide](../alludium/documents/deal-room/formal-diligence-workstream-guide.html): Use as the analysis method.
- [Formal Diligence Checklist](../alludium/documents/deal-room/formal-diligence-checklist.html): Complete as a checklist with status, evidence, owner, and open items.
- [Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.html): Follow for citations, claim language, assumptions, and evidence quality.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.html): Follow for process boundaries and review standards.

## Deliverable

- Create or update **Legal Diligence Tracker** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.

## Missing Input Policy

Ask for legal source artifacts and company name before producing a legal diligence tracker.

## Guardrails

Draft only unless a human explicitly approves the send, CRM write, Drive change, project creation, child task creation, or stage transition.

## Completion Criteria

- Required input gaps are resolved or listed as assumptions/open questions.
- Issue register separates factual gaps from counsel/human legal judgments.
- Counsel questions identify owner, dependency, and required human approval point.

## Human Review

- Approve legal conclusions, counsel communications, founder requests, showstopper classification, and stage movement.
- Approve external communications, CRM writes, Drive/project creation, legal/counsel actions, and founder-facing requests.
