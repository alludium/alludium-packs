---
id: market-map-building
name: Market Map Building
description: >
  Build a structured competitive landscape around a company or sector using a VC
  methodology. Use this skill when constructing a market map during evaluation-stage
  diligence, classifying competitors into a 3-bucket taxonomy, performing wedge
  analysis, assessing moat hypotheses, or validating TAM/SAM/SOM claims with evidence.
  The output follows a reusable VC market map template.
tags:
  - vc
  - competitive-analysis
  - market-map
  - diligence
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: recommended
      required: false
      note: Market mapping depends on available structured company, web research, and first-party source tools. Provider-specific tool IDs are intentionally omitted because company/source coverage may come from several configured surfaces.
      gracefulDegradation: Build a limited market map from provided materials and label structured-provider gaps.
    - kind: setup
      importance: recommended
      required: false
      owner: user
      ownerPath: Connect or provide Dealroom, Harmonic, Exa, Firecrawl, or deal artifacts through owned setup paths when deeper coverage is needed.
      confirmationRequired: true
      gracefulDegradation: Continue with visible competitors only and mark market-size or funding context as limited.
  routingHints:
    preferredSurface: skill
    notes:
      - Use this for evidence-backed market mapping, not for CRM updates or investment decisions.
---

# Market Map Building

Build a competitor landscape and wedge analysis grounded in sources. The goal is a
reusable artifact that becomes the default starting point for the deal team during
evaluation-stage diligence.

This skill is for the Market Map itself — not the full diligence pack, not the IC
memo, and not the 10-Factor screen.

## Minimum Inputs

Before starting, confirm there is enough material to produce a meaningful map:

- A pitch deck or founder materials that identify the buyer and the core workflow
- A clear sector definition (category + geography + stage filters)
- Or an existing company profile from `company-research-and-enrichment`

If the category is unclear, ask one clarifying question: **"Who is the buyer and
what is the core workflow?"** Do not guess.

## Core Method

### Step 1: Identify Category and Customer Segment

Extract from founder materials and the company website:

- **Buyer**: Who is paying?
- **Use case / job-to-be-done**: What problem is being solved?
- **Wedge**: What is the specific entry point / initial beachhead?

The wedge is not the full product vision. It is the narrow initial use case that
gets the company in the door with a specific buyer for a specific workflow.

### Step 2: Discover Competitors

Build the competitor list from multiple sources, then deduplicate:

1. **Dealroom when connected**: Use structured company and funding intelligence for known private
   market players, comparable financings, and investor context when connected.
2. **Exa**: Use `company_research_exa`, `web_search_exa`,
   `web_search_advanced_exa`, and deep research workflows for sector-level discovery,
   emerging categories, and competitors not yet well covered in structured providers.
3. **Harmonic**: Use structured startup discovery when the category is emerging or
   when additional startup coverage is needed beyond Dealroom.

If Dealroom is not connected, continue with Harmonic + Exa + Firecrawl and mark
structured funding / investor context as limited.

Treat Dealroom company coverage, company counts, and funding activity as discovery
and financing context only. Do not use them as a proxy for TAM or market size.

### Step 3: Classify into 3 Buckets

Every competitor goes into exactly one bucket:

| Bucket                       | Definition                                            | What to Look For                                                                                                    |
| ---------------------------- | ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Direct**                   | Same buyer and same job-to-be-done                    | Head-to-head competitors solving the identical problem for the identical buyer persona                              |
| **Adjacent**                 | Same buyer or same job-to-be-done, but not both       | Tools the same buyer uses for a different workflow, or tools solving the same problem for a different buyer segment |
| **Incumbents / Substitutes** | Legacy workflows, in-house solutions, non-consumption | Spreadsheets, manual processes, bundled platform features, or `do nothing`                                          |

**Why 3 buckets, not 2.** Direct competitors are the obvious ones. The real
insight often sits in the other two buckets. Adjacent players show where the
market is heading and who could pivot into the category. Incumbents and
substitutes show what the company is actually displacing, which is often a
manual workflow, bundled feature, or `do nothing` rather than a clean software
peer.

### Step 4: Enrich Each Competitor

Capture:

| Data Point                    | Primary Source                          | Backup Source           |
| ----------------------------- | --------------------------------------- | ----------------------- |
| Positioning + differentiation | Firecrawl (company website, about page) | Exa web search          |
| Customer segment              | Firecrawl (case studies, site copy)     | Exa                     |
| Pricing signals               | Firecrawl (pricing page extraction)     | Exa                     |
| Funding stage + history       | Dealroom                                | Harmonic                |
| Evidence links                | All tools                               | Record every source URL |

Every claim in the competitor table needs an evidence link. If a competitor cannot
be validated with credible sources, include it as **Unverified** rather than
omitting it.

### Step 5: Write the Wedge Analysis Narrative

Produce a short narrative covering:

1. **Where the wedge is.** Which buyer, which workflow, which pain point.
2. **Why now.** What behavior, regulation, technology, or market shift creates the
   window right now.
3. **Moat hypotheses.**

   - **Data advantage**: Does the company accumulate proprietary data that
     improves the product over time, and is that data hard to replicate?
   - **Distribution advantage**: Does the company have a channel, network
     effect, or go-to-market motion that compounds?
   - **Product advantage**: Is the product architecturally different in a way
     that is hard to copy, for example through switching costs or integration
     depth?

   For each moat hypothesis, state the evidence for and against. Do not assert
   a moat exists without support. Most early-stage companies do not yet have a
   moat; they have a defensibility hypothesis that needs validation.

4. **Risks.**
   - **Crowded category**: How many well-funded direct competitors exist, and
     is the category consolidating or fragmenting?
   - **Incumbent response**: Are larger platforms likely to build, bundle, or
     acquire their way into this workflow?
   - **Switching costs**: How easy is it for customers to switch away, and does
     the company need to win on product continuously?

When assessing incumbent response, use cited signals such as product announcements,
acquisitions, and official hiring pages if available. Do not assume generic job
board coverage.

### Step 6: Validate TAM / SAM / SOM (If Claimed)

Only include market sizing if supported by credible sources. If the founder deck
claims a TAM, validate it — do not parrot it.

Triangulation approach:

1. **Top-down**: Search for published analyst reports and official market sources via
   Exa. Note methodology and date.
2. **Bottom-up**: Use real pricing, customer counts, category economics, or similar
   first-principles assumptions only when the inputs are supportable.
3. **Company-claimed**: Extract TAM claims from the pitch deck and competitor websites
   via Firecrawl.
4. **Cross-validate**: If independent sources converge, confidence improves. If they
   diverge, flag that explicitly.

Dealroom funding activity may support **market heat** or **financing velocity**. It
must never be used as TAM by itself.

If no credible TAM source exists, state **"TAM unvalidated — assumptions listed
separately."**

## Decision Rules

- If the category is unclear after reviewing founder materials, ask one clarifying
  question rather than guessing.
- If a competitor cannot be validated, mark it `Unverified`.
- If TAM cannot be sourced, list assumptions separately.
- Check whether the same market map already exists in the Deal Room before creating a new one.

## Quality Checks

- **Geographic bias check**: Include relevant UK/EU peers when applicable.
- **Bucket balance**: If all competitors are direct, the adjacent or substitute
  buckets are likely under-researched.
- **Evidence density**: Every row should have at least one evidence link.
- **Wedge specificity**: The wedge must name the buyer persona and workflow.
- **Primary source preference**: Founder materials, official filings, and company
  websites over blog posts.

## Output Format

Follow this market map template:

```markdown
# Market Map: [Company Name / Sector]

## 1. Category Definition

- **Buyer**: [who is paying]
- **Use case / job-to-be-done**: [what problem is being solved]
- **Wedge**: [the specific entry point / initial beachhead]

## 2. Segments

- Segment A: [description]
- Segment B: [description]

## 3. Competitor Table

### Direct Competitors

| Company | Segment | Positioning | Differentiation | Evidence Links | Notes |
| ------- | ------- | ----------- | --------------- | -------------- | ----- |

### Adjacent Players

| Company | Segment | Positioning | Differentiation | Evidence Links | Notes |
| ------- | ------- | ----------- | --------------- | -------------- | ----- |

### Incumbents / Substitutes

| Company | Segment | Positioning | Differentiation | Evidence Links | Notes |
| ------- | ------- | ----------- | --------------- | -------------- | ----- |

## 4. Wedge Analysis

### Where the Wedge Is

[Concrete entry point]

### Why Now

[Timing thesis]

### Moat Hypotheses

- **Data advantage**: [hypothesis + evidence for/against]
- **Distribution advantage**: [hypothesis + evidence for/against]
- **Product advantage**: [hypothesis + evidence for/against]

## 5. TAM / SAM / SOM

[Only if supported by sources. Otherwise: "TAM unvalidated — assumptions listed below."]

| Scope | Estimate | Source   | Date   | Confidence   |
| ----- | -------- | -------- | ------ | ------------ |
| TAM   | $X       | [source] | [date] | High/Med/Low |
| SAM   | $X       | [source] | [date] | High/Med/Low |
| SOM   | $X       | [source] | [date] | High/Med/Low |

**Assumptions** (if TAM unvalidated):

- [assumption 1]
- [assumption 2]

## 6. Risks

- **Crowded category**: [assessment]
- **Incumbent response**: [assessment]
- **Switching costs**: [assessment]

## 7. Receipts

Sources used:

- [all URLs, documents, and databases queried]

Artifacts created:

- [any files or documents created]
```

## Tool Guidance

Use tools to gather evidence. Do not ask the user for information that tools can provide.

| Tool      | When to Use                                                                                                            |
| --------- | ---------------------------------------------------------------------------------------------------------------------- |
| Exa       | Market reports, TAM validation, analyst coverage, competitor discovery, and unstructured sector intelligence           |
| Firecrawl | Competitor website scraping for pricing pages, feature lists, about pages, and case studies                            |
| Dealroom  | Funding activity mapping, round history, investor context, and comparable financing data when connected                |
| Harmonic  | Startup discovery, founder context, and company-level structured enrichment when additional startup coverage is needed |

### Tool Sequencing

**Phase 1 — Discovery** (Dealroom when connected + Harmonic + Exa):
Generate the deduplicated competitor list and classify it into 3 buckets.

**Phase 2 — Enrichment** (Firecrawl + Exa):
Populate positioning, pricing, differentiation, and evidence.

**Phase 3 — Analysis** (Exa + supporting evidence):
Write the wedge narrative, moat hypotheses, risk assessment, and TAM validation.

If an existing Company Research & Enrichment profile exists, use it as the starting
point rather than re-researching from scratch.

## Guardrails

- **No fake market sizing.** TAM / SAM / SOM must be sourced or clearly flagged as
  assumptions.
- **Unverified over omission.** Early-stage market data is often incomplete.
- **Geographic diversity is a quality gate.** Include relevant UK/EU peers when
  the investment mandate or company market makes them relevant.
- **Evidence, not assertions.** Every moat hypothesis needs evidence for and against.
- **The wedge is not the vision.** Keep the analysis focused on the specific beachhead.
- **Do not change system-of-record fields** in Affinity or the CRM without approval.
- **Receipts are mandatory.** Every output includes a Receipts section.

## Where This Fits

The Market Map is one of the parallel diligence artifacts produced during the
Evaluation stage. It feeds directly into IC Memo Section 5 (Market + Competitive
Landscape).

```text
Founder Materials (deck, data room, transcripts)
    |
    v
[traction-and-saas-unit-economics] ---------> B3 Traction KPI Worksheet
[market-map-building] ----------------------> B4 Market Map          <-- THIS SKILL
[team-and-hiring-assessment] --------------> Team Table
[red-flags-scanner] -----------------------> B5 Red Flags Checklist
[82-factor-diligence-question-generation] -> Question Bank (82-factor)
    |
    all linked from
    v
B1 Deal Snapshot (canonical index)
    |
    feeds into
    v
B6 IC Memo (Section 5 = Market + competitive landscape)
```

## Related Skills

- `company-research-and-enrichment` — foundation data and company context
- `traction-and-saas-unit-economics` — traction signals that validate market position claims
- `red-flags-scanner` — structured risk scan that complements the Risks section
- `ten-factor-evaluation` — Factor 7 is the lightweight screening version; this skill
  provides the deep evaluation version
