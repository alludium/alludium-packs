#!/usr/bin/env python3
"""CRM history import comparison (Platform issue #4841).

Sibling of compare_stage_moves.py. It answers one question: when a user asks to import a company's
Affinity history, does the Pack produce one durable, sourced CRM history document for the Deal that
keeps every retrieved note in full, says when an import is partial, refuses to save what a refresh
could not update, and changes nothing else?

Arms are Pack git revisions (or WORKTREE). Import cases run the Deal Analyst on the "Import or
Refresh CRM History" task when the arm ships that task, and otherwise send the user's request to the
Deal Manager (what users had). Routing cases always run the Deal Manager. Both agents get their
Platform capability-bundle guidance, their tool contract, simulated Affinity tools copied from the
published connector, and simulated Platform document and task tools. Default mode is a no-spend
preflight. Prompt/tool-choice evidence only; not Platform integration or deployed proof.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import signal
import subprocess
import time
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import urllib.error
import urllib.request

import yaml

import compare_deal_manager_prompts as base
from evaluate_deal_manager import PACK, PROJECT, ROOT, tool_specs_from_names

HERE = Path(__file__).resolve().parent
EVAL_DIR = HERE.parent / "evals" / "4841"
CASES = EVAL_DIR / "cases.yaml"
EXPECTATIONS = EVAL_DIR / "expectations.yaml"
AFFINITY_TOOLS = EVAL_DIR / "affinity-tools.json"
CAPABILITY_PROMPTS = EVAL_DIR / "capability-prompts.json"
TOOL_CONTRACT = HERE / "fixtures" / "deal-manager-tool-contract.json"
SKILLS_DIR = "plugins/vc/skills"
MANAGER_PATH = f"{PACK}/agent-templates/vc_deal_pipeline_manager.yaml"
ANALYST_PATH = f"{PACK}/agent-templates/vc_deal_analyst.yaml"
DEFINITIONS_DIR = f"{PACK}/task-definition-templates/vc-workflows"
CRM_SLUG = "import-refresh-crm-history"
CRM_TEMPLATE_PATH = f"{PACK}/documents/deal-pipeline/crm-history-template.html"
# Shared guidance the task's documentRefs name; served read-only like the template.
GUIDE_PATHS = {"vc.document.evidence_citation_style_guide": f"{PACK}/documents/shared/evidence-citation-style-guide.html",
               "vc.document.template_use_guidance": f"{PACK}/documents/shared/template-use-guidance.html"}
CRM_TEMPLATE_ID = "vc.document.deal_pipeline_crm_history_template"
POINTER = "crm_history_artifact_id"
WORKTREE = "WORKTREE"

GLOBAL_ASSERTIONS = ["allTurnsComplete", "noInvalidToolCalls", "noAffinityWrites", "noInteractionFilter",
                     "noOutOfScopeReads", "noFieldWrites", "noStageMove"]
# Streamed subject calls: the final events carry the full response; a read waits at most this long.
STREAM_FINAL_EVENTS = {"response.completed", "response.incomplete"}
STREAM_READ_TIMEOUT_SECONDS = 120
IMPORT_GLOBAL_ASSERTIONS = ["oneDocument", "completedWithPointer", "safeHtml", "briefCitesNotes", "briefSubstantive",
                            "notesAttributed"]
CASE_KEYS = {"notesRetained", "notesAbsent", "importStatus", "documentMentions", "documentForbidden", "documentKeeps",
             "replyMentions", "refresh", "stableRefs", "blocked", "createsCrmTask", "passesProvider",
             "noManagerDocument", "readsDocument", "createsTask", "livingReportActive"}
ARM_NAME = re.compile(r"[a-z0-9][a-z0-9-]*")
INVALID_CALL_ERRORS = {"Invalid JSON arguments", "Unknown tool", "Missing required argument"}
DEFAULT_MAX_WALL_MINUTES = 120

# Platform limits mirrored from Craft c69fe008.
MAX_TEXT_ARTIFACT_BYTES = 100 * 1024
MAX_SOURCE_READ_LINES = 200
AFFINITY_CHARACTER_LIMIT = 25000

ORGANISATION = "22222222-2222-4222-8222-222222222222"
TASK = "33333333-3333-4333-8333-333333333333"
EXISTING_DOCUMENT = "44444444-4444-4444-8444-444444444444"
RUNNING_CRM_TASK = "55555555-5555-4555-8555-555555555555"
TEMPLATE_ARTIFACT = "66666666-6666-4666-8666-666666666666"
# A CRM history document another, still-running import created before it could save the Deal's pointer.
OTHER_IMPORT_DOCUMENT = "99999999-9999-4999-8999-999999999999"
# The visible change a colleague makes between the refresh's read and its first write.
COLLEAGUE_EDIT = "<p>Partner comment: ask for the 2025 churn figures.</p>"
TEMPLATE_REVISION = 3
USER_NAME = "Alex Partner"

ANALYST_TOOLS = ["project.getAgentContext", "project.findById", "project-task.findById", "task-definitions.findById",
                 "artifact.searchArtifacts", "artifact.list", "artifact.getArtifact", "artifact.findById",
                 "artifact.getSourceMetadata", "artifact.waitForArtifactsReady", "artifact.readSourceRange",
                 "artifact.getTextStructure", "project.getTemplateMetadata", "project.readTemplateRange",
                 "project.instantiateTemplate", "artifact.createTextArtifact", "artifact.replaceTextRange",
                 "artifact.insertTextBeforeLine", "artifact.insertTextAfterLine", "artifact.updateTextArtifact",
                 "task-management.saveTaskOutput", "task-management.completeTask", "task-management.askTaskQuestion",
                 "project.sendManagerMessage", "field-values.getFields", "field-values.setField", "activate_skill"]
DOCUMENT_READS = {"artifact.getArtifact", "artifact.findById", "artifact.getSourceMetadata", "artifact.readSourceRange",
                  "artifact.getTextStructure"}
DOCUMENT_LISTS = {"artifact.searchArtifacts", "artifact.list", "artifact.getArtifactsLinkedToChat",
                  "artifact.getArtifactsForChatContext"}
LIVING_REPORT_SKILL = "generate-or-refresh-living-report"
LINE_EDITS = {"artifact.replaceTextRange", "artifact.insertTextBeforeLine", "artifact.insertTextAfterLine"}
TASK_SAVES = {"task-management.saveTaskOutput", "task-management.completeTask"}

_ID = {"type": "string", "description": "Artifact ID"}
_REVISION = {"type": "integer", "description": "Source revision number observed before preparing the edit"}
_HASH = {"type": "string", "description": "SHA-256 source content hash observed before preparing the edit"}
_PROJECT = {"type": "string", "description": "Project ID used to resolve the current project type"}
_REF = {"type": "string", "description": "Durable project type document reference ID, for example "
                                         "vc.document.investment_memo_template. Use this instead of "
                                         "artifact.readSourceRange for pack templates."}
_OUTPUT = {"type": "object", "description": "Structured task output. For file output fields, use the returned artifact "
                                            "UUID, not a filename or storage key."}
# Request schemas approximated from Craft c69fe008 (artifact.transformers.ts, project.transformers.ts,
# task-management.transformers.ts, skill-runtime-tools.ts). Other tools use the generic contract schema.
SCHEMAS: dict[str, tuple[str, dict, list[str]]] = {
    "field-values.getFields": ("Read the current project's field values.", {"projectId": _PROJECT}, ["projectId"]),
    "field-values.setField": ("Set one field value on the current project.",
                              {"projectId": _PROJECT, "fieldKey": {"type": "string"}, "value": {}},
                              ["projectId", "fieldKey"]),
    "project.getTemplateMetadata": ("Read a project type template's metadata by documentRefId.",
                                    {"projectId": _PROJECT, "documentRefId": _REF}, ["projectId", "documentRefId"]),
    "project.readTemplateRange": ("Read a 1-based inclusive line range of a project type template by documentRefId.",
                                  {"projectId": _PROJECT, "documentRefId": _REF,
                                   "startLine": {"type": "integer"}, "endLine": {"type": "integer"}},
                                  ["projectId", "documentRefId"]),
    "project.instantiateTemplate": ("Create a filled PROJECT_SHARED copy of a project type template.",
                                    {"projectId": _PROJECT, "documentRefId": _REF,
                                     "filename": {"type": "string", "description": "Filename for the filled project artifact"},
                                     "content": {"type": "string", "description": "Full filled Markdown or HTML content to persist"},
                                     "expectedTemplateSourceRevisionNumber": {"type": "integer"},
                                     "expectedTemplateSourceContentHash": {"type": "string"}},
                                    ["projectId", "documentRefId", "filename", "content",
                                     "expectedTemplateSourceRevisionNumber", "expectedTemplateSourceContentHash"]),
    "artifact.getSourceMetadata": ("Read an artifact's source metadata: revision, content hash, size and line count.",
                                   {"id": _ID}, ["id"]),
    "artifact.readSourceRange": (f"Read a 1-based inclusive line range (at most {MAX_SOURCE_READ_LINES} lines) of a text "
                                 "artifact's source.", {"id": _ID, "startLine": {"type": "integer"},
                                                        "endLine": {"type": "integer"}}, ["id"]),
    "artifact.getTextStructure": ("List a text artifact's sections with line numbers.",
                                  {"id": _ID, "includeExcerpts": {"type": "boolean"}}, ["id"]),
    "artifact.waitForArtifactsReady": ("Wait for artifacts to finish processing.",
                                       {"artifactIds": {"type": "array", "items": {"type": "string"}}}, ["artifactIds"]),
    "artifact.createTextArtifact": ("Create a durable text artifact.",
                                    {"filename": {"type": "string"}, "content": {"type": "string"},
                                     "mimeType": {"type": "string"}}, ["filename", "content"]),
    "artifact.updateTextArtifact": ("Replace the entire source of a supported text artifact while keeping its ID.",
                                    {"id": _ID, "content": {"type": "string", "description": "Full replacement UTF-8 text "
                                     "content for the entire artifact source; this is not a patch or partial line range"},
                                     "expectedSourceRevisionNumber": _REVISION, "expectedSourceContentHash": _HASH},
                                    ["id", "content", "expectedSourceRevisionNumber", "expectedSourceContentHash"]),
    "artifact.replaceTextRange": ("Replace a line range in a text artifact.",
                                  {"id": _ID, "expectedSourceRevisionNumber": _REVISION, "expectedSourceContentHash": _HASH,
                                   "startLine": {"type": "integer"}, "endLine": {"type": "integer"},
                                   "expectedText": {"type": "string"}, "replacementText": {"type": "string"}},
                                  ["id", "expectedSourceRevisionNumber", "expectedSourceContentHash", "startLine",
                                   "endLine", "expectedText", "replacementText"]),
    "artifact.insertTextBeforeLine": ("Insert text before a line of a text artifact.",
                                      {"id": _ID, "expectedSourceRevisionNumber": _REVISION,
                                       "expectedSourceContentHash": _HASH, "line": {"type": "integer"},
                                       "text": {"type": "string"}, "expectedText": {"type": "string"}},
                                      ["id", "expectedSourceRevisionNumber", "expectedSourceContentHash", "line", "text"]),
    "artifact.insertTextAfterLine": ("Insert text after a line of a text artifact.",
                                     {"id": _ID, "expectedSourceRevisionNumber": _REVISION,
                                      "expectedSourceContentHash": _HASH, "line": {"type": "integer"},
                                      "text": {"type": "string"}, "expectedText": {"type": "string"}},
                                     ["id", "expectedSourceRevisionNumber", "expectedSourceContentHash", "line", "text"]),
    "task-management.saveTaskOutput": ("Save structured output on the current task without completing it.",
                                       {"taskId": {"type": "string"}, "output": _OUTPUT}, ["output"]),
    "task-management.completeTask": ("Complete the current task with its structured output.",
                                     {"taskId": {"type": "string"}, "output": _OUTPUT}, ["taskId"]),
    "task-management.askTaskQuestion": ("Open one structured question on the current task.",
                                        {"taskId": {"type": "string"}, "label": {"type": "string"},
                                         "description": {"type": "string"}}, ["label"]),
    "project.sendManagerMessage": ("Send a bounded message to the project's manager chat.",
                                   {"message": {"type": "string"}}, ["message"]),
    "activate_skill": ("Activate one assigned skill, or a skill explicitly referenced by an active skill when policy "
                       "allows it, for this chat turn using its skillId or exact skill name. Inspect its manifest before "
                       "reading any specific companion file, then continue the current task in the same turn. Treat "
                       "skill activation as setup, not as the final answer.",
                       {"skillId": {"type": "string"}, "skillName": {"type": "string"}}, []),
}

# Text Platform renders for tasks and skills (prompt.service.ts at Craft c69fe008), trimmed to the parts a
# CRM history task uses.
TASK_REFERENCE_GUIDANCE = (
    "For project task template references, use project.getTemplateMetadata and project.readTemplateRange with the "
    "documentId as documentRefId. For ordinary output-template copies, use project.instantiateTemplate to create the "
    "produced file artifact. When the task has an HTML file output or a file output with no format configured, and its "
    "definition directs artifact.createTextArtifact with text/html and .html, create the produced artifact with "
    "artifact.createTextArtifact instead: use a .html filename, mimeType text/html, and complete standalone HTML source "
    "beginning with <!doctype html>. Put the produced artifact ID in the task output field. The documentId is the "
    "durable template/reference ID; do not use it as a produced artifact ID or as an artifact.readSourceRange target.")
SKILL_CATALOG_GUIDANCE = (
    "Call the `activate_skill` tool with a skillId when one of the AUTO skills is needed for the current task.\n"
    "After `activate_skill` returns, treat it as setup only and continue the current task in the same turn.")
PROJECT_CONTEXT_GUIDANCE = (
    "Use the task project context above as current, dynamic project operating context. Do not infer approval for "
    "external sends, CRM writes, Drive changes, investment decisions, or legal decisions unless the project operating "
    "instructions or user explicitly authorize it.")

# Reply and document checks are regexes, not a semantic judge; read the saved documents and replies too.
URL = re.compile(r"https?://\S+|\b[\w.-]+\.example(?:/\S*)?", re.I)
WORD = re.compile(r"\w+")
UNSAFE_HTML = re.compile(r"<script\b|<iframe\b|<form\b|<object\b|<embed\b|<link\b|@import\b|javascript:|"
                         r"\son[a-z]+\s*=|<img\b[^>]*\bsrc\s*=\s*['\"]?https?:", re.I)
APPENDIX_HEADING = re.compile(r"<h2[^>]*>\s*Source appendix\s*</h2>", re.I)
# Matched on visible text, so linked citations such as [<a href="#N1">N1</a>] count.
CITATION = re.compile(r"\[\s*N\d+")
CITATION_GROUP = re.compile(r"\[([^\[\]]*\bN\d+[^\[\]]*)\]")
CITATION_REF = re.compile(r"\bN(\d+)(?:\s*[\u2013\u2014-]\s*N?(\d+))?")
# Identity reads the Deal Manager may call; every other identity.* call is a write and is refused.
IDENTITY_READS = {
    "identity.lookupCandidates": {"candidates": [], "hasMore": False},
    "identity.findOrganisation": None,
    "identity.findPerson": {"record": None},
    "identity.listAffiliations": {"affiliations": []},
    "identity.listIdentifiers": {"identifiers": []},
    "identity.listProjectLinks": None,
    "identity.findSourceCapture": {"capture": None},
}
# Instruction text from the CRM-history template that a filled document must replace.
TEMPLATE_PLACEHOLDERS = ["as far as the retrieved records support it", "A readable chronology of changes that matter",
                         "Name what would resolve each one"]
OVERVIEW = re.compile(r"<h2[^>]*>\s*Company overview\s*</h2>(.*?)(?=<h2|$)", re.I | re.S)
MIN_OVERVIEW_WORDS = 20
LINK = re.compile(r"https?://[^\s<>\"')]+|\b[\w-]+(?:\.[\w-]+)*\.example(?:/[^\s<>\"')]*)?", re.I)
BADGE = re.compile(r"<[^>]+class=\"[^\"]*\bbadge\b[^\"]*\"[^>]*>(.*?)</", re.I | re.S)


# ---------------------------------------------------------------- freezing

def parse_arm(spec: str) -> tuple[str, str]:
    """NAME=REVISION, where REVISION is a git revision or WORKTREE (the working tree, for local checks)."""
    name, _, source = spec.partition("=")
    if not ARM_NAME.fullmatch(name) or not source:
        raise SystemExit(f"--arm must look like NAME=REVISION or NAME=WORKTREE (got {spec!r})")
    return name, source


def arm_reader(source: str):
    """Return (origin, read(path) -> text or None, list(directory) -> paths) for one arm source."""
    if source == WORKTREE:
        def read(path: str) -> str | None:
            file = ROOT / path
            return file.read_text() if file.is_file() else None

        def listing(directory: str) -> list[str]:
            return sorted(str(p.relative_to(ROOT)) for p in (ROOT / directory).glob("*.yaml"))

        return {"kind": "worktree"}, read, listing
    commit = base.resolve_commit(source)

    def read(path: str) -> str | None:
        result = subprocess.run(["git", "show", f"{commit}:{path}"], cwd=ROOT, text=True, capture_output=True)
        return result.stdout if result.returncode == 0 else None

    def listing(directory: str) -> list[str]:
        out = subprocess.check_output(["git", "ls-tree", "--name-only", f"{commit}:{directory}"], cwd=ROOT, text=True)
        return [f"{directory}/{name}" for name in out.split() if name.endswith(".yaml")]

    return {"kind": "git", "revision": commit, "requested": source}, read, listing


def split_skill(text: str) -> tuple[dict, str]:
    match = re.match(r"---\n(.*?)\n---\n?(.*)", text, re.S)
    return (yaml.safe_load(match.group(1)), match.group(2).strip()) if match else ({}, text.strip())


def load_arm(name: str, source: str) -> dict:
    origin, read, listing = arm_reader(source)
    manager_raw, analyst_raw = read(MANAGER_PATH), read(ANALYST_PATH)
    if manager_raw is None or analyst_raw is None:
        raise SystemExit(f"Arm {name}: agent templates are missing at {source}")
    analyst = yaml.safe_load(analyst_raw)
    definitions = {}
    for path in listing(DEFINITIONS_DIR):
        parsed = yaml.safe_load(read(path) or "{}") or {}
        slug = (parsed.get("definition") or {}).get("slug")
        if slug:
            definitions[slug] = parsed
    skills = {}
    for assignment in analyst.get("skills", []):
        text = read(f"{SKILLS_DIR}/{assignment['externalId']}/SKILL.md")
        if text is not None:
            front, body = split_skill(text)
            skills[assignment["externalId"]] = {"name": front.get("name", assignment["externalId"]),
                                                "description": " ".join(str(front.get("description", "")).split()),
                                                "activationMode": assignment.get("activationMode", "AUTO"),
                                                "body": body, "sha256": base.sha(text)}
    template = read(CRM_TEMPLATE_PATH)
    guides = {ref: text for ref, path in GUIDE_PATHS.items() if (text := read(path)) is not None}
    crm_task = definitions.get(CRM_SLUG)
    snapshot = json.dumps({"manager": manager_raw, "analyst": analyst_raw, "definitions": sorted(definitions),
                           "crmTask": crm_task, "template": template, "guides": guides,
                           "skills": {k: v["sha256"] for k, v in sorted(skills.items())}}, sort_keys=True)
    return {"name": name, "origin": origin, "manager": yaml.safe_load(manager_raw), "analyst": analyst,
            "managerRaw": manager_raw, "analystRaw": analyst_raw, "definitions": definitions, "crmTask": crm_task,
            "template": template, "guides": guides, "skills": skills, "sha256": base.sha(snapshot),
            "route": "analyst-task" if crm_task and template else "manager-chat"}


def freeze(arm_specs: list[str]) -> dict:
    """Resolve every input shared by all arms and record problems before any provider access."""
    cases_text, expectations_text = CASES.read_text(), EXPECTATIONS.read_text()
    cases, expectations = yaml.safe_load(cases_text), yaml.safe_load(expectations_text)
    affinity_text, capability_text = AFFINITY_TOOLS.read_text(), CAPABILITY_PROMPTS.read_text()
    contract_text = TOOL_CONTRACT.read_text()
    affinity, capabilities, contract = json.loads(affinity_text), json.loads(capability_text), json.loads(contract_text)
    problems: list[str] = []
    if expectations.get("global") != GLOBAL_ASSERTIONS:
        problems.append(f"Global assertions must be exactly {GLOBAL_ASSERTIONS}")
    if expectations.get("importGlobal") != IMPORT_GLOBAL_ASSERTIONS:
        problems.append(f"Import assertions must be exactly {IMPORT_GLOBAL_ASSERTIONS}")
    case_ids = [case["id"] for case in cases["cases"]]
    if len(set(case_ids)) != len(case_ids):
        problems.append("Duplicate case IDs")
    if set(case_ids) != set(expectations["cases"]):
        problems.append("Cases and expectations do not cover the same IDs")
    for case in cases["cases"]:
        expect = expectations["cases"].get(case["id"], {})
        unknown = set(expect) - CASE_KEYS
        if unknown:
            problems.append(f"{case['id']}: unknown expectation keys {sorted(unknown)}")
        if case.get("kind") not in {"import", "routing", "skill-control"}:
            problems.append(f"{case['id']}: kind must be import, routing or skill-control")
        if case.get("kind") == "routing" and not case.get("turns"):
            problems.append(f"{case['id']}: routing cases need turns")
        if case.get("kind") == "import" and not expect.get("blocked") and expect.get("importStatus") not in {"complete", "partial"}:
            problems.append(f"{case['id']}: importStatus must be complete or partial")
    arms, names = [], set()
    for spec in arm_specs:
        name, source = parse_arm(spec)
        if name in names:
            problems.append(f"Duplicate arm name {name}")
        names.add(name)
        arms.append(load_arm(name, source))
    if not arms:
        problems.append("At least one --arm is required")
    if len({arm["sha256"] for arm in arms}) < len(arms):
        problems.append("Two arms have identical Pack inputs; nothing to compare")
    variables = {"firmName": cases["firmName"], "fundId": "Unconfirmed"}
    for arm in arms:
        for role in ("manager", "analyst"):
            prompt = base.render_prompt(arm[role]["prompt"]["template"], variables)
            if re.search(r"\{\{\w+\}\}", prompt):
                problems.append(f"Arm {arm['name']}: {role} prompt has an unrendered variable")
        if contract["capabilityBundles"] != arm["manager"]["capabilityProfile"]["bundles"]:
            problems.append(f"Arm {arm['name']}: frozen manager tool contract bundles do not match its capability profile")
        for role in ("manager", "analyst"):
            missing = set(arm[role]["capabilityProfile"]["bundles"]) - set(capabilities["bundles"])
            if missing:
                problems.append(f"Arm {arm['name']}: no frozen capability prompt for {sorted(missing)}")
        for case in cases["cases"]:
            if case.get("kind") == "skill-control" and case.get("taskSlug") not in arm["definitions"]:
                problems.append(f"Arm {arm['name']}: {case['id']} needs task {case.get('taskSlug')}")
        if arm["route"] == "analyst-task":
            task = arm["crmTask"]
            if arm["analyst"].get("id") != task["definition"]["definitionJson"].get("recommendedAgentTemplate"):
                problems.append(f"Arm {arm['name']}: the CRM task is not recommended to the analyst template")
            if CRM_SLUG not in arm["manager"].get("metadata", {}).get("supportedTaskDefinitions", []):
                problems.append(f"Arm {arm['name']}: the manager cannot start the CRM task")
    return {"cases": cases, "expectations": expectations, "arms": arms, "problems": problems, "variables": variables,
            "affinity": affinity, "capabilities": capabilities, "managerTools": [t["name"] for t in contract["tools"]],
            "identity": {"casesSha256": base.sha(cases_text), "expectationsSha256": base.sha(expectations_text),
                         "affinityToolsSha256": base.sha(affinity_text), "capabilityPromptsSha256": base.sha(capability_text),
                         "toolContractSha256": base.sha(contract_text),
                         "arms": [{"name": a["name"], "origin": a["origin"], "sha256": a["sha256"], "route": a["route"],
                                   "managerVersion": a["manager"].get("version"), "analystVersion": a["analyst"].get("version"),
                                   "crmTaskVersion": (a["crmTask"] or {}).get("version")} for a in arms],
                         "runnerSha256": base.sha(Path(__file__).read_text()),
                         "baseRunnerSha256": base.sha((HERE / "compare_deal_manager_prompts.py").read_text())}}


def plan_attempts(cases: list[dict], arms: list[str], repetitions: int) -> list[dict]:
    """Interleave arms; the order rotates with repetition and case position so no arm is always first."""
    plan = []
    for repetition in range(1, repetitions + 1):
        for index, case in enumerate(cases):
            shift = (repetition + index) % len(arms)
            for arm in arms[shift:] + arms[:shift]:
                plan.append({"index": len(plan) + 1, "case": case["id"], "arm": arm, "repetition": repetition,
                             "folder": f"attempts/{len(plan) + 1:03}-{case['id']}--{arm}--r{repetition}"})
    return plan


# ---------------------------------------------------------------- simulation

def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def note_text(note_html: str) -> str:
    """Plain text of a note, converted the way the skill asks: breaks kept, list items as '- ', links inline."""
    text = re.sub(r"<a\b[^>]*href=\"([^\"]*)\"[^>]*>(.*?)</a>", r"\2 (\1)", note_html, flags=re.S | re.I)
    text = re.sub(r"<li[^>]*>", "\n- ", text, flags=re.I)
    text = re.sub(r"</p>|<br\s*/?>|</li>|</ul>|</ol>", "\n", text, flags=re.I)
    text = html.unescape(re.sub(r"<[^>]+>", "", text))
    return "\n".join(line.strip() for line in text.splitlines() if line.strip())


def words(text: str) -> list[str]:
    """Comparable words: tags removed, entities decoded, URLs and domains dropped, lower case."""
    text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    return [w.lower() for w in WORD.findall(URL.sub(" ", text))]


def note_links(note_html: str) -> set[str]:
    """Link destinations and linked domains in a note, which the appendix must keep as references."""
    hrefs = re.findall(r"href=\"([^\"]+)\"", note_html)
    return {link.rstrip(".,;") for link in [*hrefs, *LINK.findall(html.unescape(re.sub(r"<[^>]+>", " ", note_html)))]}


def contains_note(document: str, note_html: str) -> bool:
    """Every word of the note appears in the document in order and unbroken, so no part was shortened."""
    wanted = words(note_html)
    return bool(wanted) and f" {' '.join(wanted)} " in f" {' '.join(words(document))} "


def flatten_notes(spec: list) -> list[dict]:
    return [note for item in spec for note in (item if isinstance(item, list) else [item])]


def generated_notes(spec: dict) -> list[dict]:
    start = date.fromisoformat(spec["startDate"])
    return [{"id": spec["firstId"] + i, "author": spec["author"],
             "date": f"{start + timedelta(days=i * spec['stepDays'])}T10:00:00Z",
             "html": "<p>" + html.escape((spec["text"].format(n=i + 1) * spec.get("repeat", 1)).strip()) + "</p>"}
            for i in range(spec["count"])]


def affinity_note(note: dict) -> dict:
    first, _, last = note["author"].partition(" ")
    return {"id": note["id"], "content": {"html": note["html"]},
            "creator": {"id": int(sha256(note["author"])[:6], 16), "firstName": first, "lastName": last,
                        "primaryEmailAddress": f"{first.lower()}@examplevc.example"},
            "createdAt": note["date"], "type": "entities"}


def previous_document(case: dict, notes: dict[int, dict]) -> str:
    """The CRM history document a previous import saved: the shape the template asks for, frozen per case."""
    org = case["deal"]["organisation"]["name"]
    kept = [notes[n] for n in case.get("existingDocumentNotes", [])]
    brief = case.get("existingDocumentBrief") or (
        f"{org} first appears in our CRM in {datetime.fromisoformat(kept[0]['date'][:10]):%B %Y} [N1]. "
        + " ".join(f"A {datetime.fromisoformat(n['date'][:10]):%B %Y} note records: {note_text(n['html'])} [N{i}]"
                   for i, n in enumerate(kept, 1)) if kept else f"The CRM returned no notes for {org}.")
    entries = "\n".join(
        f'    <div class="source-note" id="N{i}"><h3>N{i}</h3><p class="source-meta">Affinity · company record '
        f'{case["affinity"]["companies"][0]["id"] if case["affinity"]["companies"] else "unknown"} · note {n["id"]} · '
        f'{n["author"]} · {n["date"][:10]}</p><pre class="source-text">{html.escape(note_text(n["html"]))}</pre></div>'
        for i, n in enumerate(kept, 1))
    return (f'<!doctype html>\n<html lang="en">\n<head><meta charset="utf-8"><title>{org} CRM history and context</title>'
            f'</head>\n<body><article class="document">\n  <header class="document-header"><h1>CRM history and context</h1>'
            f'<p class="metadata">Company: {org} · CRM: Affinity · Imported 1 March 2026, 09:00 UTC · '
            f'<span class="badge">Complete import</span></p></header>\n'
            f'  <section class="section"><h2>Company overview</h2><p>{html.escape(brief)}</p></section>\n'
            f'  <section class="section"><h2>Changes since the previous import</h2><p>This is the first CRM history '
            f'import for this Deal; there is no earlier import to compare.</p></section>\n'
            f'  <section class="section"><h2>Import coverage</h2><p>{len(kept)} notes retrieved; every page was read.'
            f'</p></section>\n'
            f'  <section class="section" id="source-appendix"><h2>Source appendix</h2>\n{entries}\n  </section>\n'
            f'</article></body></html>\n')


def requested_states(value: object) -> list:
    """Every non-null lifecycle state value anywhere in a tool call's arguments."""
    if isinstance(value, list):
        return [state for item in value for state in requested_states(item)]
    if isinstance(value, dict):
        found = [item for key, item in value.items()
                 if isinstance(key, str) and key.lower().replace("_", "").endswith(("state", "stage")) and item]
        return found + [state for item in value.values() for state in requested_states(item)]
    return []


class CrmSimulator:
    """Synthetic Affinity and Platform state for one attempt."""

    def __init__(self, frozen: dict, arm: dict, case: dict):
        self.frozen, self.arm, self.case = frozen, arm, case
        self.deal = case["deal"]
        affinity = case.get("affinity") or {}
        self.companies = {c["id"]: c for c in affinity.get("companies", [])}
        self.company_notes = {c["id"]: [affinity_note(n) for n in (generated_notes(c["generatedNotes"])
                                        if c.get("generatedNotes") else flatten_notes(c.get("notes", [])))]
                              for c in self.companies.values()}
        self.opportunities = {o["id"]: o for o in affinity.get("opportunities", [])}
        self.opportunity_notes = {o["id"]: [affinity_note(n) for n in flatten_notes(o.get("notes", []))]
                                  for o in self.opportunities.values()}
        self.page_size = case.get("pageSize", 100)
        self.definitions = {base.definition_id(slug, "4841"): spec for slug, spec in arm["definitions"].items()}
        self.crm_definition = base.definition_id(CRM_SLUG, "4841") if arm["crmTask"] else None
        self.documents: dict[str, dict] = {}
        self.pending_edit = bool(self.deal.get("editedBeforeFirstUpdate"))
        # Saved documents report PROCESSING until the agent waits for them, as Platform does after a write.
        self.processing: set[str] = set()
        if self.deal.get("existingDocument") and not self.deal.get("existingDocumentMissing"):
            all_notes = {n["id"]: n for c in affinity.get("companies", [])
                         for n in (generated_notes(c["generatedNotes"]) if c.get("generatedNotes")
                                   else flatten_notes(c.get("notes", [])))}
            self.add_document(EXISTING_DOCUMENT, f"{self.deal['organisation']['name']} CRM history and context.html",
                              previous_document(case, all_notes), "PROJECT", revision=2)
        self.template = arm["template"]
        self.tasks = []
        if self.deal.get("openCrmTask") and self.crm_definition:
            self.tasks.append(self.task_record(RUNNING_CRM_TASK, CRM_SLUG, "running"))
        if self.deal.get("otherImportDocument"):
            self.add_document(OTHER_IMPORT_DOCUMENT, f"{self.deal['organisation']['name']} CRM history and context.html",
                              previous_document(case, {}), "PROJECT")
        self.turn = 0
        self.agent = "manager"
        self.created: list[dict] = []
        self.updates: list[dict] = []
        self.line_edits: list[dict] = []
        self.affinity_writes: list[dict] = []
        self.affinity_reads: list[dict] = []
        self.interaction_filter_searches: list[dict] = []
        self.out_of_scope_reads: list[dict] = []
        self.refused_creations: list[dict] = []
        self.field_writes: list[dict] = []
        self.stage_moves: list[dict] = []
        self.tasks_created: list[dict] = []
        self.task_saves: list[dict] = []
        self.questions: list[dict] = []
        self.skills_activated: list[str] = []
        self.document_reads: list[dict] = []
        self.manager_messages: list[dict] = []

    # Platform state ----------------------------------------------------------------------

    def add_document(self, doc_id: str, filename: str, content: str, owner: str, revision: int = 1) -> dict:
        document = {"id": doc_id, "filename": filename, "content": content, "revision": revision, "owner": owner,
                    "mimeType": "text/html" if filename.endswith(".html") or content.lstrip().startswith("<") else "text/plain"}
        self.documents[doc_id] = document
        return document

    def metadata(self, document: dict) -> dict:
        return {"id": document["id"], "filename": document["filename"], "mimeType": document["mimeType"],
                "sourceRevisionNumber": document["revision"], "sourceContentHash": sha256(document["content"]),
                "sizeBytes": len(document["content"].encode()), "totalLineCount": len(document["content"].splitlines()),
                "processingStatus": "PROCESSING" if document["id"] in self.processing else "READY",
                "projectId": PROJECT,
                "scope": "TASK_RUN" if document["owner"] == "TASK_RUN" else "PROJECT_SHARED"}

    def pointer(self) -> str | None:
        return EXISTING_DOCUMENT if self.deal.get("existingDocument") else None

    def project(self) -> dict:
        org = self.deal["organisation"]
        fields = {"company_name": org["name"], **(self.deal.get("fields") or {})}
        if self.arm["crmTask"]:
            fields[POINTER] = self.pointer()
        return {"id": PROJECT, "name": self.deal["name"], "projectTypeKey": "vc_deal_pipeline", "status": "active",
                "lifecycleStage": "screening",
                "investmentSubject": {"organisation": {"id": ORGANISATION, "displayName": org["name"],
                                                       "domain": org.get("domain")}},
                "fields": fields, "openTasks": [t for t in self.tasks if t["status"] in {"running", "pending"}],
                "documents": [{"id": d["id"], "filename": d["filename"], "scope": "PROJECT_SHARED"}
                              for d in self.documents.values() if d["owner"] == "PROJECT"]}

    def identity_read(self, name: str) -> dict:
        org = self.deal["organisation"]
        record = {"id": ORGANISATION, "displayName": org["name"], "domain": org.get("domain")}
        if name == "identity.listProjectLinks":
            return {"links": [{"projectId": PROJECT, "role": "deal_company", "organisation": record}]}
        if name == "identity.findOrganisation":
            return {"record": record}
        return IDENTITY_READS[name]

    def task_record(self, task_id: str, slug: str | None, status: str, task_input: dict | None = None) -> dict:
        spec = self.arm["definitions"].get(slug) if slug else None
        return {"id": task_id, "taskId": task_id, "projectId": PROJECT, "status": status,
                "taskDefinitionId": base.definition_id(slug, "4841") if slug else None, "slug": slug,
                "title": spec["title"] if spec else "Custom task", "input": task_input or {},
                "agentExecutor": {"name": "Deal Analyst"}, "action": {"label": "Open task", "href": f"/tasks/{task_id}"}}

    def task_spec(self) -> dict:
        slug = self.case.get("taskSlug", CRM_SLUG)
        return self.arm["definitions"][slug]

    def task_input(self) -> dict:
        org = self.deal["organisation"]
        if self.case.get("kind") == "skill-control":
            return {"company_name": org["name"], "organisation_id": ORGANISATION}
        task_input = {"company_name": org["name"], "organisation_id": ORGANISATION, "crm_provider": "Affinity"}
        if self.pointer():
            task_input["existing_crm_history_artifact_id"] = self.pointer()
        return task_input

    # Affinity ----------------------------------------------------------------------------

    def affinity(self, name: str, args: dict) -> tuple[object, str | None]:
        spec = next(t for t in self.frozen["affinity"]["tools"] if t["name"] == name)
        if not spec["readOnly"]:
            self.affinity_writes.append({"turn": self.turn, "tool": name, "input": args})
            return None, self.frozen["affinity"]["readOnlyDenialMessage"]
        self.affinity_reads.append({"turn": self.turn, "tool": name, "input": args})
        if name in self.frozen["affinity"].get("outOfScopeReadTools", []):
            # Lists, list entries, people and fields are outside the import (#4841 Dev run read list entries).
            self.out_of_scope_reads.append({"turn": self.turn, "tool": name, "input": args})
            return json.dumps({"data": [], "hasMore": False, "nextCursor": None}, indent=2), None
        if name == "affinity_search_companies":
            term = str(args.get("term") or "").strip().lower()
            found = [c for c in self.companies.values()
                     if not term or any(term in h.lower() for h in [c["name"], *c.get("domains", [])])]
            if args.get("withInteractionDates") or args.get("withInteractionPersons"):
                self.interaction_filter_searches.append({"turn": self.turn, "input": args})
                # Observed on live Affinity (#4841 Dev run): either flag drops companies with no
                # interactions, so a record holding only notes disappears from the results.
                found = [c for c in found if c.get("hasInteractions", True)]
            rows = [{"id": c["id"], "name": c["name"], "domain": c.get("domain"), "domains": c.get("domains", []),
                     "global": False, **({"opportunity_ids": c.get("opportunityIds", [])}
                                         if args.get("withOpportunities") else {})} for c in found]
            # The connector's implementation returns `companies` and `nextPageToken` (its tool description
            # still says `organizations` and `next_page_token`).
            size = self.case.get("searchPageSize", len(rows) or 1)
            start = int(args.get("pageToken") or 0) if str(args.get("pageToken") or "0").isdigit() else 0
            page, token = rows[start:start + size], str(start + size) if start + size < len(rows) else None
            return json.dumps({"companies": page, "count": len(page), "hasMore": token is not None,
                               "nextPageToken": token,
                               "summary": f"Found {len(page)} company/companies"
                                          + (" (more available with pageToken)" if token else "")}, indent=2), None
        if name == "affinity_get_company":
            company = self.companies.get(self.numeric(args.get("companyId")))
            if not company:
                return "Error: Not Found: The requested resource does not exist.", None
            result = {"id": company["id"], "name": company["name"], "domain": company.get("domain"),
                      "domains": company.get("domains", []), "isGlobal": False}
            if "enriched" in (args.get("fieldTypes") or []):
                fields = []
                if company.get("description"):
                    fields.append({"id": "affinity-data-description", "type": "enriched", "name": "Description",
                                   "value": {"type": "text", "data": company["description"]}})
                if company.get("people"):
                    # The connector returns the enriched People field inline on the company record.
                    fields.append({"id": "persons", "type": "enriched", "name": "People",
                                   "value": {"type": "person-multi", "data": company["people"]}})
                if fields:
                    result["fields"] = fields
            return json.dumps(result, indent=2), None
        if name == "affinity_get_opportunity":
            opportunity = self.opportunities.get(self.numeric(args.get("opportunityId")))
            if not opportunity:
                return "Error: Not Found: The requested resource does not exist.", None
            return json.dumps({"id": opportunity["id"], "name": opportunity["name"], "listId": opportunity["listId"]},
                              indent=2), None
        if name == "affinity_list_company_notes":
            key = self.numeric(args.get("companyId"))
            if key not in self.companies:
                return "Error: Not Found: The requested resource does not exist.", None
            return self.notes_page(self.company_notes[key], self.companies[key].get("failingPages", []), args,
                                   "company"), None
        if name == "affinity_list_opportunity_notes":
            key = self.numeric(args.get("opportunityId"))
            if key not in self.opportunities:
                return "Error: Not Found: The requested resource does not exist.", None
            return self.notes_page(self.opportunity_notes[key], [], args, "opportunity"), None
        return None, "Tool outside the simulated Affinity scope"

    @staticmethod
    def numeric(value: object) -> int | None:
        try:
            return int(str(value).strip())
        except (TypeError, ValueError):
            return None

    def notes_page(self, notes: list[dict], failing: list[int], args: dict, label: str) -> str:
        """Cursor pages capped at the case page size; oversized pages shrink as the connector does."""
        offset = int(args["cursor"][1:]) if str(args.get("cursor") or "").startswith("c") and \
            str(args["cursor"])[1:].isdigit() else 0
        if (offset // self.page_size) + 1 in failing:
            return ("Error: Service Unavailable: Affinity is temporarily unavailable. "
                    "Action: Retry the request later.")
        try:
            limit = max(1, min(int(args.get("limit") or 20), 100, self.page_size))
        except (TypeError, ValueError):
            limit = min(20, self.page_size)
        while True:
            page = notes[offset:offset + limit]
            following = offset + len(page)
            cursor = f"c{following}" if following < len(notes) else None
            text = json.dumps({"notes": page, "count": len(page), "hasMore": cursor is not None, "nextCursor": cursor,
                               "summary": f"Found {len(page)} note(s)" if page else f"No notes found for this {label}"},
                              indent=2)
            if len(text) <= AFFINITY_CHARACTER_LIMIT:
                return text
            if len(page) <= 1:
                return json.dumps({"notes": [{"id": str(page[0]["id"]), "contentTruncated": True}], "count": 1,
                                   "hasMore": cursor is not None, "nextCursor": cursor, "truncated": True,
                                   "summary": "The note exceeded the response limit, so its content was omitted."},
                                  indent=2)
            limit = max(1, min(limit - 1, len(page) // 2))

    # Platform tools ----------------------------------------------------------------------

    def handle(self, name: str, args: dict) -> tuple[object, str | None]:
        if name.startswith("affinity_"):
            return self.affinity(name, args)
        states = requested_states(args)
        if states:
            self.stage_moves.append({"turn": self.turn, "tool": name, "states": states})
            return None, "Lifecycle moves are outside this simulation"
        if name in IDENTITY_READS:
            return self.identity_read(name), None
        if name == "field-values.getFields":
            return {"fields": self.project()["fields"]}, None
        if name in {"project.update", "project_data", "field-values.setField"} or name.startswith("identity."):
            self.field_writes.append({"turn": self.turn, "tool": name, "input": args})
            return None, "Project and identity writes are outside this simulation"
        if name in {"project.getAgentContext", "project.findById"}:
            return {"project": self.project()}, None
        if name == "project.listMembers":
            return {"members": [{"id": "member-1", "name": USER_NAME}]}, None
        if name == "project-task.listByProject":
            return {"tasks": self.tasks}, None
        if name in {"project-task.findById", "task-management.getTaskDetail"}:
            task = next((t for t in self.tasks if t["id"] in {args.get("id"), args.get("taskId")}), None)
            return (task, None) if task else (None, "Task not found")
        if name == "task-definitions.list":
            return {"definitions": [{"id": key, "slug": spec["definition"]["slug"], "title": spec["title"],
                                     "description": " ".join(str(spec["definition"].get("description", "")).split())}
                                    for key, spec in self.definitions.items()]}, None
        if name == "task-definitions.findById":
            spec = self.definitions.get(args.get("id") or args.get("taskDefinitionId"))
            return ({"id": args.get("id") or args.get("taskDefinitionId"), "slug": spec["definition"]["slug"],
                     "title": spec["title"], "fields": spec.get("fields")}, None) if spec else (None, "Task definition not found")
        if name == "task-management.createTask":
            return self.create_task(args)
        if name in TASK_SAVES:
            return self.save_output(name, args)
        if name == "task-management.askTaskQuestion":
            self.questions.append({"turn": self.turn, "input": args})
            return {"question": {"id": f"question-{len(self.questions)}", "status": "open"}}, None
        if name == "project.sendManagerMessage":
            self.manager_messages.append({"turn": self.turn, "input": args})
            return {"ok": True}, None
        if name == "activate_skill":
            return self.activate(args)
        if name in {"project.getTemplateMetadata", "project.readTemplateRange"}:
            return self.read_template(name, args)
        if name == "project.instantiateTemplate":
            return self.instantiate(args)
        if name == "artifact.createTextArtifact":
            return self.create_text(args)
        if name in DOCUMENT_LISTS:
            return {"artifacts": [self.metadata(d) for d in self.documents.values()]}, None
        if name == "artifact.waitForArtifactsReady":
            ids = args.get("artifactIds") or []
            self.processing.difference_update(ids)
            return {"artifacts": [{"id": i, "processingStatus": "READY" if i in self.documents else "NOT_FOUND"}
                                  for i in ids]}, None
        if name in DOCUMENT_READS:
            return self.read_document(name, args)
        if name == "artifact.updateTextArtifact":
            return self.update_document(args)
        if name in LINE_EDITS:
            return self.edit_document(name, args)
        if name in {"artifact.attachToChat", "artifact.detachFromChat"}:
            return {"ok": True}, None
        if name == "artifact.instantiateMarkdownTemplate":
            return None, "Markdown templates are outside this simulation"
        return None, "Tool outside the simulated scope"

    def create_task(self, args: dict) -> tuple[object, str | None]:
        definition = args.get("taskDefinitionId")
        if definition and definition not in self.definitions:
            return None, "Unknown typed task definition"
        slug = self.definitions[definition]["definition"]["slug"] if definition else None
        task_id = f"77777777-7777-4777-8777-{len(self.tasks_created) + 1:012d}"
        task = self.task_record(task_id, slug, "running", args.get("input") or {})
        self.tasks.append(task)
        self.tasks_created.append({"turn": self.turn, "slug": slug, "input": args.get("input") or {},
                                   "title": args.get("title"), "taskId": task_id})
        return {"task": task, "taskId": task_id, "action": task["action"]}, None

    def save_output(self, name: str, args: dict) -> tuple[object, str | None]:
        output = args.get("output") if isinstance(args.get("output"), dict) else {}
        record = {"turn": self.turn, "tool": name, "output": output, "ok": False, "error": None}
        self.task_saves.append(record)
        if self.agent != "analyst":
            record["error"] = "No current task in this chat"
        elif args.get("taskId") not in {None, "", TASK}:
            record["error"] = "Task not found"
        elif output.get(POINTER) not in self.documents:
            record["error"] = (f"Required output {POINTER} must be the artifact ID returned when the document was "
                               "created" if output.get(POINTER) else f"Required output {POINTER} is missing")
        if record["error"]:
            return None, record["error"]
        record["ok"] = True
        status = "completed" if name == "task-management.completeTask" else "running"
        return {"task": {"id": TASK, "status": status, "output": output}}, None

    def activate(self, args: dict) -> tuple[object, str | None]:
        wanted = args.get("skillId") or args.get("skillName")
        skill_id = next((k for k, v in self.arm["skills"].items() if wanted in {k, v["name"]}), None)
        if self.agent != "analyst" or not skill_id:
            return None, "Skill is not assigned to this agent"
        self.skills_activated.append(skill_id)
        skill = self.arm["skills"][skill_id]
        return {"status": "activated", "skillId": skill_id, "name": skill["name"], "instructions": skill["body"],
                "resources": []}, None

    def read_template(self, name: str, args: dict) -> tuple[object, str | None]:
        ref = args.get("documentRefId")
        guides = (self.arm.get("guides") or {}) if self.template else {}
        if ref == CRM_TEMPLATE_ID and self.template:
            text, artifact, filename, title = self.template, TEMPLATE_ARTIFACT, "crm-history-template.html", \
                "CRM history and context template"
        elif ref in guides:
            index = sorted(guides).index(ref) + 1
            text, artifact, filename, title = guides[ref], f"77777777-7777-4777-8777-{index:012d}", \
                GUIDE_PATHS[ref].rsplit("/", 1)[-1], ref
        else:
            return None, "Project template not found for this project type"
        lines = text.splitlines()
        result = {"projectId": PROJECT, "documentRefId": ref, "artifactId": artifact,
                  "filename": filename, "mimeType": "text/html", "title": title,
                  "documentType": "template" if ref == CRM_TEMPLATE_ID else "guidance",
                  "sourceRevisionNumber": TEMPLATE_REVISION, "sourceContentHash": sha256(text),
                  "sizeBytes": len(text.encode()), "totalLineCount": len(lines)}
        if name == "project.getTemplateMetadata":
            return result, None
        start, end = args.get("startLine") or 1, args.get("endLine") or args.get("startLine") or 1
        if not (isinstance(start, int) and isinstance(end, int)) or start < 1 or end < start or end > len(lines):
            return None, (f"Requested template line range is outside the available content. "
                          f"Valid line range is 1-{len(lines)}.")
        return {**result, "content": "\n".join(lines[start - 1:end]), "startLine": start, "endLine": end,
                "truncated": end < len(lines)}, None

    def record_created(self, tool: str, document: dict) -> None:
        self.created.append({"turn": self.turn, "tool": tool, "id": document["id"], "filename": document["filename"],
                             "owner": document["owner"], "sizeBytes": len(document["content"].encode())})

    def instantiate(self, args: dict) -> tuple[object, str | None]:
        if args.get("documentRefId") != CRM_TEMPLATE_ID or not self.template:
            return None, "Project template not found for this project type"
        if args.get("projectId") != PROJECT:
            return None, "Project not found"
        if args.get("expectedTemplateSourceRevisionNumber") != TEMPLATE_REVISION or \
                args.get("expectedTemplateSourceContentHash") != sha256(self.template):
            # On Platform a refused creation is an uncertain external effect: the task stops for good
            # (#4841 local run, one mistyped hash character). Record it so the run fails.
            self.refused_creations.append({"turn": self.turn, "input": {k: v for k, v in args.items() if k != "content"}})
            return None, "Template source changed since it was read"
        if not str(args.get("content") or "").strip():
            return None, "content must not be empty"
        document = self.add_document(f"88888888-8888-4888-8888-{len(self.documents) + 1:012d}", str(args["filename"]),
                                     str(args["content"]), "PROJECT")
        self.record_created("project.instantiateTemplate", document)
        self.saved(document)
        return {"artifact": self.metadata(document), "templateDocumentId": CRM_TEMPLATE_ID}, None

    def create_text(self, args: dict) -> tuple[object, str | None]:
        content = str(args.get("content") or "")
        if len(content.encode()) > MAX_TEXT_ARTIFACT_BYTES:
            return None, f"Text artifact content must be {MAX_TEXT_ARTIFACT_BYTES} bytes or less"
        owner = "TASK_RUN" if self.agent == "analyst" else "PROJECT"
        document = self.add_document(f"99999999-9999-4999-8999-{len(self.documents) + 1:012d}",
                                     str(args.get("filename") or "document.html"), content, owner)
        self.record_created("artifact.createTextArtifact", document)
        return {"artifact": self.metadata(document)}, None

    def read_document(self, name: str, args: dict) -> tuple[object, str | None]:
        document = self.documents.get(args.get("id") or args.get("artifactId"))
        if not document:
            return None, "Artifact not found or access denied"
        self.document_reads.append({"turn": self.turn, "tool": name, "id": document["id"]})
        meta = self.metadata(document)
        if name == "artifact.readSourceRange":
            lines = document["content"].splitlines()
            start = args.get("startLine") or 1
            end = args.get("endLine") or start
            if not (isinstance(start, int) and isinstance(end, int)) or start < 1 or end < start:
                return None, "endLine must be greater than or equal to startLine"
            if end - start + 1 > MAX_SOURCE_READ_LINES:
                return None, (f"Requested line range must not exceed {MAX_SOURCE_READ_LINES} lines. Retry with "
                              f"startLine={start} and endLine={start + MAX_SOURCE_READ_LINES - 1}.")
            if end > len(lines):
                return None, f"Requested line range is outside the source. totalLineCount={len(lines)}"
            return {**meta, "startLine": start, "endLine": end, "content": "\n".join(lines[start - 1:end])}, None
        if name == "artifact.getTextStructure":
            sections = [{"line": i, "heading": re.sub(r"<[^>]+>", "", m.group(1)).strip()}
                        for i, line in enumerate(document["content"].splitlines(), 1)
                        for m in re.finditer(r"<h[12][^>]*>(.*?)</h[12]>", line)]
            return {**meta, "sections": sections}, None
        return meta, None

    def preconditions(self, document: dict | None, args: dict) -> str | None:
        if not document:
            return "Artifact not found or access denied"
        if self.pending_edit and document["id"] == EXISTING_DOCUMENT:
            # Someone edits the document between the agent's read and its first write.
            self.pending_edit = False
            document["content"] = document["content"].replace("</article>", f"{COLLEAGUE_EDIT}\n</article>")
            document["revision"] += 1
        if document["owner"] == "TASK_RUN":
            return "TASK_RUN sources are immutable execution evidence and cannot be edited"
        if args.get("expectedSourceRevisionNumber") != document["revision"] or \
                args.get("expectedSourceContentHash") != sha256(document["content"]):
            return "Source revision changed; re-read the source metadata before preparing a new update"
        return None

    def update_document(self, args: dict) -> tuple[object, str | None]:
        document = self.documents.get(args.get("id"))
        content = str(args.get("content") or "")
        record = {"turn": self.turn, "id": args.get("id"), "sizeBytes": len(content.encode()), "ok": False, "error": None}
        self.updates.append(record)
        record["error"] = self.preconditions(document, args) or (
            f"Text artifact content must be {MAX_TEXT_ARTIFACT_BYTES} bytes or less"
            if record["sizeBytes"] > MAX_TEXT_ARTIFACT_BYTES else None)
        if record["error"]:
            return None, record["error"]
        document["content"], document["revision"], record["ok"] = content, document["revision"] + 1, True
        self.saved(document)
        return {"artifact": self.metadata(document)}, None

    def saved(self, document: dict) -> None:
        if self.deal.get("processingAfterSave"):
            self.processing.add(document["id"])

    def edit_document(self, name: str, args: dict) -> tuple[object, str | None]:
        document = self.documents.get(args.get("id"))
        record = {"turn": self.turn, "tool": name, "id": args.get("id"), "ok": False, "error": None}
        self.line_edits.append(record)
        record["error"] = self.preconditions(document, args)
        if record["error"]:
            return None, record["error"]
        lines = document["content"].splitlines()
        if name == "artifact.replaceTextRange":
            start, end = args.get("startLine"), args.get("endLine")
            if not (isinstance(start, int) and isinstance(end, int)) or not 1 <= start <= end <= len(lines) or \
                    "\n".join(lines[start - 1:end]) != args.get("expectedText"):
                record["error"] = "expectedText does not match the current source range"
                return None, record["error"]
            lines[start - 1:end] = str(args.get("replacementText") or "").splitlines()
        else:
            line = args.get("line")
            if not isinstance(line, int) or not 1 <= line <= len(lines):
                record["error"] = "Line anchor is outside the source"
                return None, record["error"]
            at = line - 1 if name == "artifact.insertTextBeforeLine" else line
            lines[at:at] = str(args.get("text") or "").splitlines()
        content = "\n".join(lines) + "\n"
        if len(content.encode()) > MAX_TEXT_ARTIFACT_BYTES:
            record["error"] = f"Text artifact content must be {MAX_TEXT_ARTIFACT_BYTES} bytes or less"
            return None, record["error"]
        document["content"], document["revision"], record["ok"] = content, document["revision"] + 1, True
        self.saved(document)
        return {"artifact": self.metadata(document)}, None


# ---------------------------------------------------------------- prompts and tools

def capability_block(frozen: dict, bundles: list[str]) -> str:
    """The platform_capabilities block: bundle names, then each prompt list as a unique union."""
    prompts = [frozen["capabilities"]["bundles"].get(b, {}) for b in bundles]

    def union(key: str) -> list[str]:
        seen: list[str] = []
        for prompt in prompts:
            values = prompt.get(key) or []
            for value in [values] if isinstance(values, str) else values:
                if value not in seen:
                    seen.append(value)
        return seen

    lines = ["Platform Capabilities:", "Capability Bundles:", *[f"- {b}" for b in bundles]]
    for key, title in (("summary", "Capability Summary"), ("capabilities", "Available Work"),
                       ("usage", "How To Use These Capabilities"), ("boundaries", "Capability Boundaries")):
        values = union(key)
        if values:
            lines += [f"{title}:", *[f"- {v}" for v in values]]
    return "\n".join(lines)


def runtime_block(frozen: dict, case: dict) -> str:
    return (f"User Name: {USER_NAME}\n\nWorkspace Name: {frozen['cases']['firmName']}\n\n"
            f"Current Deal project id: {PROJECT}\n\nProject Name: {case['deal']['name']}\n\nProject State: screening\n")


def skills_blocks(arm: dict) -> list[dict]:
    skills = arm["skills"]
    catalog = ["Assigned Skills Catalog:"] + [f"- {s['name']} ({s['activationMode']}) | id={k} | {s['description']}"
                                              for k, s in skills.items()]
    if any(s["activationMode"] == "AUTO" for s in skills.values()):
        catalog.append(SKILL_CATALOG_GUIDANCE)
    blocks = [{"text": "\n".join(catalog)}]
    always = [f"### {s['name']} ({k})\n{s['body']}" for k, s in skills.items() if s["activationMode"] == "ALWAYS"]
    if always:
        blocks.append({"text": "Active Skill Instructions:\n" + "\n".join(always)})
    return blocks


LIVING_REPORT_OUTPUT = (
    "Living report output: discover the complete current project and task-chat source set. Before saving task output, "
    "retain every source in the hidden v1 evidence manifest with its observed revision/hash, or truthfully identify an "
    "unreadable source and its gap. Editable report drafts can be incomplete; a published task output must account for "
    "the corpus. Never replace an invalid manifest with empty arrays or remove entries to bypass a refusal. Correct the "
    "reported entries on the same report, preserving all other sources; use bounded edits when practical instead of "
    "repeatedly rewriting the full document.")


def task_block(arm: dict, simulator: CrmSimulator) -> str:
    task = simulator.task_spec()
    definition = task["definition"]
    instructions = definition["definitionJson"]["instructions"]
    lines = ["Current Task Runtime Context:", f"- Task title: {task['title']}",
             f"- Internal task ID (tool/debug context): {TASK}",
             f"- Definition: {definition['name']} (slug={definition['slug']})", "- Status: running",
             "Task Instruction:", instructions["executionInstructions"].strip()]
    for key in ("missingInputPolicy", "externalActionPolicy"):
        if instructions.get(key):
            lines.append(str(instructions[key]).strip())
    criteria = instructions.get("completionCriteria") or []
    if criteria:
        lines += ["Completion Criteria:", *[f"- {c}" for c in ([criteria] if isinstance(criteria, str) else criteria)]]
    lines.append("Structured Output Contract:")
    for field in task["fields"]["output"]:
        ref = (field.get("config") or {}).get("documentRefId")
        lines.append(f"- {field['key']} ({field['name']}, {field['fieldType']})" + (" [required]" if field.get("required") else "")
                     + (f" [documentRefId={ref}]" if ref else ""))
    if LIVING_REPORT_SKILL in definition["definitionJson"].get("requiredSkills", []):
        lines.append(LIVING_REPORT_OUTPUT)
    lines.append("Task Document References:")
    for ref in definition["definitionJson"].get("documentRefs", []):
        output = f", output={ref['outputFieldKey']}" if ref.get("outputFieldKey") else ""
        lines.append(f"- {ref['documentId']} ({ref.get('usage')}, usage={ref.get('usage')}{output}) "
                     f"artifact=template-{ref['documentId'].rsplit('.', 1)[-1]}")
    lines += [TASK_REFERENCE_GUIDANCE, "Task Project Context:",
              f"- Project: {simulator.deal['name']} (id={PROJECT})", "- Project Status: active",
              "- Project State: screening", "- Project Type: Deal Pipeline (key=vc_deal_pipeline)",
              "Project Field Values:", json.dumps(simulator.project()["fields"]), PROJECT_CONTEXT_GUIDANCE,
              "Resolved Task Input:", json.dumps(simulator.task_input()),
              "Use this task runtime context as the source of truth for execution, coordination, task questions, and "
              "structured completion."]
    return "\n".join(lines)


def system_blocks(frozen: dict, arm: dict, case: dict, agent: str, simulator: CrmSimulator) -> list[dict]:
    template = arm[agent]
    blocks = [{"text": base.render_prompt(template["prompt"]["template"], frozen["variables"])},
              {"text": runtime_block(frozen, case)},
              {"text": capability_block(frozen, template["capabilityProfile"]["bundles"])}]
    if agent == "analyst":
        blocks += skills_blocks(arm) + [{"text": task_block(arm, simulator)}]
    return blocks


def tool_specs(frozen: dict, agent: str, case: dict | None = None) -> list[dict]:
    names = ANALYST_TOOLS if agent == "analyst" else frozen["managerTools"]
    tools = []
    for platform_name in names:
        if platform_name in SCHEMAS:
            description, properties, required = SCHEMAS[platform_name]
            tools.append({"toolSpec": {"name": platform_name.replace(".", "_"), "description": description,
                                       "inputSchema": {"json": {"type": "object", "properties": properties,
                                                                "required": required, "additionalProperties": True}}}})
        else:
            tools += tool_specs_from_names([platform_name])
    if (case or {}).get("affinityConnected", True) is False:
        return tools
    for tool in frozen["affinity"]["tools"]:
        tools.append({"toolSpec": {"name": tool["name"], "description": tool["description"],
                                   "inputSchema": {"json": tool["inputSchema"]}}})
    return tools


def agent_for(arm: dict, case: dict) -> tuple[str, list[str]]:
    """Who handles the case, and the user turns it receives (placeholders are filled from cases.yaml)."""
    if case["kind"] == "routing":
        return "manager", list(case["turns"])
    if case["kind"] == "skill-control":
        return "analyst", ["{taskKickoff}"]
    return ("analyst", ["{taskKickoff}"]) if arm["route"] == "analyst-task" else ("manager", ["{importRequest}"])


# ---------------------------------------------------------------- execution

def run_attempt(frozen: dict, item: dict, output: Path, invoke, ledger, settings: dict) -> dict:
    case = next(c for c in frozen["cases"]["cases"] if c["id"] == item["case"])
    arm = next(a for a in frozen["arms"] if a["name"] == item["arm"])
    limits = frozen["cases"]["run"]["limits"]
    folder = output / item["folder"]
    folder.mkdir(parents=True, exist_ok=False)
    simulator = CrmSimulator(frozen, arm, case)
    agent, turns = agent_for(arm, case)
    turns = [t.format(taskKickoff=frozen["cases"]["taskKickoff"], importRequest=frozen["cases"]["importRequest"])
             for t in turns]
    simulator.agent = agent
    tools = tool_specs(frozen, agent, case)
    names = {t["toolSpec"]["name"]: (t["toolSpec"]["name"] if t["toolSpec"]["name"].startswith("affinity_")
                                     else next(n for n in (ANALYST_TOOLS if agent == "analyst" else frozen["managerTools"])
                                               if n.replace(".", "_") == t["toolSpec"]["name"])) for t in tools}
    required = {t["toolSpec"]["name"]: t["toolSpec"]["inputSchema"]["json"].get("required", []) for t in tools}
    conversation: list[dict] = []
    replayed = 0
    record = {**item, "agent": agent, "status": "running", "turns": [],
              "usage": {"inputTokens": 0, "cachedInputTokens": 0, "outputTokens": 0, "reasoningTokens": 0}}
    started = time.monotonic()
    try:
        for turn_index, text in enumerate(turns):
            simulator.turn = turn_index
            conversation.append(base.message_item("user", text))
            system = system_blocks(frozen, arm, case, agent, simulator)
            ledger_turn = {"index": turn_index, "userText": text, "calls": [], "texts": [], "final": "", "complete": False,
                           "stopReason": None}
            record["turns"].append(ledger_turn)
            for step in range(case.get("maxSteps") or limits["maxStepsPerTurn"]):
                if time.monotonic() - started > limits["attemptWallClockSeconds"]:
                    raise TimeoutError("Attempt wall-clock limit reached")
                request = base.subject_request(frozen, system, conversation, tools)
                response, usage = base.call_provider(invoke, ledger, "subject", f"{item['folder']} t{turn_index} s{step}",
                                                     request, folder / f"t{turn_index}-s{step:02}-request.json", settings,
                                                     replayed)
                for key in record["usage"]:
                    record["usage"][key] += usage[key]
                replayed += usage["outputTokens"]
                items = base.response_items(response)
                conversation.extend(items)
                message = "\n".join(part.get("text", "") for out in items if out["type"] == "message"
                                    for part in out["content"] if part.get("type") == "output_text")
                ledger_turn["texts"].append(message)
                ledger_turn["stopReason"] = response["status"] if response["status"] == "completed" else \
                    f"incomplete:{(response.get('incomplete_details') or {}).get('reason')}"
                uses = [out for out in items if out["type"] == "function_call"]
                if response["status"] == "incomplete":
                    break
                if not uses:
                    ledger_turn["final"], ledger_turn["complete"] = message, True
                    break
                for use in uses:
                    platform_name = names.get(use["name"])
                    try:
                        arguments = json.loads(use["arguments"])
                        arguments = arguments if isinstance(arguments, dict) else None
                    except json.JSONDecodeError:
                        arguments = None
                    if arguments is None:
                        data, error, arguments = None, "Invalid JSON arguments", {"raw": use["arguments"]}
                    elif platform_name is None:
                        data, error = None, "Unknown tool"
                    elif any(arguments.get(key) in (None, "") for key in required[use["name"]]):
                        data, error = None, "Missing required argument"
                    else:
                        data, error = simulator.handle(platform_name, arguments)
                    ledger_turn["calls"].append({"name": platform_name or use["name"], "input": compact(arguments),
                                                 "error": error, "step": step, "callId": use["call_id"]})
                    conversation.append({"type": "function_call_output", "call_id": use["call_id"],
                                         "output": json.dumps({"error": error}) if error else
                                         data if isinstance(data, str) else json.dumps(data)})
                base.write_json(folder / "attempt.json", record)
            if not ledger_turn["complete"]:
                record["status"] = "incomplete"
                record["incompleteReason"] = f"turn {turn_index} ended with stopReason={ledger_turn['stopReason']}"
                break
        else:
            record["status"] = "completed"
    except KeyboardInterrupt:
        record["status"] = "interrupted"
        finish_attempt(frozen, record, folder, simulator, started)
        raise
    except base.AccountingStop as error:
        record["status"], record["incompleteReason"] = "accounting_stop", str(error)
    except base.ProviderError as error:
        record["status"], record["systematicProviderError"] = "provider_error", error.systematic
        (folder / "provider-error.txt").write_text(str(error))
    except base.BudgetExceeded as error:
        record["status"], record["incompleteReason"] = "budget_stop", str(error)
    except TimeoutError as error:
        record["status"], record["incompleteReason"] = "incomplete", str(error)
    except subprocess.TimeoutExpired:
        record["status"] = "provider_error"
        (folder / "provider-error.txt").write_text("Provider call timed out")
    return finish_attempt(frozen, record, folder, simulator, started)


def compact(arguments: dict) -> dict:
    """Long document content is saved once in documents/, not in every call record."""
    return {k: (f"<{len(v.encode())} bytes>" if k in {"content", "text", "replacementText"} and isinstance(v, str)
                and len(v) > 2000 else v) for k, v in arguments.items()}


def finish_attempt(frozen: dict, record: dict, folder: Path, simulator: CrmSimulator, started: float) -> dict:
    documents = folder / "documents"
    documents.mkdir(exist_ok=True)
    for document in simulator.documents.values():
        (documents / f"{document['id']}.html").write_text(document["content"])
    record.update({"documents": {d["id"]: {**simulator.metadata(d), "owner": d["owner"]}
                                 for d in simulator.documents.values()},
                   "created": simulator.created, "updates": simulator.updates, "lineEdits": simulator.line_edits,
                   "affinityWrites": simulator.affinity_writes, "affinityReads": len(simulator.affinity_reads),
                   "interactionFilterSearches": simulator.interaction_filter_searches,
                   "outOfScopeReads": simulator.out_of_scope_reads,
                   "refusedCreations": simulator.refused_creations,
                   "fieldWrites": simulator.field_writes, "stageMoves": simulator.stage_moves,
                   "tasksCreated": simulator.tasks_created, "taskSaves": simulator.task_saves,
                   "questions": simulator.questions, "skillsActivated": simulator.skills_activated,
                   "documentReads": simulator.document_reads, "managerMessages": simulator.manager_messages,
                   "crmDefinitionId": simulator.crm_definition,
                   "livingReportMode": (simulator.arm["skills"].get(LIVING_REPORT_SKILL) or {}).get("activationMode"), "elapsedSeconds": round(time.monotonic() - started, 3)})
    if record["status"] in {"completed", "incomplete"}:
        record["deterministic"] = score(frozen, record, {d["id"]: d["content"] for d in simulator.documents.values()})
    base.write_json(folder / "attempt.json", record)
    return record


# ---------------------------------------------------------------- scoring

def case_notes(case: dict) -> dict[int, str]:
    affinity = case.get("affinity") or {}
    notes = {}
    for holder in affinity.get("companies", []) + affinity.get("opportunities", []):
        for note in generated_notes(holder["generatedNotes"]) if holder.get("generatedNotes") else flatten_notes(holder.get("notes", [])):
            notes[note["id"]] = note["html"]
    return notes


def note_holders(case: dict) -> dict[int, int]:
    """Note ID → the company or opportunity record the notes read returns it from."""
    affinity = case.get("affinity") or {}
    holders = {}
    for holder in affinity.get("companies", []) + affinity.get("opportunities", []):
        for note in generated_notes(holder["generatedNotes"]) if holder.get("generatedNotes") else flatten_notes(holder.get("notes", [])):
            holders[note["id"]] = holder["id"]
    return holders


def appendix_entry(appendix: str, note_id: int) -> str:
    """The appendix entry (from one N anchor to the next) that names the note ID; the whole appendix without anchors."""
    starts = [m.start() for m in re.finditer(r"id=\"N\d+\"", appendix)]
    bounds = list(zip(starts, starts[1:] + [len(appendix)])) or [(0, len(appendix))]
    for start, end in bounds:
        if re.search(rf"\b{note_id}\b", appendix[start:end]):
            return appendix[start:end]
    return ""


def visible_text(document: str) -> str:
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", document)).split())


def brief_part(document: str) -> str:
    match = APPENDIX_HEADING.search(document)
    return document[:match.start()] if match else document


def appendix_part(document: str) -> str:
    match = APPENDIX_HEADING.search(document)
    return document[match.end():] if match else ""


def import_status(document: str) -> str | None:
    badge = BADGE.search(document)
    text = visible_text(badge.group(1)) if badge else visible_text(document)
    partial = re.search(r"\bpartial import\b", text, re.I) or (badge and re.search(r"\bpartial\b", text, re.I))
    complete = re.search(r"\bcomplete import\b", text, re.I) or (badge and re.search(r"\bcomplete\b", text, re.I))
    if badge and partial and complete:
        return None
    return "partial" if partial else "complete" if complete else None


def appendix_refs(document: str) -> dict[int, str]:
    """Note ID → appendix entry reference, from the entry each note ID sits in."""
    match = APPENDIX_HEADING.search(document)
    appendix = document[match.end():] if match else ""
    entries = [(m.start(), m.group(1)) for m in re.finditer(r"id=\"(N\d+)\"", appendix)]
    refs = {}
    for m in re.finditer(r"\b(\d{4,6})\b", appendix):
        owner = [ref for start, ref in entries if start < m.start()]
        if owner and int(m.group(1)) not in refs:
            refs[int(m.group(1))] = owner[-1]
    return refs


def cited_refs(brief: str) -> set[str]:
    """Every note reference the brief cites, with ranges such as [N2–N4] expanded."""
    refs = set()
    for group in CITATION_GROUP.finditer(visible_text(brief)):
        for m in CITATION_REF.finditer(group.group(1)):
            first, last = int(m.group(1)), int(m.group(2) or m.group(1))
            refs.update(f"N{n}" for n in range(first, max(first, last) + 1))
    return refs


def appendix_anchors(document: str) -> set[str]:
    return set(re.findall(r"id=\"(N\d+)\"", appendix_part(document)))


def final_document(record: dict, documents: dict[str, str], refresh: bool) -> tuple[str | None, str]:
    if refresh:
        return EXISTING_DOCUMENT, documents.get(EXISTING_DOCUMENT, "")
    created = record["created"]
    return (created[-1]["id"], documents[created[-1]["id"]]) if created else (None, "")


def score(frozen: dict, record: dict, documents: dict[str, str]) -> dict:
    expectations = frozen["expectations"]
    expect = expectations["cases"][record["case"]]
    case = next(c for c in frozen["cases"]["cases"] if c["id"] == record["case"])
    calls = [call for turn in record["turns"] for call in turn["calls"]]
    reply = record["turns"][-1]["final"] if record["turns"] else ""
    if case["kind"] == "skill-control":
        # Only the first steps run; the report itself is not simulated, so completion is not expected.
        # The import's search and read-scope rules do not apply: report tasks may read lists or people.
        assertions = {"noAffinityWrites": not record["affinityWrites"], "noFieldWrites": not record["fieldWrites"],
                      "noStageMove": not record["stageMoves"],
                      "livingReportActive": record.get("livingReportMode") == "ALWAYS"
                      or LIVING_REPORT_SKILL in record["skillsActivated"]}
        return {"passed": all(assertions.values()), "assertions": assertions,
                "info": {"skillsActivated": record["skillsActivated"]}}
    assertions = {
        "allTurnsComplete": all(turn["complete"] for turn in record["turns"]) and record["status"] == "completed",
        "noInvalidToolCalls": not any(call["error"] in INVALID_CALL_ERRORS for call in calls),
        "noAffinityWrites": not record["affinityWrites"],
        # An interaction filter hides companies whose record holds only notes (#4841 Dev run).
        "noInteractionFilter": not record.get("interactionFilterSearches"),
        "noOutOfScopeReads": not record.get("outOfScopeReads"),
        "noFieldWrites": not record["fieldWrites"],
        "noStageMove": not record["stageMoves"],
    }
    info: dict = {}
    for pattern in expect.get("replyMentions", []):
        assertions[f"replyMentions:{pattern}"] = bool(re.search(pattern, reply, re.I))
    if case["kind"] == "import":
        refresh = bool(expect.get("refresh"))
        doc_id, document = final_document(record, documents, refresh)
        ok_updates = [u for u in record["updates"] if u["ok"] and u["id"] == EXISTING_DOCUMENT]
        ok_edits = [e for e in record["lineEdits"] if e["ok"]]
        info.update({"documentId": doc_id, "sizeBytes": len(document.encode()), "createdCount": len(record["created"]),
                     "fullUpdates": len(ok_updates), "lineEdits": len(ok_edits),
                     "skillActivated": "import-crm-history" in record["skillsActivated"]})
        if expect.get("blocked"):
            assertions["noDocument"] = not record["created"] and not any(u["ok"] for u in record["updates"]) \
                and not ok_edits
            assertions["noPointerSaved"] = not any(s["ok"] for s in record["taskSaves"])
        else:
            if refresh:
                # One full-document update of the supplied document, and no piecemeal line edits.
                assertions["oneDocument"] = not record["created"] and len(ok_updates) == 1 and not ok_edits \
                    and not any(u["ok"] for u in record["updates"] if u["id"] != EXISTING_DOCUMENT)
            else:
                # Only a template copy is a PROJECT_SHARED document a refresh can update. A refused copy
                # would have stopped the task on Platform, so a retry after it does not count.
                assertions["oneDocument"] = len(record["created"]) == 1 and \
                    record["created"][0]["tool"] == "project.instantiateTemplate" and \
                    not record.get("refusedCreations") and \
                    not any(u["ok"] for u in record["updates"] if u["id"] != doc_id)
            # The task completes on its own; saving output alone leaves it open and the pointer unwritten.
            assertions["completedWithPointer"] = any(s["ok"] and s["tool"] == "task-management.completeTask"
                                                     and s["output"].get(POINTER) == doc_id for s in record["taskSaves"])
            assertions["safeHtml"] = bool(document) and not UNSAFE_HTML.search(document)
            # The complete saved HTML must stay refreshable under the platform's update limit.
            assertions["withinSizeLimit"] = bool(document) and len(document.encode()) <= MAX_TEXT_ARTIFACT_BYTES
            notes = case_notes(case)
            retained = expect.get("notesRetained", [])
            assertions["briefCitesNotes"] = bool(document) and (not retained or bool(CITATION.search(visible_text(brief_part(document)))))
            # A citation must point at an entry the appendix actually holds.
            unresolved = sorted(cited_refs(brief_part(document)) - appendix_anchors(document))
            assertions["citationsResolve"] = bool(document) and not unresolved
            info["citationsUnresolved"] = unresolved
            overview = OVERVIEW.search(brief_part(document))
            assertions["briefSubstantive"] = bool(overview) and \
                len(WORD.findall(visible_text(overview.group(1)))) >= MIN_OVERVIEW_WORDS and \
                not any(placeholder in visible_text(document) for placeholder in TEMPLATE_PLACEHOLDERS)
            # In the appendix itself: a note quoted in the brief but dropped from the appendix is not retained.
            appendix = appendix_part(document)
            appendix_text = html.unescape(appendix)
            missing = [n for n in retained if not contains_note(appendix, notes[n])
                       or not all(link in appendix_text for link in note_links(notes[n]))]
            assertions["notesRetained"] = bool(document) and not missing
            info["notesMissing"] = missing
            # Each retained note names the record it was read from, not another matching record.
            holders = note_holders(case)
            misattributed = [n for n in retained if not re.search(rf"\b{holders[n]}\b", appendix_entry(appendix, n))]
            assertions["notesAttributed"] = bool(document) and not misattributed
            info["notesMisattributed"] = misattributed
            if expect.get("notesAbsent"):
                assertions["notesAbsent"] = not any(contains_note(document, notes[n]) for n in expect["notesAbsent"])
            if expect.get("importStatus"):
                info["importStatus"] = import_status(document)
                assertions[f"importStatus:{expect['importStatus']}"] = info["importStatus"] == expect["importStatus"]
            # Facts the case needs belong in the brief, not only in the retained notes. Links may sit
            # with their note in the appendix, so links count anywhere in the document.
            brief = brief_part(document)
            text = visible_text(brief) + " " + " ".join(re.findall(r"href=\"([^\"]+)\"", document))
            for pattern in expect.get("documentMentions", []):
                assertions[f"documentMentions:{pattern}"] = bool(re.search(pattern, text, re.I))
            for pattern in expect.get("documentForbidden", []):
                assertions[f"documentForbidden:{pattern}"] = not re.search(pattern, visible_text(brief_part(document)), re.I)
            for text_kept in expect.get("documentKeeps", []):
                assertions[f"documentKeeps:{text_kept}"] = visible_text(text_kept) in visible_text(document)
            if expect.get("stableRefs"):
                refs = appendix_refs(document)
                info["appendixRefs"] = {str(k): v for k, v in refs.items() if k in map(int, expect["stableRefs"])}
                assertions["stableRefs"] = all(refs.get(int(k)) == v for k, v in expect["stableRefs"].items())
    else:
        crm_tasks = [t for t in record["tasksCreated"] if t["slug"] == CRM_SLUG]
        if "createsCrmTask" in expect:
            assertions["createsCrmTask"] = (len(crm_tasks) == 1) if expect["createsCrmTask"] else not crm_tasks
        if expect.get("passesProvider"):
            assertions["passesProvider"] = any(re.search(expect["passesProvider"], str(t["input"].get("crm_provider", "")),
                                                         re.I) for t in crm_tasks)
        if "createsTask" in expect:
            assertions["createsTask"] = bool(record["tasksCreated"]) == expect["createsTask"]
        if expect.get("noManagerDocument"):
            assertions["noManagerDocument"] = not record["created"] and \
                not any(u["ok"] for u in record["updates"]) and not any(e["ok"] for e in record["lineEdits"])
        if expect.get("readsDocument"):
            assertions["readsDocument"] = any(r["id"] == EXISTING_DOCUMENT and r["tool"] in
                                              {"artifact.readSourceRange", "artifact.getTextStructure"}
                                              for r in record["documentReads"])
    return {"passed": all(assertions.values()), "assertions": assertions, "info": info}


def summarise(records: list[dict], arms: list[str], case_ids: list[str]) -> dict:
    cells = {}
    for arm in arms:
        for case in case_ids:
            rows = [r for r in records if r["arm"] == arm and r["case"] == case]
            ran = [r for r in rows if "deterministic" in r]
            failed: dict[str, int] = {}
            for r in ran:
                for key, value in r["deterministic"]["assertions"].items():
                    if not value:
                        failed[key] = failed.get(key, 0) + 1
            cells[f"{arm}/{case}"] = {"passed": sum(r["deterministic"]["passed"] for r in ran), "scored": len(ran),
                                      "planned": len(rows), "failedAssertions": failed,
                                      "sizeBytes": [r["deterministic"]["info"].get("sizeBytes") for r in ran
                                                    if r["deterministic"]["info"].get("sizeBytes")]}
    totals = {arm: {"passed": sum(c["passed"] for k, c in cells.items() if k.startswith(arm + "/")),
                    "scored": sum(c["scored"] for k, c in cells.items() if k.startswith(arm + "/"))} for arm in arms}
    return {"cells": cells, "totals": totals}


REPLY_EXCERPT_CHARS = 4000


def results_rows(records: list[dict]) -> list[dict]:
    """Committable per-attempt rows: verdicts, failed assertions, key facts and the bounded final reply."""
    rows = []
    for record in records:
        row = {"arm": record["arm"], "case": record["case"], "repetition": record["repetition"],
               "agent": record.get("agent"), "status": record["status"]}
        if "deterministic" in record:
            reply = record["turns"][-1]["final"] if record["turns"] else ""
            row.update({"passed": record["deterministic"]["passed"],
                        "failedAssertions": [k for k, v in record["deterministic"]["assertions"].items() if not v],
                        "info": record["deterministic"]["info"],
                        "tasksCreated": [{k: t[k] for k in ("slug", "input")} for t in record["tasksCreated"]],
                        "finalReply": reply if len(reply) <= REPLY_EXCERPT_CHARS else reply[:REPLY_EXCERPT_CHARS] + " [truncated]"})
        rows.append(row)
    return rows


def write_report(output: Path, manifest: dict) -> None:
    arms, case_ids = manifest["armNames"], manifest["caseIds"]
    cells = manifest["summary"]["cells"]
    lines = ["# CRM history import comparison (issue #4841)", "",
             f"Status: **{manifest['status']}**. Halted: {manifest.get('halted') or 'no'}.",
             "Scope: simulated prompt/tool-choice evidence; not Platform integration or deployed proof.", "",
             "| Case | " + " | ".join(arms) + " |", "|---|" + "---|" * len(arms)]
    for case in case_ids:
        lines.append(f"| {case} | " + " | ".join(f"{cells[f'{arm}/{case}']['passed']}/{cells[f'{arm}/{case}']['scored']}"
                                                  for arm in arms) + " |")
    lines.append("| **total** | " + " | ".join(
        f"**{manifest['summary']['totals'][a]['passed']}/{manifest['summary']['totals'][a]['scored']}**" for a in arms) + " |")
    lines += ["", "## Failed checks", ""]
    for key, cell in cells.items():
        if cell["failedAssertions"]:
            lines.append(f"- {key}: " + ", ".join(f"{k} ×{v}" for k, v in sorted(cell["failedAssertions"].items())))
    lines += ["", f"Spend: {json.dumps(manifest['spend'])}", "",
              "Read the saved documents and final replies as well; checks are regexes and word matches, not a judge."]
    (output / "report.md").write_text("\n".join(lines) + "\n")


def rescore(directory: Path) -> dict:
    """Re-score a finished run's saved attempts with the current expectations and scorer. No provider access."""
    frozen = {"cases": yaml.safe_load(CASES.read_text()), "expectations": yaml.safe_load(EXPECTATIONS.read_text())}
    records = []
    for path in sorted(directory.glob("attempts/*/attempt.json")):
        record = json.loads(path.read_text())
        documents = {p.stem: p.read_text() for p in (path.parent / "documents").glob("*.html")}
        if record["status"] in {"completed", "incomplete"}:
            record["deterministic"] = score(frozen, record, documents)
        records.append(record)
    rows = results_rows(records)
    return {"scorer": "current", "attempts": rows,
            "totals": {arm: {"passed": sum(1 for r in rows if r["arm"] == arm and r.get("passed")),
                             "scored": sum(1 for r in rows if r["arm"] == arm and r.get("passed") is not None)}
                       for arm in sorted({r["arm"] for r in rows})}}


def preflight(args: argparse.Namespace, frozen: dict) -> dict:
    cases = frozen["cases"]
    arms = [a["name"] for a in frozen["arms"]]
    selected = [c for c in cases["cases"] if not args.case or c["id"] in args.case]
    reps = args.repetitions or cases["run"]["repetitions"]
    plan = plan_attempts(selected, arms, reps)
    limits = cases["run"]["limits"]
    turns = {c["id"]: len(c.get("turns") or [None]) for c in cases["cases"]}
    problems = list(frozen["problems"])
    unknown = sorted(set(args.case or []) - {c["id"] for c in cases["cases"]})
    if unknown:
        problems.append(f"Unknown --case ids {unknown}")
    routes = {a["name"]: a["route"] for a in frozen["arms"]}
    return {"identity": frozen["identity"], "armNames": arms, "armRoutes": routes, "caseIds": [c["id"] for c in selected],
            "repetitions": reps, "attemptPlan": plan, "attempts": len(plan),
            "maxSubjectCalls": sum(turns[p["case"]] * limits["maxStepsPerTurn"] for p in plan), "limits": limits,
            "proposedCeilingUsd": cases["run"]["proposedCeilingUsd"], "maxWallMinutes": args.max_wall_minutes,
            "blockingProblems": problems, "ready": not problems}


def streaming_openai_invoke(request: dict, request_path: Path, settings: dict) -> dict:
    """Subject route with a streamed response. A long document write can take over a minute to generate,
    and a non-streamed request is cut off after about 60 idle seconds; streaming keeps the connection busy.
    Same single submission, no retries; the final response object is what a non-streamed call returns.
    callTimeoutSeconds bounds the whole call, not each read."""
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise base.ProviderError("OPENAI_API_KEY is not set", systematic=True)
    http = urllib.request.Request(settings["endpoint"], data=json.dumps({**request, "stream": True}).encode(),
                                  method="POST", headers={"Authorization": f"Bearer {key}",
                                                          "Content-Type": "application/json",
                                                          "Accept": "text/event-stream"})
    deadline = time.monotonic() + settings["timeout"]
    try:
        with urllib.request.urlopen(http, timeout=STREAM_READ_TIMEOUT_SECONDS) as response:
            for raw in response:
                if time.monotonic() > deadline:
                    raise base.ProviderError(f"Call exceeded {settings['timeout']} seconds")
                line = raw.decode().strip()
                if not line.startswith("data:"):
                    continue
                event = json.loads(line[5:].strip())
                if event.get("type") in STREAM_FINAL_EVENTS:
                    return event["response"]
                if event.get("type") in {"error", "response.failed"}:
                    raise base.ProviderError(f"Stream error: {json.dumps(event)[:2000]}")
    except urllib.error.HTTPError as error:
        raise base.ProviderError(f"HTTP {error.code}: {error.read().decode(errors='replace')[:2000]}",
                                 systematic=400 <= error.code < 500 and error.code not in base.TRANSIENT_HTTP) from error
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        raise base.ProviderError(f"{type(error).__name__}: {error}") from error
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise base.ProviderError("Provider returned an invalid stream event", systematic=True) from error
    raise base.ProviderError("Stream ended without a final response")


def execute(args: argparse.Namespace, invoke=None) -> dict:
    real_provider = invoke is None
    invoke = invoke or streaming_openai_invoke
    frozen = freeze(args.arm)
    report = preflight(args, frozen)
    if not report["ready"]:
        raise SystemExit("Not ready for paid execution: " + "; ".join(report["blockingProblems"]))
    run = frozen["cases"]["run"]
    if not base.positive_finite(args.max_spend_usd) or args.max_spend_usd > run["proposedCeilingUsd"]:
        raise SystemExit("--max-spend-usd must be positive, finite and no higher than the frozen proposed ceiling")
    if real_provider and not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY is not set; refusing before any output or dispatch")
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    ledger = base.SpendLedger(run["prices"], args.max_spend_usd, output / "ledger.jsonl")
    manifest = {"startedAt": datetime.now(timezone.utc).isoformat(), "status": "running", "identity": frozen["identity"],
                "subject": run["subject"], "limits": run["limits"], "ceilingUsd": args.max_spend_usd, "pid": os.getpid(),
                "maxWallMinutes": args.max_wall_minutes, "armNames": report["armNames"], "caseIds": report["caseIds"],
                "scope": "prompt-tool-choice-with-simulated-affinity-and-platform-tools", "records": []}
    base.write_json(output / "run.json", {k: v for k, v in manifest.items() if k != "records"})
    base.write_json(output / "preflight.json", report)
    for arm in frozen["arms"]:
        (output / f"manager-{arm['name']}.yaml").write_text(arm["managerRaw"])
        (output / f"analyst-{arm['name']}.yaml").write_text(arm["analystRaw"])
    ledger.event("run_start", ceilingUsd=args.max_spend_usd, attempts=report["attempts"])
    settings = {"endpoint": run["subject"]["endpoint"], "timeout": run["limits"]["callTimeoutSeconds"]}
    previous = signal.signal(signal.SIGTERM, base.raise_interrupt)
    consecutive, halted, current = 0, None, None
    deadline = time.monotonic() + args.max_wall_minutes * 60
    try:
        for item in report["attemptPlan"]:
            if time.monotonic() > deadline:
                halted = f"overall wall-clock limit of {args.max_wall_minutes} minutes"
                break
            current = item
            ledger.event("attempt_start", folder=item["folder"])
            record = run_attempt(frozen, item, output, invoke, ledger, settings)
            ledger.event("attempt_end", folder=item["folder"], status=record["status"])
            manifest["records"].append(record)
            current = None
            consecutive = consecutive + 1 if record["status"] == "provider_error" else 0
            if record["status"] == "budget_stop":
                halted = "spend ceiling"
            elif record["status"] == "accounting_stop":
                halted = ledger.halt
            elif record.get("systematicProviderError"):
                halted = "systematic provider error (not retried); see provider-error.txt"
            elif consecutive >= run["limits"]["maxConsecutiveProviderErrors"]:
                halted = "consecutive provider errors"
            verdict = record.get("deterministic", {}).get("passed")
            print(f"{record['status']:<15} {'PASS' if verdict else 'FAIL' if verdict is False else '-':<4} {item['folder']}"
                  f"  spent=${ledger.spent:.3f}", flush=True)
            if halted:
                break
    except KeyboardInterrupt:
        halted = "interrupted"
        if current:
            attempt_file = output / current["folder"] / "attempt.json"
            manifest["records"].append(json.loads(attempt_file.read_text()) if attempt_file.exists()
                                       else {**current, "status": "interrupted"})
            ledger.event("attempt_end", folder=current["folder"], status="interrupted")
    finally:
        signal.signal(signal.SIGTERM, previous)
    done = {r["folder"] for r in manifest["records"]}
    manifest["records"] += [{**i, "status": "not_run", "reason": halted} for i in report["attemptPlan"] if i["folder"] not in done]
    # The skill-control case stops at its step cap by design, so its "incomplete" attempts are expected.
    capped = {c["id"] for c in frozen["cases"]["cases"] if c["kind"] == "skill-control"}
    incomplete = halted or any(r["status"] != "completed" and not (r["case"] in capped and r["status"] == "incomplete")
                               for r in manifest["records"])
    manifest.update({"finishedAt": datetime.now(timezone.utc).isoformat(), "status": "incomplete" if incomplete else "completed",
                     "halted": halted, "spend": ledger.totals(),
                     "summary": summarise(manifest["records"], report["armNames"], report["caseIds"])})
    base.write_json(output / "summary.json", manifest)
    base.write_json(output / "results.json", {"identity": frozen["identity"], "subject": run["subject"],
                                              "status": manifest["status"], "halted": halted, "spend": manifest["spend"],
                                              "summary": manifest["summary"], "attempts": results_rows(manifest["records"])})
    base.write_json(output / "run.json", {k: v for k, v in manifest.items() if k not in {"records", "summary"}})
    write_report(output, manifest)
    ledger.event("run_end", status=manifest["status"], spend=ledger.totals())
    return manifest


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--arm", action="append", default=[], metavar="NAME=REVISION",
                        help="Pack arm; repeat for each arm (git revision, or WORKTREE for the working tree)")
    parser.add_argument("--case", action="append", default=[], help="run only this case id (repeatable)")
    parser.add_argument("--repetitions", type=int, help="override the frozen repetition count")
    parser.add_argument("--execute", action="store_true", help="make paid calls (requires --output and --max-spend-usd)")
    parser.add_argument("--output", type=Path, help="new output directory for --execute")
    parser.add_argument("--max-spend-usd", type=float, help="hard spend ceiling at Platform-billable prices")
    parser.add_argument("--max-wall-minutes", type=float, default=DEFAULT_MAX_WALL_MINUTES,
                        help=f"stop dispatching new attempts after this many minutes (default {DEFAULT_MAX_WALL_MINUTES})")
    parser.add_argument("--preflight-out", type=Path, help="write the no-spend preflight JSON here")
    parser.add_argument("--rescore", type=Path, help="re-score a finished run's saved attempts with the current scorer (no spend)")
    parser.add_argument("--reconcile", type=Path, help="rebuild spend accounting from a run's ledger after a hard kill")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    if args.reconcile:
        print(json.dumps(base.reconcile(args.reconcile), indent=2))
        return
    if args.rescore:
        result = rescore(args.rescore)
        base.write_json(args.rescore / "rescored.json", result)
        print(json.dumps(result["totals"], indent=2))
        return
    if not args.arm:
        raise SystemExit("At least one --arm is required")
    if args.execute:
        if not args.output or args.max_spend_usd is None:
            raise SystemExit("--execute requires --output and --max-spend-usd")
        manifest = execute(args)
        print(json.dumps({"status": manifest["status"], "halted": manifest["halted"], "spend": manifest["spend"],
                          "totals": manifest["summary"]["totals"]}, indent=2))
        raise SystemExit(0 if manifest["status"] == "completed" else 2)
    report = preflight(args, freeze(args.arm))
    if args.preflight_out:
        base.write_json(args.preflight_out, report)
    print(json.dumps({k: v for k, v in report.items() if k not in {"attemptPlan", "identity"}}, indent=2))
    raise SystemExit(0 if report["ready"] else 1)


if __name__ == "__main__":
    main()
