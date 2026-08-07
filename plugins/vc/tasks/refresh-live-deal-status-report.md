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
Resolve the report Fund from the supplied project fund id and the canonical `vc.funds` records available to the recommended agent. Match by exact stable-ID equality only. When exactly one matching record has `status: actively_investing`, show `Fund: <resolved Fund name>` prominently in the visible report metadata and Snapshot. The Fund-fit section must use only that Fund's configured thesis, stage, sectors, geographies, minimum and maximum check size, currency, exclusions, and scoring framework. Treat those fields as the configured decision frame, not as Deal evidence or proof that the company satisfies the mandate. Never infer a Fund from company details, report text, display name, lifecycle stage, or nearest apparent mandate; never substitute another active Fund or blend Fund records.
If fund id is missing, show `Fund: Unassigned`, state that assignment is unresolved, and make no Fund-relative fit claim. If the stored ID matches no configured record, show `Fund: Unknown (<stored id>)`, make no Fund-relative fit claim, and flag assignment or configuration correction. If it matches a record whose status is not actively investing, show `Fund: <resolved Fund name> (inactive)`, make no active-mandate fit claim, and flag correction. If no Funds are configured, show `Fund: Unassigned`, state that Fund setup is incomplete, and make no Fund-relative fit claim. Do not select or persist fund id during this task.
Use `definitionJson.documentRefs` as the durable source guidance for this output. Render one complete standalone safe static HTML artifact using the CSS-only tab pattern in `vc.document.live_deal_status_report_template`. The tabs must be ordinary fragment links backed by CSS `:target` selectors. Do not use JavaScript, forms, iframes, event handlers, external scripts, or external stylesheets. Follow Template Use Guidance for the shared token aliases, structural classes, source discipline, and pre-save HTML QA. The first visible tab must be Snapshot. Open questions must be grouped by area and include topic or sector labels where useful, priority, decision relevance, evidence needed, owner, and status. Do not invent generic questions merely to fill the table.
This is a general Deal Pipeline task and must remain runnable at every lifecycle stage. The project mapping supplies the project's current report artifact as existing live deal status report artifact when one exists. If that ID is supplied, this is a regeneration. Read that artifact's source metadata, then call `artifact.updateTextArtifact` with the same artifact ID, the complete replacement HTML, and the observed source revision number and content hash. Do not create a replacement artifact, change the artifact identity, or create a duplicate with the same filename. If the supplied artifact cannot be read or updated, stop and explain the problem instead of creating a duplicate.
If existing live deal status report artifact is not supplied, this is the first generation. Create exactly one project-shared HTML artifact with `artifact.createTextArtifact`, a clear `.html` filename, `mimeType: "text/html"`, and complete HTML beginning with `<!doctype html>`.
In both cases, save the created or updated artifact ID to the required output field live deal status report artifact. The output ID is the ID that must be supplied as existing live deal status report artifact on the next manual refresh. Keep detailed report content inside the HTML artifact rather than duplicating it in task output fields.
Also save a compact JSON array to the required output field open questions. This is a machine-actionable index for reviewed follow-up, not a second copy of the report narrative. Each item must contain id, question, area, priority, `evidenceNeeded`, `suggestedOwnerRole`, status, and `sourceRefs`. Use only the configured vocabularies in the field schema. Keep the array to at most 50 decision-relevant items and keep each string concise.
Derive questions only from evidence gaps, material conflicts, blocked work, or explicitly unresolved decisions supported by sources you actually read. `sourceRefs` may contain only real artifact IDs, task IDs, or supplied source anchors. Use a deterministic stable id derived from the normalized underlying question area and evidence need; never use an array index, timestamp, or random UUID. Preserve the same ID across refreshes when the underlying need is unchanged. When a previously reported question is demonstrably answered or superseded, retain it only when useful for the refresh delta and set the corresponding status rather than creating a near-duplicate. If there are no supported questions, save `[]`. Never invent generic questions to fill the output.
`suggestedOwnerRole` is advisory only. Do not put a fabricated person ID, agent ID, or guessed name in it. This report must not create, assign, or update tasks. Deal Manager may later compare these stable questions with existing work and present a predefined or ad-hoc task proposal, but a human must approve model-generated task creation and assignment separately.

## Available Context

- Use any supplied task context, attached files, source links, meeting notes, CRM/source records, and prior artifacts.
- Especially look for: Company Name, Confirmed Fund ID, Existing Live Deal Status Report, Additional Source Artifact IDs.
- If a named input is absent, follow the missing-input policy rather than inventing facts.

## Reference Materials

- [Live Deal Status Report Template](../alludium/documents/deal-room/live-deal-status-report-template.html): Use as the starting structure for the deliverable; adapt it to the facts and avoid generic filler.
- [Investment Diligence Question Framework](../alludium/documents/shared/investment-diligence-question-framework.html): Use as the analysis method.
- [Evidence And Citation Style Guide](../alludium/documents/shared/evidence-citation-style-guide.html): Follow for citations, claim language, assumptions, and evidence quality.
- [Template Use Guidance](../alludium/documents/shared/template-use-guidance.html): Follow for process boundaries and review standards.

## Deliverable

- Create or update **Live Deal Status Report** as a standalone safe HTML artifact. Use `.html`, `mimeType: "text/html"`, and complete static HTML suitable for the platform safe previewer.
- Also include a short human-readable summary covering: Structured Open Questions. Do not output raw JSON unless the user explicitly asks for machine-readable data.

## Missing Input Policy

Use the evidence currently available and mark unsupported sections or claims as unknown. Ask only when no company identity or readable source material is available.

## Guardrails

Do not send messages, mutate CRM records, create folders or projects, create child tasks, move stages, or record an investment decision.

## Completion Criteria

- The report is a standalone HTML artifact with eleven CSS-only report tabs and no JavaScript.
- Material claims are cited or clearly labelled as company claim, inference, assumption, or investor judgment.
- Missing information and open questions are explicit and decision-relevant.
- The visible report shows the resolved Fund name or an explicit unassigned, unknown, or inactive state.
- Fund fit uses only the exact active `vc.funds` record matched by the Deal's fund id; unresolved states produce no Fund-relative fit claim.
- A first run creates one artifact; a regeneration updates the supplied artifact without changing its ID.
- The resulting artifact ID is saved to live deal status report artifact.
- A bounded structured question index is saved to open questions, with stable IDs and only verified source references; an empty array is valid.
- The report creates or assigns no follow-up tasks.

## Human Review

- Confirm the report is an analytical synthesis and does not record a human investment decision.
- Review any task proposal derived later from structured report questions before creation or assignment.
- Approve any separate external communication, CRM write, stage movement, or investment decision outside this task.
