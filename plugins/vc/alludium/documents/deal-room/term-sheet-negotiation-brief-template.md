---
id: vc.document.term_sheet_negotiation_brief_template
title: Term Sheet Negotiation Brief Template
documentType: template
supportedProjectTypes:
  - vc_deal_room
summary: Reusable internal brief for open terms, give/get options, counsel questions, and approval points.
---

# Term Sheet Negotiation Brief Template

## Rendered Artifact Contract

When this template is used to create a task output artifact:

- Create the final artifact with `artifact_createTextArtifact`.
- Use a `.html` filename and `mimeType: "text/html"`.
- Set `content` to a complete standalone safe static HTML document beginning with `<!doctype html>`.
- Convert this Markdown scaffold into semantic HTML sections, tables, and lists with small inline CSS in a `<style>` block.
- Do not create `.md` or `text/markdown` artifacts for rendered outputs.
- Do not copy HTML into structured task output fields; those fields remain plain text or artifact UUIDs.


## Source Inputs

| Source | Artifact / Link | Notes |
| --- | --- | --- |
| Current term sheet |  |  |
| Deal terms analysis |  |  |
| Founder comments / redline |  |  |
| Counsel notes |  |  |
| IC constraints |  |  |

## Open Terms Table

| Term | Current Position | Business Tradeoff | Counsel Question | Approval Needed |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## Give / Get Options

| Option | Give | Get | Risk | Human Decision |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## Approval Points

| Approval | Owner | Evidence Required | Status |
| --- | --- | --- | --- |
|  |  |  | Not started / Open / Approved |

## Boundary

This is an internal negotiation-support brief. Do not send terms, negotiate externally, or approve legal language from this document alone.
