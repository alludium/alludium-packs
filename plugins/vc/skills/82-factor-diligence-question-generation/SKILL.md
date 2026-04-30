---
id: 82-factor-diligence-question-generation
name: 82-Factor Diligence Question Generation
description: >
  Turn an 82-Factor framework into a prioritised, practical question set tailored to a
  specific deal. Use this skill when preparing for a diligence call, identifying what is
  already known vs unknown, converting knowledge gaps into concrete questions, prioritising
  by decision impact, building a next-call agenda, or surfacing the top unknowns that block
  an investment decision. This skill maps existing DD artifacts against the 127-question bank
  across 6 categories, suppresses answered questions, and produces a focused, tiered output
  rather than an exhaustive dump.
tags:
  - vc
  - diligence
  - questions
  - 82-factor
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: recommended
      required: false
      note: Diligence question generation is strongest when the agent can inspect deal artifacts, decks, notes, or prior scorecards. Provider-specific tool IDs are intentionally omitted because artifact access may be supplied through several configured surfaces.
      gracefulDegradation: Ask the user for the relevant deal artifacts or produce only a thin missing-information checklist.
    - kind: setup
      importance: recommended
      required: false
      owner: user
      ownerPath: Attach or provide deal materials through the current chat, project, or Deal Room before running the question-generation pass.
      confirmationRequired: true
      gracefulDegradation: Continue only with explicitly provided context and label unanswered areas as unknown.
  routingHints:
    preferredSurface: skill
    notes:
      - Builder, Skills Manager, or a deal-workflow owner assigns this skill; it does not create artifacts or fetch unavailable deal materials by itself.
---

# 82-Factor Diligence Question Generation

Convert the 82-Factor framework into a deal-specific, prioritised question set. The goal
is a usable next-call agenda, not a wall of 127 questions. Surface what is genuinely unknown,
suppress what is already answered, and rank by decision impact.

This skill is for question generation and prioritisation only — not for scoring, not for
memo assembly, not for the screening evaluation itself.

## Minimum Inputs

Before generating questions, confirm the following exist:

- A company name and deal context (stage, sector, round size)
- At least one DD artifact: pitch deck, ten-factor scorecard, call notes, data room index,
  or prior memo draft

If no DD artifacts exist beyond a short inbound email or similarly thin context, stop and
recommend requesting more founder materials first. Do not generate questions in a vacuum.

## Reference Material

The full 127-question bank lives in `references/82-factor-checklist.md` within this skill
directory. That file is the canonical source — do not hard-code questions inline.

The 6 categories and their question counts:

| #   | Category                 | Sub-categories                                 | Questions |
| --- | ------------------------ | ---------------------------------------------- | --------- |
| 1   | Screening                | Deal Quality, Investment Compatibility         | 15        |
| 2   | Management Due Diligence | Resources, Team, Board, Advisors, Co-investors | 23        |
| 3   | Business Opportunity     | Product, Business Model, Competitive Strategy  | 15        |
| 4   | Intangibles              | Focus, Momentum, Buzz, Gut                     | 4         |
| 5   | Legal                    | Pre-investment, IP, Transaction, Harvest       | 59        |
| 6   | Financial                | Analysis, Financing, Ownership, Valuation      | 11        |

## Core Method

### Step 1 — Inventory Existing Knowledge

Scan all available DD artifacts and map what is already known against the 82-Factor
framework. For each category, classify every question as:

- **Answered** — evidence exists in artifacts. Record the source and a one-line summary.
- **Partially answered** — some signal exists but insufficient for confidence. Note what
  is missing.
- **Unanswered** — no evidence found.

Do not guess or infer answers. If a deck says "large TAM" with no number, that is partially
answered, not answered.

### Step 2 — Contextual Filtering

Not every question applies to every deal. Suppress questions that are irrelevant given the
deal context:

- **Stage filtering** — Pre-seed/seed deals: suppress most Legal 5.4-5.6 (transaction
  mechanics) and Financial 6.4 (formal valuation methods). These become relevant at
  Series A+. Pre-revenue deals: suppress Financial 6.1.1 (historical financials) if
  the company has none.
- **Sector filtering** — Deep-tech/biotech: elevate IP questions (5.2.x). Pure SaaS:
  de-prioritise patent questions if no IP moat is claimed.
- **Structure filtering** — If the deal is a SAFE or convertible note, suppress preferred
  stock mechanics (5.4.8, 5.6.12-5.6.14). If no co-investors yet, suppress 2.5.1.
- **Already-known filtering** — Questions classified as Answered in Step 1 are suppressed
  from the output entirely. Partially answered questions remain but flagged as needing
  follow-up on the specific gap.

Document every suppression decision. The user must be able to see what was excluded and why.

### Step 3 — Tiered Prioritisation

Assign every remaining question to a tier:

**Critical for next meeting (top 10)**
Questions whose answers would change the invest/pass decision. These are decision-blocking.
Typical areas:

- Team quality and completeness (2.1.1, 2.1.2, 2.2.1-2.2.2)
- Business model viability (3.3.1, 3.3.4)
- Competitive defensibility (3.4.1, 3.4.2)
- Burn rate and runway (6.1.3, 6.2.3)
- Deal-breaker legal issues (5.1.4 litigation, 5.2.16 IP litigation)

**Needed before IC (next 20)**
Questions that materially affect terms, valuation, or risk assessment but do not block the
initial proceed/pass decision. Typical areas:

- Cap table and ownership (6.3.1)
- Future financing needs (6.2.4, 6.2.5)
- Board composition and independence (2.3.x)
- IP ownership clarity (5.2.17 invention assignment)
- Distribution channel (3.3.3)

**Nice-to-have**
Questions that refine understanding but do not gate any decision. Typical Tier 3 areas:

- Accounting firm quality (1.1.5)
- Specific registration rights mechanics (5.6.1-5.6.5)
- Advisory board quality (2.4.1)
- Buzz and momentum (4.2, 4.3)

Tier assignment is contextual, not fixed. A question that is normally "Needed before IC"
becomes "Critical for next meeting" if the deal has a specific red flag in that area.

### Step 4 — Next Call Agenda

After prioritising, turn the highest-priority questions into a short next-call agenda in a
logical order. This is the practical output the VC workflow expects: not just a list of
questions, but a sequence the team can actually use on the call.

### Step 5 — Question Enhancement

For each question in the output, do not just copy the framework question verbatim. Enhance
it:

- **Contextualise** — Rewrite the generic question to reference the specific company,
  product, or market. "Does the company have top-quality management?" becomes "How did
  [CEO name] and [CTO name] come to work together, and what relevant domain experience
  do they bring from [prior company]?"
- **Add rationale** — Why does this question matter for this specific deal?
- **Specify evidence** — What kind of answer or artifact would resolve the question?
  "Monthly cohort retention for 12+ months" is useful. "More data on churn" is not.

## Output Shape

```
# 82-Factor Diligence Questions: [Company Name]

## Deal Context
- **Stage:** [Seed / Series A / ...]
- **Sector:** [...]
- **Round size:** [...]
- **Artifacts reviewed:** [list with dates]

## Coverage Summary

| Category | Total Qs | Answered | Partial | Unanswered | Suppressed |
|----------|----------|----------|---------|------------|------------|
| Screening | 15 | X | X | X | X |
| Management DD | 23 | X | X | X | X |
| Business Opportunity | 15 | X | X | X | X |
| Intangibles | 4 | X | X | X | X |
| Legal | 59 | X | X | X | X |
| Financial | 11 | X | X | X | X |
| **Total** | **127** | **X** | **X** | **X** | **X** |

## Critical for Next Meeting (Top 10)
[Up to 10 decision-blocking questions with rationale]

1. **[Contextualised question]**
   - Category: [X.X.X]
   - Why it matters: [1-2 sentences specific to this deal]
   - What would answer it: [specific evidence or artifact]

2. ...

## Needed Before IC (Next 20)

### [Category Name]

| Ref | Question | Why It Matters | Evidence Needed |
|-----|----------|---------------|-----------------|
| X.X.X | [Contextualised question] | [Deal-specific rationale] | [Specific artifact/data] |

### [Next Category with questions]
...

## Nice-to-Have

### [Category Name]
...

## Next Call Agenda
1. [Opening question]
2. [Second question]
3. ...

## Suppressed Questions
[Questions excluded and why — stage/sector/structure/already-answered]

| Ref | Original Question | Reason Suppressed |
|-----|-------------------|-------------------|
| X.X.X | [Question] | [Reason] |
```

## Tool Guidance

This is primarily an analytical skill. Tool use is optional and situational.

| Tool            | When to Use                                                                                                                                                  |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Exa             | Sector-specific context to improve question contextualisation — e.g., "what are the key IP risks in [sector]?" to sharpen Legal questions for a biotech deal |
| Brave / SerpAPI | Public-search fallback when sector context, legal/regulatory references, or market signals need broader source coverage                                      |

Do not use tools to answer the questions — this skill generates them. Answering is the job
of the diligence process itself.

## Guardrails

- **Generate, do not answer.** This skill produces questions and prioritises them. It does
  not attempt to answer the questions or assess the company. That is what
  `ten-factor-evaluation` and the broader DD process do.

- **Suppress aggressively, document transparently.** A 127-question dump is worse than
  useless. But every suppression must be visible and reversible. The user must trust that
  nothing important was hidden.

- **Tier assignment must follow from deal context, not habit.** Do not mechanically assign
  the same tier to the same question across all deals. A question about IP patents is Tier 3
  for a marketplace business and Tier 1 for a deep-tech company.

- **Contextualise every question.** A verbatim copy of the framework question adds no value
  over reading the checklist directly. The skill's value is in making generic questions
  specific to the deal.

- **Do not fabricate deal context.** If you do not know the stage, sector, or what artifacts
  exist, ask. Do not guess "this looks like a Series A" and filter accordingly.

- **Compress aggressively.** If the output starts to sprawl past the practical top 10 /
  next 20 / nice-to-have structure, group and compress. A usable agenda beats a
  comprehensive dump.

- **Respect prior work.** If a `ten-factor-evaluation` scorecard exists, use its Unknowns
  sections as primary input. Do not re-derive what is already mapped.

## Related Skills

This skill works well with:

- `ten-factor-evaluation` — upstream: provides the initial known/unknown map
- `red-flags-scanner` — flags that elevate specific questions to Tier 1
- `team-and-hiring-assessment` — deeper input for Management DD questions (Category 2)
- `traction-and-saas-unit-economics` — deeper input for Financial questions (Category 6)
- `ic-memo-assembly` — downstream: consumes the prioritised question set as input for the
  memo's "Key Questions" section
