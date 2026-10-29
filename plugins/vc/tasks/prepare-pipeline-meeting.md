---
id: vc.prepare_pipeline_meeting
title: Prepare Meeting
slug: prepare-pipeline-meeting
agent: vc-deal-analyst
skills:
- meeting-prep-and-summary
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/prepare-pipeline-meeting.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Prepare Meeting

## Objective

Prepare Meeting for one Pipeline Deal using its confirmed Organisation and supplied evidence.

## What To Do

Apply `meeting-prep-and-summary` to prepare this specific meeting: company context, source-backed claims to validate, targeted questions, agenda and desired outcomes. Use the supplied meeting goal, attendees, date and notes plus relevant readable project-linked and task-chat sources. A pitch deck is optional; prior notes or other supplied evidence are sufficient. The company is the Deal's confirmed Organisation. company name carries its Platform-supplied name and optional organisation_id is for tool calls only. Do not take company identity from the Deal title or legacy company fields, ask the human to re-enter it, or change People or Organisations. Respect the requested evidence scope; connected providers and external research are optional and must stay within that scope. Missing calendar, CRM or research connections do not block work from supplied evidence. Apply the output template and guidance in `definitionJson.documentRefs`, adapting headings to the actual meeting type. Cite material claims and distinguish source statements, inference and unknowns. Create a separate standalone safe static HTML Meeting Brief for this meeting with `artifact.createTextArtifact`, a `.html` filename and `mimeType: "text/html"`. The task run supplies the current Deal scope. Preserve earlier meetings' files and the four living reports; do not use `project.instantiateTemplate` or the living-report refresh lifecycle for this task. Save the returned artifact ID with the task output meeting brief artifact. This is a per-meeting task output, not a singleton Deal field. Recording a discussion in this output does not authorize a canonical investment decision or stage move. Keep the Deal fields current with the Platform Record Field Maintenance skill: read them with `field-values.getFields`, use `field-values.setField` to fill editable empty Deal fields that the evidence in this task clearly supports, and suggest rather than make any change to a populated field. Leave the Fund, lifecycle stage and decision fields, and all People and Organisation records, to the human and the Deal Manager. In the completion summary, name each field you filled or suggest changing by its label. For a suggested change, give the current value and the value the evidence supports, and ask whether to update it; a yes from the human is an explicit request to write it. Do not treat a meeting date as a metric's as-of date unless the source explicitly establishes that relationship.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Company Name, Confirmed Organisation ID, Meeting Source Files, Meeting Notes, Meeting Type, Meeting Date and Time, Meeting Goal, Attendees, Pitch Deck.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Initial Call Brief Template](../alludium/documents/deal-room/initial-call-brief-template.html): Use as the starting structure for the deliverable; adapt it to the facts and avoid generic filler.
- [Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.html): Follow for citations, claim language, assumptions, and evidence quality.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.html): Follow for process boundaries and review standards.

## Deliverable

- Create or update **Meeting Brief** as a standalone safe HTML artifact. Use `.html`, `mimeType: "text/html"`, and complete static HTML suitable for the platform safe previewer.

## Missing Input Policy

Use the confirmed Organisation and available sources; ask only for an unclear meeting goal/type or absent readable evidence. A pitch deck is never required. Mark unavailable optional details as unknown.

## Guardrails

Draft only. Do not send messages, write external CRM records, change calendars or Drive, create tasks/projects, move stage, or record an investment decision.

## Completion Criteria

- The Meeting Brief is a saved HTML task output with cited evidence and clear gaps.
- Earlier meeting files and living reports are preserved; no investment decision or identity record is changed.
- Eligible empty Deal fields are filled from explicit evidence and populated differences are presented for human review.

## Human Review

- Review the output and any proposed field replacement; final task completion remains human-confirmed.
