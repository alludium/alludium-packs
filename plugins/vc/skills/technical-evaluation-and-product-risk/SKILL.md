---
id: technical-evaluation-and-product-risk
name: Technical Evaluation & Product Risk
description: >
  Run lightweight technical and product evaluation before formal diligence,
  covering product depth, architecture plausibility, technical edge, data/IP
  defensibility, roadmap realism, technical team coverage, and proof gaps. Use
  this skill to shape decision-review inputs and diligence requests without
  implying completed technical diligence.
tags:
  - vc
  - evaluation
  - technical
  - product
  - ip
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: recommended
      required: false
      note: Technical evaluation improves with product demos, architecture notes, technical decks, repo or product evidence, IP/data descriptions, hiring context, and expert notes.
      gracefulDegradation: Produce a gap-aware technical view from provided materials only.
    - kind: setup
      importance: recommended
      required: false
      owner: user
      ownerPath: Provide product materials, demo notes, architecture claims, roadmap, technical team context, data/IP claims, and known product risks.
      confirmationRequired: true
      gracefulDegradation: Label unverified technical claims clearly.
  routingHints:
    preferredSurface: skill
    notes:
      - Use this for evaluation-stage technical triage, not code review, security review, or formal expert diligence.
---

# Technical Evaluation & Product Risk

Assess whether the product and technical story is credible enough to justify further work.

## Minimum Inputs

- company and product context
- prior investment screen or opportunity evaluation if available
- product demo notes, deck, website, or technical narrative
- architecture, roadmap, IP, data, or AI/ML claims if available
- technical team context if available

## Process

1. Summarize the product, workflow, and user value.
2. Assess product maturity, adoption evidence, and roadmap realism.
3. Pressure-test architecture and scalability claims at a lightweight level.
4. Review claimed technical edge, IP, data access, and defensibility.
5. Identify technical team coverage, dependency, and delivery risks.
6. State the main technical thesis, gating risk, next proof needed, and decision impact.

## Output Contract

Return:

- `current_technical_view`
- `main_technical_hypothesis`
- `product_depth_and_maturity`
- `architecture_and_scalability_view`
- `technical_edge_ip_or_data_view`
- `technical_team_coverage`
- `evidence_reviewed`
- `company_claims`
- `gating_technical_risk`
- `next_proof_needed`
- `decision_impact`
- `source_links`
- `assumptions`
- `confidence_and_evidence_quality`
- `human_review_prompts`

## Tool Guidance

Use company materials, product websites, demo notes, technical decks, public repos,
patent or IP sources, hiring signals, and expert notes where connected or supplied.

## Boundaries

- Do not imply code review, security review, expert validation, or IP clearance unless those inputs were actually reviewed.
- Do not equate a demo with production readiness.
- Do not overstate AI/ML, data, or defensibility claims without evidence.
- Do not make the invest/pass decision.
