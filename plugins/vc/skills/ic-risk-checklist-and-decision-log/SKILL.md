---
id: ic-risk-checklist-and-decision-log
name: IC Risk Checklist & Decision Log
description: >
  Prepare investment committee risk checklists, debate prompts, agenda inputs,
  decision logs, conditions, and post-IC action items. Use this skill when
  reviewing an IC memo, preparing the IC agenda, recording committee outcomes, or
  checking assumptions, unresolved risks, dissent, and cognitive-bias challenge
  prompts. It supports decision discipline; it does not make or record a formal
  investment decision without human signoff.
tags:
  - vc
  - ic
  - risk
  - decision-log
  - governance
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: recommended
      required: false
      note: IC risk and decision logging depends on IC memo/pack artifacts, meeting notes/transcripts, source materials, and prior diligence outputs.
      gracefulDegradation: Produce a checklist or draft decision log from provided context only.
    - kind: setup
      importance: recommended
      required: false
      owner: user
      ownerPath: Provide the IC pack, memo, agenda, notes, transcript, or decision context before claiming completeness.
      confirmationRequired: true
      gracefulDegradation: Mark missing evidence and unresolved decisions.
  routingHints:
    preferredSurface: skill
    notes:
      - Use this for risk discipline, agenda prompts, and draft logs; formal investment decisions remain human-owned.
---

# IC Risk Checklist & Decision Log

Make IC discussion explicit: risks, assumptions, dissent, conditions, and next steps.

## Minimum Inputs

- IC memo or investment pack
- DD summaries and source artifacts
- decision ask or options
- IC agenda, notes, or transcript if recording a decision

## Process

1. Extract unresolved risks, assumptions, and decision-critical unknowns.
2. Build a risk checklist with evidence, severity, owner, and mitigation/validation path.
3. Produce agenda prompts and challenge questions.
4. Include cognitive-bias challenge prompts such as anchoring, confirmation bias, groupthink, optimism bias, and authority bias when evidence suggests a risk.
5. If recording a meeting, distinguish formal decision, dissent, conditions, and action items.

## Output Contract

Return:

- `risk_checklist`
- `assumption_register`
- `challenge_prompts`
- `cognitive_bias_checks`
- `decision_log_draft`
- `dissent_and_objections`
- `conditions`
- `post_ic_action_items`
- `approval_required`

## Tool Guidance

Use attached IC materials, meeting notes/transcripts, CRM/deal context, and task outputs
when available. Meeting transcripts may come from Granola, Otter, Fireflies, Zoom,
Google Meet, Teams, or supplied notes.

## Boundaries

- Do not diagnose people or claim psychological state.
- Do not make the investment decision.
- Do not record a formal decision without human confirmation.
- Do not convert dissent into consensus; preserve disagreements.
