---
id: deal-terms-analysis
name: Deal Terms Analysis
description: >
  Analyze VC commercial deal terms across valuation, round size, ownership,
  dilution, ESOP, co-investors, and follow-on reserve implications. Use this
  skill when turning proposed terms and cap table evidence into a source-grounded
  economics review for IC or term-sheet negotiation. It is commercial analysis
  only, not legal advice or term approval.
tags:
  - vc
  - deal-terms
  - valuation
  - ownership
  - cap-table
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: recommended
      required: false
      note: Deal terms analysis is strongest with a cap table, proposed financing terms, financial forecast, reserve policy, and prior IC constraints.
      gracefulDegradation: Produce a gap-aware terms review from provided materials only.
    - kind: setup
      importance: recommended
      required: false
      owner: user
      ownerPath: Provide proposed amount, valuation, round size, cap table, ownership target, ESOP, and reserve policy before claiming economics readiness.
      confirmationRequired: true
      gracefulDegradation: Do not claim ownership, dilution, or reserve confidence.
  routingHints:
    preferredSurface: skill
    notes:
      - Use this for commercial economics and investor tradeoff analysis; legal interpretation and final term approval remain outside the skill.
---

# Deal Terms Analysis

Frame proposed VC terms as an evidence-backed commercial review.

## Minimum Inputs

- proposed investment amount
- valuation and instrument context
- round size
- cap table artifact
- ownership target or reserve policy when available

## Process

1. Normalize the proposed financing terms and identify missing economics inputs.
2. Model ownership, dilution, ESOP expansion, and reserve implications only from supplied data.
3. Compare proposed terms to IC constraints, prior deal rationale, and current diligence evidence.
4. Identify open commercial terms that need investor, founder, or counsel review.
5. Prepare IC questions and negotiation inputs without approving or sending terms.

## Output Contract

Return:

- `ownership_model_summary`
- `valuation_sensitivity`
- `round_construction_notes`
- `esop_and_dilution_notes`
- `follow_on_reserve_implications`
- `open_commercial_terms`
- `ic_questions`
- `source_links`: cap table, term snapshot, forecast, IC materials, or source records used
- `assumptions`: assumptions behind valuation, dilution, ESOP, ownership, and reserve calculations
- `confidence_and_evidence_quality`: high/medium/low confidence by major conclusion, with reason
- `open_questions`: missing commercial, finance, legal, founder, or IC inputs
- `suggested_next_actions`: draft actions with owner/date suggestions and approval status
- `human_review_prompts`: judgments that require partner, IC, counsel, or finance review

## Tool Guidance

Use connected document repositories, CRM/deal systems, spreadsheet artifacts, and supplied cap table files when available. Public market or private financing comps can be used as context only when sourced and dated.

## Boundaries

- Do not provide legal advice.
- Do not negotiate terms or recommend legal positions.
- Do not approve valuation, ownership, ESOP, or reserve decisions.
- Do not send founder-facing terms or update CRM/stage data without explicit approval.
