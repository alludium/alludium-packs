---
id: vc.document.commercial_evaluation_template
title: Commercial Evaluation Template
documentType: template
supportedProjectTypes:
  - vc_deal_room
summary: Output template for lightweight commercial evaluation before formal diligence.
---

# Commercial Evaluation Template

## Rendered Artifact Contract

When this template is used to create a task output artifact:

- Create the final artifact with `artifact_createTextArtifact`.
- Use a `.html` filename and `mimeType: "text/html"`.
- Set `content` to a complete standalone safe static HTML document beginning with `<!doctype html>`.
- Convert this Markdown scaffold into semantic HTML sections, tables, and lists with small inline CSS in a `<style>` block.
- Follow the shared VC HTML Artifact Contract in Template Use Guidance for section order, first-screen summary, spacing, responsive tables, and compact structured outputs.
- Do not create `.md` or `text/markdown` artifacts for rendered outputs.
- Do not copy HTML into structured task output fields; those fields remain plain text or artifact UUIDs.

## At A Glance

Render this section first as a compact HTML overview before the workstream detail.

| Field | Content |
| --- | --- |
| Commercial posture | Continue / watch / pass / targeted diligence / decision review |
| Strongest commercial proof | Best evidence for urgent customer pain, budget, or GTM pull |
| Main commercial doubt | The customer, budget, market, or GTM assumption still unproven |
| Evidence confidence | High / Medium / Low, with one-line rationale |
| Next proof needed | The single customer, market, pricing, or pipeline proof that changes the decision |

## Workstream Header

| Field | Content |
| --- | --- |
| Company |  |
| Evaluation run | First run / rerun |
| New evidence since prior run |  |
| Decision supported | Continue evaluation / targeted diligence / decision review / pass / watch |

## Current Commercial View

| Area | View | Evidence | Confidence | Gap |
| --- | --- | --- | --- | --- |
| Customer segment |  |  | High / Medium / Low |  |
| Pain and urgency |  |  | High / Medium / Low |  |
| Budget and pricing |  |  | High / Medium / Low |  |
| GTM path |  |  | High / Medium / Low |  |
| Competition |  |  | High / Medium / Low |  |
| Market size |  |  | High / Medium / Low |  |

## Main Commercial Hypothesis

State the customer, budget, GTM, or market belief that must be true for the opportunity to proceed.

## Evidence Reviewed

| Source | What It Supports | Quality | Recency |
| --- | --- | --- | --- |
|  |  | High / Medium / Low |  |

## Company Claims And Verification Gaps

| Claim | Current Support | Gap | Decision Impact |
| --- | --- | --- | --- |
|  | Verified / Partially supported / Company claim / Unsupported |  |  |

## Gating Commercial Risk

State the commercial risk most likely to change the investment posture.

## Next Proof Needed

| Priority | Evidence Request / Question | Owner | Success Threshold |
| --- | --- | --- | --- |
| Must answer / Should answer / Optional |  |  |  |

## Decision Impact

| Recommendation | Rationale | Conditions |
| --- | --- | --- |
| Continue / Watch / Pass / Targeted diligence / Decision review |  |  |

## Standard

Separate company claims, verified evidence, inference, and missing proof. Do not present this as customer validation or formal commercial diligence.
