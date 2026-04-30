---
id: commercial-diligence-workstream
name: Commercial Diligence Workstream
description: >
  Run a VC commercial diligence workstream covering market size, customer evidence,
  competitive landscape, pricing, go-to-market, churn/concentration risk, and
  commercial red flags. Use this skill when turning market/customer materials into
  a source-grounded commercial DD summary and validation plan. It produces analysis
  and questions, not an investment decision.
tags:
  - vc
  - commercial-diligence
  - market
  - customers
  - gtm
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: recommended
      required: false
      note: Commercial diligence is strongest with customer evidence, sales pipeline data, pricing pages, market research, company enrichment, web search, website extraction, and private-market data when connected.
      gracefulDegradation: Produce a gap-aware commercial analysis from provided materials only.
    - kind: setup
      importance: recommended
      required: false
      owner: user
      ownerPath: Provide customer materials, pipeline evidence, pricing/GTM sources, or connected research/data sources before claiming validation.
      confirmationRequired: true
      gracefulDegradation: Label unverified market and customer claims clearly.
  routingHints:
    preferredSurface: skill
    notes:
      - Use this for commercial diligence analysis and validation planning; human investors own conclusions.
---

# Commercial Diligence Workstream

Assess whether the commercial case is credible, validated, and decision-ready.

## Minimum Inputs

- company and product context
- customer/reference evidence or sales pipeline context
- pricing or GTM materials
- market map or competitor list if available
- prior screening or traction outputs

## Process

1. Summarize the customer, buyer, use case, and urgency.
2. Validate TAM/SAM/SOM claims and methodology.
3. Review competitive landscape and differentiation.
4. Assess pricing, GTM motion, sales cycle, churn, concentration, and references.
5. Use sector trend/funding/M&A checks as dated market-delta inputs where useful.
6. Produce commercial risks, validation questions, and workstream signoff inputs.

## Output Contract

Return the domain sections plus the evidence fields needed for safe human review:

- `commercial_summary`
- `tam_sam_som_assessment`
- `competitive_landscape`
- `pricing_gtm_assessment`
- `customer_reference_plan`
- `reference_summaries`
- `churn_concentration_notes`
- `sector_delta`: dated funding, M&A, trend, or product-launch changes when relevant
- `commercial_risks`
- `open_questions`
- `source_links`: source document names, URLs, transcript names, or dataset records used
- `assumptions`: assumptions behind market size, GTM, pricing, churn, and customer conclusions
- `confidence_and_evidence_quality`: high/medium/low confidence by major conclusion, with reason
- `suggested_next_actions`: validation steps, owner suggestions, and required approvals
- `human_review_prompts`: investor-only judgments or external actions requiring approval

## Tool Guidance

Use Exa for research discovery, Firecrawl for first-party websites, Brave for broad
web/news fallback, and SerpAPI when Google/Maps/Scholar/Trends/SERP evidence matters.
Use connected private-market datasets such as Dealroom, Crunchbase, or PitchBook-like
sources only when connected; do not require them.

## Boundaries

- Do not fabricate market sizing or customer evidence.
- Do not overstate reference coverage.
- Do not treat a sector trend as proof of company-specific demand.
- Do not make the invest/pass decision.
