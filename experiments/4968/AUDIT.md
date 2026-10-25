# Current VC agents: source audit and evaluation boundary

Observed 25 October 2026 for Platform issue #4968.
Packs source is pinned to `cd76e41fa4c5fe74692e3b4b29763eb24460eb7f`; Craft source to
`6902348e5680f67798f521bd2c7fa309c233b5ec`. Source declarations do not prove which Pack,
model, skills or connections a hosted workspace has installed.

## Which agents actually serve the current Deal Pipeline?

| Agent | Actual template and scope | Declared capabilities and rules |
|---|---|---|
| Pipeline Manager | [`vc_pipeline_autopilot`, v1.0.24](../../plugins/vc/alludium/agent-templates/vc_pipeline_autopilot.yaml), workspace-bound Deal type | Bounded portfolio reads/create/update; exact company identity; task coordination; file authoring; web search. Human authority for mutations. Creation uses `project.createFromChat`; company identity and duplicate acknowledgements are separate requirements. |
| Deal Manager | [`vc_deal_pipeline_manager`, v1.0.13](../../plugins/vc/alludium/agent-templates/vc_deal_pipeline_manager.yaml), one Deal | Current project reads and bounded updates; task creation/readback; identity maintenance; files and web. Trusted incoming-message attribution takes precedence; an agent-origin handoff is recommendation-only. |
| Deal Analyst | [`vc_deal_analyst`, v1.0.7](../../plugins/vc/alludium/agent-templates/vc_deal_analyst.yaml), one task/report | Current project reads, task-output save and manager handoff; file authoring/rewrite; web. Four durable reports with source/citation and refresh rules. Cannot create tasks, change stages/identity or make investment decisions. |

These are not the older `vc_deal_manager` Deal Room template or the generic Platform page agents.
The Pack manifest binds `vc_workspace` to Pipeline Manager. All three declare baseline `NONE`;
the bundles add specific allowed repository operations. Pipeline/Deal Manager always load citation
and identity guidance; Pipeline also loads pipeline hygiene and next-step generation. Analyst always
loads living-report and citation guidance, with methodology skills selected automatically.

The actual Craft capability definitions (`config/capability-profiles/platform-defaults.yaml` at the pinned Platform revision)
show why a generic tool catalogue is not native parity:

- `PROJECT_PORTFOLIO_OPERATIONS`: `project.listNavigation`, `listCreationFieldOptions`,
  `createFromChat`, `applyPortfolioOperations`.
- `INVESTMENT_SUBJECT_LOOKUP`: `identity.lookupCandidates`, `findOrganisation`,
  `project.listInvestmentSubjectDeals`.
- `PROJECT_CONTEXT_READ`: project context/find/members, project task reads and task-definition reads.
- `PROJECT_TASK_COORDINATION`: `task-management.createTask` and `getTaskDetail`.
- `TASK_OUTPUT_SAVE`: `task-management.saveTaskOutput`, present only in trusted task context;
  saving output does not complete the task. `PROJECT_MANAGER_HANDOFF`: `project.sendManagerMessage`.

## Connected applications and discovery

All three declare `ALL_CONNECTED_APPS` with `connectedApplicationExecutionMode: READ_ONLY`.
That is a permitted discovery/execution policy, not evidence that an app is connected. The
runtime discovery implementation (`packages/services/src/tool/runtime-discovery-tools.ts` at the pinned Platform revision)
provides search/list of permitted capabilities, exact-tool activation, and direct invocation.
The runtime guidance (`packages/services/src/chat/agent-execution/agent-executor.ts#L2412` at the pinned Platform revision)
explicitly separates discovery/activation from connection readiness and handles restart internally.
The connected-app execution policy (`packages/services/src/tool/connected-application-execution-policy.ts` at the pinned Platform revision)
classifies trusted read tools; activation does not grant write authority.

Existing search and category filtering are sufficient infrastructure for an initial discovery
experiment. No measured evidence here supports introducing CRM/email/meeting-note categories.
A useful next comparison holds permitted schemas, account and connection fixtures fixed and asks
for the exact company's latest CRM record, founder email and meeting note. Score wrong-company
reads, unsupported claims of connection, and correct handling of unavailable/expired/denied tools.
Do not treat category labels as capability or credential grants.

## Concrete mismatch and existing owner

Deal Manager currently instructs a named Fund write through `project_data.update_state` with
nonempty `fieldValues`, and Decision Record indexing through broad `project.update` field writes.
Craft's synthetic runtime handler (`packages/services/src/tool/synthetic-runtime-tools.ts#L1560` at the pinned Platform revision)
rejects legacy agent field writes. This is an identified source contract mismatch, not a reproduced
hosted failure.

Issue #4687 already owns the Pack correction,
including installed Pipeline Manager and Screening-task persistence proof and preserving lifecycle
transitions. It remained open and unassigned at this audit. PR #4861
remained open at `29eef5629cddb3e0e962fe3064c0c7fbdebac4d2`, adding the Platform
`platform_record_field_maintenance` skill and runtime exposure of `field-values.getFields/setField`.
Current main's method definitions alone do not grant these methods to these templates. Related
read/adoption work is #4829 and
#4795.

Decision: leave shipped prompts unchanged here. A prompt-only method substitution would teach an
unavailable capability and duplicate #4687. Use the accepted Platform skill contract and one agreed
installed Pack/runtime candidate for that issue's before/after regression. The prepared exact-Fund
case and negative controls are in [README.md](README.md#native-field-write-case-prepared-not-run).

## Existing evaluation harnesses

[Packs Deal Manager evaluation](../../plugins/vc/scripts/README.deal-manager-evaluation.md) sends real
prompt text to Bedrock with synthetic schemas and receipts. It preserves model calls and usage,
but does not install runtime skills or exercise native persistence. Its default uses paid API calls;
it was not invoked. The paired prompt/Fund/stage comparators have per-call spend reservation and
are suitable for a separately authorized paid prompt experiment, not proof of native execution.

Craft's native `test:eval:agent` path can execute the Platform runtime and reserve temporary fixture
assets. Its model-comparison wrapper (`tools/evals/agent-evals/run-model-comparison.ts#L723` at the pinned Platform revision)
enforces known cost **between cells**. It has no verified worst-case reservation before every
provider call. Under the behavior-eval skill it remains prepare-only here. A native comparison needs
that guard, isolated fixture storage, a pinned installed Pack and the same tool/skill contract.

The separate [24-cell design](README.md) uses subscription clients and a local synthetic server.
It compares current source prompt text against neutral guidance inside each client, with literal
native method/skill references identified as a boundary mismatch. It is meaningful model/tool
behavior evidence within that simulator, not actual internal-agent performance. One observation per
cell and different client models preclude a statistical ranking or cross-client causal claim.

## Shared operations: bounded next step

The field-write mismatch supports checking prompt-to-capability compatibility before increasing
catalogue breadth. Reuse the existing capability profiles and repository operation definitions as
source of truth. A future preflight could reject a prompt that names a removed write path or lacks
its required skill/tool grant; it should understand explicitly deferred activation and should not
infer permission from names. First demonstrate that check on the accepted #4687/#4861 candidate.
This audit does not justify a new operation registry or a category subsystem.
