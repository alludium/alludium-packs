---
id: founder-materials-request
name: Founder Materials Request
description: >
  Turn known diligence gaps into a founder-facing materials request and internal
  checklist. Use this skill when a VC workflow needs missing decks, KPI sheets,
  financial models, customer references, technical documents, legal artifacts, or
  clarifying answers. Outputs are drafts and checklists only; the skill never sends
  messages or updates external systems by itself.
tags:
  - vc
  - founder
  - diligence
  - materials-request
  - communications
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: recommended
      required: false
      note: Founder materials requests are strongest with prior task outputs, source gaps, CRM/contact context, and email history. Provider-specific tool IDs are intentionally omitted because those sources may come through several configured surfaces.
      gracefulDegradation: Draft from the missing-information list supplied by the user or prior task.
    - kind: setup
      importance: recommended
      required: false
      owner: user
      ownerPath: Provide the missing-materials list, founder contact, and communication context before creating a founder-facing draft.
      confirmationRequired: true
      gracefulDegradation: Produce an internal checklist only.
  routingHints:
    preferredSurface: skill
    notes:
      - External communications are drafts for review and require explicit approval to send.
---

# Founder Materials Request

Convert diligence gaps into a clear, founder-friendly request.

## Minimum Inputs

- company name
- missing materials or open questions
- stage or reason for the request
- founder/contact context if drafting external copy
- deadline or urgency if known

## Process

1. Deduplicate and group missing items by theme.
2. Separate must-have items from helpful context.
3. Translate internal diligence language into founder-friendly wording.
4. Draft the external request and internal tracker.
5. Include why each item matters, without exposing internal conviction or sensitive debate.

## Output Contract

Return:

- `materials_request_checklist`: item, reason needed, priority, owner, due date
- `draft_external_message`: email or message draft ready for human review
- `internal_notes`: sensitive rationale that should not be sent externally
- `share_instructions`: suggested file/folder/link instructions when relevant
- `approval_required`: send, CRM update, task creation, or folder/share change

## Tool Guidance

Use CRM/deal-system contact context, email history, prior task outputs, attached files,
and document repository context when available. Gmail, Outlook, Slack, or LinkedIn
may provide context or a draft channel, but sending is always approval-gated.

## Boundaries

- Do not send messages.
- Do not create folders, share links, or update CRM/task systems without approval.
- Do not request sensitive legal, financial, or personal material without clear purpose.
- Do not disclose internal concerns, scores, or conviction levels in founder-facing copy.
