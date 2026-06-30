---
id: vc.record_ic_decision
title: Record IC Decision
slug: record-ic-decision
agent: vc-ic-prep-producer
skills:
- citation-enforcement
- ic-risk-checklist-and-decision-log
- vc-task-and-next-step-generation
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/record-ic-decision.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Record IC Decision

## Objective

Record IC Decision for one venture-capital opportunity with evidence capture, human review gates, and next-action recommendations.

## What To Do

Record the IC decision outcome, vote or consensus summary, dissent and objections, conditions, post-IC action items, and stage transition recommendation. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Use the required input file artifacts investment memo artifact and ic agenda artifact as the IC decision record subjects, alongside the transcript or notes. Create or update a polished Word-ready document named IC Decision Record as a standalone safe static HTML artifact using the Artifact Create Text Artifact tool (`artifact.createTextArtifact`), a `.html` filename, and `mimeType: "text/html"`; do not use the Project Instantiate Template tool, `project.instantiateTemplate`, or `project_instantiateTemplate`, and do not create a `.md`/`text/markdown` artifact for this rendered output; then attach it to the required output field ic decision record artifact. Use `definitionJson.documentRefs` only as source guidance for rendered outputs. Read referenced templates, methodologies, checklists, style guides, operating guidance, and policies, but convert the referenced Markdown/template sections into semantic standalone HTML for `artifact.createTextArtifact`: keep the required first summary section from the task or template, preserve decision-critical section order, omit unsupported boilerplate, and resolve conflicts in favor of the shared HTML contract plus task-specific heading requirements. For refs with `outputFieldKey`, save the `artifact.createTextArtifact` result to that output field and preserve the document ID alongside the output artifact.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Investment Memo, IC Agenda, Ic Transcript Or Notes, Decision Options, Conditions Discussed, Attendees.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [IC Decision Record Template](../alludium/documents/deal-room/ic-decision-record-template.html): Use as the starting structure for the deliverable; adapt it to the facts and avoid generic filler.
- [Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.md): Follow for citations, claim language, assumptions, and evidence quality.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.md): Follow for process boundaries and review standards.

## Deliverable

- Create or update **IC Decision Record** as a standalone safe HTML artifact. Use `.html`, `mimeType: "text/html"`, and complete static HTML suitable for the platform safe previewer.

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
