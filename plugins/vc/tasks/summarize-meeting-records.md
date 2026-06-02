---
id: vc.summarize_meeting_records
title: Summarize Meeting Records
slug: summarize-meeting-records
agent: vc-meeting-operator
skills:
- meeting-prep-and-summary
- citation-enforcement
- vc-task-and-next-step-generation
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/summarize-meeting-records.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Summarize Meeting Records

## Objective

Summarize or ingest meeting records for one venture-capital opportunity with evidence capture, human review gates, and next-action recommendations.

## What To Do

Summarize or ingest the available meeting records for this opportunity, including founder, management, advisor, customer, expert, partner, IC, legal, or closing meetings represented by transcript artifacts, meeting-summary artifacts, recording exports, notes, or meeting-source links. Extract claims and gaps, capture action items, draft a CRM-neutral update, identify open questions, and recommend next actions or stage considerations without moving the deal. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Use workspace-configured scoring frameworks, CRM providers, stage names, and deal-type metric packs; do not assume a specific fund, CRM, or SaaS default unless the workspace configuration explicitly selects it. Create or update a polished Word-ready document named Meeting Records Summary.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Meeting Record Artifact IDs, Meeting Notes, Company Name, Deal Pipeline Url.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Customer Insights Summary Template](../alludium/documents/deal-room/customer-insights-summary-template.md): Use as the starting structure for the deliverable; adapt it to the facts and avoid generic filler.
- [Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.md): Follow for citations, claim language, assumptions, and evidence quality.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.md): Follow for process boundaries and review standards.

## Deliverable

- Create or update **Meeting Records Summary** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.
- Also include a short human-readable summary covering: Transcript Summary, Claims Register, Contradictions Or Gaps, Action Items, CRM Update Draft, Stage Recommendation, Summary, Recommendation, and other task-specific status fields. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Require meeting record artifacts and company name before producing the meeting summary. Use meeting notes as optional supporting context when provided.

## Guardrails

Draft only unless a human explicitly approves the send, CRM write, Drive change, project creation, child task creation, or stage transition.

## Completion Criteria

- Required input gaps are resolved or listed as assumptions/open questions.
- Material conclusions include source links or are labeled as human judgment calls.
- Next actions identify owner, dependency, and required human approval point.

## Human Review

- Approve investment-stage movement, pass/follow-up recommendations, and final task completion.
- Approve external communications, CRM writes, Drive/project creation, legal/counsel actions, and founder-facing requests.

## Workspace Methodology

- Use the workspace-configured Investment Screening Framework methodology when applicable: Use only when the workspace explicitly configures this screening framework.
