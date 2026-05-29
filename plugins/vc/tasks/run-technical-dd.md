---
id: vc.run_technical_dd
title: Run Technical DD
slug: run-technical-dd
agent: vc-diligence-analyst
skills:
- team-and-hiring-assessment
- red-flags-scanner
- citation-enforcement
- technical-diligence-workstream
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/run-technical-dd.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Run Technical DD

## Objective

Run Technical DD for one venture-capital opportunity with evidence capture, human review gates, and next-action recommendations.

## What To Do

Run technical diligence covering architecture, product, engineering team, IP and licensing, AI/ML risks, scalability, security, and technical scorecard from the supplied technical source artifact list and approved access references. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Create or update a polished Word-ready document named Technical DD Report.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Technical Source Artifact IDs, Repo Or Code Access, Product Roadmap, Ip Patent Materials, Engineering Team Materials.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Diligence Report Template](../alludium/documents/deal-room/diligence-report-template.md): Use as the starting structure for the deliverable; adapt it to the facts and avoid generic filler.
- [Formal Diligence Workstream Guide](../alludium/documents/deal-room/formal-diligence-workstream-guide.md): Use as the analysis method.
- [Formal Diligence Checklist](../alludium/documents/deal-room/formal-diligence-checklist.md): Complete as a checklist with status, evidence, owner, and open items.
- [Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.md): Follow for citations, claim language, assumptions, and evidence quality.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.md): Follow for process boundaries and review standards.

## Deliverable

- Create or update **Technical DD Report** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.
- Also include a short human-readable summary covering: Architecture Product Summary, Technical Team Assessment, Oss Licensing Ip Checks, Ai Ml Risk Assessment, Scalability Security Concerns, Technical Scorecard, Summary, Recommendation, and other task-specific status fields. Do not output raw JSON unless the user explicitly asks for machine-readable data.

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
