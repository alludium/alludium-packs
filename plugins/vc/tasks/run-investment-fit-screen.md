---
id: vc.run_investment_fit_screen
title: Run Investment Fit Screen
slug: run-investment-fit-screen
agent: vc-first-look-analyst
skills:
- investment-screening-framework
- red-flags-scanner
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/run-investment-fit-screen.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Run Investment Fit Screen

## Objective

Run a fast investment fit screen for one venture-capital opportunity using configured criteria, available evidence, human review gates, and next-action recommendations.

## What To Do

Score each configured investment-fit criterion with rationale, source links, unknowns, red flags, and human-review prompts before recommending continue, watch, or pass. Use a pitch deck, source material, source thread, opportunity intake artifact, meeting notes, or source links as evidence; do not require a pitch deck when another source is sufficient. For company-claimed facts such as ARR and other traction metrics, fundraising ask, round and stage, customer counts, roadmap, go-to-market, and founder/team details, treat uploaded/founder/company-provided materials and supplied CRM notes as the primary source; use public or web research to corroborate, challenge, timestamp, or fill gaps, and when they conflict keep the company-provided value as the primary claim, show the conflicting value and its source, and flag material conflicts for human review rather than silently overwriting the company-provided figure. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Use workspace-configured scoring frameworks, CRM providers, stage names, and deal-type metric packs; do not assume a specific fund, CRM, or SaaS default unless the workspace configuration explicitly selects it. Create or update a polished Word-ready document named Investment Fit Screen Scorecard as a standalone safe static HTML artifact using the Artifact Create Text Artifact tool (`artifact.createTextArtifact`), a `.html` filename, and `mimeType: "text/html"`; do not use `project.instantiateTemplate` or create a `.md`/`text/markdown` artifact for this rendered output; then attach it to the required output field investment screen scorecard artifact.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Company Name, Pitch Deck Artifact, Meeting Notes, Source Links, Opportunity Intake Summary, Source Material Artifact IDs.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Investment Screening Framework](../alludium/documents/shared/investment-screening-framework.md): Use as the analysis method.
- [Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.md): Follow for citations, claim language, assumptions, and evidence quality.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.md): Follow for process boundaries and review standards.

## Deliverable

- Create or update **Investment Fit Screen Scorecard** as a standalone safe HTML artifact. Use `.html`, `mimeType: "text/html"`, and complete static HTML suitable for the platform safe previewer.
- Also include a short human-readable summary covering: Overall Recommendation. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for at least one evidence source before producing an investment fit recommendation.

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

- Use the workspace-configured Investment Screening Framework methodology when applicable: Use only when the workspace explicitly configures this screening framework.
