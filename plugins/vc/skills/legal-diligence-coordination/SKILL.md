---
id: legal-diligence-coordination
name: Legal Diligence Coordination
description: >
  Coordinate VC legal diligence review support by indexing legal documents,
  tracking issues, drafting counsel questions, and surfacing showstopper risks
  without providing legal advice. Use this skill when organizing corporate,
  IP, employment, litigation, regulatory, or document-status evidence for
  counsel and investor review.
tags:
  - vc
  - legal-diligence
  - issue-register
  - counsel
  - contracts
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: recommended
      required: false
      note: Legal diligence coordination is strongest with legal source artifacts, counsel requirements, corporate structure docs, IP docs, employment agreements, and litigation/regulatory searches.
      gracefulDegradation: Produce a document index, issue register, and counsel question list from provided materials only.
    - kind: setup
      importance: recommended
      required: false
      owner: user
      ownerPath: Provide legal data-room sources, counsel requirements, and known risk areas before claiming legal diligence completeness.
      confirmationRequired: true
      gracefulDegradation: Do not claim legal sufficiency or risk clearance.
  routingHints:
    preferredSurface: skill
    notes:
      - Use this for document coordination, issue tracking, and counsel prompts; legal conclusions and signoff remain outside the skill.
---

# Legal Diligence Coordination

Make legal diligence reviewable without turning it into legal advice.

## Minimum Inputs

- legal source artifacts or data-room index
- company name
- counsel requirements when available
- corporate, IP, employment, litigation, or regulatory materials when available

## Process

1. Build a legal document index with source, status, and owner.
2. Classify issues by area, severity, evidence, and counsel dependency.
3. Separate factual document gaps from legal interpretation.
4. Draft counsel questions and investor review prompts.
5. Surface showstopper risks as review candidates, not legal conclusions.

## Output Contract

Return:

- `legal_document_index`
- `issue_register`
- `counsel_questions`
- `showstopper_risks`
- `document_gap_map`
- `review_status_by_area`
- `source_links`: legal artifacts, data-room paths, counsel notes, or searches used
- `assumptions`: assumptions behind document completeness, issue severity, and owner status
- `confidence_and_evidence_quality`: high/medium/low confidence by major conclusion, with reason
- `open_questions`: unresolved legal, counsel, founder, or investor questions
- `suggested_next_actions`: draft actions with owner/date suggestions and approval status
- `human_review_prompts`: items requiring counsel, partner, or founder-facing approval

## Tool Guidance

Use connected document repositories, CRM/deal systems, legal data-room exports, counsel notes, and supplied search results when available. Public searches can help identify missing corporate or litigation context, but they do not replace counsel review.

## Boundaries

- Do not provide legal advice.
- Do not conclude that a document is legally sufficient.
- Do not clear showstopper risks.
- Do not send counsel/founder requests or update legal status without approval.
