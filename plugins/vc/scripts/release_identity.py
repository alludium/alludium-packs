"""Shared schema for the release identity embedded in VC ontology artifacts."""


def release_identity(pack: dict) -> dict[str, str]:
    for field in ("id", "version", "repository"):
        if not isinstance(pack.get(field), str) or not pack[field].strip():
            raise ValueError(f"pack.{field} must be a non-empty string")
    return {
        "packId": pack["id"],
        "packVersion": pack["version"],
        "repository": pack["repository"],
        "tag": f"v{pack['version']}",
    }
