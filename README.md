# Alludium Packs

Public catalog for [Alludium](https://www.alludium.ai) plugins and packs.

Alludium helps teams package AI agents, skills, tools, and workflow patterns into reusable agentic workspaces. This repository is where Alludium publishes public, inspectable capability bundles that can be reviewed, reused, and eventually activated by the Alludium platform.

The repository is intentionally broader than the first VC use case. It is expected to hold bundles for multiple verticals, industries, and workflow domains over time.

## Available Packs

| Pack | Path | Status | Contents |
| --- | --- | --- | --- |
| Alludium VC | `plugins/vc/` | Draft review | VC workflow skills, Alludium runtime agent templates, MCP recommendations, and pack metadata |

## Plugin vs Pack

A plugin is the agent-tooling distribution shape. It carries skills and MCP-friendly metadata in a structure that Claude Code and Codex-style tooling can understand.

A pack is the Alludium product/runtime concept. It can include one or more plugins plus Alludium-specific assets such as runtime agent templates, task definitions, project type definitions, activation metadata, provenance, and rollback semantics.

The first VC bundle is plugin-shaped and pack-aware. Task definitions and project type definitions are intentionally deferred until the platform activation and task-loading seams are ready.

## Repository Shape

Each pack lives under `plugins/<pack-id>/`:

```text
alludium-packs/
├── plugins/
│   └── vc/
│       ├── .claude-plugin/
│       ├── .codex-plugin/
│       ├── .mcp.json
│       ├── skills/
│       ├── alludium/
│       └── scripts/
└── .github/
    └── workflows/
```

Within a pack:

- `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` describe the plugin for agent tooling.
- `skills/` contains public skills in Markdown.
- `.mcp.json` is reserved for plugin-compatible MCP server definitions.
- `alludium/manifest.yaml` describes the Alludium pack surface.
- `alludium/agent-templates/` contains Alludium runtime agent templates.
- `alludium/mcp-recommendations.yaml` records recommended MCP integrations where full plugin ingestion is not ready yet.
- `scripts/validate_pack.py` validates the pack before publishing.

## Validation

Run:

```bash
python3 -m pip install -r plugins/vc/requirements.txt
python3 plugins/vc/scripts/validate_pack.py
```

The validator checks plugin manifests, skill frontmatter, manifest inventory, template-to-skill references, and obvious secret-bearing values.

## Contributing

This repository is maintained by Alludium. New packs should follow the existing `plugins/vc/` structure and include validation before they are proposed for review.
