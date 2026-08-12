---
id: vc.link_existing_origination_candidate
title: Link Existing Origination Candidate
slug: link-existing-origination-candidate
agent: vc-sourcing-operator
skills:
- vc-sourcing-dedupe-and-novelty-check
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/link-existing-origination-candidate.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Link Existing Origination Candidate

## Objective

Add one reviewed Sourcing Line provenance relationship to an existing Origination Candidate without duplicating or reassigning the candidate.

## What To Do

Link one existing vc origination candidate project to the current Sourcing Line after an exact identity and access check. Require explicit sourcing line project id and candidate project id; do not guess either ID from names, search ranking, prior chat, or a primary-line label. Read both projects, confirm that the source is the current vc sourcing line, confirm that the target is the intended vc origination candidate, and inspect existing relationships before mutating. If the active `vc.sourcing_line_originated_candidate` edge already exists, return its real relationship ID as already linked and do not create another edge. Otherwise, after explicit human approval, call `project-relationship.create` exactly once with `sourceProjectId=sourcing_line_project_id`, `targetProjectId=candidate_project_id`, `relationshipTypeKey=vc.sourcing_line_originated_candidate`, and metadata that preserves the reviewed source key, source receipt reference, observation time, and link reason when supplied. Return linked only from the terminal platform receipt and preserve every other Sourcing Line relationship. Do not create a Candidate, alter Candidate fields, select a Deal Fund, write CRM, or replace prior provenance. Use `definitionJson.documentRefs` as the durable policy contract.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Sourcing Line Project ID, Existing Candidate Project ID, Source Receipt Reference, Link Reason.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Dedupe And Novelty Policy](../alludium/documents/origination/dedupe-novelty-policy.html): Follow for process boundaries and review standards.

## Deliverable

- Produce a concise, reviewable task response that a human can act on.
- Also include a short human-readable summary covering: Relationship ID, Candidate Project ID, Link Status, Relationship Summary. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Keep the task incomplete until the existing Candidate project ID, current Sourcing Line project ID, and enough evidence to confirm the identity match are available. Candidate project ID is intentionally collected during reviewed task intake rather than inferred from Sourcing Line data.

## Guardrails

The native project relationship is the only allowed write. Require explicit human approval immediately before `project-relationship.create`; all identity, dedupe, and relationship checks are read-only.

## Completion Criteria

- Both project IDs and project types were read and verified in the current workspace.
- Dedupe evidence supports linking to the existing Candidate rather than creating a duplicate.
- The active provenance relationship exists and its real platform relationship ID is recorded.
- No existing Sourcing Line relationship or Candidate field was removed or overwritten.

## Human Review

- Confirm the existing Candidate identity when source records or company names conflict.
- Approve adding the Sourcing Line provenance relationship.
