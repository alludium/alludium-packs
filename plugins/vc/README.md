# Alludium VC

Public VC workflow plugin and pack seed for [Alludium](https://www.alludium.ai).

Alludium VC packages reusable venture capital workflows for sourcing, screening, diligence, investment committee preparation, closing, and portfolio onboarding. It is the first bundle inside the broader `alludium-packs` catalog, not a standalone VC-only repository.

The published `v0.1.0` release contains skills, Alludium runtime agent templates, MCP definitions, and Alludium MCP mapping guidance. The current draft `v0.3.2` pack surface includes VC task-definition templates, advertises both the canonical `venture_capital` vertical key and the legacy `vc` alias, adds the VC Deal Room project type and command-view metadata, and declares workspace-variable plus application-recommendation metadata for the paired platform ingest work.

The current draft pack surface contains:

- Claude/Codex-style skills in `skills/`
- Alludium runtime agent templates in `alludium/agent-templates/`
- VC task-definition templates in `alludium/task-definition-templates/`
- VC Deal Room project type definition in `alludium/project-types/`
- VC-relevant MCP server definitions in `.mcp.json`
- Alludium application recommendations in `alludium/mcp-recommendations.yaml`
- Alludium workspace variable declarations in `alludium/workspace-variables.yaml`
- a pack-aware Alludium manifest in `alludium/manifest.yaml`

The VC task-definition templates advertise `vc_deal_room` as a supported project type. The draft `v0.3.2` surface includes that project type definition, but it still requires a paired platform release with `external-project-type-ingest` support before it can be used as the runtime source of truth.

Task-template workspace eligibility is controlled by catalog-level `verticalKeys`. Individual template `definitionJson.vertical` values remain legacy workflow metadata, so the `v0.2.2` compatibility fix is intentionally made in `alludium/task-definition-templates/catalog.v1.json`.

## Contents

| Surface                   | Path                                  | Notes                                                                                    |
| ------------------------- | ------------------------------------- | ---------------------------------------------------------------------------------------- |
| Skills                    | `skills/`                             | 23 public workflow skills used by the VC agent templates                                 |
| Agent templates           | `alludium/agent-templates/`           | 8 Alludium runtime templates using the `vc_*` baseline                                   |
| Task definition templates | `alludium/task-definition-templates/` | 26 VC workflow task templates and catalog metadata                                       |
| Project types             | `alludium/project-types/`             | VC Deal Room project type catalog and definition                                         |
| Pack manifest             | `alludium/manifest.yaml`              | Alludium-specific inventory, boundaries, and future pack surfaces                        |
| Plugin MCP manifest       | `.mcp.json`                           | Public-safe MCP definitions for VC research, CRM, meeting, and market-intelligence tools |
| Application recommendations | `alludium/mcp-recommendations.yaml` | VC application recommendations nested on the same `externalId`/`name` records as MCP mapping |
| Workspace variable declarations | `alludium/workspace-variables.yaml` | Public-safe VC workspace variable definitions without firm-specific values               |
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
        │   ├── task-definition-templates/
        │   └── project-types/
        └── scripts/
```

## Plugin vs Pack

The plugin surface is for agent tooling that already understands skills, agent definitions, and MCP manifests.

The VC pack directory is also the plugin root. Standard plugin concepts live at the pack root. Alludium-only runtime concepts live under `alludium/`.

The Alludium pack surface is the product/runtime extension point. It tracks Alludium agent templates, task-definition templates, and project types today and is expected to grow later to include workspace activation metadata, provenance, and rollback/deactivation semantics.

The task-definition-template surface requires platform support for `external-task-definition-template-ingest`. Platform versions that only understand external pack skills and Alludium agent templates can ingest the older surfaces but will ignore task templates.

The project-type surface requires platform support for `external-project-type-ingest`. Platform versions without that capability should continue using platform-local project types until the paired platform cutover lands.

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
- VC task artifact output/input fields are present, required, file-backed, and semantically named
- obvious secret-bearing values are not present

CI also runs:

```bash
python3 scripts/validate_release_contract.py
```

The release-contract validator compares the PR against `origin/main` and the latest remote `vX.Y.Z` tag, rejects backwards or same-version release-content changes, rejects reused remote tags for changed release content, and verifies versioned docs mention the current manifest version. Local runs also consider staged, unstaged, and untracked release-content files, so run it from a clean worktree for CI-like behavior.
