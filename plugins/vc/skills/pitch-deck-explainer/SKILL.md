---
id: pitch-deck-explainer
name: Pitch Deck Explainer
description: >
  Convert an uploaded or linked pitch deck into a structured, source-grounded
  explanation for VC screening, meeting prep, diligence, or IC work. Use this skill
  when extracting the company's story, claims, metrics, risks, and unanswered
  questions from a deck. It explains and verifies what the deck says; it does not
  invent missing slide content or make investment decisions.
tags:
  - vc
  - pitch-deck
  - screening
  - source-analysis
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: recommended
      required: false
      note: Pitch deck explanation depends on the deck text/images, attached source files, and optional external research for claim checks. Provider-specific tool IDs are intentionally omitted because deck access and public research may come through several configured surfaces.
      gracefulDegradation: Explain only the deck content available and mark unreadable slides or unsupported claims.
    - kind: setup
      importance: recommended
      required: false
      owner: user
      ownerPath: Attach the pitch deck, provide extracted text, or route the deck through the current deal/document owner before explanation.
      confirmationRequired: true
      gracefulDegradation: Return a missing-deck or unreadable-slide report.
  routingHints:
    preferredSurface: skill
    notes:
      - Use this to extract and structure deck claims; downstream skills own screening, diligence, and memo assembly.
---

# Pitch Deck Explainer

Explain a pitch deck as evidence. Separate what the deck claims, what is supported,
what is unclear, and what should be verified next.

## Minimum Inputs

At least one of:

- uploaded or attached pitch deck
- deck text exported from a document repository
- source thread containing deck excerpts
- founder/company materials that substitute for a deck

If the deck is missing or unreadable, stop and ask for the file or extracted text.

## Process

1. Identify the company, stage, round, product, buyer, and ask.
2. Extract claims by topic: problem, product, market, traction, business model, team, competition, terms, and risks.
3. Flag unsupported claims, missing definitions, unclear metrics, and contradictions.
4. Use public research or website extraction only to check claims that matter for the requesting workflow.
5. Produce downstream-ready outputs for screening, meeting prep, diligence, or IC assembly.

## Output Contract

Return:

- `deck_summary`: concise explanation of the company and pitch
- `claims_register`: claim, source slide/section, evidence type, confidence
- `metric_table`: metric, value, time period, definition, source, caveat
- `risks_and_unknowns`: issues requiring follow-up
- `verification_questions`: founder or diligence questions tied to specific claims
- `downstream_context`: what to pass into screening, meeting prep, or memo work

## Tool Guidance

Use attached files or document repository context first. Use Firecrawl for first-party
website checks and Exa, Brave, or SerpAPI for public corroboration where useful.

Do not treat public search as a substitute for deck evidence. External sources can
confirm, contradict, or contextualize claims, but they cannot fill missing founder data.

## Boundaries

- Do not invent unreadable or missing slide content.
- Do not normalize metrics without preserving the founder's original value and unit.
- Do not produce an invest/pass recommendation; hand off to screening or diligence skills.
- Do not create or edit a deck file.
