---
id: closing-coordination-and-cp-tracking
name: Closing Coordination & CP Tracking
description: >
  Coordinate VC closing workstreams, term-sheet review support, legal artifact
  intake, conditions precedent tracking, disclosure-letter review support, and
  closing readiness summaries. Use this skill when producing trackers, deviation
  tables, counsel questions, owner/due-date plans, or signing-readiness evidence
  maps. It is coordination and review support only, not legal advice or legal signoff.
tags:
  - vc
  - closing
  - term-sheet
  - legal-review
  - conditions-precedent
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: recommended
      required: false
      note: Closing coordination depends on term sheets, legal artifacts, counsel notes, CP checklists, CRM/project status, document repository context, and task ownership.
      gracefulDegradation: Produce a review-support checklist and missing-evidence map from provided documents only.
    - kind: setup
      importance: recommended
      required: false
      owner: user
      ownerPath: Provide legal/closing documents, counsel requirements, CP checklist, owners, and due dates before claiming readiness.
      confirmationRequired: true
      gracefulDegradation: Do not claim legal, CP, or signing readiness.
  routingHints:
    preferredSurface: skill
    notes:
      - Use this for coordination and counsel prompts; legal advice and final signoff remain outside the skill.
---

# Closing Coordination & CP Tracking

Keep closing work visible, sourced, and owner-assigned.

## Minimum Inputs

- term sheet or closing workplan
- legal document list or data-room/source documents
- CP checklist or counsel requirements
- owners, deadlines, and current blockers

## Process

Select the mode that matches the deal stage:

1. **Pre-close review mode** — summarize term-sheet status, surface deviations from
   supplied reference terms, model dilution only when cap table and round terms are
   supplied, and draft counsel/investor review questions.
2. **Active closing mode** — build owner/due-date and blocker tables, map CPs to
   evidence and missing items, and keep readiness caveats separate from legal signoff.
3. **Post-close handoff mode** — summarize closing outcomes, unresolved obligations,
   board/reporting expectations, and onboarding inputs for portfolio transition.

Across all modes, summarize legal or disclosure-letter artifacts only for
counsel/human review and never as legal advice.

## Output Contract

Return the relevant mode sections plus the evidence fields needed for safe human review:

- `term_summary`
- `deviation_table`
- `disclosure_or_legal_artifact_summary`
- `cp_tracker`
- `cp_evidence_mapping`
- `owner_due_date_table`
- `blockers`
- `dilution_scenarios`
- `counsel_review_questions`
- `signing_readiness_caveats`
- `source_links`: source document names, URLs, counsel notes, or tracker records used
- `assumptions`: assumptions behind dates, ownership, readiness, CP status, and dilution scenarios
- `confidence_and_evidence_quality`: high/medium/low confidence by major conclusion, with reason
- `open_questions`: legal, finance, counsel, founder, or internal questions that remain unanswered
- `suggested_next_actions`: draft actions with owner/date suggestions and approval status
- `human_review_prompts`: counsel-only, investor-only, or signoff-required judgments

## Tool Guidance

Use connected document repositories, CRM/deal systems, task systems, and provided
legal files when available. E-signature or legal-document systems are source/context
surfaces only unless a separate approved workflow handles mutations.

## Boundaries

- Do not provide legal advice.
- Do not negotiate terms or recommend legal positions.
- Do not claim CP satisfaction or signing readiness without counsel/human signoff.
- Do not create tasks, folders, shares, or CRM updates without approval.
