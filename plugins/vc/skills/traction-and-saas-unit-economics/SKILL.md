---
id: traction-and-saas-unit-economics
name: "Traction & SaaS Unit Economics"
description: >
  Extract, normalise, and benchmark SaaS traction metrics from founder materials,
  data rooms, and external sources. Use this skill when evaluating a company's
  revenue quality, unit economics, and growth trajectory during screening or
  diligence — turning messy or incomplete founder data into a structured KPI table,
  Revenue Quality Scorecard, and stage assessment. Handles partial data gracefully
  and flags metric hygiene issues explicitly.
tags:
  - vc
  - saas
  - traction
  - unit-economics
  - metrics
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: recommended
      required: false
      note: Traction analysis requires quantitative founder materials, data-room files, financial models, or reliable metric sources. Provider-specific tool IDs are intentionally omitted because metric evidence may come from several configured surfaces.
      gracefulDegradation: Extract only provided metrics and flag missing periods, definitions, currencies, or benchmark context.
    - kind: setup
      importance: recommended
      required: false
      owner: user
      ownerPath: Attach KPI sheets, financial models, data-room files, or route source access through owned setup paths before analysis.
      confirmationRequired: true
      gracefulDegradation: Return a missing-metrics request and avoid derived conclusions from thin data.
  routingHints:
    preferredSurface: skill
    notes:
      - This skill analyzes and benchmarks metrics; it does not alter financial records or system-of-record data.
---

# Traction & SaaS Unit Economics

Extract, normalise, and benchmark SaaS traction metrics to produce a structured
assessment of a company's revenue quality and unit economics health.

This skill is for metric extraction and benchmarking — not for full diligence pack
assembly, competitive analysis, or team evaluation.

Important: the canonical starting artifact is the raw traction worksheet. The KPI
table is the core output. Benchmarking, scoring, and SaaS-specific interpretation sit
on top of that worksheet rather than replacing it.

## Minimum Inputs

Before running, confirm there is enough quantitative material to work with:

- A pitch deck with a traction or metrics slide, or
- A KPI sheet / financial model / data room financials, or
- Call notes or transcript containing specific numbers

If no quantitative material exists, stop and recommend running the Missing Info
Request Drafter or asking the founder for a metrics snapshot.

## Core Method

1. Confirm minimum input exists.
2. Build the raw traction worksheet from all available sources.
3. Normalise units, time periods, and currencies.
4. Calculate derived metrics where inputs allow.
5. Benchmark each metric against stage- and segment-appropriate thresholds.
6. Score the Revenue Quality Scorecard.
7. Run a projections-vs-actuals realism check when both exist.
8. Assess company stage and produce the output.

## Step 1 — Metric Extraction

This step produces the canonical worksheet. Preserve it even if later analysis is thin.

Scan all founder materials for quantitative data. For each metric found, capture:

| Field       | Required      | Notes                                      |
| ----------- | ------------- | ------------------------------------------ |
| Metric name | Yes           | Use canonical names (MRR, ARR, NRR, etc.)  |
| Value       | Yes           | Exact number as stated                     |
| Unit        | Yes           | Currency (GBP/USD/EUR), %, count, months   |
| Time period | Yes           | Month, quarter, or year — never omit       |
| Source      | Yes           | Slide number, page, filename, timestamp    |
| Definition  | If ambiguous  | How did the founder calculate this?        |
| Caveats     | If applicable | One-off revenue included? Pilot customers? |

**Where to look:**

- Pitch deck: traction slides, financial projections, appendix
- Data room: P&L, MRR waterfall, cohort tables, customer list
- Financial model: assumptions tab, monthly MRR build, unit economics tab
- Call notes / transcripts: verbal claims about growth, churn, customers

**Extraction rules:**

- Preserve the founder's exact numbers and units — do not convert or round during extraction.
- If a metric is stated qualitatively ("growing fast", "low churn") with no number, record as **Qualitative only** and flag for follow-up.
- If numbers conflict across sources (deck says one ARR, model says another), record both with citations and flag as **Inconsistency**.
- If a time period is missing, flag as **Period unknown** — never assume monthly vs annual.

## Step 2 — Normalisation

After extraction, normalise all metrics to a common basis:

- **Currency**: Convert to the company's primary operating currency. State the FX rate and date used.
- **Time period**: Standardise to monthly for MRR/churn/growth, annual for ARR/NRR/Rule of 40.
- **Annualisation**: Only annualise MRR to ARR if there are at least 3 months of stable data. If annualising from fewer months, label as **Projected ARR** and flag the assumption.
- **Derived metrics**: Only compute if the required inputs are present. Mark every derived value clearly as **Derived** with the formula used.

## Step 3 — Core SaaS Metric Formulas

Use the following formulas. If a required input is missing, do not estimate — leave the metric blank and add it to the Missing KPIs list.

### Revenue Metrics

**ARR** = MRR x 12

- Only valid if MRR is relatively stable month-over-month. If MRR is volatile, report the trailing 3-month average x 12 and flag it.

**MoM MRR Growth** = (MRR_current - MRR_prior) / MRR_prior x 100

- Requires at least 2 consecutive months. Report as percentage.

**MRR Waterfall** = Beginning MRR + New MRR + Expansion MRR - Contraction MRR - Churned MRR = Ending MRR

- If the founder provides a waterfall, extract each component. If only beginning and ending MRR are available, note that the breakdown is missing.

### Retention Metrics

**Monthly Gross Churn Rate** = Churned MRR / Beginning MRR x 100

- Must be calculated on MRR, not logo count, unless MRR data is unavailable.

**Net Revenue Retention (NRR)** = (Beginning MRR + Expansion - Contraction - Churn) / Beginning MRR x 100

- Annual NRR is the standard. If only monthly components are available, compound: NRR_annual = (1 + (NRR_monthly - 1))^12

**Logo Retention** = (Customers_start - Customers_churned) / Customers_start x 100

- Secondary to NRR but useful when NRR is unavailable.

### Unit Economics

**CAC** = Total Sales & Marketing Spend / New Customers Acquired (in same period)

- Specify whether fully loaded (includes salaries, tools, overhead) or direct only. Founders often report direct-only — flag this.

**LTV** = ARPA x Gross Margin % / Monthly Churn Rate

- Where ARPA = Average Revenue Per Account (monthly). If gross margin is unknown, use revenue-based LTV and flag: "Assumes 100% gross margin."

**LTV:CAC Ratio** = LTV / CAC

- The single most important unit economics metric. See benchmarks below.

**CAC Payback Period** = CAC / (ARPA x Gross Margin %)

- Result is in months. If gross margin is unknown, report revenue-based payback and flag.

### Growth Efficiency

**Rule of 40** = Revenue Growth Rate % + Free Cash Flow Margin %

- Use YoY ARR growth for revenue growth. If FCF margin is unavailable, use EBITDA margin as a proxy and flag.
- At pre-seed/seed, growth rate alone often exceeds 40; the Rule of 40 becomes more meaningful at Series A+.

**Burn Multiple** = Net Burn / Net New ARR

- Lower is better. <1x is excellent, 1-2x is good, >3x is concerning.

**Quick Ratio** = (New MRR + Expansion MRR) / (Contraction MRR + Churned MRR)

- Requires MRR waterfall components. >4 is strong, 2-4 is healthy, <1 is contracting.

## Step 4 — Benchmarking

Benchmark each calculated metric against the appropriate stage and segment. See
`references/saas-benchmarks.md` for the full benchmark tables.

**Determine company stage:**

- **Early** (Pre-seed/Seed): <$1M ARR, <50 customers, product-market fit search
- **Growth** (Series A/B): $1M-$20M ARR, scaling GTM, repeatable sales
- **Scale** (Series C+): $20M-$100M ARR, optimising efficiency, expanding TAM
- **Late** (Pre-IPO): >$100M ARR, profitability focus, IPO readiness

**Determine customer segment:**

- **Enterprise**: ACV >$100K, long sales cycles (6-12+ months), <100 customers typical
- **Mid-Market**: ACV $10K-$100K, 3-6 month sales cycles
- **SMB**: ACV $1K-$10K, 1-3 month sales cycles, higher volume
- **PLG (Product-Led Growth)**: ACV <$1K, self-serve, very high volume, lowest touch

For each metric, assign a health status: **HEALTHY**, **WATCH**, or **CRITICAL**
based on the benchmark table for the company's stage and segment.

## Step 5 — Revenue Quality Scorecard

Score each dimension 1-5. The scorecard assesses revenue quality holistically, beyond
individual metric benchmarks.

| #   | Dimension              | 1 (Weak)                              | 3 (Adequate)                 | 5 (Strong)                              |
| --- | ---------------------- | ------------------------------------- | ---------------------------- | --------------------------------------- |
| 1   | Recurring %            | <50% of revenue is recurring          | 70-80% recurring             | >90% recurring, contractual             |
| 2   | Net Revenue Retention  | NRR <80%                              | NRR 100-110%                 | NRR >120%, strong expansion             |
| 3   | Customer Concentration | Top customer >40% of revenue          | Top customer 15-25%          | No customer >10%, healthy distribution  |
| 4   | Cohort Stability       | Cohorts degrade rapidly after month 3 | Cohorts stabilise by month 6 | Cohorts flat or expanding after month 6 |
| 5   | Growth Durability      | Growth decelerating >10pp QoQ         | Growth decelerating <5pp QoQ | Growth stable or accelerating           |
| 6   | Margin Profile         | Gross margin <50%                     | Gross margin 65-75%          | Gross margin >80%, expanding            |

**Scoring rules:**

- Score based on evidence only. No evidence for a dimension = N/A, not a guess.
- Half-scores (e.g., 3.5) are acceptable when evidence is mixed.
- A company can have strong individual metrics but weak revenue quality (e.g., high NRR driven by one whale account = good NRR score but poor concentration score).

**Revenue Quality Rating:**

- 25-30: Strong — high-quality, durable revenue base
- 18-24: Adequate — typical for stage, some areas need attention
- 12-17: Watch — material revenue quality risks
- 6-11: Critical — revenue foundation is fragile

## Step 6 — Handling Missing Data

Missing data is the norm, not the exception. Handle it explicitly:

**What to do when data is missing:**

1. Record the missing metric in the **Missing KPIs** section with why it matters.
2. Estimate impact on the assessment: "Without cohort data, we cannot validate the stated NRR figure."
3. Generate a specific follow-up question: "Can you share the monthly MRR waterfall for the last 12 months, broken down by new, expansion, contraction, and churn?"
4. Assign a **Data Completeness** grade to the overall submission:
   - **A**: 80%+ of core metrics available with sources — full assessment possible
   - **B**: 50-80% available — assessment possible with caveats
   - **C**: 25-50% available — partial assessment only, material gaps
   - **D**: <25% available — cannot produce a meaningful assessment, request more data

**Common founder data patterns and how to handle them:**

- **Only total revenue, no MRR breakdown**: Calculate implied MRR if revenue is subscription-based. Flag that recurring vs non-recurring split is unknown.
- **Logos but no revenue per customer**: Can calculate logo retention but not NRR. Flag unit economics as unassessable.
- **Only annual figures**: Cannot assess monthly trends or MoM growth. Note that intra-year dynamics are invisible.
- **Vanity metrics only** (downloads, signups, page views): Flag that no revenue or retention metrics are present. These are activity metrics, not traction metrics.
- **Projected figures mixed with actuals**: Separate actuals from projections. Only benchmark actuals. Note projections in a separate section.

## Step 7 — Projection Realism Check

If both historical actuals and founder projections exist, compare them explicitly.

- Check whether projected growth materially exceeds recent actual growth
- Check whether projected margin improvement assumes changes not evidenced anywhere else
- Check whether projected burn or runway ignores the current hiring plan

If the model projects far better performance than recent actuals support, flag it as a
realism issue rather than silently blending projections into the assessment.

## Step 8 — Stage Assessment

Based on the metrics, benchmarks, and scorecard, produce a stage assessment:

1. **Does the data support the stage the founder claims?** (e.g., founder says "Series A ready" but ARR is $200K with no NRR data — flag the mismatch)
2. **What is the metrics-based stage?** Using the stage definitions from Step 4.
3. **What are the standout strengths?** (metrics that benchmark as HEALTHY or above for the claimed stage)
4. **What are the critical gaps?** (metrics that benchmark as CRITICAL or are missing entirely)
5. **What would change the assessment?** (the 2-3 data points that would most improve confidence)

## Output Shape

```
# Traction & Unit Economics: [Company Name]

## Data Completeness: [A/B/C/D]
Sources reviewed: [list of materials with dates]

## KPI Table

| Metric | Value | Period | Unit | Source | Benchmark | Status |
|--------|-------|--------|------|--------|-----------|--------|
| ARR | X | YYYY | USD | Deck p.X | $1-3M (Early) | HEALTHY |
| MoM Growth | X% | MMM-YY | % | Model | 10-20% (Early) | WATCH |
| Monthly Churn | X% | MMM-YY | % | KPI sheet | <3% (SMB) | CRITICAL |
| CAC | $X | Q | USD | Model | — | — |
| LTV | $X | — | USD | Derived | — | — |
| LTV:CAC | X:1 | — | ratio | Derived | 3:1-5:1 | HEALTHY |
| CAC Payback | X mo | — | months | Derived | <18 mo | WATCH |
| NRR | X% | annual | % | Founder claim | >100% | — |
| Rule of 40 | X | annual | score | Derived | >40 | — |
| Burn Multiple | X | annual | ratio | Derived | <2x | — |

## Top Signals
- [Strongest traction signal]
- [Second strongest traction signal]
- [Third strongest traction signal]
- [Fourth strongest traction signal]
- [Fifth strongest traction signal]

## Revenue Quality Scorecard

| # | Dimension | Score | Evidence |
|---|-----------|-------|----------|
| 1 | Recurring % | X/5 | [brief evidence] |
| 2 | Net Revenue Retention | X/5 | [brief evidence] |
| 3 | Customer Concentration | X/5 | [brief evidence] |
| 4 | Cohort Stability | X/5 | [brief evidence] |
| 5 | Growth Durability | X/5 | [brief evidence] |
| 6 | Margin Profile | X/5 | [brief evidence] |

**Revenue Quality Rating: X/30 — [Strong/Adequate/Watch/Critical]**

## Stage Assessment
- **Founder-claimed stage**: [what they say]
- **Metrics-based stage**: [what the data says]
- **Standout strengths**: [1-3 bullets]
- **Critical gaps**: [1-3 bullets]

## Missing KPIs
| Metric | Why It Matters | Follow-Up Question |
|--------|---------------|-------------------|
| [metric] | [impact on assessment] | [specific question for founder] |

## Top Unknowns
1. [Highest-impact missing metric or unresolved inconsistency]
2. ...

## Projection Realism
[Only include when projections exist — compare the model to historical actuals and call out
where the assumptions look supported vs stretched]

## Return Scenario Inputs
[If ownership, valuation, dilution, exit, IRR, or MOIC assumptions are present, extract
them with sources and flag gaps for the financial diligence or IC memo workflow. Do not
invent return scenarios from traction data alone.]

## Inconsistencies & Flags
[Any conflicting numbers, vanity metrics, missing definitions, or hygiene issues]

## Top 5 Follow-Up Questions
1. [Ordered by decision impact]
2. ...
```

## Tool Guidance

Use tools to validate and enrich founder-provided metrics. Do not ask the user for
information that tools can provide.

| Tool            | When to Use                                                                                                                |
| --------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Exa             | Validate claimed market size, find comparable company benchmarks, and gather recent category context for stage calibration |
| Brave / SerpAPI | Public-search fallback for benchmark triangulation, market context, and recent public signals                              |
| Harmonic        | Company growth signals, headcount context, founder/team enrichment, and benchmark comparables when connected               |
| Dealroom        | Company funding history and financing milestones when connected                                                            |
| Firecrawl       | Pricing pages (to validate ACV claims), product pages (to assess PLG signals)                                              |

If an existing Company Research & Enrichment profile exists, cross-reference any
revenue or growth claims against it.
If Dealroom is unavailable, use Affinity-enriched funding fields when present. If
neither source is available, mark financing-stage calibration as a gap.

## Guardrails

- **No unit ambiguity**: Every extracted number must have a unit and time period. If the source omits them, flag it — do not assume.
- **No fabricated metrics**: If you cannot calculate a metric from the available data, leave it blank. Never estimate or interpolate unless the methodology is explicitly stated and flagged.
- **Actuals vs projections**: Keep these in separate sections. Never benchmark projections against actual-based benchmarks without flagging.
- **Source everything**: Every number in the KPI table must have a source pointer (slide, page, filename, timestamp). Derived metrics must show the formula.
- **Do not over-benchmark early-stage**: Pre-seed companies with 3 months of data should not be judged against Scale-stage benchmarks. Always match stage.
- **Vanity metric discipline**: Downloads, signups, MAU without retention/revenue are activity metrics. Acknowledge them but do not treat them as traction.
- **Founder-friendly framing**: Flag issues clearly but avoid accusatory language. "The stated NRR of 140% cannot be validated without cohort data" is better than "The NRR claim is suspicious."

## Cohort Analysis

When cohort data is available (monthly MRR by customer cohort), perform:

1. **Retention curve**: Plot MRR retention by cohort month (Month 0 = 100%). Look for:

   - Stabilisation point (where the curve flattens)
   - Whether recent cohorts perform better or worse than older ones
   - Any cohort that deviates significantly (positive or negative)

2. **Dollar retention by cohort**: Does each cohort grow over time (expansion > churn)?

   - Cohorts that expand = strong NRR signal
   - Cohorts that decay = churn problem even if aggregate NRR looks healthy (new cohort effect)

3. **Cohort size trend**: Are newer cohorts larger (healthy growth) or smaller (demand exhaustion)?

If cohort data is not available, note this as a material gap and recommend requesting
it as a priority follow-up.

## Related Skills

This skill works well with:

- `company-research-and-enrichment` — foundation data, validates claimed revenue/funding
- `ten-factor-evaluation` — this skill feeds Factor 4 (Business Model) and Factor 6 (Value Creation)
- `red-flags-scanner` — flags metric inconsistencies, vanity metrics, unrealistic projections
