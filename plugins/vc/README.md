# Alludium VC

Public VC workflow plugin and pack seed for [Alludium](https://www.alludium.ai).

Alludium VC packages reusable venture capital workflows for sourcing, screening, diligence, investment committee preparation, closing, and portfolio onboarding. It is the first bundle inside the broader `alludium-packs` catalog, not a standalone VC-only repository.

The current draft `v0.4.2` pack surface includes skills, generated agent/task Markdown for external agentic tooling, Alludium runtime agent templates, MCP definitions, VC task-definition templates, both the canonical `venture_capital` vertical key and the legacy `vc` alias, the VC Deal Room and VC Origination Pipeline project type definitions, workspace-variable declarations, application-recommendation metadata, collapsed Deal Room lifecycle mappings, required task-input mappings, runtime agent access to the platform text-artifact creation tool, and one setup task entry point for each setup-capable integration.

The current draft pack surface contains:

- Claude/Codex-style skills in `skills/`
- generated Claude/Codex-style agent Markdown in `agents/`
- generated task Markdown in `tasks/`
- Alludium runtime agent templates in `alludium/agent-templates/`
- VC task-definition templates in `alludium/task-definition-templates/`
- VC Deal Room and VC Origination Pipeline project type definitions in `alludium/project-types/`
- VC-relevant MCP server definitions in `.mcp.json`
- Alludium application recommendations in `alludium/mcp-recommendations.yaml`
- Alludium workspace variable declarations in `alludium/workspace-variables.yaml`
- a pack-aware Alludium manifest in `alludium/manifest.yaml`

The VC task-definition templates advertise `vc_deal_room` and `vc_origination_pipeline` as supported project types. The draft `v0.4.2` surface includes those project type definitions, but they still require paired platform ingest support before they can be used as the runtime source of truth.

Task-template workspace eligibility is controlled by catalog-level `verticalKeys`. Individual template `definitionJson.vertical` values remain legacy workflow metadata, so the `v0.2.2` compatibility fix is intentionally made in `alludium/task-definition-templates/catalog.v1.json`.

## Contents

| Surface                   | Path                                  | Notes                                                                                    |
| ------------------------- | ------------------------------------- | ---------------------------------------------------------------------------------------- |
| Skills                    | `skills/`                             | 60 public workflow, integration-management, and origination skills used by the VC pack   |
| Generated agents          | `agents/`                             | 8 agent Markdown compatibility artifacts generated from Alludium runtime YAML           |
| Generated tasks           | `tasks/`                              | 72 task prompt Markdown files generated from task-definition YAML                        |
| Agent templates           | `alludium/agent-templates/`           | 8 Alludium runtime templates using the `vc_*` baseline                                   |
| Task definition templates | `alludium/task-definition-templates/` | 72 VC workflow, integration-management, and origination task templates plus catalog metadata |
| Project types             | `alludium/project-types/`             | VC Deal Room and VC Origination Pipeline project type catalog and definitions            |
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
        ├── agents/
        ├── skills/
        ├── tasks/
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

The top-level `agents/` directory contains generated Claude/Codex-style agent Markdown compatibility artifacts. The current `alludium/agent-templates/` files remain the source of truth; generated agent Markdown preserves prompt placeholders and carries skills plus source metadata for external agentic tooling.

The top-level `tasks/` directory contains generated task prompt Markdown. The current `alludium/task-definition-templates/` YAML remains the source of truth; generated task Markdown extracts the execution instructions, input policy, action policy, completion criteria, human decision points, fields, skills, and routing metadata needed to start each task.

Generated Markdown must be deterministic and kept in sync by `scripts/generate_markdown.py`. CI fails if YAML changes without regenerating the corresponding Markdown output.

For same-repository pull requests, GitHub automatically runs the generator, pushes updated `agents/` and `tasks/` files back to the PR branch when YAML or generated Markdown changes, and dispatches validation for the updated branch. External fork PRs cannot receive bot pushes, so contributors from forks should run the generator locally before pushing.

Branch protection should require the `Validate` workflow, not the generated-Markdown sync helper. The helper pushes with `GITHUB_TOKEN`, so its bot push does not trigger `pull_request` workflows on the generated SHA; it explicitly dispatches `Validate` instead.

Because generated Markdown is part of the published pack artifact, YAML changes that regenerate `agents/` or `tasks/` are release-content changes. Bump the pack/plugin version and update this README plus `alludium/inventory.md` whenever those generated files change.

The `.mcp.json` file lists VC-relevant MCP servers using public-safe user/workspace credential placeholders. When the same pack is ingested into Alludium, `alludium/mcp-recommendations.yaml` tells the platform which entries can map to managed platform defaults or workspace connections.

Template `metadata.gitRepositoryUrl` values currently point at the configurable-agent implementation repository. They are runtime implementation metadata, not this pack's source provenance. Pack source provenance should be recorded separately by the platform when ingesting a tagged release.

## Inventory

See [alludium/inventory.md](alludium/inventory.md) for the current skill, template, task-template, MCP recommendation, and deferred pack-surface inventory.

## Validation

Run:

```bash
python3 -m pip install -r requirements.txt
python3 scripts/validate_pack.py
python3 scripts/generate_markdown.py --check
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
- generated agent/task Markdown is up to date
- obvious secret-bearing values are not present

CI also runs:

```bash
python3 scripts/validate_release_contract.py
```

The release-contract validator compares the PR against `origin/main` and the latest remote `vX.Y.Z` tag, rejects backwards or same-version release-content changes, rejects reused remote tags for changed release content, and verifies versioned docs mention the current manifest version. Local runs also consider staged, unstaged, and untracked release-content files, so run it from a clean worktree for CI-like behavior.
