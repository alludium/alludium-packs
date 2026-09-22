---
id: people-organisations-agent-readiness
name: "People and Organisations Agent Readiness"
description: >
  Resolve and use Person and Organisation identity records in Deal Manager
  conversations while keeping identity data separate from Deal facts and
  requiring explicit authorization for identity mutations.
tags:
  - vc
  - identity
  - people
  - organisations
  - provenance
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: required
      required: true
      applicationExternalId: alludium-platform
      toolExternalId: identity.findOrganisation
      note: Read bounded organisation candidates before proposing reuse or creation.
    - kind: tool
      importance: required
      required: true
      applicationExternalId: alludium-platform
      toolExternalId: identity.findPerson
      note: Read bounded person candidates before proposing reuse or creation.
    - kind: tool
      importance: required
      required: true
      applicationExternalId: alludium-platform
      toolExternalId: identity.findSourceCapture
      note: Read an existing source capture before replaying or correcting provenance.
    - kind: tool
      importance: required
      required: true
      applicationExternalId: alludium-platform
      toolExternalId: identity.listAffiliations
      note: Inspect existing affiliations before proposing relationship changes.
    - kind: tool
      importance: required
      required: true
      applicationExternalId: alludium-platform
      toolExternalId: identity.listChangeHistory
      note: Inspect durable identity change history when correction or replay context matters.
    - kind: tool
      importance: required
      required: true
      applicationExternalId: alludium-platform
      toolExternalId: identity.listFieldValues
      note: Read current intrinsic fields before proposing a correction or update.
    - kind: tool
      importance: required
      required: true
      applicationExternalId: alludium-platform
      toolExternalId: identity.listIdentifiers
      note: Read existing identifiers before proposing a new identifier or candidate reuse.
    - kind: tool
      importance: required
      required: true
      applicationExternalId: alludium-platform
      toolExternalId: identity.listOrganisations
      note: Browse bounded organisation records when a direct candidate lookup is insufficient.
    - kind: tool
      importance: required
      required: true
      applicationExternalId: alludium-platform
      toolExternalId: identity.listPeople
      note: Browse bounded person records when a direct candidate lookup is insufficient.
    - kind: tool
      importance: required
      required: true
      applicationExternalId: alludium-platform
      toolExternalId: identity.listProjectLinks
      note: Inspect current project links before proposing a link or unlink.
    - kind: tool
      importance: required
      required: true
      applicationExternalId: alludium-platform
      toolExternalId: identity.listSourceCaptureHistory
      note: Inspect source-capture history before replay or correction.
    - kind: tool
      importance: required
      required: true
      applicationExternalId: alludium-platform
      toolExternalId: identity.lookupCandidates
      note: Use the bounded read-only candidate lookup contract for identity proposals.
    - kind: tool
      importance: required
      required: true
      applicationExternalId: alludium-platform
      toolExternalId: identity.addAffiliation
      note: Add an affiliation only after explicit human approval and observed record identities.
    - kind: tool
      importance: required
      required: true
      applicationExternalId: alludium-platform
      toolExternalId: identity.addIdentifier
      note: Add an identifier only after explicit human approval and provenance review.
    - kind: tool
      importance: required
      required: true
      applicationExternalId: alludium-platform
      toolExternalId: identity.archiveOrganisation
      note: Archive an organisation only after explicit human approval and correction review.
    - kind: tool
      importance: required
      required: true
      applicationExternalId: alludium-platform
      toolExternalId: identity.archivePerson
      note: Archive a person only after explicit human approval and correction review.
    - kind: tool
      importance: required
      required: true
      applicationExternalId: alludium-platform
      toolExternalId: identity.captureSourceResult
      note: Capture approved source provenance with the platform-issued observation receipt.
    - kind: tool
      importance: required
      required: true
      applicationExternalId: alludium-platform
      toolExternalId: identity.correctSourceCapture
      note: Correct provenance only with an expected-receipt check and explicit approval.
    - kind: tool
      importance: required
      required: true
      applicationExternalId: alludium-platform
      toolExternalId: identity.createOrganisation
      note: Create an organisation only after explicit human approval and bounded evidence review.
    - kind: tool
      importance: required
      required: true
      applicationExternalId: alludium-platform
      toolExternalId: identity.createPerson
      note: Create a person only after explicit human approval and bounded evidence review.
    - kind: tool
      importance: required
      required: true
      applicationExternalId: alludium-platform
      toolExternalId: identity.endAffiliation
      note: End an affiliation only after explicit human approval and effective-date review.
    - kind: tool
      importance: required
      required: true
      applicationExternalId: alludium-platform
      toolExternalId: identity.linkProject
      note: Link an identity to the current project only after explicit approval and readback.
    - kind: tool
      importance: required
      required: true
      applicationExternalId: alludium-platform
      toolExternalId: identity.setFieldValue
      note: Set an intrinsic identity field only after the approved correction or update is clear.
    - kind: tool
      importance: required
      required: true
      applicationExternalId: alludium-platform
      toolExternalId: identity.unlinkProject
      note: Unlink a project only after explicit human approval and durable link readback.
    - kind: tool
      importance: required
      required: true
      applicationExternalId: alludium-platform
      toolExternalId: identity.updateOrganisation
      note: Update an organisation only after explicit human approval and provenance review.
    - kind: tool
      importance: required
      required: true
      applicationExternalId: alludium-platform
      toolExternalId: identity.updatePerson
      note: Update a person only after explicit human approval and provenance review.
  routingHints:
    preferredSurface: skill
    notes:
      - Use this in Deal Manager conversations for identity discovery, correction, affiliation, and Deal linking.
      - Keep identity records and relationship evidence separate from Deal-specific facts.
---

# People and Organisations Agent Readiness

Use this skill when a Deal conversation needs to identify, reuse, create, update,
or relate a Person or Organisation. Identity records are shared workspace data;
they are not login users, tenants, or substitutes for Deal fields.

## Discovery and proposals

1. Start with a read-only identity lookup using the strongest available evidence
   from the current Deal materials: stable source identifiers, domain, profile
   URL, email, name, role, and source context.
2. Present candidate records, the evidence supporting each candidate, conflicts,
   and any ambiguity in human-readable terms. Do not expose internal tool names,
   native UUIDs, or prescribed call sequences in the user-facing explanation.
3. Never treat a name, email domain, co-occurrence, model confidence, or a nearby
   instruction as proof of identity or employment. A person with no evidenced
   employer remains unlinked, and an ambiguous affiliation stays unresolved.
4. A review or proposal request is read-only. Do not create, reuse, correct,
   affiliate, link, unlink, or archive any identity record on that basis.

## Explicit execution

For a clear human request, execute only the exact identity action, record, fields,
affiliation, Deal link, or source capture that the human authorized. A direct exact
update request authorizes that update without a redundant ceremonial confirmation;
ambiguity, missing required values, unresolved candidates, and model-suggested
actions still require one focused question before mutation.

When the human approves a subset of candidates, act only on that subset. Do not
create every detected person, accept every proposed relationship, or silently
reuse an ambiguous record. Keep Person and Organisation intrinsic fields separate
from Deal-specific facts, and keep multiple legitimate Deal links independent.

## Provenance and correction

For accepted source captures and relationship actions, preserve the source system,
source object, source revision, project or workspace scope, visibility, and source
observation provenance returned by the identity operation. Keep the returned
record, capture, observation, affiliation, and project-link handles available for
later corrections and readback; do not replace them with display labels.

Treat a repeated source key with a new revision as a correction or new observation,
not as a new record. A replay must not restore a relationship that a human explicitly
removed. Report what was reused, what changed, and what remains unresolved. Never
claim a mutation from a proposed action or tool intent alone; verify the resulting
record and relationship state before reporting completion.

## Scope boundary

This skill does not perform automatic matching, backfill historical Deals, create
custom relationship fields, or introduce new CRM screens. Authentication,
workspace visibility, project scope, and repository permissions remain authoritative.
