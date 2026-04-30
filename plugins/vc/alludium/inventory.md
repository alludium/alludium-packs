# Alludium VC Inventory

**Version**: 0.1.0
**Status**: Phase 1 candidate

This inventory describes the current public VC plugin/pack seed. It intentionally includes only the surfaces ready for first extraction.

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

## MCP Recommendations

The first scaffold includes advisory Alludium MCP recommendations in `alludium/mcp-recommendations.yaml`.

Included recommendation IDs:

- `affinity-mcp-server`
- `harmonic-mcp-oauth`
- `dealroom-mcp`
- `exa-mcp-hosted`
- `firecrawl-mcp-hosted`
- `brave-search-mcp`
- `serpapi-mcp`
- `granola-mcp`
- `otter-mcp-oauth`
- `fireflies-mcp-oauth`

Review notes:

- These are not yet installable plugin MCP definitions.
- `.mcp.json` remains an empty placeholder until the Claude/Codex plugin MCP contract and Alludium platform MCP ingestion contract are reconciled.
- No secrets, tokens, or environment-specific values should be copied into this public repo.

---

## Deferred Pack Surfaces

Task definitions:

- deferred until task-definition source loading and pack activation are stable
- expected future path: `alludium/task-definition-templates/`

Project types:

- deferred until VC Deal Room activation semantics are designed
- expected future path: `alludium/project-types/`

Workspace activation:

- deferred until the platform has a clear pack activation service and UX owner
- expected owners may include Workspace Setup, Project Manager, or admin tooling using one underlying activation service
