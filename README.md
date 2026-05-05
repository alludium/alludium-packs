# Alludium Packs

Public catalog for [Alludium](https://www.alludium.ai) plugins and packs.

Alludium helps teams package AI agents, skills, tools, and workflow patterns into reusable agentic workspaces. This repository is where Alludium publishes public, inspectable capability bundles that can be reviewed, reused, and eventually activated by the Alludium platform.

The repository is intentionally broader than the first VC use case. It is expected to hold bundles for multiple verticals, industries, and workflow domains over time.

## Available Packs

| Pack | Path | Status | Contents |
| --- | --- | --- | --- |
| Alludium VC | `plugins/vc/` | Draft task-template expansion | VC workflow skills, Alludium runtime agent templates, VC task-definition templates, MCP recommendations, and pack metadata |

## Plugin vs Pack

A plugin is the agent-tooling distribution shape. It carries skills, agent definitions, and MCP-friendly metadata in a structure that Claude Code and Codex-style tooling can understand.

A pack is the Alludium product/runtime concept. It can include one or more plugins plus Alludium-specific assets such as runtime agent templates, task definitions, project type definitions, activation metadata, provenance, and rollback semantics.

In this repository, each pack directory is also a valid plugin root. Standard plugin surfaces live at the pack root; Alludium-only runtime surfaces live under `alludium/`.

The first VC bundle is plugin-shaped and pack-aware. VC task-definition templates now live in the public pack as a draft surface. Project type definitions remain deferred until the platform activation seam is ready.

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
- `agents/` is reserved for future plugin-native Claude/Codex agent definitions.
- `.mcp.json` contains plugin-compatible MCP server definitions using public-safe credential placeholders.
- `alludium/manifest.yaml` describes the Alludium pack surface.
- `alludium/agent-templates/` contains Alludium runtime agent templates.
- `alludium/task-definition-templates/` contains portable VC task-definition templates.
- `alludium/mcp-recommendations.yaml` records Alludium platform mapping guidance for those MCP integrations.
- `scripts/validate_pack.py` validates the pack before publishing.

## Validation

Run:

```bash
python3 -m pip install -r plugins/vc/requirements.txt
python3 plugins/vc/scripts/validate_pack.py
```

The validator checks plugin manifests, skill frontmatter, manifest inventory, agent-template references, task-template references, and obvious secret-bearing values.

## Contributing

This repository is maintained by Alludium. New packs should follow the existing `plugins/vc/` structure and include validation before they are proposed for review.

## License

This repository is licensed under the Apache License 2.0. See [LICENSE](LICENSE).
