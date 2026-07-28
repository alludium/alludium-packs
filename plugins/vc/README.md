# Alludium VC

Public VC workflow plugin and pack seed for [Alludium](https://www.alludium.ai).

Alludium VC packages reusable venture capital workflows for sourcing, screening, diligence, investment committee preparation, closing, and portfolio onboarding. It is the first bundle inside the broader `alludium-packs` catalog, not a standalone VC-only repository.

Version `0.6.0` separates fund-level Origination Pipeline control from first-class Sourcing Line experiments and Origination Candidate records. It adds chat-first line setup, experiment starter configurations, independent line schedules and receipts, candidate-specific screening and outreach state, and namespaced relationship contracts for linking pipelines, lines, candidates, and promoted Deal Pipelines. Existing Origination Pipeline instances remain readable but require the migration described in `docs/origination-project-model-migration.md` before legacy line and candidate state is treated as active automation.

Version `0.5.42` makes Deal Manager the truthful primary contact for deal work, grounds it in the
active task, file, and artifact surface, and requires real workspace links for task and artifact
handoffs.

The current draft `v0.6.0` pack surface includes skills, generated agent/task/project-blueprint Markdown for external agentic tooling, Alludium runtime agent templates, MCP definitions, VC task-definition templates, the canonical `venture_capital` vertical key and legacy `vc` alias, and the Deal Pipeline, Origination Pipeline, Sourcing Line, Origination Candidate, and Deal Execution project type definitions. Earlier release notes remain in git history and tags.

The current draft pack surface contains:

- Claude/Codex-style skills in `skills/`
- generated Claude/Codex-style agent Markdown in `agents/`
- generated task Markdown in `tasks/`
- generated project blueprint Markdown in `project-blueprints/`
- Alludium runtime agent templates in `alludium/agent-templates/`
- VC task-definition templates in `alludium/task-definition-templates/`
- Deal Pipeline, Origination Pipeline, Sourcing Line, Origination Candidate, and Deal Execution project type definitions in `alludium/project-types/`
- VC project-type document sources in `alludium/documents/`
- VC-relevant MCP server definitions in `.mcp.json`
- Alludium application recommendations in `alludium/mcp-recommendations.yaml`
- Alludium workspace variable declarations in `alludium/workspace-variables.yaml`
- a pack-aware Alludium manifest in `alludium/manifest.yaml`

The VC task-definition templates advertise the project types they support, including `vc_deal_room`, `vc_origination_pipeline`, `vc_sourcing_line`, `vc_origination_candidate`, and `vc_investment_management`. The draft `v0.6.0` surface includes those definitions, but it still requires paired platform ingest and relationship-finalizer support before it can be used as the runtime source of truth.

Task-template workspace eligibility is controlled by catalog-level `verticalKeys`. Individual template `definitionJson.vertical` values remain legacy workflow metadata, so the `v0.2.2` compatibility fix is intentionally made in `alludium/task-definition-templates/catalog.v1.json`.

External pack task-definition templates must not declare `systemUseOnly`. System-only visibility is platform authority and must be assigned by platform-owned metadata or ingest policy, not by pack YAML.

## Contents

| Surface                   | Path                                  | Notes                                                                                    |
| ------------------------- | ------------------------------------- | ---------------------------------------------------------------------------------------- |
| Skills                    | `skills/`                             | 69 public workflow, integration-management, and origination skills used by the VC pack   |
| Generated agents          | `agents/`                             | 13 agent Markdown compatibility artifacts generated from Alludium runtime YAML          |
| Generated tasks           | `tasks/`                              | 95 task prompt Markdown files generated from task-definition YAML                        |
| Project blueprints        | `project-blueprints/`                 | 5 generated project-stage/task/agent/skill blueprints                                   |
| Agent templates           | `alludium/agent-templates/`           | 13 Alludium runtime templates using the `vc_*` baseline                                  |
| Task definition templates | `alludium/task-definition-templates/` | 95 VC workflow, integration-management, and origination task templates plus catalog metadata |
| Project types             | `alludium/project-types/`             | Five VC project type catalog entries and definitions                                     |
| Documents                 | `alludium/documents/`                 | Pack-native methodology, SOP, checklist, template, and style-guide sources               |
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
        ├── project-blueprints/
        ├── skills/
        ├── tasks/
        ├── .mcp.json
        ├── alludium/
        │   ├── manifest.yaml
        │   ├── mcp-recommendations.yaml
        │   ├── agent-templates/
        │   ├── documents/
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

The document surface is pack-native source material under `alludium/documents/`. It records reusable methodology, SOPs, checklists, templates, and style guidance and is referenced by project type metadata. Task templates can also declare durable `definitionJson.documentRefs` entries and output-field `config.documentRefId` values so artifact-producing tasks can point at a stable document source independent of the runtime artifact ID. This repository still does not implement platform document rendering or runtime behavior.

The top-level `agents/` directory contains generated Claude/Codex-style agent Markdown compatibility artifacts. The current `alludium/agent-templates/` files remain the source of truth; generated agent Markdown preserves prompt placeholders and carries skills plus source metadata for external agentic tooling.

The top-level `tasks/` directory contains generated task prompt Markdown. The current `alludium/task-definition-templates/` YAML remains the source of truth; generated task Markdown extracts the execution instructions, input policy, action policy, completion criteria, human decision points, fields, skills, and routing metadata needed to start each task.

The top-level `project-blueprints/` directory contains generated project blueprint Markdown. The current `alludium/project-types/` JSON and `alludium/task-definition-templates/` YAML remain the source of truth; generated project blueprints show setup/general tasks and lifecycle-stage task mappings with recommended agents and task-referenced skills.

Generated Markdown must be deterministic and kept in sync by `scripts/generate_markdown.py`. CI fails if YAML or project-type JSON changes without regenerating the corresponding Markdown output.

For same-repository pull requests, GitHub automatically runs the generator, pushes updated `agents/`, `tasks/`, and `project-blueprints/` files back to the PR branch when source or generated Markdown changes, and dispatches validation for the updated branch. External fork PRs cannot receive bot pushes, so contributors from forks should run the generator locally before pushing.

Branch protection should require the `Validate` workflow, not the generated-Markdown sync helper. The helper pushes with `GITHUB_TOKEN`, so its bot push does not trigger `pull_request` workflows on the generated SHA; it explicitly dispatches `Validate` instead.

Because generated Markdown is part of the published pack artifact, source changes that regenerate `agents/`, `tasks/`, or `project-blueprints/` are release-content changes. Bump the pack/plugin version and update this README plus `alludium/inventory.md` whenever those generated files change.

The `.mcp.json` file lists VC-relevant MCP servers using public-safe user/workspace credential placeholders. When the same pack is ingested into Alludium, `alludium/mcp-recommendations.yaml` tells the platform which entries can map to managed platform defaults or workspace connections.

Template `metadata.gitRepositoryUrl` values currently point at the configurable-agent implementation repository. They are runtime implementation metadata, not this pack's source provenance. Pack source provenance should be recorded separately by the platform when ingesting a tagged release.

## Inventory

See [alludium/inventory.md](alludium/inventory.md) for the current skill, template, task-template, MCP recommendation, and deferred pack-surface inventory.

## Project Blueprints

- [Deal Pipeline Blueprint](project-blueprints/vc-deal-room.md)
- [Origination Pipeline Blueprint](project-blueprints/vc-origination-pipeline.md)
- [Sourcing Line Blueprint](project-blueprints/vc-sourcing-line.md)
- [Origination Candidate Blueprint](project-blueprints/vc-origination-candidate.md)
- [Deal Execution Blueprint](project-blueprints/vc-investment-management.md)

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
- task templates do not declare platform-owned `systemUseOnly` metadata
- VC task artifact output/input fields are present, required, file-backed, and semantically named
- VC project creation metadata references only declared project fields, lifecycle states, task templates, and connected-source field mappings
- generated agent/task Markdown is up to date
- obvious secret-bearing values are not present

CI also runs:

```bash
python3 scripts/validate_release_contract.py
```

The release-contract validator compares the PR against `origin/main` and the latest remote `vX.Y.Z` tag, rejects backwards or same-version release-content changes, rejects reused remote tags for changed release content, and verifies versioned docs mention the current manifest version. Local runs also consider staged, unstaged, and untracked release-content files, so run it from a clean worktree for CI-like behavior.
