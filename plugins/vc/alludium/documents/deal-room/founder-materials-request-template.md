---
id: vc.document.founder_materials_request_template
title: Founder Materials Request Template
documentType: template
supportedProjectTypes:
  - vc_deal_room
summary: Reusable founder request template for diligence materials.
---

# Founder Materials Request Template

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

Render this section first as a compact HTML overview so the founder and deal owner can see the request shape quickly.

| Field | Content |
| --- | --- |
| Request purpose | What decision or diligence step the materials support |
| Highest-priority items | The top three required materials |
| Deadline | Requested response date or dependency |
| Sensitive items | Any legal, customer, security, financial, or counsel-routed materials |
| Founder action | Clear next step and preferred delivery channel |

## Request Summary

| Field | Content |
| --- | --- |
| Company | Name and current process stage |
| Recipient | Founder, CFO, advisor, or counsel |
| Requested by | Firm owner |
| Response deadline | Date or dependency |
| Sensitivity | Founder-friendly, internal, counsel-reviewed |

## Request Table

| Category | Requested Material | Priority | Notes |
| --- | --- | --- | --- |
| Company overview | Latest deck, company one-pager, product overview | Required | Avoid duplicates already provided |
| Product | Demo, screenshots, technical overview, roadmap | Required / Optional | Match to stage depth |
| Customer and GTM | References, case studies, pipeline, churn or retention detail | Required | Mark sensitive customer data |
| Financial | Financial model, revenue metrics, burn, runway, cap table | Required | Ask for units and reporting period |
| Team | Hiring plan, org chart, key biographies | Optional / Later-stage | Tailor to current concerns |
| Legal / security | IP, data, security, regulatory, contracts | Later-stage | Route sensitive legal asks through counsel |
| Fundraise | Current round materials, term expectations, timing | Required | Ask only where relevant |

## Usage Notes

Adapt the request to the current stage and avoid asking for documents already provided. Mark required, optional, and later-stage items separately so founders can respond without overloading the first request.
