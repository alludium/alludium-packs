# CRM history import evals (issue #4841)

Cases and expectations for the "Import or Refresh CRM History" task added in VC Pack `0.6.41`.
The baseline arm (`v0.6.40`) is what users had: the Deal Manager reads Affinity in chat and
answers, which produced the reported CRM inventory. The candidate should create a sourced CRM
history document for the Deal through the Deal Analyst task and refresh that same document, keep every retrieved note in full, say
when an import is partial, refuse to save a history too large to refresh, and change nothing else.

## Cases

Every company, person, note and ID is invented (`.example` domains, plus invented `tallowmere`
names for the case where the company is named by its domain).

- **Import cases** (27): a rebrand with nine notes, history held on a second record, the record
  with the history on the second page of search results, two similarly
  named companies that must not be merged, a company whose only similarly named records have another
  domain (it must stop, not import a near match), a company named by its domain whose record has notes
  but no interactions (an interaction filter on the search hides it), people listed on the company record that must be
  labelled as profile facts rather than credited to notes, paging, a page that keeps failing (partial import), a
  linked data room that must not be treated as read, no notes, Deal fields that must not change, a
  refresh of an existing document (same ID, stable note references), an instruction hidden in a
  note, a history larger than the 100 KB document limit on first import and on refresh, a company
  with no CRM record, a saved document that no longer exists, a document a colleague edits between
  the refresh's read and its write (the edit must survive), a second import while another is still
  running and has created its document (it must stop), another open import with no document yet (it
  must go ahead: an open task alone is not a reason to stop), a large history (about 55 KB of notes) that fits and must be
  kept in full on first import and on refresh, a refreshed document that is still processing just after the save, no CRM
  connection, and no Affinity grant for the agent.
- **Routing cases** (5): the Deal Manager starts the task for an import or refresh request, answers
  a read-only question without starting it, uses the saved document in a fresh chat, and does not
  start a second import while one is running.
- **Controls** (4): the analyst still activates the living-report method on each of the four
  investment-report tasks (Screening, Evaluation, IC Memo, Term Sheet Review) now that the skill is
  AUTO instead of ALWAYS. They run four steps only and score just that; their capped attempts end
  `incomplete` by design and do not mark the run incomplete.

## Run

`plugins/vc/scripts/compare_crm_history_import.py` runs the cases on the Luna subject (OpenAI
Responses API) with the same settings and spend ledger as the #4449 and #4843 comparisons. Subject calls are streamed, because a long document write takes over a minute to
generate and a non-streamed call was cut off after about 60 seconds. Without
`--execute` it is a no-spend preflight. A run makes paid calls and needs an `OPENAI_API_KEY`.

```sh
python plugins/vc/scripts/compare_crm_history_import.py \
  --arm baseline=v0.6.40 \
  --arm candidate=<candidate commit> \
  --execute --output /tmp/crm-history-4841 --max-spend-usd 15 --max-wall-minutes 180
```

Preflight (2 arms, 36 cases, 3 repetitions): 216 attempts, at most 40 counted steps per turn plus 20
tool-discovery steps. `--rescore DIR` re-scores a finished run without spend; `--reconcile DIR`
rebuilds spend accounting after a hard stop. `WORKTREE` as a revision reads the working tree, for
local checks only.

## What is simulated

- **Affinity**: the connector's read and write tool definitions, copied verbatim from
  `@alludium/affinity-mcp-server` 1.0.4 (`affinity-tools.json`). Responses follow the connector's
  JSON shapes, cursor and search-token paging and 25,000-character page shrinking. Search results
  follow the connector's implementation (`companies`, `nextPageToken`); its tool description still
  says `organizations` and `next_page_token`, and the skill accepts either token name. Writes get Platform's read-only
  refusal and are recorded. Case `pageSize` caps a page so paging is exercised. With `fieldTypes: ["enriched"]`, a company record returns its
  Description and People fields inline, as the connector does. A search with `withInteractionDates` or
  `withInteractionPersons` drops companies without interactions, as live Affinity did in the #4841 Dev
  run. The connector's list, list-entry, person and field read tools are offered too, as on
  Platform; the import must not call them, and a call is recorded and answered with an empty page.
- **Tool discovery**: as on Dev, the Affinity tools start inactive. The agent finds them with
  `tools_search_available` or `tools_list_available` and turns each on with `tool_activate`
  (descriptions and result shapes copied from Craft `runtime-discovery-tools.ts`); an Affinity tool is
  callable only from the step after it is activated. Search returns at most 20 summaries (50 on
  request) and leaves out `affinity_search_companies` unless the limit is at least 25: it was missing
  from all 11 Affinity searches of the 0.6.46 Dev run, where one import stopped as "unavailable", and a
  local probe on 0.6.49 found it 25th for its own name, missing at the default limit and present with
  `limit: 50`. Listing the `affinity-mcp-server` app pages through every tool. An activation by `toolExternalId` (the tool name, for Affinity) or `toolId`
  works; one by `toolName` alone is refused with `LOCKED_PROJECT_AGENT_SELECTION_FORBIDDEN`, as all 9
  such activations were in a local Deal. As on Platform, steps that only search, list or activate
  tools do not use the step budget (up to 20 such steps a turn). A step that activates ends Platform's
  invocation, and after three invocations in a row with no other tool call `tool_activate` is withdrawn
  for the rest of the turn. A disconnected CRM's tools can still be listed and activated, and the first
  Affinity call then fails; without an Affinity grant the list is empty and every activation is refused. Every discovery call is recorded. A case
  sets `affinityToolsInactive: false` to hand the tools over directly.
- **Platform**: the agents' capability-bundle guidance as Platform renders it
  (`capability-prompts.json`, from Craft `c69fe008`), the skills catalog with ALWAYS skill bodies,
  `activate_skill`, a task runtime block built from the task definition, reads of the project template and
  the two shared guides the task names, template instantiation with revision/hash checks (a refused copy fails the
  run, because on Platform it stops the task), documents that
  report processing after a save until waited for (in the processing case), artifact metadata, range reads (200 lines), full updates
  (100 KB) and line edits with preconditions, immutable task-run files, task output save and
  completion, and the manager's frozen tool contract.

Approximations: the task block is a trimmed copy of Platform's template; `task-management.completeTask`
is offered directly (Platform hydrates it for tasks that complete without human confirmation); Platform
tools are offered directly, and only the Affinity tools go through tool discovery; the manager's tool schemas are
the generic contract schemas. Not covered: a document still processing (simulated documents are
always ready) and a Deal with no Organisation (the task cannot start without one). Two first
imports started at the same moment can both pass the pre-create check: the Pack re-checks live
state, but only Platform can make that check atomic. This is prompt and tool-choice evidence,
not Platform integration or deployed proof.

## Scoring

Deterministic checks only, over the saved document, the recorded tool calls and the final reply:
one template copy (or one updated document on refresh), the task completed with its output pointing
at it, safe static HTML, a filled company overview with citations and no template instructions
left, case facts present in the brief itself, every expected note's words present in order and
unbroken inside the source appendix with its links kept, the wrong company's notes absent, a colleague's edit kept,
the complete/partial label, stable references on refresh, mentions and forbidden present-tense or
"the deck shows" claims, no Affinity search with an interaction filter, no list, list-entry, person
or field reads, and no Affinity, field (including `field-values.setField`) or stage writes.
Routing checks look at which task was created and its provider, document reads and the reply.
There is no judge; read the saved documents and replies too. Offline scorer and simulator tests:
`plugins/vc/scripts/test_crm_history_eval.py`.

## Status

**Run 1** (baseline `v0.6.40`, candidate `480dc53`, `gpt-5.6-luna`, medium reasoning, 3
repetitions, $1.15 of a $15 ceiling, all 829 calls settled, not halted): baseline 4/63, candidate
49/63. Reading the failures, 12 of the candidate's 14 were scorer mistakes, so the scorer was
corrected before relying on the numbers:

- the read-only `identity.listProjectLinks`, which the Deal Manager prompt tells it to call, was
  counted as a Deal write (all 6 candidate and 57 baseline `noFieldWrites` failures); identity
  reads now get simulated answers and only identity writes count;
- citations written as links (`[<a href="#N1">N1</a>]`) were not recognised; citations are now
  matched on the brief's visible text;
- the size-limit reply pattern missed "above the platform's 90 KB pre-save threshold";
- the step-capped control marked the whole run `incomplete`; its capped attempts are now expected.

Run 1 also found two real candidate misses, fixed in the skill and task: one appendix note lost a
word ("raise a €2m seed" became "raise €2m seed"), and with two records sharing the company's
domain the analyst asked which to use instead of importing both. A blocked import also ended by
pointing to a file that was never saved.

**Run 2** (baseline `v0.6.40`, candidate `05ad94e`, same settings, $1.39 of a $5 ceiling including
$0.23 held for one timed-out call, not halted): baseline 10/63, candidate 59/62 (one attempt lost to
a provider timeout). The three candidate failures were scorer misses ("would exceed", "90,000-byte",
"No CRM notes"), since widened. Every one of the 186 notes the cases require was kept word for word,
both records sharing a domain were imported without asking, and no blocked reply pointed to a file.
Run 1 rescored with the corrected scorer: baseline 4/63, candidate 55/63, the remaining failures
being the two real misses above and identity reads the old simulator recorded as writes.

A cold review then tightened the method and the scorer: a first import re-reads the Deal's live
state and stops if another import is running or has created its document; a refused refresh
rebuilds from the current content so a colleague's edit survives; a saved document over the limit
is reported as a blocker; failed pages on refresh are not reported as deleted notes; the task must
complete with its pointer; documents must be template copies; notes are checked in the appendix;
the analyst is offered field tools; and the controls cover all four reports. Run 3 checks the
final candidate.

John's scope clarification on #4841 (comment 6505641852) then narrowed the first-import check:
only a CRM history document already on the Deal stops a first import, and another open import
task alone does not (case `other-import-open-no-document`). The Deal Manager still points a
repeat request to the open import. Overlapping imports can therefore still create duplicate work
or documents, an accepted limitation of this delivery.

Disposition for the analyst task, skill, template and Deal Manager routing surface (VC Pack
`v0.6.40`..candidate): `ran-with-evidence` for runs 1 and 2; run 3 pending.

**Tool discovery, 0.6.49** (#4841: on Dev, one import stopped as "Affinity unavailable" when tool search
left out `affinity_search_companies`). Old `3a9ecda` against new, cases `no-notes` and
`domain-as-name-no-interactions`, 5 repetitions, with the Affinity tools starting inactive:

- **Run A** (new `c4536e1`), $0.60: both arms' pass counts (2/10 and 1/10) came from a simulator
  mismatch. It required `taskId` on `completeTask`, which Platform fills in. This was fixed in `22093d4`.
- **Run B** (new `22093d4`), $0.58: old 10/10, new 10/10.
  - The old arm searched first in 10/10 attempts.
  - The new arm never searched. It activated all five read tools by `toolExternalId` first in 10/10.
  - No attempt stopped as unavailable.

The pass rate doesn't separate the arms, because the simulated old skill also recovered every time. The
evidence for the fix is how the tools were found, plus 9 real local runs: the tool was found in 7/9, and
the other 2 never started because the chat lost the message.
