---
id: founder-outreach-and-intro-paths
name: "Founder Outreach & Intro Paths"
description: >
  Convert research and relationship intelligence into high-quality founder
  communications. Use this skill when finding the warmest intro path to a
  founder, drafting personalised outreach (email, LinkedIn DM, or warm intro
  request), classifying inbound replies by intent, or deciding which channel
  and tone to use for a specific founder context. All external communications
  are drafts only — never sent automatically.
tags:
  - vc
  - outreach
  - origination
  - warm-intro
  - communications
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: recommended
      required: false
      note: Warm intro and outreach drafting depend on available relationship, CRM, founder-research, and email-history tools. Provider-specific tool IDs are intentionally omitted because relationship and outreach context may come from several configured surfaces.
      gracefulDegradation: Draft from provided research and clearly mark relationship or channel evidence as missing.
    - kind: setup
      importance: recommended
      required: false
      owner: user
      ownerPath: Route missing CRM, relationship, Gmail, or enrichment access through owned setup paths before relying on it.
      confirmationRequired: true
      gracefulDegradation: Produce human-review drafts only and avoid claiming outreach was sent or CRM was updated.
  routingHints:
    preferredSurface: skill
    notes:
      - Outreach outputs remain drafts for review; this skill never sends messages or writes CRM records by itself.
---

# Founder Outreach & Intro Paths

Find the best path to a founder, draft personalised outreach across channels,
and classify inbound replies. The unifying method: turn enrichment data and
relationship intelligence into communication that earns a response.

All outputs are **drafts for human review**. This skill never sends messages.

## Minimum Inputs

Before starting any outreach work, confirm the following exist:

- A target founder name and company, or
- An Affinity company/person record, or
- An existing Company Research & Enrichment profile

If none exist, stop and request the minimum missing input.

## Three Capabilities

This skill covers three closely related jobs. Each can run independently or
as part of a sequenced outreach workflow.

1. **Warm Intro Path Finding** — search Affinity for the strongest path to the
   founder and recommend an approach.
2. **Outreach Drafting** — write a personalised message in the right channel
   format (email, LinkedIn DM, or warm intro request).
3. **Reply Triage** — classify an inbound reply and recommend the next action.

---

## Capability 1: Warm Intro Path Finding

### Method

1. Search Affinity for the target founder and their company.
2. Identify all relationship paths:
   - **Direct** — investment team member has a direct Affinity relationship with the
     founder (met, emailed, connected).
   - **One-hop** — investment team member knows someone who knows the founder. Pull
     the intermediary's relationship strength and last interaction date.
   - **Two-hop** — the firm knows A, A knows B, B knows the founder. Only surface
     two-hop paths when no direct or one-hop path exists.
3. If Gmail thread search is available, check for prior email contact with the
   founder or company and treat that as relationship evidence alongside Affinity.
4. For each path, extract:
   - Connector name and their relationship to the founder
   - Relationship strength (Affinity score or interaction frequency)
   - Recency of last interaction (date)
   - Nature of relationship (co-investor, board member, former colleague,
     portfolio founder, conference contact)
5. Rank paths by:
   - **Strength first** — strong relationship > weak relationship
   - **Recency second** — contacted in last 6 months > contacted 2 years ago
   - **Shortest path third** — direct > one-hop > two-hop
6. If no warm path exists, state that clearly and recommend cold outreach with
   the strongest personalisation hooks available.

### Output Shape

```
# Warm Intro Paths: [Founder Name] at [Company]

## Recommended Path
[Connector] -> [Founder]
- Relationship: [nature, strength, last interaction date]
- Why this path: [1-2 sentences]

## Alternative Paths
| # | Path | Strength | Last Contact | Notes |
|---|------|----------|-------------|-------|
| 1 | [Direct/A->B] | Strong/Med/Weak | YYYY-MM-DD | ... |
| 2 | ... | ... | ... | ... |

## No Warm Path Available
[Only if no paths found — recommend cold outreach strategy]
```

### Guardrails — Intro Paths

- Never fabricate relationship data. If Affinity has no record, say so.
- Do not assume a LinkedIn connection equals a warm relationship.
- If the relationship signal is old or thin, flag it as "verify before requesting intro"
  rather than treating it as a strong path.

---

## Capability 2: Outreach Drafting

### Personalisation Framework

Every outreach message must include at least two of the following
personalisation hooks. Generic praise ("I was impressed by your company") is
never acceptable.

| Hook Type          | Source             | Example                                                                                  |
| ------------------ | ------------------ | ---------------------------------------------------------------------------------------- |
| Founder background | Harmonic, LinkedIn | "Your work on X at [previous company]..."                                                |
| Company milestone  | Exa, Harmonic      | "Congratulations on [specific launch/hire/partnership]..."                               |
| Thesis alignment   | Firm thesis doc    | "We've been focused on [specific thesis area] and [company] sits at the intersection..." |
| Shared connection  | Affinity           | "[Mutual contact] mentioned..."                                                          |
| Recent news        | Exa                | "I saw [specific article/announcement] about..."                                         |
| Market signal      | Exa, Harmonic      | "The shift toward [specific trend] is something we've been tracking..."                  |

**Personalisation rules:**

- Cite specific, verifiable details. "Your Series A" is weak. "Your $4M round
  led by [investor] in March" is strong.
- Never reference information the founder has not made public.
- If enrichment data is thin, say so and ask for more context rather than
  writing a generic message.

### Channel-Specific Guidance

#### Email (<120 words)

- **Tone**: Professional, direct, peer-to-peer. Not salesy.
- **Structure**: Hook (1-2 sentences with personalisation) -> why the firm is relevant
  (1 sentence on thesis fit) -> Ask (specific, low-friction: "Would you be
  open to a 20-minute call next week?")
- **Subject line**: Short, specific, no clickbait. Reference the company name
  or a shared connection.
- **Produce 2 subject line options** so the reviewer can choose.
- **Sign-off**: From the investment team member who has the strongest relationship
  context (or the partner responsible for the sector).

#### LinkedIn DM (<300 characters)

- **Tone**: Casual-professional. Conversational, not formal.
- **Structure**: One personalisation hook -> One sentence on why reaching out
  -> Soft ask or open question.
- **Constraint**: LinkedIn DMs over 300 characters feel like spam. Be ruthless
  about brevity.
- **Produce two variants** so the reviewer can choose.

#### Warm Intro Request Email

- **Audience**: The intermediary (connector), not the founder.
- **Tone**: Respectful of the connector's relationship. Never presumptuous.
- **Structure**: Context (why the firm is interested in the founder, 1-2 sentences)
  -> The ask ("Would you be comfortable making an introduction?") -> Make it
  easy (offer to draft the forwardable blurb).
- **Include a forwardable blurb**: 2-3 sentences the connector can paste into
  an email to the founder. This blurb follows the email personalisation rules.

### Output Shape — Outreach Draft

```
# Outreach Draft: [Founder Name] at [Company]

## Channel: [Email / LinkedIn DM / Warm Intro Request]

## Context
- Personalisation hooks used: [list]
- Sources: [Affinity record, Harmonic profile, Exa article URL]
- Sending as: [investment team member name]

## Draft

[The message text]

## Subject Line Options (email only)
1. [Option 1]
2. [Option 2]

## Forwardable Blurb (warm intro only)

[2-3 sentence blurb for the connector to forward]

## Reviewer Notes
- [Any caveats, thin-data warnings, or alternative angles]
- Suggested follow-up cadence: [e.g. 2 nudges over 10 days]
```

### Guardrails — Outreach Drafting

- **Draft only.** Never trigger a send action on Gmail, LinkedIn, or any
  messaging tool. Output is text for human review.
- **Do-not-contact list.** Before drafting, check Affinity for a do-not-contact
  flag or "pass — do not re-engage" note. If found, stop and report. Do not
  draft the message.
- **Rate limits.** If Affinity shows the founder was contacted by the firm within
  the recent past, flag it and let the reviewer decide whether another touch is warranted.
- **No fabricated credentials.** Never claim the firm has invested in a company it
  has not, or that a team member knows the founder when they do not.
- **Tone consistency.** Match the firm's voice: knowledgeable, respectful, direct,
  never desperate or hyperbolic.

---

## Capability 3: Reply Triage

### Method

1. Read the inbound reply (email or LinkedIn message).
2. Classify into exactly one of five categories.
3. Recommend the next action.

### Classification Categories

| Category             | Signal Patterns                                                                    | Recommended Action                                                                         |
| -------------------- | ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| **Interested**       | Positive language, asks about the firm, wants to learn more, suggests timing       | Draft a follow-up proposing specific meeting times. Propose CRM update: mark as "Engaged." |
| **Meeting Request**  | Explicitly proposes or accepts a call/meeting                                      | Draft a confirmation and calendar invite. Propose CRM update: mark as "Meeting Scheduled." |
| **More Info**        | Asks clarifying questions about the firm, fund, thesis, or terms before committing | Draft a response answering the specific questions. Do not over-sell.                       |
| **Not Interested**   | Declines, says not raising, not the right time, asks to check back later           | Propose CRM note with the reason and any "check back" date. Draft a graceful close.        |
| **Auto-Reply / OOO** | Out-of-office, automated bounce, assistant redirect                                | Propose CRM note for the OOO return date if given. Draft a re-contact reminder.            |

### Output Shape — Reply Triage

```
# Reply Triage: [Founder Name] at [Company]

## Classification: [Category]
## Confidence: [High / Medium / Low]

## Evidence
- Key phrases: "[quoted text from reply]"
- Reasoning: [1-2 sentences on why this category]

## Recommended Action
[Specific next step]

## Draft Response (if applicable)
[Response text — draft only]

## CRM Update (suggested)
- Affinity status: [proposed update]
- Notes: [what to log]
```

### Guardrails — Reply Triage

- If the reply is ambiguous, classify as "More Info" and draft a clarifying
  follow-up rather than guessing intent.
- Never auto-update Affinity. Propose the CRM change; the reviewer decides.
- If the reply contains a referral to someone else ("You should talk to X"),
  flag it as a new warm intro path and trigger Capability 1.
- If the reply includes sensitive attachments, data room material, or substantial
  diligence documents, flag that the next step is document review / ingest rather than
  continuing generic outreach.

---

## Sequenced Workflow

When all three capabilities run together for a single target:

1. Run Capability 1 (Warm Intro Path Finding).
2. Based on the result:
   - If a strong warm path exists -> draft a warm intro request (Capability 2).
   - If no warm path -> draft a cold email or LinkedIn DM (Capability 2).
3. When a reply arrives -> classify it (Capability 3).
4. Based on classification -> draft the appropriate follow-up (Capability 2).

## Tool Guidance

Use tools to gather evidence. Do not ask the user for information that tools
can provide.

| Tool                 | When to Use                                                                                      |
| -------------------- | ------------------------------------------------------------------------------------------------ |
| Affinity             | Relationship paths, prior firm interactions, do-not-contact flags, deal stage, contact history   |
| Harmonic             | Founder enrichment — background, previous companies, role history, company growth signals        |
| Exa                  | Recent news, press coverage, product launches, fundraising announcements — personalisation hooks |
| Brave / SerpAPI      | Public-search fallback for recent news, founder references, and source triangulation             |
| LinkedIn (Pipedream) | Profile data for LinkedIn DM drafting, mutual connections verification                           |

If an existing Company Research & Enrichment profile exists, use it as the
starting point for personalisation hooks. Do not re-research what is already
captured.

## Global Guardrails

These apply across all three capabilities:

- **All external communications are drafts.** No exceptions. No sends.
- **Receipts are mandatory.** Every draft must cite its personalisation sources
  (Affinity record, Harmonic profile, Exa article URL).
- **Do-not-contact is absolute.** If Affinity flags a founder or company, stop
  immediately. Do not draft, do not suggest workarounds.
- **Rate-limit awareness.** Check Affinity for recent firm outreach to the same
  founder before drafting. Flag if contacted within 30 days.
- **No CRM writes.** Propose Affinity updates in the output. Never write
  directly to CRM unless explicitly approved by the invoking workflow.
- **Sensitive information stays internal.** Never include portfolio company
  financials, LP names, or internal deal terms in outreach drafts.

## Related Skills

This skill works well with:

- `company-research-and-enrichment` — foundation data and enrichment profiles
  feed personalisation hooks
- `ten-factor-evaluation` — screening context informs why the firm is reaching out
  and what thesis alignment to reference
- `meeting-prep-and-summary` — once a meeting is booked, hand off to meeting
  prep for the call brief
