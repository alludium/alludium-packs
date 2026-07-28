---
id: vc.register_origination_candidate
title: Register Origination Candidate
slug: register-origination-candidate
agent: vc-sourcing-operator
skills:
- vc-sourcing-dedupe-and-novelty-check
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/register-origination-candidate.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Register Origination Candidate

## Objective

Normalize a reviewed sourcing result into a first-class Origination Candidate project with durable provenance and dedupe keys.

## What To Do

Normalize one reviewed source result into one candidate. Capture company name, domain and stable dedupe key, originating line project ID, parent pipeline project ID when available, source URLs, source record keys, discovery timestamp, evidence confidence, and why the source result matched the line. Emit `projectCreation.createRequest` with the required field values and `relationships: [{ direction: "incoming", relatedProjectId: sourcing_line_project_id, relationshipTypeKey: "vc.sourcing_line_originated_candidate", metadata: { sourceRecordKeys, discoveredAt } }]`. Do not create the project directly; the platform finalizer owns deterministic, atomic creation. Use `project-relationship.create` only to add another existing sourcing line to an existing candidate. Preserve all source receipts and do not turn unverified social or repository signals into company facts. Use `definitionJson.documentRefs` as the durable document reference contract.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Company Name, Sourcing Line Project ID, Source Evidence, Origination Pipeline Project ID.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Candidate Batch Template](../alludium/documents/origination/candidate-batch-template.md): Follow for process boundaries and review standards.
- [Dedupe And Novelty Policy](../alludium/documents/origination/dedupe-novelty-policy.md): Follow for process boundaries and review standards.

## Deliverable

- Produce a concise, reviewable task response that a human can act on.
- Also include a short human-readable summary covering: Registration Summary, Candidate Dedupe Key, Sourcing Line Relationship Key, Source Evidence Summary, Project Creation Request. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Keep registration incomplete when company identity, originating line project ID, stable dedupe key, or source evidence is missing or ambiguous.

## Guardrails

Normalize and propose only. Do not write to CRM, contact founders, create Deal Pipeline projects, or resolve ambiguous identity matches without human review.

## Completion Criteria

- One candidate identity and stable dedupe key are captured.
- Originating line and source evidence are durable and independently reviewable.
- Duplicate, prior-pass, existing-deal, and do-not-contact checks are recorded where available.
- Guided creation output contains all required candidate fields.

## Human Review

- Resolve ambiguous company or founder identity.
- Approve registration when an existing candidate, prior pass, or Deal Pipeline may match.
