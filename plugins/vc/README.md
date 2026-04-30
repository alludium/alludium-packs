# Alludium VC

Public VC workflow plugin and pack seed for Alludium. This is the first bundle inside the broader `alludium-packs` catalog, not a standalone VC-only repository.

This plugin starts with the surfaces that are ready to externalize:

- Claude/Codex-style skills in `skills/`
- Alludium runtime agent templates in `alludium/agent-templates/`
- Alludium MCP recommendations in `alludium/mcp-recommendations.yaml`
- a pack-aware Alludium manifest in `alludium/manifest.yaml`
- an MCP manifest placeholder in `.mcp.json`

Task definitions and project type definitions are intentionally deferred. They belong in the larger Alludium pack shape, but the platform task-loading and workspace-activation seams should settle before those become installable assets from this repo.

## Shape

```text
alludium-packs/
└── plugins/
    └── vc/
        ├── .claude-plugin/
        │   └── plugin.json
        ├── .codex-plugin/
        │   └── plugin.json
        ├── skills/
        ├── .mcp.json
        ├── alludium/
        │   ├── manifest.yaml
        │   ├── mcp-recommendations.yaml
        │   └── agent-templates/
        └── scripts/
```

## Plugin vs Pack

The plugin surface is for agent tooling that already understands skills and MCP manifests.

The Alludium pack surface is the product/runtime extension point. It tracks Alludium agent templates today and is expected to grow later to include task definitions, project types, workspace activation metadata, provenance, and rollback/deactivation semantics.

The `.mcp.json` file is intentionally empty in this first scaffold. VC-relevant MCPs are listed as Alludium recommendations until the standard plugin MCP manifest contract and Alludium platform MCP ingestion contract are reconciled.

Template `metadata.gitRepositoryUrl` values currently point at the configurable-agent implementation repository. They are runtime implementation metadata, not this pack's source provenance. Pack source provenance should be recorded separately by the platform when ingesting a tagged release.

## Inventory

See [alludium/inventory.md](alludium/inventory.md) for the current skill, template, MCP recommendation, and deferred pack-surface inventory.

## Validation

Run:

```bash
python3 -m pip install -r requirements.txt
python3 scripts/validate_pack.py
```

The validator checks:

- plugin manifests are valid JSON
- the Alludium manifest matches files on disk
- skill frontmatter is parseable
- skill directory names match frontmatter IDs
- public skills do not set `internalOnly: true`
- Alludium agent-template skill references resolve to included skills
- obvious secret-bearing values are not present
