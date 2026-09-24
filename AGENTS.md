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

## Validation

For VC updates, edit the authored Pack content and declare the next unused release
version once with `python3 plugins/vc/scripts/prepare_release.py --version X.Y.Z`.
Alternatively, edit `pack.version` in the manifest and run the command without
`--version`. Commit the generated metadata and Markdown with the content change;
do not hand-edit repeated release versions or hashes. Independent template and
component versions and historical release notes remain authored contracts.

Before preparing a PR, inspect whether the change alters agent prompts, task instructions,
skills, tool contracts, capability bundles, or model settings. For such changes, invoke the
shared `agent-evals:behaviour-change-eval` skill's PR checkpoint when available. Offer eval
preparation once per change, honour an existing decline or deferral, and record its disposition
in the PR description. If the plugin is unavailable, record disposition `not-checked` with
reason `plugin unavailable` and continue. This is an optional evidence checkpoint, not a PR or release gate;
it does not grant authority for paid calls. Follow the shared skill for supported runners and
coverage limits rather than copying its workflow here.

Before pushing pack changes, run the VC validation commands from the repository root:

```bash
python3 plugins/vc/scripts/validate_pack.py
python3 plugins/vc/scripts/prepare_release.py --check
python3 plugins/vc/scripts/validate_release_contract.py
```

The preparation check includes generated agent/task/blueprint Markdown freshness.
Preparation is local only; publication and platform adoption are separate steps.
