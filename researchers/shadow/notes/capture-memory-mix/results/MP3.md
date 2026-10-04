# capture-memory-mix: MP3 results

150 episode records, backends ['http:qwen/qwen3-235b-a22b-2507'], about 20818 model calls in these records; provider-reported spend on the shared ledger (all models, all pilot work) 3.3730 USD. Code commits: ['9d82e5ab', 'bd54bbed'].

Columns: captured = capture rate (shared by arms); frac@rem / frac_T = honest fraction on the original at removal and 50 rounds later (captured episodes); delta = frac_T minus frac@rem (0 = frozen, > 0 = returning); short_T / long_T = the same at round T split by memory kind; delta_long = return among the long-memory agents only.

## Cells (captured episodes unless noted)

| world | dose | memory | arm | n | inv | captured | lat | frac@rem | frac_T | delta | short_T | long_T | delta_long | recovered | half-time |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| W1_INSIDE | 0.5 | 1 | A0_no_purge | 6 | 6 | 1.00 | 2.0 | 0.104 | 0.188 | +0.083 | nan | 0.188 | +0.083 | 0.00 | 7 |
| W1_INSIDE | 0.5 | 1 | A1_purge | 3 | 9 | 1.00 | 2 | 0.125 | 0.583 | +0.458 | nan | 0.583 | +0.458 | 0.33 | 12.0 |
| W1_INSIDE | 0.5 | 1 | A2_purge_wipe | 4 | 8 | 1.00 | 2.0 | 0.094 | 0.469 | +0.375 | nan | 0.469 | +0.375 | 0.25 | 14.5 |
| W1_INSIDE | 0.5 | full | A0_no_purge | 3 | 6 | 1.00 | 11 | 0.083 | 0.000 | -0.083 | nan | 0.000 | -0.083 | 0.00 | None |
| W1_INSIDE | 0.5 | full | A1_purge | 3 | 6 | 1.00 | 11 | 0.083 | 0.000 | -0.083 | nan | 0.000 | -0.083 | 0.00 | None |
| W1_INSIDE | 0.5 | full | A2_purge_wipe | 2 | 7 | 1.00 | 10.0 | 0.000 | 0.000 | +0.000 | nan | 0.000 | +0.000 | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@0 | A0_no_purge | 3 | 0 | 1.00 | 11 | 0.083 | 0.000 | -0.083 | nan | 0.000 | -0.083 | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@0 | A1_purge | 3 | 0 | 1.00 | 11 | 0.083 | 0.000 | -0.083 | nan | 0.000 | -0.083 | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@0 | A2_purge_wipe | 2 | 0 | 1.00 | 10.0 | 0.000 | 0.000 | +0.000 | nan | 0.000 | +0.000 | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@0.5 | A0_no_purge | 4 | 4 | 1.00 | 9.5 | 0.125 | 0.062 | -0.062 | 0.125 | 0.000 | +0.000 | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@0.5 | A1_purge | 5 | 3 | 1.00 | 9 | 0.100 | 0.150 | +0.050 | 0.300 | 0.000 | +0.000 | 0.00 | 16 |
| W1_INSIDE | 0.5 | mix:1/full@0.5 | A2_purge_wipe | 3 | 5 | 1.00 | 9 | 0.125 | 0.167 | +0.042 | 0.250 | 0.083 | +0.083 | 0.00 | 13 |
| W1_INSIDE | 0.5 | mix:1/full@0.75 | A0_no_purge | 3 | 6 | 1.00 | 8 | 0.125 | 0.125 | +0.000 | 0.167 | 0.000 | +0.000 | 0.00 | 19 |
| W1_INSIDE | 0.5 | mix:1/full@0.75 | A1_purge | 5 | 4 | 1.00 | 7 | 0.125 | 0.200 | +0.075 | 0.267 | 0.000 | -0.100 | 0.00 | 17.5 |
| W1_INSIDE | 0.5 | mix:1/full@0.75 | A2_purge_wipe | 6 | 3 | 1.00 | 6.0 | 0.146 | 0.208 | +0.062 | 0.250 | 0.083 | -0.083 | 0.00 | 17.5 |
| W1_INSIDE | 0.5 | mix:1/full@0.875 | A0_no_purge | 4 | 8 | 1.00 | 5.0 | 0.094 | 0.125 | +0.031 | 0.143 | 0.000 | -0.250 | 0.00 | 19.5 |
| W1_INSIDE | 0.5 | mix:1/full@0.875 | A1_purge | 4 | 8 | 1.00 | 5.0 | 0.094 | 0.375 | +0.281 | 0.429 | 0.000 | -0.250 | 0.00 | 15 |
| W1_INSIDE | 0.5 | mix:1/full@0.875 | A2_purge_wipe | 5 | 7 | 1.00 | 3 | 0.075 | 0.400 | +0.325 | 0.429 | 0.200 | +0.000 | 0.00 | 14.0 |
| W1_INSIDE | 0.5 | mix:1/full@1 | A0_no_purge | 6 | 0 | 1.00 | 2.0 | 0.104 | 0.188 | +0.083 | nan | 0.188 | +0.083 | 0.00 | 7 |
| W1_INSIDE | 0.5 | mix:1/full@1 | A1_purge | 3 | 0 | 1.00 | 2 | 0.125 | 0.583 | +0.458 | nan | 0.583 | +0.458 | 0.33 | 12.0 |
| W1_INSIDE | 0.5 | mix:1/full@1 | A2_purge_wipe | 4 | 0 | 1.00 | 2.0 | 0.094 | 0.469 | +0.375 | nan | 0.469 | +0.375 | 0.25 | 14.5 |

## Contrasts over the short-memory fraction f (paired per draw, vs f = 0 of the same family; captured under both)

Declared primary: M1, W1_INSIDE, arm A1_purge, metric delta_original, family mix:1/full at dose 0.54, f = 0.5 minus f = 0.0. Everything else is exploratory.

| world | dose | family | arm | metric | f | mean(f) | mean(f=0) | diff | 95% CI | tasks | pairs |
|---|---|---|---|---|---|---|---|---|---|---|---|
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_original | 0.5 | 0.000 | -0.083 | +0.083 | [-0.125, +0.375] | 3 | 3 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_original | 0.75 | 0.125 | -0.083 | +0.208 | [-0.125, +0.625] | 3 | 3 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_original | 0.875 | 0.375 | -0.083 | +0.458 | [+0.125, +0.875] | 3 | 3 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_original | 1 | 0.458 | -0.083 | +0.542 | [+0.375, +0.750] | 3 | 3 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | frac_original_T | 0.5 | 0.125 | 0.000 | +0.125 | [+0.000, +0.250] | 3 | 3 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | frac_original_T | 0.75 | 0.250 | 0.000 | +0.250 | [+0.125, +0.500] | 3 | 3 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | frac_original_T | 0.875 | 0.417 | 0.000 | +0.417 | [+0.250, +0.625] | 3 | 3 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | frac_original_T | 1 | 0.583 | 0.000 | +0.583 | [+0.375, +0.750] | 3 | 3 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | long_T | 0.5 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | 3 | 3 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | long_T | 0.75 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | 3 | 3 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | long_T | 0.875 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | 3 | 3 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | long_T | 1 | 0.583 | 0.000 | +0.583 | [+0.375, +0.750] | 3 | 3 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_long | 0.5 | 0.000 | -0.083 | +0.083 | [+0.000, +0.250] | 3 | 3 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_long | 0.75 | 0.000 | -0.083 | +0.083 | [+0.000, +0.250] | 3 | 3 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_long | 0.875 | 0.000 | -0.083 | +0.083 | [+0.000, +0.250] | 3 | 3 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_long | 1 | 0.458 | -0.083 | +0.542 | [+0.375, +0.750] | 3 | 3 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_original | 0.5 | -0.062 | 0.000 | -0.062 | [-0.125, +0.000] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_original | 0.75 | 0.000 | 0.000 | +0.000 | [-0.125, +0.125] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_original | 0.875 | 0.312 | 0.000 | +0.312 | [+0.125, +0.500] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_original | 1 | 0.375 | 0.000 | +0.375 | [+0.375, +0.375] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | frac_original_T | 0.5 | 0.062 | 0.000 | +0.062 | [+0.000, +0.125] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | frac_original_T | 0.75 | 0.125 | 0.000 | +0.125 | [+0.125, +0.125] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | frac_original_T | 0.875 | 0.375 | 0.000 | +0.375 | [+0.250, +0.500] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | frac_original_T | 1 | 0.438 | 0.000 | +0.438 | [+0.375, +0.500] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | long_T | 0.5 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | long_T | 0.75 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | long_T | 0.875 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | long_T | 1 | 0.438 | 0.000 | +0.438 | [+0.375, +0.500] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_long | 0.5 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_long | 0.75 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_long | 0.875 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_long | 1 | 0.375 | 0.000 | +0.375 | [+0.375, +0.375] | 2 | 2 |

### Rescue threshold (design: smallest f with delta_original under A1_purge > +0.10 and CI lower bound > 0)

| world | dose | family | f* | delta at f* | CI lower |
|---|---|---|---|---|---|
| W1_INSIDE | 0.5 | mix:1/full | 0.875 | +0.375 | +0.125 |

## Wipe bridge: A2_purge_wipe minus A1_purge on frac_original_T, per cell (captured episodes, paired)

| world | dose | memory | mean wipe | mean purge | diff | 95% CI | tasks |
|---|---|---|---|---|---|---|---|
| W1_INSIDE | 0.5 | 1 | 0.542 | 0.583 | -0.042 | [-0.125, +0.000] | 3 |
| W1_INSIDE | 0.5 | full | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | 2 |
| W1_INSIDE | 0.5 | mix:1/full@0 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | 2 |
| W1_INSIDE | 0.5 | mix:1/full@0.5 | 0.167 | 0.125 | +0.042 | [+0.000, +0.125] | 3 |
| W1_INSIDE | 0.5 | mix:1/full@0.75 | 0.250 | 0.200 | +0.050 | [+0.000, +0.150] | 5 |
| W1_INSIDE | 0.5 | mix:1/full@0.875 | 0.438 | 0.375 | +0.062 | [-0.062, +0.188] | 4 |
| W1_INSIDE | 0.5 | mix:1/full@1 | 0.542 | 0.583 | -0.042 | [-0.125, +0.000] | 3 |

## Mean honest fraction on the original after removal, A1_purge, captured episodes (rounds 1, 5, 10, 20, 30, 50, 80 after removal)

| world | dose | memory | r1 | r5 | r10 | r20 | r30 | r50 | r80 | long r50 | short r50 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| W1_INSIDE | 0.5 | 1 | 0.167 | 0.292 | 0.375 | 0.375 | 0.583 | | | 0.458 | nan |
| W1_INSIDE | 0.5 | full | 0.083 | 0.000 | 0.000 | 0.042 | 0.000 | | | 0.000 | nan |
| W1_INSIDE | 0.5 | mix:1/full@0 | 0.083 | 0.000 | 0.000 | 0.042 | 0.000 | | | 0.000 | nan |
| W1_INSIDE | 0.5 | mix:1/full@0.5 | 0.100 | 0.025 | 0.100 | 0.075 | 0.150 | | | 0.050 | 0.200 |
| W1_INSIDE | 0.5 | mix:1/full@0.75 | 0.150 | 0.150 | 0.175 | 0.150 | 0.200 | | | 0.000 | 0.300 |
| W1_INSIDE | 0.5 | mix:1/full@0.875 | 0.125 | 0.219 | 0.219 | 0.312 | 0.375 | | | 0.000 | 0.321 |
| W1_INSIDE | 0.5 | mix:1/full@1 | 0.167 | 0.292 | 0.375 | 0.375 | 0.583 | | | 0.458 | nan |

Invalid episodes per cell and arm are in the CSV; none are dropped or retried. Capture is decided before removal and shared by the arms.
