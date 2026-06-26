---
id: vc.capture_opportunity_intake
title: Verify Opportunity Intake
slug: capture-opportunity-intake
agent: vc-intake-readiness-operator
skills:
- deal-pipeline-intake-readiness
- pitch-deck-explainer
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/capture-opportunity-intake.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Verify Opportunity Intake

## Objective

Verify that a Deal Pipeline has enough supplied or approved source context to move into screening.

## What To Do

Verify whether the created Deal Pipeline has enough supplied or approved source context to move into formal screening. Inspect project fields, task inputs, attached/source artifacts, source threads, founder materials, and approved CRM/source payloads such as import payload. When an approved CRM/source payload is present, read only the approved source record scope needed to hydrate missing project fields and source provenance. When source system and source object url identify a scoped CRM/source record such as an Affinity company or opportunity, treat that as an approved scoped read for that specific record. Resolve source object url to a tool call: if the URL path resembles `.../companies/<id>`, treat it as a company and read it with affinity get company using that ID; if it resembles `.../lists/<id>` or a list-entry path, read it with affinity get list entries; otherwise treat it as an opportunity and read it with affinity get opportunity. If the URL cannot be parsed or the direct read returns nothing, confirm the record with affinity search companies using the confirmed company identity before reading, rather than completing from the URL string. Read the record and hydrate available fields with provenance before assessing readiness. A source anchor that is recorded but not read does not count as inspected: do not mark fields missing, set readiness, or create an artifact on the basis of a CRM/source URL whose record has not actually been read. If the required CRM/source read tool is unavailable or the connection is inactive, do not complete intake from the URL string; stop and ask the user to connect the source, approve the read, supply an export/snapshot, or run the appropriate import task. Capture the source index, hydrated field map, missing information, and screening-readiness status. Do not run public-web research, Exa, Brave, SerpAPI, Firecrawl, competitor discovery, market research, investment scoring, red-flag analysis, or continue/watch/pass recommendations during intake; those belong in screening or later evaluation. Do not require a pitch deck when another supplied source explains the opportunity. When pitch deck artifact is present, inspect, extract, search, or route the deck through `pitch-deck-explainer` before using it as evidence or declaring deck-contained fields missing. Deck presence alone is not evidence. If the deck cannot be inspected with available tools, mark it as unreadable, do not count it as satisfying source readiness, and ask for a readable deck, extracted text, an approved extraction path, or manual field values before saving a final readiness artifact. Ask for the smallest missing context needed to identify the company and cite at least one source anchor. If identity or source anchoring is insufficient, do not create or save an opportunity intake artifact; use task chat/questions to request the missing item and keep the intake state interactive. Create or update opportunity intake artifact only after at least one supplied or approved source anchor has been inspected, or when a human explicitly approves a partial artifact with gaps. When an artifact is allowed, call `artifact_createTextArtifact` directly. The artifact must be an HTML text artifact, not a Markdown/project file: use a `.html` filename, `mimeType: "text/html"`, and set content to complete standalone HTML source beginning with `<!doctype html>`. Do not create `.md` files, do not use `text/markdown`, and do not pass Markdown or prose for the platform to convert. Author the summary directly as safe static HTML with semantic sections and optional inline CSS in a `<style>` block. Do not include scripts, event handlers, external assets, forms, iframes, or interactive JavaScript. Start the HTML body with a compact "At a glance" overview that surfaces company identity, readiness status, source confidence, top missing inputs, and the screening handoff recommendation before any detailed tables. Style the overview as a concise static card or summary table so the first screen is decision-useful. Include readiness status, source index, hydrated field map, missing information, and screening handoff notes in the HTML document.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Company Name, Approved Source Import Payload, Pitch Deck Artifact, Company Domain, Source System, Source Object URL, Source Thread URL, Source Thread Artifact, Source Material Artifacts, Founder Materials Artifacts, Referrer.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Deal Pipeline Operating SOP](../alludium/documents/deal-room/deal-room-sop.md): Follow for process boundaries and review standards.
- [Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.md): Follow for citations, claim language, assumptions, and evidence quality.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.md): Follow for process boundaries and review standards.

## Deliverable

- When task instructions call for it, create or update **Opportunity Intake Readiness Summary** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.
- Also include a short human-readable summary covering: Intake Readiness Status, Missing Information, Hydrated Field Map, Source Index. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

If company identity and at least one credible supplied or approved source anchor that has actually been inspected are present, complete intake and list missing screening inputs instead of blocking. A recorded but unread source anchor, such as a supplied CRM/source URL whose record was never read or an attached deck whose contents were never inspected, does not satisfy this bar. If identity, provenance, or approved source access is insufficient, or a supplied CRM/source record or deck cannot be read with the available tools, ask for the minimum missing item such as connecting/approving the CRM/source, a company domain, readable deck or extracted deck text, source thread, CRM/source record, founder material, or source artifact. If a pitch deck is attached but unreadable, do not treat the deck artifact ID as a credible source anchor until its contents have been inspected or a human explicitly approves a partial artifact with gaps.

## Guardrails

Intake readiness only. Approved CRM/source reads are allowed within the supplied scope. Public-web research, CRM writes, external sends, Drive changes, child task creation, project creation, and stage transitions are forbidden unless a human explicitly approves a separate workflow.

## Completion Criteria

- Company identity is confirmed or the task is blocked with a specific clarification question.
- At least one supplied or approved source anchor is recorded before an intake artifact is created, or the missing source anchor is requested without creating an artifact.
- Any supplied CRM/source record anchor is read with an available tool before readiness or missing fields are decided, or the user is asked to connect/approve the source or supply an export when the record cannot be read.
- Any attached pitch deck is inspected and cited, or recorded as unreadable and excluded from readiness evidence.
- Hydrated project fields list provenance and confidence without using public-web enrichment.
- Missing information names the smallest inputs needed before or during screening.
- Intake readiness is reported as ready_for_screening, needs_more_info, or blocked.

## Human Review

- Confirm the target company when source material is ambiguous.
- Provide missing deck, CRM/source record, source thread, founder material, or source artifact when intake is not ready.
- Approve final intake readiness before moving to screening.
