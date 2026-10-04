# Fixed-resource Sybil splitting: independent saved-answer review

Reviewer `shadow/sol-xcheck`, 2026-10-04. Verdict: checked headline arithmetic passes. Post-hoc review of [sybil-split-opus RESULTS](../../../dmarz/notes/sybil-split-opus/RESULTS.md), not formal hypothesis acceptance. Snapshot and hashes: [README](README.md), [recomputed.json](recomputed.json).

## What was checked

Independently read all 2,688 unique records in `sybil-split-opus/records/s1-episodes.jsonl.gz`. All report completed status. Reconstructed six truth values for each root using the saved generator's documented hash-seeded random construction, without importing its code. Rescored correct, wrong non-null and abstaining rare fields (skills 3,4,5) directly from `answer.values`. **Zero mismatches** with the three saved evaluation metrics over all 2,688 answers. No new calls or replacement observations.

The independent unit is a root: 24 ring roots plus 24 community roots, each observed in 56 conditions. Records have no duplicate root/condition keys. Conditions and repeated packets are not independent samples.

## Recomputed headline

With informative checks, budget 12, k27 minus k1 wrong-answer rates:

- Degree endpoints: 7.6389% to 56.2500%, change +48.6111 points.
- Coverage endpoints: 0% to 7.6389%, change +7.6389 points.
- Random endpoints: 0.6944% to 3.4722%, change +2.7778 points.
- Degree change minus coverage change: **+40.9722 points**, descriptive root bootstrap interval **+27.7778 to +54.8611**, equal weighting of family means. Ring +50.0000, community +31.9444 points. Agrees with +41.0 headline and both rounded family estimates.
- Same interaction at four checks: +50.6944 points.
- With unreliable checks, 12 checks: **-52.7778 points**, showing the reported sign reversal.
- Primary interaction scored on accuracy instead of wrong answers: -20.8333 points.

The root bootstrap reproduces the primary interval using the documented seed/draw count and ring-first family order. Family order changes finite Monte Carlo quantiles slightly without changing the estimand; it is kept explicit in reviewer code.

Repeated-packet audit agrees: 767 root/packet groups were called more than once, 727 had identical saved answers. S1 cost sums to the saved per-episode amount; this is ledger arithmetic, not independent billing verification.

## Interpretation boundary

No material endpoint discrepancy found. The supported result is a narrow synthetic interaction, not a general safety guarantee. Attacker-internal edges are free and change with k; the manipulation includes internal structure as well as resource partition. This review does not independently replay graph construction, admission/check outcomes, fabricated-value specificity or launch provenance. It checks saved answer scoring, complete-record denominator, primary and selected secondary contrasts. A different configuration, graph size or attacker attachment rule remains untested by these records.
