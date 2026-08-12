---
id: vc.source_thesis_targets
title: Source Thesis Targets
slug: source-thesis-targets
agent: vc-origination-scout
skills:
- company-research-and-enrichment
- founder-outreach-and-intro-paths
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/source-thesis-targets.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Source Thesis Targets

## Objective

Source Thesis Targets for one venture-capital opportunity with evidence capture, human review gates, and next-action recommendations.

## What To Do

Resolve fund id by exact stable-ID equality against one runtime-bound canonical `vc.funds` record whose status is actively investing. Apply that matched record's stage, sectors, geographies, thesis, `minimumCheckSize`, `maximumCheckSize`, currency, exclusions, and `scoringFramework`, and never use another Fund. Every populated matched Fund field is authoritative. Treat the requested thesis area, geography, stage focus, market filters, and generic Pack methodology only as missing, non-conflicting detail within the mandate; never override or weaken a populated matched Fund field. If no exact active Fund record is available, keep sourcing incomplete and emit no Fund-relative target list. Research thesis-aligned companies for the requested thesis area, geography, stage focus, and market filters; return target companies, fit rationale, source links, warm intro paths, and confidence notes. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Use workspace-configured scoring frameworks, CRM providers, stage names, and deal-type metric packs; do not assume a specific fund, CRM, or SaaS default unless the workspace configuration explicitly selects it. Create or update a polished Word-ready document named Thesis Target List.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Thesis Area, Geography, Fund ID, Stage Focus, Market Filters.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Thesis Target List Template](../alludium/documents/deal-room/thesis-target-list-template.html): Use as the starting structure for the deliverable; adapt it to the facts and avoid generic filler.
- [Origination Source Strategy Guide](../alludium/documents/origination/origination-source-strategy-guide.html): Use as the analysis method.
- [Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.html): Follow for citations, claim language, assumptions, and evidence quality.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.html): Follow for process boundaries and review standards.

## Deliverable

- Create or update **Thesis Target List** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.

## Missing Input Policy

Keep Fund-specific sourcing incomplete when fund_id is missing, unknown, inactive, or canonical vc.funds context is unavailable. Otherwise ask for missing required inputs before producing investment-stage recommendations.

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
