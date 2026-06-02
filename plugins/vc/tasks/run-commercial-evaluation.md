---
id: vc.run_commercial_evaluation
title: Run Commercial Evaluation
slug: run-commercial-evaluation
agent: vc-evaluation-analyst
skills:
- commercial-evaluation-and-market-risk
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/run-commercial-evaluation.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Run Commercial Evaluation

## Objective

Run an evaluation-stage commercial workstream for one venture-capital opportunity, identifying market/customer evidence, GTM risk, and next proof needed before formal diligence.

## What To Do

Run a commercial evaluation covering customer segment, pain urgency, budget, pricing, GTM path, competition, lightweight market sizing, and commercial gating risk. Use this as evaluation-stage work, not formal commercial diligence. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Create or update a polished Word-ready document named Commercial Evaluation.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Company Name, Opportunity Evaluation, Opportunity Evidence Artifacts, Customer Or Market Evidence.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Commercial Evaluation Template](../alludium/documents/deal-room/commercial-evaluation-template.md): Use as the starting structure for the deliverable; adapt it to the facts and avoid generic filler.
- [Evaluation Workstream Guide](../alludium/documents/shared/evaluation-workstream-guide.md): Use as the analysis method.
- [Commercial Evaluation Guide](../alludium/documents/deal-room/commercial-evaluation-guide.md): Use as the analysis method.
- [Opportunity Evaluation Framework](../alludium/documents/shared/opportunity-evaluation-framework.md): Use as the analysis method.
- [Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.md): Follow for citations, claim language, assumptions, and evidence quality.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.md): Follow for process boundaries and review standards.

## Deliverable

- Create or update **Commercial Evaluation** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.
- Also include a short human-readable summary covering: Main Commercial Hypothesis, Commercial Gating Risk, Next Commercial Proof Needed. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for the company name and at least one relevant source such as a deck, screen, call notes, customer evidence, pricing context, GTM notes, pipeline evidence, or market source before producing the evaluation.

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
