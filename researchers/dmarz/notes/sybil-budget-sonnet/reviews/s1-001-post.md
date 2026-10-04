# Post-mortem for sybil-budget-sonnet s1-001

Experiment sybil-budget-sonnet, owner dmarz (operator dmarz/budget-sonnet; launched by dmarz/orchestrator-2). Run `sybil-budget-sonnet/f66ac194`, revision `b8fed70d2056d47d499fd47ea67e6785b9a4d8ef`, source hash `5cbe54cbd48bc164c7873d2a419710118455c74cf73122a137992361998cf680`, host sim-dmarz-2 under exclusive claim `dmarz-sybil-budget-sonnet` (agentops PR #195; released PR #235 at ~08:45Z). Pre-run assessment: [s1-001-pre](s1-001-pre.md). Review: owner waiver (SETUP.md G0), not an independent review.

## Reconcile the recorded facts

- Planned, started, terminal, graded, analyzed: 2,880 / 2,880 / 2,880 / 2,880 / 2,880. Invalid 0, not started 0, no retries, no transport or provider errors.
- Model `claude-sonnet-4-6`, temperature 0, 500 output tokens; returned model id matched on every call.
- S1 usage: 2,880 calls, 38,757,548 input and 107,643 output tokens, **USD 117.887289**; wall time 4,365 s (about 73 min) including about 12 min of single-threaded grid preparation before the first dispatch.
- Study total (Q0 + S1): 2,896 calls, **USD 118.854846** actual, USD 392.195028 reserved (cap USD 400). The pre-run estimate of USD 100-140 held.
- Launch timing: S1 was launched at 07:27Z, before the owner's 07:36Z "use opus for everything going forward" instruction reached the operator; per that instruction's own rule a launched run finishes as launched. Cost was not a gate (owner, 07:42Z).
- Verification: hub artifacts published and `verify` passed; local Python 3.12 `reporting/verify_results.py` regenerated assignments, worlds and check trajectories from frozen source and matched every packet hash, grade, counter, analysis value and the accounting exactly ([record](../records/s1-001-linux-verification.json)). GIF has 25 frames. Browser playback on the public site was not checked.

## Interpret the result

See [RESULTS.md](../RESULTS.md). Measured: Sonnet minus Haiku specialist accuracy +5.7 pp across the paired grid (world bootstrap +1.2 to +10.0); 102 of 120 cells higher; attacker seat share and honest retention identical in every cell; the engineering frontier is identical to Haiku's; the primary coverage 108-minus-4 contrast is +47.2 pp (descriptive +31.9 to +61.1) versus Haiku's +56.9 pp, a difference of -9.7 pp (-29.2 to +9.7) that this sample cannot distinguish from zero. Inferred: the model is not the lever for the security frontier in this instrument; admission decides what evidence reaches the synthesiser.

## Assess experiment quality

- Pairing held: identical assignment ids and packet hashes across cohorts (checked by `reporting/compare_haiku.py`).
- Limits carried from the parent: one synthetic ring graph, two trust seeds, simulated independent checks, repeated specialist facts, one +7 fabrication, 24 worlds; threshold crossings can be unstable at this sample size; no S2.
- Measurement note: the comparison script uses its own world bootstrap (seeded), so its Sonnet-only primary interval differs slightly from `analyze.py`'s; the RESULTS headline uses `analyze.py` for single-cohort values and the script only for cross-model differences.

## Resolve issues and prior suggestions

- The results analyst's partial read at 44% (+5.9 pp, frontier unchanged) is confirmed by the final data (+5.7 pp, frontier identical).
- No defects found. Grid preparation is CPU-bound for about 12 minutes before dispatch; that looks like a stall in status output (0 calls) and was mistaken for one once. A future run should log a preparation heartbeat.

## Closeout and handoff

Claim released (PR #235); worker exited; artifacts published and verified; raw records kept in git-ignored `data/sybil-budget-sonnet/s1/` on orbital-one, summaries in `records/`. Next run: none planned for this study. The analyst recommends not running a full Opus cohort (about USD 230 for little information); if one is run, use the 432-call cut grid (N972, budgets 4/16/32, pass 0.3/0.5/0.7). Server time is better spent on a different study.
