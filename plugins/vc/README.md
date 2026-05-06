# Alludium VC

Public VC workflow plugin and pack seed for [Alludium](https://www.alludium.ai).

Alludium VC packages reusable venture capital workflows for sourcing, screening, diligence, investment committee preparation, closing, and portfolio onboarding. It is the first bundle inside the broader `alludium-packs` catalog, not a standalone VC-only repository.

The published `v0.1.0` release contains skills, Alludium runtime agent templates, MCP definitions, and Alludium MCP mapping guidance. The current draft `v0.2.2` pack surface adds VC task-definition templates for the paired platform ingest work and advertises both the canonical `venture_capital` vertical key and the legacy `vc` alias.

The current draft pack surface contains:

- Claude/Codex-style skills in `skills/`
- Alludium runtime agent templates in `alludium/agent-templates/`
- VC task-definition templates in `alludium/task-definition-templates/`
- VC-relevant MCP server definitions in `.mcp.json`
- Alludium platform mapping guidance for MCPs in `alludium/mcp-recommendations.yaml`
- a pack-aware Alludium manifest in `alludium/manifest.yaml`

Project type definitions remain intentionally deferred. The VC task-definition templates advertise `vc_deal_room` as a supported project type, but that project type is a declared platform-local dependency until the later project-type pack surface lands.

Task-template workspace eligibility is controlled by catalog-level `verticalKeys`. Individual template `definitionJson.vertical` values remain legacy workflow metadata, so the `v0.2.2` compatibility fix is intentionally made in `alludium/task-definition-templates/catalog.v1.json`.

## Contents

| Surface                   | Path                                  | Notes                                                                                    |
| ------------------------- | ------------------------------------- | ---------------------------------------------------------------------------------------- |
| Skills                    | `skills/`                             | 23 public workflow skills used by the VC agent templates                                 |
| Agent templates           | `alludium/agent-templates/`           | 8 Alludium runtime templates using the `vc_*` baseline                                   |
| Task definition templates | `alludium/task-definition-templates/` | 26 VC workflow task templates and catalog metadata                                       |
| Pack manifest             | `alludium/manifest.yaml`              | Alludium-specific inventory, boundaries, and future pack surfaces                        |
| Plugin MCP manifest       | `.mcp.json`                           | Public-safe MCP definitions for VC research, CRM, meeting, and market-intelligence tools |
| MCP platform mapping      | `alludium/mcp-recommendations.yaml`   | Alludium mapping guidance for platform-managed or workspace-managed connections          |
| Validation                | `scripts/validate_pack.py`            | Local and CI validation for manifests, skills, references, and obvious secrets           |

## Repository Shape

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
        │   ├── agent-templates/
        │   └── task-definition-templates/
        └── scripts/
```

## Plugin vs Pack

The plugin surface is for agent tooling that already understands skills, agent definitions, and MCP manifests.

The VC pack directory is also the plugin root. Standard plugin concepts live at the pack root. Alludium-only runtime concepts live under `alludium/`.

The Alludium pack surface is the product/runtime extension point. It tracks Alludium agent templates and task-definition templates today and is expected to grow later to include project types, workspace activation metadata, provenance, and rollback/deactivation semantics.

The task-definition-template surface requires platform support for `external-task-definition-template-ingest`. Platform versions that only understand external pack skills and Alludium agent templates can ingest the older surfaces but will ignore task templates.

The top-level `agents/` directory is reserved for future plugin-native Claude/Codex agent definitions. The current `alludium/agent-templates/` files are Alludium runtime YAML templates, so they intentionally remain under the Alludium extension surface until a deliberate adapter or generated native-agent format exists.

The `.mcp.json` file lists VC-relevant MCP servers using public-safe user/workspace credential placeholders. When the same pack is ingested into Alludium, `alludium/mcp-recommendations.yaml` tells the platform which entries can map to managed platform defaults or workspace connections.

Template `metadata.gitRepositoryUrl` values currently point at the configurable-agent implementation repository. They are runtime implementation metadata, not this pack's source provenance. Pack source provenance should be recorded separately by the platform when ingesting a tagged release.

## Inventory

See [alludium/inventory.md](alludium/inventory.md) for the current skill, template, task-template, MCP recommendation, and deferred pack-surface inventory.

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
- task-template skill and agent-template references resolve to manifest-declared surfaces
- obvious secret-bearing values are not present
