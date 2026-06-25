---
id: vc.document.initial_call_brief_template
title: Initial Call Brief Template
documentType: template
supportedProjectTypes:
  - vc_deal_room
summary: Reusable pre-call brief for first founder or management meetings.
---

# Initial Call Brief Template

## Rendered Artifact Contract

When this template is used to create a task output artifact:

- Create the final artifact with `artifact_createTextArtifact`.
- Use a `.html` filename and `mimeType: "text/html"`.
- Set `content` to a complete standalone safe static HTML document beginning with `<!doctype html>`.
- Convert this Markdown scaffold into semantic HTML sections, tables, and lists with small inline CSS in a `<style>` block.
- Do not create `.md` or `text/markdown` artifacts for rendered outputs.
- Do not copy HTML into structured task output fields; those fields remain plain text or artifact UUIDs.


## Meeting Header

| Field | Content |
| --- | --- |
| Company | Name, website, sector, geography |
| Meeting objective | Discover, qualify, follow-up, or partner intro |
| Attendees | Firm, founder, advisor, relationship owner |
| Source path | Inbound, outbound, referral, sourcing pipeline |
| Current view | Pass / watch / continue / unknown |

## Source Inputs

| Source Input | Use For |
| --- | --- |
| Founder deck, website, or product notes | Product summary, customer/buyer hypothesis, traction claims |
| CRM, intro, or sourcing context | Source path, relationship owner, why this meeting is happening now |
| Prior screen or sourcing verdict | Current view, key unknowns, pass/watch/continue rationale |
| Public research and third-party sources | Market, competition, financing, hiring, and credibility checks |
| Calendar invite or attendee list | Meeting objective, attendees, relationship paths, follow-up owner |

## Pre-Call Snapshot

| Topic | Notes | Evidence |
| --- | --- | --- |
| Product |  |  |
| Customer / buyer |  |  |
| Market |  |  |
| Team |  |  |
| Traction |  |  |
| Financing |  |  |

## Questions By Topic

| Topic | Question | Why It Matters |
| --- | --- | --- |
| Customer pain |  |  |
| Product depth |  |  |
| Traction quality |  |  |
| Economics |  |  |
| Team |  |  |
| Fundraise |  |  |

## Risks And Unknowns

List what is not yet validated. Separate pre-call hypotheses from known facts.

## Recommended Next Action

State the expected next step if the call goes well, what would trigger a pass, and what evidence should be requested.

## Standard

Keep the brief short enough to use in the meeting. Label weak evidence clearly and separate pre-call hypotheses from verified facts.
