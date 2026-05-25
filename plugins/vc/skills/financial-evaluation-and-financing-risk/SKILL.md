---
id: financial-evaluation-and-financing-risk
name: Financial Evaluation & Financing Risk
description: >
  Run lightweight financial evaluation before formal diligence, covering forecast
  plausibility, burn, runway, use of funds, valuation, ownership, financing path,
  and return sensitivity. Use this skill to identify decision-critical finance
  questions without presenting a verified financial diligence report.
tags:
  - vc
  - evaluation
  - financial
  - financing
  - valuation
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: recommended
      required: false
      note: Financial evaluation improves with model extracts, historical financials, cap table context, fundraising plan, pricing/usage evidence, and comparable financing data.
      gracefulDegradation: Produce a gap-aware financial view from provided materials only.
    - kind: setup
      importance: recommended
      required: false
      owner: user
      ownerPath: Provide the deck, initial model, use-of-funds narrative, valuation/cap-table context, burn/runway data, and revenue or usage evidence available at evaluation stage.
      confirmationRequired: true
      gracefulDegradation: Label unverified model, valuation, and ownership assumptions clearly.
  routingHints:
    preferredSurface: skill
    notes:
      - Use this before formal financial diligence to shape the next model, cap-table, and financing questions.
---

# Financial Evaluation & Financing Risk

Assess whether the financing and economics story is plausible enough to justify further work.

## Minimum Inputs

- company and financing context
- prior investment screen or opportunity evaluation if available
- deck, model extract, or financial narrative if available
- current round, valuation, ownership, burn, and runway context if available
- revenue, usage, pipeline, pricing, or unit-economics evidence if available

## Process

1. Summarize the business model and financing ask.
2. Assess forecast plausibility, revenue quality, and assumption sensitivity.
3. Review burn, runway, use of funds, and milestone coverage.
4. Pressure-test valuation, ownership, and return sensitivity.
5. Identify financing path, next-round readiness, and downside risks.
6. State the main financial thesis, gating risk, next proof needed, and decision impact.

## Output Contract

Return:

- `current_financial_view`
- `main_financial_hypothesis`
- `forecast_and_revenue_quality_view`
- `burn_runway_and_use_of_funds_view`
- `valuation_ownership_and_return_view`
- `financing_path_view`
- `evidence_reviewed`
- `company_claims`
- `gating_financial_risk`
- `next_proof_needed`
- `decision_impact`
- `source_links`
- `assumptions`
- `confidence_and_evidence_quality`
- `human_review_prompts`

## Tool Guidance

Use provided models, founder materials, CRM/deal context, market data, comparable
financing references, and public sources where connected or supplied.

## Boundaries

- Do not treat forecasts as verified unless source data has been reviewed.
- Do not produce tax, accounting, or legal advice.
- Do not claim cap-table or ownership certainty without the source cap table.
- Do not make the invest/pass decision.
