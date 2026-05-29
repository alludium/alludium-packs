---
id: vc.affinity_sync_write
title: Draft Affinity Write-Back Proposals
slug: affinity-sync-write
agent: vc-integration-operator
skills:
- vc-affinity-sync-write
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-integrations/affinity-sync-write.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Draft Affinity Write-Back Proposals

## Objective

Draft reviewable Affinity note, field, and stage update proposals from VC task outputs.

## What To Do

Draft Affinity write-back proposals only. Each proposal must include the target Affinity object, before value, proposed after value or note text, source evidence, approving owner, and audit note. Reference affinity add note only as an approved execution tool if it is discovered and the runtime approval model is present.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Write-Back Source.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Deliverable

- Produce a concise, reviewable task response that a human can act on.
- Also include a short human-readable summary covering: Affinity Write-Back Proposals. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for the source artifact, target Affinity record, and approval owner before drafting a write-back proposal.

## Guardrails

Draft only. Do not write notes, update fields, move stages, or change list entries.

## Completion Criteria

- Every proposal is evidence-backed and approval-gated.
- The output clearly states no Affinity writes were performed.

## Human Review

- Approve exact write target and content.
- Approve CRM field or stage changes outside this task.
