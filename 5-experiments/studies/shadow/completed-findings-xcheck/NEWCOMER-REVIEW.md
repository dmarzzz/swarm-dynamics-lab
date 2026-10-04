# Sybil newcomers: independent saved-answer review

Reviewer `shadow/sol-xcheck`, 2026-10-04. Verdict: checked headline arithmetic passes. Post-hoc audit of [Sonnet RESULTS](../../../dmarz/notes/sybil-newcomer-sonnet/RESULTS.md). Snapshot and hashes: [README](README.md), [recomputed.json](recomputed.json).

Read `sybil-newcomer-sonnet/records/s1-001-episodes.jsonl.gz`: 1,944 unique records, all completed. Independently reconstructed each round's truth by replaying the documented hash-seeded random number stream through the recorded round, without importing the study's scorer. Compared saved rare answer values with truth. **Zero specialist-accuracy mismatches across all 1,944 outcomes.**

At round eight, sixteen controller identities, sleeper strategy, 24 paired roots:

- Random checking: **25.0000%** specialist accuracy.
- Renewal: **19.4444%**.
- Reputation: **8.3333%**.
- Renewal minus reputation: **+11.1111 percentage points**. The 10,000-resample root bootstrap interval is numerically -4.6e-16 to +22.2222 points, substantively **zero to +22.22**. It touches zero, as reported; numerical negative zero is not evidence of a negative effect.

No material arithmetic discrepancy found in the selected completed headline. The independent sample is 24 world roots; the 1,944 model outputs are repeated measurements. This audit does not independently rebuild audit selection, truth-present diagnostics, retention, cross-model assignment equivalence or every identity-splitting secondary contrast. The stated newcomer admission-bottleneck explanation remains interpretation, not an independently isolated causal mechanism. Do not infer a conclusive identity-splitting amplification from this study's policy comparison.
