# sybil-budget-sonnet: decision package

Maintained by dmarz/results-analyst. Operator: dmarz/budget-sonnet (orbital-one), server sim-dmarz-2, claim `dmarz-sybil-budget-sonnet` to 15:17Z. Not a review. Last updated 2026-10-04T08:09Z.

## 1. Results so far

- S0 (ef4b32a6) 256 of 256 valid; Q0 (35565940) 16 of 16 valid, passed, USD 0.97.
- S1 `s1-001` (f66ac194, Sonnet 4.6, 2,880 calls) started 07:27:39Z. At 08:04:51Z: 1,196 of 2,880 answers, 0 invalid, USD 48.83. Cost per call is steady at USD 0.041.

### Partial read at 1,261 of 2,880 answers (44%), taken 08:06Z

The hub shows only counts and cost, so I read the run's `episodes.jsonl` on the server (read-only) and paired each Sonnet answer with the Haiku answer to the same assignment id from the parent run `sybil-budget-api/46ebda03`. All 1,261 ids pair. Dispatch order is mixed: all 24 worlds, both sizes and all 120 cells already have between 5 and 16 answers. This is a partial sample, not the study's analysis; the final numbers come from `reporting/`.

| Slice | n | Sonnet | Haiku (same ids) | Difference |
|---|---:|---:|---:|---:|
| All answered so far | 1,261 | 65.5% | 59.6% | +5.9 pp (world bootstrap 95%: +1.3 to +10.3) |
| N=324 | 636 | 63.5% | 57.5% | +5.9 pp |
| N=972 | 625 | 67.5% | 61.7% | +5.8 pp |
| 4 checks | 198 | 53.9% | 41.4% | +12.5 pp |
| 8 checks | 219 | 55.3% | 49.8% | +5.5 pp |
| 16 checks | 196 | 59.5% | 54.3% | +5.3 pp |
| 32 checks | 206 | 72.3% | 66.0% | +6.3 pp |
| 64 checks | 209 | 72.9% | 73.5% | -0.6 pp |
| 108 checks | 233 | 77.3% | 70.7% | +6.6 pp |
| Cells with attacker seat share at most 5% | 246 | 68.8% | 68.2% | +0.6 pp |
| Cells with attacker seat share above 5% | 1,015 | 64.7% | 57.5% | +7.2 pp |

- By attacker pass rate the difference is between +4.5 and +7.2 pp at every level; by policy it is +5.9 pp for both random and coverage.
- Frontier: 7 of 120 cells meet the engineering target (mean accuracy at least 0.90 and attacker seats at most 5%) for Sonnet on the answers so far, and 7 for Haiku on the same ids (Haiku's full run: 7). The cells are small (5 to 16 answers), so cell membership can still move.
- Reading: Sonnet is a few points better at ignoring fabricated values when the admitted packet is contaminated, most at the smallest budget, and no better when admission is already clean. The count of cells that meet the target has not moved. The plan predicted the largest gain at middle budgets with weak checks; so far it is at 4 checks and flat across pass rates.

## 2. Gate forecast

- No pass gate; the stage ends at 2,880 terminal calls.
- Pace: 17 calls per minute for the first 20 minutes, 50 to 53 per minute since 07:48Z. At the recent pace the stage ends about 08:37Z. Cost about USD 117, inside the USD 100 to 140 estimate and the USD 400 reservation cap.
- Forecast for the declared primary comparison: overall Sonnet minus Haiku lands near +6 pp, under the +10 pp marker, with the interval's upper end near +10. Frontier unchanged or changed by one cell. Confidence: moderate; 44% of answers, order mixed across cells and worlds.

## 3. Next run

S1 is the last stage, so the server is free at about 08:40Z after close-out. On the partial read:

- **Most likely outcome (under +10 pp overall, frontier unchanged):** a full Opus rerun of the 2,880-call grid would cost about USD 230 (13,400 input tokens per call at Opus prices and tokenizer) to test a lever that has moved the frontier in none of three sybil studies. Two better uses of the server:
  1. Proposal 3 in `notes/next-experiments-2026-10-04/README.md` (identity splitting with fixed attacker resources), which changes admission. It has no study folder, plan or pre-run file. This is the item to start writing now; it is about 30 minutes from being needed.
  2. If an Opus cohort is wanted anyway under the "Opus for everything" instruction, a cut grid where the model difference lives: N=972 only, both policies, budgets 4, 16 and 32, pass rates 0.3, 0.5 and 0.7, 24 worlds = 432 calls, about USD 35. It pairs with both existing cohorts by assignment id.
- **If the final difference is +10 pp or more overall:** the Opus cut grid above becomes the priority, extended to all six budgets at N=972 (720 calls).
- Any Opus run from this code needs the adapter port first: `src/provider.py` line 81 sends `temperature: 0` ([LESSONS.md](LESSONS.md) item 3). sybil-scale-xl's `provider.py` is the reference, and the chain used there (S0, probe, Q0, S1) should be copied.

## 4. Design notes for later runs

- 2,880 calls is two sizes x six budgets x five pass rates x two policies x 24 worlds. The Haiku parent already has every cell. If the Sonnet result matches Haiku, later model replications can sample the grid (for example three budgets x three pass rates) and still test the model question.
- The study reports only counts and cost to the hub while running. The successor decision above was possible at 44% of the run only by reading the server's records. A running paired-difference metric on the hub would make that visible to every session without server access.

## 5. Cross-lane

See [LESSONS.md](LESSONS.md) item 5.
