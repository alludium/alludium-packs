# Run attribution Pack companion — 6 September 2026

This is the Pack companion to Platform issue #4063
and PR #4073, Platform head
`89c148a334643659708bb97e4c895e383f8a49fc`. It is stacked on Pack #92 at
`855377c49b34fda783128337427a1c91391c2811`; the frozen #4072 validation pair is unchanged.

Source review found that Run VC Sourcing Pipeline still instructed the model to write Line status,
count and artifact summary fields. Platform now derives these from the exact attributed task and
committed finalization records. Removed that conflicting instruction, kept artifact IDs in the run
output and explicitly separated proposed candidates from created records. Registration carries the
exact originating sourcing run only when a run exists. Manual registration retains its existing
three required inputs and omits optional attribution. Invalid supplied attribution must be corrected,
not silently erased to evade validation.

Bumped the two changed task template versions and proposed Pack 0.6.27, including plugin/catalog/docs
references. This is an unreleased version: no tag, publish, deployment or installed runtime was changed.
Generated Markdown remains derived from the canonical YAML. Tests check the manual/run distinction,
exact-run handoff and the proposal-versus-created boundary; they do not prove native agent behavior.

Validation: full Pack validation passed (100 task templates), generated Markdown check passed
(123 files), release contract passed against the exact stacked base, and all 39 Python contract
tests passed. The new test is included in CI. Live paired/native/hosted validation remains pending;
these instructions require Platform #4073 and must not be presented as already deployed.
