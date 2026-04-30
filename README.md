# Alludium Packs

Public catalog for Alludium plugins and packs.

This repository is intentionally broader than the first VC use case. It is expected to hold public, inspectable capability bundles for multiple verticals, industries, and workflow domains.

The first bundle is:

- `plugins/vc/`: VC workflow skills, Alludium runtime agent templates, and pack metadata

## Plugin vs Pack

A plugin is the agent-tooling distribution shape. It carries skills and MCP-friendly metadata in a structure that Claude Code and Codex-style tooling can understand.

A pack is the Alludium product/runtime concept. It can include one or more plugins plus Alludium-specific assets such as runtime agent templates, task definitions, project type definitions, activation metadata, provenance, and rollback semantics.

The first VC bundle is plugin-shaped and pack-aware. Task definitions and project type definitions are intentionally deferred until the platform activation and task-loading seams are ready.

## Shape

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

## Validation

Run:

```bash
python3 -m pip install -r plugins/vc/requirements.txt
python3 plugins/vc/scripts/validate_pack.py
```
