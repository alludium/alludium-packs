---
id: vc-sourcing-digest-generation
name: "VC Sourcing Digest Generation"
description: >
  Generate daily, weekly, or monthly origination digests summarizing candidates,
  source health, budget notes, approvals, and review actions.
tags:
  - vc
  - origination
  - digest
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
  routingHints:
    preferredSurface: skill
---

# VC Sourcing Digest Generation

Use this skill after a sourcing run or review batch.

## Digest Sections

Include:

- New `Meet`, `Watch`, and active candidates
- Candidates needing human review
- Candidate counts by source and verdict
- Source failures and degraded-source notes
- Budget/cost notes and missing cost metadata
- Dedupe/quarantine counts
- Outreach drafts prepared, not sent
- Pending approvals for schedules, paid actor runs, sync writes, outreach, or Deal Room promotion

## Cadence

- Daily digest: concise operational view
- Weekly digest: source performance, expensive-source summary, backlog, and notable misses
- Monthly digest: conversion funnel, source yield, cost, and thesis-learning summary

## Boundaries

- Draft digest by default.
- Do not post to Slack, ClickUp, email, or other external channels without explicit approval.
- Do not hide degraded-source or missing-cost warnings.
