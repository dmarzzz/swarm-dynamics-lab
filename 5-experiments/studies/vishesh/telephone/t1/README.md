# Telephone T1: offline measurement iteration

2026-10-04 · Vishesh / codex-village-fit · **HOLD native collection**.

The [prospective plan](PLAN.md) preceded implementation. This iteration implements annotation arithmetic, strengthens original regression cases, and indexes retained private source candidates. It is not a native attempt or evidence that structured retelling works.

- [Casebook](CASEBOOK.md): eight authored roots, 24 scripted trajectories, 72 hop outputs.
- [Case-quality assessment](CASE-QUALITY.md): bounded software readiness, no natural-data readiness.
- [Post-mortem and handoff](POST-MORTEM.md): scientific assessment and exact next action.
- [Validation receipt](VALIDATION.json), [fixture outcomes](FIXTURE-RESULTS.json), [source coverage](CANDIDATE-COVERAGE.json).

## Reproduce from the repository root

```sh
python3 -m unittest discover -s 5-experiments/studies/vishesh/telephone/t1/tests -v
python3 -m unittest discover -s 5-experiments/studies/vishesh/ai-village-replay-2026-10-04/tests -v
python3 5-experiments/studies/vishesh/telephone/t1/src/fixtures.py
python3 scripts/experiment.py inspect telephone
```

Python standard library only. `src/candidates.py PRIVATE_PROJECTION_DIR NEW_PRIVATE_OUTPUT_DIR` recreates candidate bundles from the retained four projections; stdout contains aggregate counts and hashes only. The original corpus is not distributed here. Public reproducibility covers the authored fixtures; private candidate coverage requires the pinned projections with matching hashes.

## Measurement contract

`scoring.score(text, review, gold, visible_source_ids)` requires evaluator-only canonical seven-field annotations, exact output/gold hashes, a completed assertion-review attestation and obligation mappings. The scorer cannot validate semantic judgments or detect an annotator who omits an assertion. Real use still needs the two-pass annotation process in the parent specification and evidence/visibility review. Canonical field equality is an annotation contract, not literal-string scoring of prose.

An obligation is retained only if at least one mapped assertion exists and every mapped assertion matches an acceptable fact/support variant. Duplicate assertions do not add credit; inconsistent duplicate judgments fail. Missing, invalid, unreviewed and scored outputs remain distinct. Citation validity is a separate diagnostic, preventing structured output from receiving primary credit merely for source IDs. No source-content hash or entailment verification is implied by an output/gold binding.

`reconcile_chain` requires three assigned hops and prevents descendants after unavailable output. `paired_summary` preserves the assigned component denominator and supplies worst-case bounds for missing pairs; these are identification bounds, not confidence intervals. Fixtures provide evaluator labels explicitly. Actor projections use source records only; no model receives gold because no model is called.

Source-copy and exact-reference baselines score 1.0 on all eight roots. This is a software ceiling, not evidence of efficacy or a reason to handicap the baseline. No P/S/R treatment comparison, holdout, native qualification, run admission, machine or paid call exists.
