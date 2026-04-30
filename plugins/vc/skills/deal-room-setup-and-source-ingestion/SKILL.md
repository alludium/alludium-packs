---
id: deal-room-setup-and-source-ingestion
name: Deal Room Setup & Source Ingestion
description: >
  Plan and index the source materials for a VC deal room. Use this skill when
  turning an inbound opportunity, source thread, uploaded deck, CRM/deal-system
  record, or document repository folder into a reviewable source index, missing
  artifact checklist, and deal-room setup plan. The skill proposes structure and
  metadata; it does not create folders, mutate CRM, or attach files without a
  separately approved workflow.
tags:
  - vc
  - deal-room
  - source-ingestion
  - documents
  - diligence
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: recommended
      required: false
      note: Deal-room setup is strongest with uploaded files, attached deal documents, a CRM/deal-system record, email/source-thread context, and a document repository. Provider-specific tool IDs are intentionally omitted because source files and deal context may come from several configured surfaces.
      gracefulDegradation: Produce a source-index plan and missing-artifact checklist from the materials provided.
    - kind: setup
      importance: recommended
      required: false
      owner: user
      ownerPath: Provide the source materials, CRM/deal-system context, or document repository location before claiming a complete deal-room setup.
      confirmationRequired: true
      gracefulDegradation: Do not claim folder creation, file attachment, or CRM updates happened.
  routingHints:
    preferredSurface: skill
    notes:
      - Use this for deal-room planning and source indexing; actual system changes require explicit approval and connected tools.
---

# Deal Room Setup & Source Ingestion

Turn raw deal inputs into a clean working context for VC evaluation.

This skill is for planning, indexing, and gap detection. It is not a document
storage tool, CRM mutator, or legal data-room administrator.

## Minimum Inputs

Use any available combination of:

- company name and domain
- uploaded or attached deck, memo, transcript, or source document
- source email/thread or referral context
- CRM/deal-system record
- document repository or data-room location
- stage, owner, and intended next task

If the company identity or source packet is ambiguous, ask for clarification before
building the index.

## Process

1. Resolve the deal identity and current stage from supplied materials.
2. List the available source artifacts by type, date, owner, and decision relevance.
3. Identify missing materials required for the next stage.
4. Propose a deal-room structure: folders or sections, metadata fields, and source links.
5. Produce a handoff that downstream screening, meeting, diligence, or IC skills can consume.

## Output Contract

Return:

- `deal_room_summary`: company, stage, owner, source packet, and next intended task
- `source_index`: table of available materials with source, date, status, and use
- `missing_artifact_checklist`: missing items, reason needed, owner, priority
- `setup_plan`: proposed folder/section structure and metadata fields
- `downstream_context`: what later skills should use from the source packet
- `approval_required`: any folder creation, attachment, sharing, or CRM write needed

## Tool Guidance

Use connected source surfaces when available:

- CRM/deal system: Affinity, Salesforce, HubSpot, Attio, Airtable, Notion, or equivalent
- document repository: Google Drive, Dropbox, Box, OneDrive, SharePoint, Notion, or provided files
- public research: Exa, Brave, SerpAPI, and Firecrawl when source identity or claims need context

If files are uploaded or attached, refer to them as source documents, deal artifacts,
or attached files.

## Boundaries

- Do not create folders, attach files, change sharing, or mutate CRM without approval.
- Do not claim an artifact exists unless it is supplied or visible to the consuming agent.
- Do not infer missing legal or financial documents as complete.
- Do not broaden a document's durable scope without explicit user intent.
