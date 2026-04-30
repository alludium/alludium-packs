---
id: citation-enforcement
name: Citation Enforcement
description: >
  Scan any deal artifact for unsupported or weakly supported claims and produce an
  actionable fix list. Use this skill when reviewing a deck summary, DD workstream output,
  IC memo draft, or any research artifact where factual accuracy matters. It identifies
  four claim types, verifies that adequate support exists, labels confidence, and suggests
  fixes without fabricating evidence.
tags:
  - vc
  - diligence
  - quality
  - citations
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: recommended
      required: false
      note: Citation review is strongest when the agent can inspect the target artifact and supporting sources. Provider-specific tool IDs are intentionally omitted because artifacts and source packets may be supplied through several configured surfaces.
      gracefulDegradation: Review only the provided text and mark claims that cannot be verified from available context.
    - kind: setup
      importance: recommended
      required: false
      owner: user
      ownerPath: Provide the artifact and source packet, or route through the deal workspace owner that can attach them.
      confirmationRequired: true
      gracefulDegradation: Return a source-gap list instead of claiming verification.
  routingHints:
    preferredSurface: skill
    notes:
      - This is a read/review workflow; it does not publish edits or create authoritative citations by itself.
---

# Citation Enforcement

Scan a document for claims that lack adequate source support. Produce a structured report
that makes every unsupported claim visible and gives the author a concrete fix path.

This is a quality gate, not an editing pass. Do not rewrite the document. Flag problems,
suggest fixes, and let the author decide.

## When to Use

- After any DD workstream produces an artifact (traction worksheet, market map, team table,
  red flags scan).
- Before an IC memo is distributed as a pre-read.
- On any deck summary, research output, or briefing where factual claims will influence a
  decision.

## Minimum Inputs

Confirm the document is ready for review:

- The document must have substantive content (not just headings or placeholders).
- If the document is incomplete, return "Not ready for citation review" and state what is
  missing.

## The Four Claim Types

Scan the entire document for these four categories. Every statement that falls into one of
these types requires a citation or explicit assumption label.

### 1. Numerical Claims

Metrics, market sizes, pricing figures, growth rates, financial projections, headcount,
customer counts, or any specific number.

**Identify by**: digits, currency symbols, percentages, multipliers ("3x"), or quantity
words ("$2M ARR", "40% MoM growth", "200 enterprise customers").

**Verify**: the number has an adjacent source pointer (slide number, page reference, doc
link, web URL, or data room file). Check that the cited source actually contains the number
claimed.

### 2. Comparative Claims

Superlatives or relative positioning statements.

**Identify by**: words like "largest", "fastest", "only", "first", "leading", "best-in-class",
"cheaper than", "outperforms", or any claim of relative standing.

**Verify**: the comparison is supported by a named benchmark, third-party source, or explicit
methodology. Deck self-claims ("we are the leading...") without external validation count
as unsupported.

### 3. Externally Sourced Claims

Customer quotes, press references, analyst statements, partnership announcements, or any
claim attributed to a third party.

**Identify by**: attribution language ("according to", "as reported by", "[Customer] said"),
quotation marks, or references to external entities as evidence.

**Verify**: the original source is linked or identifiable. A customer quote without a name,
date, or reference is unsupported. Press mentions need a URL or publication reference.

### 4. High-Stakes Claims

Legal, regulatory, compliance, IP, or financial structure assertions where being wrong
carries material risk.

**Identify by**: legal language, regulatory references, IP claims ("patented", "patent-pending"),
compliance certifications, cap table assertions, or financial commitments.

**Verify**: the claim traces to an official filing, legal document, or authoritative record.
Self-reported claims in this category require explicit labelling as "founder-stated, not
independently verified."

## Scanning Methodology

Work through the document section by section:

1. Read each section and flag every statement matching one of the four claim types.
2. For each flagged statement, check for an adjacent citation (inline link, footnote,
   parenthetical reference, or source column in a table).
3. If a citation exists, verify it is specific enough to locate the source (not just
   "company website" or "industry report" without further detail).
4. If no citation exists or the citation is too vague, add the claim to the Unsupported
   Claims table.
5. After completing the scan, review for patterns (e.g., an entire section with zero
   citations, repeated reliance on a single weak source).

## Data Quality Hierarchy

When evaluating citation quality or suggesting sources, prefer higher-quality sources:

1. **Primary sources** (strongest): SEC filings (10-K, 10-Q, S-1), company financial
   statements, signed contracts, official regulatory filings
2. **Semi-primary**: Earnings call transcripts, founder-provided data rooms, verified
   customer references
3. **Secondary**: Sell-side analyst reports, Gartner/Forrester/IDC reports, Dealroom,
   and PitchBook or similar third-party private-market datasets when they are already
   cited in source materials. Do not assume these are directly queryable unless the
   invoking workflow has that tool connected.
4. **Tertiary** (weakest): Industry blog posts, news articles, social media, undated
   web pages

Label the source tier when it materially affects confidence. A TAM number from a 10-K
is not the same as a TAM number from a blog post.

## Confidence Labelling

For each unsupported claim, assign a priority based on risk:

- **P1 (Must fix)**: Numerical or high-stakes claim with no citation at all, or a claim
  that contradicts other evidence in the document.
- **P2 (Should fix)**: Comparative or externally sourced claim with no citation, or any
  claim citing only tertiary sources for a material assertion.
- **P3 (Improve)**: Claim with a vague citation that could be made more specific, or a
  low-stakes claim missing a source.

## Output Shape

Produce two outputs:

### 1. Unsupported Claims Table

```
| # | Claim | Type | Location | Current Support | Fix Path | Priority |
|---|-------|------|----------|-----------------|----------|----------|
| 1 | "$4.2B TAM by 2027" | Numerical | Market section, para 2 | None | Add source — check Gartner or IDC for category sizing | P1 |
| 2 | "Fastest-growing in category" | Comparative | Product section | Self-reported in deck | Add third-party benchmark or remove superlative | P2 |
| ... | ... | ... | ... | ... | ... | ... |
```

Every row must have a specific fix path. "Add citation" alone is not specific enough.
State what kind of source to look for or recommend removing/qualifying the claim.

### 2. Summary

After the table, provide:

- **Total claims scanned**: count
- **Unsupported**: count by priority (P1 / P2 / P3)
- **Patterns**: any systemic issues (e.g., "Traction section has 8 metrics with zero
  source pointers", "All market sizing relies on a single 2023 blog post")
- **Suggested edits** (optional): for the worst offenders, propose specific rewording
  that removes over-precision, converts to hypothesis language, or adds qualifiers.
  Example: change "$4.2B TAM" to "estimated $4-5B TAM (source needed)" or "founder
  estimates $4.2B TAM (not independently verified)."

## Fix Suggestions Without Fabrication

When suggesting fixes:

- **Never invent a citation.** If you do not have a verified source, say "source needed"
  and describe what kind of source would satisfy the claim.
- **Never link to a URL you have not verified.** Recommend a search strategy instead
  ("check SEC EDGAR for the company's S-1" or "search Gartner for category report").
- **Offer downgrade language.** If a source cannot be found, suggest converting the claim
  to: an assumption ("we assume..."), a hypothesis ("if validated, this would suggest..."),
  or a range ("founder estimates X; independent verification pending").
- **Recommend removal** when a claim adds no value without support. "Largest player in
  the space" with no source is noise — suggest cutting it.

## Tool Guidance

| Source / Tool          | When to Use                                                                                                                                                           |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Attached source packet | Primary context. Most verification comes from cross-referencing within the deal artifact set (deck, data room, call notes, traction worksheet).                       |
| Exa                    | Verify specific factual claims against web sources when document context is insufficient. Search for the exact metric, company name + claim, or market sizing figure. |
| Brave / SerpAPI        | Public-search fallback for claim verification, source triangulation, and hard-to-find current references.                                                             |

Use Exa sparingly and only when the document's own source material cannot confirm or deny
a claim. The goal is to flag gaps, not to do the author's research.

## Guardrails

- Do not rewrite the document. This skill produces a report, not an edited draft.
- Do not add citations you have not verified. Recommend sources rather than fabricating.
- Do not treat all unsupported claims as equal. Use the priority system.
- Do not flag well-known facts that need no citation (e.g., "SaaS companies typically
  use recurring revenue models").
- Do not flag opinions or assessments that are clearly labelled as such.
- If the document is an early draft with known gaps, note that in the summary rather than
  flagging every placeholder.

## Related Skills

- `ic-memo-assembly` — citation enforcement runs as a quality gate before IC distribution
- `red-flags-scanner` — overlaps on integrity/consistency signals; citation enforcement
  is the evidence layer, red flags is the risk layer
- `traction-and-saas-unit-economics` — produces numerical claims that frequently need
  citation enforcement
- `market-map-building` — produces comparative and market sizing claims that are common
  citation gaps
