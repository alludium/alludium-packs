# VC Deal Flow Stage and Task Contract Refactor Spec

Status: implementation slices 1-5 complete; release metadata pending
Owner surface: `plugins/vc/alludium`
Primary project type: `vc_deal_room`
Related project type: `vc_origination_pipeline`
Baseline: `origin/main` at `01e177376000d8e29862f86f54925a2419c77e0c`

## Problem

The current Deal Pipeline lifecycle collapses several distinct investment workflow phases into `assessment`, then places formal diligence before investment review and term-sheet work. That makes early task routing noisy, blurs the boundary between screening and evaluation, and makes reusable operational tasks look stage-specific when they should be available throughout a live deal.

The pack already has the right high-level product split:

- `vc_origination_pipeline` owns standing sourcing, source configuration, candidate enrichment, outreach drafts, and promotion into a Deal Pipeline.
- `vc_deal_room` owns one promoted investment opportunity from intake through investment, pass, or archive.

The main gap is the Deal Pipeline stage model and task contracts. The pack should preserve generic, reusable VC terminology rather than source-specific methodology names. Fund-specific frameworks can remain documents, workspace configuration, or optional methodology skills.

## Goals

1. Replace the collapsed Deal Pipeline lifecycle with a generic investment workflow that can represent the underlying process stages without using source-specific labels.
2. Separate intake, screening, opportunity evaluation, decision review, deal structuring, formal diligence, contracts, and closing.
3. Rename or reframe meeting tasks so they apply to any relevant call or meeting, not only an initial founder call.
4. Turn fuzzy task ideas into explicit task contracts with inputs, outputs, stage availability, agent routing, skill dependencies, and hard boundaries.
5. Remove stale `plannedRequiredSkills` usage from released runtime templates once the referenced skills exist.
6. Keep upstream origination and single-opportunity Deal Pipeline work distinct.

## Non-Goals

- Do not add fund-specific names to public task titles, stage names, skill names, or document IDs.
- Do not collapse `vc_origination_pipeline` into `vc_deal_room`.
- Do not make tasks send external messages, write CRM records, create projects, move stages, negotiate terms, or provide legal advice without explicit human approval and platform-supported actions.
- Do not add a large new agent set. Prefer extending existing agents and adding narrowly scoped skills.

## Baseline State On `origin/main`

At the baseline this branch was created from, `vc_deal_room` declares these lifecycle states:

`intake`, `assessment`, `diligence`, `review`, `term_sheet`, `closing`, `invested`, `passed`, `archived`.

At that baseline, the `assessment` stage owns:

- thesis target sourcing
- inbound screening
- investment screen
- founder material request
- initial-call preparation
- initial-call summary
- follow-up evaluation

That is too broad. It mixes source/origination work, project creation, fund-fit screening, meeting operations, material collection, and deeper evaluation.

`vc_origination_pipeline` currently models upstream sourcing separately. That boundary is correct and should be preserved.

## Branch Implementation State

This branch is not spec-only. The first implementation slice updates the Deal Pipeline project type toward the target lifecycle by changing:

- `vc_deal_room.initialVersion.lifecycleStates`
- `vc_deal_room.initialVersion.lifecycleTransitions`
- command-view `stageGroups`
- `investment_stage` field options
- project task mappings for existing Deal Pipeline tasks
- relevant agent template primary-stage metadata
- pack, plugin, inventory, and project-type version metadata

The remaining implementation work should focus on making task contracts match the new lifecycle rather than re-litigating whether the stage model belongs in this branch.

## Target Deal Pipeline Lifecycle

| State | Label | Purpose |
| --- | --- | --- |
| `intake` | Intake | Capture the opportunity, source context, CRM/source references, artifacts, ownership, and missing setup information. |
| `screening` | Screening | Run a fast fund-fit and evidence-quality screen from available source materials. |
| `evaluation` | Evaluation | Prepare and summarize meetings, request materials, run deeper opportunity evaluation, and create structured follow-up questions. |
| `decision_review` | Decision Review | Prepare partner or investment committee review packs, agendas, memos, memo review, and decision records. |
| `deal_structuring` | Deal Structuring | Analyze commercial terms, valuation, cap table, round construction, and term-sheet negotiation support. |
| `formal_diligence` | Formal Diligence | Run full workstreams after a preliminary decision or agreed deal path. |
| `contracts` | Contracts | Coordinate legal document review, disclosure-letter review, counsel questions, and document-status tracking. |
| `closing` | Closing | Track conditions precedent, signing readiness, transaction bible, funds/share-certificate completion, and portfolio handoff. |
| `watchlist` | Watchlist | Keep attractive but not-ready opportunities visible for later review. |
| `passed` | Passed | Preserve pass rationale, feedback, and source history. |
| `invested` | Invested | Mark completed investment and hand off to portfolio onboarding. |
| `archived` | Archived | Terminal inactive state for stale, duplicate, or administratively closed rooms. |

## Stage Groups

The command-view stage groups should use these groups:

| Group Key | Label | States |
| --- | --- | --- |
| `intake` | Intake | `intake` |
| `screening` | Screening | `screening` |
| `evaluation` | Evaluation | `evaluation` |
| `decision_review` | Decision | `decision_review` |
| `deal_structuring` | Structuring | `deal_structuring` |
| `formal_diligence` | Diligence | `formal_diligence` |
| `contracts` | Contracts | `contracts` |
| `closing` | Closing | `closing` |
| `outcomes` | Outcomes | `watchlist`, `passed`, `invested`, `archived` |

## Existing Task Remapping

| Current Task | Target Stage Availability | Required Change |
| --- | --- | --- |
| `affinity-deal-room-import` | `intake` | Keep as intake/import setup evidence. |
| `screen-inbound-opportunity` | `intake`, guided creation | Narrow to opportunity-intake triage and project creation field collection. Make deck optional. |
| `run-investment-screen` | `screening` | Rename title/description toward generic investment fit screen. Keep existing slug initially for compatibility. |
| `run-follow-up-evaluation` | `evaluation` | Reframe as generic opportunity evaluation. Avoid source-specific framework names. |
| `prepare-initial-call` | all active stages, initial mapping `evaluation` | Rename title/description to `Prepare Meeting`. Keep slug initially for compatibility, then migrate slug in a later release. |
| `summarize-initial-call` | all active stages, initial mapping `evaluation` | Rename title/description to `Summarize Meeting Records`. Keep slug initially for compatibility, then migrate slug in a later release. |
| `request-founder-materials` | all active stages, initial mapping `evaluation` | Treat as a reusable material-request task. |
| `generate-diligence-questions` | `evaluation`, `formal_diligence`, all active stages when invoked manually | Treat as reusable question generation, not formal diligence only. |
| `review-opportunity-status` | all active stages | Treat as stage-agnostic operations/status review. |
| `source-thesis-targets` | primarily `vc_origination_pipeline` | Remove or de-emphasize Deal Pipeline stage mapping unless used for a specific opportunity gap. |
| `prepare-lead-gen-packet` | primarily `vc_origination_pipeline` | Remove or de-emphasize Deal Pipeline stage mapping. |
| `prepare-team-review-pack` | `decision_review` | Keep as decision-review prep unless later split into evaluation pack vs IC pack. |
| `prepare-partner-review-pack` | `decision_review` | Keep as decision-review prep. |
| `create-ic-memo` | `decision_review` | Keep. |
| `review-ic-memo` | `decision_review` | Keep. |
| `prepare-ic-agenda` | `decision_review` | Keep. |
| `record-ic-decision` | `decision_review` | Keep. |
| `review-term-sheet` | `deal_structuring` | Keep, but consider renaming family away from `closing`. |
| `run-commercial-dd` | `formal_diligence` | Keep. |
| `run-financial-dd` | `formal_diligence` | Keep. |
| `run-founder-evaluation` | `formal_diligence`, optional earlier evaluation use | Keep but clarify formal DD vs early founder evaluation. |
| `run-technical-dd` | `formal_diligence` | Keep. |
| `manage-closing-checklist` | `closing` | Keep, but future contracts tasks should precede it. |
| `verify-conditions-precedent` | `closing` | Keep. |
| `prepare-portfolio-onboarding` | `closing`, post-investment | Keep. |

## New Or Refactored Task Contracts

### `capture-opportunity-intake`

Purpose: capture opportunity source context and project creation facts before screening.

Required inputs:

- `company_name`
- one of `source_note`, `source_artifact_ids`, or `source_record_ref`

Optional inputs:

- `company_domain`
- `source_type`
- `referrer`
- `founder_names`
- `crm_record_ref`
- `pitch_deck_artifact_id`
- `source_thread_url`

Required outputs:

- `opportunity_intake_artifact_id`
- `source_index`
- `known_fields`
- `missing_fields`
- `recommended_next_task`
- `projectCreation`

Boundary:

- May propose project creation fields.
- Must not create projects, write CRM records, send founder communications, or move stages.

Initial implementation:

- Refactor `screen-inbound-opportunity` toward this role before adding a new slug.

### `run-investment-fit-screen`

Purpose: perform a fast generic fund-fit screen using configured investment criteria and current evidence.

Required inputs:

- `company_name`
- one of `pitch_deck_artifact_id`, `source_material_artifact_ids`, `source_thread_artifact_id`, or `opportunity_intake_artifact_id`

Optional inputs:

- `meeting_notes`
- `source_links`
- `fund_criteria`
- `company_domain`
- `deal_source`

Required outputs:

- `investment_screen_scorecard_artifact_id`
- `criterion_scores`
- `overall_recommendation`
- `unknowns`
- `red_flags`
- `human_review_prompts`
- `next_actions`

Boundary:

- Recommendation is evidence-backed advice only.
- Human owns pass, watch, continue, external sends, CRM writes, and stage movement.

Initial implementation:

- Retitle `run-investment-screen`; keep slug for compatibility.

### `run-opportunity-evaluation`

Purpose: perform deeper opportunity evaluation after a deal passes screening.

Required inputs:

- `company_name`
- `investment_screen_scorecard_artifact_id`
- one of `meeting_summary_artifact_ids`, `founder_material_artifact_ids`, or `customer_evidence_artifact_ids`

Optional inputs:

- `market_sources`
- `technical_sources`
- `financial_sources`
- `customer_evidence`
- `existing_questions`
- `portfolio_overlap_context`

Required outputs:

- `opportunity_evaluation_artifact_id`
- `evaluation_scorecard`
- `key_claims_register`
- `critical_unknowns`
- `initial_diligence_recommendations`
- `recommended_decision_path`

Boundary:

- Must avoid source-specific framework labels.
- Must not create formal DD tasks or move to decision review without human approval.

Initial implementation:

- Reframe `run-follow-up-evaluation`; keep slug for compatibility.

### `prepare-meeting`

Purpose: prepare for any founder, management, advisor, customer, expert, partner, IC, legal, or closing meeting.

Required inputs:

- `company_name`
- `meeting_type`
- `meeting_goal`

Optional inputs:

- `stage`
- `attendees`
- `meeting_datetime`
- `calendar_event_ref`
- `affinity_context_ref`
- `prior_artifact_ids`
- `known_risks`
- `focus_topics`

Required outputs:

- `meeting_brief_artifact_id`
- `agenda`
- `question_list`
- `relationship_context`
- `risk_prompts`
- `source_links`

Boundary:

- Draft-only. No invites, external sends, CRM writes, or calendar writes without explicit approval.

Initial implementation:

- Retitle `prepare-initial-call`; keep slug for compatibility.

### `summarize-meeting-records`

Purpose: summarize any meeting record and convert it into claims, questions, actions, and safe update drafts.

Required inputs:

- `meeting_record_artifact_ids`
- `company_name`

Optional inputs:

- `meeting_type`
- `meeting_notes`
- `stage`
- `deal_room_url`
- `crm_context_ref`
- `prior_artifact_ids`

Required outputs:

- `meeting_summary_artifact_id`
- `claims_register`
- `contradictions_or_gaps`
- `open_questions`
- `action_items`
- `crm_update_draft`
- `stage_recommendation`

Boundary:

- Must not update CRM, send follow-up, create tasks, or move stages without approval.

Initial implementation:

- Retitle `summarize-initial-call`; keep slug for compatibility.

### `prepare-decision-review-pack`

Purpose: prepare the pack for partner or investment committee review.

Required inputs:

- `opportunity_evaluation_artifact_id`
- `diligence_question_bank_artifact_id`
- `key_material_artifact_ids`

Optional inputs:

- `deal_terms_snapshot`
- `cap_table_artifact_id`
- `financial_forecast_artifact_id`
- `prior_decision_notes`

Required outputs:

- `decision_review_pack_artifact_id`
- `decision_ask`
- `risk_register`
- `missing_evidence`
- `recommended_next_actions`

Boundary:

- Drafts review material only. Humans own decision and stage movement.

Initial implementation:

- Evaluate whether this is a new task or a narrower refactor of `prepare-partner-review-pack`.

### `analyze-deal-terms`

Purpose: analyze commercial deal terms before or during term-sheet negotiation.

Required inputs:

- `proposed_investment_amount`
- `valuation`
- `round_size`
- `cap_table_artifact_id`

Optional inputs:

- `esop`
- `co_investors`
- `ownership_target`
- `follow_on_reserve_policy`
- `deal_terms_snapshot`
- `financial_forecast_artifact_id`

Required outputs:

- `deal_terms_analysis_artifact_id`
- `ownership_model_summary`
- `valuation_sensitivity`
- `open_commercial_terms`
- `ic_questions`

Boundary:

- Commercial analysis only. No legal advice, negotiation, founder communication, or term approval.

### `track-term-sheet-negotiation`

Purpose: organize open term-sheet issues, give/get options, counsel questions, and approval points.

Required inputs:

- `term_sheet_artifact_id`
- `current_open_terms`
- `ic_constraints`

Optional inputs:

- `founder_comments_or_redline`
- `counsel_notes`
- `cap_table_artifact_id`
- `deal_terms_analysis_artifact_id`

Required outputs:

- `negotiation_brief_artifact_id`
- `open_terms_table`
- `give_get_options`
- `legal_escalations`
- `approval_required`

Boundary:

- Must separate business tradeoffs from counsel review.
- Must not negotiate, send terms, or approve legal language.

### `run-legal-diligence`

Purpose: coordinate legal diligence document review and issue tracking without providing legal advice.

Required inputs:

- `legal_source_artifact_ids`
- `company_name`

Optional inputs:

- `counsel_requirements`
- `ip_artifact_ids`
- `corporate_structure_artifact_id`
- `employment_contract_artifact_ids`
- `litigation_search_artifact_ids`

Required outputs:

- `legal_diligence_artifact_id`
- `legal_document_index`
- `issue_register`
- `counsel_questions`
- `showstopper_risks`

Boundary:

- Review support only. Counsel/human owns legal conclusions.

### `review-investment-documents`

Purpose: coordinate post-term-sheet investment document review and disclosure-letter issues.

Required inputs:

- `investment_document_artifact_ids`
- `term_sheet_review_artifact_id`

Optional inputs:

- `disclosure_letter_artifact_id`
- `counsel_notes`
- `cap_table_artifact_id`
- `board_minutes_artifact_id`

Required outputs:

- `investment_document_review_artifact_id`
- `term_to_document_mapping`
- `open_document_issues`
- `counsel_questions`
- `closing_readiness_notes`

Boundary:

- Does not provide legal advice or signoff.

### `coordinate-capital-call-and-completion`

Purpose: track the final administrative closing sequence after signing readiness.

Required inputs:

- `conditions_precedent_verification_artifact_id`
- `closing_checklist_artifact_id`
- `transaction_bible_artifact_id`

Optional inputs:

- `administrator_contact`
- `capital_call_status`
- `funds_transfer_status`
- `share_certificate_status`

Required outputs:

- `completion_tracker_artifact_id`
- `capital_call_status_summary`
- `funds_transfer_readiness`
- `share_certificate_receipt_status`
- `portfolio_handoff_trigger`

Boundary:

- Tracking and drafting only. No banking, administrator instruction, or legal completion action.

## Skills

### Existing Skills To Promote

Where the task template currently lists a skill in `plannedRequiredSkills` and that skill exists in `plugins/vc/skills`, move it to `requiredSkills` and remove the planned duplicate.

Important examples:

- `commercial-diligence-workstream`
- `financial-diligence-workstream`
- `technical-diligence-workstream`
- `founder-evaluation-and-reference-checking`
- `founder-materials-request`
- `meeting-prep-and-summary`
- `ic-risk-checklist-and-decision-log`
- `closing-coordination-and-cp-tracking`
- `vc-task-and-next-step-generation`

### New Skills To Add

| Skill | Purpose | First Consumer |
| --- | --- | --- |
| `deal-terms-analysis` | Ownership, valuation, round size, ESOP, co-investor, and commercial term analysis. | `analyze-deal-terms` |
| `term-sheet-negotiation-brief` | Open term tracking, give/get framing, approval points, and counsel escalation. | `track-term-sheet-negotiation` |
| `legal-diligence-coordination` | Legal diligence document index, issue register, counsel questions, and legal risk tracking without advice. | `run-legal-diligence` |
| `customer-reference-validation` | Customer reference planning, call summaries, buying-priority validation, adoption risks. | `run-commercial-dd`, `summarize-meeting-records` |
| `opportunity-evaluation-framework` | Generic deep opportunity evaluation methodology, not tied to source-specific factor names. | `run-opportunity-evaluation` |

## Agent Routing

Do not add a new agent until the task and skill split proves existing agents cannot carry the work.

| Agent | Updated Ownership |
| --- | --- |
| `vc_dealflow_concierge` | Intake, material requests, approved outreach drafts, promotion handoff. |
| `vc_first_look_analyst` | Screening and early opportunity evaluation. |
| `vc_meeting_operator` | Meeting prep and meeting summary at any live stage. |
| `vc_diligence_analyst` | Opportunity evaluation support and formal diligence workstreams. |
| `vc_ic_prep_producer` | Decision review, memo assembly, agenda, decision log. |
| `vc_legal_compliance_desk` | Deal structuring support, legal diligence coordination, contracts, closing, onboarding handoff. |
| `vc_pipeline_autopilot` | Cross-stage status review, recurring operations, source health, and schedule/status hygiene. |
| `vc_origination_scout` | Upstream sourcing and candidate discovery only. |

Potential future agent:

- `vc_deal_structuring_analyst`, only if `vc_legal_compliance_desk` becomes too broad after deal-terms and negotiation tasks are added.

## Public Pattern Review

Useful public patterns reviewed:

- Anthropic Financial Services uses generic private-equity commands for deal sourcing, deal screening, DD prep, DD checklist, IC memo, unit economics, returns, and value creation rather than fund-specific vocabulary: <https://github.com/anthropics/financial-services>
- Anthropic's financial-services skill overview frames reusable outputs such as comps, DCF, company profiles, and diligence data packs: <https://claude.com/resources/tutorials/claude-for-financial-services-skills>
- Octagon's public finance skills provide public-market and SEC-analysis patterns that may be useful later for public comparables, S-1 review, risk factors, and market-data enrichment: <https://github.com/OctagonAI/skills>
- CRE agent skill packs provide strong examples of crisp task boundaries for term sheets, negotiation briefs, diligence, legal review support, and closing coordination: <https://github.com/ahacker-1/cre-agent-skills>

The reusable lesson is not to copy domain wording. The useful pattern is a thin task contract, explicit inputs and outputs, reusable methodology skills, and strict boundaries around external actions, legal advice, and human decisions.

## Implementation Plan And Status

### Slice 1: Stage Model And Existing Task Remap

Status: implemented in this branch; needs validation and final review.

- Update `vc_deal_room.initialVersion.lifecycleStates`.
- Update `vc_deal_room.initialVersion.lifecycleTransitions`.
- Update command-view `stageGroups`.
- Update `investment_stage` field options.
- Remap existing Deal Pipeline `projectTaskMappings` to the target states.
- Do not add new task templates in this slice.
- Regenerate generated task/agent Markdown only if YAML changes require it.

### Slice 2: Meeting Task Generalization

Status: implemented in this branch.

- Retitle `prepare-initial-call` as `Prepare Meeting`.
- Retitle `summarize-initial-call` as `Summarize Meeting Records`.
- Update descriptions, tags, instructions, field labels, output names, agent actions, document names or document refs where needed.
- Keep current slugs and filenames for compatibility unless a release migration explicitly handles slug replacement.

### Slice 3: Early Deal Task Clarity

Status: implemented in this branch.

- Reframe `screen-inbound-opportunity` as intake/guided project creation.
- Make pitch deck optional when other source artifacts exist.
- Retitle `run-investment-screen` toward investment fit screen.
- Reframe `run-follow-up-evaluation` toward opportunity evaluation.
- Remove source-specific methodology labels from task text.

### Slice 4: Required Skills Cleanup

Status: implemented in this branch.

- Promote existing planned skills into `requiredSkills`.
- Remove stale `plannedRequiredSkills` where they duplicate real skills.
- Keep unavailable future skills out of runtime task templates.
- Update validator expectations only if needed.

### Slice 5: New Deal Structuring, Legal, And Closing Tasks

Status: implemented in this branch.

- Add `analyze-deal-terms`.
- Add `track-term-sheet-negotiation`.
- Add `run-legal-diligence`.
- Add `review-investment-documents`.
- Add `coordinate-capital-call-and-completion`.
- Add matching skills only where existing skills are insufficient.

### Slice 6: Generated Artifacts And Release Metadata

Status: required before release/PR closeout.

- Run `python3 scripts/generate_markdown.py`.
- Run `python3 scripts/validate_pack.py`.
- Update pack version, README, inventory, manifest, and catalogs according to release-content change rules.

## Validation

Each slice should run:

```bash
python3 plugins/vc/scripts/generate_markdown.py --check
python3 plugins/vc/scripts/validate_pack.py
```

For release-ready PRs, also run:

```bash
python3 plugins/vc/scripts/validate_release_contract.py
git diff --check
```

## Open Questions

1. Should stage-agnostic tasks be represented by repeated mappings across active states, by a new project-type-level availability field, or by platform logic outside the pack contract?
2. Should current slugs be preserved permanently for compatibility, or should a future migration introduce new slugs and aliases?
3. Should `contracts` and `closing` be separate lifecycle states in the first public version, or should `contracts` be added only when the new legal-document tasks land?
4. Should `watchlist` be a lifecycle state, a `current_decision` value, or both?
