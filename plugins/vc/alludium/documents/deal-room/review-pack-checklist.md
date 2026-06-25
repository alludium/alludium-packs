---
id: vc.document.review_pack_checklist
title: Review Pack Checklist
documentType: checklist
supportedProjectTypes:
  - vc_deal_room
summary: Checklist for team and partner review packs.
---

# Review Pack Checklist

## Rendered Artifact Contract

When this template is used to create a task output artifact:

- Create the final artifact with `artifact_createTextArtifact`.
- Use a `.html` filename and `mimeType: "text/html"`.
- Set `content` to a complete standalone safe static HTML document beginning with `<!doctype html>`.
- Convert this Markdown scaffold into semantic HTML sections, tables, and lists with small inline CSS in a `<style>` block.
- Do not create `.md` or `text/markdown` artifacts for rendered outputs.
- Do not copy HTML into structured task output fields; those fields remain plain text or artifact UUIDs.


## Pack Header

| Field | Content |
| --- | --- |
| Company | Name, sector, geography, current lifecycle state |
| Pack type | Team review / partner review / gap review |
| Decision requested | Continue, pass, launch diligence, prepare IC, approve condition |
| Prepared by | Owner and date |
| Required reviewers | Names or roles |

## Source Inputs

| Source Input | Use For |
| --- | --- |
| Screening scorecard or sourcing summary | Current recommendation, confidence, fit rationale, pass/watch/continue logic |
| Diligence reports and question bank | Workstream findings, open questions, evidence quality, required next work |
| Founder materials and meeting notes | Company narrative, founder claims, commercial context, unanswered questions |
| CRM or project state | Lifecycle stage, owner, prior decisions, reviewer history, next approval point |
| Source index and linked artifacts | Citation coverage, missing evidence, reviewer pre-read links |

## Required Sections

| Section | Required Content | Complete? |
| --- | --- | --- |
| Company snapshot | What the company does, customer, product, stage, source path | Yes / No |
| Decision context | Current stage, decision requested, prior decisions, owner | Yes / No |
| Evidence summary | Key source artifacts and what each supports | Yes / No |
| Screening view | Scorecard, pass/watch/continue rationale, confidence | Yes / No |
| Diligence summary | Workstream findings, open gaps, and disconfirming evidence | Yes / No |
| Risks | Top risks, severity, owner, and mitigation path | Yes / No |
| Recommended next action | Exact action, owner, dependency, and approval needed | Yes / No |
| Source index | Links or artifact IDs for every material claim | Yes / No |

## Decision Readiness

| Readiness Area | Status | Notes |
| --- | --- | --- |
| Critical evidence available | Ready / Gap / Blocked |  |
| Material claims cited | Ready / Gap / Blocked |  |
| Risks explicit | Ready / Gap / Blocked |  |
| Next action owner clear | Ready / Gap / Blocked |  |
| Human approval point clear | Ready / Gap / Blocked |  |

## Escalation Rule

Do not escalate a pack as decision-ready if critical evidence is missing. Escalate it as gap review when the purpose is to decide what to investigate next.
