---
id: vc.run_team_evaluation
title: Run Team Evaluation
slug: run-team-evaluation
agent: vc-evaluation-analyst
skills:
- team-evaluation-and-founder-risk
- red-flags-scanner
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/run-team-evaluation.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Run Team Evaluation

## Objective

Run an evaluation-stage team and founder workstream for one venture-capital opportunity, identifying founder evidence, role gaps, team risk, and next proof needed before formal diligence.

## What To Do

Run a team evaluation covering founder-market fit, role coverage, relevant experience, execution evidence, integrity or consistency signals, hiring gaps, adviser or board quality, reference needs, and team gating risk. Use this as evaluation-stage work, not formal founder diligence, completed reference checking, or background checking. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Create or update a polished Word-ready document named Team Evaluation as a standalone safe static HTML artifact using `artifact_createTextArtifact`, a `.html` filename, and `mimeType: "text/html"`; then attach it to the required output field team evaluation artifact.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Company Name, Opportunity Evaluation, Opportunity Evidence Artifacts, Team Or Founder Evidence.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Team Evaluation Template](../alludium/documents/deal-room/team-evaluation-template.md): Use as the starting structure for the deliverable; adapt it to the facts and avoid generic filler.
- [Evaluation Workstream Guide](../alludium/documents/shared/evaluation-workstream-guide.md): Use as the analysis method.
- [Opportunity Evaluation Framework](../alludium/documents/shared/opportunity-evaluation-framework.md): Use as the analysis method.
- [Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.md): Follow for citations, claim language, assumptions, and evidence quality.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.md): Follow for process boundaries and review standards.

## Deliverable

- Create or update **Team Evaluation** as a standalone safe HTML artifact. Use `.html`, `mimeType: "text/html"`, and complete static HTML suitable for the platform safe previewer.
- Also include a short human-readable summary covering: Main Team Hypothesis, Team Gating Risk, Next Team Proof Needed. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for the company name and at least one relevant source such as founder names, founder materials, public profiles, meeting notes, team page, hiring plan, relationship context, or reference notes before producing the evaluation.

## Guardrails

Draft only unless a human explicitly approves the send, CRM write, Drive change, project creation, child task creation, or stage transition.

## Completion Criteria

- Required input gaps are resolved or listed as assumptions/open questions.
- Material conclusions include source links or are labeled as human judgment calls.
- Next actions identify owner, dependency, and required human approval point.

## Human Review

- Approve investment-stage movement, pass/follow-up recommendations, and final task completion.
- Approve external communications, CRM writes, Drive/project creation, legal/counsel actions, and founder-facing requests.
