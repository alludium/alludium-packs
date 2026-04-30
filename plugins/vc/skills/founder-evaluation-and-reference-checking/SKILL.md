---
id: founder-evaluation-and-reference-checking
name: Founder Evaluation & Reference Checking
description: >
  Coordinate founder evidence, team context, references, and human-only judgment
  prompts for VC diligence. Use this skill when compiling founder dossiers,
  planning reference calls, summarizing references, checking claims, benchmarking
  founder compensation when evidence exists, or preparing founder-risk inputs for
  team review and IC. It separates verified facts from interpretation and never
  claims character judgment or background verification without evidence.
tags:
  - vc
  - founders
  - references
  - diligence
  - team
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: recommended
      required: false
      note: Founder evaluation depends on founder materials, public profiles, enrichment sources, relationship context, meeting/reference notes, and reliable evidence sources. Provider-specific tool IDs are intentionally omitted because those surfaces vary by workspace.
      gracefulDegradation: Produce a facts/unknowns table and reference plan from supplied materials only.
    - kind: setup
      importance: recommended
      required: false
      owner: user
      ownerPath: Provide founder names, source materials, reference notes, and any approved enrichment or relationship sources.
      confirmationRequired: true
      gracefulDegradation: Avoid unsupported background or character conclusions.
  routingHints:
    preferredSurface: skill
    notes:
      - This skill supports human judgment; it does not make character, integrity, or hiring decisions.
---

# Founder Evaluation & Reference Checking

Build a source-grounded founder evaluation pack.

## Minimum Inputs

- founder names and company
- founder materials, public profile links, or team page
- reference inputs or transcripts if available
- prior task outputs or team assessment
- cap table / equity split / compensation data if those are to be assessed

## Process

1. Build a verified founder fact table.
2. Cross-check role history, prior ventures, claimed achievements, and relationship context.
3. Plan reference calls around unknowns and decision-critical claims.
4. Summarize reference notes with attribution and confidence.
5. Benchmark founder compensation only when compensation data and a credible comparable basis exist.
6. Produce human-only judgment prompts rather than final character conclusions.

## Output Contract

Return:

- `founder_dossier`: verified facts, sources, and confidence
- `claim_check_table`: claim, evidence, contradiction, follow-up
- `reference_plan`: who to speak to, why, and questions
- `reference_summaries`: attributed reference evidence, not gossip
- `founder_compensation_benchmarks`: stage/geography assumptions, source basis, caveats
- `founder_risk_assessment`: evidence-backed risks and validation steps
- `human_only_judgment_prompts`: decisions reserved for partners

## Tool Guidance

Use people/company enrichment, public web research, CRM/relationship context, LinkedIn
or equivalent profile sources, and meeting transcript providers when connected.
Use Affinity as the preferred CRM/relationship-context example when connected, with
Salesforce, HubSpot, Attio, Airtable, Notion, or supplied relationship notes as portable
alternatives. Use Harmonic for structured founder/company enrichment when connected.
Granola, Otter, Fireflies, Zoom/Meet/Teams exports, or supplied notes can all be valid
transcript inputs.

## Boundaries

- Do not infer character from thin evidence.
- Do not present allegations as facts.
- Do not run or claim formal background checks unless the authorized source is connected and results are available.
- Do not contact references, founders, or third parties without explicit approval.
- Do not use compensation benchmarks without clearly stating stage, geography, role, and source limitations.
