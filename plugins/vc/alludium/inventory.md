# Alludium VC Inventory

**Version**: 0.5.39
**Status**: Shared HTML artifact token and structure guidance

This inventory describes the current public VC plugin/pack seed plus the draft project-type and metadata expansion. Version numbers track pack release slices that need platform alignment, so this history only lists versions that introduced durable pack-surface changes. Version `0.1.0` contains VC skills, Alludium runtime agent templates, public-safe MCP definitions, and Alludium MCP recommendations. Version `0.2.2` adds VC task-definition templates and advertises both the canonical `venture_capital` vertical key and legacy `vc` alias. Version `0.3.0` adds the Deal Pipeline project type as a first-class pack surface. Version `0.3.1` adds the Deal Pipeline command-view metadata used by the project command center. Version `0.3.2` adds workspace variable declarations and application recommendation metadata for the paired platform ingest work. Version `0.3.4` aligns agent Deal Pipeline states with the collapsed lifecycle and tightens required task-input mappings. Version `0.3.5` adds compact Affinity and Slack management-action metadata plus focused integration-specific discovery and sync task templates and skills. Version `0.3.6` extends the same integration-management surface to Google Drive, Notion, and Harmonic, with Harmonic limited to discovery/read-preview until trusted tool rows exist. Version `0.3.7` grants all VC runtime agent templates access to the platform text-artifact creation tool and collapses recommendation-level integration actions to one setup task per integration; each setup task declares its own discovery/read/write child task plan. Version `0.4.0` adds the Origination Pipeline project type, Apify and Companies House setup/readiness tasks, scheduled sourcing task definitions, compact origination project data mappings, and supporting origination skills. Version `0.4.1` validates project manager overlays. Version `0.4.2` adds generated agent Markdown compatibility artifacts and task prompt Markdown derived from the existing Alludium YAML source of truth. Version `0.5.0` adds the Deal Pipeline Setup Guide agent, routes Affinity setup toward agent-led discovery, mapping, and seed review, and declares schedulable VC tasks for project setup orchestration. Version `0.5.1` removes task-definition template turn caps so platform defaults can control agent execution budgets. Version `0.5.2` adds pack-owned project setup entrypoint metadata for VC project types. Version `0.5.3` makes project setup steps, schedule groups, and post-approval platform actions explicit in the project type definitions, adds the project-scoped Affinity Deal Pipeline import task, keeps Origination setup distinct from Deal Pipeline import, and adds pack-native methodology, SOP, checklist, and template documents for Deal Pipeline and Origination project types. Version `0.5.4` tightens document-template semantics, adds missing authored-document refs, and generalizes legacy screening and diligence methodology skill IDs. Version `0.5.5` bumps the Affinity read-sync task template after content changed so platform ingest can create a new template version. Version `0.5.6` adds a separate `projectCreation` contract for launching individual Deal Pipeline and Origination Pipeline project instances, removes legacy CRM URL fields, and moves origination setup configuration into declared workspace variables. Version `0.5.7` removes `systemUseOnly` from external task-template YAML and treats system-only task visibility as platform-owned authority. Version `0.5.8` normalizes workspace variable select options to the platform object shape and validates that shape in the pack release checks. Version `0.5.9` switches all VC runtime agent templates from Claude Opus 4.6 to Claude Sonnet 4.6 on Bedrock and bumps each agent template version so platform ingest creates a new template version. Version `0.5.10` restores project-manager identity overlays for VC project type versions and validates the overlay contract in release checks. Version `0.5.13` adds focused commercial, technical, financial, and team evaluation skills, output templates, task definitions, and Deal Pipeline/review-pack wiring so decision review can use evaluation-stage outputs before formal diligence. Version `0.5.14` adds project data fields and task mappings for focused evaluation workstream inputs and structured summary outputs. Version `0.5.15` adds generated project blueprint Markdown for each project type. Version `0.5.16` labels platform-owned setup tasks in generated project blueprints with their canonical platform task IDs. Version `0.5.17` splits generated project blueprints into Setup, General, Management, and lifecycle-stage sections. Version `0.5.18` adds a dedicated Evaluation Analyst agent, routes evaluation-stage task templates to it, and moves founder-material requests into the generated General blueprint section. Version `0.5.19` adds focused Integration Operator and Sourcing Operator agents, routes provider integration and origination operations tasks away from generic agents, and promotes screening/evaluation methodology skills into required task contracts where they are task-critical. Version `0.5.21` reconciles the branch with mainline Sonnet 4.6 agent models and project-manager identity overlays while preserving the expanded VC lifecycle, task, agent, and blueprint contracts. Version `0.5.22` adds Deal Pipeline company logo and founder identity fields plus Affinity import guidance for CRM-sourced founder profiles. Version `0.5.23` renames the public Deal Pipeline and Origination Pipeline surfaces, narrows Deal Pipeline to intake through deal structuring, moves thesis sourcing to Origination, adds the downstream execution project type for formal diligence through closing, and expands generated project blueprints with documents and integrations. Version `0.5.24` adds explicit origination outbound lifecycle states and task templates for LinkedIn connection, initial LinkedIn reachout, second-touch email, and outbound outcome review. Version `0.5.25` splits guided Deal Pipeline project creation from post-create opportunity intake so inbox/chat creation can hand structured data to a separate intake hydration task. Version `0.5.26` trims high-noise VC task output surfaces so artifact-backed tasks expose durable artifacts plus concise status fields instead of duplicating document detail in task UI outputs. Version `0.5.27` removes pack-level LLM configs from VC runtime agent templates so workspace-level LLM settings remain authoritative unless a future agent explicitly needs a dedicated model. Version `0.5.28` scopes Affinity to Deal Execution while removing the copied Deal Pipeline Affinity setup requirement from Deal Execution setup. Version `0.5.29` narrows Deal Pipeline intake to supplied or approved source readiness, removes public-web research from intake, renames Investment Management to Deal Execution, and leaves investment scoring and external research to screening. Version `0.5.30` adds HTML rendered-artifact contracts for selected VC output templates. Version `0.5.31` makes the Opportunity Intake Readiness Summary conditional so missing-source intake runs stay interactive until a source anchor is supplied or a human approves a partial artifact. Version `0.5.32` bumps the Deal Pipeline project type version after release content changed so platform ingest can create a new project type version. Version `0.5.33` requires attached pitch decks to be inspected or marked unreadable before they can count as intake readiness evidence; version `0.5.34` requires supplied CRM/source record anchors to be read before intake readiness decisions and adds company-claimed-fact source precedence so founder/company materials remain primary over public web research with conflicts surfaced; version `0.5.36` adds executive-summary and at-a-glance overview guidance to Deal Pipeline HTML output templates so generated documents surface the decision-critical view before full detail; version `0.5.38` adds a shared VC HTML artifact contract, makes the intake readiness Executive Summary mandatory by exact heading, improves safe-preview spacing guidance, keeps detailed field maps/source indexes out of structured task output fields, and notes that historical richtext intake output values may need manual review only where workspaces depend on the new compact summaries; version `0.5.39` tightens VC HTML artifact token aliases, shared structural classes, status badges, and pre-save QA guidance for evaluation and diligence outputs.

---

## Included Skills

These skills are included because the current `vc_*` Alludium agent templates reference them directly.

- `citation-enforcement`
- `closing-coordination-and-cp-tracking`
- `commercial-diligence-workstream`
- `commercial-evaluation-and-market-risk`
- `company-research-and-enrichment`
- `deal-terms-analysis`
- `deal-pipeline-setup-and-source-ingestion`
- `financial-diligence-workstream`
- `financial-evaluation-and-financing-risk`
- `founder-evaluation-and-reference-checking`
- `founder-materials-request`
- `founder-outreach-and-intro-paths`
- `ic-memo-assembly`
- `ic-risk-checklist-and-decision-log`
- `investment-diligence-question-framework`
- `investment-screening-framework`
- `legal-diligence-coordination`
- `market-map-building`
- `meeting-prep-and-summary`
- `pipeline-health-and-crm-hygiene`
- `pitch-deck-explainer`
- `portfolio-onboarding-and-100-day-plan`
- `red-flags-scanner`
- `team-and-hiring-assessment`
- `team-evaluation-and-founder-risk`
- `term-sheet-negotiation-brief`
- `technical-diligence-workstream`
- `technical-evaluation-and-product-risk`
- `traction-and-saas-unit-economics`
- `vc-task-and-next-step-generation`
- `vc-affinity-discovery`
- `vc-affinity-deal-pipeline-import`
- `vc-affinity-sync-read`
- `vc-affinity-sync-write`
- `vc-slack-discovery`
- `vc-slack-sync-read`
- `vc-slack-sync-write`
- `vc-google-drive-discovery`
- `vc-google-drive-sync-read`
- `vc-google-drive-sync-write`
- `vc-notion-discovery`
- `vc-notion-sync-read`
- `vc-notion-sync-write`
- `vc-harmonic-discovery`
- `vc-harmonic-sync-read`

Review notes:

- This is a template-required inventory, not a complete public-capability taxonomy.
- Broader reusable skills can move into another public plugin later if they do not belong in the VC vertical.
- `brand_monitoring_analysis` and `people_company_research_brief` were considered during planning but are intentionally deferred because no current `vc_*` agent template references them.
- No `internalOnly: true` skills are included.

---

## Included Alludium Agent Templates

- `vc_dealflow_concierge`
- `vc_diligence_analyst`
- `vc_first_look_analyst`
- `vc_ic_prep_producer`
- `vc_legal_compliance_desk`
- `vc_meeting_operator`
- `vc_origination_scout`
- `vc_pipeline_autopilot`
- `vc_deal_room_setup_guide`

Review notes:

- These templates are Alludium runtime templates, not Claude Code subagent definitions.
- The generated `agents/*.md` files are Markdown compatibility artifacts for external agentic tools; `alludium/agent-templates/*.yaml` remains the source of truth.
- Template `metadata.gitRepositoryUrl` values currently point at the configurable-agent implementation repository. That is runtime implementation metadata, not this pack's source provenance.
- Source provenance for this pack should be recorded by Alludium ingestion from repo, tag, commit SHA, and file path.

---

## Included Task Definition Templates

These templates are included because the platform VC workspace pack currently references them as installable VC workflow templates.

- `vc.create_ic_memo`
- `vc.generate_diligence_questions`
- `vc.manage_closing_checklist`
- `vc.prepare_deal_flow_agenda`
- `vc.create_deal`
- `vc.prepare_ic_agenda`
- `vc.prepare_meeting`
- `vc.prepare_lead_gen_packet`
- `vc.prepare_partner_review_pack`
- `vc.prepare_portfolio_onboarding`
- `vc.prepare_team_review_pack`
- `vc.record_ic_decision`
- `vc.analyze_deal_terms`
- `vc.track_term_sheet_negotiation`
- `vc.request_founder_materials`
- `vc.review_opportunity_status`
- `vc.review_ic_memo`
- `vc.review_term_sheet`
- `vc.run_legal_diligence`
- `vc.review_investment_documents`
- `vc.run_commercial_dd`
- `vc.run_financial_dd`
- `vc.run_opportunity_evaluation`
- `vc.run_founder_evaluation`
- `vc.run_technical_dd`
- `vc.run_investment_fit_screen`
- `vc.capture_opportunity_intake`
- `vc.source_thesis_targets`
- `vc.summarize_meeting_records`
- `vc.verify_conditions_precedent`
- `vc.coordinate_capital_call_and_completion`
- `vc.affinity_setup`
- `vc.affinity_discovery`
- `vc.affinity_sync_read`
- `vc.affinity_deal_room_import`
- `vc.affinity_sync_write`
- `vc.slack_setup`
- `vc.slack_discovery`
- `vc.slack_sync_read`
- `vc.slack_sync_write`
- `vc.google_drive_setup`
- `vc.google_drive_discovery`
- `vc.google_drive_sync_read`
- `vc.google_drive_sync_write`
- `vc.notion_setup`
- `vc.notion_discovery`
- `vc.notion_sync_read`
- `vc.notion_sync_write`
- `vc.harmonic_setup`
- `vc.harmonic_discovery`
- `vc.harmonic_sync_read`

Review notes:

- The generated `tasks/*.md` files are prompt/instruction compatibility artifacts for external agentic tools; task-definition YAML remains the source of truth.
- Task-definition YAML must not declare `systemUseOnly`; platform-owned ingest policy controls any system-only task visibility.
- Task templates remain unavailable to the platform until the paired platform PR teaches external pack ingest to stage and apply this surface.
- The task-template catalog preserves the current platform `vc-workflows` pack metadata, template IDs, and template versions while advertising both supported vertical keys: `venture_capital` and `vc`.
- Platform eligibility is driven by catalog `verticalKeys`, which the platform loader persists to `task_definitions.vertical_keys`; the per-template `definitionJson.vertical: vc` field remains legacy workflow metadata and is not used for workspace eligibility checks.
- The task-template surface requires platform capability `external-task-definition-template-ingest`.
- Task templates advertise `vc_deal_room`, `vc_origination_pipeline`, `vc_investment_management`, or a combination according to their declared workflow scope; all three project types are now included in this pack's `projectTypes` surface.
- Task templates without `supportedProjectScopes` are single-project `project_instance` tasks. Templates with `project_management` scope support pipeline, admin, or project-type management work and keep outputs on the task or future management surface unless an explicit management mapping is introduced.
- The integration templates are application-specific `project_management` tasks. Each integration now exposes one setup task (`vc.*_setup`) in recommendation metadata. That setup task owns the discovery/read/write child task references and approval policy; the lower-level discovery, read-preview, and write-proposal templates remain available as setup-owned child tasks rather than direct application-card actions.

---

## Included Project Types

- `vc_deal_room`
- `vc_origination_pipeline`
- `vc_investment_management`

Review notes:

- `vc_deal_room` covers one investment opportunity from source capture through deal structuring and now keeps version `1.1.2`.
- `vc_origination_pipeline` captures upstream sourcing, candidate engagement, and candidate promotion as a separate project type and now keeps version `0.2.3`.
- `vc_investment_management` is user-facing as Deal Execution, covers formal diligence, contracts, closing, completion, and portfolio handoff after Deal Pipeline deal structuring, and now keeps version `0.1.2`.
- Generated project blueprints live in `project-blueprints/` and show each project type's setup/general tasks plus lifecycle-stage task mappings, recommended agents, and task-referenced skills. Platform-owned setup tasks are labeled with their canonical platform task IDs.
- The definitions include project fields, instruction templates, lifecycle states, lifecycle transitions, command-view metadata, project-manager identity overlays, conservative `projectTaskMappings`, pack-owned `projectSetup` metadata, project-type document references, and separate `projectCreation` metadata for one-project launchers.
- Deal Pipeline setup declares source, variables, schedules, and invite steps plus post-approval platform actions for applying variables, creating/importing Deal Pipeline projects, inviting approved collaborators, and enabling approved schedules. Origination setup declares source, variables, and schedules plus post-approval platform actions for applying variables and enabling approved schedules; it does not declare initial import or invite actions.
- Deal Pipeline creation starts from `company_name`, with domain, deal source, stage, lead partner, pitch deck, and confidentiality as recommended creation fields. Connected CRM source records render through `projectCreation.sourceReference` and map into the lower-level source fields. Origination creation stays separate from Deal Pipeline creation and starts from `pipeline_name`; the only optional creation input is confidentiality, owner should default to the current user or platform actor, and firm/fund identity, thesis, focus, source selection, cadence, budget, thresholds, digest destination, and workspace links belong to setup variables.
- The project-type surface requires platform capability `external-project-type-ingest`.
- Expanded lifecycle-stage task mappings remain declarative, manual-review mappings for direct project-backed inputs and required artifact outputs. The new `projectCreation.postCreate.triggerInitialStateTasks` flag is an explicit platform-launcher intent, separate from project setup.

---

## Included Project Type Documents

The document surface lives at `alludium/documents/catalog.v1.json` with Markdown source files under `alludium/documents`. It is a pack-native source surface for methodology, SOPs, checklists, templates, and style guidance. Project types reference documents through `initialVersion.documentLibrary.documentIds`; task templates reference them through durable `definitionJson.documentRefs` entries and output-field `config.documentRefId` values when an artifact should be produced from a pack document. Platform runtime support is intentionally not implemented in this pack.

Included shared documents:

- `vc.document.investment_screening_framework`
- `vc.document.investment_diligence_question_framework`
- `vc.document.evidence_citation_style_guide`
- `vc.document.file_naming_source_index_sop`

Included Deal Pipeline documents:

- `vc.document.deal_room_sop`
- `vc.document.founder_materials_request_template`
- `vc.document.investment_memo_template`
- `vc.document.ic_agenda_template`
- `vc.document.ic_decision_record_template`
- `vc.document.diligence_report_template`
- `vc.document.review_pack_checklist`
- `vc.document.deal_terms_analysis_template`
- `vc.document.term_sheet_negotiation_brief_template`
- `vc.document.term_sheet_review_template`
- `vc.document.legal_diligence_tracker_template`
- `vc.document.investment_document_review_template`
- `vc.document.closing_checklist`
- `vc.document.conditions_precedent_tracker_template`
- `vc.document.completion_tracker_template`
- `vc.document.portfolio_onboarding_plan_template`

Included Origination documents:

- `vc.document.origination_pipeline_sop`
- `vc.document.source_registry_template`
- `vc.document.candidate_batch_template`
- `vc.document.sourcing_scoring_rubric`
- `vc.document.source_health_review_checklist`
- `vc.document.paid_source_spend_audit_checklist`
- `vc.document.sourcing_digest_template`
- `vc.document.outreach_queue_template`
- `vc.document.promotion_package_template`
- `vc.document.dedupe_novelty_policy`
- `vc.document.apify_source_setup_checklist`
- `vc.document.companies_house_source_setup_checklist`

---

## MCP Definitions And Platform Mapping

The first scaffold includes public-safe plugin MCP definitions in `.mcp.json` and VC application recommendations in `alludium/mcp-recommendations.yaml`. The recommendations file remains the platform-mapping surface: records use `externalId`, `name`, and the mapping fields (`pluginCredentialBoundary`, `alludiumPlatformMapping`, `platformDefaultAvailable`) for MCP-backed entries. Records that should also appear in the application picker add `recommendationStatus` and an `applicationRecommendation` metadata block on the same record so there is no second source of truth.

Included MCP IDs:

- `affinity-mcp-server`
- `harmonic-mcp-oauth`
- `dealroom-mcp`
- `exa-mcp-hosted`
- `firecrawl-mcp-hosted`
- `brave-search-mcp`
- `serpapi-mcp`
- `tavily-mcp-hosted`
- `perplexity-mcp`
- `brightdata-mcp-hosted`
- `meltwater-mcp`
- `granola-mcp`
- `otter-mcp-oauth`
- `fireflies-mcp-oauth`

Application-only integration IDs used by standardized recommendation actions:

- `slack_v2`
- `google_drive`
- `notion`

Standardized setup actions:

- `affinity-mcp-server`: declares one `setup` action pointing at `vc.affinity_setup`; that setup task owns the Affinity discovery, read-preview, and write-proposal child task references.
- `slack_v2`: declares one `setup` action pointing at `vc.slack_setup`; that setup task owns the Slack discovery, read-preview, and notification-proposal child task references.
- `google_drive`: declares one `setup` action pointing at `vc.google_drive_setup`; that setup task owns the Google Drive discovery, read-preview, and file-proposal child task references.
- `notion`: declares one `setup` action pointing at `vc.notion_setup`; that setup task owns the Notion discovery, read-preview, and update-proposal child task references.
- `harmonic-mcp-oauth`: declares one `setup` action pointing at `vc.harmonic_setup`; that setup task owns the Harmonic discovery and read-preview child task references. No write child task is declared because no current write/update surface is trusted.

Review notes:

- `.mcp.json` uses user/workspace credential placeholders, not Alludium platform secrets.
- `alludium/mcp-recommendations.yaml` records how Alludium can map the same external IDs to platform defaults or workspace connections when the pack is ingested.
- Slack uses the platform application external ID `slack_v2`, not the informal `slack` label, because pack recommendation keys must match `applications.external_id`.
- Google Drive uses the platform application external ID `google_drive` and current Pipedream tool IDs such as `google_drive-search-shared-drives`, `google_drive-list-files`, `google_drive-get-file-by-id`, and `google_drive-download-file`.
- Notion uses the platform application external ID `notion` and current Pipedream tool IDs such as `notion-search`, `notion-retrieve-page`, `notion-retrieve-block`, `notion-retrieve-database-schema`, `notion-retrieve-database-content`, and `notion-query-database`.
- Affinity currently has the application record `affinity-mcp-server`; connection-backed tool discovery is still required before live tool rows can be relied on in this pack.
- Harmonic currently has the application record `harmonic-mcp-oauth` and an active OAuth connection template, but no live tool rows in the local platform catalog; Harmonic task templates must report that gap until tool discovery after authorization succeeds.
- Alludium template references to `alludium-platform`, `google_drive`, and `linkedin` are tracked as platform-only/template-only integrations rather than plugin MCP definitions.
- Pipedream-provided integrations remain excluded from `.mcp.json`; Slack is represented as application-only recommendation metadata keyed by `slack_v2`.
- `alludium-docs-mcp` and `xero-mcp-server` exist in platform MCP config but are intentionally excluded because they are not part of the first VC workflow surface.
- No secrets, tokens, or environment-specific values should be copied into this public repo.

---

## Workspace Variable Declarations

The VC pack declares public-safe workspace variable definitions in `alludium/workspace-variables.yaml`.

Included workspace variables:

- `vc.fundStage`
- `vc.fundSectors`
- `vc.fundGeography`
- `vc.fundThesis`
- `vc.scoringFramework`
- `vc.firmName`
- `vc.fundName`
- `vc.originationEnabledSources`
- `vc.originationRunCadence`
- `vc.originationDigestDestination`
- `vc.originationSourceCostBudget`
- `vc.originationPromotionThreshold`
- `vc.originationManualReviewThreshold`
- `vc.originationCrmPipelineUrl`
- `vc.originationDocumentWorkspaceUrl`

Review notes:

- These declarations define workspace-owned facts only; they do not contain firm-specific values.
- Platform ingestion should attach pack provenance while leaving variable values owned by the workspace variable substrate.

---

Workspace activation:

- deferred until the platform has a clear pack activation service and UX owner
- expected owners may include Workspace Setup, Project Manager, or admin tooling using one underlying activation service
