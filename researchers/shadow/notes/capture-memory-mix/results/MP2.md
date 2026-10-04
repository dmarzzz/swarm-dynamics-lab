# capture-memory-mix: MP2 results

90 selected arm records (90 raw records in the files, 46 of them invalid, 0 superseded by a later attempt of the same episode; see 'Attempt lineage' below), backends ['http:google/gemma-3-27b-it:sample'], about 12170 model calls in the selected records; provider-reported spend on the shared ledger (all models, all pilot work, including superseded attempts) 3.9326 USD. Code commits: ['016104d9', '3ffb56b6'].

Columns: captured = capture rate (shared by arms); frac@rem / frac_T = honest fraction on the original at removal and 30 rounds later (eval_round in the records' cfg; captured episodes); delta = frac_T minus frac@rem (0 = frozen, > 0 = returning); short_T / long_T = the same at round T split by memory kind; delta_long = return among the long-memory agents only.

## Cells (captured episodes unless noted)

| world | dose | memory | arm | n | inv | captured | lat | frac@rem | frac_T | delta | short_T | long_T | delta_long | recovered | half-time |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| W1_INSIDE | 0.5 | 1 | A0_no_purge | 2 | 4 | 1.00 | 2.0 | 0.000 | 0.000 | +0.000 | nan | 0.000 | +0.000 | 0.00 | None |
| W1_INSIDE | 0.5 | 1 | A1_purge | 3 | 3 | 1.00 | 2 | 0.000 | 0.000 | +0.000 | nan | 0.000 | +0.000 | 0.00 | None |
| W1_INSIDE | 0.5 | 1 | A2_purge_wipe | 3 | 3 | 1.00 | 2 | 0.042 | 0.042 | +0.000 | nan | 0.042 | +0.000 | 0.00 | None |
| W1_INSIDE | 0.5 | full | A0_no_purge | 3 | 3 | 1.00 | 9 | 0.042 | 0.000 | -0.042 | nan | 0.000 | -0.042 | 0.00 | None |
| W1_INSIDE | 0.5 | full | A1_purge | 3 | 3 | 1.00 | 9 | 0.042 | 0.000 | -0.042 | nan | 0.000 | -0.042 | 0.00 | None |
| W1_INSIDE | 0.5 | full | A2_purge_wipe | 2 | 4 | 1.00 | 9.0 | 0.062 | 0.000 | -0.062 | nan | 0.000 | -0.062 | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@0 | A0_no_purge | 3 | 0 | 1.00 | 9 | 0.042 | 0.000 | -0.042 | nan | 0.000 | -0.042 | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@0 | A1_purge | 3 | 0 | 1.00 | 9 | 0.042 | 0.000 | -0.042 | nan | 0.000 | -0.042 | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@0 | A2_purge_wipe | 2 | 0 | 1.00 | 9.0 | 0.062 | 0.000 | -0.062 | nan | 0.000 | -0.062 | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@0.5 | A0_no_purge | 4 | 2 | 1.00 | 6.5 | 0.125 | 0.000 | -0.125 | 0.000 | 0.000 | -0.125 | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@0.5 | A1_purge | 4 | 2 | 1.00 | 6.5 | 0.125 | 0.000 | -0.125 | 0.000 | 0.000 | -0.125 | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@0.5 | A2_purge_wipe | 2 | 4 | 1.00 | 6.5 | 0.125 | 0.000 | -0.125 | 0.000 | 0.000 | -0.125 | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@0.75 | A0_no_purge | 3 | 3 | 1.00 | 4 | 0.208 | 0.000 | -0.208 | 0.000 | 0.000 | -0.667 | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@0.75 | A1_purge | 3 | 3 | 1.00 | 4 | 0.208 | 0.042 | -0.167 | 0.056 | 0.000 | -0.667 | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@0.75 | A2_purge_wipe | 3 | 3 | 1.00 | 4 | 0.208 | 0.000 | -0.208 | 0.000 | 0.000 | -0.667 | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@0.875 | A0_no_purge | 3 | 3 | 1.00 | 2 | 0.167 | 0.000 | -0.167 | 0.000 | 0.000 | -0.333 | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@0.875 | A1_purge | 3 | 3 | 1.00 | 2 | 0.167 | 0.125 | -0.042 | 0.143 | 0.000 | -0.333 | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@0.875 | A2_purge_wipe | 3 | 3 | 1.00 | 2 | 0.167 | 0.083 | -0.083 | 0.095 | 0.000 | -0.333 | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@1 | A0_no_purge | 2 | 0 | 1.00 | 2.0 | 0.000 | 0.000 | +0.000 | nan | 0.000 | +0.000 | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@1 | A1_purge | 3 | 0 | 1.00 | 2 | 0.000 | 0.000 | +0.000 | nan | 0.000 | +0.000 | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@1 | A2_purge_wipe | 3 | 0 | 1.00 | 2 | 0.042 | 0.042 | +0.000 | nan | 0.042 | +0.000 | 0.00 | None |

## Contrasts over the short-memory fraction f (paired per draw, vs f = 0 of the same family; captured under both)

Declared primary: M1, W1_INSIDE, arm A1_purge, metric delta_original, family mix:1/full at dose 0.54, f = 0.5 minus f = 0.0. Everything else is exploratory.

| world | dose | family | arm | metric | f | mean(f) | mean(f=0) | diff | 95% CI | tasks | pairs |
|---|---|---|---|---|---|---|---|---|---|---|---|
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_original | 0.5 | -0.125 | -0.062 | -0.062 | [-0.125, +0.000] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_original | 0.75 | -0.188 | -0.062 | -0.125 | [-0.125, -0.125] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_original | 0.875 | 0.125 | -0.125 | +0.250 | [+0.250, +0.250] | 1 | 1 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_original | 1 | 0.000 | -0.125 | +0.125 | [+0.125, +0.125] | 1 | 1 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | frac_original_T | 0.5 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | frac_original_T | 0.75 | 0.062 | 0.000 | +0.062 | [+0.000, +0.125] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | frac_original_T | 0.875 | 0.375 | 0.000 | +0.375 | [+0.375, +0.375] | 1 | 1 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | frac_original_T | 1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | 1 | 1 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | long_T | 0.5 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | long_T | 0.75 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | long_T | 0.875 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | 1 | 1 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | long_T | 1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | 1 | 1 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_long | 0.5 | -0.125 | -0.062 | -0.062 | [-0.250, +0.125] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_long | 0.75 | -0.750 | -0.062 | -0.688 | [-1.000, -0.375] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_long | 0.875 | 0.000 | -0.125 | +0.125 | [+0.125, +0.125] | 1 | 1 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_long | 1 | 0.000 | -0.125 | +0.125 | [+0.125, +0.125] | 1 | 1 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_original | 0.75 | -0.250 | -0.125 | -0.125 | [-0.125, -0.125] | 1 | 1 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_original | 0.875 | 0.000 | -0.125 | +0.125 | [+0.125, +0.125] | 1 | 1 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_original | 1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | 1 | 1 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | frac_original_T | 0.75 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | 1 | 1 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | frac_original_T | 0.875 | 0.250 | 0.000 | +0.250 | [+0.250, +0.250] | 1 | 1 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | frac_original_T | 1 | 0.125 | 0.000 | +0.125 | [+0.125, +0.125] | 1 | 1 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | long_T | 0.75 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | 1 | 1 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | long_T | 0.875 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | 1 | 1 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | long_T | 1 | 0.125 | 0.000 | +0.125 | [+0.125, +0.125] | 1 | 1 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_long | 0.75 | -0.500 | -0.125 | -0.375 | [-0.375, -0.375] | 1 | 1 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_long | 0.875 | 0.000 | -0.125 | +0.125 | [+0.125, +0.125] | 1 | 1 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_long | 1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | 1 | 1 |

### Rescue threshold (design: smallest f with delta_original under A1_purge > +0.10 and CI lower bound > 0)

| world | dose | family | f* | delta at f* | CI lower |
|---|---|---|---|---|---|
| W1_INSIDE | 0.5 | mix:1/full | 0.875 | +0.125 | +0.125 |

## Wipe bridge: A2_purge_wipe minus A1_purge on frac_original_T, per cell (captured episodes, paired)

| world | dose | memory | mean wipe | mean purge | diff | 95% CI | tasks |
|---|---|---|---|---|---|---|---|
| W1_INSIDE | 0.5 | 1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | 2 |
| W1_INSIDE | 0.5 | full | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | 2 |
| W1_INSIDE | 0.5 | mix:1/full@0 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | 2 |
| W1_INSIDE | 0.5 | mix:1/full@0.5 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | 2 |
| W1_INSIDE | 0.5 | mix:1/full@0.75 | 0.000 | 0.042 | -0.042 | [-0.125, +0.000] | 3 |
| W1_INSIDE | 0.5 | mix:1/full@0.875 | 0.083 | 0.125 | -0.042 | [-0.125, +0.000] | 3 |
| W1_INSIDE | 0.5 | mix:1/full@1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | 2 |

## Mean honest fraction on the original after removal, A1_purge, captured episodes (rounds 1, 5, 10, 20, 30 after removal; recovery phase 40 rounds)

| world | dose | memory | r1 | r5 | r10 | r20 | r30 | long r30 | short r30 |
|---|---|---|---|---|---|---|---|---|---|
| W1_INSIDE | 0.5 | 1 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | nan |
| W1_INSIDE | 0.5 | full | 0.083 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | nan |
| W1_INSIDE | 0.5 | mix:1/full@0 | 0.083 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | nan |
| W1_INSIDE | 0.5 | mix:1/full@0.5 | 0.094 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| W1_INSIDE | 0.5 | mix:1/full@0.75 | 0.208 | 0.208 | 0.208 | 0.125 | 0.042 | 0.000 | 0.056 |
| W1_INSIDE | 0.5 | mix:1/full@0.875 | 0.167 | 0.208 | 0.167 | 0.125 | 0.125 | 0.000 | 0.143 |
| W1_INSIDE | 0.5 | mix:1/full@1 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | nan |

## Attempt lineage (raw records vs selected records)

An attempt = one run of an episode's arms in the append-only file. Resumed workers re-ran every episode that did not already have all arms valid. Selection: last attempt with all arms valid, else last attempt. 'episodes multi valid' counts episodes with more than one fully valid attempt (selection then takes the last one; see CORRECTIONS.md for the first-valid-attempt sensitivity check; this is NOT a first-observed-record analysis).

| world | dose | memory | episodes | attempts | episodes rerun | episodes multi valid | raw records | raw invalid | superseded records | selected records | selected valid | selected invalid | first observed valid |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| W1_INSIDE | 0.5 | 1 | 6 | 6 | 0 | 0 | 18 | 10 | 0 | 18 | 8 | 10 | 8 |
| W1_INSIDE | 0.5 | full | 6 | 6 | 0 | 0 | 18 | 10 | 0 | 18 | 8 | 10 | 8 |
| W1_INSIDE | 0.5 | mix:1/full@0.5 | 6 | 6 | 0 | 0 | 18 | 8 | 0 | 18 | 10 | 8 | 10 |
| W1_INSIDE | 0.5 | mix:1/full@0.75 | 6 | 6 | 0 | 0 | 18 | 9 | 0 | 18 | 9 | 9 | 9 |
| W1_INSIDE | 0.5 | mix:1/full@0.875 | 6 | 6 | 0 | 0 | 18 | 9 | 0 | 18 | 9 | 9 | 9 |
| **total** | | | **30** | **30** | **0** | **0** | **90** | **46** | **0** | **90** | **44** | **46** | **44** |

Retry accounting: no episode was re-run; 46 selected records are invalid and are counted in the 'inv' column, not dropped silently. Capture is decided before removal and shared by the arms.
