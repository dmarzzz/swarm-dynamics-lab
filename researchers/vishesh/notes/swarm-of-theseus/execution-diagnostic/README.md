# Theseus targeted execution repairs

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by vishesh/codex-theseus; source snapshots shown per cohort ([registry](../../../../../experiments/evidence-metadata.json), [rubric](../../../../../experiments/EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

**Swarm of Theseus D2 executor confirmation** (`theseus-execution-d2`)
Source: `66d20ec1`.

- **evidence_confidence:** **1/4** — Atomic calls outperform eight-case batches on six fixed executor worlds, but neither interface qualifies for the later study. Basis: Complete paired diagnostic and full-contract audit; E gains 7.55 points in all six worlds but fails strict gates. Finite Boolean tasks, dependent repetitions and unequal compute prevent a general reliability or culture claim.
- **sample_size_summary:** Observed: six paired fixed worlds, two Boolean families, 96 distinct case/family pairs; 432/432 calls and 768 assigned decisions. D 344/384, E 373/384; both fail qualification. Two orders and two native repetitions are dependent.

**Swarm of Theseus R1 atomic repair** (`theseus-execution-r1`)
Source: `c4c7a879`.

- **evidence_confidence:** **1/4** — Repaired atomic executor F qualifies on the fresh fixed R1 screen; a material repair advantage and cultural preservation are unestablished. Basis: F192/192 versus E188/192 across six fixed worlds; all accounting/audits complete. Gain2.08points in two worlds misses the prospective material-benefit criterion. Bundled repair, finite Boolean tasks and dependent repetitions limit generality.
- **sample_size_summary:** Observed: six fresh paired fixed worlds,96 distinct case/family pairs;384/384 calls/decisions,192 per arm, two native repetitions. F192/192 qualifies; E188/192 fails. Acquisition and cultural turnover not run.
<!-- experiment-evidence:end -->

## Current outcome: execution repair cycle complete

[D2 postmortem](RESULTS-D2.md): 432/432 calls, D 344/384 versus E 373/384. Atomic execution helps, but both gates fail. [R1 postmortem](RESULTS-R1.md): 384/384 fresh calls, unchanged E 188/192 versus repaired F 192/192. F qualifies; its 2.08-point paired gain does not meet the separate material-benefit threshold. Freeze F as a candidate executor, stop this repair line, and use the [next proposal](NEXT-PLAN.md) to qualify acquisition before selective inheritance.

Both complete raw audits agree with primary scores. New model spend USD0.626774; estimated cumulative D1/D2/R1 spend USD0.812231 of the original USD5. The sim-dmarz-3 claim is released after worker exit and verified artifacts. Cultural preservation remains untested. Historical plans and outcomes below are retained, not live launch authorization.

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

## Follow-up analysis and next run

The [deeper D1 interpretation](INTERPRETATION-D1.md) shows that D's seven errors are three distinct failures, with only four of six distinct valid releases accepted. The [D2 plan](D2-PLAN.md) tests batching, order sensitivity and native repeatability on six fresh worlds. D2 and its single fresh repair are now complete; [setup evidence](D2-SETUP.md) and [R1 setup](R1-SETUP.md) record the gates and closeout.

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

The operator then resolves applicable independent review, verifies pricing and non-overlapping authorized budget, obtains a fresh exclusive fleet claim, deploys this exact source/dependencies and verifies workload/credentials without exposing their values. Publish a new immutable diagnostic-only pre-review, register `swarm-of-theseus-execution-d1` with the immutable PLAN URL and TLDR, visually verify the page, and complete a fresh admission receipt. Researcher review is not required by owner direction; the owning operator completes the assessment. Fill actual evidence references; never fabricate fields to get past the gate. No new server purchase is included.

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

The completed D2/R1 runs answer the bounded executor question within their stated limits. Acquisition, changed-rule identifiability, swarm advantage and cultural preservation still require their own subsequent designs.

Shared validation limitations are recorded in results/R1/validation-closeout.json. Do not confuse unrelated registry failures with native execution or qualification.

## Current continuation: A1 acquisition

[A1 status](A1-STATUS.md): prospective plan and tested instrument published;204planned calls,0native calls. Orbital-one dispatch compatibility is blocked; no culture result. R1's bounded F qualification remains the latest native evidence.

## Latest native attempt: A1

[A1 postmortem](RESULTS-A1.md): actual direct launch stopped on its firstHTTP429;1/204calls,0model responses,203unstarted, no retry. Prior estimated plus unknown exposureUSD0.8226830437/5. Acquisition remains untested; R1's qualified supplied-policy executor is not a cultural result.
