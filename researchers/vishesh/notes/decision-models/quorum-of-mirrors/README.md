# Quorum of Mirrors — revised design and offline contracts

QM-2 narrows DM-02 to a useful test: does a source-aware instruction help when a crowd repeatedly sees the same observations and only partial ancestry is available?

- [Plan](PLAN.md): generator, information boundaries, comparisons, metrics, stages and visualization mapping.
- [Review and issue ledger](REVIEW.md): evaluation against the handoff and prior critique, verification and remaining gates.
- [Reference contracts](reference.py) and [tests](test_reference.py): deterministic offline instrument checks; no provider or scientific-run entry point.

## Current evidence

No native Quorum of Mirrors run is recorded in the reviewed upstream snapshot. Adaptive-quorum is a different project. Fourteen offline unit tests pass; they establish narrow software properties, not model competence or intervention efficacy. The revised design is not an accepted hypothesis or preregistered run.

A hand-derived example uses three observations [positive, negative, negative], each with reliability 0.8. Their independent-root posterior is 20%. Counting three copies of each as independent gives 1/65 (1.54%); counting seven copies of the positive and one of each negative gives 1024/1025 (99.90%). The information did not change. Full-lineage deduplication preserves 20% in both cases. With two roots concealed, capping opaque evidence can instead yield 50%; another fixture shows that capping can discard helpful evidence. These are analytical examples checked by tests, not measured model behavior.

Run software validation from the repository root:

```sh
python3 -m unittest discover -s researchers/vishesh/notes/decision-models/quorum-of-mirrors -p 'test_*.py' -v
```

No model calls, external services, experiment assignments or credential access occur. The first live screen still needs completed research/review gates, a frozen provider/assignment contract, verified public-plan registration, exclusive allocation and a separate authorized budget. Paid budget is zero until authorized. A public design document alone does not satisfy these gates.
