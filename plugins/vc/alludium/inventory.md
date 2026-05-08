# Alludium VC Inventory

**Version**: 0.3.6
**Status**: Draft project-type and metadata expansion

This inventory describes the current public VC plugin/pack seed plus the draft project-type and metadata expansion. Version numbers track pack release slices that need platform alignment, so this history only lists versions that introduced durable pack-surface changes. Version `0.1.0` contains VC skills, Alludium runtime agent templates, public-safe MCP definitions, and Alludium MCP recommendations. Version `0.2.2` adds VC task-definition templates and advertises both the canonical `venture_capital` vertical key and legacy `vc` alias. Version `0.3.0` adds the VC Deal Room project type as a first-class pack surface. Version `0.3.1` adds the VC Deal Room command-view metadata used by the project command center. Version `0.3.2` adds workspace variable declarations and application recommendation metadata for the paired platform ingest work. Version `0.3.4` aligns agent Deal Room states with the collapsed lifecycle and tightens required task-input mappings. Version `0.3.5` adds compact Affinity and Slack management-action metadata plus focused integration-specific discovery and sync task templates and skills. Version `0.3.6` extends the same integration-management surface to Google Drive, Notion, and Harmonic, with Harmonic limited to discovery/read-preview until trusted tool rows exist.

---

## Included Skills

These skills are included because the current `vc_*` Alludium agent templates reference them directly.

- `82-factor-diligence-question-generation`
- `citation-enforcement`
- `closing-coordination-and-cp-tracking`
- `commercial-diligence-workstream`
- `company-research-and-enrichment`
- `deal-room-setup-and-source-ingestion`
- `financial-diligence-workstream`
- `founder-evaluation-and-reference-checking`
- `founder-materials-request`
- `founder-outreach-and-intro-paths`
- `ic-memo-assembly`
- `ic-risk-checklist-and-decision-log`
- `market-map-building`
- `meeting-prep-and-summary`
- `pipeline-health-and-crm-hygiene`
- `pitch-deck-explainer`
- `portfolio-onboarding-and-100-day-plan`
- `red-flags-scanner`
- `team-and-hiring-assessment`
- `technical-diligence-workstream`
- `ten-factor-evaluation`
- `traction-and-saas-unit-economics`
- `vc-task-and-next-step-generation`
- `vc-affinity-discovery`
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

Review notes:

- These templates are Alludium runtime templates, not Claude Code subagent definitions.
- Template `metadata.gitRepositoryUrl` values currently point at the configurable-agent implementation repository. That is runtime implementation metadata, not this pack's source provenance.
- Source provenance for this pack should be recorded by Alludium ingestion from repo, tag, commit SHA, and file path.

---

## Included Task Definition Templates

These templates are included because the platform VC workspace pack currently references them as installable VC workflow templates.

- `vc.create_ic_memo`
- `vc.generate_82_factor_questions`
- `vc.manage_closing_checklist`
- `vc.prepare_deal_flow_agenda`
- `vc.prepare_ic_agenda`
- `vc.prepare_initial_call`
- `vc.prepare_lead_gen_packet`
- `vc.prepare_partner_review_pack`
- `vc.prepare_portfolio_onboarding`
- `vc.prepare_team_review_pack`
- `vc.record_ic_decision`
- `vc.request_founder_materials`
- `vc.review_opportunity_status`
- `vc.review_ic_memo`
- `vc.review_term_sheet`
- `vc.run_commercial_dd`
- `vc.run_financial_dd`
- `vc.run_follow_up_evaluation`
- `vc.run_founder_evaluation`
- `vc.run_technical_dd`
- `vc.run_ten_factor_screen`
- `vc.screen_inbound_opportunity`
- `vc.source_thesis_targets`
- `vc.summarize_initial_call`
- `vc.verify_conditions_precedent`
- `vc.affinity_discovery`
- `vc.affinity_sync_read`
- `vc.affinity_sync_write`
- `vc.slack_discovery`
- `vc.slack_sync_read`
- `vc.slack_sync_write`
- `vc.google_drive_discovery`
- `vc.google_drive_sync_read`
- `vc.google_drive_sync_write`
- `vc.notion_discovery`
- `vc.notion_sync_read`
- `vc.notion_sync_write`
- `vc.harmonic_discovery`
- `vc.harmonic_sync_read`

Review notes:

- Task templates remain unavailable to the platform until the paired platform PR teaches external pack ingest to stage and apply this surface.
- The task-template catalog preserves the current platform `vc-workflows` pack metadata, template IDs, and template versions while advertising both supported vertical keys: `venture_capital` and `vc`.
- Platform eligibility is driven by catalog `verticalKeys`, which the platform loader persists to `task_definitions.vertical_keys`; the per-template `definitionJson.vertical: vc` field remains legacy workflow metadata and is not used for workspace eligibility checks.
- The task-template surface requires platform capability `external-task-definition-template-ingest`.
- All task templates advertise `vc_deal_room` as a supported project type; that project type is now included in this pack's `projectTypes` surface.
- Task templates without `supportedProjectScopes` are single-project `project_instance` tasks. Templates with `project_management` scope support pipeline, admin, or project-type management work and keep outputs on the task or future management surface unless an explicit management mapping is introduced.
- The integration templates are application-specific `project_management` tasks. They describe Affinity, Slack, Google Drive, Notion, and Harmonic tool use, discovery scope, preview/import behavior, and write-proposal boundaries without binding to a single Deal Room lifecycle stage, while the recommendation metadata only maps which management actions exist for each application.

---

## Included Project Types

- `vc_deal_room`

Review notes:

- `vc_deal_room` is copied from the current platform-local project type definition and keeps version `1.0.2`.
- The definition includes VC Deal Room fields, the instruction template, collapsed lifecycle states, lifecycle transitions, command-view metadata, and conservative `projectTaskMappings`.
- The project-type surface requires platform capability `external-project-type-ingest`.
- Task auto-fire and lifecycle-stage triggers are not enabled. The current mappings are declarative, manual-review mappings for direct project-backed inputs and required artifact outputs.

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

Standardized management actions:

- `affinity-mcp-server`: declares `discovery`, `sync_read`, and `sync_write` actions directly on the Affinity recommendation record. Discovery enumerates lists, stages, and counts after authorization; read sync is preview/import oriented; write sync is proposal-only unless the platform approval model is present.
- `slack_v2`: declares `discovery`, `sync_read`, and `sync_write` actions directly on the Slack recommendation record. Discovery enumerates workspaces/channels and classifies channel purpose; read sync is limited to selected channel/thread context; write sync is limited to approved notifications and handoffs.
- `google_drive`: declares `discovery`, `sync_read`, and `sync_write` actions directly on the Google Drive recommendation record. Discovery enumerates shared drives, folders, files, and source scopes after authorization; read sync previews selected file/folder context before attachment or import; write sync is proposal-only and excludes broad file creation, sharing, deletion, moving, and permission changes.
- `notion`: declares `discovery`, `sync_read`, and `sync_write` actions directly on the Notion recommendation record. Discovery enumerates/searches pages and databases after authorization; read sync previews selected page/database content; write sync is proposal-only and excludes broad page/database mutation unless a separate explicit approval workflow exists.
- `harmonic-mcp-oauth`: declares `discovery` and `sync_read` actions directly on the Harmonic recommendation record. The local platform catalog currently has an active Harmonic OAuth application template but zero trusted Harmonic tool rows, so the task templates and skills explicitly report the tool-discovery gap. No `sync_write` action is declared because no current write/update surface is trusted.

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

Review notes:

- These declarations define workspace-owned facts only; they do not contain firm-specific values.
- Platform ingestion should attach pack provenance while leaving variable values owned by the workspace variable substrate.

---

Workspace activation:

- deferred until the platform has a clear pack activation service and UX owner
- expected owners may include Workspace Setup, Project Manager, or admin tooling using one underlying activation service
