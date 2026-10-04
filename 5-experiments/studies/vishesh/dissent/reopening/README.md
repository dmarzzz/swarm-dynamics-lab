# Reliable reopening diagnostic

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by vishesh/codex-decision-models; source `4e830695` ([registry](../../../../../experiments/evidence-metadata.json), [rubric](../../../../../experiments/EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **1/4** — On 18 authored qualification requests, Jev correctly handled all clean and conflicting-current controls but chose PROCEED on all three expired favorable observations; qualification failed. Basis: Q0-A2 completed 18/18 valid native responses and scored 15/18. All traces and original-ledger charges reconcile, with complete operational and owning scientific reviews. The inspected controls share three grammars and do not isolate context mechanisms or estimate a field failure rate. D0 was not run; its causal context and repeat contrasts remain untested. The prior zero-dispatch attempt is preserved.
- **sample_size_summary:** Observed Q0: 18 authored controls sharing three grammars; 18/18 valid, 15/18 correct (clean 12/12, conflict 3/3, stale 0/3). No independent field sample or holdout. D0: unrun; planned 12 cases × 6 conditions × 2 repeats = 144 dependent requests. Q0-A1: zero dispatch.
<!-- experiment-evidence:end -->

**The approved Q0-A2 replacement completed with 18 valid responses but failed qualification at 15/18.** All 12 clean and three current-conflict controls were correct; all three expired favorable observations incorrectly produced PROCEED. D0 was not run. The [result](REPORT.md), [post-mortem](reviews/Q0-A2-POST.md) and [owning quality review](reviews/Q0-A2-QUALITY.json) are complete; workers, relay and allocation are released. RD5's adverse fixed-reserve result and Q0-A1's zero-dispatch failure remain preserved.

[Prospective plan](PLAN.md) · [Structured proposal](next-run-plan.json) · [Concrete case preview](offline/preview.html) · [Validation](offline/validation.json) · [Draft quality review](DRAFT-REVIEW.md) · [Native integration](IMPLEMENTATION.md) · [Operator handoff](OPERATOR.md) · [Parent result](../rd5/REPORT.md) · [Authoritative study setup](../rd5/SETUP.md).

The plan was published at `0c00781507b9477bfa2347504ed0bade43a7ae4b` before the new case implementation. It accepts the trace-grounded context diagnosis, rejects another fixed-reserve sweep and keeps the simple literal controller as the practical comparator. The new action ordering is fixed within each case; changing timestamps cannot silently reorder the choices.

## Concrete improvements

- Twelve reciprocal stop/resume cases in six authored base families across process readings, bridge capacity and required build tests. All six context variants preserve the correct answer.
- Separate history-only, ballots-only and full-context conditions; absolute clock translation preserves age and deadline slack, while the age-only variant changes neither clock nor history.
- Two identical-input repeats per diagnostic cell, randomized in separate blocks. Qualification is separate; its answers are not reused as the main comparison's clean baseline.
- A scorer retaining all assignments, false commitments, unresolved service, invalid/missing responses, repeated-answer disagreement and paired missingness bounds.
- A literal comparator using actor-visible inputs. Deliberately wrong history/majority/always-DEFER policies fail the known-answer checks. This is software evidence, not a native result or independent audit.

**88 offline tests pass**, covering all 162 proposed request fixtures. The largest serialized request is 2,712 bytes. The fixture manifest, dependency hashes, tests and reader preview are retained. The native suite adds admission, original-ledger, byte delivery, failure/lifecycle, accounting, artifact and closeout checks using fake transports and disposable synthetic ledgers. No credentials, network/provider requests or budget-ledger mutations are used by the builder. The preview contains expected labels only, clearly outside actor requests.

## Current boundary

The proposed sequence is 18 Q0 calls and, only after a correct valid Q0, 144 D0 calls. There are 12 authored diagnostic cases, six shared families and three reused grammars; these are not 144 independent tasks. There is no untouched or independently sourced holdout. This small stage diagnoses a component and cannot establish a robust field policy or emergent swarm behavior.

The manual native runner completed the approved replacement once. [Current status](RUN-STATUS.md) separates completed execution, failed qualification, reviewed science and costs. The original ledger now contains 506 calls and USD 0.023434447 committed API, including historical unknown reservations. Q0-A2 added USD 0.000735378 in settled API cost.

Disposition: **FINISH / PARK — retain the valid negative qualification and leave D0 unrun.** The fixed 18/18 qualification gate was not softened. The three stale misses do not isolate history, ballots or time, and the unrun matrix supplies no causal context estimate. The literal baseline already supplies a correct practical answer for this finite task. A further model comparison needs a demonstrated unresolved use case, not another favorable-outcome attempt.

## Reproduce the offline preparation

```sh
python3 researchers/vishesh/notes/dissent/reopening/prepare_offline.py
```

This runs known-answer/fault checks and exports the authored fixtures. It never starts an experimental worker. The preserved RD5 source, results and qualification are unchanged; 488 is its historical call-count boundary, while the cumulative ledger now has 506 calls.

The HTML fixture viewer was generated and its input data were checked, but browser rendering is unverified: the browser URL policy blocked opening the local file. See [preview status](offline/preview-status.json). This does not affect the Python case/scoring checks.
