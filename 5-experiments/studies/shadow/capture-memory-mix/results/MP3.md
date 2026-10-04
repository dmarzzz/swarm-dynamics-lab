# capture-memory-mix: MP3 results

180 selected arm records (327 raw records in the files, 127 of them invalid, 147 superseded by a later attempt of the same episode; see 'Attempt lineage' below), backends ['http:qwen/qwen3-235b-a22b-2507'], about 45056 model calls in the selected records; provider-reported spend on the shared ledger (all models, all pilot work, including superseded attempts) 3.9326 USD. Code commits: ['9d82e5ab', 'bd54bbed'].

Columns: captured = capture rate (shared by arms); frac@rem / frac_T = honest fraction on the original at removal and 30 rounds later (eval_round in the records' cfg; captured episodes); delta = frac_T minus frac@rem (0 = frozen, > 0 = returning); short_T / long_T = the same at round T split by memory kind; delta_long = return among the long-memory agents only.

## Cells (captured episodes unless noted)

| world | dose | memory | arm | n | inv | captured | lat | frac@rem | frac_T | delta | short_T | long_T | delta_long | recovered | half-time |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| W1_INSIDE | 0.5 | 1 | A0_no_purge | 12 | 0 | 1.00 | 2.0 | 0.115 | 0.177 | +0.062 | nan | 0.177 | +0.062 | 0.00 | 4.0 |
| W1_INSIDE | 0.5 | 1 | A1_purge | 12 | 0 | 1.00 | 2.0 | 0.115 | 0.375 | +0.260 | nan | 0.375 | +0.260 | 0.17 | 17 |
| W1_INSIDE | 0.5 | 1 | A2_purge_wipe | 12 | 0 | 1.00 | 2.0 | 0.115 | 0.406 | +0.292 | nan | 0.406 | +0.292 | 0.17 | 12 |
| W1_INSIDE | 0.5 | full | A0_no_purge | 12 | 0 | 1.00 | 11.0 | 0.052 | 0.021 | -0.031 | nan | 0.021 | -0.031 | 0.00 | None |
| W1_INSIDE | 0.5 | full | A1_purge | 12 | 0 | 1.00 | 11.0 | 0.052 | 0.010 | -0.042 | nan | 0.010 | -0.042 | 0.00 | None |
| W1_INSIDE | 0.5 | full | A2_purge_wipe | 11 | 1 | 1.00 | 11 | 0.034 | 0.000 | -0.034 | nan | 0.000 | -0.034 | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@0 | A0_no_purge | 12 | 0 | 1.00 | 11.0 | 0.052 | 0.021 | -0.031 | nan | 0.021 | -0.031 | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@0 | A1_purge | 12 | 0 | 1.00 | 11.0 | 0.052 | 0.010 | -0.042 | nan | 0.010 | -0.042 | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@0 | A2_purge_wipe | 11 | 0 | 1.00 | 11 | 0.034 | 0.000 | -0.034 | nan | 0.000 | -0.034 | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@0.5 | A0_no_purge | 12 | 0 | 1.00 | 7.5 | 0.083 | 0.094 | +0.010 | 0.146 | 0.042 | +0.000 | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@0.5 | A1_purge | 12 | 0 | 1.00 | 7.5 | 0.083 | 0.094 | +0.010 | 0.167 | 0.021 | -0.021 | 0.00 | 16 |
| W1_INSIDE | 0.5 | mix:1/full@0.5 | A2_purge_wipe | 12 | 0 | 1.00 | 7.5 | 0.083 | 0.125 | +0.042 | 0.188 | 0.062 | +0.021 | 0.00 | 15.5 |
| W1_INSIDE | 0.5 | mix:1/full@0.75 | A0_no_purge | 11 | 1 | 1.00 | 5 | 0.091 | 0.091 | +0.000 | 0.121 | 0.000 | -0.091 | 0.00 | 19 |
| W1_INSIDE | 0.5 | mix:1/full@0.75 | A1_purge | 12 | 0 | 1.00 | 5.0 | 0.104 | 0.156 | +0.052 | 0.208 | 0.000 | -0.167 | 0.00 | 20 |
| W1_INSIDE | 0.5 | mix:1/full@0.75 | A2_purge_wipe | 12 | 0 | 1.00 | 5.0 | 0.104 | 0.167 | +0.062 | 0.208 | 0.042 | -0.125 | 0.00 | 19.5 |
| W1_INSIDE | 0.5 | mix:1/full@0.875 | A0_no_purge | 12 | 0 | 1.00 | 2.5 | 0.104 | 0.125 | +0.021 | 0.131 | 0.083 | -0.083 | 0.00 | 16.5 |
| W1_INSIDE | 0.5 | mix:1/full@0.875 | A1_purge | 12 | 0 | 1.00 | 2.5 | 0.104 | 0.229 | +0.125 | 0.250 | 0.083 | -0.083 | 0.00 | 14 |
| W1_INSIDE | 0.5 | mix:1/full@0.875 | A2_purge_wipe | 12 | 0 | 1.00 | 2.5 | 0.104 | 0.302 | +0.198 | 0.309 | 0.250 | +0.083 | 0.08 | 12.5 |
| W1_INSIDE | 0.5 | mix:1/full@1 | A0_no_purge | 12 | 0 | 1.00 | 2.0 | 0.115 | 0.177 | +0.062 | nan | 0.177 | +0.062 | 0.00 | 4.0 |
| W1_INSIDE | 0.5 | mix:1/full@1 | A1_purge | 12 | 0 | 1.00 | 2.0 | 0.115 | 0.375 | +0.260 | nan | 0.375 | +0.260 | 0.17 | 17 |
| W1_INSIDE | 0.5 | mix:1/full@1 | A2_purge_wipe | 12 | 0 | 1.00 | 2.0 | 0.115 | 0.406 | +0.292 | nan | 0.406 | +0.292 | 0.17 | 12 |

## Contrasts over the short-memory fraction f (paired per draw, vs f = 0 of the same family; captured under both)

Declared primary: M1, W1_INSIDE, arm A1_purge, metric delta_original, family mix:1/full at dose 0.54, f = 0.5 minus f = 0.0. Everything else is exploratory.

| world | dose | family | arm | metric | f | mean(f) | mean(f=0) | diff | 95% CI | tasks | pairs |
|---|---|---|---|---|---|---|---|---|---|---|---|
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_original | 0.5 | 0.010 | -0.042 | +0.052 | [-0.052, +0.167] | 12 | 12 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_original | 0.75 | 0.052 | -0.042 | +0.094 | [-0.052, +0.240] | 12 | 12 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_original | 0.875 | 0.125 | -0.042 | +0.167 | [+0.031, +0.323] | 12 | 12 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_original | 1 | 0.260 | -0.042 | +0.302 | [+0.177, +0.427] | 12 | 12 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | frac_original_T | 0.5 | 0.094 | 0.010 | +0.083 | [+0.031, +0.135] | 12 | 12 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | frac_original_T | 0.75 | 0.156 | 0.010 | +0.146 | [+0.062, +0.240] | 12 | 12 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | frac_original_T | 0.875 | 0.229 | 0.010 | +0.219 | [+0.104, +0.344] | 12 | 12 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | frac_original_T | 1 | 0.375 | 0.010 | +0.365 | [+0.240, +0.490] | 12 | 12 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | long_T | 0.5 | 0.021 | 0.010 | +0.010 | [-0.031, +0.062] | 12 | 12 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | long_T | 0.75 | 0.000 | 0.010 | -0.010 | [-0.031, +0.000] | 12 | 12 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | long_T | 0.875 | 0.083 | 0.010 | +0.073 | [+0.000, +0.219] | 12 | 12 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | long_T | 1 | 0.375 | 0.010 | +0.365 | [+0.240, +0.490] | 12 | 12 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_long | 0.5 | -0.021 | -0.042 | +0.021 | [-0.073, +0.125] | 12 | 12 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_long | 0.75 | -0.167 | -0.042 | -0.125 | [-0.333, +0.052] | 12 | 12 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_long | 0.875 | -0.083 | -0.042 | -0.042 | [-0.271, +0.188] | 12 | 12 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_long | 1 | 0.260 | -0.042 | +0.302 | [+0.177, +0.427] | 12 | 12 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_original | 0.5 | 0.023 | -0.034 | +0.057 | [-0.057, +0.182] | 11 | 11 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_original | 0.75 | 0.011 | -0.034 | +0.045 | [-0.080, +0.182] | 11 | 11 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_original | 0.875 | 0.136 | -0.034 | +0.170 | [+0.045, +0.307] | 11 | 11 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_original | 1 | 0.273 | -0.034 | +0.307 | [+0.205, +0.398] | 11 | 11 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | frac_original_T | 0.5 | 0.102 | 0.000 | +0.102 | [+0.011, +0.250] | 11 | 11 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | frac_original_T | 0.75 | 0.114 | 0.000 | +0.114 | [+0.045, +0.205] | 11 | 11 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | frac_original_T | 0.875 | 0.250 | 0.000 | +0.250 | [+0.125, +0.409] | 11 | 11 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | frac_original_T | 1 | 0.375 | 0.000 | +0.375 | [+0.273, +0.489] | 11 | 11 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | long_T | 0.5 | 0.045 | 0.000 | +0.045 | [+0.000, +0.136] | 11 | 11 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | long_T | 0.75 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | 11 | 11 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | long_T | 0.875 | 0.182 | 0.000 | +0.182 | [+0.000, +0.455] | 11 | 11 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | long_T | 1 | 0.375 | 0.000 | +0.375 | [+0.273, +0.489] | 11 | 11 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_long | 0.5 | 0.000 | -0.034 | +0.034 | [-0.080, +0.159] | 11 | 11 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_long | 0.75 | -0.182 | -0.034 | -0.148 | [-0.364, +0.045] | 11 | 11 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_long | 0.875 | 0.000 | -0.034 | +0.034 | [-0.284, +0.364] | 11 | 11 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_long | 1 | 0.273 | -0.034 | +0.307 | [+0.205, +0.398] | 11 | 11 |

### Rescue threshold (design: smallest f with delta_original under A1_purge > +0.10 and CI lower bound > 0)

| world | dose | family | f* | delta at f* | CI lower |
|---|---|---|---|---|---|
| W1_INSIDE | 0.5 | mix:1/full | 1 | +0.260 | +0.156 |

## Wipe bridge: A2_purge_wipe minus A1_purge on frac_original_T, per cell (captured episodes, paired)

| world | dose | memory | mean wipe | mean purge | diff | 95% CI | tasks |
|---|---|---|---|---|---|---|---|
| W1_INSIDE | 0.5 | 1 | 0.406 | 0.375 | +0.031 | [-0.031, +0.083] | 12 |
| W1_INSIDE | 0.5 | full | 0.000 | 0.011 | -0.011 | [-0.034, +0.000] | 11 |
| W1_INSIDE | 0.5 | mix:1/full@0 | 0.000 | 0.011 | -0.011 | [-0.034, +0.000] | 11 |
| W1_INSIDE | 0.5 | mix:1/full@0.5 | 0.125 | 0.094 | +0.031 | [-0.042, +0.135] | 12 |
| W1_INSIDE | 0.5 | mix:1/full@0.75 | 0.167 | 0.156 | +0.010 | [-0.031, +0.062] | 12 |
| W1_INSIDE | 0.5 | mix:1/full@0.875 | 0.302 | 0.229 | +0.073 | [+0.010, +0.135] | 12 |
| W1_INSIDE | 0.5 | mix:1/full@1 | 0.406 | 0.375 | +0.031 | [-0.031, +0.083] | 12 |

## Mean honest fraction on the original after removal, A1_purge, captured episodes (rounds 1, 5, 10, 20, 30 after removal; recovery phase 40 rounds)

| world | dose | memory | r1 | r5 | r10 | r20 | r30 | long r30 | short r30 |
|---|---|---|---|---|---|---|---|---|---|
| W1_INSIDE | 0.5 | 1 | 0.146 | 0.208 | 0.271 | 0.354 | 0.375 | 0.375 | nan |
| W1_INSIDE | 0.5 | full | 0.042 | 0.010 | 0.000 | 0.021 | 0.010 | 0.010 | nan |
| W1_INSIDE | 0.5 | mix:1/full@0 | 0.042 | 0.010 | 0.000 | 0.021 | 0.010 | 0.010 | nan |
| W1_INSIDE | 0.5 | mix:1/full@0.5 | 0.104 | 0.073 | 0.135 | 0.083 | 0.094 | 0.021 | 0.167 |
| W1_INSIDE | 0.5 | mix:1/full@0.75 | 0.104 | 0.125 | 0.177 | 0.177 | 0.156 | 0.000 | 0.208 |
| W1_INSIDE | 0.5 | mix:1/full@0.875 | 0.115 | 0.156 | 0.177 | 0.177 | 0.229 | 0.083 | 0.250 |
| W1_INSIDE | 0.5 | mix:1/full@1 | 0.146 | 0.208 | 0.271 | 0.354 | 0.375 | 0.375 | nan |

## Attempt lineage (raw records vs selected records)

An attempt = one run of an episode's arms in the append-only file. Resumed workers re-ran every episode that did not already have all arms valid. Selection: last attempt with all arms valid, else last attempt. 'episodes multi valid' counts episodes with more than one fully valid attempt (selection then takes the last one; see CORRECTIONS.md for the first-valid-attempt sensitivity check; this is NOT a first-observed-record analysis).

| world | dose | memory | episodes | attempts | episodes rerun | episodes multi valid | raw records | raw invalid | superseded records | selected records | selected valid | selected invalid | first observed valid |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| W1_INSIDE | 0.5 | 1 | 12 | 24 | 12 | 0 | 72 | 32 | 36 | 36 | 36 | 0 | 4 |
| W1_INSIDE | 0.5 | full | 12 | 21 | 9 | 0 | 63 | 23 | 27 | 36 | 35 | 1 | 14 |
| W1_INSIDE | 0.5 | mix:1/full@0.5 | 12 | 20 | 8 | 0 | 60 | 19 | 24 | 36 | 36 | 0 | 17 |
| W1_INSIDE | 0.5 | mix:1/full@0.75 | 12 | 21 | 9 | 0 | 63 | 22 | 27 | 36 | 35 | 1 | 14 |
| W1_INSIDE | 0.5 | mix:1/full@0.875 | 12 | 23 | 11 | 0 | 69 | 31 | 33 | 36 | 36 | 0 | 5 |
| **total** | | | **60** | **109** | **49** | **0** | **327** | **127** | **147** | **180** | **178** | **2** | **54** |

Retry accounting: 147 of 327 raw records were superseded by a later attempt (resume re-runs after provider errors or interrupted runs); 2 selected records are invalid and are counted in the 'inv' column, not dropped silently. Capture is decided before removal and shared by the arms.
