---
id: team-and-hiring-assessment
name: "Team & Hiring Assessment"
description: >
  Evaluate founders, leadership, and team composition for VC due diligence. Extract
  team members and roles from founder materials and connected enrichment sources.
  Verify backgrounds. Assess team completeness relative to company stage. Identify
  hiring gaps using first-party evidence where available. Scan for negative signals
  and contradictions. Separate verified facts from interpretation. Use this skill
  when building a team profile for a deal, assessing founder-market fit, evaluating
  leadership gaps before IC, or flagging team-related risks during diligence.
tags:
  - vc
  - diligence
  - team
  - hiring
  - founders
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: recommended
      required: false
      note: Team assessment depends on available founder materials, public-profile research, structured enrichment, and relationship context. Provider-specific tool IDs are intentionally omitted because people/company context may come from several configured surfaces.
      gracefulDegradation: Assess only provided team evidence and mark background, hiring, or relationship gaps explicitly.
    - kind: setup
      importance: recommended
      required: false
      owner: user
      ownerPath: Provide team materials or route Harmonic, Exa, Affinity, or first-party source setup through owned paths.
      confirmationRequired: true
      gracefulDegradation: Separate verified facts from interpretation and avoid unsupported team conclusions.
  routingHints:
    preferredSurface: skill
    notes:
      - This skill evaluates team evidence; CRM or hiring-plan mutations require separate approval and tools.
---

# Team & Hiring Assessment

Produce a structured, evidence-backed assessment of a company's team for VC due
diligence. Extract verifiable facts about each team member, assess completeness
relative to stage, surface hiring signals, and flag risks. Separate what is known
from what is inferred.

This skill covers team extraction, background verification, stage-appropriate
completeness analysis, first-party hiring signals, and team-specific negative
signal scanning. It does not cover broader 10-Factor scoring (use
`ten-factor-evaluation`) or general red-flag analysis beyond team (use
`red-flags-scanner`).

## Minimum Inputs

Before running, confirm sufficient material exists:

- A pitch deck with a team slide, or
- Founder public-profile identifiers or names + company, or
- First-call notes that name key people and roles

If none exist, stop and ask for the minimum missing input.

## Core Method

1. Confirm minimum input exists.
2. Extract the team roster from founder materials (deck, website, data room).
3. Enrich each key person using connected tools.
4. Build the Team Profile Table.
5. Assess team completeness for the company's current stage.
6. Analyse hiring signals from official first-party sources.
7. Run the negative signal scan.
8. Apply the Team Quality Framework (10-Factor and 82-Factor questions).
9. Produce the output artifact.

## Step 1: Team Roster Extraction

Extract every person mentioned in founder materials. For each, capture:

- **Name** (as stated in materials)
- **Role / title** (current)
- **Source** (which slide, page, or document mentions them)

If the deck mentions "team of 12" but only names 3, note the gap explicitly. Do
not invent team members.

If no meaningful team roster exists, start with the founders and explicitly request
an org chart or team list rather than pretending the team is fully visible.

## Step 2: Per-Person Data Extraction

For each key person (founders, C-suite, VP-level, board members), extract:

| Field                       | What to Capture                                                      |
| --------------------------- | -------------------------------------------------------------------- |
| Current role                | Title, scope, full-time / part-time / advisory                       |
| Prior companies             | Company name, role, tenure (start-end), relevance to current venture |
| Prior exits                 | Any acquisitions, IPOs, or notable outcomes at prior companies       |
| Domain expertise            | Specific domain knowledge relevant to the company's market           |
| Education                   | Degrees, institutions, notable programmes (MBA, PhD, YC, etc.)       |
| Tenure at company           | When they joined, whether pre- or post-funding                       |
| Equity / commitment signals | Full-time, vesting, co-founder vs hired executive                    |
| Notable outcomes            | Products shipped, revenue milestones, patents, publications          |

Mark every field with its evidence source. If a field cannot be verified, mark it
`Unverified` with the basis for the claim (for example, `deck slide 8, not
confirmed elsewhere`).

### Cross-Verification Rules

- Cross-check cited public-profile evidence against deck claims. Flag discrepancies.
- If a founder claims `ex-Google` or `ex-McKinsey`, verify the specific role and
  duration. A 6-month internship is materially different from a 5-year senior role.
- If Harmonic, Affinity-enriched fields, founder materials, or cited public sources
  show different titles or company history, flag the inconsistency.
- Require disambiguation when multiple people share a name. Use location + company
  to confirm identity before attributing facts.

## Step 3: Team Table and Hiring Plan

Before deeper assessment, produce the simple team table and hiring-gap view. This is
the core artifact the VC workflow expects.

## Step 4: Team Completeness by Stage

Assess whether the team has the roles it needs for its current stage.

### Pre-Seed / Seed

**Must-have roles:**

- Technical co-founder or CTO (if technical product)
- Commercial founder or CEO with customer access
- At least one founder with deep domain expertise in the target market

**Expected gaps (acceptable):**

- No CFO, Head of People, or dedicated ops
- No VP Sales or Head of Marketing (founder-led sales is normal)
- Board may be founders only

**Warning signals:**

- Solo non-technical founder building a technical product
- Neither founder has sold to the target buyer before
- All founders from the same background (for example, all engineers and no commercial voice)

### Series A

**Must-have roles:**

- CEO with demonstrated ability to hire and lead beyond the founding team
- CTO or VP Engineering managing a growing team
- At least one commercial hire (Head of Sales, VP Growth, or similar)
- Product leadership (may still be founder-led)

**Expected gaps (acceptable):**

- No CFO (fractional is fine)
- Marketing may still be founder-led
- No dedicated People / HR lead

**Warning signals:**

- No non-founder leadership hires after 12+ months post-seed
- CTO is sole engineer with no credible plan to build team
- No commercial hire despite explicit go-to-market ambitions

### Series B and Later

**Must-have roles:**

- Full C-suite or clear path to it
- VP Engineering or equivalent managing the engineering org
- Head of Product
- People / HR function

**Warning signals:**

- Key leadership positions unfilled for 6+ months after fundraise
- Heavy founder concentration with no delegation
- Repeated executive departures at the same level

### Completeness Output

Produce a table:

| Role     | Status | Person | Concern                |
| -------- | ------ | ------ | ---------------------- |
| CEO      | Filled | [Name] | None / [issue]         |
| CTO      | Filled | [Name] | Tenure < 6 months      |
| VP Sales | Gap    | —      | Expected at this stage |
| ...      | ...    | ...    | ...                    |

## Step 5: Hiring Signals

Hiring patterns reveal momentum, burn discipline, and strategic priorities, but only
when supported by trustworthy first-party evidence.

### What to Measure

- **Current open roles**: Count and categorise roles from the company's official
  careers page or other first-party hiring page.
- **Role mix**: Heavy engineering hiring suggests product investment. Heavy sales
  hiring suggests GTM push. Leadership hiring suggests gaps being filled.
- **Time-to-fill**: If a role is still open across multiple dated first-party
  snapshots or company updates, treat that as a possible sign of hiring friction
  or unrealistic expectations.
- **Recent hires**: Note only when supported by cited public evidence from official
  bios, company announcements, or trustworthy public coverage.

### Interpretation Guide

| Signal                   | Positive Read                 | Negative Read                                                          |
| ------------------------ | ----------------------------- | ---------------------------------------------------------------------- |
| 5-10 roles at Series A   | Scaling with fresh capital    | Check whether capital and team maturity support it                     |
| 0 roles post-funding     | Capital efficient             | Stalled hiring or unclear scaling plan                                 |
| All engineering roles    | Deep product investment       | Neglecting GTM                                                         |
| All sales roles          | GTM push                      | Product may be underdeveloped                                          |
| Leadership roles open    | Building out team             | Persistent gaps not being closed                                       |
| Long-open critical roles | Deliberate search for quality | Hard-to-fill role, unattractive proposition, or stalled hiring process |

### Hiring Output

```text
Open roles: [count] ([breakdown by function])
Recent hires (6 months): [count] ([notable names/roles] or Unknown)
Signal: [1-2 sentence interpretation]
Concern: [if any]
```

If there is no official careers page or other trustworthy first-party hiring
evidence, output `Hiring signal unavailable from first-party sources`.

## Founder Compensation Benchmarking

When founder salary, option refresh, or executive compensation data appears in
founder materials, financial models, or closing documents, benchmark it against the
company stage, geography, funding level, and cash runway where reliable comparables
are available. Treat compensation as a diligence signal, not a moral judgement.

- If compensation appears materially high for stage or runway, flag the cash-burn and
  alignment question.
- If compensation appears materially low, flag founder sustainability and hidden
  personal-runway risk.
- If no compensation data is available, state `Founder compensation unknown` and add a
  follow-up question only when it matters for runway, governance, or closing.

## Step 6: Negative Signal Scanning

Scan for team-related risks. Only report verifiable facts with sources. Use cautious
language for allegations.

### What to Scan

**Public-profile / career-history signals:**

- Key departures in the last 12 months where supported by cited evidence
- Short tenures across the leadership team (pattern of < 18 months)
- Title inflation
- Profile inconsistencies vs deck claims

**Public culture / leadership signals (when supported by cited evidence):**

- Credible public reporting suggesting leadership or culture problems
- Repeated negative themes across independent public sources, such as management,
  culture, burnout, or turnover
- A visible deterioration in public reporting or employee sentiment over time
- Pattern severity relative to company stage and source volume

Do not invent ratings, thresholds, or review-site metrics. Use this section only
when there is cited public evidence available through connected tools.

**Background inconsistencies:**

- Education claims that cannot be verified
- Employment history gaps or overlaps
- Prior company failures not disclosed in materials
- Legal issues (litigation, regulatory action, sanctions)

**Co-founder dynamics:**

- Co-founder departure pre-funding
- Equity split that does not match contribution claims
- Conflicting narratives about who founded the company

### Reporting Rules

- Label every finding with its evidence source and a confidence level
  (`Verified` / `Probable` / `Unverified`).
- Label allegations as `Allegation / report` and do not assert guilt.
- If multiple people share a name, confirm identity before attributing any finding.
- Restrict negative findings to internal outputs only.
- If a finding is serious (fraud, sanctions, litigation), recommend escalation to
  counsel rather than drawing conclusions.

## Step 7: Team Quality Framework

Apply team assessment criteria from the 10-Factor Team sub-questions and the
82-Factor Management Due Diligence section.

### 10-Factor Team Sub-Questions

For each, provide a 1-2 sentence evidence-based assessment:

1. **Intelligence** — Do the founders demonstrate analytical depth and learning velocity?
2. **Integrity** — Any signals of dishonesty, inconsistency, or misrepresentation?
3. **Noble purpose** — Are they mission-driven? Is there a genuine `why` beyond financial return?
4. **Leadership** — Can they attract and retain strong people? Evidence of team-building?
5. **Commercial ability** — Can they sell? Evidence of customers, partnerships, or funding?
6. **Market understanding** — Do they deeply understand the buyer, workflow, and pain?
7. **Grit** — Evidence of perseverance through adversity?
8. **Team gel** — Do their skills complement each other? Evidence of prior collaboration?
9. **Diversity** — Diversity of background, perspective, skill set, and network?
10. **Gaps** — What critical skills or roles are missing?
11. **Humility** — Coachability and willingness to listen?

### 82-Factor Management DD

Address these where evidence exists. Do not force answers when data is absent; mark
them as `Unknown`.

- 2.1.1 Top-quality management?
- 2.1.2 Is the management team complete and functional in each critical area?
- 2.1.3 Can top-quality managers be brought in to fill gaps?
- 2.1.5 Has this management team met with success in the past as a team?
- 2.1.6 Are team members committed to long-term success?
- 2.1.7 How does the management team view investors and their involvement?
- 2.2.1 Is each individual member high quality?
- 2.2.2 Are they genuine entrepreneurs?
- 2.2.3 Do they have solid business judgment?
- 2.2.4 Does each member have an impressive and relevant background?
- 2.2.5 Does each member have proper motivation?
- 2.2.6 CEO skills assessment
- 2.2.7 CTO skills assessment
- 2.2.8 CFO skills assessment
- 2.2.9 Business development officer assessment
- 2.2.10 Marketing & sales officer assessment
- 2.2.11 COO skills assessment
- 2.3.1 Strong, diverse, and balanced board of directors?
- 2.3.2 Independently functioning board?
- 2.3.3 Directors able to devote adequate time and attention?
- 2.4.1 Strong, effective, balanced board of advisers?
- 2.5.1 Can co-investors materially aid the company's success?

## Output Shape

```markdown
# Team & Hiring Assessment: [Company Name]

## Team Roster

| Name   | Role             | Tenure        | Background Summary | Evidence |
| ------ | ---------------- | ------------- | ------------------ | -------- |
| [Name] | CEO / Co-founder | [date joined] | [2-3 line summary] | [links]  |
| ...    | ...              | ...           | ...                | ...      |

## Team Completeness / Hiring Plan

| Role | Status | Person | Concern / Gap |
| ---- | ------ | ------ | ------------- |

## Per-Person Profiles

### [Name] — [Role]

- **Prior companies**: [list with roles and tenures]
- **Prior exits**: [if any]
- **Domain expertise**: [specific areas]
- **Education**: [degrees, institutions]
- **Notable outcomes**: [products, milestones]
- **Verification status**: [Verified / Partially verified / Unverified]
- **Evidence**: [links]

## Stage Completeness

Current stage: [Pre-seed / Seed / Series A / Series B+]

| Role | Status | Person | Concern |
| ---- | ------ | ------ | ------- |
| ...  | ...    | ...    | ...     |

Assessment: [2-3 sentences on overall completeness]

## Hiring Signals

- Open roles: [count] ([breakdown]) or `Hiring signal unavailable from first-party sources`
- Recent hires (6 months): [count] ([notable]) or `Unknown`
- Signal: [interpretation]
- Source: [careers page URL or other first-party evidence]

## Founder Compensation

- Status: [Known / Unknown / Not material at this stage]
- Assessment: [stage/runway alignment and any follow-up question]
- Source: [financial model, closing docs, call notes, or Unknown]

## Negative Signals

| Signal    | Severity     | Evidence | Source | Confidence                   |
| --------- | ------------ | -------- | ------ | ---------------------------- |
| [finding] | High/Med/Low | [detail] | [link] | Verified/Probable/Unverified |

## Team Quality Assessment

### 10-Factor Team Evaluation

| #   | Dimension    | Assessment      | Confidence   |
| --- | ------------ | --------------- | ------------ |
| 1   | Intelligence | [1-2 sentences] | High/Med/Low |
| ... | ...          | ...             | ...          |
| 11  | Humility     | ...             | ...          |

### 82-Factor Management DD

| #     | Question                | Answer       | Evidence | Status                   |
| ----- | ----------------------- | ------------ | -------- | ------------------------ |
| 2.1.1 | Top-quality management? | [assessment] | [source] | Answered/Partial/Unknown |
| ...   | ...                     | ...          | ...      | ...                      |

## Key Strengths

[2-3 bullets]

## Key Risks

[2-3 bullets]

## Top Questions to Validate

1. [Highest priority]
2. ...

## Suggested Hiring Plan (6-12 months)

[Roles implied by the company's plan and current gaps]
```

## Tool Guidance

Use tools to gather evidence. Do not ask the user for information that tools can provide.

| Tool            | When to Use                                                                                      |
| --------------- | ------------------------------------------------------------------------------------------------ |
| Harmonic        | Team enrichment, founder backgrounds, prior companies, growth signals, headcount data            |
| Exa             | Founder research, conference talks, prior exits, publications, and cited public-profile evidence |
| Brave / SerpAPI | Public-search fallback for founder references, adverse media, and source triangulation           |
| Firecrawl       | Official team pages, careers pages, leadership bios, and first-party hiring evidence             |
| Affinity        | Prior firm relationship with any team member or company                                          |

### Tool Sequencing

1. Start with deck and founder materials extraction.
2. Run Harmonic enrichment for the company to get structured team data.
3. Use Exa for cited public-profile and founder-history research where Harmonic data is thin.
4. Use Firecrawl for official team pages and careers pages.
5. Use Affinity to check relationship history.

If an existing Company Research & Enrichment profile exists, use it as the starting
point for team data rather than re-extracting.

## Guardrails

- **Facts vs interpretation**: Every background claim needs evidence.
- **No fabrication**: Do not invent public profiles, hiring data, or background details.
- **No review-site assumption**: If there is no trustworthy first-party or cited public
  evidence, state that the signal is unavailable.
- **Negative signal language**: Use `Allegation / report` with source citation.
- **Disambiguation**: If multiple people share a name, confirm identity first.
- **Confidence labels**: Mark every assessment as High / Medium / Low confidence.
- **No CRM writes**: Do not update Affinity or any system of record without approval.
- **Stage-appropriate expectations**: Do not penalise a seed company for lacking a CFO.

## Handling Contradictions

If evidence conflicts, surface it explicitly:

- State both claims with sources.
- Explain why the discrepancy matters.
- Turn it into a validation question.
- If the contradiction suggests credibility risk, flag it clearly but carefully.

Do not resolve contradictions by averaging or choosing the more flattering version.

## Related Skills

- `company-research-and-enrichment` — foundation data and company context
- `red-flags-scanner` — broader risk scan beyond team-specific signals
- `ten-factor-evaluation` — uses team assessment as input for Factor 10 scoring
- `82-factor-diligence-question-generation` — deeper question generation from team unknowns
