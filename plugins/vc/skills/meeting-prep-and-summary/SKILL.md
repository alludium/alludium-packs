---
id: meeting-prep-and-summary
name: "Meeting Prep & Summary"
description: >
  Prepare structured pre-meeting briefs and extract structured post-meeting summaries
  for VC meetings. Use this skill when preparing for a founder call, due diligence
  expert session, board meeting, or customer reference call; when turning a meeting
  transcript into a structured summary with action items; when updating the Deal
  Snapshot after a meeting; or when drafting follow-up communications from meeting
  notes. Adapts depth and focus by meeting type.
tags:
  - vc
  - meetings
  - prep-brief
  - summary
  - action-items
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: recommended
      required: false
      note: Meeting prep and summary depend on available calendar, transcript, notes, CRM, and research context. Provider-specific tool IDs are intentionally omitted because meeting context may come from several configured surfaces.
      gracefulDegradation: Work from provided agenda, notes, transcript, or deal context and mark missing source areas.
    - kind: setup
      importance: recommended
      required: false
      owner: user
      ownerPath: Provide or authorize calendar, notes, transcript, CRM, or deal context through owned paths before relying on it.
      confirmationRequired: true
      gracefulDegradation: Draft a prep brief or summary from available context only; do not claim calendar or CRM changes.
  routingHints:
    preferredSurface: skill
    notes:
      - This skill can prepare and summarize; external follow-up, scheduling, or CRM updates require explicit approval and available tools.
---

# Meeting Prep & Summary

Produce structured pre-meeting briefs and post-meeting summaries for VC meetings.
The goal is to ensure every meeting is prepared for and every meeting produces
captured decisions, action items, and Deal Snapshot updates — not just notes.

This skill covers two closely related capabilities:

1. **Pre-meeting prep briefs** — context, prior interactions, targeted questions
2. **Post-meeting structured summaries** — decisions, action items, KPIs, follow-ups

## Minimum Inputs

### For a Prep Brief

- A calendar event or meeting identifier (date, time, attendees, company name)
- At least one of: Deal Snapshot, Affinity record, pitch deck, or prior meeting notes

### For a Post-Meeting Summary

- A transcript or meeting notes export (Granola, Otter, Fireflies, Zoom, Google Meet)
- The meeting type (founder call, DD expert session, board meeting, customer reference)

If neither exists, stop and ask for the minimum missing input rather than guessing.

## Meeting Type Classification

Classify every meeting into one of four types before proceeding. The type determines
the depth, focus areas, and output shape.

| Type               | Primary Focus                                                          | Depth                                                   |
| ------------------ | ---------------------------------------------------------------------- | ------------------------------------------------------- |
| Founder Call       | 10-Factor validation, relationship building, deal progression          | Medium — cover all factors lightly, go deep on 2-3      |
| DD Expert Session  | Specific unknowns from diligence, technical or market validation       | Deep — narrow scope, exhaust the expert's domain        |
| Board Meeting      | KPI review, strategic decisions, portfolio health                      | Broad — cover all agenda items, flag deviations         |
| Customer Reference | Product satisfaction, competitive comparison, willingness to recommend | Focused — structured interview, capture verbatim quotes |

If the meeting type is ambiguous, infer from attendees and context. If still unclear,
ask before proceeding.

---

## Pre-Meeting Prep Brief

### Core Method

1. Classify the meeting type.
2. Pull company context from the Deal Snapshot or Affinity record.
3. Retrieve prior interaction history from Affinity — last 3 touchpoints with dates,
   participants, and outcomes.
4. Search for recent news and developments (last 30 days) relevant to the company,
   its market, and its competitors.
5. Enrich attendee profiles — role, background, professional background summary if available, prior firm interactions.
6. Generate targeted questions based on meeting type (see below).
7. Draft a suggested agenda with time-boxed segments.
8. Assign roles in the meeting — who should ask what.
9. Define success criteria — what a good outcome from this meeting would be.
10. Assemble the prep brief.

### Targeted Questions by Meeting Type

**Founder Call** — Generate 5-7 questions mapped to the 10-Factor framework. Prioritise
factors with low confidence or unresolved unknowns from the most recent Ten-Factor
Evaluation. If no prior evaluation exists, cover Problem, Product, Traction, Team,
and Business Model.

**DD Expert Session** — Pull the top unknowns from the current diligence artifacts
(82-Factor question bank, Red Flags scan, Traction KPI gaps). Generate 5-10 questions
scoped to the expert's domain. Include specific data points or claims to validate.

**Board Meeting** — Generate questions around:

- KPI trajectory vs plan (pull from Traction KPI Worksheet if available)
- Cash position and runway
- Key hires made or missed
- Strategic decisions pending
- Support requests the company has made or should make

**Customer Reference** — Generate a structured interview guide:

- How did you find and evaluate the product?
- What problem does it solve for you? What did you use before?
- What do you like most? What is the biggest weakness?
- Would you recommend it? To whom?
- Who else did you consider? Why did you choose this product?
- What would make you stop using it?

### Prep Brief Output Shape

```
# Meeting Prep Brief: [Company Name] — [Meeting Type]
Date: [date] | Time: [time] | Duration: [expected]

## Attendees
| Name | Role | Organisation | Prior Firm Interactions |
|------|------|-------------|----------------------|

## Company Snapshot
[2-3 paragraph summary: what the company does, current stage, last known metrics,
deal status in pipeline]

## Prior Interactions
| Date | Type | Participants | Key Outcomes |
|------|------|-------------|-------------|

## Recent Developments
- [News item 1 — source, date, why it matters]
- [News item 2]
- [News item 3]

## Desired Outcomes for This Meeting
[What the investment team needs to learn or accomplish — 2-3 bullets]

## Targeted Questions
1. [Question — maps to Factor X / Unknown Y]
2. ...

## Suggested Agenda (Time-Boxed)
1. [Minutes] — [Topic]
2. [Minutes] — [Topic]
3. [Minutes] — [Topic]

## Roles in the Meeting
| Person | Role in Meeting | Topics to Cover |
|--------|------------------|-----------------|

## Success Criteria
- [What must be learned, resolved, or agreed for this meeting to count as successful]

## Context Documents
[Links to Deal Snapshot, prior meeting summaries, relevant artifacts]
```

---

## Post-Meeting Structured Summary

### Core Method

1. Ingest the transcript or meeting notes. Accept exports from Granola, Fireflies,
   Zoom, or Google Meet.
2. Classify the meeting type if not already known.
3. Extract structured elements:
   - **Key decisions** — what was decided, by whom, with what rationale
   - **Action items** — each with owner, deadline (explicit or inferred), and context
   - **KPIs and metrics mentioned** — with values, time periods, and source context
   - **Concerns raised** — by whom, about what, how serious
   - **Follow-up needs** — next meeting, additional materials requested, introductions needed
4. Generate the structured summary adapted to meeting type.
5. Identify Deal Snapshot updates (see below).
6. Extract explicit next-step actions.
7. Draft follow-up communications if appropriate (always as drafts).

### Meeting-Type-Specific Extraction

**Founder Call** — Map discussion points to 10-Factor categories. Flag any factor where
new evidence changes the confidence level. Capture the founder's answers to validation
questions and note contradictions with prior materials.

**DD Expert Session** — Capture the expert's assessment of each topic discussed. Note
where the expert validated, contradicted, or added nuance to existing diligence
findings. Flag any new risks or unknowns surfaced.

**Board Meeting** — Capture all KPI updates in a structured table. Note strategic
decisions with vote/consensus outcomes. Separate investment-team-owned action items from
company-owned action items. Flag any metric that deviated significantly from plan.

**Customer Reference** — Capture responses in the structured interview format. Extract
verbatim quotes (with timestamps if available). Note competitive intelligence —
alternatives considered, switching triggers, price sensitivity.

### Action Item Extraction Rules

Every action item must have:

- **Description** — what needs to happen
- **Owner** — a named person (not "the team" or "someone")
- **Deadline** — explicit date if stated, otherwise infer from context ("before next
  board meeting" = specific date, "soon" = flag as "deadline TBD")
- **Context** — why this action was raised, linked to the relevant discussion point

Separate action items into two categories:

1. **Investment-team-owned** — actions for investment team members. Propose as draft tasks for approval.
2. **External requests** — actions for the founder, company, or third parties. List as
   requests, not tasks. Do not create tasks for external parties.

### Summary Output Shape

```
# Meeting Summary: [Company Name] — [Meeting Type]
Date: [date] | Duration: [actual] | Participants: [names]

## TL;DR
[3-5 bullet executive summary — the essential takeaways]

## Key Decisions
| # | Decision | Made By | Rationale | Follow-up |
|---|----------|---------|-----------|-----------|

## Action Items — Investment-Team-Owned
| # | Action | Owner | Deadline | Context |
|---|--------|-------|----------|---------|

## Action Items — External Requests
| # | Request | Requested Of | Deadline | Context |
|---|---------|-------------|----------|---------|

## KPIs & Metrics Discussed
| Metric | Value | Period | Trend | Source Context |
|--------|-------|--------|-------|---------------|

## Concerns Raised
| # | Concern | Raised By | Severity | Resolution |
|---|---------|-----------|----------|------------|

## [Meeting-Type-Specific Section]
[Founder Call: 10-Factor Evidence Updates]
[DD Expert: Diligence Finding Updates]
[Board Meeting: Strategic Discussion Notes]
[Customer Reference: Structured Interview Responses]

## Follow-up Needs
- [Next meeting: date/topic if discussed]
- [Materials requested]
- [Introductions needed]

## Receipts
- Transcript source: [tool + link]
- Summary generated: [timestamp]
- Deal Snapshot updates proposed: [list]
```

---

## Deal Snapshot Integration

After every meeting summary, identify updates for the Deal Snapshot:

1. **Decision History** — add a row: Date | Decision | Rationale | Follow-ups | Owner
2. **Meeting Notes** — add link to the new summary
3. **Diligence Artifacts** — update if the meeting produced new evidence for any
   artifact (Traction KPI Worksheet, Red Flags, 10-Factor scores)
4. **Status/Stage** — suggest a stage change if the meeting outcome warrants one
   (e.g., "proceed to DD" after a strong first call)
5. **Receipts** — add links to transcript source and summary document

Present all Deal Snapshot updates as suggestions. Do not write directly to the
Deal Snapshot without explicit approval.

---

## Follow-Up Drafts

Draft follow-up communications when the meeting produced action items or next steps:

**Founder follow-up** — thank the founder, summarise key takeaways (from their
perspective, not the internal assessment), list next steps with owners and timelines,
attach or link any materials promised.

**Internal debrief** — summarise the meeting for investment team members who were not present.
Include the internal assessment, updated conviction level, and recommended next steps.

**Board meeting recap** — formal summary for the portfolio company's records. Include
decisions, action items, and next meeting date.

**Customer reference thank-you** — brief, warm note thanking the reference for their time.

### Guardrail: Drafts Only

All follow-up communications are drafts. Never send automatically. Present each draft
with a clear label: "DRAFT — requires approval before sending." Include the intended
recipient and channel (email, Slack, etc.).

Always preserve important direct quotes with timestamps when the transcript provides them,
especially for customer references, commitments, and metric claims.

---

## Tool Guidance

Use tools to gather context. Do not ask the user for information that tools can provide.

| Tool                                   | When to Use                                                                                                                           |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| Granola                                | Retrieve meeting notes and transcripts when connected. Use semantic search to find prior meetings with the same company or attendees. |
| Otter / Fireflies / Zoom / Google Meet | Alternative transcript and notes sources when connected.                                                                              |
| Affinity                               | Pull prior interaction history, deal status, relationship context, attendee records.                                                  |
| Exa                                    | Recent news, press mentions, market developments for prep briefs.                                                                     |
| Brave / SerpAPI                        | Public-search fallback for current news, source triangulation, and broader market developments.                                       |
| Harmonic                               | Attendee enrichment — founder background, team changes, company signals.                                                              |
| Firecrawl                              | Company website for latest product updates, pricing, team page.                                                                       |

If a transcript is not yet available (meeting just ended), ask when it will be ready
rather than proceeding without it.

---

## Guardrails

- Follow-up drafts are always drafts — never sent automatically.
- Do not fabricate meeting content. If a section of the transcript is unclear or
  inaudible, flag it as "[unclear — verify with attendees]".
- Attribute statements to specific people. "Revenue is growing 20% MoM" is different
  from "The founder claimed revenue is growing 20% MoM."
- Separate fact from opinion. If the founder makes a claim without evidence, note it
  as a claim, not a fact.
- Do not include internal firm assessments or conviction levels in external-facing
  follow-up drafts.
- Do not write directly to CRM, Deal Snapshot, or task systems without explicit
  approval. Present updates as suggestions.
- Summaries include timestamps or quote context when the transcript provides them.
- Tasks are created only for investment-team-owned actions. External actions are listed as requests.

---

## Quality Checks

- Every action item has an owner and a deadline (or explicit "TBD").
- Every KPI mentioned includes a value, time period, and source context.
- Every concern includes who raised it and the severity.
- The summary covers all major discussion topics — cross-check against the transcript
  or agenda.
- No information from the prep brief is presented as if it came from the meeting.
- Citations link back to specific transcript timestamps or sections where possible.

---

## Related Skills

This skill works well with:

- `company-research-and-enrichment` — foundation data for prep briefs
- `ten-factor-evaluation` — maps founder call findings to the 10-Factor scorecard
- `82-factor-diligence-question-generation` — generates targeted questions for DD expert sessions
- `traction-and-saas-unit-economics` — validates KPIs discussed in meetings
- `red-flags-scanner` — cross-references meeting findings against risk patterns
