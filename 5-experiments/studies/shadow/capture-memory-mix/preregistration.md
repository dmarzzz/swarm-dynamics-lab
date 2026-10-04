# Pre-registration record: capture-memory-mix (exploratory, researcher notes)

What was fixed before each stage ran, and what changed afterwards (labelled). Sections follow
`templates/experiment-worker/preregistration.md`. Nothing here is an accepted hypothesis; the lane is a hunch built on
[capture-memory](../capture-memory/) under the 12-hour goal in `GOAL-12H.md`.

## 1. Hypotheses (fixed 04:05Z, before M1)

- **H1 (rescue).** In a captured population whose honest agents hold an unbounded running-mean memory (frozen after a
  perfect purge in capture-memory S1b), adding a fraction f of one-slot-memory agents restarts the return toward the
  original convention: `delta_original` under A1_purge rises with f from f = 0.
- **H2 (non-monotone).** The return is not monotone in f: an all-short population (f = 1) returns less than some
  interior mixture, because short agents alone have no anchor and long agents alone cannot move.
- **H3 (wipe harm persists).** A2_purge_wipe minus A1_purge on the round-T fraction is negative for every f < 1 and
  its size is governed by how much the mixture relies on the long-memory anchor.
- **H4 (regime control).** In W2_OUTSIDE (not metastable) the f-dependence is monotone and wipe does not harm.

## 2. Contrasts declared in advance (design.yaml `primary_contrast`)

- Primary: stage M1, W1_INSIDE, arm A1_purge, metric `delta_original` (frac on original at round 50 minus at removal),
  family mix 1/full at dose 0.54, f = 0.5 minus f = 0, paired per (task, seed), episodes captured under both, 95%
  cluster bootstrap over tasks.
- Rescue threshold rule: smallest grid f with `delta_original` > +0.10 and CI lower bound > 0.
- Secondary: `frac_original_T`, `long_T`, `delta_long`, `short_T`, `half_time`; wipe bridge per f.
- Everything else exploratory.

## 3. Minimum meaningful effect

Primary difference at or above +0.10; wipe bridge at or below -0.10 to call harm; rescue threshold f* reported as a
grid point, not interpolated.

## 4. Units, denominators, retry policy

Unit of assignment = (task, seed) draw; unit of analysis = episode (one arm, one memory spec); cluster = task.
Invalid episodes (policy raised) are recorded with the error string, counted per cell, never retried, never dropped.
Capture is decided before the intervention and shared by the three arms of an episode.

## 5. Real-model pilot MP (fixed 04:40Z, before any paid pilot call)

Model chosen by calibration (`src/calibrate.py`, probe logs): the first model whose first-token response curve over a
5-slot window is a majority rule with fitted beta > 1 and |h| < h_s(beta). Cells: N = 16, dose 8/16, entrench 5,
takeover cap 60, recovery 40, scored at round 30; memory in {1, full, mix 1/full at 0.5, 0.75, 0.875}; arms A0/A1/A2;
6 tasks x 1 seed first, extended if budget allows. Decision rule (design.yaml `pilot_MP.decision`): reproduction =
any of (a) freeze vs return between full and 1, (b) wipe minus purge < -0.1 at full, (c) a mixture's `delta_original`
exceeds all-full by > 0.1; each with its paired CI; reported as a pilot regardless of n.

Scripted prediction at the model's fitted parameters is produced BEFORE the pilot (`src/predict.py`) and kept in
`results/pilot-pred-*` (git-ignored, regenerable: deterministic).

## 6. Amendments after seeing data (labelled)

- 05:45Z (after run 1): hard cap raised from USD 5 to 10 on dmarz's OK. The ledger is reconciled to OpenRouter account
  usage (`src/ledger_sync.py`), which is authoritative over the local file.
- 05:50Z: added f = 5/8 and 15/16 cells to locate the peak; tasks extended 0 to 11 (later 0 to 23 on the original five
  cells). Added because run 1 showed the peak between 1/2 and 1; not a change of metric or rule.
- 06:20Z (after run 2): the pilot outcome is bimodal, so the mean-based contrasts in the design under-describe it.
  Added, as exploratory and clearly post hoc, two count-based summaries in `src/mp_stats.py`: number of episodes fully
  recovered (the design's `recovered` metric, already pre-declared as secondary in capture-memory) and number at or
  above 0.5 at round T, with a one-sided Fisher exact test of interior mixtures (f in {5/8, 3/4, 7/8}) against all
  other cells. The grouping "interior mixtures" was chosen after seeing run 1 (which showed 3/4 and 7/8 rescuing) and
  before run 2 finished, so it is partially pre-specified; treat the p-values as descriptive.
- 05:55Z: second model gemma-3-27b-it added in `mode: sample` because no provider returns its logprobs; third model
  qwen3-235b-a22b added in logprobs mode. Both use the same cells and rules.
- 06:30Z: adapter bug (unbound `resp` after exhausted retries) found in the first qwen attempt; 79 invalid episodes
  kept in `results/pilot-mp3-attempt1` (git-ignored, on disk), the pilot restarted clean with more retries.
- 2026-10-04 (shadow/sol-cm2, after dmarz's review; see CORRECTIONS.md): section 4 "never retried" holds for the
  scripted stages only. The pilots ran a resumable worker that re-runs every episode without a fully valid attempt
  (validity-triggered, outcome-blind). Selection rule, stated now and applied to all pilots: per episode, the last
  attempt with every arm valid, else the last attempt (`src/lineage.py`); it selects exactly the records the earlier
  per-arm dedup selected. Pilot captions corrected to the configured scoring round (30, not 50).
