#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


THIS_FILE = Path(__file__).resolve()
PACK_ROOT = THIS_FILE.parents[1]
METHOD_ROOT = PACK_ROOT / "skills" / "embedded-deal-continuity" / "references"
SCHEMA_PATH = METHOD_ROOT / "method-run.schema.json"
EXAMPLE_PATH = METHOD_ROOT / "examples" / "public-neutral-s1-run.json"
CHANGE_CATEGORIES = (
    "added",
    "preserved",
    "stale",
    "superseded",
    "conflicting",
    "unresolved",
)


def _json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _path(error: Any) -> str:
    parts = [str(part) for part in error.absolute_path]
    return ".".join(parts) or "$"


def _unique_index(
    values: list[dict[str, Any]],
    key_name: str,
    label: str,
    errors: list[str],
) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for value in values:
        key = value[key_name]
        if key in indexed:
            errors.append(f"duplicate {label} {key}")
        indexed[key] = value
    return indexed


def validate_run(payload: dict[str, Any], schema: dict[str, Any] | None = None) -> list[str]:
    """Return schema and cross-reference errors for one complete method run."""

    schema = schema or _json(SCHEMA_PATH)
    schema_errors = sorted(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(payload),
        key=lambda error: (list(error.absolute_path), error.message),
    )
    errors = [f"schema {_path(error)}: {error.message}" for error in schema_errors]
    if schema_errors:
        return errors

    method_input = payload["input"]
    method_output = payload["output"]

    authorities = _unique_index(
        method_input["authorityRecords"], "authorityId", "authority", errors
    )
    citations = _unique_index(method_input["citations"], "citationId", "citation", errors)
    claims = _unique_index(method_input["evidenceClaims"], "claimId", "claim", errors)
    changes = _unique_index(
        method_input["changeConsequences"], "changeId", "change", errors
    )

    source_revisions: dict[tuple[str, str], dict[str, Any]] = {}
    for revision in method_input["sourceRevisions"]:
        key = (revision["sourceId"], revision["revisionId"])
        if key in source_revisions:
            errors.append(f"duplicate source revision {key[0]}@{key[1]}")
        source_revisions[key] = revision
        if revision["authorityId"] not in authorities:
            errors.append(
                f"source revision {key[0]}@{key[1]} references unknown authority "
                f"{revision['authorityId']}"
            )

    for citation_id, citation in citations.items():
        key = (citation["sourceId"], citation["revisionId"])
        if key not in source_revisions:
            errors.append(
                f"citation {citation_id} references unknown source revision {key[0]}@{key[1]}"
            )

    method_owner_id = method_input["authorityContext"]["methodOwnerAuthorityId"]
    investment_authority_id = method_input["authorityContext"]["investmentAuthorityId"]
    for role, authority_id in (
        ("method owner", method_owner_id),
        ("investment authority", investment_authority_id),
    ):
        authority = authorities.get(authority_id)
        if authority is None:
            errors.append(f"{role} references unknown authority {authority_id}")
        elif authority["status"] != "current":
            errors.append(f"{role} {authority_id} must be current")

    fund_context = method_input["fundMethodContext"]
    for citation_id in fund_context["citationIds"]:
        citation = citations.get(citation_id)
        if citation is None:
            errors.append(f"Fund method context references unknown citation {citation_id}")
        elif citation["revisionId"] != fund_context["revisionId"]:
            errors.append(
                f"Fund method citation {citation_id} uses revision {citation['revisionId']} "
                f"instead of {fund_context['revisionId']}"
            )
        else:
            source_revision = source_revisions.get((citation["sourceId"], citation["revisionId"]))
            if source_revision and source_revision["authorityId"] != method_owner_id:
                errors.append(
                    f"Fund method revision {fund_context['revisionId']} is not owned by "
                    f"{method_owner_id}"
                )

    for claim_id, claim in claims.items():
        authority = authorities.get(claim["authorityId"])
        if authority is None:
            errors.append(f"claim {claim_id} references unknown authority {claim['authorityId']}")
        for citation_id in claim["citationIds"]:
            citation = citations.get(citation_id)
            if citation is None:
                errors.append(f"claim {claim_id} references unknown citation {citation_id}")
                continue
            revision = source_revisions.get((citation["sourceId"], citation["revisionId"]))
            if claim["evidenceState"] == "current" and revision is not None:
                if revision["status"] != "current":
                    errors.append(
                        f"current claim {claim_id} uses non-current source revision "
                        f"{revision['sourceId']}@{revision['revisionId']} ({revision['status']})"
                    )
                source_authority = authorities.get(revision["authorityId"])
                if source_authority and source_authority["status"] != "current":
                    errors.append(
                        f"current claim {claim_id} uses {source_authority['status']} source authority "
                        f"{source_authority['authorityId']}"
                    )
        if (
            claim["evidenceState"] == "current"
            and authority is not None
            and authority["status"] != "current"
        ):
            errors.append(
                f"current claim {claim_id} uses {authority['status']} claim authority "
                f"{authority['authorityId']}"
            )

    for change_id, change in changes.items():
        claim_citation_ids: set[str] = set()
        for claim_id in change["claimIds"]:
            claim = claims.get(claim_id)
            if claim is None:
                errors.append(f"change {change_id} references unknown claim {claim_id}")
            else:
                claim_citation_ids.update(claim["citationIds"])
        for citation_id in change["citationIds"]:
            if citation_id not in citations:
                errors.append(f"change {change_id} references unknown citation {citation_id}")
            if citation_id not in claim_citation_ids:
                errors.append(
                    f"change {change_id} citation {citation_id} is unsupported by its claims"
                )
        for authority_id in change["authorityIds"]:
            if authority_id not in authorities:
                errors.append(f"change {change_id} references unknown authority {authority_id}")

    first_look = method_output["firstLook"]
    output_claim_ids: list[str] = []
    for output_claim in first_look["claims"]:
        claim_id = output_claim["claimId"]
        output_claim_ids.append(claim_id)
        claim = claims.get(claim_id)
        if claim is None:
            errors.append(f"First Look references unsupported claim {claim_id}")
            continue
        authority = authorities[claim["authorityId"]]
        expected = {
            "statement": claim["claim"],
            "evidenceState": claim["evidenceState"],
            "citationIds": claim["citationIds"],
            "authorityId": claim["authorityId"],
            "authorityStatus": authority["status"],
            "uncertainty": claim["uncertainty"],
        }
        for field_name, expected_value in expected.items():
            if output_claim[field_name] != expected_value:
                errors.append(
                    f"First Look claim {claim_id} {field_name} does not match input "
                    f"({output_claim[field_name]!r} != {expected_value!r})"
                )
    if len(output_claim_ids) != len(set(output_claim_ids)):
        errors.append("First Look contains duplicate claim IDs")
    if set(first_look["supportingClaimIds"]) != set(output_claim_ids):
        errors.append("First Look supportingClaimIds must exactly match its claim items")

    seen_changes: dict[str, str] = {}
    for category in CHANGE_CATEGORIES:
        for output_change in method_output["whatChanged"][category]:
            change_id = output_change["changeId"]
            if change_id in seen_changes:
                errors.append(
                    f"What Changed repeats {change_id} in {seen_changes[change_id]} and {category}"
                )
            seen_changes[change_id] = category
            change = changes.get(change_id)
            if change is None:
                errors.append(f"What Changed references unsupported change {change_id}")
                continue
            if change["category"] != category:
                errors.append(
                    f"What Changed places {change_id} in {category} instead of {change['category']}"
                )
            expected_statuses: list[str] = []
            for authority_id in change["authorityIds"]:
                status = authorities[authority_id]["status"]
                if status not in expected_statuses:
                    expected_statuses.append(status)
            expected = {
                "changeLevel": change["changeLevel"],
                "consequence": change["consequence"],
                "claimIds": change["claimIds"],
                "citationIds": change["citationIds"],
                "authorityStatuses": expected_statuses,
                "uncertainty": change["uncertainty"],
            }
            for field_name, expected_value in expected.items():
                if output_change[field_name] != expected_value:
                    errors.append(
                        f"What Changed item {change_id} {field_name} does not match input "
                        f"({output_change[field_name]!r} != {expected_value!r})"
                    )
    missing_changes = sorted(set(changes) - set(seen_changes))
    if missing_changes:
        errors.append(f"What Changed omits supplied changes: {missing_changes}")
    extra_changes = sorted(set(seen_changes) - set(changes))
    if extra_changes:
        errors.append(f"What Changed adds unsupported changes: {extra_changes}")

    next_decision = method_output["nextDecision"]
    if next_decision["ownerAuthorityId"] != investment_authority_id:
        errors.append(
            "Next Decision owner must be the input human investment authority "
            f"{investment_authority_id}"
        )
    next_claim_citations: set[str] = set()
    for claim_id in next_decision["supportingClaimIds"]:
        claim = claims.get(claim_id)
        if claim is None:
            errors.append(f"Next Decision references unsupported claim {claim_id}")
        else:
            next_claim_citations.update(claim["citationIds"])
    for citation_id in next_decision["citationIds"]:
        if citation_id not in citations:
            errors.append(f"Next Decision references unknown citation {citation_id}")
        if citation_id not in next_claim_citations:
            errors.append(
                f"Next Decision citation {citation_id} is unsupported by its supporting claims"
            )

    approval = method_output["approvalBoundary"]
    if approval["reviewOwnerAuthorityId"] != investment_authority_id:
        errors.append(
            "approval review owner must be the input human investment authority "
            f"{investment_authority_id}"
        )

    receipt = method_output["revisionReceipt"]
    if receipt["fundMethodRevisionId"] != fund_context["revisionId"]:
        errors.append(
            f"revision receipt uses Fund method {receipt['fundMethodRevisionId']} instead of "
            f"{fund_context['revisionId']}"
        )
    if set(receipt["changeIdsUsed"]) != set(changes):
        errors.append("revision receipt changeIdsUsed must exactly match supplied changes")

    used_citation_ids: set[str] = set(fund_context["citationIds"])
    for output_claim in first_look["claims"]:
        used_citation_ids.update(output_claim["citationIds"])
    for category in CHANGE_CATEGORIES:
        for output_change in method_output["whatChanged"][category]:
            used_citation_ids.update(output_change["citationIds"])
    used_citation_ids.update(next_decision["citationIds"])
    expected_revisions = {
        (
            citations[citation_id]["sourceId"],
            citations[citation_id]["revisionId"],
            source_revisions[
                (citations[citation_id]["sourceId"], citations[citation_id]["revisionId"])
            ]["status"],
        )
        for citation_id in used_citation_ids
        if citation_id in citations
        and (citations[citation_id]["sourceId"], citations[citation_id]["revisionId"])
        in source_revisions
    }
    actual_revisions = {
        (revision["sourceId"], revision["revisionId"], revision["status"])
        for revision in receipt["sourceRevisionsUsed"]
    }
    if actual_revisions != expected_revisions:
        errors.append(
            "revision receipt sourceRevisionsUsed must exactly match cited source revisions "
            f"(actual={sorted(actual_revisions)}, expected={sorted(expected_revisions)})"
        )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate an Embedded Deal Continuity v1 method run."
    )
    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        default=EXAMPLE_PATH,
        help="Complete method-run JSON; defaults to the public-neutral example.",
    )
    args = parser.parse_args()
    errors = validate_run(_json(args.path))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"Validated Embedded Deal Continuity v1 method run: {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
