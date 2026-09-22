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
      importance: recommended
      required: false
      note: Identity lookup and mutation capabilities depend on the current project scope and the tools exposed by the Platform runtime.
      gracefulDegradation: Present a read-only proposal with evidence and ask the human to resolve missing or ambiguous identity context.
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
