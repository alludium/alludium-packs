---
id: vc.document.sourcing_line_template_catalog
title: Sourcing Line Template Catalog
documentType: methodology
supportedProjectTypes:
  - vc_origination_pipeline
  - vc_sourcing_line
summary: Starter configurations for repeatable, measurable sourcing experiments.
---

# Sourcing Line Template Catalog

Use these templates as starting hypotheses, not immutable provider recipes. A sourcing line is a repeatable experiment:

`registered source(s) x query or screen x cadence x review policy x outreach policy`

Every instantiated line must receive its own identity, retain the parent Origination Pipeline relationship, start as a minimal draft with its canonical chat, and move to paused only after its configuration proposal is approved. Schedules, paid reads, external writes, and outreach remain disabled until separately approved.

## Template: Thesis Radar

**Starter template key:** `thesis_radar`

Best for broad, persistent coverage of an investment thesis.

- **Source mix:** structured company database plus first-party company sites; optional registry confirmation.
- **Screen/query:** thesis concepts, geography, stage proxies, maturity bounds, and explicit exclusions.
- **Cadence:** weekly full discovery with a daily incremental refresh when the provider supports reliable cursors.
- **Review policy:** surface only novel candidates above the configured thesis-fit threshold; preserve Watch candidates for later refresh.
- **Outreach policy:** disabled by default. A human must move an individual candidate to outreach-ready.
- **Learning question:** Which parts of the thesis produce qualified, previously unknown companies?

## Template: Trigger And Event Watch

**Starter template key:** `trigger_event_watch`

Best for time-sensitive signals such as incorporations, launches, hiring, funding, grants, or regulatory events.

- **Source mix:** event or registry source plus first-party verification.
- **Screen/query:** named triggers, time window, geography, company maturity, and false-positive exclusions.
- **Cadence:** daily or event-driven where supported.
- **Review policy:** freshness and confidence must be shown separately from thesis fit.
- **Outreach policy:** disabled until the trigger is verified and a human approves the candidate.
- **Learning question:** Which observable triggers predict a worthwhile conversation early enough to act?

## Template: Builder-Signal Convergence

**Starter template key:** `builder_signal_convergence`

Best for finding founders through public technical and product-building activity.

- **Source mix:** GitHub or developer ecosystem signals combined with company/founder identity enrichment; optional LinkedIn confirmation.
- **Screen/query:** repository momentum, contributor identity, product intent, geography evidence, and commercial-company indicators.
- **Cadence:** weekly discovery with daily refresh only for a reviewed shortlist.
- **Review policy:** require at least two independent signals before Inbox surfacing; do not infer company formation from repository activity alone.
- **Outreach policy:** draft-only after candidate review. Never auto-send.
- **Learning question:** Which combinations of technical activity and commercial intent lead to qualified founders?

## Template: Ecosystem And Community Scout

**Starter template key:** `ecosystem_community_scout`

Best for discovering emerging founders in public communities, accelerators, events, universities, and specialist forums.

- **Source mix:** community or social source plus independent first-party verification.
- **Screen/query:** named communities, problem statements, founder/building language, geography, recency, and spam exclusions.
- **Cadence:** daily for high-volume feeds or weekly for lower-volume communities.
- **Review policy:** community posts are leads, not verified company facts; require human review for sensitive or ambiguous identity matches.
- **Outreach policy:** respect community norms and do-not-contact policy; draft-only after review.
- **Learning question:** Which communities and signal patterns consistently yield novel, thesis-fit candidates?

## Template: Relationship-Led Reactivation

**Starter template key:** `relationship_reactivation`

Best for revisiting known people and companies when new evidence changes the investment case.

- **Source mix:** CRM/relationship system plus approved public change signals.
- **Screen/query:** prior Watch/Pass records, recontact window, relationship owner, material change, and do-not-contact status.
- **Cadence:** weekly or monthly.
- **Review policy:** preserve human decisions and relationship ownership; require evidence of a material change before resurfacing.
- **Outreach policy:** relationship owner approval is mandatory; no automated send.
- **Learning question:** Which changes justify reopening a prior conversation, and after what interval?

## Template: Targeted Outbound Message Experiment

**Starter template key:** `targeted_outbound_experiment`

Best for learning which cold outreach framing earns a qualified response from a tightly defined cohort.

- **Source mix:** an approved candidate cohort from another sourcing line or a reviewed structured search, plus relationship and do-not-contact checks.
- **Screen/query:** a narrow founder/company cohort with explicit inclusion, exclusion, and sample-size rules.
- **Cadence:** finite experiment batches or a low-volume weekly cohort; never an unbounded send schedule.
- **Review policy:** every candidate and message variant must be reviewable; record assignment, delivery status, reply class, and opt-out.
- **Outreach policy:** draft-only by default. A human approves each send or an explicitly bounded batch; the pack never enables automated sending.
- **Learning question:** Which evidence-backed message proposition and channel produce qualified replies without harming relationships?
- **Minimum metrics:** approved, sent, delivered, replied, qualified reply, meeting, opt-out, cost, and conversion by message variant.

## Required Instantiation Record

For every line, capture:

- Sourcing Line project ID, `line_name`, and an optional stable human-readable key
- `origination_pipeline_project_id`
- `starter_template_key` and the hypothesis being tested
- registered source keys and approved connection scopes
- query/screen definition, exclusions, and evidence requirements
- cadence, timezone, cursor/window policy, result limit, and paid-source budget
- Inbox threshold and review owner
- outreach mode, approval owner, do-not-contact rules, and message experiment if any
- success metrics, baseline, review date, and retirement condition

Templates may be combined, but every active line must still have one coherent learning question and independently measurable results.
