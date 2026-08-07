---
id: vc.promote_candidate_to_deal_pipeline
title: Promote Candidate to Deal Pipeline
slug: promote-candidate-to-deal-pipeline
agent: vc-sourcing-operator
skills:
- origination-deal-pipeline-promotion
- citation-enforcement
- deal-pipeline-setup-and-source-ingestion
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/promote-candidate-to-deal-pipeline.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Promote Candidate to Deal Pipeline

## Objective

Prepare a reviewed, explicitly Fund-routed promotion package for creating a Deal Pipeline from an approved origination candidate while preserving every sourcing-line provenance path.

## What To Do

Promote only human-approved candidates. Require fund id to exactly match one active record in canonical `vc.funds`; never infer it from the primary, latest, or majority Sourcing Line, even when every contributing line currently has the same Fund. Prepare a Deal Pipeline creation package with the explicitly selected Fund, company identity, founder evidence, every contributing Sourcing Line, all source receipts, enrichment/verdict/screen summaries, relationship context, outreach state, conflicts, and open questions. Preserve the Candidate project and its complete multi-line provenance after promotion. Emit `dealCreationProposal.createRequest` with the selected Fund and an incoming `vc.origination_candidate_promoted_to_deal` relationship from origination candidate project id. Do not create or update the Deal Pipeline unless the platform action is explicitly approved.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Origination Candidate Project ID, Promotion Candidate, Target Fund ID.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Promotion Package Template](../alludium/documents/origination/promotion-package-template.html): Use as the starting structure for the deliverable; adapt it to the facts and avoid generic filler.
- [Origination Source Strategy Guide](../alludium/documents/origination/origination-source-strategy-guide.html): Use as the analysis method.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.html): Follow for process boundaries and review standards.

## Deliverable

- Create or update **Promotion Package Artifact** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.
- Also include a short human-readable summary covering: Deal Creation Proposal. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for the approved candidate, an explicit active fund id, target Deal Pipeline policy, promotion threshold evidence, owner, every contributing Sourcing Line and source receipt, and required source artifacts. If fund id is missing, unknown, or inactive, keep promotion incomplete rather than inheriting a Fund from line provenance.

## Guardrails

Promotion package by default. Deal Pipeline creation/update, CRM changes, document creation, and notifications require separate explicit approval.

## Completion Criteria

- Promotion package includes the explicitly selected active fund_id, every Sourcing Line and source receipt, candidate evidence, recommended initial Deal Pipeline state, required tasks, owner, and unresolved risks.
- Human approval boundary for project creation/update is explicit.
- Deal creation request includes `createRequest.fieldValues.fund_id` and the incoming candidate-to-Deal relationship.
