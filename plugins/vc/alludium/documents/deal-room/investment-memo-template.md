---
id: vc.document.investment_memo_template
title: Investment Memo Template
documentType: template
supportedProjectTypes:
  - vc_deal_room
summary: Reusable investment memo structure for IC preparation.
---

# Investment Memo Template

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

Render this section as the first visible HTML block, using a compact summary card or table before the detailed memo.

| Field | Content |
| --- | --- |
| Decision ask | Invest / proceed to IC / continue diligence / pass, with the specific approval requested |
| Recommendation | One sentence stating the recommended action and the main condition |
| Why now | The timing argument in one line |
| Top upside | The single strongest reason this can return capital to the fund |
| Top risk | The risk most likely to change the recommendation |
| Must decide before IC | The one question or condition that cannot be deferred |

## Cover Summary

| Field | Content |
| --- | --- |
| Company | Name, sector, geography, stage |
| Decision ask | Invest / proceed to IC / continue diligence / pass |
| Round | Round size, valuation, lead, expected close date |
| Proposed check | Amount, target ownership, reserve implication |
| Owner | Deal lead and memo preparer |
| Recommendation | One-line recommendation with conditions |

## Source Inputs

| Source Input | Use For |
| --- | --- |
| Founder deck or data room materials | Company narrative, product, market, traction, financial claims, fundraise terms |
| CRM notes or intro context | Source path, relationship context, prior partner views, open action history |
| Initial call brief and transcript | Founder claims, customer pain, GTM motion, current unknowns |
| Diligence reports and question bank | Workstream findings, open risks, disconfirming evidence, required follow-up |
| Financial model or cap table | Burn, runway, ownership, valuation, reserves, return sensitivity |
| Term sheet or counsel notes | Terms, closing conditions, legal/commercial issues |

## Executive Summary

Write one tight page covering the business, why now, why this fund, proposed action, headline returns or ownership logic, and the top three risks. Include both the bull case and the bear case; do not bury the bear case in the risk section.

## Investment Thesis

| Thesis Pillar | Evidence | Why It Matters | Confidence |
| --- | --- | --- | --- |
| Pillar 1 | Cited evidence | Link to return, ownership, or strategic fit | High / Medium / Low |
| Pillar 2 | Cited evidence | Link to return, ownership, or strategic fit | High / Medium / Low |
| Pillar 3 | Cited evidence | Link to return, ownership, or strategic fit | High / Medium / Low |

## Business Overview

- Company snapshot and product description
- Customer, buyer, and workflow summary
- Business model and pricing
- Current traction and operating cadence
- What must be true for this to become a fund-returning outcome

## Market And Competition

| Topic | Required Content |
| --- | --- |
| Market | Size, growth, urgency, and customer budget owner |
| Category dynamics | Tailwinds, adoption barriers, timing risk |
| Competitive set | Direct alternatives, incumbents, substitutes |
| Differentiation | What is defensible versus what is merely claimed |

## Diligence Findings

| Workstream | Finding | Evidence | Risk / Gap | Owner |
| --- | --- | --- | --- | --- |
| Commercial |  |  |  |  |
| Financial |  |  |  |  |
| Technical |  |  |  |  |
| Founder / team |  |  |  |  |
| Legal / regulatory |  |  |  |  |

## Terms, Ownership, And Returns

Include round terms, implied valuation, target ownership, dilution assumptions, reserves, exit path, and sensitivity cases when available. If a returns model is not available, state that plainly and avoid implying precision.

## Risks, Mitigants, And Unknowns

| Risk | Severity | Evidence | Mitigant | Decision Impact |
| --- | --- | --- | --- | --- |
|  | High / Medium / Low |  |  | Proceed / condition / pass |

## Conditions And Next Actions

| Condition / Action | Owner | Due Date | Blocks Decision? |
| --- | --- | --- | --- |
|  |  |  | Yes / No |

## Standard

Every material claim should cite a source. The memo should distinguish completed diligence from remaining work, state what would change the recommendation, and end with a source index.
