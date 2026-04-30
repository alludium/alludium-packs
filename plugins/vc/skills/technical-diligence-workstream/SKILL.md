---
id: technical-diligence-workstream
name: Technical Diligence Workstream
description: >
  Run a VC technical diligence workstream from product, architecture, engineering,
  security, IP, AI/ML, infrastructure, and team evidence. Use this skill when
  producing a technical risk checklist, expert-review agenda, or technical
  workstream summary. It supports review and question generation; it does not
  claim code, security, IP, or architecture verification without source access.
tags:
  - vc
  - technical-diligence
  - product
  - engineering
  - risk
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: recommended
      required: false
      note: Technical diligence depends on supplied product/architecture docs, security or IP materials, optional repo/code access, first-party website evidence, and public technical sources.
      gracefulDegradation: Produce a document-based technical risk checklist and questions only.
    - kind: setup
      importance: recommended
      required: false
      owner: user
      ownerPath: Provide architecture docs, product docs, repo/code access, security/IP materials, or expert notes before claiming technical verification.
      confirmationRequired: true
      gracefulDegradation: Mark unverified technical claims and ask for source access.
  routingHints:
    preferredSurface: skill
    notes:
      - Use this for technical diligence planning and synthesis; specialist review and final technical acceptance remain human-owned.
---

# Technical Diligence Workstream

Create a source-grounded technical diligence view.

## Minimum Inputs

- product description and architecture/product docs
- engineering/team context
- security, privacy, compliance, IP, patent, or OSS materials when relevant
- repo/code access or expert review notes if code-level review is expected

## Process

1. Summarize product and architecture from supplied sources.
2. Identify technical claims and whether they are verified, unverified, or contradicted.
3. Review engineering team coverage and execution risks.
4. Surface security, scalability, data, AI/ML, OSS, IP, and vendor-dependency concerns.
5. Produce a technical scorecard and expert-review questions.

## Output Contract

Return the domain sections plus the evidence fields needed for safe human review:

- `architecture_product_summary`
- `technical_team_assessment`
- `oss_licensing_ip_checks`
- `ai_ml_risk_assessment`
- `scalability_security_concerns`
- `technical_scorecard`
- `expert_review_questions`
- `source_gaps`
- `source_links`: source document names, repository references, URLs, expert notes, or dataset records used
- `assumptions`: assumptions behind architecture, scalability, security, AI/ML, IP, and team conclusions
- `confidence_and_evidence_quality`: high/medium/low confidence by major conclusion, with reason
- `technical_risks`: prioritized risks and their evidence basis
- `open_questions`: questions that need founder, expert, security, legal, or engineering review
- `suggested_next_actions`: validation steps, owner suggestions, and required approvals
- `human_review_prompts`: specialist-only or investor-only judgments

## Tool Guidance

Use attached technical documents first. Use Firecrawl for first-party product,
docs, security, careers, or engineering pages. Use Exa, Brave, and SerpAPI for
public technical context where useful.

## Boundaries

- Do not claim code review happened without repo/code access.
- Do not claim security, IP, privacy, or compliance signoff.
- Do not treat marketing pages as proof of architecture.
- Do not publish technical findings externally without approval.
