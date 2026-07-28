---
id: vc.run_vc_sourcing_pipeline
title: Run Sourcing Line
slug: run-vc-sourcing-pipeline
agent: vc-sourcing-operator
skills:
- origination-pipeline-orchestration
- vc-source-registry-and-state-management
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/run-vc-sourcing-pipeline.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Run Sourcing Line

## Objective

Execute one configured Sourcing Line experiment across its approved sources with line-scoped receipts, cost gates, candidate proposals, and human approval boundaries.

## What To Do

Run only sources referenced by this Sourcing Line and apply its query or screen, cadence policy, cursor/window, result limit, budget, Inbox threshold, and review policy. Preserve the reference workflow order across Companies House recent and mature windows, GitHub builder signals, X/Twitter builder signals, cheap enrichment, Affinity relationship check, first verdict, LinkedIn company enrichment only for Meet or Watch, second verdict for fresh LinkedIn company data, sync proposal, portfolio-overlap review, screen, outreach drafts, and digest. LinkedIn people discovery is weekly by default or explicit override only. Create child tasks for the enabled steps; keep each child within its own source/action boundary. Emit each `candidateCreationProposals` item as `{ fieldValues, sourceRefs, relationships, attention }`; relationships must contain `{ direction: "incoming", relatedProjectId: sourcing_line_project_id, relationshipTypeKey: "vc.sourcing_line_originated_candidate", metadata }`, and attention must contain an evidence-backed reason and deterministic rank. These are review proposals, not completed project creations.

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
- Also include a short human-readable summary covering: Run Status, New Candidates Count, Promotion Ready Count, Run Completed At, Candidate Creation Proposals. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for the line definition, registered source keys, cadence policy, budget cap, result limits, review thresholds, and credential readiness before running. If paid-source budget is missing, run only no-cost previews or produce a dry-run plan.

## Guardrails

Read, score, draft, and propose only unless a child task has explicit human approval for the specific write. Do not send outreach, silently update CRM/manual decisions, or create Deal Pipeline projects.

## Completion Criteria

- Run receipt lists enabled sources, skipped sources, cadence mode, result limits, cost metadata or missing cost metadata, and degraded-source notes.
- Run status is one of dry_run, completed, partial, blocked, or failed.
- Receipt identifies the Sourcing Line project, parent pipeline, template or custom hypothesis, screen version, and message variant when applicable.
- Candidate counts are split by source, new, duplicate, rejected, enriched, Meet, Watch, Pass, screened, outreach-drafted, and promotion-ready where available.
- Source-state update includes dedupe keys, pagination/offset notes, seen IDs, and unresolved state-store gaps.
- Every proposed candidate includes project field values, source references, the incoming sourcing-line relationship, and an attention reason and rank.
- Candidate creation remains an explicit, approval-gated platform finalization step.
- Follow-up child tasks and human approvals are listed without performing unapproved writes.

## Human Review

- Approve enabling or changing a recurring schedule.
- Approve paid-source actor runs and source-specific result limits.
- Approve sync writes, outreach sending, or Deal Pipeline promotion in separate tasks.
