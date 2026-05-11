---
id: vc-relationship-context-check
name: "VC Relationship Context Check"
description: >
  Check whether sourced companies are already known in Affinity or another CRM,
  preferring domain matches and rejecting unsupported name-only matches.
tags:
  - vc
  - origination
  - crm
  - relationship
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: recommended
      required: false
      applicationExternalId: affinity-mcp-server
      note: Use Affinity when authorized; otherwise work from supplied CRM exports or mark relationship context unknown.
      gracefulDegradation: Return a CRM-unavailable report and avoid known/unknown claims beyond supplied evidence.
  routingHints:
    preferredSurface: skill
---

# VC Relationship Context Check

Use this skill to avoid rediscovering companies already known to the firm.

## Lookup Order

1. Exact domain match from enrichment or company website.
2. Exact company LinkedIn URL or slug when available.
3. Company name fallback only when paired with additional evidence.

## Known Company Rule

Treat a company as known only when there is at least one credible signal:

- CRM list membership
- Notes
- Email or calendar interaction
- Owner assignment
- Pipeline/opportunity record
- Reliable domain or LinkedIn identity match

Reject a name-only match when it has no lists, notes, interactions, owners, or stable identity match.

## Output

Return matched-by, known/not-found/weak-match, CRM URL, list names, note count, interaction flags, owner flags, last activity if available, and evidence receipts.

## Boundaries

- Read-only.
- Do not create organizations, notes, list entries, or tasks.
- Do not mark outreach as completed.
