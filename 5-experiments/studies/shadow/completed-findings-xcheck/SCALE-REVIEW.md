# Sybil scaling: independent arithmetic review

Reviewer `shadow/sol-xcheck`, 2026-10-04. Verdict: headline arithmetic agrees; revise cell-ranking counts. This is a post-hoc arithmetic review, not independent raw-record verification or formal experiment approval. Snapshot and reproducibility are in [README](README.md).

## Evidence and recomputation

Inputs: `5-experiments/studies/dmarz/sybil-scale-{api,sonnet,opus}/results-cells.csv`, `results-summary.json`; Opus `model-comparison-{sonnet,haiku}-cells.csv`. All are pinned and hashed in [recomputed.json](recomputed.json). Sources: [Opus RESULTS](../../dmarz/sybil-scale-opus/RESULTS.md), [Sonnet RESULTS](../../dmarz/sybil-scale-sonnet/RESULTS.md).

At N972, visible badges, coverage, attacker pass probability 0.1:

- Haiku: 4 checks 47.2222%, 108 checks 98.6111%, difference +51.3889 points. Saved root-difference bootstrap reproduces interval +38.8889 to +62.5000.
- Sonnet: 47.2222% to 100%, difference +52.7778 points, interval +38.8889 to +66.6667.
- Opus: 0% to 100%, difference +100 points, interval +100 to +100.

Each CSV contains 100 cells with 24 reported valid outcomes per cell, totaling 2,400 per cohort. These are 24 paired roots, not 2,400 independent worlds. Opus minus Sonnet mean cell accuracy is -14.2917 points; Opus minus Haiku -9.5972. Both agree with the published headline.

## Discrepancy: numerical ties counted as wins

The published Opus higher/lower/equal counts are 9/67/24 versus Sonnet and 36/51/13 versus Haiku. Independent subtraction of cell means gives **7/66/27** and **32/51/17**. The published paired-difference CSV explains the discrepancy: mathematically zero paired means are saved as tiny nonzero values and then classified with strict `d > 0` / `d < 0` in `reporting/compare_models.py`.

Three Sonnet comparisons are numerical ties: `(N108, random,12,pass0.9,visible)` is -2.31296e-18; `(N324,random,4,pass0.1,masked)` and `(N324,random,4,pass0.9,masked)` are +4.62593e-18. Four Haiku comparisons are numerical ties: `(N36,coverage,4,pass0.1,visible)`, `(N108,random,4,pass0.1,visible)`, `(N324,coverage,36,pass0.1,visible)`, `(N324,coverage,36,pass0.9,visible)`, all +2.31296e-18 or +4.62593e-18. Exact rows are saved in `scale.opus_minus_*` in the recomputation.

Correction: classify by integer correct-field totals, since every cell has 72 rare-field answers, or use an explicit numerical tolerance. This changes no substantive accuracy effect or direction. Do not count numerical cancellation as a behavioral difference.

## Limits and reporting hygiene

Raw scaling answers and assignments are not present on main at this snapshot. The owner-produced `verification-summary.json` is not an independent audit receipt. Primary intervals can be rederived from saved per-world differences, but their truth scoring and assignment equivalence cannot be independently verified here. Rare wrong/abstention totals likewise remain owner-produced aggregate claims, not independently rescored observations.

Opus README retains an earlier `Results / Not yet collected` section despite a completed RESULTS report. Reconcile that stale navigation text. Opus changes sampling/thinking/output configuration as well as model. Its fewer wrong values and more abstentions cannot be attributed to model identity alone. Ceiling bootstrap intervals do not prove population reliability.
