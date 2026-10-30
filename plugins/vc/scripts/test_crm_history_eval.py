#!/usr/bin/env python3
"""Offline tests for compare_crm_history_import.py. No provider is contacted and nothing is spent."""
from __future__ import annotations

import argparse
import html
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

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


OVERVIEW_FILLER = ("The retrieved notes describe its product, early customers and our meetings with the founders; "
                   "current traction is unconfirmed.")


def good_document(case_id: str, note_ids: list[int], status: str = "Complete import", refs: dict | None = None) -> str:
    """A document the skill asks for: dated, cited brief and every note's full text in the appendix."""
    notes = ch.case_notes(case(case_id))
    holders = ch.note_holders(case(case_id))
    entries = "".join(
        f'<div class="source-note" id="{(refs or {}).get(n, f"N{i}")}"><h3>{(refs or {}).get(n, f"N{i}")}</h3>'
        f'<p class="source-meta">Affinity · record {holders[n]} · note {n}</p><pre class="source-text">{html.escape(ch.note_text(notes[n]))}'
        f'</pre></div>' for i, n in enumerate(note_ids, 1))
    return (f'<!doctype html><html><body><article><header><p class="metadata">CRM: Affinity · '
            f'<span class="badge">{status}</span></p></header><section><h2>Company overview</h2>'
            f'<p>A 2025 note describes the company [N1]. {OVERVIEW_FILLER}</p></section>'
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

    def test_enriched_people_come_inline_on_the_company_record(self):
        data, error = sim("profile-people-labelled").handle(
            "affinity_get_company", {"companyId": "503301", "fieldTypes": ["enriched"]})
        self.assertIsNone(error)
        fields = {f["name"]: f for f in json.loads(data)["fields"]}
        self.assertEqual(fields["People"]["value"]["type"], "person-multi")
        self.assertEqual([p["lastName"] for p in fields["People"]["value"]["data"]], ["Voss", "Pell"])
        plain, _ = sim("profile-people-labelled").handle("affinity_get_company", {"companyId": "503301"})
        self.assertNotIn("fields", json.loads(plain))

    def test_a_similar_name_with_another_domain_is_the_only_search_result(self):
        simulator = sim("similar-name-other-domain")
        data, _ = simulator.handle("affinity_search_companies", {"term": "Fernway"})
        self.assertEqual([c["id"] for c in json.loads(data)["companies"]], [503201, 503202])
        data, _ = simulator.handle("affinity_search_companies", {"term": "fernway.example"})
        self.assertEqual(json.loads(data)["companies"], [])

    def test_an_interaction_filter_hides_a_notes_only_record(self):
        simulator = sim("domain-as-name-no-interactions")
        data, _ = simulator.handle("affinity_search_companies", {"term": "tallowmere.ai"})
        self.assertEqual([c["id"] for c in json.loads(data)["companies"]], [503403])
        for flag in ("withInteractionDates", "withInteractionPersons"):
            data, _ = simulator.handle("affinity_search_companies", {"term": "tallowmere.ai", flag: True})
            self.assertEqual(json.loads(data)["companies"], [])
            data, _ = simulator.handle("affinity_search_companies", {"term": "tallowmere", flag: True})
            self.assertEqual([c["id"] for c in json.loads(data)["companies"]], [503401, 503402])

    def test_search_pages_by_token(self):
        simulator = sim("search-second-page")
        first = json.loads(simulator.handle("affinity_search_companies", {"term": "Tarnwell"})[0])
        self.assertEqual([c["id"] for c in first["companies"]], [502201])
        self.assertTrue(first["hasMore"])
        second = json.loads(simulator.handle("affinity_search_companies",
                                             {"term": "Tarnwell", "pageToken": first["nextPageToken"]})[0])
        self.assertEqual([c["id"] for c in second["companies"]], [502202])
        self.assertFalse(second["hasMore"])

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
        self.assertEqual(len(simulator.refused_creations), 1)
        self.assertNotIn("content", simulator.refused_creations[0]["input"])
        args["expectedTemplateSourceContentHash"] = meta["sourceContentHash"]
        data, error = simulator.handle("project.instantiateTemplate", args)
        self.assertIsNone(error)
        self.assertEqual(simulator.created[0]["id"], data["artifact"]["id"])

    def test_the_task_guides_are_readable(self):
        simulator = sim("no-notes")
        for ref in ch.GUIDE_PATHS:
            data, error = simulator.handle("project.readTemplateRange",
                                           {"projectId": ch.PROJECT, "documentRefId": ref, "startLine": 1, "endLine": 5})
            self.assertIsNone(error, ref)
            self.assertTrue(data["content"])
        args = {"projectId": ch.PROJECT, "documentRefId": "vc.document.template_use_guidance", "filename": "x",
                "content": "<p>x</p>"}
        self.assertIsNotNone(simulator.handle("project.instantiateTemplate", args)[1])

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

    def test_a_disconnected_crm_fails_on_the_first_affinity_call(self):
        # As on Platform, the tools of a disconnected app can be listed and activated; the call itself fails.
        simulator = sim("crm-not-connected")
        names = {t["toolSpec"]["name"] for t in ch.tool_specs(FROZEN, "analyst", case("crm-not-connected"), simulator)}
        self.assertFalse(any(n.startswith("affinity_") for n in names))
        listed = simulator.handle("tools_list_available", {"applicationExternalId": "affinity-mcp-server", "limit": 50})[0]
        self.assertIn("affinity_search_companies", [t["name"] for t in listed["result"]["tools"]])
        activated, error = simulator.handle("tool_activate", {"toolExternalId": "affinity_search_companies"})
        self.assertIsNone(error)
        self.assertTrue(activated["result"]["activated"])
        self.assertIn("affinity_search_companies",
                      {t["toolSpec"]["name"] for t in ch.tool_specs(FROZEN, "analyst", case("crm-not-connected"), simulator)})
        _, error = simulator.handle("affinity_search_companies", {"term": "Pellucid"})
        self.assertIn("not connected", error)

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


class ProcessingTests(unittest.TestCase):
    def test_a_saved_document_processes_until_waited_for(self):
        s = sim("refresh-processing-after-save")
        meta, _ = s.handle("artifact.getSourceMetadata", {"id": ch.EXISTING_DOCUMENT})
        self.assertEqual(meta["processingStatus"], "READY")
        result, error = s.handle("artifact.updateTextArtifact", {
            "id": ch.EXISTING_DOCUMENT, "content": "<p>new</p>", "expectedSourceRevisionNumber": meta["sourceRevisionNumber"],
            "expectedSourceContentHash": meta["sourceContentHash"]})
        self.assertIsNone(error)
        self.assertEqual(result["artifact"]["processingStatus"], "PROCESSING")
        s.handle("artifact.waitForArtifactsReady", {"artifactIds": [ch.EXISTING_DOCUMENT]})
        meta, _ = s.handle("artifact.getSourceMetadata", {"id": ch.EXISTING_DOCUMENT})
        self.assertEqual(meta["processingStatus"], "READY")


class StreamingInvokeTests(unittest.TestCase):
    class FakeStream:
        def __init__(self, lines):
            self.lines = [line.encode() for line in lines]

        def __enter__(self):
            return self.lines

        def __exit__(self, *exc):
            return False

    def invoke(self, lines):
        original, key = ch.urllib.request.urlopen, os.environ.get("OPENAI_API_KEY")
        sent = {}

        def fake(request, timeout):
            sent["body"] = json.loads(request.data)
            return self.FakeStream(lines)
        ch.urllib.request.urlopen = fake
        os.environ["OPENAI_API_KEY"] = "test-key"
        try:
            return ch.streaming_openai_invoke({"model": "m", "input": []}, None, {"endpoint": "https://x", "timeout": 60}), sent
        finally:
            ch.urllib.request.urlopen = original
            if key is None:
                os.environ.pop("OPENAI_API_KEY", None)
            else:
                os.environ["OPENAI_API_KEY"] = key

    def test_returns_the_completed_response(self):
        final = {"id": "r1", "status": "completed", "output": [], "usage": {"input_tokens": 1}}
        result, sent = self.invoke(["event: response.created", 'data: {"type": "response.created"}', "",
                                    'data: {"type": "response.output_text.delta", "delta": "x"}',
                                    "data: " + json.dumps({"type": "response.completed", "response": final})])
        self.assertEqual(result, final)
        self.assertTrue(sent["body"]["stream"])

    def test_failed_or_cut_streams_raise(self):
        with self.assertRaises(ch.base.ProviderError):
            self.invoke(['data: {"type": "response.failed", "response": {"status": "failed"}}'])
        with self.assertRaises(ch.base.ProviderError):
            self.invoke(['data: {"type": "response.created"}'])


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

    def test_tool_specs_expose_discovery_and_named_platform_tools(self):
        names = {t["toolSpec"]["name"] for t in ch.tool_specs(FROZEN, "analyst", case("no-notes"), sim("no-notes"))}
        self.assertTrue({"tools_search_available", "tools_list_available", "tool_activate",
                         "project_instantiateTemplate", "activate_skill", "task-management_completeTask"} <= names)
        self.assertNotIn("task-management_createTask", names)
        # As on Dev, the Affinity tools start inactive and must be found and activated.
        self.assertFalse(any(n.startswith("affinity_") for n in names))


class ToolDiscoveryTests(unittest.TestCase):
    def test_search_cuts_the_company_search_tool_below_its_live_position(self):
        # #4841: missing from all 11 Dev searches and at the default limit locally; found with `limit: 50`.
        simulator = sim("no-notes")
        for query in ["affinity_search_companies", "Affinity search companies", "affinity", None]:
            for limit, present in [(None, False), (20, False), (24, False), (25, True), (50, True)]:
                arguments = {**({"query": query} if query else {}), **({"limit": limit} if limit else {})}
                data, error = simulator.handle("tools_search_available", arguments)
                self.assertIsNone(error)
                names = [t["name"] for t in data["result"]]
                self.assertEqual("affinity_search_companies" in names, present, (query, limit))
                self.assertIn("affinity_list_company_notes", names)
        self.assertEqual(len(simulator.tool_discovery), 20)

    def test_listing_the_affinity_app_pages_through_every_tool(self):
        simulator = sim("no-notes")
        seen, cursor = [], None
        while True:
            data, _ = simulator.handle("tools_list_available", {"applicationExternalId": "affinity-mcp-server",
                                                                 "limit": 10, **({"cursor": cursor} if cursor else {})})
            seen += [t["name"] for t in data["result"]["tools"]]
            cursor = data["result"].get("nextCursor")
            if not cursor:
                break
        self.assertEqual(sorted(seen), sorted(t["name"] for t in FROZEN["affinity"]["tools"]))
        self.assertEqual(simulator.handle("tools_list_available",
                                          {"applicationExternalId": "slack_v2"})[0]["result"]["tools"], [])

    def test_activation_by_external_id_makes_a_tool_callable(self):
        simulator = sim("no-notes")
        self.assertEqual(simulator.active_affinity_tools(), [])
        data, error = simulator.handle("tool_activate", {"toolExternalId": "affinity_search_companies"})
        self.assertIsNone(error)
        self.assertEqual(data["result"]["toolExternalId"], "affinity_search_companies")
        self.assertEqual([t["name"] for t in simulator.active_affinity_tools()], ["affinity_search_companies"])
        listed = simulator.handle("tools_list_available", {"applicationExternalId": "affinity-mcp-server", "limit": 50})[0]
        notes = next(t for t in listed["result"]["tools"] if t["name"] == "affinity_list_company_notes")
        self.assertTrue(simulator.handle("tool_activate", {"toolId": notes["id"]})[0]["result"]["activated"])
        refused, error = simulator.handle("tool_activate", {"toolExternalId": "affinity_made_up"})
        self.assertIsNone(error)
        self.assertFalse(refused["result"]["activated"])

    def test_activation_by_name_alone_is_refused_in_a_deal(self):
        # #4841 local probe: 9 of 9 `toolName`-only activations were refused in a locked Deal project.
        simulator = sim("no-notes")
        data, error = simulator.handle("tool_activate", {"toolName": "affinity_search_companies"})
        self.assertIsNone(error)
        self.assertEqual(data["result"]["code"], "LOCKED_PROJECT_AGENT_SELECTION_FORBIDDEN")
        self.assertFalse(data["result"]["activated"])
        self.assertEqual(simulator.active_affinity_tools(), [])

    def test_a_case_can_hand_the_tools_over_directly(self):
        direct = {**case("no-notes"), "affinityToolsInactive": False}
        names = {t["toolSpec"]["name"] for t in ch.tool_specs(FROZEN, "analyst", direct)}
        self.assertIn("affinity_search_companies", names)
        self.assertNotIn("tool_activate", names)


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

    def test_citations_must_resolve_to_appendix_entries(self):
        ids = list(range(9001, 9010))
        doc = good_document("rebrand-nine-notes", ids).replace("describes the company", "describes Ledgerly, now Corvane,")
        result = score(*first_import("rebrand-nine-notes", doc.replace("[N1]", "[N999]")))
        self.assertIn("citationsResolve", failed(result))
        self.assertEqual(["N999"], result["info"]["citationsUnresolved"])
        self.assertIn("citationsResolve", failed(score(*first_import("rebrand-nine-notes",
                                                                      doc.replace("[N1]", "[N1, N10]")))))
        self.assertIn("citationsResolve", failed(score(*first_import("rebrand-nine-notes",
                                                                      doc.replace("[N1]", "[N8\u2013N10]")))))
        result = score(*first_import("rebrand-nine-notes", doc.replace("[N1]", "[N1, N3\u2013N5]")))
        self.assertTrue(result["passed"], failed(result))

    def test_notes_name_the_record_they_came_from(self):
        ids = list(range(9101, 9106))
        doc = good_document("secondary-record-notes", ids)
        result = score(*first_import("secondary-record-notes", doc))
        self.assertTrue(result["passed"], failed(result))
        # Same company, but the notes were read from 500102, not the empty 500101 record.
        result = score(*first_import("secondary-record-notes", doc.replace("record 500102", "record 500101")))
        self.assertIn("notesAttributed", failed(result))
        self.assertEqual(result["info"]["notesMisattributed"], ids)

    def test_the_brief_must_be_filled_in(self):
        doc = good_document("fund-and-fields-unchanged", [9701, 9702])
        self.assertIn("briefSubstantive", failed(score(*first_import("fund-and-fields-unchanged",
                                                                      doc.replace(OVERVIEW_FILLER, "")))))
        placeholder = doc.replace("</section>", "<p>As far as the retrieved records support it.</p></section>", 1)
        self.assertTrue(score(*first_import("fund-and-fields-unchanged", placeholder))["passed"])
        placeholder = doc.replace("</section>", "<p>as far as the retrieved records support it</p></section>", 1)
        self.assertIn("briefSubstantive", failed(score(*first_import("fund-and-fields-unchanged", placeholder))))

    def test_profile_people_must_not_be_credited_to_notes(self):
        doc = good_document("profile-people-labelled", [12501, 12502])
        self.assertTrue(score(*first_import("profile-people-labelled", doc))["passed"])
        labelled = doc.replace("</section>", "<p>Affinity's company profile lists Hanna Voss and Jonas Pell.</p></section>", 1)
        self.assertTrue(score(*first_import("profile-people-labelled", labelled))["passed"])
        separate = doc.replace("</section>", "<p>Affinity's company profile lists Hanna Voss; the notes report "
                               "30 sites [N1].</p></section>", 1)
        self.assertTrue(score(*first_import("profile-people-labelled", separate))["passed"])
        for claim in ("<p>The notes name Hanna Voss as a founder.</p>",
                      "<p>The team includes Jonas Pell [N2].</p>"):
            wrong = doc.replace("</section>", claim + "</section>", 1)
            self.assertTrue([k for k in failed(score(*first_import("profile-people-labelled", wrong)))
                             if k.startswith("documentForbidden:")], claim)

    def test_an_interaction_filtered_search_fails_every_case(self):
        doc = good_document("domain-as-name-no-interactions", [12601])
        rec, docs = first_import("domain-as-name-no-interactions", doc)
        self.assertTrue(score(rec, docs)["passed"], failed(score(rec, docs)))
        rec["interactionFilterSearches"] = [{"turn": 1, "input": {"term": "tallowmere", "withInteractionDates": True}}]
        self.assertIn("noInteractionFilter", failed(score(rec, docs)))

    def test_list_people_and_field_reads_are_recorded_and_fail_every_case(self):
        simulator = sim("domain-as-name-no-interactions")
        for tool in FROZEN["affinity"]["outOfScopeReadTools"]:
            data, error = simulator.handle(tool, {"companyId": "503403"})
            self.assertIsNone(error)
            self.assertEqual(json.loads(data)["data"], [])
        self.assertEqual([r["tool"] for r in simulator.out_of_scope_reads], FROZEN["affinity"]["outOfScopeReadTools"])
        self.assertIn("affinity_get_company_list_entries", FROZEN["affinity"]["outOfScopeReadTools"])
        doc = good_document("domain-as-name-no-interactions", [12601])
        rec, docs = first_import("domain-as-name-no-interactions", doc)
        self.assertTrue(score(rec, docs)["passed"], failed(score(rec, docs)))
        rec["outOfScopeReads"] = [{"turn": 1, "tool": "affinity_get_company_list_entries", "input": {"companyId": "503403"}}]
        self.assertIn("noOutOfScopeReads", failed(score(rec, docs)))

    def test_a_refused_template_copy_fails_even_after_a_retry(self):
        doc = good_document("no-notes", [])
        rec, docs = first_import("no-notes", doc)
        self.assertNotIn("oneDocument", failed(score(rec, docs)))
        rec["refusedCreations"] = [{"turn": 1, "input": {"expectedTemplateSourceContentHash": "0" * 64}}]
        self.assertIn("oneDocument", failed(score(rec, docs)))

    def test_profile_regexes_allow_correct_statements(self):
        doc = good_document("profile-people-labelled", [12501, 12502])
        for claim in ("<p>No retrieved note mentions Hanna Voss or Jonas Pell; Affinity's company profile lists them.</p>",
                      "<p>The notes say nothing about the team; Affinity's company profile lists Hanna Voss.</p>"):
            ok = doc.replace("</section>", claim + "</section>", 1)
            self.assertTrue(score(*first_import("profile-people-labelled", ok))["passed"], claim)
        for claim in ("<p>Jonas Pell is CTO [N1, N2].</p>", "<p>According to [N1], Hanna Voss is the CTO.</p>"):
            wrong = doc.replace("</section>", claim + "</section>", 1)
            self.assertTrue([k for k in failed(score(*first_import("profile-people-labelled", wrong)))
                             if k.startswith("documentForbidden:")], claim)

    def test_blocked_reply_phrasings(self):
        for reply in ("I was unable to find Fernway in Affinity.", "I wasn't able to confidently identify Fernway.",
                      "None of the Affinity records matches Fernway."):
            rec = record("similar-name-other-domain", reply=reply)
            self.assertTrue(score(rec, {})["passed"], reply)

    def test_importing_a_near_match_fails_the_blocked_case(self):
        rec = record("similar-name-other-domain",
                     reply="I could not confidently find Fernway in Affinity: the closest record, Fernway Studio "
                           "(fernwaystudio.example), has another domain. Nothing was saved.")
        self.assertTrue(score(rec, {})["passed"], failed(score(rec, {})))
        doc = good_document("similar-name-other-domain", [12401])
        self.assertIn("noDocument", failed(score(*first_import("similar-name-other-domain", doc))))

    def test_case_facts_must_be_in_the_brief(self):
        ids = list(range(9001, 9010))
        doc = good_document("rebrand-nine-notes", ids)
        # Both names appear in the retained notes, but the brief never mentions them.
        self.assertIn("documentMentions:Ledgerly", failed(score(*first_import("rebrand-nine-notes", doc))))

    def test_a_note_link_must_stay_in_the_appendix(self):
        doc = good_document("linked-document-not-read", [9501, 9502, 9503]).replace(
            "</section>", "<p>Linked, not read: https://dataroom.example/haldane-series-a</p></section>", 1)
        self.assertTrue(score(*first_import("linked-document-not-read", doc))["passed"])
        notes = ch.case_notes(case("linked-document-not-read"))
        links = set().union(*(ch.note_links(notes[n]) for n in (9501, 9502, 9503)))
        self.assertTrue(links)
        stripped = doc
        for link in links:
            stripped = stripped.replace(link, "")
        self.assertIn("notesRetained", failed(score(*first_import("linked-document-not-read", stripped))))

    def test_a_note_link_kept_as_a_link_in_the_appendix_counts(self):
        doc = good_document("linked-document-not-read", [9501, 9502, 9503])
        self.assertIn("documentMentions:dataroom\\.example/haldane-series-a",
                      failed(score(*first_import("linked-document-not-read", doc))))
        doc = doc.replace("</section></article>", '<p><a href="https://dataroom.example/haldane-series-a">data room</a>'
                          "</p></section></article>")
        result = score(*first_import("linked-document-not-read", doc))
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

    def test_an_import_stops_when_a_crm_history_document_already_exists(self):
        rec = record("other-import-running", reply="This Deal already has a CRM history document, so the initial "
                     "import is blocked. Ask for a refresh to update it.")
        self.assertTrue(score(rec, {})["passed"], failed(score(rec, {})))
        rec, docs = first_import("other-import-running", good_document("other-import-running", [12101, 12102]))
        self.assertIn("noDocument", failed(score(rec, docs)))

    def test_another_open_import_task_alone_does_not_block_an_import(self):
        blocked = record("other-import-open-no-document", reply="Another CRM history import is already running for this Deal.")
        self.assertFalse(score(blocked, {})["passed"])
        rec, docs = first_import("other-import-open-no-document", good_document("other-import-open-no-document", [12151, 12152]))
        self.assertTrue(score(rec, docs)["passed"], failed(score(rec, docs)))

    def test_an_open_import_task_without_a_document_is_visible(self):
        context, _ = sim("other-import-open-no-document").handle("project.getAgentContext", {"projectId": ch.PROJECT})
        self.assertEqual([t["slug"] for t in context["project"]["openTasks"]], [ch.CRM_SLUG])
        self.assertEqual(context["project"]["documents"], [])

    def test_a_saved_document_above_the_update_limit_fails(self):
        ids = list(range(9001, 9010))
        doc = good_document("rebrand-nine-notes", ids).replace("describes the company", "describes Ledgerly, now Corvane,")
        big = doc.replace("</article>", "<p>" + "x" * ch.MAX_TEXT_ARTIFACT_BYTES + "</p></article>")
        self.assertIn("withinSizeLimit", failed(score(*first_import("rebrand-nine-notes", big))))

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
        twice = dict(rec, updates=[{"id": ch.EXISTING_DOCUMENT, "ok": True}] * 2)
        self.assertIn("oneDocument", failed(score(twice, {ch.EXISTING_DOCUMENT: doc})))
        edited = dict(rec, lineEdits=[{"id": ch.EXISTING_DOCUMENT, "ok": True}])
        self.assertIn("oneDocument", failed(score(edited, {ch.EXISTING_DOCUMENT: doc})))
        edits_only = dict(rec, updates=[], lineEdits=[{"id": ch.EXISTING_DOCUMENT, "ok": True}])
        self.assertIn("oneDocument", failed(score(edits_only, {ch.EXISTING_DOCUMENT: doc})))
        refused_then_saved = dict(rec, updates=[{"id": ch.EXISTING_DOCUMENT, "ok": False},
                                                {"id": ch.EXISTING_DOCUMENT, "ok": True}])
        self.assertTrue(score(refused_then_saved, {ch.EXISTING_DOCUMENT: doc})["passed"])

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
        doc = good_document("linked-document-not-read", [9501, 9502, 9503]).replace(
            "</section>", "<p>Linked, not read: https://dataroom.example/haldane-series-a</p></section>", 1)
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
            response([call("tool_activate", {"toolExternalId": "affinity_search_companies"}, "a1"),
                      call("tool_activate", {"toolExternalId": "affinity_list_company_notes"}, "a2")]),
            response([call("affinity_search_companies", {"term": "Pellucid"}, "b")]),
            response([call("affinity_list_company_notes", {"companyId": "500601", "limit": 100}, "c")]),
            response([call("project_instantiateTemplate", {
                "projectId": ch.PROJECT, "documentRefId": ch.CRM_TEMPLATE_ID, "filename": "Pellucid CRM history",
                "content": content, "expectedTemplateSourceRevisionNumber": meta["sourceRevisionNumber"],
                "expectedTemplateSourceContentHash": meta["sourceContentHash"]}, "d")]),
            response([call("task-management_completeTask", {"output": {ch.POINTER: doc_id}}, "e")]),
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

    def test_the_dev_search_only_path_ends_without_an_import_and_fails(self):
        # #4841 0.6.46 Dev run: four tool searches, no company-search tool, "unavailable", nothing saved.
        queries = ["Affinity search companies get company list company notes", "Affinity CRM companies notes",
                   "affinity_search_companies", "search company Affinity CRM"]
        script = iter([response([call("activate_skill", {"skillId": "import-crm-history"}, "a")]),
                       *[response([call("tools_search_available", {"query": q}, f"q{i}")]) for i, q in enumerate(queries)],
                       response([call("affinity_search_companies", {"term": "Pellucid"}, "x")]),
                       response([message("The task is blocked: the required Affinity company-search capability is "
                                         "unavailable.")])])
        with tempfile.TemporaryDirectory() as tmp:
            rec = ch.execute(self.args(Path(tmp) / "run", ["no-notes"]), invoke=lambda *_: next(script))["records"][0]
            self.assertEqual([c["tool"] for c in rec["toolDiscovery"]], ["tools_search_available"] * 4)
            self.assertEqual(rec["activatedTools"], [])
            self.assertFalse(rec["deterministic"]["passed"])
            self.assertTrue({"noInvalidToolCalls", "oneDocument", "completedWithPointer"} <=
                            set(failed(rec["deterministic"])))

    def test_listing_then_activating_reaches_affinity(self):
        script = iter([
            response([call("tools_list_available", {"applicationExternalId": "affinity-mcp-server", "limit": 50}, "l")]),
            response([call("tool_activate", {"toolExternalId": "affinity_search_companies"}, "a")]),
            response([call("affinity_search_companies", {"term": "Pellucid"}, "b")]),
            response([message("Stopping here.")])])
        with tempfile.TemporaryDirectory() as tmp:
            rec = ch.execute(self.args(Path(tmp) / "run", ["no-notes"]), invoke=lambda *_: next(script))["records"][0]
            search = [c for t in rec["turns"] for c in t["calls"] if c["name"] == "affinity_search_companies"]
            self.assertEqual(len(search), 1)
            self.assertIsNone(search[0]["error"])
            self.assertEqual(rec["activatedTools"], ["affinity_search_companies"])

    def test_activating_by_name_alone_never_reaches_affinity(self):
        # The pre-fix skill's path in a Deal: each `toolName` activation is refused, and after three
        # activation-only steps Platform withdraws `tool_activate` for the rest of the turn.
        sent = []
        script = iter([*[response([call("tool_activate", {"toolName": "affinity_search_companies"}, f"a{i}")])
                          for i in range(3)],
                       response([call("tool_activate", {"toolExternalId": "affinity_search_companies"}, "late")]),
                       response([message("Affinity is unavailable.")])])

        def invoke(request, *_):
            sent.append({t["name"] for t in request["tools"]})
            return next(script)
        with tempfile.TemporaryDirectory() as tmp:
            rec = ch.execute(self.args(Path(tmp) / "run", ["no-notes"]), invoke=invoke)["records"][0]
        self.assertTrue(all("tool_activate" in tools for tools in sent[:3]))
        self.assertTrue(all("tool_activate" not in tools for tools in sent[3:]))
        self.assertEqual(rec["activatedTools"], [])
        late = [c for t in rec["turns"] for c in t["calls"] if c["callId"] == "late"]
        self.assertEqual(late[0]["error"], "Unknown tool")
        self.assertFalse(rec["deterministic"]["passed"])

    def test_the_restart_limit_counts_activation_only_invocations(self):
        # A step that activates ends Platform's invocation; one with any other tool call is not activation-only.
        simulator = sim("no-notes")
        steps = [(True, False), (True, False), (False, True), (True, False), (True, False), (True, False)]
        for activated, progress in steps[:5]:
            simulator.count_activation_step(activated, progress)
        self.assertEqual(simulator.activation_only_steps, 1)
        simulator.count_activation_step(*steps[5])
        self.assertEqual(simulator.activation_only_steps, 2)
        simulator.count_activation_step(True, False)
        simulator.count_activation_step(False, True)
        simulator.count_activation_step(True, False)
        self.assertEqual(simulator.activation_only_steps, ch.ACTIVATION_ONLY_RESTART_LIMIT)
        simulator.start_turn()
        self.assertEqual(simulator.activation_only_steps, 0)

    def test_without_an_affinity_grant_nothing_can_be_listed_or_activated(self):
        simulator = sim("crm-not-granted")
        listed = simulator.handle("tools_list_available", {"applicationExternalId": "affinity-mcp-server", "limit": 50})[0]
        self.assertEqual(listed["result"]["tools"], [])
        self.assertEqual(simulator.handle("tools_search_available", {"query": "affinity"})[0]["result"], [])
        refused = simulator.handle("tool_activate", {"toolExternalId": "affinity_search_companies"})[0]["result"]
        self.assertEqual((refused["activated"], refused["code"]), (False, "TOOL_ACTIVATION_DENIED"))
        self.assertEqual(simulator.active_affinity_tools(), [])
        direct = {**case("crm-not-granted"), "affinityToolsInactive": False}
        self.assertFalse(any(t["toolSpec"]["name"].startswith("affinity_") for t in ch.tool_specs(FROZEN, "analyst", direct)))

    def test_a_partial_grant_lists_and_activates_only_the_granted_tools(self):
        # #119 review: the list is permission-scoped, so a nonempty list can still leave out a read tool.
        simulator = sim("crm-partial-grant")
        listed = simulator.handle("tools_list_available", {"applicationExternalId": "affinity-mcp-server", "limit": 50})[0]
        self.assertEqual({t["externalId"] for t in listed["result"]["tools"]},
                         {"affinity_search_companies", "affinity_get_company"})
        granted = simulator.handle("tool_activate", {"toolExternalId": "affinity_search_companies"})[0]["result"]
        self.assertTrue(granted["activated"])
        refused = simulator.handle("tool_activate", {"toolExternalId": "affinity_list_company_notes"})[0]["result"]
        self.assertEqual((refused["activated"], refused["code"]), (False, "TOOL_ACTIVATION_DENIED"))
        self.assertEqual([t["name"] for t in simulator.active_affinity_tools()], ["affinity_search_companies"])
        direct = {**case("crm-partial-grant"), "affinityToolsInactive": False}
        offered = {t["toolSpec"]["name"] for t in ch.tool_specs(FROZEN, "analyst", direct) if t["toolSpec"]["name"].startswith("affinity_")}
        self.assertEqual(offered, {"affinity_search_companies", "affinity_get_company"})

    def test_discovery_steps_do_not_use_the_step_budget(self):
        # Platform leaves search, list and activate steps out of the step budget, so a capped turn still
        # gets its full number of working steps after finding its tools.
        script = iter([response([call("tools_list_available", {"applicationExternalId": "affinity-mcp-server",
                                                               "limit": 50}, "l")]),
                       response([call("tool_activate", {"toolExternalId": "affinity_search_companies"}, "a")]),
                       response([call("affinity_search_companies", {"term": "Pellucid"}, "b")]),
                       response([call("affinity_search_companies", {"term": "Pellucid"}, "c")]),
                       response([message("not reached")])])
        freeze = ch.freeze

        def capped(arms):
            frozen = freeze(arms)
            next(c for c in frozen["cases"]["cases"] if c["id"] == "no-notes")["maxSteps"] = 2
            return frozen
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(ch, "freeze", capped):
            rec = ch.execute(self.args(Path(tmp) / "run", ["no-notes"]), invoke=lambda *_: next(script))["records"][0]
        self.assertEqual([c["callId"] for t in rec["turns"] for c in t["calls"]], ["l", "a", "b", "c"])
        self.assertEqual(rec["status"], "incomplete")

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
