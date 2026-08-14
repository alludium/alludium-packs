---
id: vc.generate_refresh_screening_report
title: Generate or Refresh Screening Report
slug: generate-refresh-screening-report
agent: vc-deal-analyst
skills:
- generate-or-refresh-living-report
- investment-screening-framework
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/generate-refresh-screening-report.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Generate or Refresh Screening Report

## Objective

Generate or refresh the compact evidence-backed Screening Report for one Deal at any active stage.

## What To Do

Apply `generate-or-refresh-living-report` to discover the current project-linked evidence corpus, include any additive focus artifacts, compare the prior evidence basis when refreshing, and preserve the report lifecycle. Use `definitionJson.documentRefs` as the durable criteria, template, style, and operating-guidance contract. Apply the source-neutral Screening Criteria and keep the report compact and decision-oriented. Use the exact active `vc.funds` record matching fund id only as a separate Fund-fit frame. Cite material claims, mark unknowns, render from the Screening Report Template, and return the resulting artifact ID as screening report artifact. Do not record a human investment decision or move stage.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Company Name, Confirmed Fund ID, Focus Artifact IDs, Existing Screening Report.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Deal Pipeline Screening Criteria](../alludium/documents/deal-pipeline/screening-criteria.html): Use as the analysis method.
- [Deal Pipeline Screening Report Template](../alludium/documents/deal-pipeline/screening-report-template.html): Use as the starting structure for the deliverable; adapt it to the facts and avoid generic filler.
- [Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.html): Follow for citations, claim language, assumptions, and evidence quality.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.html): Follow for process boundaries and review standards.

## Deliverable

- Create or update **Screening Report** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.

## Missing Input Policy

Use available evidence and mark unsupported factors unknown; ask only when company identity or readable source material is absent.

## Guardrails

Do not send messages, mutate CRM, create tasks or projects, move stage, or record an investment decision.

## Completion Criteria

- All material screening dimensions are addressed without filler and material claims are cited.
- Fund fit is separate and uses only the exact active configured Fund.
- The shared living-report lifecycle and evidence-basis manifest contract is satisfied.
- The resulting ID is saved to screening report artifact.

## Human Review

- Review the analyst recommendation and make any pass or continue decision separately.
