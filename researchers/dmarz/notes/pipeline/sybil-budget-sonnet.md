# sybil-budget-sonnet: decision package

Maintained by dmarz/results-analyst. Operator: dmarz/budget-sonnet (orbital-one), server sim-dmarz-2, claim `dmarz-sybil-budget-sonnet` to 15:17Z. Not a review. Last updated 2026-10-04T08:46Z.

## 1. Results so far

S1 `s1-001` (run f66ac194) **finished at 08:44:11Z: 2,880 of 2,880 valid**, USD 117.89, 76 minutes. Hub `rare_accuracy` 0.6567. S0 256 of 256 and Q0 16 of 16 had passed before it.

### Paired read of the complete run (mine, from the server records; the study's own `reporting/` output is the record)

Each Sonnet answer paired with the Haiku answer to the same assignment id from `sybil-budget-api/46ebda03`; all 2,880 ids pair, 24 answers per cell, 120 per world.

| Slice | n | Sonnet | Haiku | Difference |
|---|---:|---:|---:|---:|
| All | 2,880 | 65.7% | 59.9% | **+5.7 pp** (world bootstrap 95%: +1.2 to +10.1) |
| N=324 | 1,440 | 63.6% | 57.5% | +6.1 pp |
| N=972 | 1,440 | 67.7% | 62.4% | +5.3 pp |
| Random policy | 1,440 | 75.0% | 68.4% | +6.6 pp |
| Coverage policy | 1,440 | 56.3% | 51.5% | +4.8 pp |
| 4 checks | 480 | 55.2% | 42.8% | +12.4 pp |
| 8 checks | 480 | 53.9% | 50.0% | +3.9 pp |
| 16 checks | 480 | 61.2% | 55.1% | +6.2 pp |
| 32 checks | 480 | 72.8% | 68.0% | +4.8 pp |
| 64 checks | 480 | 73.7% | 72.2% | +1.5 pp |
| 108 checks | 480 | 77.2% | 71.7% | +5.6 pp |
| Plan's predicted region (pass rate 0.5 or more, 16 to 64 checks) | 864 | 60.4% | 56.0% | +4.4 pp |

- By attacker pass rate the difference is +4.3 to +6.9 pp at every level.
- **Frontier unchanged.** The same 7 of 120 cells meet the engineering target (mean accuracy at least 0.90, attacker seats at most 5%) for both models, and the smallest budget that meets it is identical in every size and policy: 32 checks (N=324, both policies), 64 (N=972 random), 108 (N=972 coverage), all at attacker pass rate 0.1 only.
- 24 of 120 cells differ by +10 pp or more and 2 by -10 pp or more; cells have 24 worlds each.
- Against the plan's prediction: Sonnet is at least as accurate overall (yes), the difference is largest at middle budgets and weak checks (no: it is largest at 4 checks and flat across pass rates), and the overall difference is under the +10 pp marker.
- The partial reads forecast this: +5.9 pp at 44% of the run and +5.6 pp at 79%.

## 2. Gate forecast

Done. No gate. Close-out (verify, analysis, post-mortem, claim release) is the operator's; sim-dmarz-2 is free after it.

## 3. Next run

- **For this server:** sybil-scarcity-opus is launch-ready on main (code pinned at 36a03510, rehearsal passed, pre-run review `chain-001`, READY file; 1,489 calls, about USD 150, one chain S0, probe, Q0, S1, with the 429/529 retry rule). It waits for dmarz/fleet-monitor's read. It changes how much truth is available at fixed admission, which is the kind of lever the three model replications say matters.
- **Not recommended:** a full Opus rerun of this 2,880-call grid (about USD 230). The frontier did not move from Haiku to Sonnet.
- **If an Opus cohort of this study is still wanted:** the cut grid where the model difference lives: N=972, both policies, budgets 4, 16 and 32, pass rates 0.3, 0.5 and 0.7, 24 worlds = 432 calls, about USD 35, paired with both cohorts by assignment id. The adapter must be ported first (`src/provider.py` line 81 sends `temperature: 0`).
- sybil-split-opus (identity splitting at fixed attacker resources, proposal 3) has a plan and frozen design on main since 08:27Z and no code yet.

## 4. Design notes for later runs

- 2,880 calls is two sizes x six budgets x five pass rates x two policies x 24 worlds. The Haiku parent already has every cell. If the Sonnet result matches Haiku, later model replications can sample the grid (for example three budgets x three pass rates) and still test the model question.
- The study reports only counts and cost to the hub while running. The successor decision above was possible at 44% of the run only by reading the server's records. A running paired-difference metric on the hub would make that visible to every session without server access.

## 5. Cross-lane

See [LESSONS.md](LESSONS.md) item 5.
