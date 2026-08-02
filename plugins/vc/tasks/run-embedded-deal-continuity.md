---
id: vc.run_embedded_deal_continuity
title: Run Embedded Deal Continuity
slug: run-embedded-deal-continuity
agent: vc-evaluation-analyst
skills:
- embedded-deal-continuity
- citation-enforcement
- investment-diligence-question-framework
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/run-embedded-deal-continuity.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Run Embedded Deal Continuity

## Objective

Produce one provisional cited First Look, What Changed, and Next Decision bundle from adapter-supplied evidence and S0/S1 change state.

## What To Do

Apply `vc.embedded-deal-continuity` method version `1.0.0` to the required deal continuity input. Validate the input against `$defs.input` in the method schema before composing. Produce one deal continuity output matching `$defs.output` with all three sections: First Look, What Changed, and Next Decision. Preserve the exact cited claim, source revision, Fund/mandate method revision, S0/S1 consequence, authority, and uncertainty identities supplied by the Platform adapter. Place every change exactly once across added, preserved, stale, superseded, conflicting, and unresolved. Never present stale, superseded, conflicting, or unresolved evidence as current. First Look is provisional and must not claim final investment disposition. Next Decision must be one unresolved question, missing-evidence request, or explicitly human-owned judgment and must not encode an automatic invest/pass disposition, score, or equivalent posture. Set the approval boundary to pending human review with posture and IC export non-authoritative and approve/edit/reject as the only allowed review actions. Do not call providers, fetch private data, invent a general Fund ontology, create predictive scores, send messages, mutate CRM or project state, or export to IC. Return exact contract errors instead of filling missing citation, revision, authority, or uncertainty data.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Deal Continuity Input.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Deliverable

- Produce a concise, reviewable task response that a human can act on.
- Also include a short human-readable summary covering: Deal Continuity Output. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Stop and list the exact schema or reference failures when the versioned input, citation, source revision, authority, uncertainty, Fund/mandate method revision, or S0/S1 consequence is missing or inconsistent.

## Guardrails

Provisional output only. Human approval, edit, rejection, posture recording, IC export, external communication, and project or CRM mutation require separate explicit authority outside this task.

## Completion Criteria

- First Look, What Changed, and Next Decision are present under method version 1.0.0.
- Every output claim and change resolves to supplied citations, revisions, authorities, and uncertainty.
- All six change-state buckets remain explicit and every supplied change appears exactly once.
- Next Decision contains no automatic investment disposition or score.
- The approval boundary remains pending human review and posture and IC export remain non-authoritative.

## Human Review

- Approve, edit, or reject the provisional continuity bundle before any posture or IC export can become authoritative.
- Make every Fund-relative investment judgment, stage movement, external communication, and final investment decision.
