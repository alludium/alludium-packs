---
id: vc.generate_refresh_evaluation_report
title: Generate or Refresh Evaluation Report
slug: generate-refresh-evaluation-report
agent: vc-deal-analyst
skills:
- generate-or-refresh-living-report
- investment-diligence-question-framework
- market-map-building
- commercial-evaluation-and-market-risk
- technical-evaluation-and-product-risk
- financial-evaluation-and-financing-risk
- team-evaluation-and-founder-risk
- red-flags-scanner
- citation-enforcement
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/generate-refresh-evaluation-report.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Generate or Refresh Evaluation Report

## Objective

Generate or refresh the living evidence-backed Evaluation Report for one Deal at any active stage.

## What To Do

Apply `generate-or-refresh-living-report` to discover the current project-linked evidence corpus, include the mapped Screening Report and any additive focus artifacts, compare the prior evidence basis when refreshing, and preserve the report lifecycle. On refresh, read the existing report only as the comparison baseline and create one new complete report; never edit the earlier report, which stays unchanged as history. Use `definitionJson.documentRefs` as the durable criteria, template, style, and operating-guidance contract. Maintain the Evaluation Report as the living record of evidence, change, open questions, risk, and next work. Apply the source-neutral Evaluation Criteria by decision-useful domain; do not mechanically reproduce a source checklist. Keep Fund thesis as a separate exact-match frame, render from the Evaluation Report Template, and return the resulting artifact ID as evaluation report artifact. Do not record an investment decision or move stage. The company under review is the Deal's confirmed Organisation. company name carries that Organisation's name as the Platform supplied it to this task, and organisation id, when present, identifies it for tool calls only. Do not ask the user to re-enter or confirm a company name, and do not take the company name from the Deal title, which is the opportunity's own name and may differ. Keep the Deal fields current with the Platform Record Field Maintenance skill: read them with `field-values.getFields`, use `field-values.setField` to fill editable empty Deal fields that the evidence in this task clearly supports, and suggest rather than make any change to a populated field. Leave the Fund, lifecycle stage and decision fields, and all People and Organisation records, to the human and the Deal Manager. In the completion summary, name each field you filled or suggest changing by its label. For a suggested change, give the current value and the value the evidence supports, and ask whether to update it; a yes from the human is an explicit request to write it.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Company Name, Confirmed Fund ID, Focus Artifact IDs, Screening Report, Existing Evaluation Report, Confirmed Organisation ID.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Deal Pipeline Evaluation Criteria](../alludium/documents/deal-pipeline/evaluation-criteria.html): Use as the analysis method.
- [Deal Pipeline Evaluation Report Template](../alludium/documents/deal-pipeline/evaluation-report-template.html): Use as the starting structure for the deliverable; adapt it to the facts and avoid generic filler.
- [Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.html): Follow for citations, claim language, assumptions, and evidence quality.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.html): Follow for process boundaries and review standards.

## Deliverable

- Create or update **Evaluation Report** as a polished Word-ready document. The source template may be Markdown, but the intended artifact should be suitable for `.docx`/Word export.

## Missing Input Policy

Use available evidence, preserve unknowns and conflicts, and ask only when no readable source exists.

## Guardrails

Do not send messages, write to an external CRM, create tasks or projects, move stage, or record an investment decision.

## Completion Criteria

- The report covers all grouped evidence domains and records material change since the previous version.
- Claims, unknowns, conflicts, risks, and next evidence are explicit.
- The shared living-report lifecycle and evidence-basis manifest contract is satisfied.
- The resulting ID is saved to evaluation report artifact.

## Human Review

- Review the analysis and approve any follow-up work or lifecycle decision separately.
