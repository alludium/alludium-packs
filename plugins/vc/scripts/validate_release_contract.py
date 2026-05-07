#!/usr/bin/env python3
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[3]
PACK_ROOT = REPO_ROOT / "plugins" / "vc"
MANIFEST_PATH = PACK_ROOT / "alludium" / "manifest.yaml"
DEFAULT_BASE_REF = "origin/main"
SEMVER_PATTERN = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
RELEASE_CONTENT_PATHS = [
    "plugins/vc/.claude-plugin",
    "plugins/vc/.codex-plugin",
    "plugins/vc/.mcp.json",
    "plugins/vc/alludium",
    "plugins/vc/skills",
]
VERSIONED_DOC_PATHS = [
    "plugins/vc/README.md",
    "plugins/vc/alludium/inventory.md",
]


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def warn(message: str) -> None:
    print(f"WARNING: {message}", file=sys.stderr)


def run_git(args: list[str], *, allow_failure: bool = False) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        if allow_failure:
            return ""
        fail(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def read_yaml_text(text: str, context: str) -> dict[str, Any]:
    try:
        parsed = yaml.safe_load(text)
    except Exception as exc:  # pragma: no cover - defensive CLI guard
        fail(f"Failed to parse {context}: {exc}")
    if not isinstance(parsed, dict):
        fail(f"{context} must be a YAML object")
    return parsed


def read_manifest_version_from_text(text: str, context: str) -> str:
    manifest = read_yaml_text(text, context)
    version = manifest.get("pack", {}).get("version")
    if not isinstance(version, str) or not version:
        fail(f"{context} must declare pack.version")
    return version


def read_current_manifest_version() -> str:
    return read_manifest_version_from_text(
        MANIFEST_PATH.read_text(encoding="utf-8"),
        str(MANIFEST_PATH.relative_to(REPO_ROOT)),
    )


def read_base_manifest_version(base_ref: str) -> str:
    manifest_at_base = run_git(
        ["show", f"{base_ref}:plugins/vc/alludium/manifest.yaml"],
        allow_failure=False,
    )
    return read_manifest_version_from_text(manifest_at_base, f"{base_ref}:plugins/vc/alludium/manifest.yaml")


def try_parse_semver(version: str) -> tuple[int, int, int] | None:
    match = SEMVER_PATTERN.fullmatch(version)
    if match is None:
        return None
    return tuple(int(part) for part in match.groups())


def parse_semver(version: str, context: str = "Pack version") -> tuple[int, int, int]:
    parsed = try_parse_semver(version)
    if parsed is None:
        fail(
            f"{context} {version!r} must be strict semantic version X.Y.Z "
            "with no prefix or prerelease suffix"
        )
    return parsed


def release_content_changed(base_ref: str, *, include_worktree: bool = True) -> bool:
    committed_diff = run_git(
        ["diff", "--name-only", f"{base_ref}...HEAD", "--", *RELEASE_CONTENT_PATHS],
        allow_failure=False,
    )
    staged_diff = ""
    unstaged_diff = ""
    untracked = ""
    if include_worktree:
        staged_diff = run_git(
            ["diff", "--cached", "--name-only", "--", *RELEASE_CONTENT_PATHS],
            allow_failure=False,
        )
        unstaged_diff = run_git(
            ["diff", "--name-only", "--", *RELEASE_CONTENT_PATHS],
            allow_failure=False,
        )
        untracked = run_git(
            ["ls-files", "--others", "--exclude-standard", "--", *RELEASE_CONTENT_PATHS],
            allow_failure=False,
        )
    return any([committed_diff, staged_diff, unstaged_diff, untracked])


def require_docs_reference_version(version: str) -> None:
    expected_refs = {version, f"v{version}"}
    for relative_path in VERSIONED_DOC_PATHS:
        path = REPO_ROOT / relative_path
        body = path.read_text(encoding="utf-8")
        if not any(ref in body for ref in expected_refs):
            fail(f"{relative_path} must mention current pack version {version}")


def list_remote_semver_tags(remote: str) -> dict[str, tuple[int, int, int]]:
    output = run_git(["ls-remote", "--tags", "--refs", remote, "refs/tags/v*"], allow_failure=False)
    versions: dict[str, tuple[int, int, int]] = {}
    for line in output.splitlines():
        parts = line.split()
        if len(parts) != 2:
            continue
        ref = parts[1]
        tag_name = ref.removeprefix("refs/tags/")
        if not tag_name.startswith("v"):
            continue
        version = tag_name[1:]
        parsed = try_parse_semver(version)
        if parsed is not None:
            versions[version] = parsed
    return versions


def highest_remote_version(remote: str) -> tuple[str, tuple[int, int, int]] | None:
    versions = list_remote_semver_tags(remote)
    if not versions:
        return None
    version, parsed = max(versions.items(), key=lambda item: item[1])
    return version, parsed


def validate_release_contract(base_ref: str, remote: str) -> None:
    current_version = read_current_manifest_version()
    current_semver = parse_semver(current_version, "Current pack version")
    base_version = read_base_manifest_version(base_ref)
    base_semver = parse_semver(base_version, f"Base pack version at {base_ref}")
    content_changed = release_content_changed(base_ref)

    if current_semver < base_semver:
        fail(
            f"Pack version moved backwards from {base_version} on {base_ref} "
            f"to {current_version}"
        )
    if content_changed and current_semver == base_semver:
        fail(
            "VC pack release content changed without a manifest version bump. "
            f"Current version is still {current_version}."
        )

    if content_changed:
        warn(
            "Release-content diff includes local staged, unstaged, and untracked files. "
            "Run from a clean worktree for CI-like behavior."
        )

    require_docs_reference_version(current_version)

    version_changed = current_version != base_version
    if content_changed or version_changed:
        remote_versions = list_remote_semver_tags(remote)
        if current_version in remote_versions:
            fail(
                f"Remote tag v{current_version} already exists. Choose a new pack version "
                "before changing release content."
            )
        highest = highest_remote_version(remote)
        if highest is not None:
            highest_version, highest_semver = highest
            if current_semver <= highest_semver:
                fail(
                    f"Pack version {current_version} must be greater than the latest remote "
                    f"release tag v{highest_version}"
                )

    print(
        "Validated VC pack release contract: "
        f"version {current_version}, "
        f"base {base_version}, "
        f"release_content_changed={str(content_changed).lower()}"
    )


def run_self_test() -> None:
    assert parse_semver("0.3.2") == (0, 3, 2)
    assert parse_semver("10.20.30") == (10, 20, 30)
    for invalid in ["v0.3.2", "0.3", "0.3.2-beta", "01.2.3"]:
        assert try_parse_semver(invalid) is None
    remote_tags = """
1111111111111111111111111111111111111111\trefs/tags/not-semver
2222222222222222222222222222222222222222\trefs/tags/v0.3.2
3333333333333333333333333333333333333333\trefs/tags/v0.4.0
4444444444444444444444444444444444444444\trefs/tags/v0.4.0^{}
"""
    parsed_versions: dict[str, tuple[int, int, int]] = {}
    for line in remote_tags.splitlines():
        parts = line.split()
        if len(parts) != 2 or "^{}" in parts[1]:
            continue
        tag_name = parts[1].removeprefix("refs/tags/")
        if not tag_name.startswith("v"):
            continue
        parsed = try_parse_semver(tag_name[1:])
        if parsed is not None:
            parsed_versions[tag_name[1:]] = parsed
    assert max(parsed_versions.items(), key=lambda item: item[1]) == ("0.4.0", (0, 4, 0))
    print("Release contract self-test passed")


def main() -> None:
    if "--self-test" in sys.argv:
        run_self_test()
        return

    base_ref = next(
        (arg.removeprefix("--base-ref=") for arg in sys.argv[1:] if arg.startswith("--base-ref=")),
        os.environ.get("RELEASE_CONTRACT_BASE_REF", DEFAULT_BASE_REF),
    )
    remote = next(
        (arg.removeprefix("--remote=") for arg in sys.argv[1:] if arg.startswith("--remote=")),
        os.environ.get("RELEASE_CONTRACT_REMOTE", "origin"),
    )
    validate_release_contract(base_ref, remote)


if __name__ == "__main__":
    main()
