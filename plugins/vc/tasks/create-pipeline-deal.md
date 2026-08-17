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

Use `definitionJson.documentRefs` as the durable style contract. Identify one company from the supplied chat, domain, deck, source link, or artifact. Preserve source provenance, distinguish verified facts from assumptions, and capture only confidently supported optional fields. A Fund is optional at creation; when supplied, require an exact active `vc.funds` id and never infer or blend mandates. Complete with company name and any reviewed optional fields. Do not create the project directly: the platform finalizer owns deterministic creation after human approval. Creation must not trigger initial-state tasks.

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

Ask only when the company cannot be identified confidently from the available context.

## Guardrails

Do not send messages, write CRM records, create projects, create tasks, or move lifecycle state.

## Completion Criteria

- The company identity is explicit and source context is preserved.
- The output contains projectCreation.fieldValues.company name.
- Any supplied Fund is an exact active configured Fund id.

## Human Review

- Approve creation of the Deal Pipeline project and its reviewed fields.
