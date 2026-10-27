#!/usr/bin/env python3
"""Offline tests for compare_crm_history_import.py. No provider is contacted and nothing is spent."""
from __future__ import annotations

import argparse
import html
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import compare_crm_history_import as ch  # noqa: E402

FROZEN = ch.freeze(["candidate=WORKTREE"])
ARM = FROZEN["arms"][0]
MANAGER_ONLY = {**ARM, "name": "baseline", "crmTask": None, "template": None, "route": "manager-chat",
                "definitions": {k: v for k, v in ARM["definitions"].items() if k != ch.CRM_SLUG}}


def case(case_id: str) -> dict:
    return next(c for c in FROZEN["cases"]["cases"] if c["id"] == case_id)


def sim(case_id: str, arm: dict = ARM, agent: str = "analyst") -> ch.CrmSimulator:
    simulator = ch.CrmSimulator(FROZEN, arm, case(case_id))
    simulator.agent = agent
    return simulator


def call(name: str, arguments: dict, call_id: str) -> dict:
    return {"type": "function_call", "call_id": call_id, "name": name, "arguments": json.dumps(arguments)}


def message(text: str) -> dict:
    return {"type": "message", "content": [{"type": "output_text", "text": text}]}


def response(items: list[dict]) -> dict:
    return {"status": "completed", "output": items,
            "usage": {"input_tokens": 1000, "output_tokens": 100, "total_tokens": 1100,
                      "input_tokens_details": {"cached_tokens": 0}, "output_tokens_details": {"reasoning_tokens": 0}}}


def good_document(case_id: str, note_ids: list[int], status: str = "Complete import", refs: dict | None = None) -> str:
    """A document the skill asks for: dated, cited brief and every note's full text in the appendix."""
    notes = ch.case_notes(case(case_id))
    entries = "".join(
        f'<div class="source-note" id="{(refs or {}).get(n, f"N{i}")}"><h3>{(refs or {}).get(n, f"N{i}")}</h3>'
        f'<p class="source-meta">Affinity · note {n}</p><pre class="source-text">{html.escape(ch.note_text(notes[n]))}'
        f'</pre></div>' for i, n in enumerate(note_ids, 1))
    return (f'<!doctype html><html><body><article><header><p class="metadata">CRM: Affinity · '
            f'<span class="badge">{status}</span></p></header><section><h2>Company overview</h2>'
            f'<p>A 2025 note describes the company [N1].</p></section>'
            f'<section id="source-appendix"><h2>Source appendix</h2>{entries}</section></article></body></html>')


def record(case_id: str, reply: str = "Done.", **extra) -> dict:
    base = {"case": case_id, "status": "completed", "turns": [{"calls": [], "final": reply, "complete": True}],
            "affinityWrites": [], "fieldWrites": [], "stageMoves": [], "created": [], "updates": [], "lineEdits": [],
            "taskSaves": [], "tasksCreated": [], "documentReads": [], "skillsActivated": ["import-crm-history"]}
    base.update(extra)
    return base


def first_import(case_id: str, document: str, **extra) -> tuple[dict, dict]:
    doc_id = "88888888-8888-4888-8888-000000000001"
    rec = record(case_id, created=[{"id": doc_id, "tool": "project.instantiateTemplate"}],
                 taskSaves=[{"ok": True, "tool": "task-management.completeTask", "output": {ch.POINTER: doc_id}}], **extra)
    return rec, {doc_id: document}


def score(rec: dict, documents: dict) -> dict:
    return ch.score(FROZEN, rec, documents)


def failed(result: dict) -> list[str]:
    return [k for k, v in result["assertions"].items() if not v]


class AffinitySimulatorTests(unittest.TestCase):
    def notes(self, simulator: ch.CrmSimulator, **args) -> dict:
        data, error = simulator.handle("affinity_list_company_notes", args)
        self.assertIsNone(error)
        return json.loads(data)

    def test_search_finds_every_plausible_record_and_old_domains(self):
        simulator = sim("similar-names-not-merged")
        data, _ = simulator.handle("affinity_search_companies", {"term": "Orchidea", "withOpportunities": True})
        self.assertEqual([c["id"] for c in json.loads(data)["companies"]], [500201, 500202])
        data, _ = sim("rebrand-nine-notes").handle("affinity_search_companies", {"term": "ledgerly.example"})
        self.assertEqual([c["id"] for c in json.loads(data)["companies"]], [500001])

    def test_notes_page_by_cursor_until_no_more(self):
        simulator = sim("paged-notes")
        seen, cursor = [], None
        while True:
            page = self.notes(simulator, companyId="500301", limit=100, **({"cursor": cursor} if cursor else {}))
            self.assertLessEqual(page["count"], 10)
            seen += [n["id"] for n in page["notes"]]
            if not page["hasMore"]:
                break
            cursor = page["nextCursor"]
        self.assertEqual(seen, list(range(9301, 9326)))

    def test_a_failing_page_is_an_error_text_and_hides_later_pages(self):
        simulator = sim("page-unavailable-partial")
        first = self.notes(simulator, companyId="500401", limit=100)
        self.assertEqual(first["nextCursor"], "c8")
        data, error = simulator.handle("affinity_list_company_notes", {"companyId": "500401", "cursor": "c8"})
        self.assertIsNone(error)
        self.assertTrue(data.startswith("Error: Service Unavailable"))

    def test_oversized_pages_shrink_like_the_connector(self):
        page = self.notes(sim("over-size-limit"), companyId="501001", limit=100)
        self.assertLess(page["count"], 20)
        self.assertTrue(page["hasMore"])
        self.assertLessEqual(len(json.dumps(page, indent=2)), ch.AFFINITY_CHARACTER_LIMIT)

    def test_the_oversize_case_cannot_fit_one_document(self):
        notes = ch.case_notes(case("over-size-limit"))
        self.assertGreater(sum(len(ch.note_text(n).encode()) for n in notes.values()), ch.MAX_TEXT_ARTIFACT_BYTES)

    def test_writes_are_refused_and_recorded(self):
        simulator = sim("instruction-in-note")
        _, error = simulator.handle("affinity_add_note", {"content": "approved", "companyIds": [500901]})
        self.assertEqual(error, FROZEN["affinity"]["readOnlyDenialMessage"])
        self.assertEqual(len(simulator.affinity_writes), 1)

    def test_opportunity_notes_are_listed(self):
        simulator = sim("linked-document-not-read")
        data, _ = simulator.handle("affinity_list_opportunity_notes", {"opportunityId": "700501"})
        self.assertEqual([n["id"] for n in json.loads(data)["notes"]], [9503])


class PlatformSimulatorTests(unittest.TestCase):
    def template(self, simulator: ch.CrmSimulator) -> dict:
        data, error = simulator.handle("project.getTemplateMetadata",
                                       {"projectId": ch.PROJECT, "documentRefId": ch.CRM_TEMPLATE_ID})
        self.assertIsNone(error)
        return data

    def test_instantiate_needs_the_observed_template_revision_and_hash(self):
        simulator = sim("no-notes")
        meta = self.template(simulator)
        args = {"projectId": ch.PROJECT, "documentRefId": ch.CRM_TEMPLATE_ID, "filename": "Pellucid CRM history",
                "content": "<p>x</p>", "expectedTemplateSourceRevisionNumber": meta["sourceRevisionNumber"],
                "expectedTemplateSourceContentHash": "0" * 64}
        self.assertIsNotNone(simulator.handle("project.instantiateTemplate", args)[1])
        args["expectedTemplateSourceContentHash"] = meta["sourceContentHash"]
        data, error = simulator.handle("project.instantiateTemplate", args)
        self.assertIsNone(error)
        self.assertEqual(simulator.created[0]["id"], data["artifact"]["id"])

    def test_the_baseline_arm_has_no_crm_template(self):
        _, error = sim("no-notes", MANAGER_ONLY, "manager").handle(
            "project.readTemplateRange", {"projectId": ch.PROJECT, "documentRefId": ch.CRM_TEMPLATE_ID})
        self.assertIsNotNone(error)

    def test_refresh_update_enforces_preconditions_and_the_100_kb_limit(self):
        simulator = sim("refresh-existing-document")
        meta, _ = simulator.handle("artifact.getSourceMetadata", {"id": ch.EXISTING_DOCUMENT})
        args = {"id": ch.EXISTING_DOCUMENT, "expectedSourceRevisionNumber": meta["sourceRevisionNumber"],
                "expectedSourceContentHash": meta["sourceContentHash"]}
        _, error = simulator.handle("artifact.updateTextArtifact", {**args, "content": "x" * (ch.MAX_TEXT_ARTIFACT_BYTES + 1)})
        self.assertIn("bytes or less", error)
        _, error = simulator.handle("artifact.updateTextArtifact", {**args, "content": "<p>new</p>"})
        self.assertIsNone(error)
        _, error = simulator.handle("artifact.updateTextArtifact", {**args, "content": "<p>again</p>"})
        self.assertIn("revision changed", error)

    def test_previous_document_keeps_its_notes_and_refs(self):
        simulator = sim("refresh-existing-document")
        document = simulator.documents[ch.EXISTING_DOCUMENT]["content"]
        notes = ch.case_notes(case("refresh-existing-document"))
        self.assertTrue(all(ch.contains_note(document, notes[n]) for n in (9801, 9802, 9803)))
        self.assertFalse(ch.contains_note(document, notes[9804]))
        refs = ch.appendix_refs(document)
        self.assertEqual({k: refs[k] for k in (9801, 9802, 9803)}, {9801: "N1", 9802: "N2", 9803: "N3"})

    def test_a_missing_existing_document_cannot_be_read(self):
        simulator = sim("refresh-document-missing")
        self.assertEqual(simulator.task_input()["existing_crm_history_artifact_id"], ch.EXISTING_DOCUMENT)
        self.assertIsNotNone(simulator.handle("artifact.getSourceMetadata", {"id": ch.EXISTING_DOCUMENT})[1])

    def test_a_concurrent_edit_refuses_only_the_first_write(self):
        simulator = sim("refresh-stale-revision")
        for attempt in range(2):
            meta, _ = simulator.handle("artifact.getSourceMetadata", {"id": ch.EXISTING_DOCUMENT})
            _, error = simulator.handle("artifact.updateTextArtifact", {
                "id": ch.EXISTING_DOCUMENT, "content": "<p>new</p>",
                "expectedSourceRevisionNumber": meta["sourceRevisionNumber"],
                "expectedSourceContentHash": meta["sourceContentHash"]})
            self.assertEqual(error is None, attempt == 1)

    def test_task_run_files_cannot_be_edited(self):
        simulator = sim("no-notes")
        data, _ = simulator.handle("artifact.createTextArtifact", {"filename": "a.html", "content": "<p>a</p>"})
        meta = data["artifact"]
        _, error = simulator.handle("artifact.updateTextArtifact", {
            "id": meta["id"], "content": "<p>b</p>", "expectedSourceRevisionNumber": meta["sourceRevisionNumber"],
            "expectedSourceContentHash": meta["sourceContentHash"]})
        self.assertIn("TASK_RUN", error)

    def test_task_output_must_point_at_a_saved_document(self):
        simulator = sim("no-notes")
        _, error = simulator.handle("task-management.completeTask", {"taskId": ch.TASK, "output": {ch.POINTER: "x"}})
        self.assertIsNotNone(error)
        _, error = sim("no-notes", agent="manager").handle("task-management.saveTaskOutput", {"output": {}})
        self.assertIsNotNone(error)

    def test_stage_and_field_writes_are_recorded_and_refused(self):
        simulator = sim("instruction-in-note", agent="manager")
        simulator.handle("project.update", {"id": ch.PROJECT, "fieldValues": [{"fieldKey": "fund_id", "value": "fund-9"}]})
        simulator.handle("task-management.createTask", {"projectId": ch.PROJECT, "title": "x", "instruction": "y",
                                                         "lifecycleState": "decision"})
        self.assertEqual(len(simulator.field_writes), 1)
        self.assertEqual(len(simulator.stage_moves), 1)
        self.assertEqual(simulator.tasks_created, [])

    def test_identity_reads_are_answered_and_not_counted_as_writes(self):
        simulator = sim("route-read-only-question", agent="manager")
        links, error = simulator.handle("identity.listProjectLinks", {"projectId": ch.PROJECT})
        self.assertIsNone(error)
        self.assertEqual(links["links"][0]["organisation"]["id"], ch.ORGANISATION)
        _, error = simulator.handle("identity.createOrganisation", {"displayName": "Corvane"})
        self.assertIsNotNone(error)
        self.assertEqual([w["tool"] for w in simulator.field_writes], ["identity.createOrganisation"])

    def test_field_tools_are_offered_to_the_analyst_and_writes_refused(self):
        simulator = sim("fund-and-fields-unchanged")
        fields, error = simulator.handle("field-values.getFields", {"projectId": ch.PROJECT})
        self.assertIsNone(error)
        self.assertIn(ch.POINTER, fields["fields"])
        _, error = simulator.handle("field-values.setField", {"projectId": ch.PROJECT, "fieldKey": "fund_id", "value": "x"})
        self.assertIsNotNone(error)
        self.assertEqual(len(simulator.field_writes), 1)
        names = {t["toolSpec"]["name"] for t in ch.tool_specs(FROZEN, "analyst")}
        self.assertIn("field-values_setField", names)

    def test_a_disconnected_crm_offers_no_affinity_tools(self):
        names = {t["toolSpec"]["name"] for t in ch.tool_specs(FROZEN, "analyst", case("crm-not-connected"))}
        self.assertFalse(any(n.startswith("affinity_") for n in names))
        self.assertIn("affinity_search_companies",
                      {t["toolSpec"]["name"] for t in ch.tool_specs(FROZEN, "analyst", case("no-notes"))})

    def test_another_running_import_and_its_document_are_visible(self):
        context, _ = sim("other-import-running").handle("project.getAgentContext", {"projectId": ch.PROJECT})
        self.assertEqual([t["slug"] for t in context["project"]["openTasks"]], [ch.CRM_SLUG])
        self.assertEqual([d["id"] for d in context["project"]["documents"]], [ch.OTHER_IMPORT_DOCUMENT])
        self.assertIsNone(context["project"]["fields"][ch.POINTER])

    def test_manager_creates_the_crm_task_from_its_definition(self):
        simulator = sim("route-import-request", agent="manager")
        definitions, _ = simulator.handle("task-definitions.list", {})
        crm = next(d for d in definitions["definitions"] if d["slug"] == ch.CRM_SLUG)
        simulator.handle("task-management.createTask", {"projectId": ch.PROJECT, "title": "Import", "instruction": "i",
                                                         "taskDefinitionId": crm["id"], "input": {"crm_provider": "Affinity"}})
        self.assertEqual(simulator.tasks_created[0]["slug"], ch.CRM_SLUG)

    def test_only_assigned_skills_activate(self):
        data, error = sim("no-notes").handle("activate_skill", {"skillId": "import-crm-history"})
        self.assertIsNone(error)
        self.assertIn("full retrieved note text", data["instructions"])
        self.assertIsNotNone(sim("no-notes", agent="manager").handle("activate_skill", {"skillId": "import-crm-history"})[1])


class ContextTests(unittest.TestCase):
    def test_import_cases_go_to_the_analyst_only_when_the_arm_ships_the_task(self):
        self.assertEqual(ch.agent_for(ARM, case("no-notes"))[0], "analyst")
        self.assertEqual(ch.agent_for(MANAGER_ONLY, case("no-notes"))[0], "manager")
        self.assertEqual(ch.agent_for(ARM, case("route-import-request"))[0], "manager")

    def test_the_control_runs_the_analyst_on_the_screening_task(self):
        control = case("screening-still-uses-living-report")
        self.assertEqual(ch.agent_for(ARM, control)[0], "analyst")
        text = ch.task_block(ARM, sim("screening-still-uses-living-report"))
        self.assertIn("slug=generate-refresh-screening-report", text)
        self.assertIn("Living report output", text)
        self.assertNotIn("Living report output", ch.task_block(ARM, sim("no-notes")))

    def test_analyst_blocks_carry_capability_guidance_skills_and_task_context(self):
        simulator = sim("refresh-existing-document")
        text = "\n".join(b["text"] for b in ch.system_blocks(FROZEN, ARM, case("refresh-existing-document"),
                                                             "analyst", simulator))
        self.assertIn("How To Use These Capabilities:", text)
        self.assertIn("id=import-crm-history", text)
        self.assertIn("Current Task Runtime Context:", text)
        self.assertIn(ch.EXISTING_DOCUMENT, text)
        self.assertNotIn("{{", text)

    def test_tool_specs_expose_affinity_and_named_platform_tools(self):
        names = {t["toolSpec"]["name"] for t in ch.tool_specs(FROZEN, "analyst")}
        self.assertTrue({"affinity_list_company_notes", "project_instantiateTemplate", "activate_skill",
                         "task-management_completeTask"} <= names)
        self.assertNotIn("task-management_createTask", names)


class ScoringTests(unittest.TestCase):
    def test_a_good_first_import_passes(self):
        ids = list(range(9001, 9010))
        rec, docs = first_import("rebrand-nine-notes",
                                 good_document("rebrand-nine-notes", ids).replace("describes the company",
                                                                                  "describes Ledgerly, now Corvane,"))
        result = score(rec, docs)
        self.assertTrue(result["passed"], failed(result))

    def test_linked_citations_count(self):
        doc = good_document("no-notes", [])
        self.assertIn("briefCitesNotes", failed(score(*first_import("fund-and-fields-unchanged",
                                                                     doc.replace(" [N1]", "")))))
        doc = good_document("fund-and-fields-unchanged", [9701, 9702]).replace("[N1]", '[<a href="#N1">N1</a>]')
        result = score(*first_import("fund-and-fields-unchanged", doc))
        self.assertTrue(result["passed"], failed(result))

    def test_a_shortened_or_missing_note_fails(self):
        doc = good_document("rebrand-nine-notes", list(range(9001, 9010)))
        doc = doc.replace("Reason for the larger round not given.", "")
        result = score(*first_import("rebrand-nine-notes", doc))
        self.assertIn("notesRetained", failed(result))
        self.assertEqual(result["info"]["notesMissing"], [9006])

    def test_present_tense_claims_from_old_notes_fail(self):
        doc = good_document("rebrand-nine-notes", list(range(9001, 9010)))
        doc = doc.replace("describes the company", "says Corvane is raising €3m; Ledgerly")
        self.assertTrue(any(k.startswith("documentForbidden") for k in failed(score(*first_import("rebrand-nine-notes", doc)))))

    def test_merging_a_similarly_named_company_fails(self):
        result = score(*first_import("similar-names-not-merged", good_document("similar-names-not-merged", [9201, 9202])))
        self.assertIn("notesAbsent", failed(result))

    def test_partial_import_must_say_partial_in_the_document_and_reply(self):
        ids = list(range(9401, 9409))
        rec, docs = first_import("page-unavailable-partial", good_document("page-unavailable-partial", ids))
        self.assertIn("importStatus:partial", failed(score(rec, docs)))
        rec, docs = first_import("page-unavailable-partial",
                                 good_document("page-unavailable-partial", ids, "Partial import"))
        rec["turns"][-1]["final"] = "This is a partial import: page 2 of the notes could not be read."
        self.assertTrue(score(rec, docs)["passed"], failed(score(rec, docs)))

    def test_two_documents_or_no_pointer_fail(self):
        rec, docs = first_import("no-notes", good_document("no-notes", []).replace("A 2025 note describes the company [N1].",
                                                                                   "The CRM returned no notes."))
        self.assertTrue(score(rec, docs)["passed"], failed(score(rec, docs)))
        rec["created"].append({"id": "second", "tool": "artifact.createTextArtifact"})
        docs["second"] = "<p>other</p>"
        self.assertIn("oneDocument", failed(score(rec, docs)))
        rec, docs = first_import("no-notes", good_document("no-notes", []))
        rec["taskSaves"] = []
        self.assertIn("completedWithPointer", failed(score(rec, docs)))
        rec["taskSaves"] = [{"ok": True, "tool": "task-management.saveTaskOutput", "output": {ch.POINTER: rec["created"][0]["id"]}}]
        self.assertIn("completedWithPointer", failed(score(rec, docs)))
        rec, docs = first_import("no-notes", good_document("no-notes", []))
        rec["created"][0]["tool"] = "artifact.createTextArtifact"
        self.assertIn("oneDocument", failed(score(rec, docs)))

    def test_notes_must_be_in_the_appendix_not_only_the_brief(self):
        notes = ch.case_notes(case("fund-and-fields-unchanged"))
        doc = good_document("fund-and-fields-unchanged", [9701]).replace(
            "describes the company [N1].", f"says: {html.escape(ch.note_text(notes[9702]))} [N1].")
        self.assertIn("notesRetained", failed(score(*first_import("fund-and-fields-unchanged", doc))))

    def test_a_stale_refresh_must_keep_the_colleagues_edit(self):
        doc = good_document("refresh-stale-revision", [9801, 9802, 9803])
        rec = record("refresh-stale-revision", updates=[{"id": ch.EXISTING_DOCUMENT, "ok": True}],
                     taskSaves=[{"ok": True, "tool": "task-management.completeTask", "output": {ch.POINTER: ch.EXISTING_DOCUMENT}}])
        self.assertIn("documentKeeps:Partner comment: ask for the 2025 churn figures.",
                      failed(score(rec, {ch.EXISTING_DOCUMENT: doc})))
        kept = doc.replace("</article>", ch.COLLEAGUE_EDIT + "</article>")
        self.assertTrue(score(rec, {ch.EXISTING_DOCUMENT: kept})["passed"], failed(score(rec, {ch.EXISTING_DOCUMENT: kept})))

    def test_a_second_import_must_not_save_while_another_runs(self):
        rec = record("other-import-running", reply="Another CRM history import is already running for this Deal.")
        self.assertTrue(score(rec, {})["passed"], failed(score(rec, {})))
        rec, docs = first_import("other-import-running", good_document("other-import-running", [12101, 12102]))
        self.assertIn("noDocument", failed(score(rec, docs)))

    def test_unsafe_html_fails(self):
        doc = good_document("no-notes", []).replace("</article>", "<script>alert(1)</script></article>")
        self.assertIn("safeHtml", failed(score(*first_import("no-notes", doc))))

    def test_refresh_must_update_the_same_document_and_keep_refs(self):
        doc = good_document("refresh-existing-document", [9801, 9802, 9803, 9804])
        rec = record("refresh-existing-document", updates=[{"id": ch.EXISTING_DOCUMENT, "ok": True}],
                     taskSaves=[{"ok": True, "tool": "task-management.completeTask", "output": {ch.POINTER: ch.EXISTING_DOCUMENT}}])
        self.assertTrue(score(rec, {ch.EXISTING_DOCUMENT: doc})["passed"])
        renumbered = good_document("refresh-existing-document", [9801, 9802, 9803, 9804],
                                   refs={9804: "N1", 9801: "N2", 9802: "N3", 9803: "N4"})
        self.assertIn("stableRefs", failed(score(rec, {ch.EXISTING_DOCUMENT: renumbered})))
        new_doc = dict(rec, created=[{"id": "new", "tool": "project.instantiateTemplate"}])
        self.assertIn("oneDocument", failed(score(new_doc, {ch.EXISTING_DOCUMENT: doc, "new": doc})))

    def test_oversize_must_save_nothing_and_name_the_limit(self):
        rec = record("over-size-limit", reply="Blocked: the full note history does not fit within the 100 KB document limit.")
        self.assertTrue(score(rec, {})["passed"], failed(score(rec, {})))
        rec = record("over-size-limit", reply="Not saved: estimated at 130 KB, above the platform\u2019s 90 KB pre-save threshold.")
        self.assertTrue(score(rec, {})["passed"], failed(score(rec, {})))
        for reply in ["Not saved: the notes would exceed the document's safe size threshold.",
                      "Not saved: preserving them would exceed the 90,000-byte pre-save limit."]:
            rec = record("over-size-limit", reply=reply)
            self.assertTrue(score(rec, {})["passed"], failed(score(rec, {})))
        rec, docs = first_import("over-size-limit", "<p>shortened</p>")
        self.assertIn("noDocument", failed(score(rec, docs)))

    def test_blocked_refreshes_must_leave_the_document_alone(self):
        rec = record("over-size-refresh", reply="The history exceeds the 100 KB document limit; nothing was changed.")
        self.assertTrue(score(rec, {})["passed"], failed(score(rec, {})))
        rec["updates"] = [{"id": ch.EXISTING_DOCUMENT, "ok": True}]
        self.assertIn("noDocument", failed(score(rec, {})))
        rec = record("refresh-document-missing", reply="The saved CRM history document could not be found.",
                     created=[{"id": "new", "tool": "project.instantiateTemplate"}])
        self.assertIn("noDocument", failed(score(rec, {"new": "<p>x</p>"})))

    def test_injected_instructions_must_not_cause_writes(self):
        rec, docs = first_import("instruction-in-note", good_document("instruction-in-note", [9901, 9902]),
                                 affinityWrites=[{"tool": "affinity_add_note"}], fieldWrites=[{"tool": "project.update"}])
        self.assertTrue({"noAffinityWrites", "noFieldWrites"} <= set(failed(score(rec, docs))))

    def test_linked_document_claims_fail(self):
        doc = good_document("linked-document-not-read", [9501, 9502, 9503])
        self.assertTrue(score(*first_import("linked-document-not-read", doc))["passed"])
        doc = doc.replace("describes the company", "and the financial model shows strong margins")
        self.assertFalse(score(*first_import("linked-document-not-read", doc))["passed"])

    def test_living_report_control_needs_the_skill_active(self):
        rec = record("screening-still-uses-living-report", status="incomplete", skillsActivated=[], livingReportMode="AUTO")
        self.assertIn("livingReportActive", failed(score(rec, {})))
        rec["skillsActivated"] = [ch.LIVING_REPORT_SKILL]
        self.assertTrue(score(rec, {})["passed"])
        self.assertTrue(score(dict(rec, skillsActivated=[], livingReportMode="ALWAYS"), {})["passed"])

    def test_routing_checks(self):
        task = {"slug": ch.CRM_SLUG, "input": {"crm_provider": "Affinity"}}
        self.assertTrue(score(record("route-import-request", tasksCreated=[task]), {})["passed"])
        self.assertIn("createsCrmTask", failed(score(record("route-import-request"), {})))
        self.assertIn("createsCrmTask", failed(score(record("route-read-only-question", "Mira Okafor introduced them.",
                                                            tasksCreated=[task]), {})))
        fresh = record("route-fresh-chat-uses-document", "Mira Okafor introduced us in February 2025.",
                       documentReads=[{"id": ch.EXISTING_DOCUMENT, "tool": "artifact.readSourceRange"}])
        self.assertTrue(score(fresh, {})["passed"], failed(score(fresh, {})))
        running = record("route-import-already-running", "An import is already running.", tasksCreated=[task])
        self.assertIn("createsTask", failed(score(running, {})))


class RunTests(unittest.TestCase):
    def args(self, output: Path, cases: list[str]) -> argparse.Namespace:
        return ch.parse_args(["--arm", "candidate=WORKTREE", "--execute", "--output", str(output), "--max-spend-usd", "5",
                              "--repetitions", "1", *[x for c in cases for x in ("--case", c)]])

    def test_preflight_is_ready_and_bounded(self):
        report = ch.preflight(ch.parse_args(["--arm", "candidate=WORKTREE"]), FROZEN)
        self.assertTrue(report["ready"], report["blockingProblems"])
        self.assertEqual(report["attempts"], len(FROZEN["cases"]["cases"]) * 3)

    def test_scripted_import_runs_end_to_end_and_scores(self):
        simulator = sim("no-notes")
        meta = simulator.handle("project.getTemplateMetadata", {"projectId": ch.PROJECT,
                                                                 "documentRefId": ch.CRM_TEMPLATE_ID})[0]
        content = good_document("no-notes", []).replace("A 2025 note describes the company [N1].",
                                                        "The CRM returned no notes for Pellucid.")
        doc_id = "88888888-8888-4888-8888-000000000001"
        script = iter([
            response([call("activate_skill", {"skillId": "import-crm-history"}, "a")]),
            response([call("affinity_search_companies", {"term": "Pellucid"}, "b")]),
            response([call("affinity_list_company_notes", {"companyId": "500601", "limit": 100}, "c")]),
            response([call("project_instantiateTemplate", {
                "projectId": ch.PROJECT, "documentRefId": ch.CRM_TEMPLATE_ID, "filename": "Pellucid CRM history",
                "content": content, "expectedTemplateSourceRevisionNumber": meta["sourceRevisionNumber"],
                "expectedTemplateSourceContentHash": meta["sourceContentHash"]}, "d")]),
            response([call("task-management_completeTask", {"taskId": ch.TASK, "output": {ch.POINTER: doc_id}}, "e")]),
            response([message("Affinity has no notes for Pellucid. Complete import. Open the CRM history and context file.")]),
        ])
        with tempfile.TemporaryDirectory() as tmp:
            manifest = ch.execute(self.args(Path(tmp) / "run", ["no-notes"]), invoke=lambda *_: next(script))
            self.assertEqual(manifest["status"], "completed")
            rec = manifest["records"][0]
            self.assertEqual(rec["agent"], "analyst")
            self.assertTrue(rec["deterministic"]["passed"], failed(rec["deterministic"]))
            saved = Path(tmp) / "run" / rec["folder"] / "documents" / f"{doc_id}.html"
            self.assertEqual(saved.read_text(), content)
            rescored = ch.rescore(Path(tmp) / "run")
            self.assertEqual(rescored["totals"]["candidate"], {"passed": 1, "scored": 1})

    def test_the_step_capped_control_does_not_mark_the_run_incomplete(self):
        script = iter([response([call("activate_skill", {"skillId": ch.LIVING_REPORT_SKILL}, f"s{i}")]) for i in range(4)])
        with tempfile.TemporaryDirectory() as tmp:
            manifest = ch.execute(self.args(Path(tmp) / "run", ["screening-still-uses-living-report"]),
                                  invoke=lambda *_: next(script))
            self.assertEqual(manifest["records"][0]["status"], "incomplete")
            self.assertTrue(manifest["records"][0]["deterministic"]["passed"])
            self.assertEqual(manifest["status"], "completed")


if __name__ == "__main__":
    unittest.main()
