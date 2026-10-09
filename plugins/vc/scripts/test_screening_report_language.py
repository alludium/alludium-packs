#!/usr/bin/env python3
"""Deterministic presentation-boundary tests; not a model-behaviour evaluation."""
import json
from pathlib import Path
import unittest
import yaml

from check_screening_report_language import check_language

ROOT = Path(__file__).resolve().parents[1]


class ScreeningLanguageTests(unittest.TestCase):
    def test_reader_facing_scenarios_preserve_citations_and_hidden_provenance(self):
        manifest = {"schemaVersion": 1, "sources": [{"artifactId": "source-123", "observedRevision": "1", "contentHash": "sha256:abc", "role": "project evidence"}], "unavailableSources": []}
        cases = [
            ("No active Fund has been confirmed for this Deal, so Fund fit is not assessed.", "Screening completed; please confirm a Fund to assess Fund fit."),
            ("Fund fit for North Star Fund I: stage is aligned; ownership remains unverified.", "Screening completed for North Star Fund I; confirm the ownership assumptions."),
            ("This is the first Screening Report; there is no earlier report to compare.", "First Screening Report created; customer references remain a gap."),
            ("The previous report's source history is unavailable, so changes in the supporting evidence cannot be determined.", "Screening Report refreshed; earlier source changes cannot be determined."),
        ]
        for prose, summary in cases:
            with self.subTest(prose=prose):
                html = f'<h2>Screening Report</h2><p>{prose}</p><p>The pitch deck (searchable) describes the product [S2].</p><a href="/artifacts/source-123?fund_id=fund-1">[S2] Pitch deck — source-123, sha256:abc</a><section hidden data-evidence-basis-manifest="v1"><pre>{json.dumps(manifest)}</pre><span>evidence-basis manifest; provider-searchable; fund_id</span></section>'
                self.assertEqual(check_language(html, summary), [])
                self.assertIn(json.dumps(manifest), html)

    def test_reported_leaks_are_rejected_in_report_and_summary(self):
        examples = [
            "Populate the Deal's exact active fund_id before any Fund-relative cheque assessment.",
            "Fund selection is unresolved because the persisted Deal fund_id is empty.",
            "[S2] is a provider-searchable PDF whose relevant content states…",
            "No prior Screening Report or evidence-basis manifest was available for comparison.",
            "Evidence-basis manifest included.",
            "Structured output: Saved to screening_report_artifact_id",
        ]
        for example in examples:
            with self.subTest(example=example):
                self.assertTrue(check_language(f"<p>{example}</p>", "Report created."))
                self.assertTrue(check_language("<p>Report</p>", example))

    def test_all_declared_fields_are_rejected_only_in_visible_content(self):
        task = yaml.safe_load((ROOT / "alludium/task-definition-templates/vc-workflows/generate-refresh-screening-report.yaml").read_text())
        keys = {field["key"] for direction in ("input", "output") for field in task["fields"][direction]}
        self.assertIn("existing_screening_report_artifact_id", keys)
        for key in keys:
            with self.subTest(key=key):
                self.assertTrue(check_language(f"<p>Missing {key}</p>", "Report ready."))
                self.assertTrue(check_language("<p>Report ready.</p>", f"Missing `{key}`"))
                self.assertEqual(check_language(f'<section hidden>{key}</section><a href="/source?{key}=123">Source</a>', "Report ready."), [])

    def test_runtime_fund_status_and_storage_scope_stay_out_of_visible_prose(self):
        # The 9 October local inactive-Fund run exposed the persisted status,
        # while the active-Fund report printed its source's storage scope.
        for value in ("closed_to_new_investments", "actively_investing", "PROJECT_SHARED", "TASK_RUN"):
            with self.subTest(value=value):
                self.assertTrue(check_language(f"<p>The current Fund record is {value}.</p>", "Report ready."))
                self.assertTrue(check_language("<p>Report ready.</p>", f"Current status: {value}"))
                self.assertEqual(check_language(f'<section hidden>{value}</section><a href="/source?status={value}">Source</a>', "Report ready."), [])
        self.assertEqual(check_language(
            "<p>The previously selected Fund is closed to new investments. No active Fund has been confirmed for this Deal, so Fund fit is not assessed.</p>",
            "Further company diligence is needed; confirm an active Fund. Open the generated Screening Report file.",
        ), [])

    def test_inline_formatting_entities_and_hidden_content(self):
        self.assertTrue(check_language("<p>fund_<span>id</span></p>", ""))
        self.assertTrue(check_language("<p>provider&#45;searchable</p>", ""))
        self.assertTrue(check_language('<img alt="provider-searchable pitch deck">', ""))
        self.assertEqual(check_language('<head><title>fund_id</title></head><!-- evidence-basis manifest --><div style="display: none"><p>fund_id</p></div><br><p>Pitch deck</p>', "Report created."), [])

    def test_adjacent_blocks_cells_and_breaks_preserve_word_boundaries(self):
        layouts = [
            "<p>Missing {term}</p><p>Confirm the Fund.</p>",
            "<p>Missing</p><p>{term}</p><p>Unconfirmed</p>",
            "<table><tr><td>{term}</td><td>Unconfirmed</td></tr></table>",
            "<table><tr><th>Missing</th><th>{term}</th></tr></table>",
            "<div>Missing</div><div>{term}</div><div>Unconfirmed</div>",
            "<ul><li>Missing</li><li>{term}</li><li>Unconfirmed</li></ul>",
            "<p>Missing<br>{term}<br/>Unconfirmed</p>",
            "<h2>Missing</h2>{term}<hr>Unconfirmed",
        ]
        for term in ("fund_id", "evidence-basis manifest", "provider-searchable"):
            for layout in layouts:
                with self.subTest(term=term, layout=layout):
                    findings = check_language(layout.format(term=term), "Report ready.")
                    self.assertEqual(len(findings), 1)
                    self.assertIn(term, findings[0])

    def test_hidden_blocks_do_not_split_visible_inline_words(self):
        html = '<div>fund_<section hidden><p>Internal provenance</p></section><span>id</span></div>'
        self.assertTrue(check_language(html, ""))
        for hidden in ('hidden', 'style="display: none"', 'style="visibility: hidden"'):
            with self.subTest(hidden=hidden):
                self.assertEqual(check_language(
                    f'<section {hidden}><p>fund_id</p><table><tr><td>provider-searchable</td></tr></table></section><p>Report ready.</p>',
                    "Report ready.",
                ), [])

    def test_generated_file_reference_does_not_require_a_fabricated_link(self):
        summary = "Cedar Harbor needs further validation.\n\n- Confirm customer references.\n\nOpen the generated Screening Report file."
        self.assertEqual(check_language("<p>Fund fit is not assessed.</p>", summary), [])
        task = yaml.safe_load((ROOT / "alludium/task-definition-templates/vc-workflows/generate-refresh-screening-report.yaml").read_text())
        instructions = task["definition"]["definitionJson"]["instructions"]
        text = instructions["executionInstructions"]
        self.assertIn("only when a tool returned a supported URL for that exact report", text)
        self.assertIn("Otherwise say \"Open the generated Screening Report file\"", text)
        self.assertIn("Never invent a URL, route, or URI scheme", text)
        self.assertNotIn("and a Screening Report link", " ".join(instructions["completionCriteria"]))

    def test_normal_deal_manager_completion_rejects_artifact_bookkeeping(self):
        # The 8 October Dev task had no definition binding. Its summary passed
        # the original terminology check despite exposing this internal section.
        summary = (
            "Prepared and saved the Screening Report.\n\n"
            "- **Artifact ID:** `9a74eadb-45f5-439e-af7e-90ddc308e93e`\n"
            "- **Recommendation:** Watch / Hold\n"
            "- **Next evidence needed:** customer references."
        )
        self.assertTrue(check_language("<p>No Fund fit assessed.</p>", summary))

    def test_summary_bookkeeping_sections_do_not_ban_report_source_provenance(self):
        report = '<h2>Source index</h2><p>Artifact ID: source-123; SHA-256: abc</p>'
        for label in ("Artifact ID", "artifact-ID", "Artifact IDs", "Structured output", "Saved field", "Validation checklist", "Bookkeeping"):
            for section in (f"- **{label}:** source-123", f"## {label}\nsource-123", f"{label}: source-123"):
                with self.subTest(section=section):
                    self.assertTrue(check_language(report, section))
        self.assertEqual(check_language(
            report,
            "Watch pending customer validation.\n\n- Confirm customer references.\n\n"
            "[Screening Report](/artifacts/report-123)",
        ), [])

    def test_screening_contract_preserves_routing_and_hidden_manifest(self):
        task = yaml.safe_load((ROOT / "alludium/task-definition-templates/vc-workflows/generate-refresh-screening-report.yaml").read_text())
        instructions = task["definition"]["definitionJson"]["instructions"]
        text = instructions["executionInstructions"]
        self.assertIn("exact active `vc.funds` record matching `fund_id`", text)
        self.assertIn("every visible report section and the task completion summary", text)
        self.assertIn("The final completion response must contain only:", text)
        self.assertIn("Saving the required structured task output is still mandatory", text)
        self.assertEqual(check_language("", " ".join(instructions["completionCriteria"])), [])
        self.assertIn("first report", text)
        self.assertIn("readable prior report with no usable source baseline", text)
        self.assertIn("hidden, preserving its schema and provenance fields", text)
        self.assertIn("preserve source citations, links, artifact IDs and hashes", text)
        fields = {field["key"]: field for field in task["fields"]["input"]}
        self.assertFalse(fields["fund_id"]["required"])
        self.assertEqual(task["fields"]["output"][0]["key"], "screening_report_artifact_id")
        shared = (ROOT / "skills/generate-or-refresh-living-report/SKILL.md").read_text()
        self.assertIn('data-evidence-basis-manifest="v1"', shared)
        for key in ('"schemaVersion"', '"sources"', '"artifactId"', '"observedRevision"', '"contentHash"', '"unavailableSources"'):
            self.assertIn(key, shared)


if __name__ == "__main__":
    unittest.main()
