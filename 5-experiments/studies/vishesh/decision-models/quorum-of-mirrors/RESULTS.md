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

The useful warning is that explicit source IDs and instructions did not eliminate errors, and identical inputs produced different choices in two pairs. These are candidates for the next controlled comparison, not a demonstrated copying mechanism. Eight bit triples reused at two reliability settings (16 configurations), each called twice, do not establish general model reliability.

- [Full post-mortem](reviews/S0-02-post.md)
- [Observed matrix](results/QM-S0-02/matrix.html) and [CSV](results/QM-S0-02/matrix.csv)
- [All-assigned summary](results/QM-S0-02/summary.json), [response journal](results/QM-S0-02/receipts.jsonl), [audit](results/QM-S0-02/audit.json)
- [Prospective attempt plan](reviews/S0-02-pre.md) and [verified registration receipt](results/QM-S0-02/public-plan-receipt.json)
- [Preserved zero-call setup failure](reviews/S0-01-post.md)

The missing-output-directory defect was repaired before attempt 2, with no changes to evidence or scoring. All 27 offline checks passed on the allocated host. The approved budget was separate from other studies. No new VM was provisioned; the existing idle host was allocated exclusively. Credentials stayed in the local relay, which was stopped after completion.

Next scientific step: a separately frozen, paired S1 comparison of repetition and ancestry visibility. No S1 or confirmatory outcome is claimed here.

## Iteration 3: retrospective decision references, 2026-10-04

The [analysis plan](ITERATION-3.md) was written before the reanalysis code, after S0 outcomes were known. These comparisons were **not preregistered S0 endpoints**. No new model requests, exclusions or edits to raw observations occurred. [Independent arithmetic](reassess_s0.py) does not import the original scorer; it checks request hashes, all 32 unique receipts, repeated-input identity, report/root consistency, model identity and frozen labels. [Computed data and input hashes](analysis/iteration-3/comparisons.json) support the [all-case explorer](analysis/iteration-3/cases.html).

| Method | Exact-MAP correct / 32 saved call slots | Interpretation |
|---|---:|---|
| Model with full lineage and source instructions | 29 | Measured |
| Majority of nine reports | 24 | Computed misspecified reference |
| Majority of three unique roots | 32 | Computed exact rule for this grammar |

Replacing the observed model choice with the root rule corrects three slots and spoils none. Replacing report counting with root counting corrects eight slots. These are deterministic paired recalculations, not measured causal effects of a prompt or discussion.

The input-defined agreement subset contains 12 configurations / 24 calls, all model-correct. The conflict subset contains four configurations / eight calls, five correct, two wrong and one DEFER. Non-correct IDs: `q65-011-r1`, `q65-011-r2`, `q80-100-r2`. Repeated requests agreed in 14/16 pairs. There are eight distinct bit triples, not 32 independent worlds; no population interval is justified here.

**Practical consequence:** when provenance is complete and trustworthy and all sources have equal known reliability, a three-root majority is simpler and more reliable on these saved inputs than this native reader. The next study must justify any added model/committee complexity against that baseline. Partial provenance and semantic ancestry are unresolved, so this result does not establish a general-purpose misinformation defense.

## Evaluation against the plan

S0 met the frozen thresholds: validity 32/32 versus minimum 31; MAP correctness 29/32 versus minimum 28; weakest label-by-q cell 6/8 versus minimum 6. Repeat disagreement was retained, not rerun away. The first attempt failed before any call because its output parent directory was absent; the repair and failed-attempt record remain intact. No swarm efficacy endpoint was scheduled or measured in S0.

The current documentation defect—obsolete “no dispatcher/no approved budget” statements beside completed results—is repaired in the overview. The new setup runbook closes the earlier exploratory exemption prospectively. Historical S0 execution evidence is preserved separately from current process admission. S1 has no executed assignments or results; [its plan](S1-PLAN.md) corrects the missing native comparator and [SETUP.md](SETUP.md) records unresolved research/review and deployment gates.
