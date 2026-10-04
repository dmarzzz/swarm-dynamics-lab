# Independent completed-findings arithmetic review

Reviewer: `shadow/sol-xcheck`, 2026-10-04. Post-hoc saved-data audit, no model calls, no new scientific observations. Source snapshot: [`d28e538cb367a440bd3ad40927e8da82b7041352`](https://github.com/dmarzzz/swarm-lab/tree/d28e538cb367a440bd3ad40927e8da82b7041352). All actual input hashes are in [recomputed.json](recomputed.json). Later source edits are not covered by this snapshot.

## Findings

- [Sybil scaling review](SCALE-REVIEW.md): primary effects agree, including Opus +100.0 percentage points. **A small reporting defect needs correction:** floating-point cancellation turns exact cell-mean ties into reported wins/losses. Correct Opus higher/lower/equal counts are 7/66/27 against Sonnet and 32/51/17 against Haiku, not 9/67/24 and 36/51/13. Mean differences remain -14.29 and -9.60 points. Only aggregate outputs and saved primary differences were available on main; this is not independent raw-answer verification of scaling.
- [Fixed-resource Sybil splitting review](SPLIT-REVIEW.md): 2,688 saved answers independently scored, zero mismatches. Primary +40.97 points, descriptive interval +27.78 to +54.86, agrees. Weak checks reverse the interaction to -52.78 points.
- [Verification-budget review](BUDGET-REVIEW.md): 2,880 saved answers independently scored, zero accuracy mismatches. Exactly 7/120 cells satisfy the descriptive joint point-mean target. Coverage at N324 raises accuracy while worsening attacker admission.
- [Newcomer review](NEWCOMER-REVIEW.md): 1,944 saved answers independently scored, zero accuracy mismatches. Round-eight policy accuracies 25.00%, 19.44%, 8.33%; renewal minus reputation +11.11 points with an interval touching zero.
- [Market-splitting review](MARKET-REVIEW.md): all 36 episodes / 864 frames independently checked for concentration, three-round evasion and accumulated profit. Zero endpoint mismatches. Firm regulation 6/6 registrations and evasions, owner and none 0/6; ratio-of-means profit gain 15.8906%.

The raw Sybil scoring checks cover 7,512 recorded answers, not 7,512 independent worlds. Saved admission metrics, model identity, provider spending and historical pre-registration receipts are not independently attested by recomputing endpoint arithmetic.

## Reproduce

From repository root, with Python and NumPy installed:

```sh
nice -n 10 python3 5-experiments/studies/shadow/completed-findings-xcheck/recompute.py
python3 scripts/lab.py check
```

[recompute.py](recompute.py) imports no study implementation. It reconstructs synthetic truth from documented SHA256-seeded random construction, scores saved answer values directly, builds root-paired contrasts, and reconstructs market HHI from firms' saved quantities. Bootstrap uses 10,000 root resamples, seed 20261004; split resamples within each graph family, with ring first to reproduce the published PRNG draw allocation. These are descriptive intervals, not generalization or simultaneous confidence guarantees.

Reviews live in reviewer-owned notes because these exploratory notes studies have no formal `experiments/<id>/README.md` targets accepted by `lab.py`'s `reviews/` schema. No formal hypothesis acceptance or research-gate approval is asserted. The task is [review-dmarz-completed-xcheck](../../../../lab/tasks/review-dmarz-completed-xcheck.md).
