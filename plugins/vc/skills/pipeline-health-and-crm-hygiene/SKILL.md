---
id: pipeline-health-and-crm-hygiene
name: "Pipeline Health & CRM Hygiene"
description: >
  Assess deal pipeline health and maintain CRM quality across a VC investment pipeline.
  Use this skill when producing a weekly pipeline digest, evaluating whether a deal should
  advance/hold/regress in stage, identifying stale deals, generating CRM update suggestions
  from recent evidence, or creating specific next-step tasks for deal owners. Three closely
  related capabilities unified by one method — translating deal activity into actionable
  pipeline intelligence.
tags:
  - vc
  - pipeline
  - crm
  - hygiene
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: recommended
      required: false
      note: Pipeline health depends on available CRM, deal-activity, and supporting research sources. Provider-specific tool IDs are intentionally omitted because CRM and deal activity may be supplied through several configured surfaces.
      gracefulDegradation: Ask for a pipeline snapshot or use provided deal activity instead of fabricating CRM state.
    - kind: setup
      importance: recommended
      required: false
      owner: user
      ownerPath: Route missing Affinity, deal-room, or research access through owned setup paths before relying on it.
      confirmationRequired: true
      gracefulDegradation: Provide suggested updates for human review only and avoid claiming CRM mutation.
  routingHints:
    preferredSurface: skill
    notes:
      - CRM hygiene changes remain suggestions unless a separate confirmed mutation path is available.
---

# Pipeline Health & CRM Hygiene

Translate deal activity signals into actionable pipeline intelligence. Assess stage
readiness, patch CRM data from evidence, identify stale deals, and generate owner-assigned
next steps. Produce a weekly digest that gives the team a clean, current view of the
pipeline without manual CRM grooming.

This skill covers pipeline hygiene — not deal screening, not diligence, not IC prep. It
operates on deals already in the pipeline and keeps them accurately staged, well-documented,
and moving.

## Critical Guardrail

CRM changes are ALWAYS suggestions. Never auto-update CRM/deal-system fields, stage values,
notes, or any other record without explicit human approval. Every suggestion must include the
evidence that supports it and a clear before/after comparison.

## Pipeline Stages

Use this as the platform's default working stage model for VC pipeline hygiene.
Treat it as an operating convention, not immutable source doctrine:

1. **Origination** — deal sourced, initial contact made
2. **Screening** — inbound triaged, 10-Factor screen underway or complete
3. **Evaluation** — diligence in progress, artifacts being produced
4. **Decision** — IC review, memo circulated, decision pending
5. **Negotiation** — term sheet discussion, structuring
6. **DD (Due Diligence)** — formal legal/financial/technical DD
7. **Closing** — documents executing, funds transferring

Every active deal in the connected CRM/deal system or supplied pipeline snapshot should
sit in exactly one stage. Movement between stages requires evidence documented below.

## Minimum Inputs

Before running any pipeline assessment, confirm:

- Access to a CRM/deal-system pipeline snapshot (Affinity, Salesforce, HubSpot, Attio,
  Airtable, Notion, or equivalent) with current stages, owners, and last activity dates
- At least one of: recent meeting notes, email activity, CRM activity log, or deal artifacts

If no CRM/deal-system data or supplied pipeline snapshot is available, stop and report the
source gap rather than guessing pipeline state.

## Core Method

1. Pull the current pipeline snapshot from the connected CRM/deal system or supplied
   source: all active deals, their stages, owners, last activity timestamps, and recent notes.
2. For each deal, run three assessments in sequence:
   - Stage assessment (advance / hold / regress)
   - CRM patch check (fields vs evidence)
   - Next-step generation (if action is needed)
3. Flag stale deals based on stage-specific thresholds.
4. Compile the weekly digest from individual deal assessments.

---

## 1. Stage Assessment

For each deal, evaluate whether the current stage is correct by comparing available evidence
against the requirements for the current and adjacent stages.

### Stage Advancement Criteria

A deal should advance when evidence satisfies the exit criteria for its current stage:

| From        | To          | Required Evidence                                                                |
| ----------- | ----------- | -------------------------------------------------------------------------------- |
| Origination | Screening   | Intro received and classified, founder materials on file                         |
| Screening   | Evaluation  | 10-Factor evaluation complete, key unknowns documented, team decision to proceed |
| Evaluation  | Decision    | Diligence pack substantially complete, key unknowns documented, IC memo drafted  |
| Decision    | Negotiation | IC decision to proceed, terms discussed, principal assigned                      |
| Negotiation | DD          | Term sheet signed or agreed in principle                                         |
| DD          | Closing     | DD complete, no blocking findings, legal docs in final form                      |

### Hold Signals

Recommend holding at current stage when:

- Evidence is accumulating but exit criteria not yet met
- Active engagement exists (meetings scheduled, materials requested) but deliverables pending
- A specific blocker is identified and being worked (name it)

### Regress Signals

Recommend moving a deal backward when:

- New information materially weakens the thesis (e.g., key metric was misstated)
- A critical team member departed
- Competitive development undermines the deal's positioning
- The founder has gone unresponsive for longer than the stale threshold AND prior evidence
  was thin

### Output per Deal

```
## [Company Name] — Currently: [Stage]

**Recommendation**: Advance to [Stage] / Hold / Regress to [Stage]
**Evidence**:
- [Specific fact supporting the recommendation, with source]
- [Second fact if applicable]
**Missing for advancement**: [What would need to happen to advance]
**Owner**: [Deal owner from CRM/deal-system snapshot]
```

---

## 2. CRM Patch Methodology

Compare CRM/deal-system field values to the latest available evidence. Produce structured
update suggestions for any field that is stale, missing, or contradicted by newer information.

### Fields to Check

For each deal, check at minimum:

- Company name and description
- Stage (handled by stage assessment above)
- Deal owner
- Last contact date
- Next meeting date
- Key contacts (founders, board members)
- Round size and valuation (if known)
- Sector/vertical tags
- Source/referrer
- Notes (last meaningful note vs last activity)

### Comparison Method

1. Read current CRM/deal-system field values.
2. Scan recent evidence: meeting notes, email threads, deck updates, news, call summaries.
3. For each field where evidence differs from CRM value:
   - Record the current CRM value
   - Record the evidence-based value
   - Cite the source (meeting date, document name, URL)
   - Classify as: **Missing** (field empty, evidence exists), **Stale** (field outdated),
     or **Contradicted** (field conflicts with newer evidence)

### Suggestion Format

```
### CRM Update Suggestion: [Company Name]

| Field | Current Value | Suggested Value | Source | Type |
|-------|--------------|-----------------|--------|------|
| Round size | $2M | $3M | Deck v3 (2026-03-15) | Stale |
| Key contact | [empty] | Jane Smith, CTO | First call notes (2026-03-10) | Missing |
| Sector tags | "fintech" | "fintech, regtech" | Company website /about | Stale |

**Action required**: Review and approve in the CRM/deal system. No changes made.
```

Never apply these updates directly. Present them for approval.

---

## 3. Next-Step Generation

For every deal that needs action, generate a concrete next step. The quality bar for next
steps is high — vague tasks waste pipeline meetings.

### Good Next Steps

Every next step must have ALL of:

- **Specific action**: what exactly needs to happen (not "follow up" — instead "send
  follow-up email requesting Q1 revenue numbers mentioned in call")
- **Owner**: a named person from the investment team
- **Deadline**: a specific date, or relative timeframe ("by Friday", "within 3 business days")
- **Context**: why this action matters now (connects to stage advancement or risk mitigation)

### Bad Next Steps (Never Generate These)

- "Follow up with founder" — no specific action, no deadline
- "Do more research" — no scope, no owner
- "Check on progress" — too vague to be actionable
- "Continue diligence" — not a task, it is a state description
- Any task without an owner

### Next-Step Sources

Derive next steps from:

- Stage advancement gaps: what evidence is missing to advance?
- Meeting action items: what was promised in the last call?
- Stale deal recovery: what re-engagement action would unblock?
- CRM gaps: what information needs to be gathered to fill missing fields?
- External signals: news or competitive moves that require a response

### Output Format

```
### Next Steps: [Company Name]

1. **[Action verb] [specific deliverable]**
   Owner: [Name] | Due: [Date]
   Why: [One sentence connecting to pipeline progress]

2. **[Action verb] [specific deliverable]**
   Owner: [Name] | Due: [Date]
   Why: [One sentence]
```

---

## 4. Stale Deal Identification

A deal is stale when it has no meaningful activity (meetings, emails, note updates, artifact
creation) for longer than the threshold for its current stage. Different stages tolerate
different periods of inactivity.

### Stale Thresholds by Stage

These are reasonable default operating thresholds for the platform. They should be
calibrated from a firm's historical pipeline data when that data is available:

| Stage       | Days Without Activity | Rationale                                                                        |
| ----------- | --------------------- | -------------------------------------------------------------------------------- |
| Origination | 7                     | Early deals lose momentum fast; if no response in a week, nudge or deprioritize  |
| Screening   | 10                    | Materials should arrive quickly; 10 days suggests founder disengagement          |
| Evaluation  | 14                    | Diligence has multiple workstreams; 2 weeks without any movement is a signal     |
| Decision    | 7                     | IC-ready deals should move to decision quickly; delays suggest cold feet         |
| Negotiation | 10                    | Active negotiation should have regular touchpoints                               |
| DD          | 21                    | Formal DD has longer cycles (legal review, data rooms); 3 weeks is the threshold |
| Closing     | 14                    | Closing should be mechanical; 2 weeks of silence is unusual                      |

### Stale Deal Output

For each stale deal, produce:

```
### STALE: [Company Name]
Stage: [Stage] | Owner: [Name]
Last activity: [Date] ([N] days ago)
Last known context: [Brief summary of what was happening]
Suggested action: [Specific nudge, escalation, or archive recommendation]
```

### Stale vs Dead

- **Stale** (1x threshold): nudge the owner, suggest a specific re-engagement action.
- **Very stale** (2x threshold): flag prominently for pipeline review discussion.
- **Likely dead** (3x threshold): recommend archiving with a clear rationale. Do not
  auto-archive.

---

## 5. Weekly Pipeline Digest

Compile individual deal assessments into a single weekly digest. This is the primary output
for Monday pipeline meetings.

### Digest Structure

```
# Weekly Pipeline Digest — [Date Range]

## Pipeline Summary
- Active deals: [N]
- Stage distribution: Origination [N] | Screening [N] | Evaluation [N] | Decision [N] | Negotiation [N] | DD [N] | Closing [N]
- Deals moved this week: [N]
- Stale deals: [N] ([N] very stale, [N] likely dead)
- CRM updates suggested: [N]
- Next steps generated: [N]

## Stage Moves This Week
[Table of deals that changed stage, with direction and evidence summary]

| Deal | From | To | Key Evidence |
|------|------|----|-------------|
| [Company] | Screening | Evaluation | 10-Factor complete, score 3.8/5 |

## Deals Needing Attention

### Stage Change Recommendations
[Deals where a stage change is recommended but not yet made]

### Stale Deals
[Ordered by severity: likely dead first, then very stale, then stale]

### CRM Updates Pending
[Summary of suggested field updates, grouped by deal]

## Next Steps for This Week
[All generated next steps, grouped by owner so each person sees their action list]

### [Owner Name]
1. [Company] — [Action] (Due: [Date])
2. [Company] — [Action] (Due: [Date])

### [Owner Name]
1. ...

## Notes
[Any cross-cutting observations: cluster of stale deals in one sector, pattern of
missing CRM fields, pipeline concentration risk, etc.]
```

---

## Tool Guidance

Use tools to gather evidence. Do not ask the user for information that tools can provide.

| Tool / Source                  | When to Use                                                                                                                                                                                                                                                        |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| CRM/deal system                | Pipeline snapshot, stages, owners, activity dates, notes, and field values. Affinity is the preferred design-partner example; Salesforce, HubSpot, Attio, Airtable, Notion, or a supplied spreadsheet/snapshot can serve the same role when connected or provided. |
| Exa                            | Company news that affects deal status — competitor funding, leadership changes, regulatory shifts, and product launches.                                                                                                                                           |
| Brave / SerpAPI                | Public-search fallback for current news, source triangulation, and hard-to-find public signals.                                                                                                                                                                    |
| Dealroom / private-market data | Competitive financing context, sector funding trends, comparable financings, and market timing signals when connected.                                                                                                                                             |

### Tool Sequencing

1. Always start with the CRM/deal-system snapshot or supplied pipeline snapshot to get the current pipeline state.
2. Run Exa, Brave, or SerpAPI searches for deals in Evaluation or later stages where external signals matter.
3. Use Dealroom when financing or market activity context would change a stage recommendation or urgency.

Do not run Exa or Dealroom checks for every deal — focus on deals where external context
would materially change the assessment.
If Dealroom is unavailable, use Exa-only external context and explicitly note that
structured financing context was not checked.

---

## Guardrails

- CRM changes are suggestions, never auto-applied. Every suggestion includes evidence and
  requires explicit approval before any CRM/deal-system update.
- Stage changes are recommendations. The agent does not move deals between stages.
- External communications (nudge emails, follow-ups) are drafts only. Never send without
  approval.
- Every recommendation must include the evidence that supports it. "This deal feels stale"
  is not acceptable — "No activity since 2026-03-01 (12 days), last action was founder
  email requesting metrics" is.
- Do not fabricate activity dates or invent evidence.
- If CRM/deal-system data is incomplete or access is limited, say so explicitly rather than
  working from partial data without disclosure.
- Stale thresholds are defaults. If the firm has customized thresholds, use those instead.
- Do not recommend archiving deals in Negotiation or later stages without flagging the
  seniority of the decision (partner-level).

---

## Related Skills

This skill works well with:

- `ten-factor-evaluation` — screening scores feed stage assessment at the Screening stage
- `meeting-prep-and-summary` — meeting outputs are primary evidence for stage moves and CRM patches
- `company-research-and-enrichment` — enrichment data fills CRM gaps and informs next steps
- `vc-task-and-next-step-generation` — use when pipeline, meeting, IC, diligence, or
  closing findings need owner/date/action drafts rather than broad pipeline hygiene
