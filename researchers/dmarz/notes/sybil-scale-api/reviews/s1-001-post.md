# Post-mortem: s1-001

Experiment sybil-scale-api / dmarz/sybil-specialists / exploratory S1 / 2026-10-04. Parent q0-001; [pre-run review](s1-001-pre.md). Run sybil-scale-api/56defc84; revision 722bfc3308affc75ab34d360bae6aca36b50acb5; runtime 134fd9552ee8bf45777cb751b4104465a7bfd079eb33bc27f1c226c8a6f4b322. Model claude-haiku-4-5-20251001. **Disposition: complete-valid-result.** No formal S2 advancement.

## What ran and what happened

2,400 planned → 2,400 started → 2,400 terminal → 2,400 graded → 2,400 analyzed; zero failures, missing outcomes, duplicates or retries. Every one of 100 cells contains 24 worlds. Preparation plus collection took 1,151.92 seconds; rendering and publication brought start-to-done to approximately 20 minutes. S1 used 18,296,288 input and 99,128 output tokens, USD 18.791928. Q0 adds USD 0.661997, for USD 19.453925 total. All 2,464 calls have returned usage; conservative reservation USD 68.300028 remains distinguished from cost. No reporting errors were recorded.

The primary strong-check, visible-badge coverage contrast at 972 identities is +51.4 percentage points for proportional versus four checks (descriptive paired-world 95% interval +38.9 to +62.5). Attacker seat share falls 7.9 points. Under weak checks the corresponding accuracy gain is +6.9 points (−5.6 to +19.4), while attacker seat share rises 10.0 points. Equal-budget random checking ties coverage's largest-world strong-check accuracy at 98.6%; no uniquely superior coverage defense was demonstrated. Large-world proportional coverage badges have small, unresolved effects. Full secondary findings, all denominators and caveats are in [RESULTS.md](../RESULTS.md) and the aggregate tables.

The nine regression tests, 264-case scripted fleet S0 and 64/64 exact API Q0 passed before escalation. Model clean competence remains separate from security effectiveness. Every S1 packet hash, model evaluation and scripted baseline was independently recomputed from recorded assignments; the entire frozen analysis matched using Python 3.12 and pinned dependencies. No data exclusions or protocol changes followed result inspection.

## Visualization review

Mapping v1 delivered initial, progress, final and hidden-badge 1800×1200 images, plus a 33-frame measured-prefix replay. Across S0/Q0/S1, 30 uploaded artifact checksums passed and all 99 GIF frames decoded. Final-first artifact ordering was normalized using the same image bytes. The browser displayed the completed run, final chart and replay; the earlier Cloudflare 1010/403 access problem resolved without any security-setting change. Local figures were independently regenerated and inspected: labels and panels are legible, every final cell has 24 observations, costs and counts agree with the source records.

The replay samples completion order at 33 prefixes and is not a physical-time simulation of identity interactions. Early prefixes contain unequal cell counts and should not be read as treatment trajectories. Fixed axes are shared across conditions. The main figure shows means; uncertainty is provided in the paired contrasts and full cell tables. The footer uses “shared observations” for budget duplicates; separate reliability-label actor draws remain as specified in the plan.

Two display details should be clearer in a future runtime: progress updates inherited the last preparation message even after calls started, and the generic S1 qualification_passed metric is 0 because S1 has no qualification subtest. Neither denotes failed qualification: Q0 passed and the exact-runtime gate was enforced. The S1 status, counts, final message and figures correctly report completion. Do not rerun paid data to repair these labels.

## Experiment-quality assessment

This meaningfully tests the requested population/budget scaling question under a disclosed fixed graph family. The 24 worlds are the replication units, not calls or identities. The post-collection selection audit explains the coverage allocation change: four checks all target outside identities at 36, but all target core identities at the larger sizes. This diagnostic uses retained data and is labelled post-collection; it is not a new preregistered endpoint.

Evidence supports proportional informative checking in this fixture, not arbitrary Sybil resistance, equal-cost superiority over random, or autonomous-agent scaling. Even the high-accuracy condition rejects most honest specialists. The +7 attack, repeated six-fact task, growing attacker resources, fixed two trusted seeds and changing graph distances limit generalization. Badges are not established as an effective defense. A clean successful run can yield a negative result for the proposed policy's unique advantage; no favorable-result rerun is justified.

## Failure and repair ledger

| Kind | Evidence | Cause / repair | Acceptance | Status |
|---|---|---|---|---|
| Paid execution | 2,400 valid once; zero failed/not-started | No repair needed | Ledger, assignments and outcomes reconciled | Closed |
| Local numeric reproduction | 302 last-bit float differences, maximum 3.33e−16, under Python 3.9/NumPy 2.0.2 | Use Python 3.12 and pinned packages, matching server arithmetic | Full analysis exactly matches; all individual evaluations already matched | Closed; no data change |
| Public visual access | Earlier old/new image routes returned 403/1010 | No access-control change; later browser access succeeded | Completed run and final image visible; replay loaded | Closed |
| Shared artifact bookkeeping | A transient main revision contained unrelated invalid author fields and an unreferenced artifact | Preserved others' files and pulled their subsequent corrections | Project-wide strict check returned 0 errors before filing new figures | Closed |
| Display labels | Stale preparation message while running; S1 qualification field 0/not-applicable | Documented interpretation; defer clearer stage-specific labels to a future runtime | Correct completed status, prior qualification and final counts verified | Non-blocking follow-up |

## Next run

The completed result needs no scientific repair. A separately planned follow-up should compare coverage and random at equal intermediate checking budgets, vary verifier discrimination, balance positive/negative fabrication, and make specialist facts less redundant. A fixed-attacker-resource arm would distinguish population growth from identity amplification. Use disjoint worlds and fresh per-size clean qualification if prompts/task change; preserve this runtime and all prior attempts. No successor is launched here. S2 and holdout 10000–19999 remain closed. Host release follows the completed upload and worker-exit checks in [DEPLOYMENT.md](../DEPLOYMENT.md).
