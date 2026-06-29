---
id: vc.create_ic_memo
title: Create IC Memo
slug: create-ic-memo
agent: vc-ic-prep-producer
skills:
- ic-memo-assembly
- citation-enforcement
- ic-risk-checklist-and-decision-log
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/create-ic-memo.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Create IC Memo

## Objective

Create IC Memo for one venture-capital opportunity with evidence capture, human review gates, and next-action recommendations.

## What To Do

Assemble the IC memo and pack checklist from review packs, evaluation-stage workstream outputs, available formal diligence outputs, source artifacts, unresolved risks, assumptions, and citation coverage. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Use required evaluation input file artifacts commercial evaluation artifact, technical evaluation artifact, financial evaluation artifact, team evaluation artifact, and diligence question bank artifact as the decision-review source set. Use formal diligence artifacts commercial dd artifact, financial dd artifact, founder evaluation artifact, and technical dd artifact when present, but do not block evaluation-stage review on them. Use the required input file artifacts team review pack artifact and partner review pack artifact as the review-pack sources for the IC memo. Create or update a polished Word-ready document named Investment Memo as a standalone safe static HTML artifact using the Artifact Create Text Artifact tool (`artifact.createTextArtifact`), a `.html` filename, and `mimeType: "text/html"`; do not use the Project Instantiate Template tool, `project.instantiateTemplate`, or `project_instantiateTemplate`, and do not create a `.md`/`text/markdown` artifact for this rendered output; then attach it to the required output field investment memo artifact.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Team Review Pack, Partner Review Pack, Commercial Evaluation, Technical Evaluation, Financial Evaluation, Team Evaluation, Structured Diligence Question Bank, Commercial DD Report, Financial DD Report, Founder Evaluation, Technical DD Report.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Investment Memo Template](../alludium/documents/deal-room/investment-memo-template.md): Use as the starting structure for the deliverable; adapt it to the facts and avoid generic filler.
- [Opportunity Evaluation Framework](../alludium/documents/shared/opportunity-evaluation-framework.md): Use as the analysis method.
- [Evaluation Workstream Guide](../alludium/documents/shared/evaluation-workstream-guide.md): Use as the analysis method.
- [Formal Diligence Workstream Guide](../alludium/documents/deal-room/formal-diligence-workstream-guide.md): Use as the analysis method.
- [Formal Diligence Checklist](../alludium/documents/deal-room/formal-diligence-checklist.md): Complete as a checklist with status, evidence, owner, and open items.
- [Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.md): Follow for citations, claim language, assumptions, and evidence quality.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.md): Follow for process boundaries and review standards.

## Deliverable

- Create or update **Investment Memo** as a standalone safe HTML artifact. Use `.html`, `mimeType: "text/html"`, and complete static HTML suitable for the platform safe previewer.

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
