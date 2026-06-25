---
id: vc.document.ic_memo_review_template
title: IC Memo Review Template
documentType: template
supportedProjectTypes:
  - vc_deal_room
summary: Reusable review format for checking IC memo readiness, gaps, and required changes.
---

# IC Memo Review Template

## Rendered Artifact Contract

When this template is used to create a task output artifact:

- Create the final artifact with `artifact_createTextArtifact`.
- Use a `.html` filename and `mimeType: "text/html"`.
- Set `content` to a complete standalone safe static HTML document beginning with `<!doctype html>`.
- Convert this Markdown scaffold into semantic HTML sections, tables, and lists with small inline CSS in a `<style>` block.
- Do not create `.md` or `text/markdown` artifacts for rendered outputs.
- Do not copy HTML into structured task output fields; those fields remain plain text or artifact UUIDs.


## Review Header

| Field | Content |
| --- | --- |
| Memo under review | Artifact ID or link |
| Agenda under review | Artifact ID or link |
| Reviewer | Name or role |
| IC date | Date |
| Readiness view | Ready / ready with edits / not ready |

## Readiness Assessment

| Area | Status | Notes |
| --- | --- | --- |
| Decision ask is clear | Pass / Issue / Blocker |  |
| Thesis is evidence-backed | Pass / Issue / Blocker |  |
| Financial and ownership logic ties | Pass / Issue / Blocker |  |
| Risks and dissent are visible | Pass / Issue / Blocker |  |
| Terms and conditions are explicit | Pass / Issue / Blocker |  |
| Source index is complete | Pass / Issue / Blocker |  |

## Required Changes

| Priority | Change | Reason | Owner |
| --- | --- | --- | --- |
| Must fix / Should fix / Polish |  |  |  |

## Recommended IC Handling

State whether the memo should proceed, proceed with named caveats, be held for more diligence, or be reframed as a gap-review discussion.

## Standard

Review the memo against its evidence base. Do not rewrite the investment case unless the task explicitly asks for memo production.
