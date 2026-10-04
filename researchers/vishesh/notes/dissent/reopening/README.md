# Reliable reopening diagnostic draft

**The design revision is implemented and checked offline. No new native run has started.** RD5's adverse fixed-reserve result remains complete. The proposed next study asks whether history, opposing ballots, clock or evidence age can disrupt otherwise correct use of fresh evidence.

[Prospective plan](PLAN.md) · [Structured proposal](next-run-plan.json) · [Concrete case preview](offline/preview.html) · [Validation](offline/validation.json) · [Draft quality review](DRAFT-REVIEW.md) · [Remaining implementation](IMPLEMENTATION.md) · [Parent result](../rd5/REPORT.md) · [Authoritative study setup](../rd5/SETUP.md).

The plan was published at `0c00781507b9477bfa2347504ed0bade43a7ae4b` before the new case implementation. It accepts the trace-grounded context diagnosis, rejects another fixed-reserve sweep and keeps the simple literal controller as the practical comparator. The new action ordering is fixed within each case; changing timestamps cannot silently reorder the choices.

## Concrete improvements

- Twelve reciprocal stop/resume cases in six authored base families across process readings, bridge capacity and required build tests. All six context variants preserve the correct answer.
- Separate history-only, ballots-only and full-context conditions; absolute clock translation preserves age and deadline slack, while the age-only variant changes neither clock nor history.
- Two identical-input repeats per diagnostic cell, randomized in separate blocks. Qualification is separate; its answers are not reused as the main comparison's clean baseline.
- A scorer retaining all assignments, false commitments, unresolved service, invalid/missing responses, repeated-answer disagreement and paired missingness bounds.
- A literal comparator using actor-visible inputs. Deliberately wrong history/majority/always-DEFER policies fail the known-answer checks. This is software evidence, not a native result or independent audit.

**23 offline tests pass**, covering all 162 proposed request fixtures. The largest serialized request is 2,712 bytes. The fixture manifest, dependency hashes, tests and reader preview are retained. No credentials, network/provider requests or budget-ledger mutations are used by the builder. The preview contains expected labels only, clearly outside actor requests.

## What remains a draft

The proposed sequence is 18 Q0 calls and, only after a correct valid Q0, 144 D0 calls. There are 12 authored diagnostic cases, six shared families and three reused grammars; these are not 144 independent tasks. There is no untouched or independently sourced holdout. This small stage diagnoses a component and cannot establish a robust field policy or emergent swarm behavior.

Native dispatch is not implemented in this package. Its existing transport/ledger integration must be extended and tested prospectively, preserving the old fences and original ledger, after the scope decision and before launch readiness. Public registration, source/runtime, price, approved-account allocation and current admission evidence are also absent because nothing is being launched.

Disposition: **DECISION NEEDED** on whether this narrow component question is worth collecting. It proposes at most 162 new calls, lifetime 650, which is 150 above the original 500-call ceiling; the USD 2 split cap is unchanged. Conservative combined exposure would remain below USD 1.068 under the stated route and machine ceilings. The owner must approve that changed scope and call ceiling before allocation or dispatch. If Jev is not needed for a later semantic task, the literal baseline already supplies the practical answer and this draft should be parked.

## Reproduce the offline preparation

```sh
python3 researchers/vishesh/notes/dissent/reopening/prepare_offline.py
```

This runs known-answer/fault checks and exports the authored fixtures. It never starts an experimental worker. The preserved RD5 source, results, qualification and approved stop of 488 are unchanged.

The HTML fixture viewer was generated and its input data were checked, but browser rendering is unverified: the browser URL policy blocked opening the local file. See [preview status](offline/preview-status.json). This does not affect the Python case/scoring checks.
