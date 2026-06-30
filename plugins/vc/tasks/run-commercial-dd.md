---
id: vc.run_commercial_dd
title: Run Commercial DD
slug: run-commercial-dd
agent: vc-diligence-analyst
skills:
- citation-enforcement
- commercial-diligence-workstream
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/run-commercial-dd.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Run Commercial DD

## Objective

Run Commercial DD for one venture-capital opportunity with evidence capture, human review gates, and next-action recommendations.

## What To Do

Run commercial diligence covering market sizing, competition, customer references where applicable, business-model-appropriate traction and economics, GTM/pricing where applicable, and commercial risks. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Use workspace-configured scoring frameworks, CRM providers, stage names, and deal-type metric packs; do not assume a specific fund, CRM, or SaaS default unless the workspace configuration explicitly selects it. Create or update polished Word-ready documents named Commercial DD Report, Market Analysis, and Customer Reference Summary.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Company Name, Business Model, Customer Or User Evidence, Go To Market Evidence, Pricing Or Revenue Evidence, Market Sources.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Diligence Report Template](../alludium/documents/deal-room/diligence-report-template.html): Use as the starting structure for the deliverable; adapt it to the facts and avoid generic filler.
- [Formal Diligence Workstream Guide](../alludium/documents/deal-room/formal-diligence-workstream-guide.html): Use as the analysis method.
- [Formal Diligence Checklist](../alludium/documents/deal-room/formal-diligence-checklist.html): Complete as a checklist with status, evidence, owner, and open items.
- [Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.html): Follow for citations, claim language, assumptions, and evidence quality.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.html): Follow for process boundaries and review standards.

## Deliverable

- Create or update **Commercial DD Report** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.
- Create or update **Market Analysis** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.
- Create or update **Customer Reference Summary** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.

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

## Workspace Methodology

- Use the workspace-configured Market Map Building methodology when applicable: Use only when the workspace explicitly configures this market mapping method.
- Use the workspace-configured Traction And Saas Unit Economics methodology when applicable: Use only for SaaS deals or workspaces that select this metric pack.
