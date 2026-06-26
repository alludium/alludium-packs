---
id: vc.generate_diligence_questions
title: Generate Diligence Questions
slug: generate-diligence-questions
agent: vc-evaluation-analyst
skills:
- investment-diligence-question-framework
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/generate-diligence-questions.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Generate Diligence Questions

## Objective

Generate a structured investment diligence question bank for one venture-capital opportunity with evidence capture, human review gates, and next-action recommendations.

## What To Do

Generate prioritized investment diligence questions with rationale, source gap, owner, and urgency. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Use workspace-configured scoring frameworks, CRM providers, stage names, and deal-type metric packs; do not assume a specific fund, CRM, or SaaS default unless the workspace configuration explicitly selects it. Create or update a polished Word-ready document named Structured Diligence Question Bank as a standalone safe static HTML artifact using the Artifact Create Text Artifact tool (`artifact.createTextArtifact`), a `.html` filename, and `mimeType: "text/html"`; do not use the Project Instantiate Template tool, `project.instantiateTemplate`, or `project_instantiateTemplate`, and do not create a `.md`/`text/markdown` artifact for this rendered output; then attach it to the required output field diligence question bank artifact. Use `definitionJson.documentRefs` only as source guidance for rendered outputs. Read referenced templates, methodologies, checklists, style guides, operating guidance, and policies, but manually transform the relevant structure into the standalone HTML content passed to `artifact.createTextArtifact`. For refs with `outputFieldKey`, save the `artifact.createTextArtifact` result to that output field and preserve the document ID alongside the output artifact.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Company Name, Known Claims, Existing Answers, Priority Workstreams.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Investment Diligence Question Framework](../alludium/documents/shared/investment-diligence-question-framework.md): Use as the analysis method.
- [Opportunity Evaluation Framework](../alludium/documents/shared/opportunity-evaluation-framework.md): Use as the analysis method.
- [Evaluation Workstream Guide](../alludium/documents/shared/evaluation-workstream-guide.md): Use as the analysis method.
- [Commercial Evaluation Guide](../alludium/documents/deal-room/commercial-evaluation-guide.md): Use as the analysis method.
- [Technical Evaluation Guide](../alludium/documents/deal-room/technical-evaluation-guide.md): Use as the analysis method.
- [Financial Evaluation Guide](../alludium/documents/deal-room/financial-evaluation-guide.md): Use as the analysis method.
- [Formal Diligence Workstream Guide](../alludium/documents/deal-room/formal-diligence-workstream-guide.md): Use as the analysis method.
- [Formal Diligence Checklist](../alludium/documents/deal-room/formal-diligence-checklist.md): Complete as a checklist with status, evidence, owner, and open items.
- [Legal Diligence Guide](../alludium/documents/deal-room/legal-diligence-guide.md): Use as the analysis method.
- [Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.md): Follow for citations, claim language, assumptions, and evidence quality.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.md): Follow for process boundaries and review standards.

## Deliverable

- Create or update **Structured Diligence Question Bank** as a standalone safe HTML artifact. Use `.html`, `mimeType: "text/html"`, and complete static HTML suitable for the platform safe previewer.

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

- Use the workspace-configured Investment Diligence Question Framework methodology when applicable: Use only when the workspace explicitly configures this diligence framework.
