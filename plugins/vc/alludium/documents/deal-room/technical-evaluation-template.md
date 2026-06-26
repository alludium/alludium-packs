---
id: vc.document.technical_evaluation_template
title: Technical Evaluation Template
documentType: template
supportedProjectTypes:
  - vc_deal_room
summary: Output template for lightweight technical and product evaluation before formal diligence.
---

# Technical Evaluation Template

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
| Technical posture | Continue / watch / pass / targeted diligence / decision review |
| Strongest technical proof | Best evidence for product depth, architecture, data/IP edge, or execution quality |
| Main technical doubt | The product, architecture, defensibility, or delivery assumption still unproven |
| Evidence confidence | High / Medium / Low, with one-line rationale |
| Next proof needed | The single demo, artefact, expert input, or technical evidence item that changes the decision |

## Workstream Header

| Field | Content |
| --- | --- |
| Company |  |
| Evaluation run | First run / rerun |
| New evidence since prior run |  |
| Decision supported | Continue evaluation / targeted diligence / decision review / pass / watch |

## Current Technical View

| Area | View | Evidence | Confidence | Gap |
| --- | --- | --- | --- | --- |
| Product depth |  |  | High / Medium / Low |  |
| Architecture plausibility |  |  | High / Medium / Low |  |
| Technical edge |  |  | High / Medium / Low |  |
| IP or data defensibility |  |  | High / Medium / Low |  |
| Roadmap realism |  |  | High / Medium / Low |  |
| Technical team coverage |  |  | High / Medium / Low |  |

## Main Technical Hypothesis

State the product, architecture, IP, data, or technical execution belief that must be true for the opportunity to proceed.

## Evidence Reviewed

| Source | What It Supports | Quality | Recency |
| --- | --- | --- | --- |
|  |  | High / Medium / Low |  |

## Company Claims And Verification Gaps

| Claim | Current Support | Gap | Decision Impact |
| --- | --- | --- | --- |
|  | Verified / Partially supported / Company claim / Unsupported |  |  |

## Gating Technical Risk

State the technical risk most likely to change the investment posture.

## Next Proof Needed

| Priority | Evidence Request / Question | Owner | Success Threshold |
| --- | --- | --- | --- |
| Must answer / Should answer / Optional |  |  |  |

## Decision Impact

| Recommendation | Rationale | Conditions |
| --- | --- | --- |
| Continue / Watch / Pass / Targeted diligence / Decision review |  |  |

## Standard

Separate company claims, verified evidence, inference, and missing proof. Do not imply code review, security review, expert validation, or IP clearance unless those inputs were actually reviewed.
