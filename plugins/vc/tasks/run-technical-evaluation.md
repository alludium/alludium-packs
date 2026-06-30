---
id: vc.run_technical_evaluation
title: Run Technical Evaluation
slug: run-technical-evaluation
agent: vc-evaluation-analyst
skills:
- technical-evaluation-and-product-risk
- red-flags-scanner
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/run-technical-evaluation.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Run Technical Evaluation

## Objective

Run an evaluation-stage technical and product workstream for one venture-capital opportunity, identifying product evidence, technical risk, and next proof needed before formal diligence.

## What To Do

Run a technical evaluation covering product depth, architecture plausibility, technical edge, IP or data defensibility, roadmap realism, technical team coverage, and technical gating risk. Use this as evaluation-stage work, not formal technical diligence, code review, security review, expert validation, or IP clearance. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Create or update a polished Word-ready document named Technical Evaluation as a standalone safe static HTML artifact using the Artifact Create Text Artifact tool (`artifact.createTextArtifact`), a `.html` filename, and `mimeType: "text/html"`; do not use the Project Instantiate Template tool, `project.instantiateTemplate`, or `project_instantiateTemplate`, and do not create a `.md`/`text/markdown` artifact for this rendered output; then attach it to the required output field technical evaluation artifact. Use `definitionJson.documentRefs` only as source guidance for rendered outputs. Read referenced templates, methodologies, checklists, style guides, operating guidance, and policies, but convert the referenced Markdown/template sections into semantic standalone HTML for `artifact.createTextArtifact`: keep the required first summary section from the task or template, preserve decision-critical section order, omit unsupported boilerplate, and resolve conflicts in favor of the shared HTML contract plus task-specific heading requirements. For refs with `outputFieldKey`, save the `artifact.createTextArtifact` result to that output field and preserve the document ID alongside the output artifact.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Company Name, Opportunity Evaluation, Opportunity Evidence Artifacts, Product Or Technical Evidence.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Technical Evaluation Template](../alludium/documents/deal-room/technical-evaluation-template.html): Use as the starting structure for the deliverable; adapt it to the facts and avoid generic filler.
- [Evaluation Workstream Guide](../alludium/documents/shared/evaluation-workstream-guide.md): Use as the analysis method.
- [Technical Evaluation Guide](../alludium/documents/deal-room/technical-evaluation-guide.md): Use as the analysis method.
- [Opportunity Evaluation Framework](../alludium/documents/shared/opportunity-evaluation-framework.md): Use as the analysis method.
- [Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.md): Follow for citations, claim language, assumptions, and evidence quality.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.md): Follow for process boundaries and review standards.

## Deliverable

- Create or update **Technical Evaluation** as a standalone safe HTML artifact. Use `.html`, `mimeType: "text/html"`, and complete static HTML suitable for the platform safe previewer.
- Also include a short human-readable summary covering: Main Technical Hypothesis, Technical Gating Risk, Next Technical Proof Needed. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for the company name and at least one relevant source such as a deck, product demo notes, product materials, architecture claims, roadmap, IP/data narrative, or technical team context before producing the evaluation.

## Guardrails

Draft only unless a human explicitly approves the send, CRM write, Drive change, project creation, child task creation, or stage transition.

## Completion Criteria

- Required input gaps are resolved or listed as assumptions/open questions.
- Material conclusions include source links or are labeled as human judgment calls.
- Next actions identify owner, dependency, and required human approval point.

## Human Review

- Approve investment-stage movement, pass/follow-up recommendations, and final task completion.
- Approve external communications, CRM writes, Drive/project creation, legal/counsel actions, and founder-facing requests.
