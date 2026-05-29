---
id: vc.review_investment_documents
title: Review Investment Documents
slug: review-investment-documents
agent: vc-legal-compliance-desk
skills:
- legal-diligence-coordination
- closing-coordination-and-cp-tracking
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/review-investment-documents.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Review Investment Documents

## Objective

Coordinate post-term-sheet investment document review, disclosure-letter issues, counsel questions, and closing readiness notes without providing legal advice.

## What To Do

Coordinate investment document review by mapping document provisions back to the term sheet review, disclosure letter, counsel notes, board minutes, and cap table context. Identify open document issues, counsel questions, and closing readiness notes without interpreting legal sufficiency. Cite material claims, separate assumptions from evidence, and do not provide legal advice, sign off documents, send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Create or update a polished Word-ready document named Investment Document Review.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Investment Document Artifact IDs, Term Sheet Review, Negotiation Brief, Legal Diligence, Disclosure Letter, Counsel Notes, Cap Table, Board Minutes.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Investment Document Review Template](../alludium/documents/deal-room/investment-document-review-template.md): Use as the starting structure for the deliverable; adapt it to the facts and avoid generic filler.
- [Legal Diligence Guide](../alludium/documents/deal-room/legal-diligence-guide.md): Use as the analysis method.
- [Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.md): Follow for citations, claim language, assumptions, and evidence quality.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.md): Follow for process boundaries and review standards.

## Deliverable

- Create or update **Investment Document Review** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.
- Also include a short human-readable summary covering: Term To Document Mapping, Open Document Issues, Counsel Questions, Closing Readiness Notes, Summary, Recommendation, Source Links, Assumptions, and other task-specific status fields. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for investment document artifacts and term sheet review before producing document-readiness notes.

## Guardrails

Draft only unless a human explicitly approves the send, CRM write, Drive change, project creation, child task creation, or stage transition.

## Completion Criteria

- Required input gaps are resolved or listed as assumptions/open questions.
- Term-to-document mapping distinguishes business mismatches from counsel questions.
- Closing readiness notes identify owner, dependency, and required human approval point.

## Human Review

- Approve legal conclusions, document sufficiency, signing readiness, counsel/founder communications, and stage movement.
- Approve external communications, CRM writes, Drive/project creation, legal/counsel actions, and founder-facing requests.
