---
id: vc.document.ic_decision_record_template
title: IC Decision Record Template
documentType: template
supportedProjectTypes:
  - vc_deal_room
summary: Reusable record for IC decisions and conditions.
---

# IC Decision Record Template

## Rendered Artifact Contract

When this template is used to create a task output artifact:

- Create the final artifact with `artifact_createTextArtifact`.
- Use a `.html` filename and `mimeType: "text/html"`.
- Set `content` to a complete standalone safe static HTML document beginning with `<!doctype html>`.
- Convert this Markdown scaffold into semantic HTML sections, tables, and lists with small inline CSS in a `<style>` block.
- Do not create `.md` or `text/markdown` artifacts for rendered outputs.
- Do not copy HTML into structured task output fields; those fields remain plain text or artifact UUIDs.


## Decision Summary

| Field | Content |
| --- | --- |
| Company | Name and project |
| Meeting date | Date |
| Decision | Approved / approved with conditions / continue diligence / passed |
| Decision makers present | Names or roles |
| Deal lead | Owner |
| Investment amount | Proposed amount and ownership |
| Terms discussed | Valuation, round, instrument, key conditions |

## Rationale

| Area | Summary | Evidence |
| --- | --- | --- |
| Approval rationale | Main reasons for decision | Memo, model, diligence artifacts |
| Dissent or concerns | Objections and unresolved issues | Reviewer comments or cited evidence |
| Conditions | Required items before closing or next stage | Owner and deadline |

## Follow-Up

| Action | Owner | Deadline | Blocks Close? |
| --- | --- | --- | --- |
|  |  |  | Yes / No |

## Standard

The record should be short, durable, and auditable. It should capture the decision made, not relitigate the entire memo.
