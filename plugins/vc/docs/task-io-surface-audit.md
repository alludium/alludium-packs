# VC Task Input/Output Surface Audit

Date: 2026-06-04

Scope: all task definition templates in `plugins/vc/alludium/task-definition-templates`, generated task docs in `plugins/vc/tasks`, project-type mappings in `plugins/vc/alludium/project-types`, validation scripts in `plugins/vc/scripts`, and `documentRefs` / `outputFieldKey` contracts. This artifact records the audit and implemented output-surface cleanup slices.

## Executive Summary

- Baseline main had 92 task templates, 645 output declarations, 66 file outputs, and 579 non-file outputs.
- This branch now has 229 output declarations: 66 file outputs and 163 non-file outputs. The cleanup removed 416 output declarations while preserving mapped artifacts, document-ref output contracts, project setup/import evidence, command-view artifact slots, required fields, and downstream project mappings.
- The repeated generic bundle (`summary`, `next_actions`, `recommendation`, `source_links`, `assumptions`, `evidence_quality`, `open_questions`, `risks`, `human_decision_points`) has dropped from 263 baseline declarations to 1 retained declaration. The retained field is `vc-pack-variable-discovery.summary`, which is projected into parent Pack Setup context.
- For tasks with `output_template` documents, this branch now removes non-contract standalone fields when the durable artifact should carry that content. Remaining non-file outputs on template-backed tasks are mapped, required, or compact status/count fields.
- The remaining cleanup is now product-shaped rather than generic-noise cleanup: decide how lean no-artifact task surfaces and integration setup receipts should be.

## Global Inventory Statistics

| Metric | Value |
| --- | ---: |
| Task templates | 92 |
| Input field declarations | 260 |
| Unique input keys | 177 |
| Output field declarations | 229 |
| Unique output keys | 179 |
| File outputs | 66 |
| Non-file outputs | 163 |
| Required outputs | 71 (66 file, 5 non-file) |
| Optional outputs | 158 |
| Tasks with any `documentRefs` | 53 |
| Tasks with `output_template` refs | 41 |
| `output_template` refs | 42 |
| `output_template` refs with `outputFieldKey` | 41 |
| All `documentRefs` with `outputFieldKey` | 49 |
| Project output-mapped fields | 104 |
| Project setup/import evidence output keys | 6 |
| Command-view artifact output refs | 20 |
| Likely removable/hideable outputs remaining | Product-review candidates only |

Output field types: `date` 1, `file` 66, `json` 39, `number` 23, `richtext` 66, `select` 1, `string` 33.

## Cleanup Completed

- `capture-opportunity-intake` was reduced from 15 outputs to 4: artifact, recommendation, missing information, and red flags.
- The 24 highest-noise artifact-backed tasks were reduced so they keep artifact IDs and concise status fields only.
- A second document-template pass removed 51 more standalone fields from `output_template` tasks where the durable artifact should carry the content.
- A third pass removed the remaining unused generic output bundle from `generate-diligence-questions`, `run-investment-fit-screen`, `prepare-deal-flow-agenda`, `review-opportunity-status`, and `capture-investment-management-handoff`.
- A fourth pass removed artifact-internal metadata from `generate-diligence-questions` and `run-investment-fit-screen`, plus `run-vc-sourcing-pipeline.child_task_plan`.
- Template patch versions were bumped for every changed task template so platform ingest can create new task definition template versions.
- Generated task markdown was regenerated from YAML.

## Remaining Review Targets

| Task | Outputs | Review target | Notes |
| --- | ---: | --- | --- |
| Artifact-backed status fields | varies | Compact decision/count fields | Remaining fields such as `overall_recommendation`, source health/status fields, and counts are intentionally small scan surfaces. |
| No-artifact workflow tasks | varies | Task-specific inline fields | `prepare-deal-flow-agenda`, `review-opportunity-status`, `create-deal`, and `capture-investment-management-handoff` still use fields as their primary result surface. |
| Integration discovery/setup/sync tasks | varies | Operational receipt fields | These are not project-mapped, but they act as inline setup/sync receipts where there is no artifact output. |

No generic output bundle remains. The only remaining generic-named output is `vc-pack-variable-discovery.summary`, retained because `definitionJson.instructions.orchestration.parentContextProjection` maps it to `packSetup.variableDiscovery.summary`.

## Template-Backed Non-File Outputs Remaining

These remain because they are mapped, required, or compact status/count fields rather than document-internal detail.

| Task | Remaining non-file outputs |
| --- | --- |
| `analyze-deal-terms` | `open_commercial_terms` |
| `audit-linkedin-query-spend` | `paid_source_spend_status` |
| `prepare-initial-linkedin-reachout` | `initial_reachout_draft_count` |
| `prepare-outreach-draft-queue` | `outreach_draft_count` |
| `prepare-second-reachout-email` | `second_reachout_draft_count` |
| `record-linkedin-connection-attempt` | `outbound_status` |
| `review-outreach-outcome` | `recommended_terminal_state` |
| `review-source-errors-and-spend` | `source_health_status` |
| `run-commercial-evaluation` | `main_commercial_hypothesis`, `commercial_gating_risk`, `next_commercial_proof_needed` |
| `run-financial-evaluation` | `main_financial_hypothesis`, `financial_gating_risk`, `next_financial_proof_needed` |
| `run-team-evaluation` | `main_team_hypothesis`, `team_gating_risk`, `next_team_proof_needed` |
| `run-technical-evaluation` | `main_technical_hypothesis`, `technical_gating_risk`, `next_technical_proof_needed` |
| `run-vc-sourcing-pipeline` | `run_status`, `new_candidates_count`, `promotion_ready_count`, `run_completed_at` |
| `screen-founder-connected-candidate` | `founder_connected_screen_recommendation` |

## Repeated Generic Fields

| Output key | Current declarations | Project output mappings | Policy |
| --- | ---: | ---: | --- |
| `summary` | 1 | 0 | Retain only for `vc-pack-variable-discovery`, where parent setup orchestration consumes it. Otherwise use task completion summary or artifact executive summary. |
| `next_actions` | 0 | 0 | Move into artifact/body; do not add as standalone UI field. |
| `recommendation` | 0 | 0 | Use task-specific decision fields instead, e.g. `overall_recommendation` or `fit_recommendation`. |
| `source_links` | 0 | 0 | Move into artifact/body; do not add as standalone UI field. |
| `assumptions` | 0 | 0 | Move into artifact/body; do not add as standalone UI field. |
| `evidence_quality` | 0 | 0 | Move into artifact/body; do not add as standalone UI field. |
| `open_questions` | 0 | 0 | Move into artifact/body; do not add as standalone UI field. |
| `risks` | 0 | 0 | Move into artifact/body; do not add as standalone UI field. |
| `human_decision_points` | 0 | 0 | Move into artifact/body; do not add as standalone UI field. |

## Risk Notes

- Do not remove file outputs referenced by `documentRefs[].outputFieldKey` or `config.documentRefId`; the validator enforces that pair.
- Do not remove project output-mapped artifact IDs without updating `projectTaskMappings`, command-view output slots, project fields, generated docs, and downstream input mappings.
- Be careful with non-file mapped fields in origination setup and deal structuring, especially `source_registry`, `review_policy`, and `open_commercial_terms`.
- Setup/import fields such as `import_status`, `import_summary`, `imported_field_map`, `source_index`, and `next_task_recommendations` are referenced by setup import evidence.
- Generated markdown docs mention output keys because docs are generated from YAML. Those mentions are documentation surface, not independent downstream runtime usage.

## Suggested Follow-Up Slices

1. Review no-artifact task surfaces: decide whether tasks such as `create-deal`, `capture-investment-management-handoff`, `prepare-deal-flow-agenda`, and `review-opportunity-status` should keep their task-specific inline outputs or rely more on the completion response.
2. Review integration discovery/setup/sync receipt fields as a UX question; they are mostly unmapped but currently serve as the only structured task result.
3. Add a validator warning for tasks with `output_template` refs and more than three unmapped non-file outputs.
4. Consider generated-doc language that distinguishes contract outputs from artifact-internal detail.

## Per-Task Recommendation Table

| Task | Version | In | Out | Contract/mapped outputs | Visible status outputs | Move/hide candidates | Recommendation |
| --- | --- | ---: | ---: | --- | --- | --- | --- |
| `affinity-deal-room-import` | `0.1.4` | 1 | 6 | `affinity_import_receipt_artifact_id`, `import_status`, `import_summary`, `imported_field_map`, `source_index`, `next_task_recommendations` | - | - | Preserve mapped/status surface; revisit only with UX evidence. |
| `affinity-discovery` | `0.1.4` | 1 | 2 | - | `affinity_discovery_report`, `scope_questions` | - | Current surface is tight. |
| `affinity-setup` | `0.1.11` | 1 | 7 | - | `setup_summary`, `accepted_connection_scope`, `child_task_plan`, `selected_source_scope`, `accepted_stage_mapping`, `seed_selection`, +1 more | - | Preserve mapped/status surface; revisit only with UX evidence. |
| `affinity-sync-read` | `0.1.6` | 1 | 2 | - | `affinity_import_preview`, `mapping_decisions` | - | Current surface is tight. |
| `affinity-sync-write` | `0.1.3` | 1 | 1 | - | `affinity_write_back_proposals` | - | Current surface is tight. |
| `analyze-deal-terms` | `0.1.1` | 10 | 2 | `deal_terms_analysis_artifact_id`, `open_commercial_terms` | - | - | Current surface is tight. |
| `apify-discovery` | `0.1.4` | 1 | 2 | - | `apify_discovery_report`, `source_scope_questions` | - | Current surface is tight. |
| `apify-setup` | `0.1.8` | 1 | 4 | - | `setup_summary`, `accepted_connection_scope`, `child_task_plan`, `sync_policy` | - | Current surface is tight. |
| `apify-sync-read` | `0.1.4` | 1 | 2 | - | `apify_results_preview`, `source_registry_mapping` | - | Current surface is tight. |
| `audit-linkedin-query-spend` | `0.1.9` | 1 | 2 | `linkedin_spend_audit_artifact_id`, `paid_source_spend_status` | - | - | Current surface is tight. |
| `capture-investment-management-handoff` | `0.1.1` | 5 | 3 | `projectCreation` | `handoff_summary`, `missing_information` | - | Current no-artifact surface is compact; revisit only with UX evidence. |
| `capture-opportunity-intake` | `1.0.19` | 10 | 4 | `opportunity_intake_artifact_id` | `fit_recommendation`, `missing_information`, `red_flags` | - | Current surface is tight. |
| `check-affinity-relationship-context` | `0.1.3` | 1 | 3 | `relationship_context_artifact_id` | `known_candidate_count`, `relationship_report` | - | Current surface is tight. |
| `companies-house-discovery` | `0.1.4` | 1 | 2 | - | `companies_house_discovery_report`, `source_scope_questions` | - | Current surface is tight. |
| `companies-house-setup` | `0.1.8` | 1 | 4 | - | `setup_summary`, `accepted_connection_scope`, `child_task_plan`, `sync_policy` | - | Current surface is tight. |
| `companies-house-sync-read` | `0.1.4` | 1 | 2 | - | `companies_house_results_preview`, `source_registry_mapping` | - | Current surface is tight. |
| `configure-origination-pipeline` | `0.1.12` | 3 | 5 | `source_registry`, `review_policy`, `projectCreation` | `configuration_summary`, `child_task_plan` | - | Current surface is tight. |
| `coordinate-capital-call-and-completion` | `0.1.2` | 7 | 1 | `completion_tracker_artifact_id` | - | - | Current surface is tight. |
| `create-deal` | `1.0.0` | 6 | 3 | `projectCreation` | `creation_summary`, `missing_creation_context` | - | Current surface is tight. |
| `create-ic-memo` | `1.0.16` | 11 | 1 | `investment_memo_artifact_id` | - | - | Current surface is tight. |
| `discover-companies-house-candidates` | `0.1.5` | 1 | 4 | `companies_house_discovery_artifact_id`, `source_result_count` | `discovery_report`, `source_state_summary` | - | Current surface is tight. |
| `discover-github-builder-signals` | `0.1.4` | 1 | 4 | `github_discovery_artifact_id`, `source_result_count` | `discovery_report`, `source_state_summary` | - | Current surface is tight. |
| `discover-linkedin-founder-candidates` | `0.1.5` | 1 | 4 | `linkedin_discovery_artifact_id`, `source_result_count` | `discovery_report`, `source_state_summary` | - | Current surface is tight. |
| `discover-reddit-builder-signals` | `0.1.4` | 1 | 4 | `reddit_discovery_artifact_id`, `source_result_count` | `discovery_report`, `source_state_summary` | - | Current surface is tight. |
| `discover-x-founder-signals` | `0.1.5` | 1 | 4 | `x_founder_discovery_artifact_id`, `source_result_count` | `discovery_report`, `source_state_summary` | - | Current surface is tight. |
| `enrich-sourcing-candidate` | `0.1.5` | 1 | 4 | `enrichment_artifact_id` | `enriched_candidate_count`, `enrichment_status`, `enrichment_report` | - | Current surface is tight. |
| `generate-diligence-questions` | `1.0.20` | 4 | 1 | `diligence_question_bank_artifact_id` | - | - | Artifact-only surface is tight. |
| `generate-sourcing-digest` | `0.1.9` | 1 | 1 | `sourcing_digest_artifact_id` | - | - | Current surface is tight. |
| `google-drive-discovery` | `0.1.4` | 1 | 2 | - | `google_drive_discovery_report`, `source_scope_questions` | - | Current surface is tight. |
| `google-drive-setup` | `0.1.4` | 1 | 4 | - | `setup_summary`, `accepted_connection_scope`, `child_task_plan`, `sync_policy` | - | Current surface is tight. |
| `google-drive-sync-read` | `0.1.4` | 1 | 2 | - | `google_drive_context_preview`, `target_context_mapping` | - | Current surface is tight. |
| `google-drive-sync-write` | `0.1.3` | 1 | 1 | - | `google_drive_write_proposals` | - | Current surface is tight. |
| `harmonic-discovery` | `0.1.3` | 1 | 2 | - | `harmonic_discovery_report`, `source_scope_questions` | - | Current surface is tight. |
| `harmonic-setup` | `0.1.4` | 1 | 4 | - | `setup_summary`, `accepted_connection_scope`, `child_task_plan`, `sync_policy` | - | Current surface is tight. |
| `harmonic-sync-read` | `0.1.4` | 1 | 2 | - | `harmonic_results_preview`, `target_context_mapping` | - | Current surface is tight. |
| `ingest-manual-sourcing-tip` | `0.1.4` | 1 | 3 | `manual_tip_ingestion_artifact_id` | `normalized_candidate_key`, `ingestion_report` | - | Current surface is tight. |
| `manage-closing-checklist` | `1.0.14` | 9 | 1 | `closing_checklist_artifact_id` | - | - | Current surface is tight. |
| `notion-discovery` | `0.1.4` | 1 | 2 | - | `notion_discovery_report`, `scope_questions` | - | Current surface is tight. |
| `notion-setup` | `0.1.4` | 1 | 4 | - | `setup_summary`, `accepted_connection_scope`, `child_task_plan`, `sync_policy` | - | Current surface is tight. |
| `notion-sync-read` | `0.1.4` | 1 | 2 | - | `notion_context_preview`, `target_context_mapping` | - | Current surface is tight. |
| `notion-sync-write` | `0.1.3` | 1 | 1 | - | `notion_update_proposals` | - | Current surface is tight. |
| `prepare-deal-flow-agenda` | `1.0.8` | 3 | 5 | - | `agenda`, `stale_deal_list`, `new_deal_list`, `stage_change_candidates`, `seven_day_action_plan` | - | Current no-artifact surface is task-specific and compact. |
| `prepare-ic-agenda` | `1.0.12` | 1 | 1 | `ic_agenda_artifact_id` | - | - | Current surface is tight. |
| `prepare-initial-linkedin-reachout` | `0.1.1` | 1 | 2 | `initial_linkedin_reachout_artifact_id`, `initial_reachout_draft_count` | - | - | Current surface is tight. |
| `prepare-lead-gen-packet` | `1.0.16` | 3 | 1 | `lead_generation_packet_artifact_id` | - | - | Current surface is tight. |
| `prepare-meeting` | `1.0.14` | 5 | 1 | `initial_call_brief_artifact_id` | - | - | Current surface is tight. |
| `prepare-outreach-draft-queue` | `0.1.9` | 1 | 2 | `outreach_queue_artifact_id`, `outreach_draft_count` | - | - | Current surface is tight. |
| `prepare-partner-review-pack` | `1.0.17` | 10 | 1 | `partner_review_pack_artifact_id` | - | - | Current surface is tight. |
| `prepare-portfolio-onboarding` | `1.0.13` | 4 | 1 | `portfolio_onboarding_plan_artifact_id` | - | - | Current surface is tight. |
| `prepare-prospect-summary` | `0.1.9` | 1 | 1 | `prospect_summary_artifact_id` | - | - | Current surface is tight. |
| `prepare-second-reachout-email` | `0.1.1` | 1 | 2 | `second_reachout_email_artifact_id`, `second_reachout_draft_count` | - | - | Current surface is tight. |
| `prepare-team-review-pack` | `1.0.19` | 9 | 1 | `team_review_pack_artifact_id` | - | - | Current surface is tight. |
| `promote-candidate-to-deal-pipeline` | `0.1.10` | 1 | 1 | `promotion_package_artifact_id` | - | - | Current surface is tight. |
| `record-ic-decision` | `1.0.13` | 6 | 1 | `ic_decision_record_artifact_id` | - | - | Current surface is tight. |
| `record-linkedin-connection-attempt` | `0.1.1` | 1 | 2 | `connection_record_artifact_id`, `outbound_status` | - | - | Current surface is tight. |
| `request-founder-materials` | `1.0.12` | 4 | 1 | `founder_materials_request_artifact_id` | - | - | Current surface is tight. |
| `review-ic-memo` | `1.0.15` | 2 | 1 | `ic_memo_review_artifact_id` | - | - | Current surface is tight. |
| `review-investment-documents` | `0.1.3` | 8 | 1 | `investment_document_review_artifact_id` | - | - | Current surface is tight. |
| `review-opportunity-status` | `1.0.12` | 4 | 4 | - | `stage_summary`, `missing_inputs`, `stage_transition_recommendation`, `next_task_suggestions` | - | Current no-artifact surface is task-specific and compact. |
| `review-outreach-outcome` | `0.1.1` | 1 | 2 | `outreach_outcome_artifact_id`, `recommended_terminal_state` | - | - | Current surface is tight. |
| `review-portfolio-overlap` | `0.1.4` | 1 | 3 | `portfolio_overlap_artifact_id` | `high_overlap_count`, `overlap_report` | - | Current surface is tight. |
| `review-reddit-candidate-inbox` | `0.1.3` | 1 | 4 | `reddit_inbox_review_artifact_id`, `needs_review_count` | `approved_candidate_count`, `review_report` | - | Current surface is tight. |
| `review-source-errors-and-spend` | `0.1.9` | 1 | 2 | `source_health_artifact_id`, `source_health_status` | - | - | Current surface is tight. |
| `review-term-sheet` | `1.0.13` | 5 | 1 | `term_sheet_review_artifact_id` | - | - | Current surface is tight. |
| `review-unicorn-signature` | `0.1.0` | 1 | 3 | `unicorn_signature_artifact_id`, `unicorn_signature_recommendation` | `unicorn_signature_report` | - | Current surface is tight. |
| `run-commercial-dd` | `1.0.18` | 6 | 3 | `commercial_dd_artifact_id`, `market_analysis_artifact_id`, `customer_reference_summary_artifact_id` | - | - | Current surface is tight. |
| `run-commercial-evaluation` | `0.1.1` | 4 | 4 | `commercial_evaluation_artifact_id`, `main_commercial_hypothesis`, `commercial_gating_risk`, `next_commercial_proof_needed` | - | - | Current surface is tight. |
| `run-deal-fit-analysis` | `0.1.0` | 1 | 3 | `deal_fit_artifact_id`, `deal_fit_ready_count` | `deal_fit_report` | - | Current surface is tight. |
| `run-financial-dd` | `1.0.17` | 5 | 2 | `financial_dd_artifact_id`, `unit_economics_artifact_id` | - | - | Current surface is tight. |
| `run-financial-evaluation` | `0.1.1` | 4 | 4 | `financial_evaluation_artifact_id`, `main_financial_hypothesis`, `financial_gating_risk`, `next_financial_proof_needed` | - | - | Current surface is tight. |
| `run-founder-evaluation` | `1.0.16` | 3 | 1 | `founder_evaluation_artifact_id` | - | - | Current surface is tight. |
| `run-investment-fit-screen` | `1.0.18` | 6 | 2 | `investment_screen_scorecard_artifact_id` | `overall_recommendation` | - | Artifact plus one concise decision field. |
| `run-legal-diligence` | `0.1.4` | 7 | 1 | `legal_diligence_artifact_id` | - | - | Current surface is tight. |
| `run-opportunity-evaluation` | `1.0.16` | 3 | 1 | `follow_up_evaluation_artifact_id` | - | - | Current surface is tight. |
| `run-team-evaluation` | `0.1.1` | 4 | 4 | `team_evaluation_artifact_id`, `main_team_hypothesis`, `team_gating_risk`, `next_team_proof_needed` | - | - | Current surface is tight. |
| `run-technical-dd` | `1.0.15` | 5 | 1 | `technical_dd_artifact_id` | - | - | Current surface is tight. |
| `run-technical-evaluation` | `0.1.1` | 4 | 4 | `technical_evaluation_artifact_id`, `main_technical_hypothesis`, `technical_gating_risk`, `next_technical_proof_needed` | - | - | Current surface is tight. |
| `run-vc-sourcing-pipeline` | `0.1.14` | 2 | 7 | `run_status`, `new_candidates_count`, `promotion_ready_count`, `run_completed_at`, `run_receipt_artifact_id`, `candidate_batch_artifact_id`, `source_state_artifact_id` | - | - | Preserve compact run status/counts and artifacts. |
| `score-sourcing-candidate` | `0.1.10` | 2 | 5 | `scoring_artifact_id`, `promotion_ready_count` | `meet_candidate_count`, `watch_candidate_count`, `scoring_report` | - | Current surface is tight. |
| `screen-active-sourcing-candidate` | `0.1.12` | 1 | 3 | `screening_artifact_id`, `promotion_ready_count` | `screening_report` | - | Current surface is tight. |
| `screen-founder-connected-candidate` | `0.1.2` | 2 | 2 | `founder_connected_screen_artifact_id`, `founder_connected_screen_recommendation` | - | - | Current surface is tight. |
| `screen-identified-candidate` | `0.1.1` | 2 | 5 | `identified_screen_artifact_id`, `outreach_ready_count` | `watchlist_count`, `pass_count`, `identified_screen_report` | - | Current surface is tight. |
| `slack-discovery` | `0.1.3` | 1 | 2 | - | `slack_discovery_report`, `channel_scope_questions` | - | Current surface is tight. |
| `slack-setup` | `0.1.4` | 1 | 4 | - | `setup_summary`, `accepted_connection_scope`, `child_task_plan`, `sync_policy` | - | Current surface is tight. |
| `slack-sync-read` | `0.1.4` | 1 | 2 | - | `slack_context_preview`, `target_context_mapping` | - | Current surface is tight. |
| `slack-sync-write` | `0.1.3` | 1 | 1 | - | `slack_handoff_draft` | - | Current surface is tight. |
| `source-thesis-targets` | `1.0.14` | 4 | 1 | `thesis_target_list_artifact_id` | - | - | Current surface is tight. |
| `summarize-meeting-records` | `1.0.14` | 4 | 1 | `customer_insights_artifact_id` | - | - | Current surface is tight. |
| `sync-sourcing-candidate` | `0.1.4` | 1 | 3 | `sync_plan_artifact_id` | `sync_status`, `sync_report` | - | Current surface is tight. |
| `track-term-sheet-negotiation` | `0.1.1` | 7 | 1 | `negotiation_brief_artifact_id` | - | - | Current surface is tight. |
| `vc-pack-variable-discovery` | `1.0.3` | 3 | 3 | `summary`, `variable_answers`, `invite_candidates` | - | - | Retain: fields are projected into parent Pack Setup context. |
| `verify-conditions-precedent` | `1.0.13` | 4 | 1 | `conditions_precedent_verification_artifact_id` | - | - | Current surface is tight. |

## Inventory Appendix

### `affinity-deal-room-import`

- Template id: `vc.affinity_deal_room_import`; version: `0.1.4`; family: `integration_project_import`; stage: `intake`.
- Inputs (1): `import_payload`.
- Outputs (6): `affinity_import_receipt_artifact_id`, `import_status`, `import_summary`, `imported_field_map`, `source_index`, `next_task_recommendations`.

### `affinity-discovery`

- Template id: `vc.affinity_discovery`; version: `0.1.4`; family: `integration_discovery`; stage: `-`.
- Inputs (1): `discovery_goal`.
- Outputs (2): `affinity_discovery_report`, `scope_questions`.

### `affinity-setup`

- Template id: `vc.affinity_setup`; version: `0.1.11`; family: `integration_setup`; stage: `-`.
- Inputs (1): `setup_goal`.
- Outputs (7): `setup_summary`, `accepted_connection_scope`, `child_task_plan`, `selected_source_scope`, `accepted_stage_mapping`, `seed_selection`, `sync_policy`.

### `affinity-sync-read`

- Template id: `vc.affinity_sync_read`; version: `0.1.6`; family: `integration_sync_read`; stage: `-`.
- Inputs (1): `selected_affinity_scope`.
- Outputs (2): `affinity_import_preview`, `mapping_decisions`.

### `affinity-sync-write`

- Template id: `vc.affinity_sync_write`; version: `0.1.3`; family: `integration_sync_write`; stage: `-`.
- Inputs (1): `write_back_source`.
- Outputs (1): `affinity_write_back_proposals`.

### `analyze-deal-terms`

- Template id: `vc.analyze_deal_terms`; version: `0.1.1`; family: `deal_structuring`; stage: `deal_structuring`.
- Inputs (10): `proposed_investment_amount`, `valuation`, `round_size`, `cap_table_artifact_id`, `esop`, `co_investors`, `ownership_target`, `follow_on_reserve_policy`, `deal_terms_snapshot`, `financial_forecast_artifact_id`.
- Outputs (2): `deal_terms_analysis_artifact_id`, `open_commercial_terms`.
- Output-template refs: `deal_terms_analysis_artifact_id`.

### `apify-discovery`

- Template id: `vc.apify_discovery`; version: `0.1.4`; family: `integration_discovery`; stage: `-`.
- Inputs (1): `discovery_goal`.
- Outputs (2): `apify_discovery_report`, `source_scope_questions`.

### `apify-setup`

- Template id: `vc.apify_setup`; version: `0.1.8`; family: `integration_setup`; stage: `-`.
- Inputs (1): `setup_goal`.
- Outputs (4): `setup_summary`, `accepted_connection_scope`, `child_task_plan`, `sync_policy`.

### `apify-sync-read`

- Template id: `vc.apify_sync_read`; version: `0.1.4`; family: `integration_sync_read`; stage: `-`.
- Inputs (1): `selected_apify_scope`.
- Outputs (2): `apify_results_preview`, `source_registry_mapping`.

### `audit-linkedin-query-spend`

- Template id: `vc.audit_linkedin_query_spend`; version: `0.1.9`; family: `origination_spend_audit`; stage: `operate`.
- Inputs (1): `spend_audit_scope`.
- Outputs (2): `linkedin_spend_audit_artifact_id`, `paid_source_spend_status`.
- Output-template refs: `linkedin_spend_audit_artifact_id`.

### `capture-investment-management-handoff`

- Template id: `vc.capture_investment_management_handoff`; version: `0.1.1`; family: `investment_management_setup`; stage: `formal_diligence`.
- Inputs (5): `company_name`, `lead_partner`, `handoff_source_artifact_ids`, `ic_decision_record_artifact_id`, `term_sheet_review_artifact_id`.
- Outputs (3): `projectCreation`, `handoff_summary`, `missing_information`.

### `capture-opportunity-intake`

- Template id: `vc.capture_opportunity_intake`; version: `1.0.19`; family: `intake`; stage: `intake`.
- Inputs (10): `company_name`, `pitch_deck_artifact_id`, `company_domain`, `source_system`, `source_object_url`, `source_thread_url`, `source_thread_artifact_id`, `source_material_artifact_ids`, `founder_materials_artifact_ids`, `referrer`.
- Outputs (4): `opportunity_intake_artifact_id`, `fit_recommendation`, `missing_information`, `red_flags`.

### `check-affinity-relationship-context`

- Template id: `vc.check_affinity_relationship_context`; version: `0.1.3`; family: `origination_relationship_check`; stage: `enrich`.
- Inputs (1): `relationship_check_scope`.
- Outputs (3): `relationship_context_artifact_id`, `known_candidate_count`, `relationship_report`.

### `companies-house-discovery`

- Template id: `vc.companies_house_discovery`; version: `0.1.4`; family: `integration_discovery`; stage: `-`.
- Inputs (1): `discovery_goal`.
- Outputs (2): `companies_house_discovery_report`, `source_scope_questions`.

### `companies-house-setup`

- Template id: `vc.companies_house_setup`; version: `0.1.8`; family: `integration_setup`; stage: `-`.
- Inputs (1): `setup_goal`.
- Outputs (4): `setup_summary`, `accepted_connection_scope`, `child_task_plan`, `sync_policy`.

### `companies-house-sync-read`

- Template id: `vc.companies_house_sync_read`; version: `0.1.4`; family: `integration_sync_read`; stage: `-`.
- Inputs (1): `selected_companies_house_scope`.
- Outputs (2): `companies_house_results_preview`, `source_registry_mapping`.

### `configure-origination-pipeline`

- Template id: `vc.configure_origination_pipeline`; version: `0.1.12`; family: `origination_pipeline_setup`; stage: `setup`.
- Inputs (3): `pipeline_name`, `configuration_goal`, `current_pipeline_context`.
- Outputs (5): `configuration_summary`, `source_registry`, `review_policy`, `child_task_plan`, `projectCreation`.

### `coordinate-capital-call-and-completion`

- Template id: `vc.coordinate_capital_call_and_completion`; version: `0.1.2`; family: `closing`; stage: `closing`.
- Inputs (7): `conditions_precedent_verification_artifact_id`, `closing_checklist_artifact_id`, `transaction_bible_artifact_id`, `administrator_contact`, `capital_call_status`, `funds_transfer_status`, `share_certificate_status`.
- Outputs (1): `completion_tracker_artifact_id`.
- Output-template refs: `completion_tracker_artifact_id`.

### `create-deal`

- Template id: `vc.create_deal`; version: `1.0.0`; family: `deal_pipeline_project_creation`; stage: `setup`.
- Inputs (6): `company_name`, `freeform_deal_context`, `company_domain`, `source_object_url`, `source_thread_url`, `pitch_deck_artifact_id`.
- Outputs (3): `projectCreation`, `creation_summary`, `missing_creation_context`.

### `create-ic-memo`

- Template id: `vc.create_ic_memo`; version: `1.0.16`; family: `ic`; stage: `decision_review`.
- Inputs (11): `team_review_pack_artifact_id`, `partner_review_pack_artifact_id`, `commercial_evaluation_artifact_id`, `technical_evaluation_artifact_id`, `financial_evaluation_artifact_id`, `team_evaluation_artifact_id`, `diligence_question_bank_artifact_id`, `commercial_dd_artifact_id`, `financial_dd_artifact_id`, `founder_evaluation_artifact_id`, `technical_dd_artifact_id`.
- Outputs (1): `investment_memo_artifact_id`.
- Output-template refs: `investment_memo_artifact_id`.

### `discover-companies-house-candidates`

- Template id: `vc.discover_companies_house_candidates`; version: `0.1.5`; family: `origination_source_discovery`; stage: `source`.
- Inputs (1): `companies_house_discovery_scope`.
- Outputs (4): `companies_house_discovery_artifact_id`, `discovery_report`, `source_result_count`, `source_state_summary`.

### `discover-github-builder-signals`

- Template id: `vc.discover_github_builder_signals`; version: `0.1.4`; family: `origination_source_discovery`; stage: `source`.
- Inputs (1): `github_discovery_scope`.
- Outputs (4): `github_discovery_artifact_id`, `discovery_report`, `source_result_count`, `source_state_summary`.

### `discover-linkedin-founder-candidates`

- Template id: `vc.discover_linkedin_founder_candidates`; version: `0.1.5`; family: `origination_source_discovery`; stage: `source`.
- Inputs (1): `linkedin_discovery_scope`.
- Outputs (4): `linkedin_discovery_artifact_id`, `discovery_report`, `source_result_count`, `source_state_summary`.

### `discover-reddit-builder-signals`

- Template id: `vc.discover_reddit_builder_signals`; version: `0.1.4`; family: `origination_source_discovery`; stage: `source`.
- Inputs (1): `reddit_discovery_scope`.
- Outputs (4): `reddit_discovery_artifact_id`, `discovery_report`, `source_result_count`, `source_state_summary`.

### `discover-x-founder-signals`

- Template id: `vc.discover_x_founder_signals`; version: `0.1.5`; family: `origination_source_discovery`; stage: `source`.
- Inputs (1): `x_discovery_scope`.
- Outputs (4): `x_founder_discovery_artifact_id`, `discovery_report`, `source_result_count`, `source_state_summary`.

### `enrich-sourcing-candidate`

- Template id: `vc.enrich_sourcing_candidate`; version: `0.1.5`; family: `origination_enrichment`; stage: `enrich`.
- Inputs (1): `candidate_batch`.
- Outputs (4): `enrichment_artifact_id`, `enriched_candidate_count`, `enrichment_status`, `enrichment_report`.

### `generate-diligence-questions`

- Template id: `vc.generate_diligence_questions`; version: `1.0.20`; family: `diligence`; stage: `evaluation`.
- Inputs (4): `company_name`, `known_claims`, `existing_answers`, `priority_workstreams`.
- Outputs (1): `diligence_question_bank_artifact_id`.

### `generate-sourcing-digest`

- Template id: `vc.generate_sourcing_digest`; version: `0.1.9`; family: `origination_digest`; stage: `operate`.
- Inputs (1): `digest_scope`.
- Outputs (1): `sourcing_digest_artifact_id`.
- Output-template refs: `sourcing_digest_artifact_id`.

### `google-drive-discovery`

- Template id: `vc.google_drive_discovery`; version: `0.1.4`; family: `integration_discovery`; stage: `-`.
- Inputs (1): `discovery_goal`.
- Outputs (2): `google_drive_discovery_report`, `source_scope_questions`.

### `google-drive-setup`

- Template id: `vc.google_drive_setup`; version: `0.1.4`; family: `integration_setup`; stage: `-`.
- Inputs (1): `setup_goal`.
- Outputs (4): `setup_summary`, `accepted_connection_scope`, `child_task_plan`, `sync_policy`.

### `google-drive-sync-read`

- Template id: `vc.google_drive_sync_read`; version: `0.1.4`; family: `integration_sync_read`; stage: `-`.
- Inputs (1): `selected_google_drive_scope`.
- Outputs (2): `google_drive_context_preview`, `target_context_mapping`.

### `google-drive-sync-write`

- Template id: `vc.google_drive_sync_write`; version: `0.1.3`; family: `integration_sync_write`; stage: `-`.
- Inputs (1): `drive_write_source`.
- Outputs (1): `google_drive_write_proposals`.

### `harmonic-discovery`

- Template id: `vc.harmonic_discovery`; version: `0.1.3`; family: `integration_discovery`; stage: `-`.
- Inputs (1): `discovery_goal`.
- Outputs (2): `harmonic_discovery_report`, `source_scope_questions`.

### `harmonic-setup`

- Template id: `vc.harmonic_setup`; version: `0.1.4`; family: `integration_setup`; stage: `-`.
- Inputs (1): `setup_goal`.
- Outputs (4): `setup_summary`, `accepted_connection_scope`, `child_task_plan`, `sync_policy`.

### `harmonic-sync-read`

- Template id: `vc.harmonic_sync_read`; version: `0.1.4`; family: `integration_sync_read`; stage: `-`.
- Inputs (1): `selected_harmonic_scope`.
- Outputs (2): `harmonic_results_preview`, `target_context_mapping`.

### `ingest-manual-sourcing-tip`

- Template id: `vc.ingest_manual_sourcing_tip`; version: `0.1.4`; family: `origination_manual_tip`; stage: `source`.
- Inputs (1): `manual_tip`.
- Outputs (3): `manual_tip_ingestion_artifact_id`, `normalized_candidate_key`, `ingestion_report`.

### `manage-closing-checklist`

- Template id: `vc.manage_closing_checklist`; version: `1.0.14`; family: `closing`; stage: `closing`.
- Inputs (9): `ic_decision_record_artifact_id`, `term_sheet_review_artifact_id`, `closing_source_artifact_ids`, `legal_document_status`, `legal_diligence_artifact_id`, `investment_document_review_artifact_id`, `owners`, `deadlines`, `blockers`.
- Outputs (1): `closing_checklist_artifact_id`.
- Output-template refs: `closing_checklist_artifact_id`.

### `notion-discovery`

- Template id: `vc.notion_discovery`; version: `0.1.4`; family: `integration_discovery`; stage: `-`.
- Inputs (1): `discovery_goal`.
- Outputs (2): `notion_discovery_report`, `scope_questions`.

### `notion-setup`

- Template id: `vc.notion_setup`; version: `0.1.4`; family: `integration_setup`; stage: `-`.
- Inputs (1): `setup_goal`.
- Outputs (4): `setup_summary`, `accepted_connection_scope`, `child_task_plan`, `sync_policy`.

### `notion-sync-read`

- Template id: `vc.notion_sync_read`; version: `0.1.4`; family: `integration_sync_read`; stage: `-`.
- Inputs (1): `selected_notion_scope`.
- Outputs (2): `notion_context_preview`, `target_context_mapping`.

### `notion-sync-write`

- Template id: `vc.notion_sync_write`; version: `0.1.3`; family: `integration_sync_write`; stage: `-`.
- Inputs (1): `notion_write_source`.
- Outputs (1): `notion_update_proposals`.

### `prepare-deal-flow-agenda`

- Template id: `vc.prepare_deal_flow_agenda`; version: `1.0.8`; family: `pipeline`; stage: `evaluation`.
- Inputs (3): `pipeline_snapshot`, `meeting_date`, `stale_deal_threshold`.
- Outputs (5): `agenda`, `stale_deal_list`, `new_deal_list`, `stage_change_candidates`, `seven_day_action_plan`.

### `prepare-ic-agenda`

- Template id: `vc.prepare_ic_agenda`; version: `1.0.12`; family: `ic`; stage: `decision_review`.
- Inputs (1): `investment_memo_artifact_id`.
- Outputs (1): `ic_agenda_artifact_id`.
- Output-template refs: `ic_agenda_artifact_id`.

### `prepare-initial-linkedin-reachout`

- Template id: `vc.prepare_initial_linkedin_reachout`; version: `0.1.1`; family: `origination_outreach_drafts`; stage: `initial_reachout_linkedin`.
- Inputs (1): `initial_reachout_scope`.
- Outputs (2): `initial_linkedin_reachout_artifact_id`, `initial_reachout_draft_count`.
- Output-template refs: `initial_linkedin_reachout_artifact_id`.

### `prepare-lead-gen-packet`

- Template id: `vc.prepare_lead_gen_packet`; version: `1.0.16`; family: `pipeline`; stage: `source`.
- Inputs (3): `candidate_companies`, `meeting_date`, `thesis_context`.
- Outputs (1): `lead_generation_packet_artifact_id`.
- Output-template refs: `lead_generation_packet_artifact_id`.

### `prepare-meeting`

- Template id: `vc.prepare_meeting`; version: `1.0.14`; family: `meeting`; stage: `evaluation`.
- Inputs (5): `company_name`, `pitch_deck_artifact_id`, `founder_names`, `meeting_datetime`, `deal_room_url`.
- Outputs (1): `initial_call_brief_artifact_id`.
- Output-template refs: `initial_call_brief_artifact_id`.

### `prepare-outreach-draft-queue`

- Template id: `vc.prepare_outreach_draft_queue`; version: `0.1.9`; family: `origination_outreach_drafts`; stage: `engage`.
- Inputs (1): `outreach_scope`.
- Outputs (2): `outreach_queue_artifact_id`, `outreach_draft_count`.
- Output-template refs: `outreach_queue_artifact_id`.

### `prepare-partner-review-pack`

- Template id: `vc.prepare_partner_review_pack`; version: `1.0.17`; family: `diligence`; stage: `decision_review`.
- Inputs (10): `team_review_pack_artifact_id`, `commercial_evaluation_artifact_id`, `technical_evaluation_artifact_id`, `financial_evaluation_artifact_id`, `team_evaluation_artifact_id`, `diligence_question_bank_artifact_id`, `commercial_dd_artifact_id`, `financial_dd_artifact_id`, `founder_evaluation_artifact_id`, `technical_dd_artifact_id`.
- Outputs (1): `partner_review_pack_artifact_id`.
- Output-template refs: `partner_review_pack_artifact_id`.

### `prepare-portfolio-onboarding`

- Template id: `vc.prepare_portfolio_onboarding`; version: `1.0.13`; family: `onboarding`; stage: `closing`.
- Inputs (4): `ic_decision_record_artifact_id`, `closing_checklist_artifact_id`, `conditions_precedent_verification_artifact_id`, `completion_tracker_artifact_id`.
- Outputs (1): `portfolio_onboarding_plan_artifact_id`.
- Output-template refs: `portfolio_onboarding_plan_artifact_id`.

### `prepare-prospect-summary`

- Template id: `vc.prepare_prospect_summary`; version: `0.1.9`; family: `origination_prospect_summary`; stage: `review`.
- Inputs (1): `prospect_summary_candidate`.
- Outputs (1): `prospect_summary_artifact_id`.
- Output-template refs: `prospect_summary_artifact_id`.

### `prepare-second-reachout-email`

- Template id: `vc.prepare_second_reachout_email`; version: `0.1.1`; family: `origination_outreach_drafts`; stage: `second_reachout_email`.
- Inputs (1): `second_reachout_scope`.
- Outputs (2): `second_reachout_email_artifact_id`, `second_reachout_draft_count`.
- Output-template refs: `second_reachout_email_artifact_id`.

### `prepare-team-review-pack`

- Template id: `vc.prepare_team_review_pack`; version: `1.0.19`; family: `diligence`; stage: `decision_review`.
- Inputs (9): `commercial_evaluation_artifact_id`, `technical_evaluation_artifact_id`, `financial_evaluation_artifact_id`, `team_evaluation_artifact_id`, `diligence_question_bank_artifact_id`, `commercial_dd_artifact_id`, `financial_dd_artifact_id`, `founder_evaluation_artifact_id`, `technical_dd_artifact_id`.
- Outputs (1): `team_review_pack_artifact_id`.
- Output-template refs: `team_review_pack_artifact_id`.

### `promote-candidate-to-deal-pipeline`

- Template id: `vc.promote_candidate_to_deal_pipeline`; version: `0.1.10`; family: `origination_promotion`; stage: `promote`.
- Inputs (1): `promotion_candidate`.
- Outputs (1): `promotion_package_artifact_id`.
- Output-template refs: `promotion_package_artifact_id`.

### `record-ic-decision`

- Template id: `vc.record_ic_decision`; version: `1.0.13`; family: `ic`; stage: `decision_review`.
- Inputs (6): `investment_memo_artifact_id`, `ic_agenda_artifact_id`, `ic_transcript_or_notes`, `decision_options`, `conditions_discussed`, `attendees`.
- Outputs (1): `ic_decision_record_artifact_id`.
- Output-template refs: `ic_decision_record_artifact_id`.

### `record-linkedin-connection-attempt`

- Template id: `vc.record_linkedin_connection_attempt`; version: `0.1.1`; family: `origination_outbound_state`; stage: `connecting_on_linkedin`.
- Inputs (1): `connection_attempt`.
- Outputs (2): `connection_record_artifact_id`, `outbound_status`.
- Output-template refs: `connection_record_artifact_id`.

### `request-founder-materials`

- Template id: `vc.request_founder_materials`; version: `1.0.12`; family: `deal_room`; stage: `evaluation`.
- Inputs (4): `company_name`, `missing_materials`, `founder_contact`, `due_date`.
- Outputs (1): `founder_materials_request_artifact_id`.
- Output-template refs: `founder_materials_request_artifact_id`.

### `review-ic-memo`

- Template id: `vc.review_ic_memo`; version: `1.0.15`; family: `ic`; stage: `decision_review`.
- Inputs (2): `investment_memo_artifact_id`, `ic_agenda_artifact_id`.
- Outputs (1): `ic_memo_review_artifact_id`.
- Output-template refs: `ic_memo_review_artifact_id`.

### `review-investment-documents`

- Template id: `vc.review_investment_documents`; version: `0.1.3`; family: `contracts`; stage: `contracts`.
- Inputs (8): `investment_document_artifact_ids`, `term_sheet_review_artifact_id`, `negotiation_brief_artifact_id`, `legal_diligence_artifact_id`, `disclosure_letter_artifact_id`, `counsel_notes`, `cap_table_artifact_id`, `board_minutes_artifact_id`.
- Outputs (1): `investment_document_review_artifact_id`.
- Output-template refs: `investment_document_review_artifact_id`.

### `review-opportunity-status`

- Template id: `vc.review_opportunity_status`; version: `1.0.12`; family: `pipeline`; stage: `evaluation`.
- Inputs (4): `company_name`, `investment_stage`, `stage_snapshot`, `relevant_artifact_ids`.
- Outputs (4): `stage_summary`, `missing_inputs`, `stage_transition_recommendation`, `next_task_suggestions`.

### `review-outreach-outcome`

- Template id: `vc.review_outreach_outcome`; version: `0.1.1`; family: `origination_outbound_state`; stage: `outbound_outcome`.
- Inputs (1): `outreach_state`.
- Outputs (2): `outreach_outcome_artifact_id`, `recommended_terminal_state`.
- Output-template refs: `outreach_outcome_artifact_id`.

### `review-portfolio-overlap`

- Template id: `vc.review_portfolio_overlap`; version: `0.1.4`; family: `origination_portfolio_overlap`; stage: `review`.
- Inputs (1): `portfolio_overlap_scope`.
- Outputs (3): `portfolio_overlap_artifact_id`, `high_overlap_count`, `overlap_report`.

### `review-reddit-candidate-inbox`

- Template id: `vc.review_reddit_candidate_inbox`; version: `0.1.3`; family: `origination_reddit_approval`; stage: `review`.
- Inputs (1): `reddit_inbox_scope`.
- Outputs (4): `reddit_inbox_review_artifact_id`, `approved_candidate_count`, `needs_review_count`, `review_report`.

### `review-source-errors-and-spend`

- Template id: `vc.review_source_errors_and_spend`; version: `0.1.9`; family: `origination_source_health`; stage: `operate`.
- Inputs (1): `source_health_scope`.
- Outputs (2): `source_health_artifact_id`, `source_health_status`.
- Output-template refs: `source_health_artifact_id`.

### `review-term-sheet`

- Template id: `vc.review_term_sheet`; version: `1.0.13`; family: `closing`; stage: `deal_structuring`.
- Inputs (5): `term_sheet_artifact_id`, `deal_terms`, `standard_terms_reference`, `counsel_notes`, `deal_terms_analysis_artifact_id`.
- Outputs (1): `term_sheet_review_artifact_id`.
- Output-template refs: `term_sheet_review_artifact_id`.

### `review-unicorn-signature`

- Template id: `vc.review_unicorn_signature`; version: `0.1.0`; family: `origination_unicorn_signature`; stage: `review`.
- Inputs (1): `unicorn_signature_scope`.
- Outputs (3): `unicorn_signature_artifact_id`, `unicorn_signature_recommendation`, `unicorn_signature_report`.

### `run-commercial-dd`

- Template id: `vc.run_commercial_dd`; version: `1.0.18`; family: `diligence`; stage: `formal_diligence`.
- Inputs (6): `company_name`, `business_model`, `customer_or_user_evidence`, `go_to_market_evidence`, `pricing_or_revenue_evidence`, `market_sources`.
- Outputs (3): `commercial_dd_artifact_id`, `market_analysis_artifact_id`, `customer_reference_summary_artifact_id`.
- Output-template refs: `commercial_dd_artifact_id`.

### `run-commercial-evaluation`

- Template id: `vc.run_commercial_evaluation`; version: `0.1.1`; family: `evaluation`; stage: `evaluation`.
- Inputs (4): `company_name`, `follow_up_evaluation_artifact_id`, `opportunity_evidence_artifact_ids`, `customer_or_market_evidence`.
- Outputs (4): `commercial_evaluation_artifact_id`, `main_commercial_hypothesis`, `commercial_gating_risk`, `next_commercial_proof_needed`.
- Output-template refs: `commercial_evaluation_artifact_id`.

### `run-deal-fit-analysis`

- Template id: `vc.run_deal_fit_analysis`; version: `0.1.0`; family: `origination_deal_fit`; stage: `review`.
- Inputs (1): `deal_fit_scope`.
- Outputs (3): `deal_fit_artifact_id`, `deal_fit_ready_count`, `deal_fit_report`.

### `run-financial-dd`

- Template id: `vc.run_financial_dd`; version: `1.0.17`; family: `diligence`; stage: `formal_diligence`.
- Inputs (5): `financial_source_artifact_ids`, `business_model`, `cap_table`, `bank_statement_evidence`, `use_of_funds_plan`.
- Outputs (2): `financial_dd_artifact_id`, `unit_economics_artifact_id`.
- Output-template refs: `financial_dd_artifact_id`, `unit_economics_artifact_id`.

### `run-financial-evaluation`

- Template id: `vc.run_financial_evaluation`; version: `0.1.1`; family: `evaluation`; stage: `evaluation`.
- Inputs (4): `company_name`, `follow_up_evaluation_artifact_id`, `opportunity_evidence_artifact_ids`, `financial_or_financing_evidence`.
- Outputs (4): `financial_evaluation_artifact_id`, `main_financial_hypothesis`, `financial_gating_risk`, `next_financial_proof_needed`.
- Output-template refs: `financial_evaluation_artifact_id`.

### `run-founder-evaluation`

- Template id: `vc.run_founder_evaluation`; version: `1.0.16`; family: `diligence`; stage: `formal_diligence`.
- Inputs (3): `founder_names`, `founder_profiles`, `reference_inputs`.
- Outputs (1): `founder_evaluation_artifact_id`.
- Output-template refs: `founder_evaluation_artifact_id`.

### `run-investment-fit-screen`

- Template id: `vc.run_investment_fit_screen`; version: `1.0.18`; family: `screening`; stage: `screening`.
- Inputs (6): `company_name`, `pitch_deck_artifact_id`, `meeting_notes`, `source_links`, `opportunity_intake_artifact_id`, `source_material_artifact_ids`.
- Outputs (2): `investment_screen_scorecard_artifact_id`, `overall_recommendation`.

### `run-legal-diligence`

- Template id: `vc.run_legal_diligence`; version: `0.1.4`; family: `diligence`; stage: `formal_diligence`.
- Inputs (7): `legal_source_artifact_ids`, `company_name`, `counsel_requirements`, `ip_artifact_ids`, `corporate_structure_artifact_id`, `employment_contract_artifact_ids`, `litigation_search_artifact_ids`.
- Outputs (1): `legal_diligence_artifact_id`.
- Output-template refs: `legal_diligence_artifact_id`.

### `run-opportunity-evaluation`

- Template id: `vc.run_opportunity_evaluation`; version: `1.0.16`; family: `evaluation`; stage: `evaluation`.
- Inputs (3): `company_name`, `investment_screen_scorecard_artifact_id`, `customer_insights_artifact_id`.
- Outputs (1): `follow_up_evaluation_artifact_id`.
- Output-template refs: `follow_up_evaluation_artifact_id`.

### `run-team-evaluation`

- Template id: `vc.run_team_evaluation`; version: `0.1.1`; family: `evaluation`; stage: `evaluation`.
- Inputs (4): `company_name`, `follow_up_evaluation_artifact_id`, `opportunity_evidence_artifact_ids`, `team_or_founder_evidence`.
- Outputs (4): `team_evaluation_artifact_id`, `main_team_hypothesis`, `team_gating_risk`, `next_team_proof_needed`.
- Output-template refs: `team_evaluation_artifact_id`.

### `run-technical-dd`

- Template id: `vc.run_technical_dd`; version: `1.0.15`; family: `diligence`; stage: `formal_diligence`.
- Inputs (5): `technical_source_artifact_ids`, `repo_or_code_access`, `product_roadmap`, `ip_patent_materials`, `engineering_team_materials`.
- Outputs (1): `technical_dd_artifact_id`.
- Output-template refs: `technical_dd_artifact_id`.

### `run-technical-evaluation`

- Template id: `vc.run_technical_evaluation`; version: `0.1.1`; family: `evaluation`; stage: `evaluation`.
- Inputs (4): `company_name`, `follow_up_evaluation_artifact_id`, `opportunity_evidence_artifact_ids`, `product_or_technical_evidence`.
- Outputs (4): `technical_evaluation_artifact_id`, `main_technical_hypothesis`, `technical_gating_risk`, `next_technical_proof_needed`.
- Output-template refs: `technical_evaluation_artifact_id`.

### `run-vc-sourcing-pipeline`

- Template id: `vc.run_vc_sourcing_pipeline`; version: `0.1.14`; family: `origination_pipeline_run`; stage: `source`.
- Inputs (2): `sourcing_run_scope`, `run_mode`.
- Outputs (7): `run_status`, `new_candidates_count`, `promotion_ready_count`, `run_completed_at`, `run_receipt_artifact_id`, `candidate_batch_artifact_id`, `source_state_artifact_id`.
- Output-template refs: `candidate_batch_artifact_id`.

### `score-sourcing-candidate`

- Template id: `vc.score_sourcing_candidate`; version: `0.1.10`; family: `origination_scoring`; stage: `score`.
- Inputs (2): `enriched_candidate_batch`, `scoring_policy`.
- Outputs (5): `scoring_artifact_id`, `meet_candidate_count`, `watch_candidate_count`, `promotion_ready_count`, `scoring_report`.

### `screen-active-sourcing-candidate`

- Template id: `vc.screen_active_sourcing_candidate`; version: `0.1.12`; family: `origination_screening`; stage: `review`.
- Inputs (1): `screening_scope`.
- Outputs (3): `screening_artifact_id`, `promotion_ready_count`, `screening_report`.

### `screen-founder-connected-candidate`

- Template id: `vc.screen_founder_connected_candidate`; version: `0.1.2`; family: `origination_founder_connected_screening`; stage: `engage`.
- Inputs (2): `founder_connection_context`, `prior_screen_context`.
- Outputs (2): `founder_connected_screen_artifact_id`, `founder_connected_screen_recommendation`.
- Output-template refs: `(no outputFieldKey)`.

### `screen-identified-candidate`

- Template id: `vc.screen_identified_candidate`; version: `0.1.1`; family: `origination_screening`; stage: `review`.
- Inputs (2): `identified_candidate_batch`, `first_pass_screen_policy`.
- Outputs (5): `identified_screen_artifact_id`, `outreach_ready_count`, `watchlist_count`, `pass_count`, `identified_screen_report`.

### `slack-discovery`

- Template id: `vc.slack_discovery`; version: `0.1.3`; family: `integration_discovery`; stage: `-`.
- Inputs (1): `discovery_goal`.
- Outputs (2): `slack_discovery_report`, `channel_scope_questions`.

### `slack-setup`

- Template id: `vc.slack_setup`; version: `0.1.4`; family: `integration_setup`; stage: `-`.
- Inputs (1): `setup_goal`.
- Outputs (4): `setup_summary`, `accepted_connection_scope`, `child_task_plan`, `sync_policy`.

### `slack-sync-read`

- Template id: `vc.slack_sync_read`; version: `0.1.4`; family: `integration_sync_read`; stage: `-`.
- Inputs (1): `selected_slack_scope`.
- Outputs (2): `slack_context_preview`, `target_context_mapping`.

### `slack-sync-write`

- Template id: `vc.slack_sync_write`; version: `0.1.3`; family: `integration_sync_write`; stage: `-`.
- Inputs (1): `handoff_source`.
- Outputs (1): `slack_handoff_draft`.

### `source-thesis-targets`

- Template id: `vc.source_thesis_targets`; version: `1.0.14`; family: `pipeline`; stage: `source`.
- Inputs (4): `thesis_area`, `geography`, `stage_focus`, `market_filters`.
- Outputs (1): `thesis_target_list_artifact_id`.
- Output-template refs: `thesis_target_list_artifact_id`.

### `summarize-meeting-records`

- Template id: `vc.summarize_meeting_records`; version: `1.0.14`; family: `meeting`; stage: `evaluation`.
- Inputs (4): `meeting_record_artifact_ids`, `meeting_notes`, `company_name`, `deal_room_url`.
- Outputs (1): `customer_insights_artifact_id`.
- Output-template refs: `customer_insights_artifact_id`.

### `sync-sourcing-candidate`

- Template id: `vc.sync_sourcing_candidate`; version: `0.1.4`; family: `origination_candidate_sync`; stage: `review`.
- Inputs (1): `sync_scope`.
- Outputs (3): `sync_plan_artifact_id`, `sync_status`, `sync_report`.

### `track-term-sheet-negotiation`

- Template id: `vc.track_term_sheet_negotiation`; version: `0.1.1`; family: `deal_structuring`; stage: `deal_structuring`.
- Inputs (7): `term_sheet_artifact_id`, `current_open_terms`, `ic_constraints`, `founder_comments_or_redline`, `counsel_notes`, `cap_table_artifact_id`, `deal_terms_analysis_artifact_id`.
- Outputs (1): `negotiation_brief_artifact_id`.
- Output-template refs: `negotiation_brief_artifact_id`.

### `vc-pack-variable-discovery`

- Template id: `vc.vc_pack_variable_discovery`; version: `1.0.3`; family: `pack_setup`; stage: `setup`.
- Inputs (3): `declared_variables`, `current_answers`, `workspace_context`.
- Outputs (3): `summary`, `variable_answers`, `invite_candidates`.

### `verify-conditions-precedent`

- Template id: `vc.verify_conditions_precedent`; version: `1.0.13`; family: `closing`; stage: `closing`.
- Inputs (4): `closing_checklist_artifact_id`, `closing_source_artifact_ids`, `counsel_requirements`, `closing_status`.
- Outputs (1): `conditions_precedent_verification_artifact_id`.
- Output-template refs: `conditions_precedent_verification_artifact_id`.
