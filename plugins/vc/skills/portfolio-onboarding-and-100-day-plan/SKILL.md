---
id: portfolio-onboarding-and-100-day-plan
name: Portfolio Onboarding & 100-Day Plan
description: >
  Turn an approved or closing-stage investment into a portfolio onboarding plan,
  board/reporting setup notes, support-intake structure, milestone plan, and
  100-day value-creation agenda. Use this skill after IC approval or closing prep
  when the firm needs a handoff into portfolio operations. It plans onboarding;
  broad portfolio monitoring and platform support workflows are deferred.
tags:
  - vc
  - portfolio
  - onboarding
  - 100-day-plan
  - post-investment
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: recommended
      required: false
      note: Portfolio onboarding depends on closing summary, IC decision, board/reporting expectations, CRM/project context, meeting notes, and support needs.
      gracefulDegradation: Produce a handoff checklist and draft 100-day plan from provided context only.
    - kind: setup
      importance: recommended
      required: false
      owner: user
      ownerPath: Provide closing summary, investment terms, board/reporting expectations, milestones, and owner context.
      confirmationRequired: true
      gracefulDegradation: Avoid claiming board cadence, tasks, or reporting workflows were created.
  routingHints:
    preferredSurface: skill
    notes:
      - Use this for onboarding planning and handoff; task creation, calendar setup, and external communications require approval.
---

# Portfolio Onboarding & 100-Day Plan

Create a practical handoff from investment approval/closing into portfolio work.

## Minimum Inputs

- IC decision or closing summary
- investment terms and board/reporting expectations
- known milestones, risks, and value-creation priorities
- owner context and support needs

## Process

1. Summarize the investment handoff and unresolved closing/onboarding dependencies.
2. Identify board, reporting, governance, and communication setup needs.
3. Convert value-creation priorities into a 100-day plan.
4. Create milestone, owner, cadence, and support-intake recommendations.
5. Surface risks that should be watched after onboarding without creating a portfolio watchtower.

## Output Contract

Return:

- `portfolio_handoff_summary`
- `board_setup_notes`
- `reporting_cadence`
- `hundred_day_plan`
- `milestones`
- `support_request_intake`
- `owner_assignments`
- `open_risks`
- `approval_required`

## Tool Guidance

Use CRM/deal systems, document repositories, meeting notes, calendar context, and task
systems when connected. Examples, when connected, include Affinity, Salesforce, HubSpot,
Google Drive, Notion, Slack, Teams, Asana, ClickUp, Monday, Jira, Linear, or Trello.

## Boundaries

- Do not create board cadence, tasks, calendar events, CRM updates, or external messages without approval.
- Do not imply ongoing portfolio monitoring is active.
- Do not publish internal IC rationale externally.
- Do not treat a 100-day plan as a binding operating plan without company alignment.
