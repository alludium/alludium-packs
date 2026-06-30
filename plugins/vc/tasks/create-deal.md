---
id: vc.create_deal
title: Create Deal
slug: create-deal
agent: vc-dealflow-concierge
skills:
- deal-pipeline-setup-and-source-ingestion
- company-research-and-enrichment
- citation-enforcement
- pitch-deck-explainer
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/create-deal.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Create Deal

## Objective

Gather enough structured context from chat, inbox material, CRM references, source notes, domains, decks, or origination handoffs to create one Deal Pipeline project.

## What To Do

Guide the user through creating a Deal Pipeline project from whatever context is available: an inbox request, intro note, CRM/source record link, company domain, pitch deck, founder material, source thread, or origination promotion package. Ask only for the missing details needed to confidently identify the company and preserve source context. Capture company name; include domain, source, founder, pitch-deck, source-reference, confidentiality, and other declared Deal Pipeline creation fields only when confidently collected. Do not create the project, run intake, screen the opportunity, create child tasks, move stages, mutate CRM records, send messages, or write external files; the platform finalizer owns deterministic project creation after task completion.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Company Name, Deal Context, Company Domain, Source Record URL, Source Thread URL, Pitch Deck Artifact.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Deal Pipeline Operating SOP](../alludium/documents/deal-room/deal-room-sop.html): Follow for process boundaries and review standards.
- [Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.html): Follow for citations, claim language, assumptions, and evidence quality.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.html): Follow for process boundaries and review standards.

## Deliverable

- Produce a concise, reviewable task response that a human can act on.
- Also include a short human-readable summary covering: Project Creation Field Values, Creation Summary, Missing Creation Context. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for company name or enough evidence to infer it, plus at least one source note, source artifact, source record, pitch deck, company domain, source thread, or origination handoff before completing project creation.

## Guardrails

Guided creation only. No CRM writes, external sends, Drive changes, project creation, child task creation, stage transitions, or screening work.

## Completion Criteria

- company name is captured for guided project creation finalization.
- Available source context is preserved as declared Deal Pipeline creation fields or summarized as creation notes.
- Missing enrichment or screening inputs are listed for the post-create intake task rather than blocking creation unnecessarily.
- The output distinguishes project-creation facts from later intake, enrichment, and screening judgments.

## Human Review

- Confirm the target company identity when source material is ambiguous.
- Confirm whether incomplete context is sufficient to create the project and let intake continue after creation.
