---
id: vc.capture_opportunity_intake
title: Capture Opportunity Intake
slug: capture-opportunity-intake
agent: vc-dealflow-concierge
skills:
- deal-pipeline-setup-and-source-ingestion
- company-research-and-enrichment
- citation-enforcement
- pitch-deck-explainer
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/capture-opportunity-intake.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Capture Opportunity Intake

## Objective

Hydrate and assess a created Deal Pipeline from available source context before formal screening.

## What To Do

Hydrate the created Deal Pipeline from the best available source context: CRM/source record, company domain, pitch deck, intro note, source thread, founder material, origination promotion package, or other supplied evidence. Capture known project fields, source index, missing information, evidence quality, and recommended readiness for formal screening. Do not require a pitch deck when another source explains the opportunity. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Create or update a polished Word-ready document named Opportunity Intake Summary.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Company Name, Pitch Deck Artifact, Company Domain, Source System, Source Object URL, Source Thread URL, Source Thread Artifact, Source Material Artifacts, Founder Materials Artifacts, Referrer.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Deal Pipeline Operating SOP](../alludium/documents/deal-room/deal-room-sop.md): Follow for process boundaries and review standards.
- [Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.md): Follow for citations, claim language, assumptions, and evidence quality.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.md): Follow for process boundaries and review standards.

## Deliverable

- Create or update **Opportunity Intake Summary** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.
- Also include a short human-readable summary covering: Intake Recommendation, Intake Summary, Missing Information, Early Red Flags, Pass Feedback Draft, Next Actions, Summary, Recommendation, and other task-specific status fields. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for the minimum missing context needed to identify the company and cite at least one source. If company identity and one credible source are present, complete intake and list missing enrichment or screening inputs instead of blocking.

## Guardrails

Draft only unless a human explicitly approves the send, CRM write, Drive change, child task creation, or stage transition.

## Completion Criteria

- Required input gaps are resolved or listed as assumptions/open questions.
- Material conclusions include source links or are labeled as human judgment calls.
- Next actions identify owner, dependency, and required human approval point.
- Intake recommendation clearly states whether the project is ready for screening, needs more context, should be watched, or should be passed.

## Human Review

- Approve investment-stage movement, pass/follow-up recommendations, and final task completion.
- Approve external communications, CRM writes, Drive/project creation, legal/counsel actions, and founder-facing requests.
