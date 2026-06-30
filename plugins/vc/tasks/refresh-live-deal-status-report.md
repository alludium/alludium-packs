---
id: vc.refresh_live_deal_status_report
title: Refresh Live Deal Status Report
slug: refresh-live-deal-status-report
agent: vc-evaluation-analyst
skills:
- citation-enforcement
- investment-diligence-question-framework
---

> **GENERATED FILE**
> Source: `alludium/task-definition-templates/vc-workflows/refresh-live-deal-status-report.yaml`
> Do not edit directly. Change the YAML source and run `python plugins/vc/scripts/generate_markdown.py`.

# Refresh Live Deal Status Report

## Objective

Create or manually refresh the current evidence-backed live deal status report for one venture-capital opportunity at any deal stage.

## What To Do

Create or refresh the current Live Deal Status Report from the supplied source artifacts and every relevant READY Deal Pipeline file available in the task chat. Begin source discovery with `artifact.getArtifactsForChatContext` for the current task chat so the evidence inventory includes both directly attached files and project-shared files inherited by the chat. This is the report only: include Snapshot, Product, Technology, Market, Business model, Go-to-market, Competition, Team, Financials, Deal, and Open questions. Do not include the separate evidence ledger, human posture, votes, or decision record. Cite material claims inline, distinguish company claims from corroborated evidence, label inference and investor judgment, preserve material conflicts, and state missing information plainly.
Use `definitionJson.documentRefs` as the durable source guidance for this output. Render one complete standalone safe static HTML artifact using the CSS-only tab pattern in `vc.document.live_deal_status_report_template`. The tabs must be ordinary fragment links backed by CSS `:target` selectors. Do not use JavaScript, forms, iframes, event handlers, external scripts, or external stylesheets. Follow Template Use Guidance for the shared token aliases, structural classes, source discipline, and pre-save HTML QA. The first visible tab must be Snapshot. Open questions must be grouped by area and include topic or sector labels where useful, priority, decision relevance, evidence needed, owner, and status. Do not invent generic questions merely to fill the table.
This is a general Deal Pipeline task and must remain runnable at every lifecycle stage. The project mapping supplies the project's current report artifact as existing live deal status report artifact when one exists. If that ID is supplied, this is a regeneration. Read that artifact's source metadata, then call `artifact.updateTextArtifact` with the same artifact ID, the complete replacement HTML, and the observed source revision number and content hash. Do not create a replacement artifact, change the artifact identity, or create a duplicate with the same filename. If the supplied artifact cannot be read or updated, stop and explain the problem instead of creating a duplicate.
If existing live deal status report artifact is not supplied, this is the first generation. Create exactly one project-shared HTML artifact with `artifact.createTextArtifact`, a clear `.html` filename, `mimeType: "text/html"`, and complete HTML beginning with `<!doctype html>`.
In both cases, save the created or updated artifact ID to the required output field live deal status report artifact. The output ID is the ID that must be supplied as existing live deal status report artifact on the next manual refresh. Keep detailed report content inside the HTML artifact rather than duplicating it in task output fields.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Company Name, Existing Live Deal Status Report, Additional Source Artifact IDs.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Live Deal Status Report Template](../alludium/documents/deal-room/live-deal-status-report-template.html): Use as the starting structure for the deliverable; adapt it to the facts and avoid generic filler.
- [Investment Diligence Question Framework](../alludium/documents/shared/investment-diligence-question-framework.html): Use as the analysis method.
- [Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.html): Follow for citations, claim language, assumptions, and evidence quality.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.html): Follow for process boundaries and review standards.

## Deliverable

- Create or update **Live Deal Status Report** as a standalone safe HTML artifact. Use `.html`, `mimeType: "text/html"`, and complete static HTML suitable for the platform safe previewer.

## Missing Input Policy

Use the evidence currently available and mark unsupported sections or claims as unknown. Ask only when no company identity or readable source material is available.

## Guardrails

Do not send messages, mutate CRM records, create folders or projects, create child tasks, move stages, or record an investment decision.

## Completion Criteria

- The report is a standalone HTML artifact with eleven CSS-only report tabs and no JavaScript.
- Material claims are cited or clearly labelled as company claim, inference, assumption, or investor judgment.
- Missing information and open questions are explicit and decision-relevant.
- A first run creates one artifact; a regeneration updates the supplied artifact without changing its ID.
- The resulting artifact ID is saved to live deal status report artifact.

## Human Review

- Confirm the report is an analytical synthesis and does not record a human investment decision.
- Approve any separate external communication, CRM write, stage movement, or investment decision outside this task.
