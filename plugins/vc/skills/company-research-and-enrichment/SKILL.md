---
id: company-research-and-enrichment
name: "Company Research & Enrichment"
description: >
  Build a structured, source-cited company profile from VC data providers. Use this
  skill when you need to resolve a company's identity, enrich it with structured and
  unstructured data, normalise conflicting fields, flag gaps with confidence levels,
  and produce a reusable profile artifact. This is the foundational data-gathering
  skill — screening, diligence, origination, portfolio monitoring, IC prep, and
  outreach all depend on the profile it produces.
tags:
  - vc
  - research
  - enrichment
  - company-profile
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: recommended
      required: false
      note: Company enrichment depends on available research, CRM, structured-data, and web-research tools. Provider-specific tool IDs are intentionally omitted because company context may come from several configured surfaces.
      gracefulDegradation: Use the sources currently available and label missing CRM, structured-provider, or website evidence explicitly.
    - kind: setup
      importance: recommended
      required: false
      owner: user
      ownerPath: Connect or provide the relevant Affinity, Harmonic, Dealroom, Exa, Firecrawl, or artifact context through owned setup paths.
      confirmationRequired: true
      gracefulDegradation: Produce a partial profile with unknown fields and source gaps rather than inventing enrichment.
  routingHints:
    preferredSurface: skill
    notes:
      - The skill is read-oriented and does not mutate CRM or system-of-record fields without an explicit separate owner path.
---

# Company Research & Enrichment

Resolve a company's identity across the connected sources, enrich it into a
structured profile, and surface what is known, what conflicts, and what is
missing. The profile is a reusable artifact consumed by downstream skills.

At minimum, the profile should cover: who the company is, who the founders are,
funding signals, headcount signals, market context, and receipts for where each
fact came from.

## Minimum Inputs

To start, you need at least one of:

- Company name and website domain
- Company LinkedIn URL
- A pitch deck or email containing the company name and enough context to resolve identity

If you have only a company name with no disambiguating identifier, attempt
resolution via Affinity, Harmonic, or the company website. If multiple matches
return, stop and ask the user to confirm which entity before proceeding.

## Source Priority Order

Query sources in this order. Each layer adds evidence the previous ones may lack.

| Priority | Source                        | Why First / Why Here                                                                                                                                                    |
| -------- | ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1        | **Affinity**                  | Check the existing CRM record first. It surfaces prior firm relationship context, notes, pipeline status, and enriched company fields without duplicating work.         |
| 2        | **Harmonic**                  | Primary structured enrichment source for company overview, founders, headcount, growth signals, and related company context.                                            |
| 3        | **Dealroom (when connected)** | Secondary structured source for round history, investor context, comparable financings, and company intelligence when Affinity-enriched or Harmonic data is incomplete. |
| 4        | **Exa**                       | Public-web research layer for market context, recent press, competitor discovery, founder history, and qualitative validation.                                          |
| 5        | **Brave / SerpAPI**           | Broad search coverage for current news, hard-to-find public references, and source triangulation when Exa does not return enough coverage.                              |
| 6        | **Firecrawl**                 | First-party website extraction for product detail, pricing, team pages, security/compliance pages, and careers pages.                                                   |

You do not need to query every source for every profile. Stop when the profile is
complete enough for the requesting workflow. If Dealroom is not connected, fall
back to Affinity-enriched fields, Harmonic, Exa, and Firecrawl, and mark missing
structured fields as `Unknown`.

## Core Method

1. **Resolve identity.** Confirm the company exists and is unambiguous. Start with
   Affinity and Harmonic. Use the official domain and existing artifacts to
   disambiguate. If Affinity already has a record, anchor to that entity.
2. **Check Affinity first.** Capture CRM status, prior notes, pipeline status, and
   relationship context if available. Do not assume warm relationship strength data
   exists in every agent.
3. **Structured enrichment.** Query Harmonic, then Affinity enriched fields, then
   Dealroom if connected. For each output field, record which source supplied the
   value. If a source returns nothing, move to the next.
4. **Qualitative enrichment.** Use Exa for market context, competitive landscape,
   regulatory signals, founder history, and recent press. Use Firecrawl for the
   company's own website, pricing pages, team page, careers page, and security or
   compliance pages.
5. **Normalise and reconcile.** When sources disagree, apply the conflict rules
   below.
6. **Flag gaps.** Every missing field should be marked with a confidence level and
   a suggested next step to fill it.
7. **Produce the profile artifact.**

This artifact should be immediately useful for first-pass screening, meeting prep,
and downstream diligence even before deeper work starts.

## Handling Conflicting Data

Sources frequently disagree on funding amounts, headcount, founding dates, and
company descriptions. When they do:

1. **Prefer the most authoritative source for that field type.**

   - Funding amounts and investor history: Affinity enriched > Dealroom > Harmonic
   - Headcount and growth trends: Harmonic > Affinity enriched > official website
   - Market positioning and ecosystem: Exa > official website > Harmonic
   - Team backgrounds: Harmonic > official bios / cited public profiles > founder materials
   - Product detail and pricing: official website via Firecrawl > founder materials > Exa

2. **Never silently pick one value.** Record all conflicting values, which source
   each came from, and which you selected as primary.
3. **If the conflict is material** (for example, a materially different round size
   or founding date), escalate it as a validation question in the gaps section.
4. **Recency matters.** When two sources are equally authoritative, prefer the more
   recently updated value and note the timestamp if available.

## Confidence Levels

Every field in the profile carries a confidence tag:

| Level      | Meaning                                                                  | When to Use                                                                                                      |
| ---------- | ------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------- |
| **High**   | Corroborated by 2+ sources or from a single authoritative primary source | Official company website for product and pricing, or funding confirmed by structured data plus founder materials |
| **Medium** | Single structured source, no contradiction                               | Harmonic headcount or Affinity-enriched location with no conflicting signal                                      |
| **Low**    | Inferred or supported only by a single secondary / public-web source     | Press article describing revenue, or a public founder bio not corroborated elsewhere                             |
| **Gap**    | No data from any source                                                  | Mark the field, note which sources were checked, and suggest how to fill it                                      |

When a downstream skill encounters a Gap-level field that matters to a decision,
it should flag it as `Unknown` rather than guessing.

## Output Format

The profile maps to the firm's Deal Snapshot fields where applicable.

```markdown
# Company Profile: [Company Name]

Generated: [date]
Sources queried: [list of sources actually queried]
Requested by: [skill or workflow that triggered this]

---

## Identity

| Field                     | Value | Source | Confidence |
| ------------------------- | ----- | ------ | ---------- |
| Company name              |       |        |            |
| Legal name                |       |        |            |
| Website                   |       |        |            |
| LinkedIn URL              |       |        |            |
| Structured company source |       |        |            |
| Location / HQ             |       |        |            |
| Founded                   |       |        |            |
| Stage                     |       |        |            |
| Operating status          |       |        |            |
| One-liner                 |       |        |            |

## Firm Relationship Context

- Affinity record: [exists / not found]
- Pipeline status: [stage if exists]
- Prior interactions: [summary of notes, emails, meetings]
- Relationship context: [relevant internal context if available]
- Source / Referrer: [if known]

## What They Do

[3 bullets — synthesised from structured descriptions and website]

## Team

| Name        | Role | Background                                | Source | Confidence |
| ----------- | ---- | ----------------------------------------- | ------ | ---------- |
| [Founder 1] | CEO  | [education, prior companies, prior exits] |        |            |
| [Founder 2] | CTO  | [...]                                     |        |            |
| ...         |      |                                           |        |            |

- Total headcount: [number] ([source], [trend if available])
- Engineering headcount: [number] ([source] or Unknown)
- Key hires (last 6 months): [only if supported by cited evidence]
- Hiring signals: [official careers-page evidence if available, otherwise Unknown]

## Funding

| Round | Date | Amount | Lead Investor | Other Investors | Source | Confidence |
| ----- | ---- | ------ | ------------- | --------------- | ------ | ---------- |
|       |      |        |               |                 |        |            |

- Total raised: [amount] ([source] or Unknown)
- Last round: [type + date]
- Current raise: [if known — amount, stage, target ownership]
- Investor quality signals: [notable investors if supported]

## Product & Traction

- Product description: [from website + structured sources]
- Customer type: [B2B / B2C / B2B2C]
- Key metrics: [MRR/ARR, growth rate, users — whatever is available]
- Web traffic: [only if provided by a connected source, otherwise Unknown]
- Tech stack: [if available]

## Market & Competition

- Market / sector: [primary category]
- Market size signals: [TAM/SAM if available, with source]
- Ecosystem positioning: [market context from Exa / Harmonic if available]
- Key competitors: [list with positioning notes]
- Competitive differentiation: [from company materials + research]

## Risks & Signals

- Negative press: [any concerning coverage]
- Regulatory exposure: [if relevant to sector]
- Red flags: [any material conflicts or concerns surfaced during enrichment]

## Data Gaps

| Field        | Sources Checked                  | Suggested Action                                |
| ------------ | -------------------------------- | ----------------------------------------------- |
| [field name] | [which sources returned nothing] | [ask founder / request artifact / verify later] |

## Conflicts Log

| Field | Source A (value) | Source B (value) | Selected | Rationale |
| ----- | ---------------- | ---------------- | -------- | --------- |
|       |                  |                  |          |           |

## Receipts

- Sources queried: [list]
- Artifacts referenced: [deck, docs, notes, URLs]
- Suggested downstream uses: [ten-factor, meeting prep, outreach, etc.]
```

## Depth Levels

Match effort to purpose:

| Depth        | When                                  | What to Query                                                    |
| ------------ | ------------------------------------- | ---------------------------------------------------------------- |
| **Quick**    | Origination check, triage             | Affinity + Harmonic, then official website if needed             |
| **Standard** | Ten-factor screening, first-call prep | Affinity + Harmonic + Dealroom if connected + Exa                |
| **Deep**     | IC prep, deep diligence               | All relevant sources including Firecrawl and deeper Exa research |

If the requesting workflow does not specify depth, default to Standard.

## Tool Guidance

| Tool            | Primary Use                                                 | Key Operations                                                                                                    |
| --------------- | ----------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| Affinity        | CRM check, relationship context, enriched fields            | Company lookup, existing notes, pipeline status, enriched company fields                                          |
| Harmonic        | Structured company + team enrichment                        | Company enrichment, employee/team context, related-company discovery                                              |
| Dealroom        | Funding validation, investor context, comparable financings | Structured round history, investor context, sector activity when connected                                        |
| Exa             | Public-web research                                         | `web_search_exa`, `company_research_exa`, `web_search_advanced_exa`, `people_search_exa`, deep research workflows |
| Brave / SerpAPI | Broad search fallback and triangulation                     | Current news, hard-to-find public references, search result diversity, and source triangulation                   |
| Firecrawl       | First-party website extraction                              | Pricing pages, feature lists, team pages, careers pages, security/compliance pages                                |

## Guardrails

- **CRM before external sources.** Query Affinity first so the profile is anchored in
  the firm's existing context.
- **Do not block on Dealroom.** If Dealroom is not connected, continue with the other
  sources and mark the missing structured fields as `Unknown`.
- **Cite every value.** A field without a source is not decision-grade.
- **Do not write to Affinity from this skill.** This skill is read-only.
- **Do not contact founders or external parties.** Outreach is handled elsewhere.
- **Respect depth boundaries.** Do not run deep research if quick enrichment is enough.
- **Log empty checks.** A useful gap report records which sources were checked and
  returned nothing.

## Related Skills

- `ten-factor-evaluation` — primary consumer; uses this profile as evidence base
- `market-map-building` — extends the Market & Competition section into a full map
- `team-and-hiring-assessment` — deep-dives on the Team section
- `founder-outreach-and-intro-paths` — uses relationship context for warm intro routing
- `red-flags-scanner` — uses Risks & Signals and Conflicts Log as starting points
- `meeting-prep-and-summary` — pulls from this profile for meeting preparation
- `ic-memo-assembly` — consumes the full profile for IC memo population
