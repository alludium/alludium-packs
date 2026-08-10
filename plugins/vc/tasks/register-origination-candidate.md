---
id: vc.register_origination_candidate
title: Register Origination Candidate
slug: register-origination-candidate
agent: vc-origination-candidate-manager
skills:
- vc-sourcing-dedupe-and-novelty-check
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/register-origination-candidate.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Register Origination Candidate

## Objective

Create a new durable candidate from a reviewed sourcing result, with a native non-exclusive Sourcing Line provenance relationship.

## What To Do

Normalize one reviewed source result into one new candidate. Capture company identity, stable dedupe key, source evidence, source record keys, discovery timestamp, and why the result matched the source line. Use `project.listForCurrentWorkspace` with limit and offset until the accessible project projection is exhausted, then use `project.findById` to inspect candidate-type records and compare stable candidate keys before proposing creation. If an exact existing Candidate is found, do not emit `projectCreation.createRequest` and do not complete this creation task; return the existing Candidate project link and route the Sourcing Line Manager to `link-existing-origination-candidate`. For a genuinely new Candidate, emit `projectCreation.createRequest` with candidate fields and an incoming `vc.sourcing_line_originated_candidate` relationship from sourcing line project id. Do not persist an exclusive owner-line or hub ID on the candidate. Multiple sourcing lines may independently relate to the same candidate through the dedicated existing-candidate link task rather than by duplicating the candidate. Do not infer a Deal Fund from any provenance line. Use `definitionJson.documentRefs` as the durable document reference contract; apply operating guidance and policy references to evidence capture, dedupe, and relationship handling.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Company Name, Sourcing Line Project ID, Source Evidence.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Candidate Batch Template](../alludium/documents/origination/candidate-batch-template.html): Follow for process boundaries and review standards.
- [Dedupe And Novelty Policy](../alludium/documents/origination/dedupe-novelty-policy.html): Follow for process boundaries and review standards.

## Deliverable

- Produce a concise, reviewable task response that a human can act on.
- Also include a short human-readable summary covering: Candidate Dedupe Key, Source Evidence Summary, Project Creation Request. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Keep registration incomplete when company identity, sourcing-line project ID, stable dedupe key, source evidence, or the new-versus-existing identity decision is missing or ambiguous.

## Guardrails

Normalize and propose only. Do not write CRM, contact founders, create Deals, or resolve ambiguous identity matches without human review.

## Completion Criteria

- One candidate identity and stable dedupe key are captured.
- Source evidence and a non-exclusive sourcing-line relationship are independently reviewable.
- The candidate has no mandatory hub or exclusive owner-line field.
- Guided creation output contains all required candidate fields and relationship metadata.

## Human Review

- Resolve ambiguous company or founder identity.
- Resolve whether an existing Candidate, prior pass, or Deal is the same company before approving creation.
- When an existing Candidate matches, stop creation and approve a separate link-existing-origination-candidate task instead.
