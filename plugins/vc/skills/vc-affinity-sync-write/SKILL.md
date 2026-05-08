---
id: vc-affinity-sync-write
name: "VC Affinity Sync Write"
description: >
  Draft Affinity CRM write-back proposals for notes, fields, and stage-related
  recommendations, without performing external writes.
tags:
  - vc
  - affinity
  - crm
  - sync-write
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: recommended
      required: false
      note: Write-back proposals may reference `affinity_add_note` only if discovered, authorized, and explicitly approved by the runtime workflow.
      gracefulDegradation: Produce before/after proposals for human copy-and-apply review.
  routingHints:
    preferredSurface: skill
    notes:
      - This skill drafts proposals. It does not mutate Affinity.
---

# VC Affinity Sync Write

Use this skill to turn Alludium outputs into reviewable Affinity update proposals.

## Allowed Proposal Types

- Add an internal note summarizing approved screening, diligence, IC, or follow-up output
- Suggest field corrections for owner, stage, source/referrer, next meeting, or last activity
- Suggest stage movement with evidence and required human signoff
- Suggest next-step text that a human can approve before CRM entry

## Required Evidence

Every proposal must include:

- Affinity target object and URL or ID
- current value or current note state
- proposed value or note text
- source artifact, task output, meeting note, or human decision that supports it
- approval owner and audit note

## Tool Guidance

If the platform has discovered `affinity_add_note`, mention it as the possible approved execution tool for note creation. Do not use it from this skill unless the runtime workflow has explicit approval support and the user approves the exact note.

## Boundaries

- Do not change fields, stages, notes, owners, contacts, or list entries.
- Do not present a proposal as completed CRM work.
- Do not propose automated write-back without an approval model and audit trail.
