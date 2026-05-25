---
id: team-evaluation-and-founder-risk
name: Team Evaluation & Founder Risk
description: >
  Run lightweight team and founder evaluation before formal diligence, covering
  founder-market fit, role coverage, execution evidence, integrity signals,
  hiring gaps, adviser/board quality, and reference needs. Use this skill to
  form evidence-backed prompts for human judgment without implying completed
  references or background checks.
tags:
  - vc
  - evaluation
  - founders
  - team
  - risk
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: recommended
      required: false
      note: Team evaluation improves with founder bios, role history, call notes, public profiles, prior company evidence, relationship context, reference notes, hiring plan, and cap-table context.
      gracefulDegradation: Produce a facts/unknowns table and reference plan from supplied materials only.
    - kind: setup
      importance: recommended
      required: false
      owner: user
      ownerPath: Provide founder names, team materials, role history, meeting notes, public profiles, and any approved relationship or reference context.
      confirmationRequired: true
      gracefulDegradation: Avoid unsupported integrity, character, or capability conclusions.
  routingHints:
    preferredSurface: skill
    notes:
      - Use this before formal founder diligence to shape the next reference and team-risk questions.
---

# Team Evaluation & Founder Risk

Assess whether the team is credible enough to justify further work and what proof is needed next.

## Minimum Inputs

- founder names and company context
- prior investment screen or opportunity evaluation if available
- founder materials, team page, public profiles, or meeting notes
- role coverage, hiring plan, adviser, board, or reference context if available

## Process

1. Build a sourced founder and leadership fact table.
2. Assess founder-market fit and relevant execution evidence.
3. Identify role coverage, hiring gaps, and dependency risks.
4. Review adviser, board, relationship, and reference context where available.
5. Flag contradictions, unresolved claims, and human-only judgment questions.
6. State the main team thesis, gating risk, next proof needed, and decision impact.

## Output Contract

Return:

- `current_team_view`
- `main_team_hypothesis`
- `founder_fact_table`
- `founder_market_fit_view`
- `role_coverage_and_hiring_gaps`
- `reference_and_relationship_context`
- `evidence_reviewed`
- `company_or_founder_claims`
- `gating_team_risk`
- `next_proof_needed`
- `decision_impact`
- `source_links`
- `assumptions`
- `confidence_and_evidence_quality`
- `human_review_prompts`

## Tool Guidance

Use founder materials, public profiles, company websites, CRM relationship context,
meeting transcripts, reference notes, enrichment sources, and supplied investor notes.

## Boundaries

- Do not infer character from thin evidence.
- Do not present allegations as facts.
- Do not claim formal references or background checks unless authorized results are available.
- Do not contact references, founders, or third parties without explicit approval.
- Do not make the invest/pass decision.
