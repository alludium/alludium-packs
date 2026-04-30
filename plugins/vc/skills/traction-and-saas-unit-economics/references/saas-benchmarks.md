# SaaS Benchmark Tables

Reference benchmarks for SaaS metrics by company stage and customer segment.
Sources: OpenView Partners, Bessemer Venture Partners, SaaS Capital, Paddle.

---

## Monthly Churn Rate

| Segment    | HEALTHY | WATCH | CRITICAL |
| ---------- | ------- | ----- | -------- |
| Enterprise | <1%     | 1-2%  | >3%      |
| Mid-Market | <2%     | 2-4%  | >5%      |
| SMB        | <4%     | 4-6%  | >8%      |
| PLG        | <5%     | 5-8%  | >10%     |

**Notes**: Enterprise churn should be very low due to long contracts and high switching
costs. PLG naturally has higher churn due to low-touch, low-ACV customers. Monthly
churn of 5% = ~46% annual churn — not sustainable at any stage.

---

## LTV:CAC Ratio

| Rating   | Value     | Interpretation                          |
| -------- | --------- | --------------------------------------- |
| CRITICAL | <1:1      | Losing money on every customer acquired |
| WATCH    | 1:1 - 2:1 | Marginal economics, fragile             |
| HEALTHY  | 3:1 - 5:1 | Standard target range                   |
| STRONG   | 5:1 - 8:1 | Efficient acquisition                   |
| FLAG     | >8:1      | Possibly under-investing in growth      |

**Stage nuance**: Early-stage companies with LTV:CAC >8:1 may be under-spending on
sales and marketing. This is a positive problem but should trigger a question about
GTM investment plans. At Scale stage, >8:1 may indicate a mature, efficient engine.

---

## CAC Payback Period (months)

| Rating    | Months | Notes                                          |
| --------- | ------ | ---------------------------------------------- |
| EXCELLENT | <6     | Rare; typical of strong PLG or viral loops     |
| HEALTHY   | 6-18   | Standard range for most SaaS                   |
| WATCH     | 18-24  | Acceptable for Enterprise with high ACV        |
| CRITICAL  | >24    | Cash-intensive; needs strong NRR to compensate |

**Segment adjustment**: Enterprise SaaS with ACV >$100K can tolerate 18-24 month
payback if NRR is >120% (expansion revenue compensates). SMB SaaS with >18 month
payback is almost always a problem.

---

## Net Revenue Retention (NRR)

| Rating      | Value    | What It Means                                             |
| ----------- | -------- | --------------------------------------------------------- |
| CRITICAL    | <80%     | Revenue base is shrinking — existential risk              |
| WATCH       | 80-100%  | Stable but not growing from existing customers            |
| HEALTHY     | 100-110% | Modest expansion, typical for SMB/Mid-Market              |
| STRONG      | 110-120% | Good expansion revenue, typical for Mid-Market/Enterprise |
| WORLD-CLASS | >120%    | Exceptional; Snowflake, Datadog territory                 |

**Stage expectations**:

- **Early**: NRR data may not be meaningful with <20 customers. Logo retention is more useful.
- **Growth**: NRR should be >100%. If <100%, churn is outpacing expansion — a serious concern.
- **Scale**: NRR >110% is a strong signal. Below 100% at this stage is a red flag.

---

## MoM MRR Growth Rate

| Stage                 | HEALTHY | WATCH  | CRITICAL |
| --------------------- | ------- | ------ | -------- |
| Early (Pre-seed/Seed) | 10-20%  | 5-10%  | <5%      |
| Growth (Series A/B)   | 5-10%   | 3-5%   | <3%      |
| Scale (Series C+)     | 3-7%    | 1-3%   | <1%      |
| Late (Pre-IPO)        | 1-3%    | 0.5-1% | <0.5%    |

**Notes**: Growth rates naturally decelerate as ARR increases (the "law of large
numbers" in SaaS). A company growing 15% MoM at $100K MRR is normal; 15% MoM at
$10M MRR would be extraordinary. Always contextualise growth rate against the
revenue base.

---

## Gross Margin

| Rating      | Value  | Interpretation                                                    |
| ----------- | ------ | ----------------------------------------------------------------- |
| CRITICAL    | <50%   | Not a software business — heavy services or COGS                  |
| WATCH       | 50-65% | Services-heavy or infrastructure-heavy; needs path to improvement |
| HEALTHY     | 65-75% | Typical SaaS range                                                |
| STRONG      | 75-85% | Efficient delivery model                                          |
| WORLD-CLASS | >85%   | Pure software, minimal delivery cost                              |

**Common gotchas**:

- AI/ML companies often have lower margins (GPU/inference costs). 50-65% may be acceptable if improving.
- Companies that blend services revenue with SaaS revenue will show depressed margins. Ask for SaaS-only gross margin.
- Hosting costs that scale linearly with customers (rather than sub-linearly) are a structural margin risk.

---

## Rule of 40

| Rating     | Score | Interpretation                                                       |
| ---------- | ----- | -------------------------------------------------------------------- |
| CONCERNING | <20   | Growth too slow for the burn, or burn too high for the growth        |
| WATCH      | 20-40 | Below benchmark but may be acceptable if investing heavily in growth |
| HEALTHY    | 40-60 | Meeting the benchmark — balanced growth and efficiency               |
| STRONG     | >60   | Best-in-class; either very fast growth, very efficient, or both      |

**Stage nuance**: The Rule of 40 is most meaningful for companies with >$10M ARR.
Earlier-stage companies should be heavily skewed toward growth (e.g., 80% growth +
-40% margin = Rule of 40 score of 40). A pre-seed company with a low Rule of 40 is
less concerning than a Series C company with the same score.

---

## Burn Multiple

| Rating     | Value  | Interpretation                            |
| ---------- | ------ | ----------------------------------------- |
| EXCELLENT  | <1x    | Very capital-efficient growth             |
| GOOD       | 1-1.5x | Efficient                                 |
| ACCEPTABLE | 1.5-2x | Normal for Growth stage                   |
| WATCH      | 2-3x   | Inefficient; needs justification          |
| CRITICAL   | >3x    | Burning cash without proportionate growth |

**Formula reminder**: Burn Multiple = Net Burn / Net New ARR.
A burn multiple of 2x means spending $2 for every $1 of new ARR. Context matters:
a company investing in a new product line or geographic expansion may have a
temporarily elevated burn multiple.

---

## Quick Ratio (SaaS)

| Rating   | Value | Interpretation                                            |
| -------- | ----- | --------------------------------------------------------- |
| CRITICAL | <1    | MRR is contracting — losing more than gaining             |
| WATCH    | 1-2   | Growing but fragile — churn is consuming most new revenue |
| HEALTHY  | 2-4   | Healthy balance of growth and retention                   |
| STRONG   | >4    | Excellent growth efficiency, low churn impact             |

**Formula reminder**: Quick Ratio = (New MRR + Expansion MRR) / (Contraction MRR + Churned MRR)

---

## Benchmark Quick Reference Card

For rapid assessment, use this simplified view:

| Metric                  | Good   | Great  | Red Flag |
| ----------------------- | ------ | ------ | -------- |
| MoM Growth (Early)      | >10%   | >20%   | <5%      |
| Monthly Churn (blended) | <3%    | <1.5%  | >5%      |
| NRR                     | >100%  | >120%  | <80%     |
| LTV:CAC                 | >3:1   | >5:1   | <1:1     |
| CAC Payback             | <18 mo | <12 mo | >24 mo   |
| Gross Margin            | >65%   | >80%   | <50%     |
| Rule of 40              | >40    | >60    | <20      |
| Burn Multiple           | <2x    | <1x    | >3x      |
| Quick Ratio             | >2     | >4     | <1       |

---

## Sources

- **OpenView Partners**: SaaS Benchmarks Report (annual)
- **Bessemer Venture Partners**: Cloud Index, State of the Cloud
- **SaaS Capital**: SaaS Retention Benchmarks, Index
- **Paddle**: State of SaaS (ProfitWell data)
- **Jason Lemkin / SaaStr**: Rule of 40, stage-based expectations
- **David Sacks**: Burn Multiple framework
