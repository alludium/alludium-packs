---
id: vc.document.origination_pipeline_sop
title: Origination Pipeline Operating SOP
documentType: sop
supportedProjectTypes:
  - vc_origination_pipeline
  - vc_sourcing_line
  - vc_origination_candidate
summary: Operating method for standing venture sourcing pipelines.
---

# Origination Pipeline Operating SOP

## Purpose

Use this SOP to operate a standing sourcing machine without collapsing provider configuration, repeatable experiments, and company progression into one project.

- The **Origination Pipeline** is the fund-level control plane for shared source connections, policy, budgets, cross-line Inbox, and reporting.
- A **Sourcing Line** is one measurable experiment: source mix, query or screen, cadence, review policy, and outreach boundary. It owns schedules and run receipts.
- An **Origination Candidate** is one deduplicated pre-deal company. It owns multi-line provenance, evidence, review decisions, relationship context, outreach state, and promotion.

Deal Pipeline work starts only after a candidate is promoted or a partner explicitly creates an opportunity workspace.

## Workflow

| Step | Output | Approval Gate |
| --- | --- | --- |
| Configure shared sources, thesis, aggregate budgets, review policy, and promotion policy on the hub | Source registry and control-plane policy | Human confirms connection scope and shared controls |
| Start a minimal draft Sourcing Line and continue in its canonical chat | Native hub-to-line relationship and line proposal | Human approves the line configuration before it moves to paused |
| Enable reviewed line schedules and run source methods | Line-scoped run receipt, source state, cost, and candidate proposals | Human approves schedule enablement, paid reads, and limits |
| Deduplicate and register reviewed companies | Origination Candidate with native line provenance | Human resolves ambiguous identity and existing-record matches |
| Enrich, score, screen, and review relationship context | Candidate-specific artifacts and next decision | Human owns Watch, Pass, outreach-ready, and promotion-ready decisions |
| Draft and review outreach experiments | Candidate outreach artifact plus line/message-variant metrics | Human approves each send or an explicitly bounded batch; the pack never auto-sends |
| Aggregate attention across lines and candidates | Hub digest and Inbox | Human chooses follow-up; the digest does not mutate line or candidate state |
| Promote a qualified candidate | Promotion package and candidate-to-deal relationship proposal | Human approves atomic Deal Pipeline creation or linking |

## Source Provenance

Every line run and candidate should preserve the originating project IDs, source family/detail, query or screen version, message variant when relevant, owner, freshness, relationship path, thesis rationale, evidence quality, dedupe state, and promotion rationale. A company found by multiple lines remains one candidate with multiple native line relationships. Promotion carries that trail into the downstream Deal Pipeline.

## Controls

Do not create candidates or Deal Pipelines, mutate CRM records, contact founders, spend on paid sources, or enable recurring schedules without explicit human approval. Compatibility ID fields support rollout but do not replace native project relationships.
