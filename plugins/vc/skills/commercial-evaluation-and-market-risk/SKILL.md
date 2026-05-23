---
id: commercial-evaluation-and-market-risk
name: Commercial Evaluation & Market Risk
description: >
  Run lightweight commercial evaluation before formal diligence, covering customer
  segment, pain urgency, GTM path, pricing, competition, market size, and the main
  commercial risk. Use this skill when the goal is to decide what proof is needed
  next, not to claim completed commercial diligence.
tags:
  - vc
  - evaluation
  - commercial
  - market
  - gtm
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: recommended
      required: false
      note: Commercial evaluation improves with founder materials, call notes, customer or pipeline snippets, pricing context, competitor evidence, and public market research.
      gracefulDegradation: Produce a gap-aware commercial view from provided materials only.
    - kind: setup
      importance: recommended
      required: false
      owner: user
      ownerPath: Provide the deck, screen, call notes, customer evidence, pipeline context, pricing notes, or market sources available at evaluation stage.
      confirmationRequired: true
      gracefulDegradation: Label unverified customer, pricing, and market claims clearly.
  routingHints:
    preferredSurface: skill
    notes:
      - Use this before formal diligence to shape the next proof request and decision-review inputs.
---

# Commercial Evaluation & Market Risk

Assess whether the commercial case is attractive enough to justify further work.

## Minimum Inputs

- company and product context
- prior investment screen or opportunity evaluation if available
- founder materials, website, or call notes
- customer, pipeline, pricing, or GTM evidence if available
- competitor or market sources if available

## Process

1. Identify the narrow first customer segment and buyer.
2. Assess pain urgency, budget, and adoption path.
3. Review pricing, GTM motion, sales cycle, and channel assumptions.
4. Map direct competitors, substitutes, and incumbent alternatives.
5. Pressure-test market sizing logic at a lightweight level.
6. State the main commercial thesis, gating risk, next proof needed, and decision impact.

## Output Contract

Return:

- `current_commercial_view`
- `main_commercial_hypothesis`
- `customer_segment_and_urgency`
- `pricing_and_gtm_view`
- `competition_and_market_view`
- `evidence_reviewed`
- `company_claims`
- `gating_commercial_risk`
- `next_proof_needed`
- `decision_impact`
- `source_links`
- `assumptions`
- `confidence_and_evidence_quality`
- `human_review_prompts`

## Tool Guidance

Use company materials, CRM/deal context, public web research, first-party websites,
market databases, and customer or pipeline snippets where connected or supplied.
Do not require formal customer references at evaluation stage.

## Boundaries

- Do not claim customer validation without direct customer, usage, contract, or equivalent evidence.
- Do not treat market growth as proof of company-specific demand.
- Do not fabricate TAM/SAM/SOM assumptions.
- Do not make the invest/pass decision.
