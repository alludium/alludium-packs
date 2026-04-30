---
id: red-flags-scanner
name: Red Flags Scanner
description: >
  Systematically scan an investment opportunity for warning signals across five categories:
  Integrity/Consistency, Team, Market, Traction, and Legal/Compliance. Use this skill when
  building a risk register for a deal, scanning founder materials for internal contradictions,
  running external background checks on founders and companies, checking corporate hygiene
  signals, producing a ranked flag table with severity and recommended validation steps, or
  preparing the risk input for an IC memo.
tags:
  - vc
  - diligence
  - risk
  - red-flags
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: recommended
      required: false
      note: Red-flag scanning is strongest with founder materials, deal artifacts, research tools, and reliable external sources. Provider-specific tool IDs are intentionally omitted because the evidence packet may come from several configured surfaces.
      gracefulDegradation: Scan provided materials only and mark unverified external checks as unavailable.
    - kind: setup
      importance: recommended
      required: false
      owner: user
      ownerPath: Provide deal artifacts or route external-source access through owned setup paths before claiming verification.
      confirmationRequired: true
      gracefulDegradation: Return risks as hypotheses with validation steps, not conclusions.
  routingHints:
    preferredSurface: skill
    notes:
      - Red flags inform validation; this skill does not make pass/invest decisions or mutate deal state.
---

# Red Flags Scanner

Scan an investment opportunity for warning signals and produce a ranked, evidence-backed risk
register. The goal is detection with calibration — surface what needs attention, classify its
severity, and recommend the next validation step.

This skill is for structured risk scanning — not for making invest/pass decisions, not for
writing the IC memo, and not for deep legal review.

## Critical Guardrail

**Red flags inform, not kill.** Every flag recommends a validation step — not automatic deal
termination. A flag at any severity means "investigate further," not "walk away." Only the
investment team decides whether a pattern of flags changes the deal outcome.

## Minimum Inputs

Before running the scan, confirm there is enough material to do meaningful work:

- A pitch deck, or
- Founder notes / first-call notes, or
- A Deal Snapshot with linked materials

If none exist, stop and ask for the minimum missing input rather than guessing.

## Core Method

1. Confirm minimum input exists.
2. Gather evidence from founder materials, call notes, company website, existing Deal Room
   artifacts, and external sources via tools.
3. Scan across all five categories (detailed below). For each flag detected:
   - **Flag** — name the specific warning signal.
   - **Category** — which of the five categories it belongs to.
   - **Severity** — High, Medium, or Low (see classification guidance below).
   - **Evidence** — cite the source: slide number, doc link, URL, or transcript timestamp.
   - **Confidence** — High, Medium, or Low (how strong is the evidence for this flag).
   - **Recommended Action** — one concrete next step to validate or resolve.
4. Check for cross-category patterns. If multiple flags reinforce the same underlying concern,
   call out the pattern explicitly.
5. Produce the output: flag table, pattern summary, and escalation recommendations.

## The Five Scanning Categories

### 1. Integrity / Consistency

Scan founder materials for internal contradictions and credibility signals.

**Specific flags:**

- Conflicting metrics across slides (e.g., revenue on slide 5 differs from slide 12).
- Missing time periods or definitions (e.g., "MRR" without specifying the month).
- "Too perfect" projections without stated assumptions.
- Deck claims vs external evidence mismatch (for example, stated customer count vs what
  cited public-web evidence or press coverage suggests).
- Stated metrics vs cited third-party data inconsistency where trustworthy external
  estimates are available.

**How to detect contradictions:**

- Cross-reference every quantitative claim in the deck against other slides, call notes,
  and external sources. Build a claims table if three or more numbers are involved.
- When the deck says X and reality suggests Y, do not resolve the contradiction — flag it,
  present both data points with sources, and recommend a founder question.
- Pay special attention to revenue, growth rate, customer count, and team size — these are
  the most commonly overstated metrics.

### 2. Team

Scan for team composition risks and founder credibility signals.

**Specific flags:**

- Role gaps not acknowledged (e.g., no CTO for a deep-tech company, no commercial hire
  for a sales-led GTM).
- Unclear founder-market fit (founders lack domain experience and no explanation of how
  they compensate).
- Reputation risk with credible evidence (e.g., prior lawsuits, fraud allegations,
  regulatory sanctions — only flag with verifiable sources).
- Career-history inconsistencies across founder materials, official bios, Harmonic, and
  cited public sources.
- Credible public reporting suggesting leadership or culture problems.

**Important:** Label negative personal findings as "Allegation / report" with the source.
Do not assert guilt. Use cautious, factual language.

### 3. Market

Scan for market viability and positioning risks.

**Specific flags:**

- Tiny niche with no expansion path (TAM too small for venture-scale returns and no
  credible adjacent market play).
- Incumbents already solving the problem with bundling advantage (the startup's feature
  is a checkbox for a larger player).
- Fabricated or unsourced TAM/SAM/SOM numbers (market sizing with no methodology or
  credible source).
- "Why now" is missing or unconvincing (no clear shift in behaviour, regulation, or
  technology creating a window).

### 4. Traction

Scan for evidence quality and metric credibility.

**Specific flags:**

- Vanity metrics without retention or usage data (e.g., "10,000 signups" with no
  activation or retention numbers).
- Lack of customer proof where stage warrants it (e.g., Series A company with no
  referenceable customers).
- Revenue claims without supporting breakdown (no cohort data, no churn visibility,
  no unit economics).
- Growth narrative unsupported by data (e.g., "hockey stick growth" but only two
  data points shown).
- Evidence the deal is widely shopped, stale, or over-brokered, such as repeated
  investor passes, unusually broad outreach, stale fundraising narratives, or
  inconsistent process timing across sources.

### 5. Legal / Compliance

Scan for legal, structural, and regulatory risks.

**Specific legal/compliance flags:**

- IP assignment problems (founders or key engineers have not assigned IP to the company).
- Regulatory risk not acknowledged (operating in a regulated space with no mention of
  compliance approach).
- Aggressive or unusual NDA/term sheet terms.

**Additional flags from 82-Factor legal DD:**

- Cap table consistency issues (ownership percentages do not add up, option pool not
  specified, unclear SAFE/note conversion terms).
- Litigation or adverse media (pending lawsuits, regulatory actions, or credible
  negative press involving the company or founders).
- Corporate filings gaps (company not properly incorporated, missing annual filings,
  jurisdiction concerns).
- Key contract risks (customer concentration, single-vendor dependency, unfavorable
  terms with major partners).
- Open-source license risks (core product built on copyleft-licensed code without
  proper compliance, or license incompatibilities in the stack).

## Severity Classification

Assign severity based on potential deal impact, not just the flag's existence.

**High** — Could materially change the investment decision if confirmed. Requires
resolution before proceeding to IC. Examples:

- Founder involved in active litigation related to the business.
- Revenue numbers contradicted by multiple independent sources.
- IP not assigned to the company.
- Cap table arithmetic does not work.

**Medium** — Warrants investigation and a clear answer but does not block the deal
process on its own. Examples:

- Credible public reporting suggesting a pattern of leadership complaints.
- Missing time periods on key metrics (could be oversight or intentional).
- No regulatory compliance discussion for a regulated market.
- Key role gap with no hiring plan.

**Low** — Worth noting and monitoring but unlikely to change the outcome. Examples:

- Minor inconsistency between deck versions (likely a stale slide).
- TAM methodology is weak but directionally reasonable.
- Corporate website missing a security/privacy page.
- Single negative press mention with no corroboration.

**When in doubt, classify one level higher and note the uncertainty.** It is better to
investigate a Medium flag that turns out benign than to miss a High flag classified as Low.

## Handling Cross-Source Contradictions

When information from different sources conflicts:

1. **Name both sources explicitly.** "Deck slide 7 states MRR of $50K; the founder said
   $35K on the first call (timestamp 14:22)."
2. **Do not resolve the contradiction.** Present both data points side by side.
3. **Classify the severity** based on the magnitude and materiality of the discrepancy.
4. **Recommend a specific question.** "Ask founder to reconcile the MRR figure — which
   number is current and what accounts for the difference?"
5. **Note if a pattern exists.** If multiple claims from the same source are contradicted,
   flag that as a separate Integrity pattern.

## External Scanning

Use tools to gather evidence beyond founder materials. Do not ask the user for information
that tools can provide.

### Founder and Company Background

- Search for litigation, regulatory actions, sanctions, and prior bankruptcies.
- Search for major customer complaints, security incidents, and data breaches.
- Search for negative press, controversy, and adverse media involving the company or
  key founders.
- Check founder history: prior companies, outcomes, any public disputes.

### Corporate Hygiene Signals

When external data is accessible, check:

- Incorporation jurisdiction and filing status.
- Website legitimacy (real product pages, not just a landing page).
- Product demo availability or evidence of a working product.
- Security page, privacy policy, and terms of service.

### Signal Calibration

- If evidence comes from a low-quality or unverifiable source, mark the flag as
  **Low confidence** and recommend confirmation before escalating.
- If a potential legal/compliance issue is detected, recommend counsel review — do not
  attempt legal analysis.
- Negative information about individuals must be labeled as "Allegation / report" with
  the source. Do not assert guilt or wrongdoing.

## Output Shape

```
# Red Flags Scan: [Company Name]

## Summary

Flags found: X total (X High / X Medium / X Low)
Patterns: [1-2 sentence summary of any cross-category patterns]
Escalation needed: [Yes/No — Yes if any High flags require counsel or specialist review]

## Flag Table

| # | Category | Flag | Severity | Evidence | Confidence | Recommended Action |
|---|----------|------|----------|----------|------------|--------------------|
| 1 | Integrity | [specific flag] | High | [source] | High | [action] |
| 2 | Team | [specific flag] | Medium | [source] | Medium | [action] |
| ... | ... | ... | ... | ... | ... | ... |

## Detail by Category

### Integrity / Consistency
[For each flag in this category: evidence summary, why it matters, recommended question]

### Team
[...]

### Market
[...]

### Traction
[...]

### Legal / Compliance
[...]

## Cross-Category Patterns
[If multiple flags point to the same underlying concern, describe the pattern]

## Shopped Deal Signals
[List any evidence that the process is widely shopped, stale, or over-brokered. If none
were checked or found, state that explicitly.]

## Escalation Recommendations
[Any flags requiring legal counsel, specialist review, or immediate founder discussion]

## Clean Areas
[Categories or sub-areas where no flags were found — explicitly noting what was checked
and came back clean provides signal too]
```

## Tool Guidance

Use tools to gather evidence. Do not ask the user for information that tools can provide.

| Tool                           | When to Use                                                                                                                         |
| ------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------- |
| Exa                            | Negative press, founder history, prior company outcomes, public disputes, and cited third-party evidence                            |
| Brave / SerpAPI                | Public-search fallback for adverse media, litigation mentions, and source triangulation                                             |
| Dealroom / private-market data | Funding-process, investor, comparable financing, and transaction context when connected; useful for shopped-deal signal calibration |
| Firecrawl                      | Company website legitimacy, security/privacy pages, product evidence, and official-site contradictions                              |
| Harmonic                       | Structured company and team context to compare against founder materials                                                            |
| Affinity                       | Existing firm notes, prior interactions, and internal context that may surface contradictions                                       |

If an existing Company Research & Enrichment profile or Ten-Factor Evaluation exists, use
them as starting points — do not duplicate work already done.

## Guardrails

- **Red flags inform, not kill.** Every flag must include a validation step. No flag
  automatically means Pass.
- **No speculation presented as fact.** Every flag needs evidence or must be labeled as
  a hypothesis requiring confirmation.
- **At least one concrete next action per flag.** "Investigate further" is not a valid
  action. "Ask founder to provide IP assignment agreements" is.
- **Calibrate severity honestly.** Do not inflate severity to appear thorough. Do not
  deflate severity to avoid uncomfortable conversations.
- **Protect personal reputation carefully.** Negative findings about individuals must
  cite sources, use cautious language, and be restricted to internal outputs.
- **Do not fabricate evidence or cite unverified sources.**
- **Do not make CRM changes** from this skill unless explicitly approved by the
  invoking workflow.
- **Log all external sources checked** in the Clean Areas section, even when nothing
  was found — absence of evidence is still useful signal.

## Related Skills

This skill works well with:

- `ten-factor-evaluation` — red flags feed directly into Factor 9 (Risks) scoring
- `team-and-hiring-assessment` — deeper team analysis when Team flags are raised
- `82-factor-diligence-question-generation` — converts flag recommended actions into
  structured diligence questions
- `citation-enforcement` — validates that flag evidence meets citation standards
- `company-research-and-enrichment` — foundation data and external signals
- `ic-memo-assembly` — red flags output feeds Section 10 (Risks & Mitigations)
