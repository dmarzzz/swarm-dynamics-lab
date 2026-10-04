# Sybil verification budget: independent saved-answer review

Reviewer `shadow/sol-xcheck`, 2026-10-04. Verdict: checked headline arithmetic passes. Post-hoc audit of [RESULTS](../../../dmarz/notes/sybil-budget-api/RESULTS.md) and the completed-finding summary in `latest-results-review-2026-10-04/evidence.json`. Snapshot and input hashes: [README](README.md), [recomputed.json](recomputed.json).

Read `sybil-budget-api/records/s1-001-episodes.jsonl.gz`: 2,880 unique saved records, all completed, 120 cells of 24 roots. Reconstructed synthetic truth directly from SHA256-seeded random values and compared saved `answer.values` to true values, without importing the study scorer. **Zero rare-accuracy mismatches across 2,880 answers.** Admission metrics below are read from saved evaluations, not independently reconstructed.

## Headline recomputation

Exactly **7 of 120** observed cells satisfy mean specialist accuracy at least 0.90 and mean attacker seat share at most 0.05; all use attacker check-pass probability 0.1:

- N324: coverage32; random32, random64, random108.
- N972: coverage108; random64, random108.

At N324 with coverage and strong checks, increasing checks from 32 to 108 raises independently rescored accuracy **97.2222% to 100%**, while saved attacker seat share rises **1.98045% to 10.69959%**. This reproduces the reported 97.2 to 100 and 1.98 to 10.70 figures. More checks are not monotonically safer under this metric.

## Limits

No material discrepancy found. These are exploratory point-mean targets over a large grid, not reliability guarantees or multiplicity-adjusted policy certification. Twenty-four world roots are the independent units, not 2,880 calls. Reused redundant synthetic facts and independent check construction limit external validity. The reviewer did not reconstruct seat allocation, audit provider billing or retrospectively certify immutable registration. The separate Sonnet replication is not pooled or reviewed here.
