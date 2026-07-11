---
id: vc.run_vc_sourcing_pipeline_delegated
title: Run VC Sourcing Pipeline (Delegated PoC)
slug: run-vc-sourcing-pipeline-delegated
agent: vc-sourcing-operator
skills:
- origination-pipeline-orchestration
- vc-source-registry-and-state-management
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/run-vc-sourcing-pipeline-delegated.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Run VC Sourcing Pipeline (Delegated PoC)

## Objective

Run the read-only VC sourcing PoC across the frozen Brave and SerpAPI source set using bounded Gemini worker jobs.

## What To Do

This is the worker-delegation PoC and is always a dry run. First create a compact source run plan for the frozen Brave and SerpAPI source set. Delegate one source_collection child per source with task-management.delegateWorkerJob; do not pass the parent transcript or raw payloads. When both source summaries are available, call tasks.normalizeWorkerCandidates with the bounded observations, then tasks.draftWorkerRunReceipt. Persist the returned Markdown through the normal artifact creation tool and attach it as the run receipt. Parent/child handoffs contain only artifact IDs, counts, warnings, status, and a summary capped at 1,500 tokens. Never call outreach, messaging, CRM write, sync-write, project creation, or any other mutation tool. Use definitionJson.documentRefs as the durable document contract and preserve evidence references through normalization and receipt drafting.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Sourcing Run Scope, Run Mode.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Candidate Batch Template](../alludium/documents/origination/candidate-batch-template.md): Use as the starting structure for the deliverable; adapt it to the facts and avoid generic filler.
- [Origination Pipeline Operating SOP](../alludium/documents/origination/origination-pipeline-sop.md): Follow for process boundaries and review standards.
- [Origination Source Strategy Guide](../alludium/documents/origination/origination-source-strategy-guide.md): Use as the analysis method.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.md): Follow for process boundaries and review standards.

## Deliverable

- Create or update **Run Receipt Artifact** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.
- Create or update **Candidate Batch Artifact** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.
- Create or update **Source State Artifact** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.
- Also include a short human-readable summary covering: Run Status, New Candidates Count, Promotion Ready Count, Run Completed At. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Require the KeyWise-shaped fixture, the frozen Brave and SerpAPI source set, dry-run mode, result limit, and scoring rubric reference. Stop rather than substituting a different connector.

## Guardrails

Read, score, draft, and create local task artifacts only. No external writes or outreach.

## Completion Criteria

- Exactly one source_collection child exists for Brave and one for SerpAPI.
- Child summaries are at most 1,500 tokens and no child transcript is copied to the parent.
- Candidate counts reconcile with source observations and retain evidence references.
- Run receipt lists enabled sources, skipped sources, degraded-source notes, counts, warnings, and dry-run status.
- No mutation, outreach, messaging, CRM write, sync-write, or project-creation tool was called.

## Human Review

- Approve any later productionization or external write behavior outside this PoC.
