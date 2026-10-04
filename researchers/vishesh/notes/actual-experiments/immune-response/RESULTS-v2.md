# V2 qualification results

2026-10-04 UTC. These are scripted engineering results, not LLM findings. Protocol and instrument were committed before execution at local commit efa48c3; the identical change was rebased and published as bcba39e before model execution. Source hashes in each manifest identify the executable contents.

S0: 32 assigned, 32 recorded, zero invalid. S1: 256 assigned, 256 recorded, zero invalid. All 17 unit tests passed. S1 covers eight task IDs in each of four strata with eight arms; model calls and model cost are zero. All paired estimates include assigned outcomes; complete-pair estimates coincide because none failed.

| Private-restored factorial arm | Shared restored | Stale IDs blocked | Completion in each incident stratum | Relapse after recovery |
|---|---|---|---:|---:|
| Q10 | no | no | 38.9% | 0% (persistent failure) |
| Q10F | no | yes | 38.9% | 0% (persistent failure) |
| Q11R | yes | no | 72.2% | 100% |
| Q11 | yes | yes | 100% | 0% |

In shared_evidence, the primary all-assigned paired difference Q11-Q10F is +61.1 percentage points (8/8 valid pairs). Shared restoration without filtering contributes +33.3 points; filtering with shared restoration contributes +27.8 points; filtering without restoration contributes zero. The interaction is +27.8 points. All three incident strata have identical scripted outcomes, so they are not evidence of broad robustness. All arms complete 100% in the no-incident control and accept the legitimate round-18 update by round 20. Source revocation still loses 18 source turns.

The result verifies the fixture's intended distinction: resetting the private and shared stores permits recovery, while blocking stale descendants makes that recovery persist. The scripted policy deterministically prefers higher-version records; it does not demonstrate that an LLM does so. No confidence interval or significance claim is warranted for this engineering test. Detection, selective repair, unique benign learning, general deployment safety and large-swarm behavior remain untested. Native S0 results will be added separately after execution.
