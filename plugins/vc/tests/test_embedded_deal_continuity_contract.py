from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path
from typing import Any

import yaml


PACK_ROOT = Path(__file__).resolve().parents[1]
METHOD_ROOT = PACK_ROOT / "skills" / "embedded-deal-continuity" / "references"
SCHEMA_PATH = METHOD_ROOT / "method-run.schema.json"
EXAMPLE_PATH = METHOD_ROOT / "examples" / "public-neutral-s1-run.json"
RUBRIC_PATH = METHOD_ROOT / "evaluation-rubric.v1.yaml"
TASK_PATH = (
    PACK_ROOT
    / "alludium"
    / "task-definition-templates"
    / "vc-workflows"
    / "run-embedded-deal-continuity.yaml"
)
VALIDATOR_PATH = PACK_ROOT / "scripts" / "validate_embedded_deal_continuity.py"

spec = importlib.util.spec_from_file_location("deal_continuity_validator", VALIDATOR_PATH)
if spec is None or spec.loader is None:  # pragma: no cover - import guard
    raise RuntimeError(f"Unable to load {VALIDATOR_PATH}")
validator_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator_module)


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"{path} must contain an object")
    return value


class EmbeddedDealContinuityContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = load_json(SCHEMA_PATH)
        cls.example = load_json(EXAMPLE_PATH)
        cls.task = yaml.safe_load(TASK_PATH.read_text(encoding="utf-8"))
        cls.rubric = yaml.safe_load(RUBRIC_PATH.read_text(encoding="utf-8"))

    def errors(self, payload: dict[str, Any]) -> list[str]:
        return validator_module.validate_run(payload, self.schema)

    def assert_error_contains(self, payload: dict[str, Any], text: str) -> None:
        errors = self.errors(payload)
        self.assertTrue(errors, "Expected validation to fail")
        self.assertTrue(
            any(text in error for error in errors),
            f"Expected {text!r} in validation errors: {errors}",
        )

    def test_public_neutral_example_and_task_share_one_versioned_method(self) -> None:
        self.assertEqual(self.errors(self.example), [])
        contract = self.task["definition"]["definitionJson"]["methodContract"]
        self.assertEqual(
            contract,
            {
                "id": "vc.embedded-deal-continuity",
                "version": "1.0.0",
                "schemaPath": "skills/embedded-deal-continuity/references/method-run.schema.json",
                "inputDefinition": "#/$defs/input",
                "outputDefinition": "#/$defs/output",
            },
        )
        self.assertEqual(self.example["input"]["method"], self.example["output"]["method"])

    def test_all_three_outputs_and_six_change_buckets_are_present(self) -> None:
        output = self.example["output"]
        self.assertEqual(output["firstLook"]["title"], "First Look")
        self.assertEqual(output["whatChanged"]["title"], "What Changed")
        self.assertEqual(output["nextDecision"]["title"], "Next Decision")
        for category in validator_module.CHANGE_CATEGORIES:
            self.assertIn(category, output["whatChanged"])
            self.assertEqual(len(output["whatChanged"][category]), 1)

    def test_citations_and_revision_identity_are_mandatory(self) -> None:
        missing_citation = copy.deepcopy(self.example)
        missing_citation["input"]["evidenceClaims"][0]["citationIds"] = []
        self.assert_error_contains(missing_citation, "should be non-empty")

        missing_revision = copy.deepcopy(self.example)
        del missing_revision["input"]["citations"][0]["revisionId"]
        self.assert_error_contains(missing_revision, "revisionId")

        wrong_revision = copy.deepcopy(self.example)
        product_citation = next(
            citation
            for citation in wrong_revision["input"]["citations"]
            if citation["citationId"] == "cite-deck-v2-product"
        )
        product_citation["revisionId"] = "deck-v1"
        self.assert_error_contains(wrong_revision, "current claim claim-product-workflow uses non-current")

    def test_stale_authority_cannot_be_presented_as_current(self) -> None:
        stale_authority = copy.deepcopy(self.example)
        stale_authority["output"]["whatChanged"]["stale"][0]["authorityStatuses"] = [
            "current"
        ]
        self.assert_error_contains(stale_authority, "authorityStatuses does not match input")

    def test_unsupported_claims_fail_closed(self) -> None:
        unsupported = copy.deepcopy(self.example)
        unsupported["output"]["firstLook"]["claims"][0]["claimId"] = "claim-invented"
        self.assert_error_contains(unsupported, "First Look references unsupported claim")

    def test_change_omission_and_automatic_disposition_are_rejected(self) -> None:
        missing_change = copy.deepcopy(self.example)
        missing_change["output"]["whatChanged"]["unresolved"] = []
        self.assert_error_contains(missing_change, "What Changed omits supplied changes")

        disposition = copy.deepcopy(self.example)
        disposition["output"]["nextDecision"]["disposition"] = "invest"
        self.assert_error_contains(disposition, "Additional properties are not allowed")

    def test_human_authority_boundary_is_non_authoritative(self) -> None:
        authoritative = copy.deepcopy(self.example)
        authoritative["output"]["approvalBoundary"]["postureAuthoritative"] = True
        self.assert_error_contains(authoritative, "False was expected")

    def test_evaluation_rubric_covers_required_failures_and_prose_tie_break(self) -> None:
        criteria = {criterion["id"] for criterion in self.rubric["criteria"]}
        self.assertTrue(
            {
                "citation_correctness",
                "wrong_revision_use",
                "stale_authority_use",
                "unsupported_claims",
                "change_comprehension",
                "unresolved_state_visibility",
                "no_automated_investment_judgment",
                "human_authority_boundary",
            }.issubset(criteria)
        )
        self.assertEqual(self.rubric["comparison"]["baseline"], "strong_same_source_cited_prose")
        self.assertEqual(self.rubric["comparison"]["tieResult"], "prefer_cited_prose")
        self.assertEqual(
            self.rubric["comparison"]["unnecessaryComplexityResult"], "prefer_cited_prose"
        )


if __name__ == "__main__":
    unittest.main()
