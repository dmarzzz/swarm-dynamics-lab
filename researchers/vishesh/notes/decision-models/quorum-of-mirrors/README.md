# Quorum of Mirrors — design, instrument and native qualification

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by vishesh/codex-pi-review; source `9781739c` ([registry](../../../../../experiments/evidence-metadata.json), [rubric](../../../../../experiments/EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **1/4** — A native reader can make the evidence-based MAP choice on the small S0 fixture screen; source-aware swarm efficacy is untested. Basis: The predeclared small competence screen passed; two of 16 repeated pairs disagreed. This is qualification, not an effect comparison or general reliability sample. Intended swarm benefit remains untested.
- **sample_size_summary:** S0: 16 synthetic patterns × 2 identical-request samples = 32/32 valid decisions; 29 correct. S1 not run.
<!-- experiment-evidence:end -->

QM-2 narrows DM-02 to a useful test: does a source-aware instruction help when a crowd repeatedly sees the same observations and only partial ancestry is available?

- [Plan](PLAN.md): generator, information boundaries, comparisons, metrics, stages and visualization mapping.
- [Review and issue ledger](REVIEW.md): evaluation against the handoff and prior critique, verification and remaining gates.
- [Reference contracts](reference.py) and [tests](test_reference.py): deterministic offline instrument checks; no provider or scientific-run entry point.

## Current evidence

[The first native S0 screen passed](RESULTS.md): 29/32 correct MAP choices, all 32 responses valid, 14/16 identical-request pairs agreeing. API cost $0.00103152. A zero-call setup failure was preserved and repaired before the successful attempt. All 27 offline tests pass. This qualifies a small evidence-reading task, not swarm efficacy. Adaptive-quorum is a different project. Formal survey and hypothesis review remain open.

The sections below retain the design and preparation history; RESULTS.md and the attempt-2 post-mortem are current.

A hand-derived example uses three observations [positive, negative, negative], each with reliability 0.8. Their independent-root posterior is 20%. Counting three copies of each as independent gives 1/65 (1.54%); counting seven copies of the positive and one of each negative gives 1024/1025 (99.90%). The information did not change. Full-lineage deduplication preserves 20% in both cases. With two roots concealed, capping opaque evidence can instead yield 50%; another fixture shows that capping can discard helpful evidence. These are analytical examples checked by tests, not measured model behavior.

Run software validation from the repository root:

```sh
python3 -m unittest discover -s researchers/vishesh/notes/decision-models/quorum-of-mirrors -p 'test_*.py' -v
```

No model calls, external services, experiment assignments or credential access occur. The first live screen still needs completed research/review gates, a frozen provider/assignment contract, verified public-plan registration, exclusive allocation and a separate authorized budget. Paid budget is zero until authorized. A public design document alone does not satisfy these gates.

## S0 preparation history (superseded by the result above)

The QM-2 design is published. The owner requested continuing through the shared worker workflow. The prospective [S0 plan](reviews/S0-01-pre.md), [request/scoring implementation](qualification.py), and [additional tests](test_qualification.py) prepare a 32-call Jev competence matrix. Twenty-three offline tests now pass. `qualification.py --prepare PATH` writes the exact manifest without model calls; `--analyze MANIFEST --receipts JOURNAL` checks saved outcomes. No live dispatcher or credential relay is included yet.

Exploratory S0/S1 are allowed under the worker template while the formal survey remains open; S2 waits. The requested isolated budget is $1 API plus $1 dedicated infrastructure for at most six hours, pending owner approval. No allocation or paid request has occurred. Qualification labels are exact MAP answers, not sampled world truth; native API choice scores are not presented as calibrated beliefs.
