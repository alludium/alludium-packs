# VC Fund Routing and Deal Pipeline Cleanup

Pack version `0.5.48` established the canonical multi-Fund collection, project-scoped Deal Manager resolution, a workspace-scoped Pipeline Manager, progressive context rules, and Platform-backed Fund selection. The hub-free Origination follow-on applies that same Fund identity contract to Sourcing Lines and explicit Candidate-to-Deal promotion.

## Canonical Fund contract

- `vc.funds` is the only workspace Fund variable for Deal Pipeline, Deal Execution, Sourcing Lines, and Origination Candidates.
- Each Fund has stable `id`, `name`, and `status`; mandate fields remain workspace-owned context.
- Deal projects store only a human-confirmed `fund_id`.
- Each Sourcing Line stores one required, active `fund_id` and uses only that Fund's mandate for its experiment.
- Origination Candidates do not inherit or persist a Fund from their contributing lines. Deal promotion requires a separate explicit target-Fund choice.
- Suggestions remain conversational until the user explicitly confirms the exact Fund.
- First Look, evaluation, diligence, and the Deal Execution handoff use one matching active Fund and never blend mandates.

The representative fixture is `alludium/fixtures/fund-routing.yaml`.

## Deal Pipeline fields removed

The `vc_deal_room` project type version moves from `1.1.4` to `1.1.8`; draft `1.1.5` introduced the field cleanup, `1.1.6` added the explicit Deal Manager template binding and task-coordination overlay, `1.1.7` completed the `0.5.47` coordination contract, and `1.1.8` adds the Platform-backed Fund option source and navigation allowlist. Existing projects remain readable on their pinned version.

| Removed fields | Reason / canonical owner |
| --- | --- |
| `connected_systems`, `matching_signals`, `source_owner`, `crm_provider` | Unconsumed duplicates; source identity remains in `source_system`, `source_object_id`, `source_object_url`, and the Affinity receipt fields. |
| `meeting_notes_artifact_id` | Superseded by the active `meeting_record_artifact_ids` collection. |
| `deal_room_url`, `drive_deal_room_url` | The project and consolidated Data Room are canonical. |
| `investment_stage` | Duplicated the project lifecycle state. |
| `fund_thesis_context` | Replaced by confirmed `fund_id` plus `vc.funds`. |
| `thesis_target_list_artifact_id` | Sourcing Lines own target-list output. |
| `repo_or_code_access`, `financial_source_artifact_ids`, `technical_source_artifact_ids`, `market_source_artifact_ids`, `customer_evidence_artifact_ids` | Copied formal-diligence inputs; current Deal Pipeline evaluation uses its evaluation evidence fields, while Deal Execution retains formal diligence sources. |
| `legal_source_artifact_ids`, `investment_document_artifact_ids`, `transaction_bible_artifact_id`, `closing_source_artifact_ids`, `legal_document_status` | Deal Execution owns legal, contract, and closing evidence. |
| `term_approval_state`, `closing_status`, `close_readiness`, `onboarding_readiness`, `board_rep`, `reporting_cadence` | Deal Execution owns post-structuring status and portfolio handoff. |
| Formal DD, legal, closing, completion, and portfolio-onboarding artifact output fields | Their producer tasks are mapped only to Deal Execution. |

`cap_table_artifact_id`, term-sheet fields and outputs, `active_conditions`, IC records, source identity, source URLs, Affinity receipts, and evaluation outputs are retained because Deal Pipeline still owns provenance, decision review, and deal structuring.

## Agent and context contract

`vc_deal_room.initialVersion.projectManager.agentTemplateKey` is `vc_deal_manager`. The Pack change is from the generic platform `project_manager` runtime with VC display overlay copy to the stable Pack-owned Deal Manager template. The Deal Manager binds only the small `vc.firmName` and current project `fund_id` prompt values. It deliberately does not render the complete `vc.funds` array into every system prompt.

Deal Manager starts from a compact project context covering company identity, lifecycle stage, lead or owner, round/size, CRM/source provenance, task state, and relevant artifact/report pointers. It then reads selected task definitions, task state, artifacts, and Fund mandate context progressively. It prefers a matching predefined task, uses ad-hoc tasks only for specific uncovered work, validates people/agent assignees, checks for existing work, and requires explicit approval for model- or report-generated task creation and assignment.

`vc_pipeline_autopilot` retains its stable template ID but displays as **Pipeline Manager**. It is the intended non-Deal VC workspace chat agent. It begins with native Alludium Deal navigation, compares selected Deals, finds missing/invalid Fund assignments, prepares weekly and selected-Fund summaries, and produces reviewed task or chat-to-Deal proposals. It does not replace Deal Manager or persist model suggestions.

The Live Deal Status Report remains an eleven-tab HTML artifact. Its optional `fund_id` input is mapped directly from the Deal. The report resolves that ID by exact equality against `vc.funds`, shows the matching actively-investing Fund's human-readable name, and evaluates Fund fit using only that record's mandate fields. Unassigned, unknown, inactive, and unconfigured states are displayed explicitly and make no Fund-relative fit claim; the report never selects or persists a Fund.

The task also returns a bounded `open_questions` JSON index with stable IDs, evidence needs, suggested owner roles, statuses, and real source references. The report never creates tasks; Deal Manager may turn the index into a deduplicated proposal for human approval.

## Platform boundary

Remi's platform work in issue `#3264` adds `agentTemplateKey` to the strict project-manager overlay schema and resolves a Pack template for canonical project chat. The Pack now emits that supported key. Platform issue `#3219` owns the remaining compact Deal context, progressive Fund access, and approved task-coordination policy needed to expose all declared tools safely.

Pack version `0.5.48` uses the reviewed generic Platform schemas for:

- platform `#3464`: bind the VC workspace chat surface to `vc_pipeline_autopilot` without hard-coding Navigator or a deployment ID;
- platform `#3465`: Pack-declared `navigationFieldKeys: ["fund_id"]`, bounded projection, and server-side Fund/Unassigned filters;
- platform `#3448`: schema-driven collection settings for `vc.funds`;
- platform `#3449`: workspace-variable-backed project field options and server validation for `fund_id`;

Platform `#3466` remains a Platform-owned typed, reviewed workspace-chat-to-Deal workflow and does not require a new Pack declaration in this release.

Until the paired Platform consumers land, these declarations do not provide the corresponding UI or server behavior on their own. The Pack does not add a VC-only repository method, raw deployment ID, copied Fund fields, or browser-authoritative selection and navigation behavior.

## Hub retirement and Origination routing

The active Origination contract no longer requires `vc_origination_pipeline`. `/vc/origination` is a workspace projection over the Sourcing Line and Origination Candidate projects the current user may access:

- `vc_sourcing_line` requires only `line_name` and an active canonical `fund_id` at creation.
- `vc_origination_candidate` preserves every contributing line through native `vc.sourcing_line_originated_candidate` relationships; it has no exclusive owner-line or candidate-level Fund.
- The workspace Origination Manager derives attention, health, counts, performance, and promotion readiness from current visible projects and receipts. Hub caches and a scheduled cross-line digest are not evidence or prerequisites.
- Promotion preserves all line provenance and requires the user to select the exact active Deal Fund. The creation proposal must carry that choice as `createRequest.fieldValues.fund_id`.

The retired `vc_origination_pipeline` key is historical migration context only. Because Origination was not previously used as a released production workflow, this release does not transform Hub projects into lines or Candidates. Existing pinned project-type versions remain readable under the platform's normal versioning rules, but the current Pack catalog must not offer Hub creation or require a Hub relationship.
