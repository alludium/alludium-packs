---
id: vc.verify_conditions_precedent
title: Verify Conditions Precedent
slug: verify-conditions-precedent
agent: vc-legal-compliance-desk
skills:
- citation-enforcement
- closing-coordination-and-cp-tracking
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/verify-conditions-precedent.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Verify Conditions Precedent

## Objective

Verify Conditions Precedent for one venture-capital opportunity with evidence capture, human review gates, and next-action recommendations.

## What To Do

Map conditions precedent to available closing evidence, identify missing items and blocker severity, and prepare counsel review recommendation and signing readiness. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Use the required input file artifact closing checklist artifact as the closing checklist subject, and use closing source artifacts for legal documents, counsel notes, CP lists, signed documents, and evidence files. Create or update a polished Word-ready document named Conditions Precedent Verification.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Closing Checklist, Closing Source Artifact IDs, Counsel Requirements, Closing Status.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Conditions Precedent Tracker Template](../alludium/documents/deal-room/conditions-precedent-tracker-template.md): Use as the starting structure for the deliverable; adapt it to the facts and avoid generic filler.
- [Legal Diligence Guide](../alludium/documents/deal-room/legal-diligence-guide.md): Use as the analysis method.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.md): Follow for process boundaries and review standards.

## Deliverable

- Create or update **Conditions Precedent Verification** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.
- Also include a short human-readable summary covering: Cp Evidence Mapping, Missing Items, Blocker Severity, Counsel Review Recommendation, Signing Readiness, Summary, Recommendation, Source Links, and other task-specific status fields. Do not output raw JSON unless the user explicitly asks for machine-readable data.

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
