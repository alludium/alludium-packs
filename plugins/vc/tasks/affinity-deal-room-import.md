---
id: vc.affinity_deal_room_import
title: Import Affinity Deal Pipeline Seed
slug: affinity-deal-room-import
agent: vc-deal-room-setup-guide
skills:
- vc-affinity-deal-pipeline-import
- vc-affinity-sync-read
- deal-pipeline-setup-and-source-ingestion
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-integrations/affinity-deal-room-import.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Import Affinity Deal Pipeline Seed

## Objective

Import one approved Affinity seed deal into an already-created Deal Pipeline project with source provenance and approval evidence.

## What To Do

Import only the approved Affinity seed deal represented by the import payload into the current Deal Pipeline project. Confirm the platform has already created the target project, verify the payload contains reviewed source scope, accepted stage mapping, selected seed deal, and approval metadata, then perform the smallest approved Affinity reads needed to populate source provenance and field mapping. Map company identity into company name, company_domain, optional company logo url when an approved Affinity/enrichment field provides a usable image URL, source reference fields, owner/source fields, and initial investment stage. When approved associated person IDs are available on the Affinity organization or opportunity, read only those person records needed to identify founders or founder contacts, then populate founder_names and founder_profiles. Prefer founder_profiles as a JSON array of objects with name, email, linkedinUrl, sourcePersonId, title, and sourceUrl keys, omitting unknown keys. sourcePersonId is the external person record ID from the source CRM; sourceUrl is the external person/profile URL when available. Produce a durable import receipt artifact and compact summaries of imported fields, source records read, duplicate handling, unresolved gaps, and recommended next Deal Pipeline tasks. Do not create projects, import unapproved records, enable recurring sync, write to Affinity, move stages, create notes, update external records, send notifications, or create follow-up tasks.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Import Payload.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Deliverable

- Create or update **Affinity Import Receipt** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.
- Also include a short human-readable summary covering: Import Status, Import Summary, Imported Field Map, Source Index, Next Task Recommendations. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

If the target project, approved seed deal, reviewed source scope, accepted stage mapping, or approval metadata is missing, mark the import blocked, name the missing evidence, and produce an import receipt. Do not invent source IDs or broaden scope.

## Guardrails

Project-scoped import only. Reads are limited to approved Affinity records. External writes, recurring sync, CRM mutation, stage movement, note creation, notifications, and project creation are forbidden.

## Completion Criteria

- The target Deal Pipeline project already exists and is named in the receipt.
- The approved Affinity seed deal, source scope, stage mapping, and approval metadata are recorded.
- Imported project-field values list source IDs, source URLs, confidence, and gaps.
- Founder identity output uses founder_names plus structured founder_profiles when associated Affinity person records or approved seed fields provide enough evidence.
- Duplicate handling states that the platform-created project is the canonical target for this seed deal.
- No external writes, recurring schedules, or additional project creations were performed.

## Human Review

- Approve retrying a blocked import with corrected setup evidence.
- Approve any later Affinity write-back, recurring sync, notification, or follow-up task creation separately.
