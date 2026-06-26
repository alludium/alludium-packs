---
id: vc.document.customer_insights_summary_template
title: Customer Insights Summary Template
documentType: template
supportedProjectTypes:
  - vc_deal_room
summary: Reusable meeting-record summary for customer, founder, and diligence call evidence.
---

# Customer Insights Summary Template

## Rendered Artifact Contract

When this template is used to create a task output artifact:

- Create the final artifact with `artifact_createTextArtifact`.
- Use a `.html` filename and `mimeType: "text/html"`.
- Set `content` to a complete standalone safe static HTML document beginning with `<!doctype html>`.
- Convert this Markdown scaffold into semantic HTML sections, tables, and lists with small inline CSS in a `<style>` block.
- Do not create `.md` or `text/markdown` artifacts for rendered outputs.
- Do not copy HTML into structured task output fields; those fields remain plain text or artifact UUIDs.

## At A Glance

Render this section first as a compact HTML insight card before the detailed evidence tables.

| Field | Content |
| --- | --- |
| Source coverage | Complete / partial / excerpt, with reliability |
| Strongest customer insight | The most decision-relevant customer, buyer, or workflow signal |
| Main contradiction or gap | The claim, question, or missing source that limits confidence |
| Investment implication | Continue / watch / pass / request follow-up, with one-line rationale |
| Next action | Specific follow-up item, owner, and approval need |

## Source Coverage

| Source | Date | Coverage | Reliability |
| --- | --- | --- | --- |
| Transcript, notes, recording, CRM note, or artifact |  | Complete / partial / excerpt | High / Medium / Low |

## Insight Summary

| Topic | Evidence | Investment Implication |
| --- | --- | --- |
| Customer pain |  |  |
| Buyer and budget |  |  |
| Product workflow |  |  |
| Traction or urgency |  |  |
| Competition |  |  |

## Contradictions And Gaps

| Gap / Contradiction | Why It Matters | Follow-Up |
| --- | --- | --- |
|  |  |  |

## Action Items

| Action | Owner | Due Date | Approval Needed? |
| --- | --- | --- | --- |
|  |  |  | Yes / No |

## CRM-Neutral Update Draft

Provide a short update that can be reviewed before any CRM write. Do not imply that the write has happened.

## Standard

Tie claims back to meeting records or notes. If a transcript is partial, state the coverage gap before drawing conclusions.
