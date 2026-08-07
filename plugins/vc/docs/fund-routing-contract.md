# VC Fund Routing and Deal Pipeline Cleanup

Pack version `0.5.47` extends the interim multi-Fund contract with project-scoped Deal Manager resolution, a workspace-scoped Pipeline Manager, progressive context rules, and structured report questions for reviewed task proposals.

## Canonical Fund contract

- `vc.funds` is the only workspace Fund variable for Deal Pipeline, Deal Execution, and Origination Pipeline.
- Each Fund has stable `id`, `name`, and `status`; mandate fields remain workspace-owned context.
- Deal projects store only a human-confirmed `fund_id`.
- Suggestions remain conversational until the user explicitly confirms the exact Fund.
- First Look, evaluation, diligence, and the Deal Execution handoff use one matching active Fund and never blend mandates.

The representative fixture is `alludium/fixtures/fund-routing.yaml`.

## Deal Pipeline fields removed

The `vc_deal_room` project type version moves from `1.1.4` to `1.1.6`; draft `1.1.5` introduced the field cleanup and `1.1.6` adds the explicit Deal Manager template binding and task-coordination overlay. Existing projects remain readable on their pinned version.

| Removed fields | Reason / canonical owner |
| --- | --- |
| `connected_systems`, `matching_signals`, `source_owner`, `crm_provider` | Unconsumed duplicates; source identity remains in `source_system`, `source_object_id`, `source_object_url`, and the Affinity receipt fields. |
| `meeting_notes_artifact_id` | Superseded by the active `meeting_record_artifact_ids` collection. |
| `deal_room_url`, `drive_deal_room_url` | The project and consolidated Data Room are canonical. |
| `investment_stage` | Duplicated the project lifecycle state. |
| `fund_thesis_context` | Replaced by confirmed `fund_id` plus `vc.funds`. |
| `thesis_target_list_artifact_id` | Origination Pipeline owns target-list output. |
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

The following generic Platform contracts are intentionally not invented in this Pack before their schemas exist:

- platform `#3464`: bind the VC workspace chat surface to `vc_pipeline_autopilot` without hard-coding Navigator or a deployment ID;
- platform `#3465`: Pack-declared `navigationFieldKeys: ["fund_id"]`, bounded projection, and server-side Fund/Unassigned filters;
- platform `#3448`: schema-driven collection settings for `vc.funds`;
- platform `#3449`: workspace-variable-backed project field options and server validation for `fund_id`;
- platform `#3466`: typed, reviewed workspace-chat-to-Deal creation.

Until those consumers land, the Pack provides the stable agent IDs, project field, prompt/task behavior, report output, fixtures, and explicit dependencies. It does not add a VC-only repository method, raw deployment ID, copied Fund fields, or an unvalidated workspace-chat/navigation schema.
