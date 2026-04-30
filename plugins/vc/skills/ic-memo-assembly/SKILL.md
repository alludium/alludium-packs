---
id: ic-memo-assembly
name: IC Memo Assembly
description: >
  Assemble a 12-section IC memo from existing Deal Room artifacts, enforce
  citation standards, and maintain the IC Decision Log. Use this skill when
  preparing an investment committee pack from completed diligence outputs,
  drafting the IC memo for a deal that has passed evaluation, running a citation
  sweep on a memo draft, recording IC decisions and follow-ups after the meeting,
  or checking whether a deal's artifacts are complete enough to begin memo assembly.
tags:
  - vc
  - ic-memo
  - diligence
  - decision-log
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: recommended
      required: false
      note: IC memo assembly requires access to Deal Room artifacts and supporting diligence outputs. Provider-specific tool IDs are intentionally omitted because deal artifacts may be supplied through several configured surfaces.
      gracefulDegradation: Return the missing-artifact checklist and stop instead of drafting unsupported memo sections.
    - kind: setup
      importance: recommended
      required: false
      owner: user
      ownerPath: Attach or route the required deal artifacts through the current project or Deal Room owner before assembly.
      confirmationRequired: true
      gracefulDegradation: Produce only chat-level summaries or gap lists when document creation or source artifacts are unavailable.
  routingHints:
    preferredSurface: skill
    notes:
      - This skill assembles from existing artifacts; it does not make investment decisions or mutate systems of record.
---

# IC Memo Assembly

Assemble a 12-section IC investment memo by pulling from existing Deal Room
artifacts. This is assembly work, not blank-page writing. Every section maps to a
specific diligence output. Where gaps exist, flag them rather than fabricating content.

This skill also covers citation enforcement on the assembled memo and maintaining
the IC Decision Log after the committee meets.

## Prerequisite Completeness Check

Before drafting, confirm the Deal Room contains the minimum required inputs.
Run this check first and stop if any required item is missing.

### Required Inputs (must exist)

| #   | Artifact                                             | Produced By                        | Used In Sections |
| --- | ---------------------------------------------------- | ---------------------------------- | ---------------- |
| 1   | Deck summary or equivalent company overview artifact | Existing deal materials            | 1, 2, 3, 4, 6    |
| 2   | Call notes / transcript summary                      | `meeting-prep-and-summary`         | 3, 9             |
| 3   | Traction KPI worksheet                               | `traction-and-saas-unit-economics` | 7, 6             |
| 4   | Market map                                           | `market-map-building`              | 5                |
| 5   | Team table                                           | `team-and-hiring-assessment`       | 8                |
| 6   | Red flags list                                       | `red-flags-scanner`                | 10               |

### Recommended Inputs (proceed without, but note gaps)

| Artifact                     | Produced By                               | Used In Sections            |
| ---------------------------- | ----------------------------------------- | --------------------------- |
| 10-Factor scorecard          | `ten-factor-evaluation`                   | 12 (recommendation context) |
| Diligence question bank      | `82-factor-diligence-question-generation` | 11                          |
| Deal terms / cap table notes | Founder materials / call notes            | 9                           |
| Company research profile     | `company-research-and-enrichment`         | 1, 2, 5                     |

### If Required Inputs Are Missing

List every missing artifact, name the skill or agent that produces it, and stop.
Do not draft partial memos. Return the missing items as a checklist so the deal
lead can sequence the remaining work.

## Core Method

1. Run the prerequisite completeness check. Stop if any required input is missing.
2. Create the memo document titled `IC Memo -- {Company} -- {YYYY-MM-DD}`.
3. Populate each of the 12 sections by pulling from the mapped artifacts (see
   Artifact-to-Section Mapping below). Do not re-research unless a specific gap
   exists and cannot be filled from Deal Room materials.
4. Run the Citation Enforcement pass on the completed draft.
5. Generate the IC Pre-read Pack Index listing links to all supporting artifacts.
6. Output a 10-bullet IC summary + top risks + open questions in chat, and the
   full memo draft as a document.

## The 12-Section IC Memo Template

### 1. Company Overview

One-liner describing what the company does. Include: name, website, location,
stage, sector, and founding date. Keep to 3-5 sentences maximum.

### 2. Why Now

What timing advantage exists? Identify the shift in behaviour, regulation, or
technology that creates the current window. Cite specific signals.

### 3. Problem + Customer

What pain does the company solve? Who is the buyer? How urgent and expensive
is the problem? Pull from deck summary and call notes.

### 4. Product + Differentiation

What is the product? What makes it meaningfully better, faster, or cheaper than
alternatives? Include evidence of customer satisfaction if available.

### 5. Market + Competitive Landscape

Market dynamics, TAM/SAM/SOM (only if credibly sourced), competitive positioning.
Pull directly from the market map artifact. Include the competitor table
and moat hypotheses.

### 6. Business Model + Pricing

Revenue model, pricing structure, target buyers, distribution channel, unit
economics viability, path to gross margin. Pull from deck summary and traction
worksheet.

### 7. Traction

KPI table from the traction artifact plus a short narrative.
Include: revenue metrics, growth, retention, product usage. Flag any qualitative-
only claims or inconsistencies between sources.

### 8. Team

Pull from the team assessment artifact. Include the team table, functional
gap analysis, and suggested hiring plan. Assess founder-market fit.

### 9. Deal Terms

Round size, valuation, amount the fund would invest, target ownership percentage,
pro rata rights, other notable terms. If deal terms are not yet known, include
a placeholder section and state "Terms TBC -- do not invent valuations."

### 10. Risks & Mitigations

Pull from the Red Flags Scanner output. Rank risks by severity (High/Med/Low).
For each risk, include the evidence, the mitigation (if any), and the recommended
next action. Surface conflicting evidence here rather than resolving it elsewhere.

### 11. Diligence Plan + Open Questions

Pull from the 82-Factor Diligence Question Generator output if available.
Organise questions into: Critical (must answer before decision), Important
(should answer soon), and Nice-to-have. Align to 82-Factor categories.

### 12. Recommendation + Decision Ask

Synthesise all inputs into one of three recommendations:

- **Invest** -- proceed to term sheet. State conviction drivers.
- **Continue diligence** -- specify what must be resolved and by when.
- **Pass** -- state the primary reasons clearly.

Include the specific decision ask for the IC: what action is being requested
and what conditions apply.

## Artifact-to-Section Mapping

Use this table to trace every section back to its source artifacts:

| Section                             | Primary Source(s)                | Secondary Source(s)                                                    |
| ----------------------------------- | -------------------------------- | ---------------------------------------------------------------------- |
| 1. Company Overview                 | Deck summary                     | Company research profile                                               |
| 2. Why Now                          | Deck summary                     | Company research profile, Exa research                                 |
| 3. Problem + Customer               | Deck summary, call notes         | --                                                                     |
| 4. Product + Differentiation        | Deck summary                     | Company website, product demo                                          |
| 5. Market + Competitive Landscape   | Market map                       | Exa research, Dealroom when connected / Affinity-enriched company data |
| 6. Business Model + Pricing         | Deck summary, traction worksheet | Call notes                                                             |
| 7. Traction                         | Traction KPI worksheet           | Call notes, financial model                                            |
| 8. Team                             | Team table                       | Call notes                                                             |
| 9. Deal Terms                       | Call notes, founder materials    | Cap table summary                                                      |
| 10. Risks & Mitigations             | Red flags list                   | All other artifacts                                                    |
| 11. Diligence Plan + Open Questions | Diligence question bank          | 10-Factor scorecard unknowns                                           |
| 12. Recommendation + Decision Ask   | All inputs (synthesis)           | 10-Factor scorecard                                                    |

## Citation Enforcement

After assembling the memo, run a citation pass. Scan every statement and classify
claims into four types:

### Claim Types Requiring Citations

| Type                   | Description                                         | Examples                                     |
| ---------------------- | --------------------------------------------------- | -------------------------------------------- |
| **Numerical**          | Any metric, market size, or pricing figure          | "MRR of $120k", "TAM of $4.2B"               |
| **Comparative**        | Superlatives or relative positioning                | "largest provider", "3x faster"              |
| **Externally sourced** | Customer quotes, press references, third-party data | "featured in TechCrunch", "NPS of 72"        |
| **High-stakes**        | Legal, financial, or regulatory claims              | "IP fully assigned", "no pending litigation" |

### Citation Rules

- Every claim in the four types above must have an adjacent source pointer:
  slide number, document link, page reference, timestamp, or web URL.
- If a claim cannot be supported, either remove it, convert it to hypothesis
  language ("We believe..."), or label it explicitly as `[ASSUMPTION]`.
- Do not fabricate citations. If no source exists, recommend where to find one.
- Prefer primary sources (founder materials, official filings, company website)
  over secondary sources (blog posts, analyst estimates).
- Label confidence level (High/Medium/Low) on any claim sourced from secondary
  or unverified material.

### Unsupported Claims Table

After the citation pass, produce an appendix table:

```
| Claim | Section | Claim Type | Why Risky | Suggested Source | Fix |
|-------|---------|------------|-----------|------------------|-----|
```

Include this table as a working artifact for the deal lead. It does not appear
in the final IC memo.

## IC Decision Log

After the IC meeting, record the outcome in the Decision Log. This is an
append-only record -- never overwrite previous entries.

### Decision Log Entry Format

```
| Date | Company | Decision | Rationale | Follow-ups | Owner |
|------|---------|----------|-----------|------------|-------|
```

### Decision Status Taxonomy

- **Pass** -- deal rejected. Record the primary reasons.
- **Continue** -- proceed with further diligence. List specific items to resolve.
- **Term sheet** -- proceed to offer. Note key terms discussed.
- **Pending** -- decision deferred. List what is needed to close the decision.

### Decision Log Rules

- Decisions must be explicit and attributable (who agreed).
- If the decision is ambiguous from meeting notes, mark as Pending and list
  what is needed to close.
- Every "Continue" or "Pending" decision must have at least one follow-up
  with an owner and deadline.
- Propose a Deal Snapshot Decision History update with the same entry.
- Draft follow-up tasks with owner and deadline for each action item; do not create
  tasks without explicit approval.

## IC Pre-read Pack Index

Generate this section at the end of every memo. It provides the IC members with
direct links to all supporting artifacts:

```
## Pre-read Pack

| Document | Location | Last Updated |
|----------|----------|--------------|
| Pitch deck | [link] | YYYY-MM-DD |
| Traction KPI worksheet | [link] | YYYY-MM-DD |
| Market map | [link] | YYYY-MM-DD |
| Team table | [link] | YYYY-MM-DD |
| Red flags scan | [link] | YYYY-MM-DD |
| Diligence question bank | [link] | YYYY-MM-DD |
| 10-Factor scorecard | [link] | YYYY-MM-DD |
| Legal docs (if any) | [link] | YYYY-MM-DD |
```

## Tool Guidance

Use tools to fill gaps in the assembled memo. Do not ask the user for information
that tools can provide.

| Tool            | When to Use                                                                                                          |
| --------------- | -------------------------------------------------------------------------------------------------------------------- |
| Exa             | Supplementary research for "Why Now" signals, recent press, and market validation when Deal Room artifacts have gaps |
| Brave / SerpAPI | Public-search fallback for recent news, source triangulation, and market-source diversity                            |
| Dealroom        | Comparable financing context, investor history, and sector activity when connected                                   |

If a Company Research & Enrichment profile exists, use it as the starting point
for sections 1, 2, and 5.
If Dealroom is unavailable, continue from Deal Room artifacts, the company research
profile, and Exa rather than blocking the memo.

## Output Shape

```
# IC Memo -- [Company] -- [YYYY-MM-DD]

## 1. Company Overview
[one-liner + company details]

## 2. Why Now
[timing thesis with citations]

## 3. Problem + Customer
[pain, buyer, urgency]

## 4. Product + Differentiation
[what it does, why it's better]

## 5. Market + Competitive Landscape
[market dynamics + competitor table + moat hypotheses]

## 6. Business Model + Pricing
[revenue model, pricing, unit economics path]

## 7. Traction
[KPI table + narrative]

## 8. Team
[team table + gap analysis + hiring plan]

## 9. Deal Terms
[round details or "Terms TBC"]
[include valuation sensitivity, ownership/dilution view, IRR/MOIC cases, and key assumptions when provided]

## 10. Risks & Mitigations
[ranked risk table with evidence and actions]

## 11. Diligence Plan + Open Questions
[prioritised question list, 82-factor aligned]

## 12. Recommendation + Decision Ask
[Invest / Continue / Pass + rationale + specific ask]

## Pre-read Pack
[artifact index table with links]

## Receipts
[sources used and artifacts created during assembly]
```

## Guardrails

- IC memos are **internal-only artifacts**. Never send externally unless the
  user explicitly approves.
- Assumptions must be labelled as `[ASSUMPTION]`. Never present assumptions
  as established facts.
- The memo must be readable in under 10 minutes. Use headings, bullets, and
  tables. Cut prose that does not add decision value.
- Do not invent deal terms, valuations, or cap table structures. Use placeholders
  when information is not available.
- Valuation, dilution, IRR, and MOIC scenarios must show assumptions and should
  be omitted or marked `[ASSUMPTION]` when the required inputs are missing.
- If evidence conflicts across sources, surface the contradiction in the Risks
  section with both citations. Do not resolve conflicts by averaging or guessing.
- Do not change system-of-record fields in Affinity without approval. Create
  draft notes instead.
- Log all sources and actions in a Receipts section.
- Match the firm's tone: clear, direct, founder-friendly. Avoid jargon and unnecessary
  length.

## Related Skills

- `citation-enforcement` -- standalone citation sweep (this skill includes a
  built-in citation pass, but the dedicated skill handles deeper audits)
- `traction-and-saas-unit-economics` -- deeper traction analysis for Section 7
- `team-and-hiring-assessment` -- deeper team evaluation for Section 8
- `market-map-building` -- deeper competitive landscape for Section 5
- `red-flags-scanner` -- structured risk scan for Section 10
- `82-factor-diligence-question-generation` -- full question bank for Section 11
- `ten-factor-evaluation` -- screening scorecard that feeds Section 12 context
- `company-research-and-enrichment` -- foundation data for Sections 1, 2, 5
- `meeting-prep-and-summary` -- call notes that feed Sections 3, 9
