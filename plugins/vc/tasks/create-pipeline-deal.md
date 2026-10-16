---
id: vc.create_pipeline_deal
title: Create Pipeline Deal
slug: create-pipeline-deal
agent: vc-deal-pipeline-manager
skills:
- company-research-and-enrichment
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/create-pipeline-deal.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Create Pipeline Deal

## Objective

Gather the minimum reviewed identity, source, and Fund context needed to create one simplified VC Deal Pipeline project.

## What To Do

Use `definitionJson.documentRefs` as the durable style contract. Identify one company from the supplied chat, domain, deck, source link, or artifact. Preserve source provenance, distinguish verified facts from assumptions, and capture only confidently supported optional fields. A Fund is optional at creation; when supplied, require an exact active `vc.funds` id and never infer or blend mandates. Do not create the project directly: the platform finalizer owns deterministic creation after human approval. Creation must not trigger initial-state tasks. First read `projectCreation.projectTypeVersion` in the Resolved Task Context. It is the Deal setup this task was started on, not a value you produce. If it is a 1.0.x version with x below 7, this task was started before Deals recorded their company as an Organisation, and that Deal setup can no longer create a Deal. Do not produce a creation payload or complete the task: tell the user in one sentence that the Deal setup has changed and they should start the Deal again from New deal, then stop. The Deal's company is a confirmed Organisation, recorded in `projectCreation.identityLink` with `recordType: organisation` and `roleKey: deal_company`. Reuse an existing Organisation (`mode: reuse`, `recordId`) only with the exact Organisation ID that a Platform identity lookup returned and the user selected; a matching name is never a reuse. When a reused Organisation already has Deals, include `projectCreation.existingDealAcknowledgement` with the `organisationId` and `matchFingerprint` returned by `project.listInvestmentSubjectDeals`, and only after the user has seen those Deals and confirmed a separate Deal. Otherwise create a minimal Organisation (`mode: create`, `displayName`) from the company name alone; do not invent a domain, website, or logo. If you cannot look up existing Organisations, tell the user that a new Organisation record will be created under that name before you complete. Set `projectCreation.name` to the Deal title. Default it to the Organisation's name unless the user gave a different title; the title is the opportunity's own name and does not rename the Organisation. Never put company name, company domain, or company logo url in `projectCreation.fieldValues`.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Company Name, Company Domain, Confirmed Fund ID, Source Artifact IDs.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.html): Follow for citations, claim language, assumptions, and evidence quality.

## Deliverable

- Produce a concise, reviewable task response that a human can act on.
- Also include a short human-readable summary covering: Project Creation Payload. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask only when the company cannot be identified confidently from the available context, or when it is unclear whether an existing Organisation is the same company.

## Guardrails

Do not send messages, write CRM records, create projects, create tasks, or move lifecycle state.

## Completion Criteria

- The company identity is explicit and source context is preserved.
- The output contains projectCreation.name and exactly one projectCreation.identityLink that reuses a user-selected Organisation by ID or creates a minimal Organisation.
- The output carries no legacy company fields in projectCreation.fieldValues.
- Any supplied Fund is an exact active configured Fund id.
- A task started on a Deal setup version 1.0.x with x below 7 produces no creation payload and tells the user to start the Deal again from New deal.

## Human Review

- Approve creation of the Deal Pipeline project and its reviewed fields.
