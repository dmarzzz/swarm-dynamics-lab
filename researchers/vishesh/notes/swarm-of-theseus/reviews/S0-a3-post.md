# Post-mortem: S0-a3

- Owner: vishesh/codex-theseus; S0, 2026-10-04 UTC; parent S0-a2; source fcee9c26074ec72dfa262ae750812828b983421b.
- Disposition: repair-and-rerun. Execution complete, qualification failed, culture contrast untested.

## What ran and what happened

12 planned, started, terminal, graded and analyzed; zero failures or missing outcomes; all 72 frames preserved. 288 model calls, 213,939 input tokens, 48,499 output tokens, estimated usage USD 0.456434. Cumulative quota reservation after S0-a2/a3 USD 3.781728 for 545 calls, distinct from USD 0.917261 estimated usage.

Verbatim controls: seed bank and repair dock both 1.0 accuracy and 1.0 receipt retention. Observatory accuracy 0.75 (worlds 1.0 and 0.5), convention 1.0. The original 0.85 accuracy gate therefore fails. Retained founders show convention loss even without replacement (seed bank 0.5, observatory 0, repair dock 0.3333), a potentially useful memory-scaffold observation, not yet a turnover effect.

## Visualization review

72/72 frames, per-world PNGs and replay HTML retained/uploaded. Source-ID roster and step scores can be recomputed from raw events. Prior attempt playback was verified through initial state, advancing cursor and missing-step display. Per-run immutable URLs are pinned through report metadata so experiment-level plan updates cannot rewrite their provenance.

## Experiment-quality assessment

Response-contract repair eliminated recorded execution failures and improved convention correctness in verbatim arms, but before/after values are from disjoint small worlds, not a randomized estimate of repair effect. In a failing observatory response, the work evidence list was [0,1,0] while the three unique roots had signals [0,1,1]; some report positions were substituted for root identities. Exact selection cause is inferred from that trace, not proven by intervention. Scoring the final label remains appropriate; explanations cannot redeem an incorrect action.

## Failure and repair ledger

| ID | Finding | Response | Acceptance | Status |
|---|---|---|---|---|
| CONTRACT-1 | all verbatim receipt means now 1.0 | preserve explicit field semantics | same threshold on fresh worlds | resolved in S0-a3 |
| EXEC-1 | zero provider failures | preserve concise schema / 1024 ceiling | zero failures | resolved in S0-a3 |
| CONTRACT-2 | most action inconsistencies resolved; observatory remains below gate | retain case-ID keyed response | correct fresh control | partially resolved |
| PROVENANCE-1 | evidence values detach from root IDs | evidence objects include source_id and signal | observatory verbatim >=0.85 and all other original gates | pending S0-a4 |

## Next run

S0-a4 uses untouched seeds 106/107, same task generator, fields and thresholds except evidence now retains source identity. No deterministic deduplication or solver is inserted into actors. This is the final bounded repair screen in this cycle. USD 15 quota, 1,728-call ceiling are non-overlapping allocations from the original shared cap; before S0-a4, 545 call slots used. If still unqualified, preserve the boundary, publish the instrument and limit, and do not run S1. If passed, independently audit all frames, freeze S1 review, verify source/config hashes and run the original six-arm comparison on seeds 200/201.
