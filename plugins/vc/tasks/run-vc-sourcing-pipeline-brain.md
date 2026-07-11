---
id: vc.run_vc_sourcing_pipeline_brain
title: Run VC Sourcing Pipeline (Bare Brain PoC)
slug: run-vc-sourcing-pipeline-brain
agent: orchestrator-minimal
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/run-vc-sourcing-pipeline-brain.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Run VC Sourcing Pipeline (Bare Brain PoC)

## Objective

Orchestrate the frozen read-only sourcing pipeline with a pure decision brain and bounded workers.

## What To Do

Plan, then call orchestrate.delegate once with one source_collection job for Brave and one for SerpAPI. Evaluate only their bounded envelopes. Retry at most one source exactly once only when its status is failed; never retry a completed or warning-only source. Delegate normalize_score with returned result IDs, add the source envelope result counts and compare that sum exactly with the normalize_score total. If they differ, flag and include COUNT_MISMATCH. Then decide accept, flag, or insufficient and delegate draft_receipt with references, reconciled counts, and the decision. The draft_receipt worker persists the receipt. Call orchestrate.finish with decisions and artifact IDs. Never call a connector, artifact read, persistence, domain, or mutation tool from the brain.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Sourcing Run Scope, Run Mode.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Deliverable

- Produce a concise, reviewable task response that a human can act on.
- Also include a short human-readable summary covering: Run Status, Run Receipt Result. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Require the frozen KeyWise fixture, Brave and SerpAPI, dry-run mode, result limit, and rubric reference.

## Guardrails

Read-only and draft-only. External writes and project or stage mutations are forbidden.

## Completion Criteria

- The brain called only orchestrate.delegate and orchestrate.finish.
- Every brain-bound payload was at most 1,500 tokens.
- Exactly one Brave and one SerpAPI source job ran, with at most one retry for one failed source.
- Counts reconcile by source, outcome, and Meet, Watch, or Pass tier.
- The receipt worker persisted an evidence-backed dry-run receipt and returned its artifact ID.
- Outages, zero-yield sources, contradictions, and warnings are surfaced for human review.

## Human Review

- Review degraded coverage, contradictions, insufficiency, and any proposal to enable external writes.
