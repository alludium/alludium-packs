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

Prepare a reviewed promotion package for creating or updating a Deal Pipeline from an approved origination candidate.

## What To Do

Promote only human-approved candidates. Prepare a Deal Pipeline creation/update package with company identity, founder evidence, source receipts, enrichment/verdict/screen summaries, relationship context, outreach state, and open questions. Do not create or update the Deal Pipeline unless the platform action is explicitly approved. When creation is approved, the platform finalizer should use atomic project creation with `relationships: [{ direction: "incoming", relatedProjectId: origination_candidate_project_id, relationshipTypeKey: "vc.origination_candidate_promoted_to_deal", metadata: { promotionPackageArtifactId } }]`. Use `project-relationship.create` only when both the candidate and Deal Pipeline already exist. Compatibility project-ID fields may be written during rollout but do not replace the native relationship. Emit `dealCreationProposal.createRequest` with Deal Pipeline field values and `relationships: [{ direction: "incoming", relatedProjectId: origination_candidate_project_id, relationshipTypeKey: "vc.origination_candidate_promoted_to_deal", metadata: { promotionPackageArtifactId } }]`. This task does not claim to finalize creation or return a Deal Pipeline project ID; those mappings can be added only when the platform finalizer exposes a confirmed result contract.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Origination Candidate Project ID, Promotion Candidate.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Promotion Package Template](../alludium/documents/origination/promotion-package-template.md): Use as the starting structure for the deliverable; adapt it to the facts and avoid generic filler.
- [Origination Source Strategy Guide](../alludium/documents/origination/origination-source-strategy-guide.md): Use as the analysis method.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.md): Follow for process boundaries and review standards.

## Deliverable

- Create or update **Promotion Package Artifact** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.
- Also include a short human-readable summary covering: Deal Creation Proposal. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for approved candidate, target Deal Pipeline policy, promotion threshold evidence, owner, and required source artifacts.

## Guardrails

Promotion package by default. Deal Pipeline creation/update, CRM changes, document creation, and notifications require separate explicit approval.

## Completion Criteria

- Promotion package includes source receipts, candidate evidence, recommended initial Deal Pipeline state, required tasks, owner, and unresolved risks.
- Human approval boundary for project creation/update is explicit.
- Deal creation proposal contains the incoming candidate relationship and is not represented as a completed project creation.
