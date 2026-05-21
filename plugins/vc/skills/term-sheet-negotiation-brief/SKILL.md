---
id: term-sheet-negotiation-brief
name: Term Sheet Negotiation Brief
description: >
  Organize term-sheet negotiation issues into open terms, give/get options,
  business tradeoffs, counsel questions, and approval points. Use this skill
  when preparing an internal negotiation brief from proposed terms, founder
  comments, counsel notes, and IC constraints. It does not negotiate, send terms,
  or approve legal language.
tags:
  - vc
  - term-sheet
  - negotiation
  - approvals
  - legal-review
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: recommended
      required: false
      note: Negotiation briefs are strongest with current term sheet, redlines/comments, deal terms analysis, counsel notes, and IC constraints.
      gracefulDegradation: Produce an internal issue list and missing-input map from provided materials only.
    - kind: setup
      importance: recommended
      required: false
      owner: user
      ownerPath: Provide the current term sheet, open terms, IC constraints, and counsel notes before treating the brief as ready for partner review.
      confirmationRequired: true
      gracefulDegradation: Do not label any term as approved or negotiated.
  routingHints:
    preferredSurface: skill
    notes:
      - Use this for internal business tradeoff framing and counsel escalation; legal drafting and negotiation authority stay with humans.
---

# Term Sheet Negotiation Brief

Turn open term-sheet issues into a reviewable internal brief.

## Minimum Inputs

- current term sheet
- open terms or founder comments
- IC constraints or approval conditions
- deal terms analysis when available
- counsel notes when available

## Process

1. Extract open terms and separate business, economics, governance, and legal drafting issues.
2. Summarize the business tradeoff for each issue using supplied evidence.
3. Prepare give/get options as internal scenarios, not recommendations to send.
4. Identify counsel questions and approval points.
5. Produce a readiness view for partner/human review before any external communication.

## Output Contract

Return:

- `open_terms_table`
- `give_get_options`
- `business_tradeoffs`
- `legal_escalations`
- `approval_required`
- `founder_or_counsel_comment_summary`
- `source_links`: term sheet versions, comments, counsel notes, IC decisions, or deal terms analysis used
- `assumptions`: assumptions behind issue severity, negotiation range, and approval status
- `confidence_and_evidence_quality`: high/medium/low confidence by major conclusion, with reason
- `open_questions`: unresolved business, counsel, finance, or partner questions
- `suggested_next_actions`: draft actions with owner/date suggestions and approval status
- `human_review_prompts`: items requiring partner, IC, counsel, or founder-facing approval

## Tool Guidance

Use document repositories, redline files, counsel notes, deal terms analysis, and Deal Room artifacts when available. Treat e-signature, document automation, and CRM systems as read/context surfaces unless a separate approved workflow handles mutations.

## Boundaries

- Do not negotiate with founders.
- Do not send terms or comments externally.
- Do not approve legal language.
- Do not present business tradeoffs as legal advice.
