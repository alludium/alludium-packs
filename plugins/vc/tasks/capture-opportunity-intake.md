---
id: vc.capture_opportunity_intake
title: Verify Opportunity Intake
slug: capture-opportunity-intake
agent: vc-intake-readiness-operator
skills:
- deal-pipeline-intake-readiness
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/capture-opportunity-intake.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Verify Opportunity Intake

## Objective

Verify that a Deal Pipeline has enough supplied or approved source context to move into screening.

## What To Do

Verify whether the created Deal Pipeline has enough supplied or approved source context to move into formal screening. Inspect project fields, task inputs, attached/source artifacts, source threads, founder materials, and approved CRM/source payloads such as import payload. When an approved CRM/source payload is present, read only the approved source record scope needed to hydrate missing project fields and source provenance. Capture the source index, hydrated field map, missing information, and screening-readiness status. Do not run public-web research, Exa, Brave, SerpAPI, Firecrawl, competitor discovery, market research, investment scoring, red-flag analysis, or continue/watch/pass recommendations during intake; those belong in screening or later evaluation. Do not require a pitch deck when another supplied source explains the opportunity. Ask for the smallest missing context needed to identify the company and cite at least one source anchor. Create or update the required output field opportunity intake artifact by calling `artifact_createTextArtifact` directly. The artifact must be an HTML text artifact, not a Markdown/project file: use a `.html` filename, `mimeType: "text/html"`, and set content to complete standalone HTML source beginning with `<!doctype html>`. Do not create `.md` files, do not use `text/markdown`, and do not pass Markdown or prose for the platform to convert. Author the summary directly as safe static HTML with semantic sections and optional inline CSS in a `<style>` block. Do not include scripts, event handlers, external assets, forms, iframes, or interactive JavaScript. Include readiness status, source index, hydrated field map, missing information, and screening handoff notes in the HTML document.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Company Name, Approved Source Import Payload, Pitch Deck Artifact, Company Domain, Source System, Source Object URL, Source Thread URL, Source Thread Artifact, Source Material Artifacts, Founder Materials Artifacts, Referrer.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Deal Pipeline Operating SOP](../alludium/documents/deal-room/deal-room-sop.md): Follow for process boundaries and review standards.
- [Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.md): Follow for citations, claim language, assumptions, and evidence quality.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.md): Follow for process boundaries and review standards.

## Deliverable

- Create or update **Opportunity Intake Readiness Summary** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.
- Also include a short human-readable summary covering: Intake Readiness Status, Missing Information, Hydrated Field Map, Source Index. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

If company identity and at least one credible supplied or approved source anchor are present, complete intake and list missing screening inputs instead of blocking. If identity, provenance, or approved source access is insufficient, ask for the minimum missing item such as company domain, deck, source thread, CRM/source record, founder material, or source artifact.

## Guardrails

Intake readiness only. Approved CRM/source reads are allowed within the supplied scope. Public-web research, CRM writes, external sends, Drive changes, child task creation, project creation, and stage transitions are forbidden unless a human explicitly approves a separate workflow.

## Completion Criteria

- Company identity is confirmed or the task is blocked with a specific clarification question.
- At least one supplied or approved source anchor is recorded, or the missing source anchor is requested.
- Hydrated project fields list provenance and confidence without using public-web enrichment.
- Missing information names the smallest inputs needed before or during screening.
- Intake readiness is reported as ready_for_screening, needs_more_info, or blocked.

## Human Review

- Confirm the target company when source material is ambiguous.
- Provide missing deck, CRM/source record, source thread, founder material, or source artifact when intake is not ready.
- Approve final intake readiness before moving to screening.
