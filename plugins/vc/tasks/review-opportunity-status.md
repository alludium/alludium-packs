---
id: vc.review_opportunity_status
title: Review Opportunity Status
slug: review-opportunity-status
agent: vc-pipeline-autopilot
skills:
- citation-enforcement
- vc-task-and-next-step-generation
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/review-opportunity-status.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Review Opportunity Status

## Objective

Review the current status of one venture-capital opportunity and suggest missing inputs, stage movement, and next tasks without producing a formal investment evaluation document.

## What To Do

Review the supplied stage snapshot and current Deal Pipeline state, identify missing inputs, recommend stage movement, and list next task suggestions using the workspace configured stage graph; do not create tasks automatically. This is a status/control helper, not a formal investment evaluation memo. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Use workspace-configured scoring frameworks, CRM providers, stage names, and deal-type metric packs; do not assume a specific fund, CRM, or SaaS default unless the workspace configuration explicitly selects it.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Company Name, Investment Stage, Stage Snapshot, Relevant Artifact IDs.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Deal Pipeline Operating SOP](../alludium/documents/deal-room/deal-room-sop.md): Follow for process boundaries and review standards.
- [Opportunity Evaluation Framework](../alludium/documents/shared/opportunity-evaluation-framework.md): Use as the analysis method.
- [Evaluation Workstream Guide](../alludium/documents/shared/evaluation-workstream-guide.md): Use as the analysis method.
- [Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.md): Follow for citations, claim language, assumptions, and evidence quality.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.md): Follow for process boundaries and review standards.

## Deliverable

- Produce a concise, reviewable task response that a human can act on.
- Also include a short human-readable summary covering: Stage Summary, Missing Inputs, Stage Transition Recommendation, Next Task Suggestions, Source Links, Summary, Recommendation, Assumptions, and other task-specific status fields. Do not output raw JSON unless the user explicitly asks for machine-readable data.

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

- Use the workspace-configured Pipeline Health And Crm Hygiene methodology when applicable: Use only when the workspace CRM/stage model matches the skill assumptions.
