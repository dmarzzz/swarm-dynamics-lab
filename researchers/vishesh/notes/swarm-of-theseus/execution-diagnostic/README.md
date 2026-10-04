# Theseus targeted execution repairs

D1 is complete: 144 calls, 480 assigned decisions, $0.178341 model cost, no retries. See [results and postmortem](RESULTS-D1.md), [full evidence](results/D1/evidence.tar.gz), and [next design revision](NEXT-PLAN.md). Atomic calls scored 96/96; the matched batched condition scored 89/96. This is execution evidence, not cultural preservation. [PLAN.md](PLAN.md) was committed before implementation. [REPAIR-MAP.md](REPAIR-MAP.md) maps every one of the 13 historical errors to retained regression fixtures and specific controlled contrasts. Original v2 outcomes and stop rules are preserved.

The native runner, balanced case generator, five controlled request interfaces, independent command/truth audit, assigned-denominator analysis, durable failure accounting and saved-record viewer are implemented. Nineteen offline checks pass, including reporting-interruption reconciliation without repeating model calls. This is implementation validation, not evidence that the model is repaired.

| Change | Built behavior | How D1 tests it |
|---|---|---|
| R1 instruction consistency | Separate explicit-rule executor prompt; old framing retained only in A | B-A |
| R2 evidence reading | Each case retains all three sources under named JSON keys | C-B |
| R3 conflicting output representations | Decisions-only arms omit notebook from prompt and schema; never overwrite an emitted command from prose | D-C |
| R4 cross-case interference | Stateless one-case requests with identical mapping and documentation | E-D |
| R5 coverage and shortcut defects | Each class/source contains all four signal/freshness pairs; independent opaque IDs/order | Mandatory coverage assertions before assignment; no post-hoc gate repair |
| R6 reliable evaluation | Strict invalid-response accounting, independent truth/command comparison, raw records and all planned denominators | Fault checks and complete post-run analysis |

The completed screen used 144 calls / 480 assigned decisions / 3 independent worlds, maximum USD 5 and 2 hours, serial dispatch, no retries. Atomic and batched arms match cases, not compute. Each condition must be reported even if worse. No automatic culture-pilot launch or performance claim follows from unit tests. Researcher review is not required by owner direction. Public registration, dedicated-host, operator-assessment and budget checks passed before execution; [PRE-RUN.md](PRE-RUN.md) preserves the historical build-only assessment.

## Local checks

From the repository root:

```sh
python3 -m unittest discover -s researchers/vishesh/notes/swarm-of-theseus/execution-diagnostic/tests -v
```

No network, credentials or model calls. Python standard library only for these tests. `regressions.json` contains the 13 prior wrong cases solely as development fixtures; new assignments never read it.

## Prepare the next run without launching

On the final clean published checkout:

```sh
python3 researchers/vishesh/notes/swarm-of-theseus/execution-diagnostic/src/runner.py prepare /tmp/theseus-d1-prepared
```

Use a fresh output directory. This only writes the 144 exact planned requests, assignment/source/instrument hashes and a deliberately blocked admission template. It creates no experiment outcomes and sends no provider requests.

The operator then resolves applicable independent review, verifies pricing and non-overlapping authorized budget, obtains a fresh exclusive fleet claim, deploys this exact source/dependencies and verifies workload/credentials without exposing their values. Publish a new immutable diagnostic-only pre-review, register `swarm-of-theseus-execution-d1` with the immutable PLAN URL and TLDR, visually verify the page, and complete a fresh admission receipt. The reviewer must differ from the operator. Fill actual evidence references; never fabricate fields to get past the gate. No new server purchase is included.

On that admitted dedicated host, with its existing approved secure credential mechanism populating the worker environment:

```sh
python3 researchers/vishesh/notes/swarm-of-theseus/execution-diagnostic/src/runner.py run \
  --admission /srv/swarm/theseus-d1-admission.json \
  --output /srv/swarm/theseus-d1-results/D1
```

Do not put credential values into arguments, receipts or logs. The runner requires `/usr/local/lib/swarm/swarm_report.py` and its authorized reporting configuration. It reserves the allocation ID in a host-wide registry before creating a fresh per-run quota ledger. A duplicate allocation/output cannot be resumed or reset by this launcher. Cross-host budget exclusivity remains the operator's central-authority verification responsibility; a local ledger is not authority.

Failure handling preserves call-start and finished records, writes every assigned terminal outcome, and attempts to close started dashboard records. Report errors stop dispatch; they never retry a model call. `terminal.json` names pending reporting reconciliation and renderer failure separately from execution. Abrupt process/host death may leave an ambiguous started call; retain its reservation and analyze the existing records, never rerun it invisibly. Reconcile the central reservation and release the exclusive host after uploads.

## Inspect and analyze

`python3 src/analyze.py RESULTS_DIRECTORY` recomputes every assigned cell, adjacent world contrasts, incident invariance groups, missingness, false holds/ships and costs. `src/render.py` exposes `render(RESULTS_DIRECTORY)` to write `replay.html` from saved records; it is also called by the runner. It shows the raw response next to viewer-only evaluation, never a invented repair narrative. Empty/missing outcomes remain visible. The optional `tests/render_fixture.py OUTPUT_DIRECTORY` produces an explicitly labeled software-viewer fixture, not model evidence.

A next admitted model run can answer which interface changes help this finite explicit-rule task. Acquisition, changed-rule identifiability, swarm advantage and cultural preservation still require their own subsequent designs.

Shared registry validation: the full strict check currently fails on the pre-existing missing `discussion-memory-v3-film-v1.mp4` artifact. Neither new Theseus artifact produces a validation error. Repository checks pass with five pre-existing library-link warnings. This upstream file is not fabricated or removed from its owner’s manifest.
