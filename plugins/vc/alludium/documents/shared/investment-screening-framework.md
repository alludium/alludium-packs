---
id: vc.document.investment_screening_framework
title: Investment Screening Framework
documentType: methodology
supportedProjectTypes:
  - vc_deal_room
  - vc_origination_pipeline
summary: Reusable first-look scorecard methodology for venture screening.
---

# Investment Screening Framework

## Rendered Artifact Contract

When this document is used to create a task output artifact:

- Create the final artifact with `artifact_createTextArtifact`.
- Use a `.html` filename and `mimeType: "text/html"`.
- Set `content` to a complete standalone safe static HTML document beginning with `<!doctype html>`.
- Convert this Markdown scaffold into semantic HTML sections, tables, and lists with small inline CSS in a `<style>` block.
- Do not create `.md` or `text/markdown` artifacts for rendered outputs.
- Do not copy HTML into structured task output fields; those fields remain plain text or artifact UUIDs.


## Purpose

Use this framework to create a first-look investment screen for one company or a sourced candidate batch. The output should help an investor decide whether to pass, watch, continue, promote, or ask for specific missing evidence. It is a screening tool, not a full diligence memo.

## Source Precedence For Company-Claimed Facts

For facts the company asserts about itself — ARR and other traction metrics,
fundraising ask, round and stage, customer counts and named customers, roadmap,
go-to-market, founder names and roles, and team narrative — uploaded/founder/
company-provided materials and supplied CRM notes are the primary source. Use public,
structured, and web sources to corroborate, challenge, timestamp, or fill gaps; do not
let them silently replace a company-provided value. When they conflict on a
company-claimed fact, keep the company-provided value as the primary claim, show the
conflicting value and its source, explain which value the scorecard uses and why, and
flag material conflicts for partner judgment. Independent validation facts such as
press, market context, registry data, and third-party headcount signals may be led by
high-quality external sources. The "Evidence To Look For" column below lists candidate
sources, not a precedence order.

## Scorecard

| Dimension | What To Assess | Evidence To Look For | Rating |
| --- | --- | --- | --- |
| Thesis fit | Fit to fund mandate, stage, geography, sector, and timing | Fund thesis, source context, company description | Strong / Mixed / Weak / Unknown |
| Problem | Pain severity, urgency, buyer owner, and whether the problem is worth solving now | Customer evidence, founder materials, market notes, intro context | Strong / Mixed / Weak / Unknown |
| Product | Clear product, workflow, customer value, differentiation, and adoption path | Demo, pitch deck, product notes, usage evidence | Strong / Mixed / Weak / Unknown |
| Market | Category size, growth, budget pool, timing, and route to first segment | Market reports, customer notes, source thesis, public research | Strong / Mixed / Weak / Unknown |
| Business model | Pricing, gross margin potential, sales motion, and revenue-quality path | Pricing notes, contracts, pipeline, model, customer claims | Strong / Mixed / Weak / Unknown |
| Funding requirement | Stage, cheque size, valuation, ownership path, reserves, and syndicate fit | Fundraise materials, cap table, round plan, terms | Strong / Mixed / Weak / Unknown |
| Value creation | Edge or asset that can compound into durable enterprise value | Product evidence, IP, data, distribution, workflow lock-in, customer proof | Strong / Mixed / Weak / Unknown |
| Competition | Differentiation, defensibility, category crowding, incumbent risk, switching costs | Competitor map, customer alternatives, public sources | Strong / Mixed / Weak / Unknown |
| Exit | Plausible acquirers, IPO logic, strategic value, and fund-return relevance | Comparable exits, buyer map, category consolidation, return model | Strong / Mixed / Weak / Unknown |
| Risks and unknowns | Disqualifying issues, missing evidence, contradictions, and what would change the answer | Red flags, source gaps, disconfirming evidence, open questions | Clear / Manageable / Severe / Unknown |
| Team | Founder-market fit, integrity, ambition, hiring gaps, commercial ability, and coachability | Founder bios, references, prior outcomes, role coverage | Strong / Mixed / Weak / Unknown |

## Recommendation Bands

| Recommendation | Use When | Required Next Step |
| --- | --- | --- |
| Continue | Most core dimensions are strong or answerable and no obvious hard stop exists | Run follow-up evaluation or diligence questions |
| Watch | Fit is plausible, but timing, traction, or evidence is not yet strong enough | Define watch trigger and owner |
| Pass | Fund fit, evidence quality, risk, or timing is materially weak | Record concise pass rationale |
| Promote | Sourcing candidate has enough evidence for Deal Pipeline review | Prepare promotion package and require human approval |
| Needs partner judgment | Evidence is incomplete but strategic relevance may override the screen | Escalate exact tradeoff, not a generic "maybe" |

## Routing Notes

Use the screen to route work, not to imply diligence is complete.

- `too early`: strong thesis fit but evidence, product, team, or financing path is not ready.
- `too late`: mature stage, valuation, ownership path, or round dynamics do not fit the fund.
- `out of thesis`: company may be credible but does not fit mandate, geography, sector, stage, or return model.
- `watchlist`: attractive but waiting on a trigger such as customer proof, fundraise timing, hiring, regulatory event, or category inflection.
- `promote`: enough evidence exists for a human to approve downstream Deal Pipeline review.

## Output Standard

Every screen should include a one-paragraph verdict, the scorecard table, cited evidence, unknowns, disconfirming evidence, and an explicit next action. Do not average ratings mechanically. If a dimension is unknown, state the specific source input that would make it assessable.
