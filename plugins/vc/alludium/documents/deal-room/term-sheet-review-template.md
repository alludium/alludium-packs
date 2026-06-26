---
id: vc.document.term_sheet_review_template
title: Term Sheet Review Template
documentType: template
supportedProjectTypes:
  - vc_deal_room
summary: Reusable business review format for term-sheet deviations, red flags, and counsel questions.
---

# Term Sheet Review Template

## Rendered Artifact Contract

When this template is used to create a task output artifact:

- Create the final artifact with `artifact_createTextArtifact`.
- Use a `.html` filename and `mimeType: "text/html"`.
- Set `content` to a complete standalone safe static HTML document beginning with `<!doctype html>`.
- Convert this Markdown scaffold into semantic HTML sections, tables, and lists with small inline CSS in a `<style>` block.
- Do not create `.md` or `text/markdown` artifacts for rendered outputs.
- Do not copy HTML into structured task output fields; those fields remain plain text or artifact UUIDs.

## At A Glance

Render this section first as a compact HTML business-review card before the full term-sheet review.

| Field | Content |
| --- | --- |
| Business recommendation | Acceptable / acceptable with counsel changes / not ready |
| Main deviation | The most material deviation from expected economics, rights, or process |
| Highest red flag | The issue most likely to block or reprice the deal |
| Counsel status | Not reviewed / in review / reviewed, with the key counsel question |
| Next approval | The business or legal approval needed before proceeding |

## Review Header

| Field | Content |
| --- | --- |
| Source reviewed | Term sheet artifact or link |
| Company | Name |
| Reviewer | Business owner |
| Counsel status | Not reviewed / in review / reviewed |

## Business Term Summary

| Term | Proposed | Expected / Prior View | Comment |
| --- | --- | --- | --- |
| Valuation |  |  |  |
| Instrument |  |  |  |
| Investment amount |  |  |  |
| Ownership |  |  |  |
| Liquidation preference |  |  |  |
| Board / observer rights |  |  |  |
| Pro rata / information rights |  |  |  |

## Deviations And Red Flags

| Issue | Severity | Business Impact | Counsel Question |
| --- | --- | --- | --- |
|  | High / Medium / Low |  |  |

## Approval Recommendation

State whether business terms are acceptable, acceptable with counsel changes, or not ready. Do not provide legal advice.

## Standard

Frame the output as business review, not legal advice. Escalate legal interpretation, ambiguous drafting, and non-standard rights to counsel.
