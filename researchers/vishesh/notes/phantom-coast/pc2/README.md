# Phantom Coast PC-2: repeated inspections waste the budget

Native qualification and pilot completed on 2026-10-04 UTC. The dominant observed failure was repeated inspection: under misleading reports without an audit, the three-proposal team visited **2.5 distinct cells in twelve slots**, versus **12 for uniform acquisition**. Every directly inspected cell was mapped correctly across all 96 episodes. The weakness was acquiring useful new evidence.

[Public experiment](https://swarm-live.pages.dev/#/x/phantom-coast-pc2) · [Measured replay, all 624 frames](https://swarm-live.pages.dev/api/a/phantom-coast-pc2/s1-a1/replay-public.gif) · [Final frame](https://swarm-live.pages.dev/api/a/phantom-coast-pc2/s1-a1/final_frame.png) · [Prospective plan](PLAN.md) · [Post-mortem](reviews/S1-A1-POST.md) · [Analysis JSON](results/S1-A1-analysis.json) · [Saved-data audit](results/S1-A1-audit.json)

## What ran

Eight independent generated roots, four block and four scattered, crossed with team/single/uniform policy, misleading/benign inherited reports and source-audit on/off: **96 dependent episodes and 1,792 assigned native requests**. All episodes completed twelve slots. 1,791 responses were valid; one team proposal was invalid and retained. Its remaining two valid proposals satisfied the predeclared quorum, so no sensing slot failed. A separate four-root qualification passed all 24 requests, 432 map labels and twelve unique-unmeasured-cell choices. PC-1 is a separate cohort and is not pooled into these effect estimates.

The instrument was frozen at `6b357eb5b7be8b9b789843116ff4e44043415988`, TypeSafe `typesafe/jev-1.13-20260917`, without fallback or model retries. Forty-four offline checks passed on the allocated Linux host. The immutable public plan, prospective assessments, current exclusive allocation and cumulative spending receipts preceded dispatch. Researcher review was not required by owner direction. No independent review is claimed.

## Acquisition and endpoint results

Means across the same eight roots, **misleading report, audit off**. Error percentages use 288 assigned cells per condition across eight dependent maps. Upper error counts both wrong and unresolved labels; it is a conservative risk criterion, not observed misclassification.

| Policy | Distinct cells /12 slots | Repeated slots | Reported cells remeasured /4 | Known wrong | Upper error |
|---|---:|---:|---:|---:|---:|
| Team | 2.50 | 9.50 | 2.50 | 4.17% | 92.71% |
| Single | 3.25 | 8.75 | 2.38 | 4.51% | 90.63% |
| Uniform | 12.00 | 0.00 | 1.88 | 2.43% | 66.67% |

Team coverage under benign reports was also low: 4.00 distinct cells and eight repeats. Misleading reports reduced team visits to distinct reported cells by 0.625 on average relative to benign reports; the single-policy reduction was 1.125, while uniform acquisition was unchanged. Nevertheless, the misleading team spent all of its distinct inspections inside the reported region on average. These observations support a narrow pattern of inefficient, repetitive acquisition; they do not establish broad avoidance of the reported region.

The prespecified primary interaction in **upper error** was **+2.43 percentage points**: team misleading-minus-benign, less the same uniform contrast. It was +6.25 points for block roots and −1.39 for scattered roots. The paired missing-label interval was [−148.96, +153.13] percentage points on this difference-of-differences scale; this is an identification bound, not a confidence interval. True error remains poorly identified because many labels are UNKNOWN. A labelled post-run sensitivity check omitting root 506 changes the point interaction to −0.40 points. The primary result retains all eight roots; the sign is fragile.

The fresh yoked judge exactly matched the team's aggregate upper error in each condition. Native endpoints also closely matched deterministic reconstruction from the acquired evidence. Uniform benign endpoints were slightly more unresolved than the deterministic reader. Full observed/unobserved and LAND/WATER error strata, first report visits with censoring, observation overlap, per-root contrasts and audit coverage gains are in the analysis JSON. There were **zero wrong or unresolved labels among directly inspected cells** in all conditions.

## Was the source audit worth a slot?

| Policy, misleading report | Audit-off upper error | Audit-on upper error | Change | Distinct-cell gain |
|---|---:|---:|---:|---:|
| Team | 92.71% | 89.58% | −3.13 points | +1.25 |
| Single | 90.63% | 88.19% | −2.43 points | +1.00 |
| Uniform | 66.67% | 67.36% | +0.69 points | −0.25 |

No policy/report condition met the predeclared mean improvement threshold of 2/36 = 5.56 percentage points. The team audit reduced seven known errors and two unresolved labels across its 288 cells, but its mean benefit remained below that threshold. Auditing displaced useful coverage for uniform acquisition. A different cost for confidently wrong versus unresolved labels could change the decision; that would be a new utility analysis, not this run's frozen criterion.

## Cost, integrity and delivery

| Policy | Native calls | Valid | Input tokens on valid responses | Known S1 cost |
|---|---:|---:|---:|---:|
| Team, including yoked endpoint checks | 1,280 | 1,279 | 3,039,539 | $0.127660638 |
| Single | 416 | 416 | 940,045 | $0.039481890 |
| Uniform | 96 | 96 | 514,560 | $0.021611520 |

Compute is intentionally unequal; these are instrument costs, not a deployment-cost equivalence. S1 known spend was $0.188754048. Q0 added $0.005229966 and PC-1 had spent $0.162723246. **Cumulative known API spend is $0.356707260; conservative exposure is $0.358051260**, including the invalid response's $0.001344 reservation. Its exact charge is unresolved. The original $5 total authority, with a $4 API envelope, was never reset. No new machine or incremental infrastructure charge was needed.

The operator audit reconstructed all **1,792 wire inputs, 1,152 acquisition events and 96 endpoints**, verified request hashes and recomputed every primary contrast. All ten original S1 artifacts matched authenticated hub readback. The original 13.9 MB GIF returned public 404; a 7.1 MB shared-palette encoding preserves all 624 frames, dimensions, order and durations and passes public byte verification. The original remains retained. The final PNG also passes public verification. An offline interactive replay, built by `reporting/build_replay.py`, supports world/policy/audit/slot controls and was checked in a browser against native values. These are saved measured events, not live model animation.

The worker stopped, the temporary approved OpenRouter credential was removed, the ledger was backed up, and the exclusive allocation was released. [Closeout receipt](results/CLOSEOUT.json). One zero-call credential-staging failure preceded Q0 and remains documented in its post-mortem; it did not consume a scientific sample or reset spending.

## Decision and next iteration

For this small synthetic cohort, use uniform coverage as the operational baseline. Adding three-proposal coordination did not produce useful inspection coverage. The targeted audit showed a modest benefit under misleading learned-policy conditions, below the chosen practical threshold.

A future, separately preregistered iteration should compare a coverage guard against the existing policies on fresh roots, strengthen strategic qualification without conditioning on a favorable treatment effect, and specify a practical wrong-versus-unknown loss. Profile the recorder before scaling: the first-to-last request window was about 54 minutes, while recorded per-call intervals summed to about six minutes; substantial time occurred outside those intervals. Retain safe, bounded validation reason codes so an invalid response can be diagnosed without logging provider bodies or credentials. None of these proposed changes was applied to the completed cohort, and no confirmation run was started.
