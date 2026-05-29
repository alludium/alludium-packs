---
id: vc.run_opportunity_evaluation
title: Run Opportunity Evaluation
slug: run-opportunity-evaluation
agent: vc-evaluation-analyst
skills:
- investment-diligence-question-framework
- red-flags-scanner
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/run-opportunity-evaluation.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Run Opportunity Evaluation

## Objective

Run a deeper opportunity evaluation after screening for one venture-capital opportunity with evidence capture, human review gates, and next-action recommendations.

## What To Do

Build an opportunity evaluation from the investment fit screen, meeting records, founder materials, customer evidence, market sources, technical sources, financial sources, and existing questions. Produce a deeper evaluation scorecard, key claims register, critical unknowns, initial diligence recommendations, and recommended decision path. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Use workspace-configured scoring frameworks, CRM providers, stage names, and deal-type metric packs; do not assume a specific fund, CRM, or SaaS default unless the workspace configuration explicitly selects it. Create or update a polished Word-ready document named Opportunity Evaluation.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Company Name, Investment Fit Screen Scorecard, Meeting Records Summary.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Opportunity Evaluation Template](../alludium/documents/deal-room/follow-up-evaluation-template.md): Use as the starting structure for the deliverable; adapt it to the facts and avoid generic filler.
- [Opportunity Evaluation Framework](../alludium/documents/shared/opportunity-evaluation-framework.md): Use as the analysis method.
- [Evaluation Workstream Guide](../alludium/documents/shared/evaluation-workstream-guide.md): Use as the analysis method.
- [Commercial Evaluation Guide](../alludium/documents/deal-room/commercial-evaluation-guide.md): Use as the analysis method.
- [Technical Evaluation Guide](../alludium/documents/deal-room/technical-evaluation-guide.md): Use as the analysis method.
- [Financial Evaluation Guide](../alludium/documents/deal-room/financial-evaluation-guide.md): Use as the analysis method.
- [Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.md): Follow for citations, claim language, assumptions, and evidence quality.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.md): Follow for process boundaries and review standards.

## Deliverable

- Create or update **Opportunity Evaluation** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.

## Missing Input Policy

Ask for the investment screen and at least one meeting, founder-material, customer, market, technical, or financial evidence source before producing the evaluation.

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

- Use the workspace-configured Investment Diligence Question Framework methodology when applicable: Use only when the workspace explicitly configures this diligence framework.
- Use the workspace-configured Market Map Building methodology when applicable: Use only when the workspace explicitly configures this market mapping method.
