# VC Fund Routing and Deal Pipeline Cleanup

Pack version `0.5.46` defines the interim multi-Fund contract.

## Canonical Fund contract

- `vc.funds` is the only workspace Fund variable for Deal Pipeline, Deal Execution, and Origination Pipeline.
- Each Fund has stable `id`, `name`, and `status`; mandate fields remain workspace-owned context.
- Deal projects store only a human-confirmed `fund_id`.
- Suggestions remain conversational until the user explicitly confirms the exact Fund.
- First Look, evaluation, diligence, and the Deal Execution handoff use one matching active Fund and never blend mandates.

The representative fixture is `alludium/fixtures/fund-routing.yaml`.

## Deal Pipeline fields removed

The `vc_deal_room` project type version moves from `1.1.4` to `1.1.5`. Existing projects remain readable on their pinned version.

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

## Platform boundary

The platform supports `workspace.variable` and `project.field` prompt bindings, and project chats expose typed project reads and updates. The pack-owned `vc_deal_manager` therefore binds `vc.firmName`, `vc.funds`, and `fund_id`, and declares supported project, task, artifact, and `project.update` tools.

The current platform project-manager overlay schema is strict and does not accept `agentTemplateKey`; canonical project chats always resolve the platform-managed `project_manager` deployment. That deployment does not bind pack workspace variables, and its project context/tool reads expose typed project fields but not effective `vc.funds` values. The pack therefore cannot honestly attach `vc_deal_manager` or supply Fund mandates to the canonical runtime identity without a platform change. For this interim slice, `vc_deal_room.initialVersion.projectManager` carries the safe routing, confirmation, and unresolved-selection rules, while the pack-owned template has the full bindings and owns supported task routes. The canonical chat must treat Fund setup as unavailable when the runtime has not supplied `vc.funds`; no unsupported `agentTemplateKey`, alias, fallback, or copied Fund data is emitted.
