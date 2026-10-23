# Deal stage-move comparison (issue #4843)

Status: **incomplete**. Halted: no.
Scope: simulated prompt/tool-choice evidence; not Platform integration or deployed proof.

| Case | baseline | candidate | candidate-prompt-only |
|---|---|---|---|
| reported-phrase | 0/3 | 3/3 | 0/3 |
| column-phrase | 3/3 | 3/3 | 0/3 |
| label-term-sheet | 1/3 | 3/3 | 0/3 |
| key-phrase | 2/3 | 3/3 | 0/3 |
| already-there | 0/3 | 3/3 | 3/3 |
| backtrack-with-reason | 3/3 | 3/3 | 0/3 |
| memo-edit-control | 1/3 | 1/3 | 2/3 |
| unknown-stage-control | 0/3 | 3/3 | 0/3 |
| grouped-column-control | 2/3 | 3/3 | 3/3 |
| agent-origin-control | 3/3 | 3/3 | 3/3 |
| quoted-control | 3/3 | 3/3 | 3/3 |
| refused-move | 0/3 | 3/3 | 0/3 |
| **total** | **18/36** | **34/36** | **14/36** |

Spend: {"ceilingUsd": 7.0, "confirmedUsd": 0.144727, "unreconciledExposureUsd": 0.0, "spentUsd": 0.144727, "directProviderConfirmedUsd": 0.111328, "dispatchedCalls": 313, "settledCalls": 313, "unreconciledCalls": 0, "accountingHalt": null}

Read the saved final replies as well; reply checks are regexes, not a semantic judge.
