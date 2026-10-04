# Results: when verification amplifies capture (program v5, line T)

Completed 2026-10-04. Exploratory chain 001 at source hash `e24e85f5…` (launch commit `e5f34521`, code commit `d3219ceb`), run queue 270, operator dmarz/fleet-monitor, server sim-dmarz-8. All four stages ran once: S0 216/216 scripted rows, P0 1/1, Q0 23/23, S1 504/504. No call failed, none was re-sent, none went unstarted, and there was no billing pause. Total model cost USD 0.052047 over 528 calls. Same-researcher check only; the run is not independently reviewed. Sanitized records are in [records/](records/); the post-run review is [reviews/chain-001-post.md](reviews/chain-001-post.md).

Every number below was recomputed from the saved rows with the study's own code (`src/analyze.py`, driven by [reporting/build_report.py](reporting/build_report.py); output in [records/report-numbers.json](records/report-numbers.json)). The recomputation regraded all 744 rows and reproduced every stage's totals and saved analysis exactly. `chain.py verify`, run on the server by the launcher, returned exit 0 with every check true in all four stages ([records/verify-summary.json](records/verify-summary.json)).

## Read this first

1. **The primary outcome is computed by the scripted admission, not by the model.** Attacker seats are fixed once the design and the 24 roots are fixed. The model (`qwen/qwen3.7-flash`, reasoning disabled) only answers the admitted packets; its answers are reported further down and cannot change the primary. The 324 identities per graph are scripted, not model agents.
2. **`direct` credit is not safer in level.** The primary measures how attacker seats change with the check budget, not how many there are. Measured attacker seats of 162, mean over the 24 comparison roots:

| Controller passes a check | Rule | 32 checks | 64 checks | 108 checks |
|---|---|---:|---:|---:|
| 10% (strong) | `propagated` | 4.38 (2.7%) | 14.29 (8.8%) | 15.92 (9.8%) |
| 10% (strong) | `direct` | 19.58 (12.1%) | 17.00 (10.5%) | 10.38 (6.4%) |
| 10% (strong) | `anchors` | 21.21 (13.1%) | 16.21 (10.0%) | 5.92 (3.7%) |
| 90% (weak) | `propagated` | 31.00 (19.1%) | 52.88 (32.6%) | 46.42 (28.7%) |
| 90% (weak) | `direct` | 23.79 (14.7%) | 27.96 (17.3%) | 32.62 (20.1%) |
| 90% (weak) | `anchors` | 22.17 (13.7%) | 22.04 (13.6%) | 22.08 (13.6%) |

   Under strong checks at 32 checks `direct` seats more attacker identities than `propagated` in 21 of 24 roots (15.2 more on average, interval 10.6 to 19.6); at 108 checks it seats fewer in 18 of 24, the same number in 3 and more in 3 (5.5 fewer on average, 3.3 to 7.9). Under weak checks `propagated` seats more on average at every budget (7.2, 24.9 and 13.8 more; in 14, 23 and 23 of 24 roots).

## Primary contrast

[attacker seats (`propagated`, 108) − (`propagated`, 32)] − [attacker seats (`direct`, 108) − (`direct`, 32)], controller check pass 0.1, per root.

**+20.75 seats** (95% root-bootstrap interval +17.33 to +24.21; 10,000 draws, seed 20261004; 24 of 24 roots, all positive).

Per root, in root order 9541 to 9564: 15, 19, 21, 12, 31, 32, 17, 33, 28, 22, 31, 26, 13, 13, 12, 14, 17, 9, 17, 29, 13, 8, 28, 38.

Its two parts: from 32 to 108 checks attacker seats rise by 11.54 under `propagated` (9.83 to 13.17; rise in 24 of 24 roots) and fall by 9.21 under `direct` (−12.63 to −5.79; a rise in 3 of 24 roots). The prediction written before the run was positive and of the order of +20 seats (engineering roots: +23.4).

The `propagated` rule on these fresh roots gives attacker seat shares of 2.7%, 8.8% and 9.8% at 32, 64 and 108 checks; the budget study reported 1.98%, 8.51% and 10.70% on its own roots with its own ranking. Same direction; not a paired replication.

## Other admission strata (scripted, prespecified, descriptive, no multiplicity correction)

- Same contrast with `anchors` in place of `direct`: +26.83 (23.54 to 30.25), 24 of 24 roots positive. Under `anchors` seats fall by 15.29 from 32 to 108 checks (no root rises).
- `direct` against `anchors`: +6.08 (5.33 to 6.92).
- At 64 instead of 108 checks: +12.50 (10.33 to 14.67).
- Under weak checks: +6.58 (1.75 to 11.13), positive in 15 of 24 roots. There both rules escalate: `propagated` +15.42 (10.67 to 20.04), `direct` +8.83 (6.71 to 11.13); `anchors` −0.08.
- Honest-specialist retention (share of the 81 honest specialists seated), strong checks, at 32, 64, 108 checks: `propagated` 0.34, 0.65, 0.78; `direct` 0.30, 0.34, 0.39; `anchors` 0.28, 0.29, 0.32. Weak checks: `propagated` 0.38, 0.65, 0.55; `direct` 0.29, 0.35, 0.40; `anchors` 0.27 at every budget.
- Truth availability (rare skills with at least one true report seated) is 1.00 in every cell except one (`direct`, weak checks, 32 checks: 0.99). It is at its ceiling and does not discriminate.
- Truth plurality (rare skills where true reports outnumber fabricated ones), strong checks: `propagated` 1.00 at every budget; `direct` 0.78, 0.94, 0.96; `anchors` 0.32, 0.82, 0.99. Weak checks: `propagated` 0.42, 0.51, 0.35; `direct` 0.32, 0.40, 0.43; `anchors` 0.08, 0.18, 0.25.

## Model answers per cell

Rare-skill answers of `qwen/qwen3.7-flash` on the admitted packets, 24 calls per cell, all valid. Correct / wrong / abstained, in percent of the 72 rare-skill fields of a cell; "reference" is the plurality rule on the same packets.

| Controller pass | Rule | Checks | Model correct / wrong / abstained | Reference correct / wrong / abstained | Model minus reference, correct |
|---|---|---:|---|---|---:|
| 10% | propagated | 32 | 97.2 / 1.4 / 1.4 | 100.0 / 0.0 / 0.0 | −2.8 |
| 10% | propagated | 64 | 98.6 / 1.4 / 0.0 | 100.0 / 0.0 / 0.0 | −1.4 |
| 10% | propagated | 108 | 98.6 / 1.4 / 0.0 | 100.0 / 0.0 / 0.0 | −1.4 |
| 10% | direct | 32 | 61.1 / 34.7 / 4.2 | 77.8 / 6.9 / 15.3 | −16.7 |
| 10% | direct | 64 | 91.7 / 8.3 / 0.0 | 94.4 / 0.0 / 5.6 | −2.8 |
| 10% | direct | 108 | 95.8 / 4.2 / 0.0 | 95.8 / 0.0 / 4.2 | 0.0 |
| 10% | anchors | 32 | 40.3 / 48.6 / 11.1 | 31.9 / 9.7 / 58.3 | +8.3 |
| 10% | anchors | 64 | 66.7 / 26.4 / 6.9 | 81.9 / 2.8 / 15.3 | −15.3 |
| 10% | anchors | 108 | 95.8 / 1.4 / 2.8 | 98.6 / 0.0 / 1.4 | −2.8 |
| 90% | propagated | 32 | 48.6 / 51.4 / 0.0 | 41.7 / 47.2 / 11.1 | +6.9 |
| 90% | propagated | 64 | 38.9 / 61.1 / 0.0 | 51.4 / 44.4 / 4.2 | −12.5 |
| 90% | propagated | 108 | 36.1 / 63.9 / 0.0 | 34.7 / 54.2 / 11.1 | +1.4 |
| 90% | direct | 32 | 40.3 / 52.8 / 6.9 | 31.9 / 43.1 / 25.0 | +8.3 |
| 90% | direct | 64 | 44.4 / 55.6 / 0.0 | 40.3 / 37.5 / 22.2 | +4.2 |
| 90% | direct | 108 | 45.8 / 54.2 / 0.0 | 43.1 / 45.8 / 11.1 | +2.8 |
| 90% | anchors | 32 | 38.9 / 55.6 / 5.6 | 8.3 / 11.1 / 80.6 | +30.6 |
| 90% | anchors | 64 | 45.8 / 47.2 / 6.9 | 18.1 / 25.0 / 56.9 | +27.8 |
| 90% | anchors | 108 | 34.7 / 56.9 / 8.3 | 25.0 / 22.2 / 52.8 | +9.7 |

- Every wrong rare-skill answer of the model, in every cell, equals the fabricated value (share 1.00).
- Pooled over the 432 attacked calls: model 62.2% correct, 34.8% wrong, 3.0% abstained; reference 59.7%, 19.4%, 20.8%. The model abstains far less than the plurality rule, which returns null on a tie.
- `propagated` minus `direct` in rare-skill correctness, paired by root (complete for all 24 roots, so bounds equal the estimate): strong checks +36.1 points at 32 checks (22.2 to 51.4), +6.9 at 64 (1.4 to 13.9), +2.8 at 108 (0.0 to 6.9); weak checks +8.3 (−5.6 to 23.6), −5.6 (−23.6 to 12.5), −9.7 (−25.0 to 5.6).
- **Clean endpoints** (108 checks, the weak-check audit and admission, every controller report truthful): 100% correct under all three rules, 72 of 72 calls, equal to the reference. The same admitted sets with fabricated reports give 36.1%, 45.8% and 34.7% correct.
- Qualification (P0 and Q0, 24 clean fixtures): 24 of 24 valid and exactly right; `full` 8 of 8, `sparse` 8 of 8, `missing` 8 of 8 null on the withheld fact.
- Repeated packets: 5 packets occur twice within a root (10 calls); the two answers are identical in 3 of the 5.

Full per-cell table: [records/s1-cells.csv](records/s1-cells.csv).

## Dangling-rule audit, as measured

Computed offline from the frozen audits (no model involved). On the 24 comparison roots, 34 of 144 snapshots contain an identity whose neighbours have all failed. The `propagated` admitted set equals the budget study's ranking in 134 of 144 snapshots, including all 110 without such an identity; in the other 10 it differs by 3 to 14 of 162 seats, and the attacker seat count differs by at most 1. Mean attacker seats under strong checks, earlier ranking against `propagated`: 4.38 and 4.38 at 32 checks, 14.29 and 14.29 at 64, 16.00 and 15.92 at 108. On the engineering roots the figures were 12 of 48 snapshots, 42 of 48 equal, at most 1 seat.

## Interface and resources

Probe (P0), as the provider returned it: response model `qwen/qwen3.7-flash`, provider `Alibaba`, finish reason `stop`, reasoning tokens 0, 3,072 input and 57 output tokens for a 5,938-byte request (0.517 tokens per byte), latency 1.31 s, provider-reported cost USD 0.00009957, equal to the snapshot-price computation.

Over all 528 paid calls: every response named the model `qwen/qwen3.7-flash` and the provider `Alibaba`, ended with `stop`, reported 0 reasoning tokens and took one HTTP attempt. Input 3,033 to 3,101 tokens per call (0.514 to 0.520 tokens per byte), output 30 to 65 tokens. Latency median 1.21 s, 95th percentile 1.47 s, maximum 2.65 s. The provider reported a cost on every call: equal to the snapshot-price computation on 523 calls and lower on 5 (down to 30% of it), never higher. The cause of the 5 lower costs was not determined.

| Stage | Hub run | Rows | Calls | Input tokens | Output tokens | Cost (USD) | Worker time | Hub start to end (UTC) |
|---|---|---:|---:|---:|---:|---:|---:|---|
| S0 | 81f7ffe1 | 216 | 0 | 0 | 0 | 0 | 22.8 s | 11:33:18 to 11:33:45 |
| P0 | 135ea6a1 | 1 | 1 | 3,072 | 57 | 0.000100 | 2.6 s | 11:33:45 to 11:33:49 |
| Q0 | f65a2ee6 | 23 | 23 | 70,907 | 1,335 | 0.002298 | 14.5 s | 11:33:49 to 11:34:05 |
| S1 | d9c433dd | 504 | 504 | 1,546,045 | 27,817 | 0.049649 | 213.8 s | 11:34:05 to 11:37:39 |
| Total | | 744 | 528 | 1,620,024 | 29,209 | 0.052047 | | chain 11:33:17 to 11:37:39 |

The pre-run estimate was about USD 0.045 to 0.05 and 6 to 13 minutes for S1; actual USD 0.0496 and 3.6 minutes. Ledger at the end: 528 calls, 528 transport attempts, 0 voided, USD 0.052047 settled against the USD 2 cap.

## Interpretation and limits

Interpretation, kept apart from the measurements above.

Supported, for this simulator and these 24 roots: with the audit held fixed, the rise in attacker seats between 32 and 108 coverage checks under strong checking appears when the credit of a passed check is propagated to neighbours and does not appear when it is placed on the passed identity alone or not placed at all. That is what the candidate mechanism of the budget study predicts. Because the outcome is scripted, this is a property of the admission rules on this graph family, not a finding about model behaviour.

Not supported: that `direct` credit is the safer rule. At 32 checks under strong checking it seats more than four times as many attacker identities as `propagated` (19.6 against 4.4), and the model's rare-skill answers are then much worse (61.1% against 97.2% correct). At 108 checks it seats fewer (10.4 against 15.9) with about the same answer quality (95.8% against 98.6%). Under weak checks `propagated` seats more attacker identities on average at every budget and answer quality is low under every rule (35% to 49% correct), with no distinguishable difference between `propagated` and `direct`.

Also measured: under strong checks, more attacker seats under `propagated` at 108 checks did not come with worse answers, which matches the budget study's observation that accuracy and attacker seat share rose together. The clean endpoints show that the wrong answers under weak checks come from the fabricated reports, not from which identities were seated: with the same seats and truthful reports the model is right every time.

Suspected, not checked by a discriminating test: `propagated` credit at small budgets lifts honest specialists near passed identities into the seats that, under `direct` and `anchors`, go to outside identities near the bridges, the controller's among them.

Limits: scripted identities, graph and checks; one graph family, one audit policy (coverage), one fabrication type (+7), one population size; `direct` and `anchors` are counterfactual rules written for this study, not published defenses; one model configuration with one call per cell; 24 development-sized roots; secondary intervals without multiplicity correction; the dangling rule differs from the earlier implementation as audited above. No confirmatory claim is made. The run is not independently reviewed.
