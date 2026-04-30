---
id: financial-diligence-workstream
name: Financial Diligence Workstream
description: >
  Run a VC financial diligence workstream covering historicals, burn/runway,
  cap table, unit economics, forecasts, use of funds, valuation assumptions, IRR
  or MOIC scenarios, and dilution sensitivities. Use this skill when producing
  a source-grounded financial DD summary or scenario pack. It does not provide
  audit assurance, valuation certainty, or an investment decision.
tags:
  - vc
  - financial-diligence
  - metrics
  - cap-table
  - scenarios
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: recommended
      required: false
      note: Financial diligence depends on financial statements, KPI sheets, forecast models, cap tables, bank evidence, use-of-funds materials, and optional CRM/private-market context.
      gracefulDegradation: Produce missing-metrics requests and assumption checks only.
    - kind: setup
      importance: recommended
      required: false
      owner: user
      ownerPath: Provide financial models, KPI exports, cap table, bank evidence, and relevant assumptions before scenario analysis.
      confirmationRequired: true
      gracefulDegradation: Do not infer missing metrics or scenario outputs.
  routingHints:
    preferredSurface: skill
    notes:
      - Use this for financial analysis and scenario support; humans own valuation, audit, and investment conclusions.
---

# Financial Diligence Workstream

Turn financial materials into a structured diligence view with explicit assumptions.

## Minimum Inputs

- financial statements or management accounts
- KPI/traction exports
- forecast model
- cap table or round terms
- bank evidence or use-of-funds plan when relevant

## Process

1. Extract historicals, burn, runway, revenue quality, and unit economics.
2. Compare actuals to forecasts and flag model hygiene issues.
3. Summarize cap table and ownership assumptions.
4. Build assumption-led valuation, ownership, dilution, IRR, or MOIC scenarios only when inputs support them.
5. Benchmark founder compensation only when compensation data and a credible comparable basis exist.
6. Identify risks, missing evidence, and questions for finance/legal review.

## Output Contract

Return the domain sections plus the evidence fields needed for safe human review:

- `historicals_summary`
- `burn_runway_analysis`
- `cap_table_summary`
- `unit_economics`
- `forecast_stress_test`
- `valuation_scenarios`
- `irr_moic_scenarios`
- `dilution_scenarios`
- `founder_compensation_benchmarks`
- `use_of_funds_assessment`
- `financial_risks`
- `missing_inputs`
- `source_links`: source document names, sheets, exports, URLs, or dataset records used
- `assumptions`: assumptions behind forecasts, valuation, ownership, dilution, IRR/MOIC, and compensation benchmarks
- `confidence_and_evidence_quality`: high/medium/low confidence by major conclusion, with reason
- `open_questions`: finance/legal/investment questions that remain unanswered
- `suggested_next_actions`: validation steps, owner suggestions, and required approvals
- `human_review_prompts`: investor-only, finance-only, legal-only, or counsel-only judgments

## Tool Guidance

Use provided financial files first. Use CRM/deal-system funding context and connected
private-market datasets such as Dealroom, Crunchbase, or PitchBook-like sources only
when connected. Use Harmonic when connected for company stage, headcount, and growth
context that may affect compensation or benchmark interpretation. Use Firecrawl for
pricing pages and Exa, Brave, or SerpAPI for market or comparable context where useful.

## Boundaries

- Do not invent metrics, assumptions, or round terms.
- Do not imply audit assurance or valuation certainty.
- Do not benchmark projections as if they were actuals.
- Do not benchmark founder compensation without stating stage, geography, role, runway,
  and source limitations.
- Do not make a final investment recommendation.
