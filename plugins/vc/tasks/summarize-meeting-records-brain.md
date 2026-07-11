---
id: vc.summarize_meeting_records_brain
title: Summarize Meeting Records (Bare Brain PoC)
slug: summarize-meeting-records-brain
agent: orchestrator-minimal
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/summarize-meeting-records-brain.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Summarize Meeting Records (Bare Brain PoC)

## Objective

Orchestrate evidence extraction and summary persistence without exposing meeting bodies to the brain.

## What To Do

Delegate evidence_extraction with meeting artifact IDs only. Evaluate its bounded claim counts, contradiction counts, warnings, and summary; never read a meeting record or extraction artifact. Decide sufficient, contradictory, or insufficient. Delegate meeting_synthesis with extraction artifact IDs and that decision. The synthesis worker must persist the Meeting Records Summary and return its artifact ID. Finish with the decision, counts, warnings, and ID. Use definitionJson.documentRefs as the durable document contract: apply the output_template as the output skeleton and the operating_guidance as process constraints, then preserve the output template's document ID with the artifact.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Meeting Record Artifact IDs, Meeting Notes, Company Name.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Customer Insights Summary Template](../alludium/documents/deal-room/customer-insights-summary-template.html): Use as the starting structure for the deliverable; adapt it to the facts and avoid generic filler.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.md): Follow for process boundaries and review standards.

## Deliverable

- Create or update **Meeting Records Summary** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.

## Missing Input Policy

Require meeting record artifacts and company name. Do not place meeting bodies in brain context.

## Guardrails

Draft only. Messages, CRM writes, project creation, child-task mutation, and stage movement are forbidden.

## Completion Criteria

- The brain called only orchestrate.delegate and orchestrate.finish.
- Every brain-bound payload was at most 1,500 tokens.
- Claims retain meeting and evidence references, with assumptions separated from evidence.
- Contradictory claims are presented side by side and surfaced for human review.
- The synthesis worker persisted the final artifact and returned its ID.

## Human Review

- Review contradictions, evidence gaps, external follow-up drafts, and any stage recommendation.
