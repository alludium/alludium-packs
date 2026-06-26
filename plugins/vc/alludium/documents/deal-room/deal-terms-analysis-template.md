---
id: vc.document.deal_terms_analysis_template
title: Deal Terms Analysis Template
documentType: template
supportedProjectTypes:
  - vc_deal_room
summary: Reusable commercial review format for valuation, ownership, dilution, ESOP, and round construction analysis.
---

# Deal Terms Analysis Template

## Rendered Artifact Contract

When this template is used to create a task output artifact:

- Create the final artifact with `artifact_createTextArtifact`.
- Use a `.html` filename and `mimeType: "text/html"`.
- Set `content` to a complete standalone safe static HTML document beginning with `<!doctype html>`.
- Convert this Markdown scaffold into semantic HTML sections, tables, and lists with small inline CSS in a `<style>` block.
- Do not create `.md` or `text/markdown` artifacts for rendered outputs.
- Do not copy HTML into structured task output fields; those fields remain plain text or artifact UUIDs.

## At A Glance

Render this section first as a compact HTML terms card before the detailed model and analysis.

| Field | Content |
| --- | --- |
| Terms posture | Attractive / workable / stretched / not ready |
| Proposed ownership | Base-case ownership and sensitivity if available |
| Main economic tradeoff | The valuation, dilution, ESOP, reserve, or round-construction issue that matters most |
| IC question | The term or return question committee must answer |
| Next proof needed | The model, cap table, reserve, or syndicate input needed before approval |

## Source Inputs

| Source | Artifact / Link | Notes |
| --- | --- | --- |
| Proposed investment amount |  |  |
| Valuation |  |  |
| Round size |  |  |
| Cap table |  |  |
| Forecast / reserve policy |  |  |

## Ownership Model

| Scenario | Investment | Valuation | Ownership | Dilution / ESOP Notes |
| --- | --- | --- | --- | --- |
| Base case |  |  |  |  |
| Sensitivity case |  |  |  |  |

## Commercial Terms

| Term | Proposed | Investor View | Open Question |
| --- | --- | --- | --- |
| Ownership |  |  |  |
| ESOP |  |  |  |
| Co-investors |  |  |  |
| Follow-on reserves |  |  |  |

## IC Questions

| Question | Owner | Evidence Needed | Decision Impact |
| --- | --- | --- | --- |
|  |  |  |  |

## Standard

Frame the output as commercial analysis only. Do not provide legal advice, negotiate terms, or approve the deal.
