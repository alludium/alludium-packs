---
id: ten-factor-evaluation
name: Ten-Factor Evaluation
description: >
  Apply a Ten-Factor screening method to an investment opportunity using founder
  materials, deal artifacts, and external research. Use this skill when screening an
  inbound deal, evaluating whether a company fits the firm's investment criteria, turning a
  deck or first-call notes into a structured scorecard, identifying what is known vs
  unknown, generating top validation questions, or recommending whether to proceed, do
  deeper diligence, or pass.
tags:
  - vc
  - screening
  - evaluation
  - ten-factor
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: recommended
      required: false
      note: Ten-Factor evaluation depends on founder materials, deal artifacts, company context, and available external research sources. Provider-specific tool IDs are intentionally omitted because evidence may be supplied through several configured surfaces.
      gracefulDegradation: Score only factors supported by available evidence and mark the rest N/A or unknown.
    - kind: setup
      importance: recommended
      required: false
      owner: user
      ownerPath: Provide founder materials or route missing research/data access through owned setup paths before deeper evaluation.
      confirmationRequired: true
      gracefulDegradation: Produce a limited screening view with explicit unknowns and validation questions.
  routingHints:
    preferredSurface: skill
    notes:
      - This skill recommends next steps from evidence; it does not create deal rooms or mutate CRM by itself.
---

# Ten-Factor Evaluation

Apply a Ten-Factor screening method to produce a structured, evidence-backed assessment
of a company. The goal is to clearly separate what is known from what is unknown, and
recommend a next step.

This skill is for the screening method itself — not the full inbound workflow, not Deal Room
creation, and not deep diligence.

## Important Source Truth

Keep this distinction explicit:

- the underlying Ten-Factor checklist is qualitative
- it does not define a native numeric scoring rubric
- Barry's later operating material introduces a practical scorecard format with
  score, rationale, evidence, unknowns, roll-up, and recommendation

So when this skill uses a `1-5 or N/A` score, treat that as the operating convention for the
platform implementation, not as a claim that the original checklist itself defined a formal
scoring system.

## Minimum Inputs

Before running the method, confirm there is enough material to do meaningful work:

- A pitch deck, or
- Founder notes / first-call notes, or
- A similarly rich company briefing

If none exist, stop and ask for the minimum missing input rather than guessing.

## Thesis Fit Pre-Check

If the firm's investment thesis is available, do a fast fit check before full evaluation:

- Is the company outside fund geography, stage, or sector focus?
- Is there a hard mismatch that makes full scoring low-value?

If there is a clear thesis mismatch, say so, explain why, and recommend Pass without
running the full 10 factors.

## Core Method

1. Confirm minimum input exists.
2. Run thesis fit pre-check if thesis context is available.
3. Gather evidence from founder materials, call notes, company website, existing research
   artifacts, and external sources via tools.
4. For each of the 10 factors:
   - **Known** — summarise the strongest evidence. Cite sources.
   - **Assessment** — 2-3 sentences explaining the score. Surface contradictions explicitly.
   - **Score 1-5 or N/A** — where 1 is very weak and 5 is very strong. Include a confidence
     signal (High/Medium/Low). If evidence is insufficient to assess a factor credibly,
     use `N/A` and state exactly what would make the factor assessable.
   - **Unknowns** — what would improve confidence? Be specific. "Monthly churn by cohort
     for 12 months" is useful. "More data" is not.
5. Produce the roll-up, cases, questions, and recommendation.

## The 10 Factors

### 1. Problem

How big is the problem? Is the pain real, urgent, and expensive enough to support
venture-scale adoption — or is it a nice-to-have?

### 2. Product

What is the technology solution?

- Is there evidence customers like the product?
- Is it meaningfully better, faster, or cheaper than alternatives?
- Can it scale globally?

### 3. Market

What market does the company operate in?

- Market dynamics: crowded, fast-moving, sluggish, fragmented?
- **Why now?** Is there a shift in behaviour, regulation, or technology creating a window?
- Is the go-to-market strategy credible?

### 4. Business Model

What is the proposed business model?

- Does the model make sense for the market?
- What is the pricing plan? Who pays?
- Who are the target buyers? (TAM, SAM, SOM)
- How will the company reach customers? (distribution channel)
- Will the company make money? (path to gross margin, unit economics viability)
- Do the economics support venture-scale returns?

### 5. Funding Requirement

Does the investment fit the fund strategy?

- Stage, cheque size, and ownership expectations.
- Can the fund provide what this company needs?
- Can the fund reasonably reach its target ownership at exit, factoring in follow-on capital and dilution?

### 6. Value Creation

What value is actually being created?

- Patent portfolio, unique dataset, or team with unparalleled expertise ("edge")?
- Community of early customers or advocates driving above-average engagement?
- How much value can be captured? If radically cheaper than alternatives, the company needs
  to sell much more to generate equivalent revenue.

### 7. Competition

Are there moats the company can build or high barriers to entry?

- Is there a significant incumbent advantage or a giant moving into the space?
- What defensibility exists today, and what could be built over time?

### 8. Exit

Who will ultimately buy this company?

- Why and when would an acquirer buy it?
- Does the company have relationships with potential acquirers?
- On what metric would it be valued? Revenue multiples? EBITDA? Patent portfolio? Team?
- What kind of price would be paid? Are there proxies or precedent transactions?

### 9. Risks

What are the key risks we need to get comfortable with?

- On the flip side — are we taking enough risk?
- Is this a moonshot? If it succeeded, could it generate outsized returns?
  (Horsley Bridge data: 6% of venture companies generate 60% of returns.)

### 10. Team

Does the team have a unique advantage or edge? This is the deepest factor — assess thoroughly.

- Raw intelligence?
- Integrity?
- Mission-driven with noble purpose?
- Can they lead and hire fantastic people?
- Commercial ability — can they sell?
- Do they understand the market and product?
- Grit, ambition, and hustle?
- Do their skills gel as a group?
- Diversity?
- What are the gaps?
- Are they humble — will they listen to investors, customers, employees?

## Starred Items

The framework marks certain items with \* as especially important. Give these extra
attention in the assessment but do not inflate scores because of importance:

- Community/advocate engagement (Factor 6)
- Moats/barriers to entry (Factor 7)
- Moonshot/outsized return potential (Factor 9)
- Noble purpose (Factor 10)
- Commercial selling ability (Factor 10)

## Handling Contradictions

If evidence conflicts (deck says one revenue number, call notes imply another; hiring story
conflicts with actual team footprint), surface it explicitly. Do not average contradictions
away. Flag them, explain why they matter, and turn them into validation questions. If a
contradiction points to credibility risk, call that out clearly but carefully.

## Recommendation Logic

End with one of three recommendations:

**Proceed to first call** — enough positive signal to justify engagement. Key unknowns are
normal for this stage. No hard mismatch or fatal issue.

**Deeper diligence needed** — meaningful promise, but too many important unknowns remain or
one or two major factors need validation before confidence is warranted.

**Pass** — hard thesis mismatch, serious weakness across multiple core factors, or downside
pattern is already too strong relative to upside.

The recommendation must follow from the evidence pattern, not from gut feel.

## Output Shape

```
# Ten-Factor Evaluation: [Company Name]

## Summary

| # | Factor | Score | Confidence |
|---|--------|-------|------------|
| 1 | Problem | X/5 | High/Med/Low |
| ... | ... | ... | ... |
| 10 | Team | X/5 | ... |

Average: X.X/5 | Distribution: X strong / X mixed / X weak / X N/A

## Factor Detail

### 1. Problem — X/5 (Confidence: X)
**Known:** [evidence with sources]
**Assessment:** [2-3 sentences]
**Unknowns:** [specific questions]

### 2. Product — X/5 (Confidence: X)
...

[...all 10 factors]

## Pattern
[What stands out across the 10 factors taken together]

## Bull Case
[2-3 sentences — best realistic version]

## Bear Case
[2-3 sentences — worst realistic version]

## Top Questions to Validate
1. [Highest priority — ordered by decision impact]
2. ...

## Recommendation
[Proceed to first call / Deeper diligence needed / Pass]
[Rationale — why this follows from the evidence]
```

Use 5 questions by default for brevity. Expand to as many as 10 only when the deal has
multiple decision-blocking unknowns that genuinely need separate treatment.

## Tool Guidance

Use tools to gather evidence. Do not ask the user for information that tools can provide.

| Tool            | When to Use                                                                        |
| --------------- | ---------------------------------------------------------------------------------- |
| Harmonic        | Founder and team enrichment (Factor 10), company growth signals                    |
| Affinity        | Relationship check, source/referrer context, and enriched company fields           |
| Exa             | Market validation, competitive landscape, recent press, and "why now" signals      |
| Brave / SerpAPI | Public-search fallback for recent news, source triangulation, and broader coverage |
| Dealroom        | Funding context, comparable financing history, and investor signals when connected |
| Firecrawl       | Company website, pricing pages, and product detail                                 |

If an existing Company Research & Enrichment profile exists, use it as the starting point.
If structured funding or investor data is unavailable because Dealroom is not connected,
mark the relevant factor gap as `Unknown` and continue rather than guessing.

## Guardrails

- Score based on evidence, not enthusiasm. A great story with no traction evidence is not
  a 5 on Value Creation.
- Unknowns are not red flags. Thin evidence can justify a low-confidence score, and where
  there is no credible basis to assess, an `N/A`. It does not automatically mean Pass.
- Do not fabricate evidence or cite unverified sources.
- If Affinity shows an existing firm relationship, note it prominently but do not let it
  bias the scoring.
- Do not make CRM changes from this skill unless explicitly approved by the invoking workflow.

## Related Skills

This skill works well with:

- `company-research-and-enrichment` — foundation data
- `market-map-building` — deeper competitive context for Factor 7
- `red-flags-scanner` — structured risk scan beyond Factor 9
- `82-factor-diligence-question-generation` — deeper question set beyond the top 5
- `meeting-prep-and-summary` — first-call preparation from this evaluation
