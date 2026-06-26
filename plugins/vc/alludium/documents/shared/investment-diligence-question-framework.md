---
id: vc.document.investment_diligence_question_framework
title: Investment Diligence Question Framework
documentType: methodology
supportedProjectTypes:
  - vc_deal_room
  - vc_origination_pipeline
  - vc_investment_management
summary: Structured diligence question-bank methodology for investment workstreams.
---

# Investment Diligence Question Framework

## Rendered Artifact Contract

When this document is used to create a task output artifact:

- Create the final artifact with `artifact_createTextArtifact`.
- Use a `.html` filename and `mimeType: "text/html"`.
- Set `content` to a complete standalone safe static HTML document beginning with `<!doctype html>`.
- Convert this Markdown scaffold into semantic HTML sections, tables, and lists with small inline CSS in a `<style>` block.
- Follow the shared VC HTML Artifact Contract in Template Use Guidance for section order, first-screen summary, spacing, responsive tables, and compact structured outputs.
- Do not create `.md` or `text/markdown` artifacts for rendered outputs.
- Do not copy HTML into structured task output fields; those fields remain plain text or artifact UUIDs.

## At A Glance Output

Every rendered question bank should begin with a compact HTML overview before the full question table.

| Field | Content |
| --- | --- |
| Diligence objective | The decision this question bank supports |
| Top must-answer questions | Three to five questions most likely to change proceed/pass, valuation, terms, or approval conditions |
| Highest-risk workstream | The area with the biggest decision impact or weakest evidence |
| Evidence gaps | The key artefacts, interviews, models, or counsel inputs still needed |
| Owner / next step | The immediate assignment needed to unblock the question bank |

## Purpose

Use this framework to turn known facts, risk hypotheses, and evidence gaps into an assignable diligence question bank. Good questions are specific, answerable, owned, and tied to a decision. Avoid generic diligence prompts that do not change the investment view.

## Question Bank Format

| Priority | Workstream | Question | Why It Matters | Expected Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- |
| Must answer | Market / customer / product / team / financial / legal / fund fit | Specific question | Decision affected by the answer | Source, artifact, interview, model, or counsel input | Named owner | Open / In review / Answered / Blocked |

## Workstreams

| Workstream | Example Focus Areas |
| --- | --- |
| Market and customer | Market urgency, buyer pain, budget owner, category growth, customer proof, customer concentration |
| Product and technology | Product depth, architecture, defensibility, roadmap, security, AI or data dependencies, scalability |
| Team and governance | Founder quality, hiring plan, board needs, references, key-person risk, role coverage |
| Financial and unit economics | Revenue quality, gross margin, burn, runway, payback, forecast realism, use of funds |
| Commercial motion | Pipeline, sales cycle, pricing power, retention, expansion, channel risk, partner dependencies |
| Legal and regulatory | IP, contracts, privacy, employment, regulatory exposure, licenses, counsel items |
| Company structure and deal terms | Cap table, option pool, shareholder rights, round dynamics, valuation, reserves, ownership path |
| Exit and return fit | Acquirer logic, comparable exits, exit timing, fund-return sensitivity |

## Prioritization

Use `must answer` for questions that can change proceed/pass, valuation, terms, or approval conditions. Use `should answer` for questions that affect conviction or workstream planning. Use `optional` only for useful context that should not block the investment decision. End with the top five unanswered questions and the decision each one informs.

## Evidence Request Standard

For each must-answer question, state the requested artifact or interaction. Good outputs do not only ask "what is the traction?" They ask for the specific pipeline export, customer reference, model bridge, contract, architecture diagram, cap table, IP assignment, counsel note, or expert call needed to resolve the decision.
