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

Apply `generate-or-refresh-living-report` to discover the current project-linked evidence corpus, include any additive focus artifacts, compare the prior evidence basis when refreshing, and preserve the report lifecycle. Use `definitionJson.documentRefs` as the durable criteria, template, style, and operating-guidance contract. Apply the source-neutral Screening Criteria and keep the report compact and decision-oriented. Use the exact active `vc.funds` record matching fund id only as a separate Fund-fit frame. Cite material claims, mark unknowns, render from the Screening Report Template, and return the resulting artifact ID as screening report artifact. Do not record a human investment decision or move stage. Write every visible report section and the task completion summary in investor-facing language. Do not expose runtime field names such as fund id, focus artifacts, or screening report artifact, or internal terms such as "evidence-basis manifest" and "provider-searchable". These names remain valid in tool inputs, structured output keys, and hidden provenance only; preserve source citations, links, artifact IDs and hashes where the source index requires them. Do not copy task completion criteria or template authoring guidance into the report or summary. For a missing, unknown, or inactive Fund, continue company screening and say "No active Fund has been confirmed for this Deal, so Fund fit is not assessed." Record confirmation of an active Fund as a next step without blocking company screening, requesting another approval, or naming a storage field. For a confirmed active Fund, name that Fund and assess only its mandate; do not print the field name. Describe evidence by its reader-facing source title, for example "the pitch deck (searchable)" only if searchability was observed; otherwise describe its actual availability without inventing access or content. Keep the evidence-basis manifest required by the living-report skill hidden, preserving its schema and provenance fields while refreshing the source entries as required by that skill. In "Changes since previous report", distinguish a first report ("This is the first Screening Report; there is no earlier report to compare.") from a readable prior report with no usable source baseline ("The previous report's source history is unavailable, so changes in the supporting evidence cannot be determined."). Do not invent source changes or mention the manifest in visible prose. Before saving or completing, check the visible report and completion summary for leaked field names and internal evidence-processing terminology. Summarize the report's conclusion and material gaps, not its internal bookkeeping.

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
- The shared living-report lifecycle and hidden evidence-basis manifest contract is satisfied.
- Visible report sections and the completion summary use investor-facing Fund and source language; runtime field names and internal evidence-processing terms remain outside visible prose.
- The resulting ID is saved to screening report artifact.

## Human Review

- Review the analyst recommendation and make any pass or continue decision separately.
