---
id: vc.prepare_meeting
title: Prepare Meeting
slug: prepare-meeting
agent: vc-meeting-operator
skills:
- meeting-prep-and-summary
- company-research-and-enrichment
- citation-enforcement
- pitch-deck-explainer
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/prepare-meeting.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Prepare Meeting

## Objective

Prepare a founder, management, advisor, customer, expert, partner, IC, legal, or closing meeting for one venture-capital opportunity with evidence capture, human review gates, and next-action recommendations.

## What To Do

Prepare the meeting brief, relationship context, concise company and evidence summary, stage-relevant agenda, risk prompts, and questions by topic for the requested meeting type. Use the pitch deck, prior task artifacts, meeting goal, calendar context, CRM context, or other supplied source material when available, but do not require a pitch deck when another evidence source is sufficient. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Use workspace-configured scoring frameworks, CRM providers, stage names, and deal-type metric packs; do not assume a specific fund, CRM, or SaaS default unless the workspace configuration explicitly selects it. Create or update a polished Word-ready document named Meeting Brief.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Company Name, Pitch Deck Artifact, Founder Names, Meeting Datetime, Deal Pipeline Url.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Initial Call Brief Template](../alludium/documents/deal-room/initial-call-brief-template.md): Use as the starting structure for the deliverable; adapt it to the facts and avoid generic filler.
- [Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.md): Follow for citations, claim language, assumptions, and evidence quality.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.md): Follow for process boundaries and review standards.

## Deliverable

- Create or update **Meeting Brief** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.
- Also include a short human-readable summary covering: Meeting Brief, Founder Company Summary, Competitor Funding Activity, Stage-Relevant Scorecard Notes, Questions By Topic, Summary, Recommendation, Source Links, and other task-specific status fields. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for the meeting type, meeting goal, and missing source material before producing the meeting brief when they are not clear from project context.

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
