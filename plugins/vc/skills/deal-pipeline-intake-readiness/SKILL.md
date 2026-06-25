---
id: deal-pipeline-intake-readiness
name: Deal Pipeline Intake Readiness
description: >
  Verify that a Deal Pipeline project has enough supplied or approved source context
  to move into investment screening. Use this skill for intake-stage field hydration,
  CRM/source provenance checks, missing-information prompts, and screening-readiness
  summaries. It does not perform public-web research, investment scoring, red-flag
  analysis, market mapping, or diligence.
tags:
  - vc
  - deal-pipeline
  - intake
  - readiness
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: recommended
      required: false
      note: Intake readiness can use the platform project context, attached files, approved CRM/source records, and source-thread artifacts. Public-web research tools are out of scope for this skill.
      gracefulDegradation: Work from supplied project fields and artifacts, then ask for the minimum missing context.
    - kind: setup
      importance: recommended
      required: false
      owner: user
      ownerPath: Provide or approve the CRM/source record, source thread, deck, founder material, or source artifact needed to establish screening readiness.
      confirmationRequired: true
      gracefulDegradation: Mark intake as not ready and list the smallest missing inputs.
  routingHints:
    preferredSurface: skill
    notes:
      - This skill prepares the opportunity for screening; it does not screen the opportunity.
---

# Deal Pipeline Intake Readiness

Check whether a Deal Pipeline project has enough trustworthy, supplied context to
move into investment screening.

This skill is intentionally narrow. It is a readiness and field-hydration gate,
not a company research workflow and not an investment judgment workflow.

## Minimum Inputs

To mark intake ready for screening, require:

- company identity: `company_name`
- at least one credible source anchor:
  - company domain
  - approved CRM/source record
  - source thread URL or source-thread artifact
  - pitch deck artifact
  - source material artifact
  - founder material artifact
- provenance for every field hydrated during intake

A source anchor whose content the agent can read — a CRM/source record, deck, source
thread, source material, or founder material — counts only once it has actually been
inspected (see "A Source Anchor Must Be Read, Not Just Recorded" below). A company
domain serves as an identity/disambiguation anchor rather than a readable record, and
does not require a read during intake because public-web research is out of scope here.

If company identity is ambiguous, stop and ask the user to confirm the target
company before continuing.

## Approved Source Hydration

Use only supplied or approved source context:

- existing project fields
- task input fields
- approved CRM/source payloads such as Affinity import payloads
- approved CRM/source records within the selected scope
- attached decks, source threads, source notes, founder materials, or source artifacts
- source URLs already supplied by the user or project context

When a CRM/source payload is present, read only the approved record scope needed
to hydrate project fields and source provenance. Record which source supplied
each hydrated value.

## A Source Anchor Must Be Read, Not Just Recorded

A supplied source anchor counts as evidence only after its contents have been
inspected. The presence of a pointer is not the same as reading what it points to.

- When `source_system` and `source_object_url` (or a source object ID) identify a
  scoped CRM/source record such as an Affinity company or opportunity, treat that as
  an approved scoped read for that specific record. If the URL path resembles
  `.../companies/<id>`, treat it as a company and read it with `affinity_get_company`
  using that ID; otherwise treat it as an opportunity or list entry and read it with
  `affinity_get_opportunity` or `affinity_get_list_entries`. If the URL cannot be
  parsed or the direct read is empty, confirm the record with
  `affinity_search_companies` using the confirmed company identity before reading.
  Hydrate available fields with provenance before deciding readiness or listing fields
  as missing.
- Do not mark a field missing, set a readiness status, or create an intake artifact
  on the basis of a CRM/source URL whose record has not actually been read.
- If the required CRM/source read tool is unavailable or the connection is inactive,
  do not complete intake from the URL string. Stop and ask the user to connect the
  source, approve the read, supply an export/snapshot, or run the appropriate import
  task before producing output.

This applies to any source anchor whose content the agent can read: a CRM/source
record should be read, not just recorded as a URL. The same principle holds for other
readable anchors such as an attached deck or source thread, each handled through its
own extraction path; deck extraction specifically is owned by the deck-handling
workflow, not gated here.

## Do Not Use Public Research

Do not use Exa, Brave, SerpAPI, Firecrawl, broad web search, market research
providers, adverse-media searches, or competitor discovery during intake.

If public research would be useful, list it as a screening or evaluation follow-up
rather than doing it inside intake.

## Readiness Decision

Return one of these statuses:

- `ready_for_screening`: identity is confirmed and at least one credible source anchor has been inspected (its contents read, not just its presence noted)
- `needs_more_info`: a small set of missing fields or artifacts is needed before a durable intake artifact should be created
- `blocked`: identity, source provenance, or approved source access is insufficient, and the user must answer a specific question before intake can continue

Readiness is about whether screening can start. It is not a recommendation to
continue, watch, or pass.

## Output Contract

Return:

- `intake_readiness_status`: one readiness status
- `source_index`: supplied or approved source anchors used for intake
- `hydrated_field_map`: project fields observed or filled, with provenance
- `missing_information`: the smallest missing inputs needed for screening
- `opportunity_intake_artifact_id`: compact readiness summary artifact only when at least one supplied or approved source anchor has been inspected, or when the user explicitly approves creating a partial artifact with gaps

For `needs_more_info` or `blocked` caused by missing source anchoring, ask the user for the minimum missing domain, deck, source thread, CRM/source record, founder material, or source artifact through task chat/questions. Do not create a placeholder Opportunity Intake Readiness Summary solely to satisfy an output field.

## Boundaries

- Do not score investment fit.
- Do not produce red-flag analysis.
- Do not run public-web enrichment.
- Do not create child tasks, move stages, mutate CRM, send communications, create folders, or write external systems without explicit human approval.
- Do not block intake just because deeper screening evidence is incomplete; list those gaps for screening.
