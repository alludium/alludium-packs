---
id: vc.run_vc_sourcing_pipeline
title: Run VC Sourcing Pipeline
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

# Run VC Sourcing Pipeline

## Objective

Orchestrate one VC origination sourcing pass across approved sources with source-state receipts, cost gates, and human approval boundaries.

## What To Do

When running in a Sourcing Line, call `project.getAgentContext` for the task's exact project and read its persisted fund id; do not trust optional task-seeded Fund context. Require that exact fund id to match one active record in `vc.funds`, use only that Fund mandate, and keep receipts and candidate proposals line-scoped. Never require an Origination Pipeline hub. Run only approved origination sources and preserve the reference workflow order across Companies House recent and mature windows, GitHub builder signals, X/Twitter builder signals, cheap enrichment, Affinity relationship check, first verdict, LinkedIn company enrichment only for Meet or Watch, second verdict for fresh LinkedIn company data, sync proposal, portfolio-overlap review, screen, and outreach drafts. LinkedIn people discovery is weekly by default or explicit override only. Resolve each enabled child definition with `task-definitions.list` and `task-definitions.findById`, then call `task-management.createTaskFromDefinition` with the current sourcing-run task as `parentTaskId`, the exact Sourcing Line as `projectId`, and only the reviewed inputs for that source/action boundary. Do not claim a child exists until the platform supplies the returned task ID, and do not create disabled children. After the run reaches a terminal receipt and the user approves completion, call `project.update` for the exact Sourcing Line with typed field values for last run status, new candidates last run, last run at, latest run receipt artifact, latest candidate batch artifact, and latest source state artifact. Use only terminal output values and platform-returned artifact IDs. Do not mutate on missing inputs, rejected approval, or before child tasks finish. Re-read the exact line through `project.getAgentContext` and report persisted run state only after the read matches.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Sourcing Run Scope, Run Mode.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Candidate Batch Template](../alludium/documents/origination/candidate-batch-template.html): Use as the starting structure for the deliverable; adapt it to the facts and avoid generic filler.
- [Origination Operating SOP](../alludium/documents/origination/origination-pipeline-sop.html): Follow for process boundaries and review standards.
- [Origination Source Strategy Guide](../alludium/documents/origination/origination-source-strategy-guide.html): Use as the analysis method.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.html): Follow for process boundaries and review standards.

## Deliverable

- Create or update **Run Receipt Artifact** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.
- Create or update **Candidate Batch Artifact** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.
- Create or update **Source State Artifact** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.
- Also include a short human-readable summary covering: Run Status, New Candidates Count, Promotion Ready Count, Run Completed At. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Ask for enabled source registry, cadence policy, budget cap, result limits, review thresholds, and credential readiness before running. If paid-source budget is missing, run only no-cost previews or produce a dry-run plan.

## Guardrails

Read, score, draft, and propose only unless a child task has explicit human approval for the specific write. Do not send outreach, silently update CRM/manual decisions, or create Deal Pipeline projects.

## Completion Criteria

- Run receipt lists enabled sources, skipped sources, cadence mode, result limits, cost metadata or missing cost metadata, and degraded-source notes.
- Run status is one of dry_run, completed, partial, blocked, or failed.
- Candidate counts are split by source, new, duplicate, rejected, enriched, Meet, Watch, Pass, screened, outreach-drafted, and promotion-ready where available.
- Source-state update includes dedupe keys, pagination/offset notes, seen IDs, and unresolved state-store gaps.
- Follow-up child tasks and human approvals are listed without performing unapproved writes.

## Human Review

- Approve enabling or changing a recurring schedule.
- Approve paid-source actor runs and source-specific result limits.
- Approve sync writes, outreach sending, or Deal Pipeline promotion in separate tasks.
