# Alludium Packs Agent Instructions

This repository publishes pack release artifacts. Treat release tags as immutable publication
markers, not as PR validation aids.

## Release Tags

- Do not create or push `vX.Y.Z` tags from PR branches.
- Pack PRs may bump manifest/plugin versions to the intended next release version, but that does
  not mean the corresponding Git tag should exist yet.
- Create the matching `vX.Y.Z` tag only after the PR has merged, and place it on the merge commit
  that is reachable from `origin/main`.
- If a paired platform PR references a future pack tag, keep that dependency explicit. Do not push
  an early tag just to satisfy platform external-pack validation.

## Shared Installed Plugins

- Use the installed `platform-investigation:platform-investigation` plugin for Alludium platform
  runtime or observability investigations when that evidence is needed.
- In a fresh Codex checkout, run `bash scripts/install-shared-plugins.sh` first, or add the
  `alludium/alludium-claude-marketplace` source from Codex Plugins and install
  `platform-investigation`.
- The installed `issue-workflow:*` plugin is currently policy-bound to Craft's issue repository.
  Do not use its `create-issue`, `claim-issue`, or `update-issue` skills as Packs issue intake,
  ownership, lifecycle, or parent-child workflow.
- This repository has no local issue-intake workflow configured; keep pack release and VC
  validation guidance here authoritative, and do not create a duplicate local copy of either
  marketplace plugin.

## Validation

Before pushing pack changes, run the VC validation commands from the repository root:

```bash
python3 plugins/vc/scripts/validate_pack.py
python3 plugins/vc/scripts/generate_markdown.py --check
python3 plugins/vc/scripts/validate_release_contract.py
```
