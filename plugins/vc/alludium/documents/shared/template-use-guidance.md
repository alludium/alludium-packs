---
id: vc.document.template_use_guidance
title: Template Use Guidance
documentType: sop
supportedProjectTypes:
  - vc_deal_room
  - vc_origination_pipeline
  - vc_investment_management
summary: Operating guidance for applying VC document templates without producing generic filler.
---

# Template Use Guidance

## Purpose

Use this guidance whenever a task references a pack document as an output template, methodology, checklist, style guide, policy, or operating guide. The goal is to produce investor-grade artifacts that are consistent enough to review, but flexible enough to reflect the actual source evidence.

## Template Application Contract

Treat referenced document templates as adaptable artifact scaffolds. Preserve the core sections needed for the decision, but omit, compress, or mark sections as not available when they are irrelevant or unsupported by source inputs. Never fill a section with generic prose solely because the template contains it.

## Document Type Semantics

| Document Type | Use It For | Quality Bar |
| --- | --- | --- |
| Template | A reusable output structure for a generated artifact | Produces a polished reader-facing artifact without exposing authoring guidance |
| Methodology | Reusable analysis logic, scoring, or diligence structure | Explains how to reason, not merely what headings to use |
| Checklist | Status tracking, readiness review, setup review, or control completion | Captures owner, status, evidence, and blocker state |
| Style guide | Citation, source-confidence, claim-language, or formatting discipline | Governs how claims are written across artifacts |
| Policy | Boundaries, approval rules, or disallowed behavior | States what may and may not happen |
| SOP | Operating sequence, handoff convention, or repeatable process | Gives ordered, action-oriented process guidance |

## Source Input Mapping

When a template includes a source-input map, use it to route evidence into the right section. Do not treat the map as an exhaustive requirement. If a mapped source is missing, mark the affected section as unknown or not assessed rather than inventing content.

## Section Handling

| Situation | Expected Handling |
| --- | --- |
| Source evidence supports the section | Complete it with specific claims, citations, and decision relevance |
| Evidence is partial | Complete the known parts and mark gaps explicitly |
| Evidence is absent | Mark as unavailable, unknown, or not assessed; name the source input that would resolve it |
| Section is irrelevant to the deal or workflow | Omit it or compress it into a short not-applicable note |
| Template rows would create repetitive filler | Combine rows or summarize with a compact table |

## Evidence Discipline

Every material claim should have a source link, source artifact reference, or a clear label such as assumption, inference, founder claim, investor judgment, or unverified. Preserve source links when available. Do not imply precision when the source inputs do not support it.

## Output Hygiene

Do not reproduce internal drafting notes, task instructions, or template-use guidance in the generated artifact unless the referenced template intentionally includes a reader-facing standard, source index, decision criteria, or usage section. Final artifacts should read like partner-ready VC work product, not like a workflow trace.

## HTML Artifact Contract

When a VC template is rendered as a task output artifact, create the final artifact with `artifact_createTextArtifact` as a safe static HTML text artifact. Use a `.html` filename, `mimeType: "text/html"`, and complete standalone HTML source beginning with `<!doctype html>`. Do not create Markdown artifacts for rendered outputs, and do not rely on the platform to convert Markdown into HTML.

Use one shared visual system across all VC HTML artifacts. The goal is to make commercial, technical, financial, team, diligence-question, review-pack, memo, agenda, and decision-record outputs feel like one document family rather than unrelated one-off pages.

Required shell:

- Create one complete standalone HTML document with `<!doctype html>`, `<html lang="en">`, `<head>`, and `<body>`.
- Use one centered page container: `max-width: 1080px; margin: 0 auto; padding: 32px 28px 48px;`.
- Use the same font stack everywhere: `Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`.
- Use a white document surface with a quiet neutral page background. Do not use full-page gradients, decorative illustrations, oversized hero sections, or saturated theme backgrounds.

Define local token aliases inside the artifact stylesheet so preview and download render consistently without depending on host app CSS variables:

```css
:root {
  --brand: 229 56% 34%;
  --brand-primary: var(--brand);
  --brand-primary-strong: 229 58% 24%;
  --brand-secondary: 215 18% 38%;
  --brand-secondary-surface: 220 18% 94%;
  --foreground: 222 27% 14%;
  --muted-foreground: 218 12% 42%;
  --card: 0 0% 100%;
  --muted: 220 18% 96%;
  --border: 220 16% 86%;
  --color-primary: hsl(var(--brand-primary));
  --color-primary-strong: hsl(var(--brand-primary-strong));
  --color-secondary: hsl(var(--brand-secondary));
  --color-secondary-surface: hsl(var(--brand-secondary-surface));
  --color-text: hsl(var(--foreground));
  --color-muted-text: hsl(var(--muted-foreground));
  --color-card: hsl(var(--card));
  --color-page: hsl(var(--muted));
  --color-border: hsl(var(--border));
}
```

Use those aliases for the document system:

- `--color-primary` and `--color-primary-strong`: document header rule, major section headings, primary badges, and note accents.
- `--color-secondary` and `--color-secondary-surface`: metadata, secondary badges, table headers, and quiet panel backgrounds.
- `--color-text`, `--color-muted-text`, `--color-card`, `--color-page`, and `--color-border`: body copy, metadata, document surfaces, page background, borders, and table rules.

Use consistent structural classes unless a source template provides a stricter structure: `.document`, `.document-header`, `.summary-grid`, `.section`, `.badge`, `.badge.secondary`, `.metadata`, `.eyebrow`, `.note`, and table styles. Status badges should use a stable label set such as `Recommended`, `Watch`, `Targeted Diligence`, `Gap`, `Blocked`, and `Ready for Review`. Do not invent a new visual badge system when one of those labels fits.

Use a consistent document structure:

1. Header with company, project/task context, date, and artifact purpose.
2. Status strip or compact metadata row, when the workflow has a readiness, recommendation, or decision status.
3. First visible reader-facing summary block using the exact heading required by the task/template. Common headings include `Executive Summary` and `At A Glance`; they are not interchangeable when a task names one explicitly. If a task requires `Executive Summary`, that exact heading is mandatory and a status card is not a substitute.
4. Decision snapshot, key facts, or requested action.
5. Evidence, source index, and provenance.
6. Detailed findings, field map, evaluation sections, or checklist rows.
7. Missing information, risks, next actions, owners, and follow-up timing.
8. Appendix only when useful.

Keep the first screen decision-useful. Put the recommendation, status, source confidence, strongest supported facts, and highest-priority gaps before long tables or detailed evidence logs.

Use scalable safe-preview styling: readable 15-16px base text, line-height around 1.5-1.65, max-width around 960-1120px, generous section spacing, responsive summary cards, and tables wrapped in an overflow container. Avoid cramped first-screen table walls, fixed-width layouts, external assets, scripts, event handlers, forms, iframes, and interactive JavaScript.

Keep structured task output fields separate from the artifact. Detailed HTML tables, source indexes, field maps, and long narrative belong inside the HTML artifact only. Optional structured fields should be unset where possible; when the platform requires a value, use plain text, no markup, and one short pointer or summary rather than copying the document body.

Compatibility note: before `v0.5.37`, some intake task output fields accepted richer text for detailed source indexes and field maps. Existing task runs may still contain that historical content. Treat those values as legacy task-output history, review or clean them manually only when a workspace depends on the compact summaries, and write new runs using the compact plain-text summary fields plus the full HTML artifact.

Pre-save HTML QA checklist:

- Exactly one `h1`.
- Major sections use `h2`; subsections use `h3`.
- The document includes `--color-primary` and `--color-secondary` aliases and uses them for badges, section accents, and table headers.
- The document uses the shared `.document`, `.document-header`, `.summary-grid`, `.section`, `.badge`, and table styles unless the source template explicitly overrides them.
- No raw Markdown fences, raw `<html>` text in the rendered body, unresolved placeholders such as `TODO`, `{{variable}}`, `undefined`, or `null`, external scripts, forms, iframes, or event handlers.
- No duplicate same-name artifact is created during retry or recovery.
- No decorative full-page gradients, oversized hero sections, nested cards, or one-off status-color systems.

## Completion Check

Before finishing, verify that the artifact states the decision ask or workflow purpose, separates evidence from unknowns, identifies next actions and owners where relevant, and gives the human reviewer enough context to decide what to do next.
