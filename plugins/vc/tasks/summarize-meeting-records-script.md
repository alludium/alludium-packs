---
id: vc.summarize_meeting_records_script
title: Summarize Meeting Records (Deterministic PoC)
slug: summarize-meeting-records-script
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/summarize-meeting-records-script.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Summarize Meeting Records (Deterministic PoC)

## Objective

Execute the same meeting extraction and synthesis stages without an orchestrator model.

## What To Do

Execute fixed logic with no orchestrator LLM: run evidence_extraction over the supplied meeting artifact IDs, then run meeting_synthesis with its artifact references and persist the result. Use the identical worker roles, budgets, inputs, and output contracts as the bare-brain arm. Propagate extraction warnings and contradiction counts without adding an adaptive decision. Use definitionJson.documentRefs as the durable document contract: apply the output_template as the output skeleton and the operating_guidance as process constraints, then preserve the output template's document ID with the artifact.

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

Require meeting record artifacts and company name.

## Guardrails

Draft only. Messages, CRM writes, project creation, child-task mutation, and stage movement are forbidden.

## Completion Criteria

- No orchestrator model request occurred.
- Claims retain meeting and evidence references, with assumptions separated from evidence.
- Extraction warnings and contradictory claims are preserved in the persisted summary.

## Human Review

- Review contradictions, evidence gaps, external follow-up drafts, and any stage recommendation.
