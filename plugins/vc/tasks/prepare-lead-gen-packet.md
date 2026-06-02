---
id: vc.prepare_lead_gen_packet
title: Prepare Lead Gen Packet
slug: prepare-lead-gen-packet
agent: vc-origination-scout
skills:
- company-research-and-enrichment
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/prepare-lead-gen-packet.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Prepare Lead Gen Packet

## Objective

Prepare Lead Gen Packet for one venture-capital opportunity with evidence capture, human review gates, and next-action recommendations.

## What To Do

Prepare the lead-generation meeting packet from candidate companies and thesis context; include per-company snapshots, discussion points, and proposed next actions. Cite material claims, separate assumptions from evidence, and do not send messages, mutate CRM records, create folders/projects, create child tasks, or move stages without explicit human approval. Use workspace-configured scoring frameworks, CRM providers, stage names, and deal-type metric packs; do not assume a specific fund, CRM, or SaaS default unless the workspace configuration explicitly selects it. Create or update a polished Word-ready document named Lead Generation Packet.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Candidate Companies, Meeting Date, Thesis Context.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Lead Generation Packet Template](../alludium/documents/deal-room/lead-generation-packet-template.md): Use as the starting structure for the deliverable; adapt it to the facts and avoid generic filler.
- [Origination Source Strategy Guide](../alludium/documents/origination/origination-source-strategy-guide.md): Use as the analysis method.
- [Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.md): Follow for citations, claim language, assumptions, and evidence quality.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.md): Follow for process boundaries and review standards.

## Deliverable

- Create or update **Lead Generation Packet** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.
- Also include a short human-readable summary covering: Lead Gen Packet, Per Company Snapshots, Discussion Points, Proposed Next Actions, Summary, Recommendation, Source Links, Assumptions, and other task-specific status fields. Do not output raw JSON unless the user explicitly asks for machine-readable data.

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

- Use the workspace-configured Market Map Building methodology when applicable: Use only when the workspace explicitly configures this market mapping method.
- Use the workspace-configured Investment Screening Framework methodology when applicable: Use only when the workspace explicitly configures this screening framework.
