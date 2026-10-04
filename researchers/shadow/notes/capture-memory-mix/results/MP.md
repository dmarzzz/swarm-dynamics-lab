# capture-memory-mix: MP results

48 episode records, backends ['http:openai/gpt-4o-mini'], about 13100 model calls in these records; provider-reported spend on the shared ledger (all models, all pilot work) 0.3410 USD. Code commits: ['492d762f'].

Columns: captured = capture rate (shared by arms); frac@rem / frac_T = honest fraction on the original at removal and 50 rounds later (captured episodes); delta = frac_T minus frac@rem (0 = frozen, > 0 = returning); short_T / long_T = the same at round T split by memory kind; delta_long = return among the long-memory agents only.

## Cells (captured episodes unless noted)

| world | dose | memory | arm | n | inv | captured | lat | frac@rem | frac_T | delta | short_T | long_T | delta_long | recovered | half-time |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| W1_INSIDE | 0.5 | 1 | A0_no_purge | 3 | 0 | 1.00 | 2 | 0.000 | 0.000 | +0.000 | nan | 0.000 | +0.000 | 0.00 | None |
| W1_INSIDE | 0.5 | 1 | A1_purge | 3 | 0 | 1.00 | 2 | 0.000 | 0.000 | +0.000 | nan | 0.000 | +0.000 | 0.00 | None |
| W1_INSIDE | 0.5 | 1 | A2_purge_wipe | 3 | 0 | 1.00 | 2 | 0.000 | 0.000 | +0.000 | nan | 0.000 | +0.000 | 0.00 | None |
| W1_INSIDE | 0.5 | full | A0_no_purge | 3 | 0 | 0.67 | 37.0 | 0.250 | 0.125 | -0.125 | nan | 0.125 | -0.125 | 0.00 | 13.5 |
| W1_INSIDE | 0.5 | full | A1_purge | 3 | 0 | 0.67 | 37.0 | 0.250 | 0.375 | +0.125 | nan | 0.375 | +0.125 | 0.00 | 11.0 |
| W1_INSIDE | 0.5 | full | A2_purge_wipe | 3 | 0 | 0.67 | 37.0 | 0.250 | 0.000 | -0.250 | nan | 0.000 | -0.250 | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@0 | A0_no_purge | 3 | 0 | 0.67 | 37.0 | 0.250 | 0.125 | -0.125 | nan | 0.125 | -0.125 | 0.00 | 13.5 |
| W1_INSIDE | 0.5 | mix:1/full@0 | A1_purge | 3 | 0 | 0.67 | 37.0 | 0.250 | 0.375 | +0.125 | nan | 0.375 | +0.125 | 0.00 | 11.0 |
| W1_INSIDE | 0.5 | mix:1/full@0 | A2_purge_wipe | 3 | 0 | 0.67 | 37.0 | 0.250 | 0.000 | -0.250 | nan | 0.000 | -0.250 | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@0.5 | A0_no_purge | 3 | 0 | 1.00 | 16 | 0.125 | 0.042 | -0.083 | 0.000 | 0.083 | +0.000 | 0.00 | 8 |
| W1_INSIDE | 0.5 | mix:1/full@0.5 | A1_purge | 3 | 0 | 1.00 | 16 | 0.125 | 0.250 | +0.125 | 0.417 | 0.083 | +0.000 | 0.00 | 7.0 |
| W1_INSIDE | 0.5 | mix:1/full@0.5 | A2_purge_wipe | 3 | 0 | 1.00 | 16 | 0.125 | 0.000 | -0.125 | 0.000 | 0.000 | -0.083 | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@0.75 | A0_no_purge | 3 | 0 | 1.00 | 5 | 0.208 | 0.125 | -0.083 | 0.111 | 0.167 | -0.333 | 0.00 | 2 |
| W1_INSIDE | 0.5 | mix:1/full@0.75 | A1_purge | 3 | 0 | 1.00 | 5 | 0.208 | 0.750 | +0.542 | 0.722 | 0.833 | +0.333 | 0.67 | 6 |
| W1_INSIDE | 0.5 | mix:1/full@0.75 | A2_purge_wipe | 3 | 0 | 1.00 | 5 | 0.208 | 0.042 | -0.167 | 0.056 | 0.000 | -0.500 | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@0.875 | A0_no_purge | 4 | 0 | 1.00 | 3.0 | 0.156 | 0.062 | -0.094 | 0.071 | 0.000 | -0.500 | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@0.875 | A1_purge | 4 | 0 | 1.00 | 3.0 | 0.156 | 0.625 | +0.469 | 0.607 | 0.750 | +0.250 | 0.25 | 10.0 |
| W1_INSIDE | 0.5 | mix:1/full@0.875 | A2_purge_wipe | 4 | 0 | 1.00 | 3.0 | 0.156 | 0.000 | -0.156 | 0.000 | 0.000 | -0.500 | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@1 | A0_no_purge | 3 | 0 | 1.00 | 2 | 0.000 | 0.000 | +0.000 | nan | 0.000 | +0.000 | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@1 | A1_purge | 3 | 0 | 1.00 | 2 | 0.000 | 0.000 | +0.000 | nan | 0.000 | +0.000 | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@1 | A2_purge_wipe | 3 | 0 | 1.00 | 2 | 0.000 | 0.000 | +0.000 | nan | 0.000 | +0.000 | 0.00 | None |

## Contrasts over the short-memory fraction f (paired per draw, vs f = 0 of the same family; captured under both)

Declared primary: M1, W1_INSIDE, arm A1_purge, metric delta_original, family mix:1/full at dose 0.54, f = 0.5 minus f = 0.0. Everything else is exploratory.

| world | dose | family | arm | metric | f | mean(f) | mean(f=0) | diff | 95% CI | tasks | pairs |
|---|---|---|---|---|---|---|---|---|---|---|---|
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_original | 0.5 | 0.125 | 0.125 | +0.000 | [-0.125, +0.125] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_original | 0.75 | 0.375 | 0.125 | +0.250 | [-0.125, +0.625] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_original | 0.875 | 0.562 | 0.125 | +0.438 | [+0.375, +0.500] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_original | 1 | 0.000 | 0.125 | -0.125 | [-0.125, -0.125] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | frac_original_T | 0.5 | 0.250 | 0.375 | -0.125 | [-0.125, -0.125] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | frac_original_T | 0.75 | 0.625 | 0.375 | +0.250 | [-0.125, +0.625] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | frac_original_T | 0.875 | 0.688 | 0.375 | +0.312 | [+0.250, +0.375] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | frac_original_T | 1 | 0.000 | 0.375 | -0.375 | [-0.375, -0.375] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | long_T | 0.5 | 0.125 | 0.375 | -0.250 | [-0.375, -0.125] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | long_T | 0.75 | 0.750 | 0.375 | +0.375 | [+0.125, +0.625] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | long_T | 0.875 | 1.000 | 0.375 | +0.625 | [+0.625, +0.625] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | long_T | 1 | 0.000 | 0.375 | -0.375 | [-0.375, -0.375] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_long | 0.5 | 0.000 | 0.125 | -0.125 | [-0.375, +0.125] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_long | 0.75 | 0.250 | 0.125 | +0.125 | [-0.125, +0.375] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_long | 0.875 | 1.000 | 0.125 | +0.875 | [+0.875, +0.875] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_long | 1 | 0.000 | 0.125 | -0.125 | [-0.125, -0.125] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | half_time | 0.5 | 9.000 | 11.000 | -2.000 | [-2.000, -2.000] | 1 | 1 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | half_time | 0.75 | 20.000 | 11.000 | +9.000 | [-5.000, +23.000] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | half_time | 0.875 | 11.500 | 11.000 | +0.500 | [-8.000, +9.000] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_original | 0.5 | -0.125 | -0.250 | +0.125 | [+0.000, +0.250] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_original | 0.75 | -0.188 | -0.250 | +0.062 | [+0.000, +0.125] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_original | 0.875 | -0.125 | -0.250 | +0.125 | [+0.125, +0.125] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_original | 1 | 0.000 | -0.250 | +0.250 | [+0.250, +0.250] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | frac_original_T | 0.5 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | frac_original_T | 0.75 | 0.062 | 0.000 | +0.062 | [+0.000, +0.125] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | frac_original_T | 0.875 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | frac_original_T | 1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | long_T | 0.5 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | long_T | 0.75 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | long_T | 0.875 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | long_T | 1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_long | 0.5 | -0.125 | -0.250 | +0.125 | [+0.000, +0.250] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_long | 0.75 | -0.500 | -0.250 | -0.250 | [-0.250, -0.250] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_long | 0.875 | 0.000 | -0.250 | +0.250 | [+0.250, +0.250] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_long | 1 | 0.000 | -0.250 | +0.250 | [+0.250, +0.250] | 2 | 2 |

### Rescue threshold (design: smallest f with delta_original under A1_purge > +0.10 and CI lower bound > 0)

| world | dose | family | f* | delta at f* | CI lower |
|---|---|---|---|---|---|
| W1_INSIDE | 0.5 | mix:1/full | 0.875 | +0.562 | +0.500 |

## Wipe bridge: A2_purge_wipe minus A1_purge on frac_original_T, per cell (captured episodes, paired)

| world | dose | memory | mean wipe | mean purge | diff | 95% CI | tasks |
|---|---|---|---|---|---|---|---|
| W1_INSIDE | 0.5 | 1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | 3 |
| W1_INSIDE | 0.5 | full | 0.000 | 0.375 | -0.375 | [-0.375, -0.375] | 2 |
| W1_INSIDE | 0.5 | mix:1/full@0 | 0.000 | 0.375 | -0.375 | [-0.375, -0.375] | 2 |
| W1_INSIDE | 0.5 | mix:1/full@0.5 | 0.000 | 0.250 | -0.250 | [-0.250, -0.250] | 3 |
| W1_INSIDE | 0.5 | mix:1/full@0.75 | 0.042 | 0.750 | -0.708 | [-1.000, -0.250] | 3 |
| W1_INSIDE | 0.5 | mix:1/full@0.875 | 0.000 | 0.625 | -0.625 | [-0.906, -0.281] | 4 |
| W1_INSIDE | 0.5 | mix:1/full@1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | 3 |

## Mean honest fraction on the original after removal, A1_purge, captured episodes (rounds 1, 5, 10, 20, 30, 50, 80 after removal)

| world | dose | memory | r1 | r5 | r10 | r20 | r30 | r50 | r80 | long r50 | short r50 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| W1_INSIDE | 0.5 | 1 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | | | 0.000 | nan |
| W1_INSIDE | 0.5 | full | 0.250 | 0.312 | 0.312 | 0.188 | 0.375 | | | 0.312 | nan |
| W1_INSIDE | 0.5 | mix:1/full@0 | 0.250 | 0.312 | 0.312 | 0.188 | 0.375 | | | 0.312 | nan |
| W1_INSIDE | 0.5 | mix:1/full@0.5 | 0.167 | 0.292 | 0.333 | 0.333 | 0.250 | | | 0.333 | 0.167 |
| W1_INSIDE | 0.5 | mix:1/full@0.75 | 0.208 | 0.375 | 0.500 | 0.625 | 0.750 | | | 0.833 | 0.778 |
| W1_INSIDE | 0.5 | mix:1/full@0.875 | 0.188 | 0.344 | 0.438 | 0.531 | 0.625 | | | 0.750 | 0.643 |
| W1_INSIDE | 0.5 | mix:1/full@1 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | | | 0.000 | nan |

Invalid episodes per cell and arm are in the CSV; none are dropped or retried. Capture is decided before removal and shared by the arms.
