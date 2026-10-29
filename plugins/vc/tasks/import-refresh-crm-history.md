---
id: vc.import_refresh_crm_history
title: Import or Refresh CRM History
slug: import-refresh-crm-history
agent: vc-deal-analyst
skills:
- import-crm-history
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/import-refresh-crm-history.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Import or Refresh CRM History

## Objective

Import or refresh one Deal's CRM history into a single sourced company brief with the full source notes attached.

## What To Do

Activate and apply the `import-crm-history` skill. It owns the method: identifying the company's CRM records, reading every page of notes, preserving each retrieved note's full text, writing the company and relationship brief, checking the document size, and creating or refreshing the one CRM history document. Use the CRM-history template named in `definitionJson.documentRefs` as the document structure, and the citation style guide for references. The company is the Deal's confirmed Organisation. company name carries that Organisation's name as the Platform supplied it, and organisation id, when present, identifies it for tool calls only. Do not take the company name from the Deal title. crm provider names the CRM to read; crm record reference, when present, is a known record ID or link to check first, never a reason to skip checking the other plausible records. When existing crm history artifact is empty, this is a first import: create the document from the template with `project.instantiateTemplate`, exactly once and with no other tool. When it is present, this is a refresh: read that exact document and replace its whole content in one update, keeping the same artifact ID. If that document cannot be read or updated, stop and say why. Never create a second CRM history document for this Deal. This task only imports and preserves CRM context. Do not apply the living-report method, review other project evidence, screen the company, assess Fund fit, make an investment recommendation, or start any report. Do not write to the CRM, change Deal fields, stage, decisions or identity records, or create tasks. After the document is saved and ready, save the task output with `task-management.saveTaskOutput`, setting crm history artifact to that document's artifact ID, then finish by calling `task-management.completeTask` without a task ID. The task completes when this response finishes; if it is refused, report why. If the import is blocked, report the specific blocker, tell the Deal Manager with one attention required message as the skill describes, and do not complete the task. The final response is investor-facing: one or two sentences on what the history shows, whether the import is complete or partial and why, at most three material gaps, and "Open the CRM history and context file" when a document was saved. When nothing was saved, name the blocker instead and do not point to a file. Do not name runtime field keys, tools, or internal processing in the response.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Company Name, Confirmed Organisation ID, CRM Provider, Known CRM Record, Existing CRM History.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Deal Pipeline CRM History and Context Template](../alludium/documents/deal-pipeline/crm-history-template.html): Use as the starting structure for the deliverable; adapt it to the facts and avoid generic filler.
- [Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.html): Follow for citations, claim language, assumptions, and evidence quality.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.html): Follow for process boundaries and review standards.

## Deliverable

- Create or update **CRM history and context** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.

## Missing Input Policy

Company identity comes from the Deal's confirmed Organisation. When no CRM provider is named, use the one connected CRM; if none or several are connected, ask which to use. Do not ask for a CRM record ID or link.

## Guardrails

Read the CRM only. Do not create, edit or annotate CRM records, send messages, create tasks or projects, change Deal fields or stage, or record an investment decision.

## Completion Criteria

- The document contains a useful, cited company and relationship brief, not only an inventory of records and notes.
- Every retrieved note appears in the source appendix with its full text, source metadata and a working reference from the brief.
- Dated notes stay dated; past plans, pilots and rounds are not presented as current facts, and linked documents are not described as read.
- Import coverage states which records and pages were read and marks any gap as a partial import.
- A refresh updated the existing document in place and returned the same artifact ID; a first import created exactly one document from the CRM-history template.
- No CRM write, Deal field change other than the document pointer, stage move or investment judgment occurred.

## Human Review

- Decide whether to refresh an existing investment report now; the reports read the CRM history as evidence whenever they next run.
