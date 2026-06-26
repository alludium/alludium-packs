---
id: vc.document.financial_evaluation_template
title: Financial Evaluation Template
documentType: template
supportedProjectTypes:
  - vc_deal_room
summary: Output template for lightweight financial and financing evaluation before formal diligence.
---

# Financial Evaluation Template

## Rendered Artifact Contract

When this template is used to create a task output artifact:

- Create the final artifact with `artifact_createTextArtifact`.
- Use a `.html` filename and `mimeType: "text/html"`.
- Set `content` to a complete standalone safe static HTML document beginning with `<!doctype html>`.
- Convert this Markdown scaffold into semantic HTML sections, tables, and lists with small inline CSS in a `<style>` block.
- Do not create `.md` or `text/markdown` artifacts for rendered outputs.
- Do not copy HTML into structured task output fields; those fields remain plain text or artifact UUIDs.

## At A Glance

Render this section first as a compact HTML overview before the workstream detail.

| Field | Content |
| --- | --- |
| Financial posture | Continue / watch / pass / targeted diligence / decision review |
| Strongest financial proof | Best evidence for revenue quality, burn discipline, ownership path, or return potential |
| Main financial doubt | The forecast, runway, valuation, ownership, or financing assumption still unproven |
| Evidence confidence | High / Medium / Low, with one-line rationale |
| Next proof needed | The single model, cap-table, metric, or financing evidence item that changes the decision |

## Workstream Header

| Field | Content |
| --- | --- |
| Company |  |
| Evaluation run | First run / rerun |
| New evidence since prior run |  |
| Decision supported | Continue evaluation / targeted diligence / decision review / pass / watch |

## Current Financial View

| Area | View | Evidence | Confidence | Gap |
| --- | --- | --- | --- | --- |
| Business model |  |  | High / Medium / Low |  |
| Forecast plausibility |  |  | High / Medium / Low |  |
| Revenue quality |  |  | High / Medium / Low |  |
| Burn and runway |  |  | High / Medium / Low |  |
| Use of funds |  |  | High / Medium / Low |  |
| Valuation and ownership |  |  | High / Medium / Low |  |
| Financing path |  |  | High / Medium / Low |  |

## Main Financial Hypothesis

State the financing, milestone, ownership, or return belief that must be true for the opportunity to proceed.

## Evidence Reviewed

| Source | What It Supports | Quality | Recency |
| --- | --- | --- | --- |
|  |  | High / Medium / Low |  |

## Company Claims And Verification Gaps

| Claim | Current Support | Gap | Decision Impact |
| --- | --- | --- | --- |
|  | Verified / Partially supported / Company claim / Unsupported |  |  |

## Gating Financial Risk

State the financial risk most likely to change the investment posture.

## Next Proof Needed

| Priority | Evidence Request / Question | Owner | Success Threshold |
| --- | --- | --- | --- |
| Must answer / Should answer / Optional |  |  |  |

## Decision Impact

| Recommendation | Rationale | Conditions |
| --- | --- | --- |
| Continue / Watch / Pass / Targeted diligence / Decision review |  |  |

## Standard

Separate company claims, verified evidence, inference, and missing proof. Do not treat forecasts, cap-table numbers, or valuation assumptions as verified unless source data has been reviewed.
