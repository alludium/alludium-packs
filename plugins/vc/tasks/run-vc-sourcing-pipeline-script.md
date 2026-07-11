---
id: vc.run_vc_sourcing_pipeline_script
title: Run VC Sourcing Pipeline (Deterministic PoC)
slug: run-vc-sourcing-pipeline-script
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/run-vc-sourcing-pipeline-script.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Run VC Sourcing Pipeline (Deterministic PoC)

## Objective

Run the same bounded sourcing stages without an orchestrator model.

## What To Do

Execute fixed logic with no orchestrator LLM: dispatch Brave and SerpAPI source_collection jobs concurrently; retry one failed source once; run normalize_score; run draft_receipt and persist its output; finish. Use the identical worker roles, inputs, budgets, artifacts, count contract, and anomaly envelope as the bare-brain arm. Never silently adapt the fixed policy. Surface degraded coverage and warnings in the receipt.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Sourcing Run Scope, Run Mode.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Deliverable

- Produce a concise, reviewable task response that a human can act on.
- Also include a short human-readable summary covering: Run Status, Run Receipt Result. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Require the frozen KeyWise fixture, both frozen sources, dry-run mode, result limit, and rubric reference.

## Guardrails

Read-only and draft-only. External writes and project or stage mutations are forbidden.

## Completion Criteria

- No orchestrator model request occurred.
- Both sources were dispatched and one failed source was retried at most once.
- Counts reconcile by source, outcome, and Meet, Watch, or Pass tier.
- The persisted receipt states dry-run status, degraded coverage, warnings, and artifact references.

## Human Review

- Review degraded coverage, contradictions, insufficiency, and any proposal to enable external writes.
