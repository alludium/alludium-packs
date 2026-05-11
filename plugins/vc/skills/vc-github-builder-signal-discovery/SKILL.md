---
id: vc-github-builder-signal-discovery
name: "VC GitHub Builder Signal Discovery"
description: >
  Discover technical-founder and AI builder signals from public GitHub users and
  repositories using the reference pipeline's two-pass model.
tags:
  - vc
  - origination
  - github
  - discovery
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: recommended
      required: false
      note: Use GitHub or web-search access when available; otherwise work from supplied repository/profile exports.
      gracefulDegradation: Produce a search plan and mark GitHub access as missing.
  routingHints:
    preferredSurface: skill
    notes:
      - GitHub discovery is read-only and should respect API rate limits.
---

# VC GitHub Builder Signal Discovery

Use this skill to discover public GitHub signals for early technical founders.

## Two-Pass Model

Pass 1 searches users by UK and Ireland location strings, then reviews recently created repositories.

Pass 2 searches repositories by AI, LLM, agent, automation, data, infrastructure, developer-tool, or workflow keywords, then checks owner profile location and product evidence.

## Scoring Signals

Score up:

- UK or Ireland profile/location evidence
- AI/LLM/developer-tool topics and README language
- B2B, enterprise, workflow, integration, security, compliance, or pricing language
- Recent repository creation or meaningful activity
- Stars-per-day or credible external usage signal
- Homepage, docs, demo, pricing, or contact link
- Founder profile evidence outside the repository when available

Score down or reject:

- Tutorial, toy, template, fork-only, coursework, or abandoned repos
- No company/product identity
- No geography signal
- Consultancy or agency positioning unless thesis allows it

## State

Track `full_name`, repository id, owner login, query, lookback window, and rate-limit notes.

## Output

Return repository URL, owner, created date, last activity, stars, topics, language, homepage, founder/location evidence, score reasons, rejection reason, and receipt.

## Boundaries

- Do not create issues, stars, forks, comments, or pull requests.
- Do not contact maintainers.
- Do not sync external records or create Deal Rooms without approval.
