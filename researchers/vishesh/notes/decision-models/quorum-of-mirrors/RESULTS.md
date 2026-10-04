# Quorum of Mirrors: first native qualification

**S0 passed its predeclared competence screen: 29/32 correct MAP choices, 32/32 valid responses.** This is evidence-reading qualification for the future swarm experiment, not evidence that source-aware swarms improve decisions.

| Measure | Observed |
|---|---|
| Correct evidence-based MAP choice | 29/32 (90.625%) |
| Incorrect choice / DEFER | 2 / 1 |
| Provider failures / unstarted | 0 / 0 |
| Identical-request agreement | 14/16 pairs |
| Weakest answer-by-reliability cell | 6/8, matching its acceptance floor |
| Actual API cost | $0.00103152 |
| Conservative reservations retained | $0.043008 |

The useful warning is that explicit source IDs and instructions did not eliminate errors, and identical inputs produced different choices in two pairs. These are candidates for the next controlled comparison, not a demonstrated copying mechanism. Sixteen synthetic evidence patterns, each called twice, do not establish general model reliability.

- [Full post-mortem](reviews/S0-02-post.md)
- [Observed matrix](results/QM-S0-02/matrix.html) and [CSV](results/QM-S0-02/matrix.csv)
- [All-assigned summary](results/QM-S0-02/summary.json), [response journal](results/QM-S0-02/receipts.jsonl), [audit](results/QM-S0-02/audit.json)
- [Prospective attempt plan](reviews/S0-02-pre.md) and [verified registration receipt](results/QM-S0-02/public-plan-receipt.json)
- [Preserved zero-call setup failure](reviews/S0-01-post.md)

The missing-output-directory defect was repaired before attempt 2, with no changes to evidence or scoring. All 27 offline checks passed on the allocated host. The approved budget was separate from other studies. No new VM was provisioned; the existing idle host was allocated exclusively. Credentials stayed in the local relay, which was stopped after completion.

Next scientific step: a separately frozen, paired S1 comparison of repetition and ancestry visibility. No S1 or confirmatory outcome is claimed here.
