---
id: vc.score_sourcing_candidate
title: Score Sourcing Candidate
slug: score-sourcing-candidate
agent: vc-sourcing-operator
skills:
- vc-sourcing-verdict-and-screening
- vc-sourcing-dedupe-and-novelty-check
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/score-sourcing-candidate.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Score Sourcing Candidate

## Objective

Produce a Fund-specific Meet/Watch/Pass verdict and urgency score for one Candidate in one Sourcing Line context.

## What To Do

Require explicit candidate project id, sourcing line project id, candidate line relationship id, and fund id before scoring. Read the Candidate and relationship, then call `project.getAgentContext` with the exact sourcing line project id and read the current fund id entry from its returned `fieldValues`; do not use the raw project row or task-seeded context for this mutable field. Confirm the relationship is active, has type `vc.sourcing_line_originated_candidate`, and runs from that exact line to that exact Candidate. Confirm the current persisted line fund id equals the supplied ID, then require exact stable-ID equality with one rendered canonical `vc.funds` record whose status is actively investing. Apply that matched record's stage, sectors, geographies, thesis, `minimumCheckSize`, `maximumCheckSize`, currency, exclusions, and `scoringFramework`; never score from another Fund. Every populated matched Fund field is authoritative. Use the generic Pack rubric and optional reviewed task scoring policy only to supply missing, non-conflicting detail; never override or weaken a populated matched Fund field. Mirror the reference pipeline's verdict contract using that Fund and line policy. Score from already-enriched data, separate evidence from inference, and return Meet, Watch, or Pass plus urgency. Apply hard stage safety by passing companies with Series A+ funding or more than 20 employees when reliable LinkedIn company data is present, unless the matched Fund's populated stage, thesis, or scoring framework explicitly allows that later stage or company size. Run the second-pass verdict only for Meet/Watch rows with fresh LinkedIn company data so paid scraping and model cost stay bounded. After producing the scoring artifact, read the relationship again and call `project-relationship.updateMetadata` once. Because that operation replaces metadata, copy every existing key and every existing scoring by fund entry unchanged, then set only `scoring_by_fund[fund_id]` to an object containing `schema_version: vc.sourcing_line_candidate_scoring.v1`, the exact Candidate, line, relationship and Fund IDs, scoring artifact, candidate score, review verdict, thesis fit summary, scored at, and the current task ID. Never write these Fund-relative values to Candidate-wide project fields.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Candidate Project ID, Sourcing Line Project ID, Candidate-Line Relationship ID, Fund ID, Enriched Candidate Batch, Scoring Policy.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Sourcing Scoring Rubric](../alludium/documents/origination/sourcing-scoring-rubric.html): Use as the analysis method.
- [Origination Source Strategy Guide](../alludium/documents/origination/origination-source-strategy-guide.html): Use as the analysis method.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.html): Follow for process boundaries and review standards.

## Deliverable

- Create or update **Scoring Artifact** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.
- Also include a short human-readable summary covering: Meet Candidate Count, Watch Candidate Count, Promotion Ready Count, Scoring Report, Candidate Score, Review Verdict, Thesis Fit Summary, Relationship Scoring Persisted. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Keep scoring incomplete until the exact Candidate project, Sourcing Line project, active provenance relationship, active Fund, enriched evidence, line/Fund policy, LinkedIn data availability, and scoring thresholds are available and mutually consistent.

## Guardrails

The only allowed persistent mutation is replacing metadata on the verified line-candidate relationship while preserving all prior metadata and other Fund entries. Do not update Candidate-wide score fields, sync external records, change manual decisions, send outreach, or create Deal Pipelines.

## Completion Criteria

- The exact Candidate, Sourcing Line, active provenance relationship, and actively-investing Fund are recorded and verified.
- The scored candidate has action, urgency, thesis fit, confidence, funding status, HQ/geography concern, frontier-pedigree evidence, reasons, and receipts for that exact line/Fund context.
- Auto-pass decisions name the specific rule and evidence.
- Second-pass rows are limited to candidates with fresh LinkedIn company data.
- The terminal platform receipt confirms the result was stored only at `relationship.metadata.scoring_by_fund[fund_id]` without removing prior metadata or another Fund entry.
