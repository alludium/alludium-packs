---
id: vc.document.ic_agenda_template
title: IC Agenda Template
documentType: template
supportedProjectTypes:
  - vc_deal_room
summary: Reusable agenda for investment committee discussion.
---

# IC Agenda Template

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
| Company | Name and sector |
| Meeting date | Date and time |
| Decision owner | Partner or deal lead |
| Decision requested | Approve, reject, continue, approve with conditions |
| Pre-reads | Memo, model, diligence reports, term sheet, review pack |

## Agenda

| Time | Topic | Owner | Materials |
| --- | --- | --- | --- |
| 0:00 | Decision requested and process context |  | Memo |
| 0:05 | Company and round overview |  | Memo / model |
| 0:15 | Thesis and fund-fit discussion |  | Memo |
| 0:30 | Diligence findings by workstream |  | DD reports |
| 0:50 | Key risks and dissenting evidence |  | Risk table |
| 1:05 | Terms, ownership, and reserve implications |  | Model / term sheet |
| 1:20 | Open questions and conditions |  | Decision record |
| 1:30 | Decision and follow-up owners |  | Decision record |

## Decision Options

| Option | Meaning | Required Follow-Up |
| --- | --- | --- |
| Approve | Proceed on proposed terms | Closing and conditions tracking |
| Approve with conditions | Proceed only if named conditions clear | Assign owners and deadlines |
| Continue diligence | Not ready for approval | Assign must-answer questions |
| Pass | Do not proceed | Record rationale and communication plan |

## Preparation Rule

The agenda should link the memo, review pack, and decision record. Keep discussion items decision-oriented rather than turning the agenda into a second memo.
