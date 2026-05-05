# Alludium VC Inventory

**Version**: 0.1.0
**Status**: Published baseline

This inventory describes the current public VC plugin/pack seed tagged as `v0.1.0`. It intentionally includes only the surfaces ready for first extraction: VC skills, Alludium runtime agent templates, public-safe MCP definitions, and Alludium MCP recommendations.

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

## MCP Definitions And Platform Mapping

The first scaffold includes public-safe plugin MCP definitions in `.mcp.json` and Alludium platform mapping guidance in `alludium/mcp-recommendations.yaml`.

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

Review notes:

- `.mcp.json` uses user/workspace credential placeholders, not Alludium platform secrets.
- `alludium/mcp-recommendations.yaml` records how Alludium can map the same external IDs to platform defaults or workspace connections when the pack is ingested.
- Alludium template references to `alludium-platform`, `google_drive`, and `linkedin` are tracked as platform-only/template-only integrations rather than plugin MCP definitions.
- Pipedream-provided integrations are intentionally excluded from this first pack scaffold.
- `alludium-docs-mcp` and `xero-mcp-server` exist in platform MCP config but are intentionally excluded because they are not part of the first VC workflow surface.
- No secrets, tokens, or environment-specific values should be copied into this public repo.

---

## Deferred Pack Surfaces

Task definitions:

- deferred from `v0.1.0`; planned as the next pack surface now that platform task-template work has landed
- expected future path: `alludium/task-definition-templates/`

Project types:

- deferred until VC Deal Room activation semantics are designed
- expected future path: `alludium/project-types/`

Workspace activation:

- deferred until the platform has a clear pack activation service and UX owner
- expected owners may include Workspace Setup, Project Manager, or admin tooling using one underlying activation service
