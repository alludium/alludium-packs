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

Before pushing pack changes, run the VC validation commands from the repository root:

```bash
python3 plugins/vc/scripts/validate_pack.py
python3 plugins/vc/scripts/generate_markdown.py --check
python3 plugins/vc/scripts/validate_release_contract.py
```
