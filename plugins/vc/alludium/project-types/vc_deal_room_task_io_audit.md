# VC Deal Room Task I/O Audit

Status: working audit

This document is the source-of-truth review pass before finalizing the VC Deal Room project schema and `projectTaskMappings`. The current schema/mapping patch in this worktree should be treated as exploratory: it proved that mappings can be declared and validated, but it promoted too many task fields into durable project data and mapped broad context fields mechanically.

## Working Principles

Project data should be a compact durable control plane for the deal, not a duplicated dossier. It should hold identity anchors, source references, current stage/review state, explicit approval/decision state, and artifact references. Large evidence, diligence results, scorecards, checklists, memos, summaries, and review packs should usually live in markdown/file artifacts.

Task inputs should be explicit. If a task needs a project fact or a prior deliverable, it should receive that as an input. Broad `prior_task_outputs` blobs should be removed in favor of named artifact IDs and named project fields.

Task context is execution scratchground. It is appropriate for runtime question/answer history, transient agent notes, and other task-local working state. It should not be prefilled from project fields by default, and it should not be treated as durable output. If open questions discovered during a task need to survive completion, the task should either include them in the artifact or expose an explicit output such as `unresolved_questions`.

Task outputs should separate durable artifacts from task-local completion metadata. Required file outputs are strong candidates for project-level artifact references. Most low-level structured outputs should be folded into the artifact unless they represent concise project state such as a final decision, approval state, stage transition recommendation, or blocker requiring follow-up.

## Current Patch Assessment

The current patch has useful parts worth folding into a redesigned slice:

- It identifies the 25 natural file-backed outputs that should remain first-class project artifact references.
- It adds validator coverage for mapping references, which is worth keeping after the mappings are redesigned.
- It updates inventory/manifest language to say the pack owns the project-task mapping declaration.

The current patch also has parts that should be replaced:

- The 128-field flat schema is too task-field-shaped and too text-heavy.
- `prior_task_outputs` should be removed as a project field and as a task input/context pattern.
- Broad `contextMappings` for `deal_room_url`, `source_artifacts`, `open_questions`, and `prior_task_outputs` should not be kept.
- Most non-artifact output mappings should be deleted or moved into artifacts/task-local outputs.

## Target Project Data Shape

The Data tab should eventually render grouped sections rather than one long flat field list. Until the renderer supports explicit section metadata, field order should still follow these logical sections:

1. Deal identity and source: company, source system, CRM/source record references, owner, lead partner, confidentiality.
2. Source materials and working links: uploaded pitch deck artifact, deal room, source thread, transcripts, founder materials, source artifact references.
3. Stage and decision state: current lifecycle stage, current decision, review state, approval state, next decision date.
4. Artifact index: one compact area listing the stage artifacts and their latest IDs/status.
5. Stage-specific operating fields: only a small number of live operational fields that are genuinely useful across tasks, such as meeting date, missing materials, active blockers, and explicit decision ask.

Most stage evidence should be reached through artifact previews/links, not copied into project fields.

Pitch decks should be uploaded platform artifacts, not URL inputs. A raw `pitch_deck_url` field makes deck handling inconsistent with downstream artifact references and weakens reviewability. The task model should prefer a file input such as `pitch_deck_artifact_id`, optionally with a source URL captured as metadata on the uploaded artifact or as a secondary non-required source reference.

## Stage Model Review

The current `vc_deal_room` lifecycle has 21 states:

`lead_gen`, `deal_flow`, `screening`, `initial_call`, `follow_up`, `founder_evaluation`, `team_review`, `partner_review`, `commercial_dd`, `technical_dd`, `financial_dd`, `investment_committee`, `term_sheet`, `legal_review`, `legal_diligence`, `final_dd`, `signing`, `portfolio_onboarding`, `invested`, `passed`, and `archived`.

This is too granular for a user-facing Deal Room lifecycle. Several of these are task workstreams, review moments, or terminal statuses rather than stages. The command view already points in the right direction by grouping many of these into broader buckets, but its four groups are probably too broad for task activation and VC operating control.

The next project type should use 6 to 8 primary lifecycle stages. Tasks can still be associated with precise stage entry through `projectTaskMappings`, but the task-level activation policy should carry eligibility requirements, manual review gates, and optional auto-create behavior. Stage count should describe the deal's journey; task mapping should describe what work becomes available inside that stage.

### Proposed Six-Stage Flow

This is the strongest candidate if we want a clean, VC-readable control flow:

| Proposed Stage | Purpose | Current States Folded In | Candidate Tasks |
| --- | --- | --- | --- |
| `intake` | Capture deal identity, source, materials, and initial setup. | setup/admin parts of `screening` | `create-deal-room` |
| `assessment` | Decide whether the opportunity merits deeper work. | `lead_gen`, `deal_flow`, `screening`, `initial_call`, `follow_up` | `screen-inbound-opportunity`, `source-thesis-targets`, `prepare-initial-call`, `summarize-initial-call`, `run-ten-factor-screen`, `run-follow-up-evaluation`, `request-founder-materials`, `evaluate-investment-opportunity` |
| `diligence` | Run focused commercial, technical, financial, founder, and question-set workstreams. | `founder_evaluation`, `commercial_dd`, `technical_dd`, `financial_dd` | `generate-82-factor-questions`, `run-founder-evaluation`, `run-commercial-dd`, `run-technical-dd`, `run-financial-dd` |
| `review` | Assemble internal review packs and committee materials, then record the decision. | `team_review`, `partner_review`, `investment_committee` | `prepare-team-review-pack`, `prepare-partner-review-pack`, `create-ic-memo`, `prepare-ic-agenda`, `review-ic-memo`, `record-ic-decision` |
| `term_sheet` | Review terms and negotiate/approve terms before closing. | `term_sheet`, early legal review | `review-term-sheet` |
| `closing` | Track closing, CP verification, signing, and portfolio handoff. | `legal_review`, `legal_diligence`, `final_dd`, `signing`, `portfolio_onboarding` | `manage-closing-checklist`, `verify-conditions-precedent`, `prepare-portfolio-onboarding` |

Terminal outcomes should likely be statuses or terminal state values separate from the main stage flow: `invested`, `passed`, and `archived`. They are not work stages in the same sense as assessment or diligence.

### Proposed Eight-Stage Variant

If six stages feels too compressed for VC teams, use this slightly richer flow:

1. `intake`
2. `assessment`
3. `diligence_planning`
4. `diligence`
5. `investment_review`
6. `term_sheet`
7. `closing`
8. `portfolio_onboarding`

The eight-stage variant gives team/partner review and portfolio onboarding more visible space. The tradeoff is more lifecycle transitions and more stage labels for users to interpret.

### Current Recommendation

Start with the six-stage flow:

`intake -> assessment -> diligence -> review -> term_sheet -> closing`

Represent `invested`, `passed`, and `archived` as terminal outcomes/statuses rather than normal intermediate stages. If portfolio handoff needs a distinct experience after the closing work proves out, split it from `closing` later as `portfolio_onboarding`.

Task activation should not require one lifecycle state per task. Instead:

- A stage entry can make several candidate tasks available.
- Each task mapping can declare required project inputs and artifact inputs.
- A task can be auto-created only when policy explicitly allows it.
- A task can remain manual/review-gated even when all required inputs are present.
- Stage dashboards can show relevant artifacts and pending tasks grouped by stage without turning every workstream into a lifecycle state.

## Field Classification Legend

- Project input: durable project fact, suitable for project data.
- Artifact input: explicit prior file/artifact reference.
- Task-local input: supplied for one task; should not become project schema by default.
- Context: runtime task context such as ask-question transcript and working notes.
- Artifact output: primary reviewable document/file.
- Project state output: small state update worth surfacing on the project.
- Task-local output: completion metadata, should remain on task or inside artifact.
- Revise task: task shape likely needs changes before mapping.

## Stage And Task Inventory

| Bucket | Stage | Task | Required Inputs | File Outputs | Initial Audit Direction |
| --- | --- | --- | --- | --- | --- |
| Stage workflow | assessment | `source-thesis-targets` | `thesis_area`, `geography` | `thesis_target_list_artifact_id` | Reusable assessment/origination task. Keep available in Deal Room when thesis work helps assess the opportunity, but do not make it mandatory for every deal. Keep `thesis_area`, `geography`, maybe `stage_focus` as project inputs when relevant. Move target list, fit rationale, intro paths, source links, assumptions, risks, and next actions into the artifact. No `prior_task_outputs` context. |
| Stage workflow | lead_gen | `prepare-lead-gen-packet` | `candidate_companies`, `meeting_date` | `lead_generation_packet_artifact_id` | Likely pipeline/meeting-level rather than single Deal Room task. `candidate_companies` is not a single-deal project field. Consider whether this belongs to a pipeline project type or remains task-local. Artifact should carry packet details. |
| Stage workflow | deal_flow | `prepare-deal-flow-agenda` | `pipeline_snapshot`, `meeting_date` | none | This is not a single-deal artifact today and may belong outside VC Deal Room. Consider moving to pipeline/admin bucket or giving it a file output such as `deal_flow_agenda_artifact_id`. `pipeline_snapshot` should not be a single deal field. |
| Stage workflow | deal_flow | `evaluate-investment-opportunity` | `company_name`, `current_stage` | none | This task is mostly stage routing. If retained, outputs should become task-local recommendation or explicit project state only after review. Remove `prior_task_outputs`; pass named artifacts if needed. |
| Project/admin | screening | `create-deal-room` | `company_name` | none | Admin/setup task. Keep out of stage artifact chain unless it creates a setup artifact. Inputs are project identity/source refs. Outputs like folder plan/source index should probably be a setup artifact or task-local, with only `deal_room_url` promoted if human-approved. |
| Stage workflow | screening | `screen-inbound-opportunity` | `company_name`, `source_thread_url` | `first_look_scorecard_artifact_id` | Strong artifact task. Project inputs: company/source thread/uploaded pitch deck artifact/referrer/thesis context. Replace optional `pitch_deck_url` with `pitch_deck_artifact_id` or source artifact refs. Artifact should hold fit recommendation, missing info, red flags, pass draft, evidence quality, and next actions. Project state may receive a reviewed recommendation/status only. |
| Project/admin | screening | `request-founder-materials` | `company_name`, `missing_materials` | `founder_materials_request_artifact_id` | Founder-facing/request task. Keep draft message and checklist in artifact. Project may track due date and approval state, but avoid making checklist/open questions durable fields by default. |
| Stage workflow | initial_call | `prepare-initial-call` | `company_name`, `pitch_deck_url` | `initial_call_brief_artifact_id` | Strong artifact task, but input shape should change. Replace required `pitch_deck_url` with required `pitch_deck_artifact_id`; source URL can live as artifact metadata or optional source reference. Brief content and question lists should live in artifact. |
| Stage workflow | initial_call | `run-ten-factor-screen` | `company_name`, `pitch_deck_url` | `ten_factor_scorecard_artifact_id` | Strong artifact task, but input shape should change. Replace required `pitch_deck_url` with required `pitch_deck_artifact_id`, plus optional meeting notes/source artifact refs. Factor scores, unknowns, prompts, risks, and recommendation should be in scorecard artifact; only reviewed status should update project state. |
| Stage workflow | initial_call | `summarize-initial-call` | `meeting_transcript_url`, `company_name`, `deal_room_url` | `customer_insights_artifact_id` | Strong artifact task. Transcript URL is source material. Claims register, contradictions, action items, CRM draft, and recommendation should live in artifact unless a follow-up task is explicitly created. |
| Stage workflow | follow_up | `run-follow-up-evaluation` | `company_name`, `deal_room_url` | none | Looks like pre-artifact-era structured output. Decide whether this should produce a `follow_up_evaluation_artifact_id` or be absorbed by other tasks. Remove `prior_task_outputs`. |
| Stage workflow | follow_up | `generate-82-factor-questions` | `company_name`, `known_claims` | `eighty_two_factor_questions_artifact_id` | Strong artifact task. `known_claims` should likely come from customer insights/scorecard artifact, not free project text. Question set, rationale, owners, urgency, and source gaps belong in artifact. |
| Stage workflow | founder_evaluation | `run-founder-evaluation` | `founder_names`, `linkedin_profiles` | `founder_evaluation_artifact_id` | Strong artifact task. Founder names/profiles are project inputs. Reference summaries, founder dossier, risk assessment, stop signals, and human judgment prompts belong in artifact. |
| Stage workflow | team_review | `prepare-team-review-pack` | DD artifact IDs, `prior_task_outputs`, `ten_factor_summary` | `team_review_pack_artifact_id` | Needs revision. Required `prior_task_outputs` and summary text should be replaced with explicit artifact inputs, especially scorecard/question/customer insight artifacts. Team review pack should aggregate artifacts. |
| Stage workflow | partner_review | `prepare-partner-review-pack` | review/DD artifact IDs, `team_review_pack`, `open_questions` | `partner_review_pack_artifact_id` | Needs revision. `team_review_pack` JSON and `open_questions` required inputs should likely be artifact/reference inputs or task context Q&A. Output details belong in partner pack artifact. |
| Stage workflow | commercial_dd | `run-commercial-dd` | `company_name` | `commercial_dd_artifact_id`, `market_analysis_artifact_id`, `customer_reference_summary_artifact_id` | Strong artifact task, possibly too many separate artifacts but reasonable. Inputs should be source artifacts/material links, not broad context. Outputs should be artifact references only unless a reviewed blocker is explicitly project-level. |
| Stage workflow | technical_dd | `run-technical-dd` | `architecture_docs`, `repo_or_code_access` | `technical_dd_artifact_id` | Strong artifact task. Inputs are source material refs or links. Output details should live in technical DD artifact. |
| Stage workflow | financial_dd | `run-financial-dd` | `financial_statements`, `forecast_model` | `financial_dd_artifact_id`, `unit_economics_artifact_id` | Strong artifact task. Inputs are source material refs or links. Output details should live in artifacts. |
| Stage workflow | investment_committee | `create-ic-memo` | review/DD artifact IDs, `stage_outputs`, `dd_summaries` | `investment_memo_artifact_id` | Needs revision. Required `stage_outputs` and `dd_summaries` should be replaced by explicit artifact inputs. IC memo content/checklist/risks/citation coverage belong in artifact. `decision_ask` may be project state only after review. |
| Stage workflow | investment_committee | `prepare-ic-agenda` | `investment_memo_artifact_id`, `ic_pack`, `decision_ask` | `ic_agenda_artifact_id` | Needs revision. `ic_pack` should probably be explicit artifact refs, not JSON. Agenda/checklist/follow-up questions/pre-read needs belong in agenda artifact. |
| Stage workflow | investment_committee | `review-ic-memo` | `investment_memo_artifact_id`, `ic_agenda_artifact_id`, `ic_memo`, `ic_pack` | `ic_memo_review_artifact_id` | Needs revision. Requiring both artifact IDs and pasted `ic_memo`/`ic_pack` duplicates source. Keep artifact inputs; remove duplicate richtext/JSON unless there is a specific review override use case. |
| Stage workflow | investment_committee | `record-ic-decision` | `investment_memo_artifact_id`, `ic_agenda_artifact_id`, `ic_transcript_or_notes`, `decision_options` | `ic_decision_record_artifact_id` | Strong artifact task with real project state output. Decision outcome, stage transition, and conditions may update project state after approval; transcript/notes remain input/source. |
| Stage workflow | term_sheet | `review-term-sheet` | `term_sheet`, `deal_terms` | `term_sheet_review_artifact_id` | Strong artifact task. Term sheet/deal terms should ideally be artifact/source refs. Recommendation/approval required can update project approval state only after human review. |
| Stage workflow | final_dd | `verify-conditions-precedent` | `closing_checklist_artifact_id`, `cp_checklist`, `evidence_links` | `conditions_precedent_verification_artifact_id` | Strong artifact task. `cp_checklist` and evidence links may be source artifacts/links. Missing items and signing readiness belong in artifact, with only approved blocker/closing status project updates. |
| Stage workflow | signing | `manage-closing-checklist` | `ic_decision_record_artifact_id`, `term_sheet_review_artifact_id`, `closing_workplan`, `legal_document_status` | `closing_checklist_artifact_id` | Strong artifact task. Closing checklist artifact should carry owner/due date table, blockers, daily status, and readiness. Project may carry compact closing status and blocker flag. |
| Stage workflow | portfolio_onboarding | `prepare-portfolio-onboarding` | decision/checklist/CP artifact IDs, `closing_summary`, `investment_terms` | `portfolio_onboarding_plan_artifact_id` | Strong artifact task. `closing_summary` and `investment_terms` should likely be artifact/source refs or extracted from closing artifacts. Output plan/milestones/owners belong in onboarding artifact, with limited project state. |

## Immediate Task Definition Issues

These are the first issues to fix before rebuilding the schema:

1. Remove or replace `prior_task_outputs` across the VC task templates. Use explicit artifact inputs instead.
2. Remove broad context fields from templates unless a task has a concrete runtime-only reason to receive them.
3. Replace `pitch_deck_url` task inputs with uploaded file/artifact inputs such as `pitch_deck_artifact_id`.
4. Convert low-level structured outputs into markdown/file artifact content where the task already has a primary artifact output.
5. Add file outputs for tasks that are still returning rich structured deliverables without artifacts, or move them out of the Deal Room stage chain if they are operational/admin tasks.
6. Avoid duplicating artifact content as richtext/json inputs, especially in IC review tasks.

## Proposed Next Audit Order

1. Admin and pipeline boundary: `create-deal-room`, `prepare-deal-flow-agenda`, `prepare-lead-gen-packet`.
2. Screening and initial call: `screen-inbound-opportunity`, `request-founder-materials`, `prepare-initial-call`, `run-ten-factor-screen`, `summarize-initial-call`.
3. Follow-up and diligence: `run-follow-up-evaluation`, `generate-82-factor-questions`, `run-founder-evaluation`, commercial/technical/financial DD.
4. Review and IC: team review, partner review, IC memo, IC agenda, IC memo review, IC decision.
5. Closing and onboarding: term sheet, closing checklist, conditions precedent, portfolio onboarding.

## Detailed Audit: Admin And Pipeline Boundary

This bucket clarifies what belongs inside a single VC Deal Room versus what belongs to broader pipeline or workspace operations. The main decision is that a Deal Room should represent one opportunity. Pipeline-wide packets and agendas may still be useful pack tasks, but they should not force single-deal project schema fields.

### `create-deal-room`

Current stage: `screening`

Recommended stage/bucket: `intake` plus project/admin bucket

Assessment: keep, but reshape as a setup/reference task. It should not be a command-center artifact producer for the investment workflow, and it should not create folders or mutate external systems without approval. If it produces substantial setup guidance, that should be a setup-plan artifact, not many small structured outputs.

| Field | Current Section | Classification | Recommendation |
| --- | --- | --- | --- |
| `company_name` | input | Project input | Keep as durable identity field. |
| `crm_record_url` | input | Project input | Keep as source reference field, ideally paired with provider and source object ID. |
| `crm_provider` | input | Project input | Keep, but consider generic `source_system`/`crm_provider` consistency. |
| `source_artifacts` | input | Artifact input | Replace JSON with explicit source artifact IDs or uploaded-source references. |
| `desired_folder_root` | input | Task-local input | Keep task-local; do not promote to project schema unless workspace setup requires it. |
| `deal_room_url` | context | Project input if needed | Move to optional input when an existing deal room link is relevant. Do not pass as broad context. |
| `prior_task_outputs` | context | Bad shape | Remove. |
| `open_questions` | context | Context only | Do not prefill from project. Runtime Q&A belongs in task context. |
| `deal_room_fields` | output | Task-local or artifact content | Fold into setup-plan artifact or remove. |
| `artifact_checklist` | output | Artifact content | Fold into setup-plan artifact. |
| `source_index` | output | Artifact content | Fold into setup-plan artifact or source-material artifact index. |
| `drive_folder_plan` | output | Artifact content | Fold into setup-plan artifact; external folder changes require approval. |
| `manual_deal_room_link` | output | Project state output | May update `deal_room_url` after review/approval. |
| `next_stage_task_recommendations` | output | Task-local output | Keep on task or in setup artifact; do not map to project data. |
| generic outputs such as `summary`, `recommendation`, `source_links`, `assumptions`, `evidence_quality`, `risks`, `human_decision_points`, `next_actions` | output | Artifact content or task-local output | Remove as separately mapped project outputs. |

Recommended template changes:

- Move `definitionJson.stage` to `intake` when the new stage model lands.
- Remove `context` fields.
- Replace `source_artifacts` JSON with explicit source artifact/reference input naming.
- Consider adding `deal_room_setup_plan_artifact_id` as an optional or required file output if setup guidance remains substantial.
- Keep only `manual_deal_room_link` as a possible project update, and only with human approval.

### `source-thesis-targets`

Current stage: `lead_gen`

Recommended stage/bucket: `intake` when thesis-led, otherwise pipeline-level sourcing

Assessment: good artifact task, but it is not always a single-deal task. If it is used inside a Deal Room, it should represent the source thesis that produced or contextualizes the opportunity. The output should be one artifact, not duplicated structured project fields.

| Field | Current Section | Classification | Recommendation |
| --- | --- | --- | --- |
| `thesis_area` | input | Project input or task-local input | Keep as project field only for thesis-led/opportunity-created-from-thesis deals. |
| `geography` | input | Project input | Keep as durable deal/fund context. |
| `stage_focus` | input | Project input | Keep if it helps sourcing and screening. |
| `market_filters` | input | Task-local input | Keep task-local or artifact/source config; do not flatten into project schema yet. |
| `deal_room_url` | context | Project input if needed | Usually unnecessary for this task; remove context mapping. |
| `prior_task_outputs` | context | Bad shape | Remove. |
| `source_artifacts` | context | Artifact input | Move to explicit input only if the sourcing task needs uploaded source material. |
| `open_questions` | context | Context only | Do not prefill. |
| `thesis_target_list_artifact_id` | output | Artifact output | Keep and map to project artifact index when used in a Deal Room. |
| `target_company_list`, `fit_rationale`, `source_links`, `warm_intro_paths`, `confidence_notes` | output | Artifact content | Fold into the thesis target list artifact. |
| generic outputs | output | Artifact content or task-local output | Remove as separate mapped outputs. |

Recommended template changes:

- Keep `thesis_target_list_artifact_id` as the required file output.
- Remove context fields.
- Remove low-level output fields once the artifact contract is trusted.
- Do not auto-create this task for every Deal Room; it should be available when the opportunity is thesis-led or when the user asks for sourcing expansion.

### `prepare-lead-gen-packet`

Current stage: `lead_gen`

Recommended stage/bucket: pipeline-level task, not default single Deal Room stage task

Assessment: useful pack task, but likely mismatched to a single Deal Room project. `candidate_companies` and a lead-generation meeting packet describe a pipeline or meeting surface containing multiple opportunities. If retained in the Deal Room, it should be optional/manual and artifact-only.

| Field | Current Section | Classification | Recommendation |
| --- | --- | --- | --- |
| `candidate_companies` | input | Task-local or pipeline-project input | Do not add to single Deal Room project schema. |
| `meeting_date` | input | Task-local input | Do not make it a deal field unless tied to a specific deal meeting. |
| `thesis_context` | input | Task-local or project input | Use thesis/project context only when relevant. |
| `deal_room_url` | context | Bad fit | Remove for pipeline packet. |
| `prior_task_outputs` | context | Bad shape | Remove. |
| `source_artifacts` | context | Artifact input if needed | Move to explicit input if needed. |
| `open_questions` | context | Context only | Do not prefill. |
| `lead_generation_packet_artifact_id` | output | Artifact output | Keep if this task remains in pack. It may belong to a pipeline project type later. |
| `lead_gen_packet`, `per_company_snapshots`, `discussion_points`, `proposed_next_actions` | output | Artifact content | Fold into artifact. |
| generic outputs | output | Artifact content or task-local output | Remove as separately mapped outputs. |

Recommended template changes:

- Keep task in the VC pack, but do not make it a default VC Deal Room mapped task.
- Consider removing `supportedProjectTypes: [vc_deal_room]` later if a pipeline project type is introduced.
- Keep artifact output but avoid project-level mapping unless there is a specific Deal Room use case.

### `prepare-deal-flow-agenda`

Current stage: `deal_flow`

Recommended stage/bucket: pipeline-level task, not single Deal Room

Assessment: useful for fund operating cadence, but not a single opportunity Deal Room task. It should not drive the Deal Room schema. If the platform later has a VC Pipeline project type, this belongs there.

| Field | Current Section | Classification | Recommendation |
| --- | --- | --- | --- |
| `pipeline_snapshot` | input | Pipeline-project input | Do not add to single Deal Room project schema. |
| `meeting_date` | input | Task-local or pipeline-project input | Not a deal field by default. |
| `stale_deal_threshold` | input | Task-local input | Keep task-local. |
| `deal_room_url` | context | Bad fit | Remove. |
| `prior_task_outputs` | context | Bad shape | Remove. |
| `source_artifacts` | context | Artifact input if needed | Move to explicit input only if needed. |
| `open_questions` | context | Context only | Do not prefill. |
| `agenda`, `stale_deal_list`, `new_deal_list`, `stage_change_candidates`, `seven_day_action_plan` | output | Artifact content | If retained, add a `deal_flow_agenda_artifact_id` file output and fold these into it. |
| generic outputs | output | Artifact content or task-local output | Remove as separately mapped outputs. |

Recommended template changes:

- Move out of default VC Deal Room mappings.
- Consider adding a file output if this remains a first-class pack task.
- Revisit once there is a VC Pipeline project type or workspace-level operating cadence surface.

### First-Bucket Decisions

Adopt these changes before rebuilding the project schema:

1. `create-deal-room` stays in VC Deal Room, but as `intake`/admin setup with minimal project updates.
2. `source-thesis-targets` can stay as optional Deal Room assessment work, with artifact-only output mapping. It is also reusable for a future Origination project type.
3. `prepare-lead-gen-packet` and `prepare-deal-flow-agenda` should not be default mapped Deal Room tasks.
4. The project schema should not include `candidate_companies`, `pipeline_snapshot`, or `prior_task_outputs`.
5. Broad context mappings should be removed from these four tasks.

## Detailed Audit: Assessment

Assessment is the first real Deal Room investment stage. Its job is to determine whether the opportunity merits diligence. It should consume compact deal identity/source data and uploaded artifacts, then produce reviewable artifacts: first-look scorecards, initial-call briefs, ten-factor scorecards, call summaries, founder-material request drafts, and possibly thesis-target context.

Assessment should not turn every screening observation into project fields. The project should hold the company identity, source references, uploaded deck/material artifacts, meeting/transcript artifacts, current assessment state, and links to assessment artifacts. Recommendations, red flags, unknowns, claims registers, questions, and rationale should mostly live in those artifacts.

### `source-thesis-targets`

Current stage: `lead_gen`

Recommended stage/bucket: optional `assessment` task in Deal Room; also reusable in future Origination project type

Assessment: keep available in Deal Room, but as optional thesis context. The same task can be useful upstream in an Origination project and downstream in a Deal Room when the analyst wants to assess whether the opportunity fits a thesis or identify adjacent companies.

| Field | Current Section | Classification | Recommendation |
| --- | --- | --- | --- |
| `thesis_area` | input | Project input or task-local input | Use project field when assessment is thesis-led; otherwise task-local. |
| `geography` | input | Project input | Keep as durable context. |
| `stage_focus` | input | Project input or task-local input | Useful assessment filter, not mandatory. |
| `market_filters` | input | Task-local input | Do not promote to flat project field yet. |
| `source_artifacts` | context | Artifact input | Move to explicit optional input if needed. |
| `prior_task_outputs` | context | Bad shape | Remove. |
| `open_questions` | context | Context only | Runtime Q&A only; do not prefill. |
| `thesis_target_list_artifact_id` | output | Artifact output | Keep and map if produced inside Deal Room. |
| low-level sourcing outputs | output | Artifact content | Fold into artifact. |

Recommended template changes:

- Move stage to `assessment` when the new stage model lands.
- Remove context fields.
- Keep required file output.
- Keep task optional/manual in Deal Room; do not auto-trigger for every assessment.

### `screen-inbound-opportunity`

Current stage: `screening`

Recommended stage/bucket: `assessment`

Assessment: core Deal Room task. This is the primary first-look artifact and should be one of the main assessment actions. It should consume the company identity, source thread, referrer/source references, fund thesis context, and uploaded deck/material artifacts.

| Field | Current Section | Classification | Recommendation |
| --- | --- | --- | --- |
| `company_name` | input | Project input | Keep. |
| `source_thread_url` | input | Project input/source reference | Keep as source reference, though a source message/thread artifact would be better long term. |
| `pitch_deck_url` | input | Bad shape | Replace with optional `pitch_deck_artifact_id`. |
| `referrer` | input | Project input | Keep if known. |
| `fund_thesis_context` | input | Project input or artifact input | Keep compact context or use thesis/source artifact. |
| `deal_room_url` | context | Project input if needed | Move to optional input only if task needs it. |
| `prior_task_outputs` | context | Bad shape | Remove. |
| `source_artifacts` | context | Artifact input | Move to explicit input. |
| `open_questions` | context | Context only | Runtime Q&A only. |
| `first_look_scorecard_artifact_id` | output | Artifact output | Keep as primary output. |
| `fit_recommendation`, `initial_ten_factor_summary`, `missing_information`, `red_flags`, `pass_feedback_draft`, `next_actions` | output | Artifact content | Fold into scorecard artifact. Only reviewed assessment state should update project data. |
| generic outputs | output | Artifact content or task-local output | Remove as separate mapped project outputs. |

Recommended template changes:

- Replace `pitch_deck_url` with `pitch_deck_artifact_id`.
- Remove context fields.
- Consider whether `source_thread_url` should eventually become `source_thread_artifact_id`.
- Keep only `first_look_scorecard_artifact_id` as required output.

### `request-founder-materials`

Current stage: `screening`

Recommended stage/bucket: `assessment`, optional/founder-facing approval task

Assessment: useful Deal Room task, but it is an external-draft task. It should create a reviewable artifact containing the missing-materials checklist and draft request. Sending remains explicitly human-approved.

| Field | Current Section | Classification | Recommendation |
| --- | --- | --- | --- |
| `company_name` | input | Project input | Keep. |
| `missing_materials` | input | Project input or task-local input | Can be project-level if tracked as active assessment gap; otherwise task-local. |
| `founder_contact` | input | Project input | Keep if known. |
| `due_date` | input | Project/task input | May be project field only if actively tracked. |
| context fields | context | Context/bad shape | Remove broad context fields. Runtime Q&A stays task context. |
| `founder_materials_request_artifact_id` | output | Artifact output | Keep as primary output. |
| `materials_request_checklist`, `draft_external_message`, `share_instructions`, `due_date_recommendation`, `approval_required` | output | Artifact content plus possible approval state | Fold into artifact; only approval state/due date should become project fields if needed. |
| generic outputs | output | Artifact content or task-local output | Remove as separate mapped project outputs. |

Recommended template changes:

- Remove context fields.
- Keep file output.
- Keep as manually triggered/approval-gated, not automatic assessment output.

### `prepare-initial-call`

Current stage: `initial_call`

Recommended stage/bucket: `assessment`

Assessment: core assessment task. It should produce a pre-call brief artifact from company identity, uploaded deck/source artifacts, founder info, meeting metadata, and known assessment artifacts.

| Field | Current Section | Classification | Recommendation |
| --- | --- | --- | --- |
| `company_name` | input | Project input | Keep. |
| `pitch_deck_url` | input | Bad shape | Replace with required `pitch_deck_artifact_id`. |
| `founder_names` | input | Project input | Keep if known. |
| `meeting_datetime` | input | Project/task input | Keep as task input, project field only if active meeting is tracked. |
| `deal_room_url` | input | Optional project input | Keep optional if useful. |
| `prior_task_outputs` | context | Bad shape | Remove; use explicit artifacts such as first-look scorecard and thesis target list if needed. |
| `source_artifacts` | context | Artifact input | Move to explicit input. |
| `open_questions` | context | Context only | Runtime Q&A only. |
| `initial_call_brief_artifact_id` | output | Artifact output | Keep as primary output. |
| `pre_call_brief`, `founder_company_summary`, `competitor_funding_activity`, `starter_ten_factor_scorecard`, `questions_by_topic` | output | Artifact content | Fold into initial call brief artifact. |
| generic outputs | output | Artifact content or task-local output | Remove as separate mapped project outputs. |

Recommended template changes:

- Replace `pitch_deck_url` with `pitch_deck_artifact_id`.
- Add optional explicit artifact inputs such as `first_look_scorecard_artifact_id` and `thesis_target_list_artifact_id` if the task should build on them.
- Remove context fields.
- Keep only `initial_call_brief_artifact_id` as required output.

### `run-ten-factor-screen`

Current stage: `initial_call`

Recommended stage/bucket: `assessment`

Assessment: core assessment task when the workspace uses a ten-factor methodology. It should create the ten-factor scorecard artifact and avoid duplicating scores/rationale into project fields.

| Field | Current Section | Classification | Recommendation |
| --- | --- | --- | --- |
| `company_name` | input | Project input | Keep. |
| `pitch_deck_url` | input | Bad shape | Replace with required `pitch_deck_artifact_id`. |
| `meeting_notes` | input | Artifact input or task-local input | Prefer uploaded meeting notes/transcript artifact where available. |
| `source_links` | input | Artifact/source input | Prefer source artifacts or references. |
| context fields | context | Context/bad shape | Remove broad context fields. |
| `ten_factor_scorecard_artifact_id` | output | Artifact output | Keep as primary output. |
| `factor_scores`, `overall_recommendation`, `source_links`, `unknowns`, `human_review_prompts` | output | Artifact content | Fold into scorecard artifact; reviewed recommendation may update assessment state separately. |
| generic outputs | output | Artifact content or task-local output | Remove as separate mapped project outputs. |

Recommended template changes:

- Replace `pitch_deck_url` with `pitch_deck_artifact_id`.
- Consider optional `initial_call_brief_artifact_id` or `customer_insights_artifact_id` input if run after call.
- Remove context fields.
- Keep only `ten_factor_scorecard_artifact_id` as required output.

### `summarize-initial-call`

Current stage: `initial_call`

Recommended stage/bucket: `assessment`

Assessment: core assessment task after an initial call. It should consume a transcript artifact/reference and produce a customer insights summary artifact. A raw transcript URL is less ideal than an uploaded transcript/notes artifact.

| Field | Current Section | Classification | Recommendation |
| --- | --- | --- | --- |
| `meeting_transcript_url` | input | Bad shape or source reference | Prefer `meeting_transcript_artifact_id`; keep URL only as optional source reference. |
| `meeting_notes` | input | Artifact input or task-local input | Prefer uploaded notes artifact or task-local notes. |
| `company_name` | input | Project input | Keep. |
| `deal_room_url` | input | Optional project input | Should not be required unless a real dependency exists. |
| `prior_task_outputs` | context | Bad shape | Remove. |
| `source_artifacts` | context | Artifact input | Move to explicit input if needed. |
| `open_questions` | context | Context only | Runtime Q&A only. |
| `customer_insights_artifact_id` | output | Artifact output | Keep as primary output. |
| `transcript_summary`, `claims_register`, `contradictions_or_gaps`, `action_items`, `draft_crm_update`, `pass_follow_up_recommendation` | output | Artifact content | Fold into customer insights artifact. CRM update remains draft-only and approval-gated. |
| generic outputs | output | Artifact content or task-local output | Remove as separate mapped project outputs. |

Recommended template changes:

- Replace required `meeting_transcript_url` with required `meeting_transcript_artifact_id` where possible.
- Make `deal_room_url` optional unless there is a hard runtime dependency.
- Remove context fields.
- Keep only `customer_insights_artifact_id` as required output.

### `evaluate-investment-opportunity`

Current stage: `deal_flow`

Recommended stage/bucket: assessment control/review helper, not default artifact producer

Assessment: this task is an orchestration/recommendation task rather than a stage artifact producer. It can be useful as a manual review helper that summarizes current state and suggests next tasks, but it should not be the way task outputs are routed through the project.

| Field | Current Section | Classification | Recommendation |
| --- | --- | --- | --- |
| `company_name` | input | Project input | Keep. |
| `current_stage` | input | Project state input | Keep, but align with collapsed stage model. |
| `deal_room_url` | input | Optional project input | Keep optional if needed. |
| `prior_task_outputs` | input | Bad shape | Replace with explicit artifact IDs or remove. |
| context fields | context | Context/bad shape | Remove broad context fields. |
| `stage_summary`, `missing_inputs`, `stage_transition_recommendation`, `next_stage_task_suggestions` | output | Task-local or project state output after review | Keep task-local by default; only reviewed transition/status should update project state. |
| generic outputs | output | Artifact content or task-local output | Remove as separate mapped project outputs. |

Recommended template changes:

- Keep as manual/review helper, not automatic stage trigger.
- Remove `prior_task_outputs`.
- Consider whether this task should produce an artifact such as `assessment_recommendation_artifact_id`; otherwise keep outputs task-local.

### Assessment Decisions

Adopt these changes before rebuilding the project schema:

1. Assessment is the right Deal Room home for first-look, thesis context, initial call, ten-factor screen, call summary, founder material request, and manual investment-opportunity evaluation.
2. `source-thesis-targets` remains available in Deal Room assessment, but optional and reusable with future Origination.
3. `pitch_deck_url` should become `pitch_deck_artifact_id` in assessment tasks.
4. Transcript/meeting source URLs should move toward artifact IDs, especially `meeting_transcript_artifact_id`.
5. Assessment project data should keep identity/source/material references and artifact IDs, not duplicate scorecard details, claims registers, action lists, red flags, or next actions.
6. No assessment task should rely on `prior_task_outputs`.
7. Broad context fields should be removed; task-local ask-question history remains context.

## Detailed Audit: Follow-Up And Diligence

Diligence is where the artifact-first model matters most. The project should not carry a flattened copy of commercial, technical, financial, founder, or 82-factor analysis. It should carry the deal identity, the source/evidence artifacts required to run the workstream, and the resulting diligence artifact IDs.

The current templates often use string/json fields such as `financial_statements`, `architecture_docs`, `customer_or_user_evidence`, and `bank_statement_evidence`. These are really source material references. Where the platform can support it, they should become file/artifact inputs or lists of evidence artifact IDs.

### `run-follow-up-evaluation`

Current stage: `follow_up`

Recommended stage/bucket: optional assessment bridge or remove/merge into diligence planning

Assessment: this task looks like a pre-artifact-era bridge between assessment and diligence. It returns a workspace, request list, competitive landscape, early risks, and readiness recommendation, but has no primary file output. It may be better as a `diligence_plan_artifact_id` task or absorbed into `generate-82-factor-questions`, `request-founder-materials`, and the workstream tasks.

| Field | Current Section | Classification | Recommendation |
| --- | --- | --- | --- |
| `company_name` | input | Project input | Keep if task remains. |
| `deal_room_url` | input | Optional project input | Should not be required unless there is a hard dependency. |
| `prior_task_outputs` | input | Bad shape | Remove; use explicit assessment artifact IDs. |
| `founder_documents` | input | Artifact input | Replace text with source/founder material artifact IDs. |
| context fields | context | Context/bad shape | Remove broad context fields. |
| all current outputs | output | Artifact content or task-local output | Add a primary artifact output such as `follow_up_evaluation_artifact_id` or remove/merge this task. |

Recommended template changes:

- Decide whether this task is still needed.
- If kept, add a required file output and make the detailed outputs artifact content.
- Replace `prior_task_outputs` with named inputs like `first_look_scorecard_artifact_id`, `customer_insights_artifact_id`, and `ten_factor_scorecard_artifact_id`.

### `generate-82-factor-questions`

Current stage: `follow_up`

Recommended stage/bucket: `diligence`, often before or during workstream planning

Assessment: strong artifact task. It should produce the question set artifact from known claims and existing evidence. The weak point is `known_claims` as free text; this should often be derived from assessment artifacts.

| Field | Current Section | Classification | Recommendation |
| --- | --- | --- | --- |
| `company_name` | input | Project input | Keep. |
| `known_claims` | input | Artifact-derived input | Prefer explicit artifact inputs such as `customer_insights_artifact_id`, `first_look_scorecard_artifact_id`, or uploaded founder materials. |
| `existing_answers` | input | Artifact input or task-local input | Prefer evidence/question artifact reference. |
| `priority_workstreams` | input | Project/task input | Keep as task-local or compact diligence plan field. |
| context fields | context | Context/bad shape | Remove broad context fields. |
| `eighty_two_factor_questions_artifact_id` | output | Artifact output | Keep as primary output. |
| `question_set`, `rationale`, `source_gap`, `owner`, `urgency` | output | Artifact content | Fold into the question-set artifact. |
| generic outputs | output | Artifact content or task-local output | Remove as separate mapped project outputs. |

Recommended template changes:

- Move stage to `diligence` in the collapsed stage model.
- Replace broad/derived free-text inputs with explicit assessment/evidence artifact inputs where possible.
- Keep only `eighty_two_factor_questions_artifact_id` as required output.

### `run-founder-evaluation`

Current stage: `founder_evaluation`

Recommended stage/bucket: `diligence`

Assessment: strong artifact task. Founder names and profile links can be durable deal data, but reference material, cap table, and prior assessment work should be explicit source/artifact inputs.

| Field | Current Section | Classification | Recommendation |
| --- | --- | --- | --- |
| `founder_names` | input | Project input | Keep. |
| `linkedin_profiles` | input | Project input/source refs | Keep as source references, but consider richer founder identity refs later. |
| `reference_inputs` | input | Artifact input or task-local input | Prefer reference source artifacts. |
| `prior_task_outputs` | input | Bad shape | Remove; use explicit assessment/diligence artifact inputs. |
| `cap_table_or_equity_split` | input | Artifact input | Prefer cap table artifact/source material reference. |
| context fields | context | Context/bad shape | Remove broad context fields. |
| `founder_evaluation_artifact_id` | output | Artifact output | Keep as primary output. |
| founder dossier/risk/reference/stop-signal outputs | output | Artifact content | Fold into founder evaluation artifact. |
| generic outputs | output | Artifact content or task-local output | Remove as separate mapped project outputs. |

Recommended template changes:

- Move stage to `diligence`.
- Replace `prior_task_outputs`.
- Consider optional artifact inputs from `customer_insights_artifact_id` and `eighty_two_factor_questions_artifact_id`.
- Keep only `founder_evaluation_artifact_id` as required output.

### `run-commercial-dd`

Current stage: `commercial_dd`

Recommended stage/bucket: `diligence`

Assessment: strong diligence workstream. Three file outputs are reasonable if the product wants separate commercial report, market analysis, and customer reference summary surfaces. Inputs should become evidence artifact references rather than freeform JSON/text where possible.

| Field | Current Section | Classification | Recommendation |
| --- | --- | --- | --- |
| `company_name` | input | Project input | Keep. |
| `business_model` | input | Project input or artifact-derived input | Keep compact project field only if commonly known early; otherwise derive from artifacts. |
| `customer_or_user_evidence` | input | Artifact input | Replace JSON with evidence artifact IDs. |
| `go_to_market_evidence` | input | Artifact input | Replace text with evidence/source artifact refs. |
| `pricing_or_revenue_evidence` | input | Artifact input | Replace text with evidence/source artifact refs. |
| `market_sources` | input | Artifact input | Replace JSON with market source artifact refs. |
| context fields | context | Context/bad shape | Remove broad context fields. |
| `commercial_dd_artifact_id`, `market_analysis_artifact_id`, `customer_reference_summary_artifact_id` | output | Artifact outputs | Keep. |
| all detailed commercial outputs | output | Artifact content | Fold into one or more commercial artifacts. |
| generic outputs | output | Artifact content or task-local output | Remove as separate mapped project outputs. |

Recommended template changes:

- Move stage to `diligence`.
- Replace source/evidence fields with artifact reference inputs.
- Keep the three file outputs if the command view wants separate cards.

### `run-technical-dd`

Current stage: `technical_dd`

Recommended stage/bucket: `diligence`

Assessment: strong diligence workstream. Current required inputs are strings for architecture docs and repo/code access; these should be source artifact/reference inputs. Sensitive repo/code access must remain permission/approval-bound.

| Field | Current Section | Classification | Recommendation |
| --- | --- | --- | --- |
| `architecture_docs` | input | Artifact input | Replace with `architecture_docs_artifact_ids` or source artifact refs. |
| `repo_or_code_access` | input | Source/access reference | Keep explicit and permission-bound; may not be a file artifact. |
| `product_roadmap`, `ip_patent_materials`, `engineering_team_materials` | input | Artifact inputs | Prefer uploaded artifacts/source references. |
| context fields | context | Context/bad shape | Remove broad context fields. |
| `technical_dd_artifact_id` | output | Artifact output | Keep. |
| detailed technical outputs | output | Artifact content | Fold into technical DD artifact. |
| generic outputs | output | Artifact content or task-local output | Remove as separate mapped project outputs. |

Recommended template changes:

- Move stage to `diligence`.
- Make source/access inputs explicit and safer.
- Keep only `technical_dd_artifact_id` as required output.

### `run-financial-dd`

Current stage: `financial_dd`

Recommended stage/bucket: `diligence`

Assessment: strong diligence workstream. Financial materials should be artifact inputs, not strings/json. The two file outputs are reasonable if unit economics is shown separately.

| Field | Current Section | Classification | Recommendation |
| --- | --- | --- | --- |
| `financial_statements` | input | Artifact input | Replace with financial statement artifact IDs. |
| `business_model` | input | Project input or artifact-derived input | Same as commercial DD; avoid duplicating if already captured. |
| `forecast_model` | input | Artifact input | Replace with forecast model artifact ID. |
| `cap_table` | input | Artifact input | Replace with cap table artifact ID. |
| `bank_statement_evidence` | input | Artifact input | Replace JSON with evidence artifact IDs. |
| `use_of_funds_plan` | input | Artifact input | Prefer uploaded/source artifact. |
| context fields | context | Context/bad shape | Remove broad context fields. |
| `financial_dd_artifact_id`, `unit_economics_artifact_id` | output | Artifact outputs | Keep. |
| detailed financial outputs | output | Artifact content | Fold into financial artifacts. |
| generic outputs | output | Artifact content or task-local output | Remove as separate mapped project outputs. |

Recommended template changes:

- Move stage to `diligence`.
- Replace financial source fields with artifact references.
- Keep the two file outputs if the command view wants separate cards.

### Diligence Decisions

Adopt these changes before rebuilding the project schema:

1. Diligence should be one project stage, not separate lifecycle stages for commercial, technical, financial, and founder workstreams.
2. Workstreams can still be separate tasks and can be independently available/triggered inside the `diligence` stage.
3. Diligence source material should be explicit artifacts/references, not broad JSON/text fields.
4. `run-follow-up-evaluation` should either become a file-output diligence-planning task or be removed/merged.
5. Project data should store diligence artifact IDs, not workstream findings.
6. Do not map detailed risk lists, scorecards, summaries, evidence quality, assumptions, or next actions back to project fields by default.
7. Question/answer interaction during diligence remains task context; final question sets and diligence reports are artifacts.

## Detailed Audit: Review And IC

The `review` stage should convert diligence artifacts into decision materials and a recorded investment decision. This is where artifact inputs are clearest: the tasks should consume review packs, diligence reports, memos, agendas, and IC notes as named artifact inputs. The project should store resulting artifact IDs and a small number of reviewed state fields such as decision outcome, decision ask, approval state, next stage, and active conditions.

Team review, partner review, IC memo, agenda, memo review, and IC decision can all live in the collapsed `review` stage. They do not need separate lifecycle states such as `team_review`, `partner_review`, and `investment_committee`.

### `prepare-team-review-pack`

Current stage: `team_review`

Recommended stage/bucket: `review`

Assessment: strong artifact task, but the input shape still mixes explicit artifact inputs with summary blobs. The file artifact inputs are good. Required `prior_task_outputs` and required `ten_factor_summary` should be replaced with explicit assessment artifacts, especially the ten-factor scorecard and customer insights summary.

| Field | Current Section | Classification | Recommendation |
| --- | --- | --- | --- |
| DD artifact IDs | input | Artifact inputs | Keep required commercial, financial, founder, technical, and 82-factor inputs. |
| `prior_task_outputs` | input | Bad shape | Remove. |
| `ten_factor_summary` | input | Artifact-derived input | Replace with `ten_factor_scorecard_artifact_id`. |
| `eighty_two_factor_summary` | input | Artifact-derived input | Replace with `eighty_two_factor_questions_artifact_id`, already present. |
| `founder_risk_assessment` | input | Artifact-derived input | Prefer founder evaluation artifact rather than separate string. |
| context fields | context | Context/bad shape | Remove broad context fields. |
| `team_review_pack_artifact_id` | output | Artifact output | Keep. |
| all detailed review outputs | output | Artifact content | Fold into team review pack artifact. |

Recommended template changes:

- Move stage to `review`.
- Add/require `ten_factor_scorecard_artifact_id` and possibly `customer_insights_artifact_id`.
- Remove `prior_task_outputs`, summary text inputs, and broad context.
- Keep only `team_review_pack_artifact_id` as required output.

### `prepare-partner-review-pack`

Current stage: `partner_review`

Recommended stage/bucket: `review`

Assessment: strong artifact task. It should escalate a team review pack plus supporting diligence artifacts. It currently duplicates the team review pack as both file artifact and JSON, and requires `open_questions` as an input. That should be cleaned up.

| Field | Current Section | Classification | Recommendation |
| --- | --- | --- | --- |
| `team_review_pack_artifact_id` | input | Artifact input | Keep. |
| DD artifact IDs | input | Artifact inputs | Keep if partner review needs direct access; otherwise team review pack may be enough. |
| `team_review_pack` | input | Bad duplication | Remove JSON duplicate. |
| `open_questions` | input | Context or artifact content | Do not require as project input; include unresolved questions in team review pack or runtime Q&A. |
| `proposed_dd_scope` | input | Task-local/project state input | Optional; may be task-local or reviewed planning state. |
| context fields | context | Context/bad shape | Remove. |
| `partner_review_pack_artifact_id` | output | Artifact output | Keep. |
| investment thesis/fit/scope/owners/risks/decision ask | output | Artifact content; maybe project state for `decision_ask` | Fold into artifact, with only reviewed `decision_ask` optionally promoted. |

Recommended template changes:

- Move stage to `review`.
- Remove `team_review_pack` JSON and required `open_questions`.
- Keep artifact output and explicit artifact inputs.

### `create-ic-memo`

Current stage: `investment_committee`

Recommended stage/bucket: `review`

Assessment: strong artifact task. The current template is already largely artifact-driven, but it still requires `stage_outputs` and `dd_summaries`, and it accepts summary/risk/source strings that should come from artifacts.

| Field | Current Section | Classification | Recommendation |
| --- | --- | --- | --- |
| `team_review_pack_artifact_id`, `partner_review_pack_artifact_id` | input | Artifact inputs | Keep required. |
| DD artifact IDs | input | Artifact inputs | Keep if memo assembly needs direct source access. |
| `stage_outputs` | input | Bad shape | Remove; use explicit artifact IDs. |
| `dd_summaries` | input | Artifact-derived input | Remove or make task-local override; summaries live in DD artifacts. |
| `founder_risk_assessment` | input | Artifact-derived input | Prefer founder evaluation artifact. |
| `term_sheet_inputs` | input | Task-local or future term-sheet source | Likely not needed before IC memo unless term-sheet context exists. |
| `source_artifacts` | input | Artifact input | Keep only as explicit optional artifact refs if needed. |
| context fields | context | Context/bad shape | Remove. |
| `investment_memo_artifact_id` | output | Artifact output | Keep. |
| `decision_ask` | output | Project state output after review | May be promoted compactly; memo remains artifact. |
| memo/checklist/risks/citation outputs | output | Artifact content | Fold into investment memo artifact. |

Recommended template changes:

- Move stage to `review`.
- Remove `stage_outputs`, `dd_summaries`, and broad context.
- Keep investment memo artifact as primary output.
- Optionally expose reviewed `decision_ask` as compact project state.

### `prepare-ic-agenda`

Current stage: `investment_committee`

Recommended stage/bucket: `review`

Assessment: useful artifact task. It should consume the investment memo and meeting details. `ic_pack` JSON is likely a duplicate/summary blob; the source should be the memo and review artifacts.

| Field | Current Section | Classification | Recommendation |
| --- | --- | --- | --- |
| `investment_memo_artifact_id` | input | Artifact input | Keep required. |
| `ic_pack` | input | Bad shape | Replace with explicit artifact inputs or remove. |
| `decision_ask` | input | Project state/task input | Keep if already reviewed from IC memo/partner review. |
| `open_questions` | input | Context or artifact content | Do not require; unresolved questions should be in memo/review artifacts or task Q&A. |
| `attendees`, `meeting_datetime` | input | Task/project input | Keep optional. |
| context fields | context | Context/bad shape | Remove. |
| `ic_agenda_artifact_id` | output | Artifact output | Keep. |
| agenda/checklist/topics/questions/pre-read outputs | output | Artifact content | Fold into agenda artifact. |

Recommended template changes:

- Move stage to `review`.
- Remove `ic_pack` JSON and broad context.
- Keep IC agenda artifact output.

### `review-ic-memo`

Current stage: `investment_committee`

Recommended stage/bucket: `review`

Assessment: strong review artifact task, and PR #11 already correctly requires both `investment_memo_artifact_id` and `ic_agenda_artifact_id`. The remaining issue is duplicate required `ic_memo` richtext and `ic_pack` JSON. The task should review artifacts, not pasted copies.

| Field | Current Section | Classification | Recommendation |
| --- | --- | --- | --- |
| `investment_memo_artifact_id`, `ic_agenda_artifact_id` | input | Artifact inputs | Keep required. |
| `ic_memo` | input | Bad duplication | Remove required richtext duplicate. |
| `ic_pack` | input | Bad duplication | Remove JSON duplicate. |
| `source_artifacts` | input | Artifact input | Optional only if additional review sources are needed. |
| `review_focus` | input | Task-local input | Keep optional. |
| context fields | context | Context/bad shape | Remove. |
| `ic_memo_review_artifact_id` | output | Artifact output | Keep. |
| findings/gaps/readiness/changes outputs | output | Artifact content; maybe compact project state for readiness | Fold into review artifact, with optional reviewed readiness state. |

Recommended template changes:

- Keep the two required artifact inputs.
- Remove `ic_memo` and `ic_pack`.
- Keep review artifact output.

### `record-ic-decision`

Current stage: `investment_committee`

Recommended stage/bucket: `review`

Assessment: strong artifact task with the clearest project-state outputs. It should record the formal decision. This task is where a small number of outputs can update project state after human review.

| Field | Current Section | Classification | Recommendation |
| --- | --- | --- | --- |
| `investment_memo_artifact_id`, `ic_agenda_artifact_id` | input | Artifact inputs | Keep required. |
| `ic_transcript_or_notes` | input | Artifact input or task-local input | Prefer transcript/notes artifact ID; richtext is acceptable as manual fallback. |
| `decision_options` | input | Project/task input | Keep; align with allowed decision enum. |
| `conditions_discussed`, `attendees` | input | Task-local/project input | Keep optional; conditions may become artifact content/project state after approval. |
| context fields | context | Context/bad shape | Remove. |
| `ic_decision_record_artifact_id` | output | Artifact output | Keep. |
| `decision_outcome` | output | Project state output | Promote after review. |
| `stage_transition_recommendation` | output | Project state output after approval | Promote only after explicit approval. |
| `conditions` | output | Project state output or artifact content | Keep in artifact; optionally compact project state if conditions drive closing. |
| vote/objections/action outputs | output | Artifact content | Fold into IC decision record artifact. |

Recommended template changes:

- Move stage to `review`.
- Prefer transcript/notes artifact input.
- Keep IC decision artifact output.
- Allow reviewed decision outcome/stage transition/conditions to update project state.

### Review And IC Decisions

Adopt these changes before rebuilding the project schema:

1. Team review, partner review, IC memo, IC agenda, memo review, and IC decision all belong in the collapsed `review` stage.
2. Explicit artifact inputs should replace `stage_outputs`, `dd_summaries`, `team_review_pack` JSON, `ic_pack` JSON, pasted `ic_memo`, and `prior_task_outputs`.
3. Required review artifacts should remain file inputs/outputs.
4. `review-ic-memo` should continue requiring both `investment_memo_artifact_id` and `ic_agenda_artifact_id`.
5. Only a few IC outputs should update project state: decision ask, decision outcome, approved stage transition, approval/readiness state, and maybe active conditions.
6. All detailed review findings, risks, gaps, checklists, objections, debate topics, and action items should live in artifacts.
7. Broad context fields should be removed from review/IC templates; runtime Q&A stays task context.

## Detailed Audit: Term Sheet, Closing, And Onboarding

The final Deal Room work should preserve a clear distinction between negotiated/legal source materials, review artifacts, and compact close-readiness state. Term sheet review, closing checklist management, CP verification, and portfolio handoff all have natural file outputs. Those file outputs should become project artifact references; most detailed term deviations, blockers, CP evidence mappings, owner tables, milestones, and onboarding plans should remain inside artifacts.

In the six-stage model, `term_sheet` remains its own stage because it is a distinct investment-control moment. Closing checklist, CP verification, signing readiness, and portfolio onboarding should all live in `closing`. Portfolio onboarding can become a separate lifecycle stage later if post-investment handoff needs its own experience, but it does not need to force the first schema/mapping slice beyond six stages.

### `review-term-sheet`

Current stage: `term_sheet`

Recommended stage/bucket: `term_sheet`

Assessment: strong artifact task. The output shape is right at the file level, but the inputs are not artifact-first yet. A term sheet should be uploaded or referenced as a platform artifact, not pasted into a string field. `deal_terms` may be useful as extracted metadata later, but it should not be the required source of truth while the artifact exists.

| Field | Current Section | Classification | Recommendation |
| --- | --- | --- | --- |
| `term_sheet` | input | Bad shape | Replace with `term_sheet_artifact_id` or explicit source file reference. |
| `deal_terms` | input | Artifact-derived or task-local input | Prefer extracted metadata from the term sheet artifact; keep task-local override only if needed. |
| `standard_terms_reference` | input | Artifact/source input or methodology config | Use a standard terms artifact/reference or pack methodology guidance, not project schema by default. |
| `counsel_notes` | input | Task-local or artifact input | Keep optional; prefer counsel notes artifact/ref if reused. |
| context fields | context | Context/bad shape | Remove broad context fields. Runtime Q&A stays task context. |
| `term_sheet_review_artifact_id` | output | Artifact output | Keep as primary output. |
| `recommendation`, `approval_required` | output | Project state output after review | May update compact approval state only after human review. |
| `term_summary`, `deviation_table`, `review_focus`, `review_notes`, `red_flags`, `counsel_review_questions` | output | Artifact content | Fold into term sheet review artifact. |
| output `deal_room_url` | output | Bad shape | Remove; tasks should not output the project URL. |
| generic outputs | output | Artifact content or task-local output | Remove as separate mapped project outputs. |

Recommended template changes:

- Keep stage as `term_sheet`.
- Replace required `term_sheet` string with required `term_sheet_artifact_id`.
- Remove required `deal_terms` unless there is a clear extracted-metadata workflow.
- Remove broad context fields and output `deal_room_url`.
- Keep only `term_sheet_review_artifact_id` as required artifact output, with optional compact reviewed approval state.

### `manage-closing-checklist`

Current stage: `signing`

Recommended stage/bucket: `closing`

Assessment: strong artifact task and a core closing action. It already consumes the IC decision record and term sheet review as file artifacts, which is the right direction. The weakness is that required `closing_workplan` and `legal_document_status` are string fields while owners, deadlines, and blockers are JSON fields. Those are usually checklist artifact content, not durable project schema fields.

| Field | Current Section | Classification | Recommendation |
| --- | --- | --- | --- |
| `ic_decision_record_artifact_id` | input | Artifact input | Keep required. |
| `term_sheet_review_artifact_id` | input | Artifact input | Keep required. |
| `closing_workplan` | input | Artifact input or task-local input | Prefer closing plan/source artifact; avoid required project field. |
| `legal_document_status` | input | Project state or artifact content | Keep only compact current status if useful; otherwise keep in closing checklist artifact. |
| `owners`, `deadlines`, `blockers` | input | Artifact content or task-local input | Do not promote broad JSON fields into project schema by default. |
| context fields | context | Context/bad shape | Remove broad context fields. |
| `closing_checklist_artifact_id` | output | Artifact output | Keep as primary output. |
| `closing_status` | output | Project state output after review | Good compact project field. |
| `onboarding_readiness` | output | Project state output after review | May be compact project state if it gates portfolio handoff. |
| `owner_due_date_table`, `blockers`, `daily_status_summary` | output | Artifact content | Fold into closing checklist artifact; optionally expose a compact blocker flag/status later. |
| generic outputs | output | Artifact content or task-local output | Remove as separate mapped project outputs. |

Recommended template changes:

- Move stage to `closing`.
- Keep required file inputs from IC decision and term sheet review.
- Replace `closing_workplan` with `closing_workplan_artifact_id` if the workplan is an external/source document, or make it task-local.
- Keep only `closing_checklist_artifact_id` as required artifact output.
- Promote only reviewed `closing_status`, `onboarding_readiness`, and possibly compact active blocker state.

### `verify-conditions-precedent`

Current stage: `final_dd`

Recommended stage/bucket: `closing`

Assessment: strong artifact task. It should verify conditions against source evidence. The current required `closing_checklist_artifact_id` is good, but required `cp_checklist` and `evidence_links` JSON fields duplicate what should usually live in the closing checklist artifact, source artifacts, or counsel-provided artifacts.

| Field | Current Section | Classification | Recommendation |
| --- | --- | --- | --- |
| `closing_checklist_artifact_id` | input | Artifact input | Keep required. |
| `cp_checklist` | input | Artifact-derived or artifact input | Prefer checklist content from `closing_checklist_artifact_id`, or use `cp_checklist_artifact_id` if separate. |
| `evidence_links` | input | Artifact/source input | Replace broad JSON with explicit evidence artifact/source refs where possible. |
| `counsel_requirements` | input | Artifact/source input | Prefer counsel requirements artifact/ref if reused. |
| `closing_status` | input | Project state input | Keep optional compact state if useful. |
| context fields | context | Context/bad shape | Remove broad context fields. |
| `conditions_precedent_verification_artifact_id` | output | Artifact output | Keep as primary output. |
| `signing_readiness`, `blocker_severity` | output | Project state output after review | May update compact closing readiness/blocker state. |
| `cp_evidence_mapping`, `missing_items`, `counsel_review_recommendation` | output | Artifact content | Fold into CP verification artifact. |
| generic outputs | output | Artifact content or task-local output | Remove as separate mapped project outputs. |

Recommended template changes:

- Move stage to `closing`.
- Keep `closing_checklist_artifact_id` as required file input.
- Remove required `cp_checklist`/`evidence_links` JSON unless converted to explicit artifact/source refs.
- Keep only `conditions_precedent_verification_artifact_id` as required artifact output.
- Promote only compact reviewed readiness/blocker state.

### `prepare-portfolio-onboarding`

Current stage: `portfolio_onboarding`

Recommended stage/bucket: `closing` for the six-stage model; possible separate `portfolio_onboarding` stage in an eight-stage variant

Assessment: strong artifact task for transition/handoff. In the six-stage Deal Room model, this should be a closing-stage task that prepares the post-investment handoff before terminal outcome `invested`. The required artifact inputs are good. Required `closing_summary` and `investment_terms` duplicate information that should come from the IC decision record, term sheet review, closing checklist, and CP verification artifacts.

| Field | Current Section | Classification | Recommendation |
| --- | --- | --- | --- |
| `ic_decision_record_artifact_id` | input | Artifact input | Keep required. |
| `closing_checklist_artifact_id` | input | Artifact input | Keep required. |
| `conditions_precedent_verification_artifact_id` | input | Artifact input | Keep required. |
| `closing_summary` | input | Bad duplication | Remove required richtext duplicate; derive from closing artifacts or allow task-local override. |
| `investment_terms` | input | Artifact-derived input | Prefer term sheet/IC artifact source; avoid required JSON duplicate. |
| `board_rep` | input | Project input or task-local input | Could be compact project field if the firm tracks it post-close; otherwise task-local. |
| `reporting_requirements`, `milestone_inputs` | input | Artifact input or task-local input | Prefer artifact/source refs or task-local setup details. |
| context fields | context | Context/bad shape | Remove broad context fields. |
| `portfolio_onboarding_plan_artifact_id` | output | Artifact output | Keep as primary output. |
| `reporting_cadence` | output | Project state output after review | May become compact post-close operating state if useful. |
| `board_setup_notes`, `hundred_day_plan`, `milestones`, `support_request_intake`, `owner_assignments` | output | Artifact content | Fold into onboarding plan artifact. |
| generic outputs | output | Artifact content or task-local output | Remove as separate mapped project outputs. |

Recommended template changes:

- Move stage to `closing` in the six-stage model.
- Keep the three required closing/decision artifact inputs.
- Remove required `closing_summary` and `investment_terms` duplicates.
- Keep only `portfolio_onboarding_plan_artifact_id` as required artifact output.
- Treat terminal `invested` as outcome/status after reviewed close readiness, not a normal work stage.

### Term Sheet, Closing, And Onboarding Decisions

Adopt these changes before rebuilding the project schema:

1. `term_sheet` remains a distinct stage; checklist, CP verification, signing, and portfolio handoff collapse into `closing`.
2. Portfolio onboarding should be a closing-stage handoff task in the six-stage model, with the option to split into a separate stage later.
3. Term sheets, closing workplans, CP checklists, evidence links, counsel requirements, and investment terms should be artifact/source references where possible, not required pasted text/JSON.
4. Required file outputs should remain first-class project artifact references: term sheet review, closing checklist, CP verification, and portfolio onboarding plan.
5. Only compact reviewed state should update project data: term approval state, closing status, close readiness, active blocker state, onboarding readiness, and terminal outcome.
6. Detailed deviation tables, counsel questions, owner/due-date tables, blockers, evidence mappings, missing items, milestones, reporting plans, and handoff plans should live in artifacts.
7. Broad context fields should be removed from these templates; task Q&A remains runtime context.

## Audit Completion Checkpoint

The task-by-task audit is now complete across admin/pipeline boundary, assessment, diligence, review/IC, term sheet, closing, and onboarding. The audit supports replacing the current exploratory schema/mapping patch rather than polishing it in place.

The next implementation slice should rebuild the VC Deal Room project type around:

1. A compact six-stage lifecycle: `intake`, `assessment`, `diligence`, `review`, `term_sheet`, and `closing`.
2. Durable project data grouped by identity/source, materials, stage/decision state, artifact index, and small operating fields.
3. Artifact-first task inputs and outputs, especially for pitch decks, transcripts, diligence evidence, review packs, IC materials, term sheets, closing materials, and onboarding plans.
4. Removal of `prior_task_outputs` and broad context mappings from VC task templates.
5. Mapping validation that enforces real project fields/task fields while discouraging broad context and generic blob fields.
