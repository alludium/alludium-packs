---
id: vc-outreach-draft-queue
name: "VC Outreach Draft Queue"
description: >
  Draft short, question-led founder outreach notes for approved active candidates
  while keeping sending and status changes as human actions.
tags:
  - vc
  - origination
  - outreach
  - drafting
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
  routingHints:
    preferredSurface: skill
    notes:
      - Drafting is allowed; sending is never automatic.
---

# VC Outreach Draft Queue

Use this skill for candidates with active actions such as `Meet`, `IC-Summary`, or `Reach out`.

## Eligibility

Draft only when:

- Candidate action is eligible
- Founder LinkedIn URL or approved contact route exists
- Manual status/contact progress is empty or explicitly eligible
- There is a concrete evidence-backed hook

Skip when:

- No founder contact route exists
- Candidate is `Watch` without approval
- Candidate is already contacted
- The hook would require unsupported praise or speculation

## Draft Rules

- Keep notes short.
- Lead with a specific observed signal.
- Ask a concrete question.
- Avoid generic flattery.
- Do not mention internal scoring, scraping, or hidden source mechanics.

## Output

Return founder, company, profile URL, draft note, personalization angle, hook evidence, confidence, and skip reason where applicable.

## Boundaries

- Do not send messages.
- Do not update outreach status.
- Do not create browser-extension drafts unless explicitly approved.
