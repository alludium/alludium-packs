---
id: vc.run_financial_evaluation
title: Run Financial Evaluation
slug: run-financial-evaluation
agent: vc-evaluation-analyst
skills:
- financial-evaluation-and-financing-risk
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/run-financial-evaluation.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Run Financial Evaluation

## Objective

Run an evaluation-stage financial and financing workstream for one venture-capital opportunity, identifying model evidence, financing risk, and next proof needed before formal diligence.

## What To Do

Run a financial evaluation covering business model, forecast plausibility, revenue quality, burn, runway, use of funds, valuation, ownership, financing path, and financial gating risk. Use this as evaluation-stage work, not formal financial diligence, accounting advice, tax advice, or legal advice. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Create or update a polished Word-ready document named Financial Evaluation.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Company Name, Opportunity Evaluation, Opportunity Evidence Artifacts, Financial Or Financing Evidence.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Financial Evaluation Template](../alludium/documents/deal-room/financial-evaluation-template.md): Use as the starting structure for the deliverable; adapt it to the facts and avoid generic filler.
- [Evaluation Workstream Guide](../alludium/documents/shared/evaluation-workstream-guide.md): Use as the analysis method.
- [Financial Evaluation Guide](../alludium/documents/deal-room/financial-evaluation-guide.md): Use as the analysis method.
- [Opportunity Evaluation Framework](../alludium/documents/shared/opportunity-evaluation-framework.md): Use as the analysis method.
- [Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.md): Follow for citations, claim language, assumptions, and evidence quality.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.md): Follow for process boundaries and review standards.

## Deliverable

- Create or update **Financial Evaluation** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.
- Also include a short human-readable summary covering: Main Financial Hypothesis, Financial Gating Risk, Next Financial Proof Needed. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for the company name and at least one relevant source such as a deck, screen, model extract, burn/runway context, valuation or cap-table context, revenue evidence, pricing notes, or use-of-funds narrative before producing the evaluation.

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

- Use the workspace-configured Traction And Saas Unit Economics methodology when applicable: Use only for SaaS deals or workspaces that select this metric pack.
