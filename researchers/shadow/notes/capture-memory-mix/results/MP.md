# capture-memory-mix: MP results

255 episode records, backends ['http:openai/gpt-4o-mini'], about 63916 model calls in these records; provider-reported spend on the shared ledger (all models, all pilot work) 1.6230 USD. Code commits: ['016104d9', '3ffb56b6', '492d762f'].

Columns: captured = capture rate (shared by arms); frac@rem / frac_T = honest fraction on the original at removal and 50 rounds later (captured episodes); delta = frac_T minus frac@rem (0 = frozen, > 0 = returning); short_T / long_T = the same at round T split by memory kind; delta_long = return among the long-memory agents only.

## Cells (captured episodes unless noted)

| world | dose | memory | arm | n | inv | captured | lat | frac@rem | frac_T | delta | short_T | long_T | delta_long | recovered | half-time |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| W1_INSIDE | 0.5 | 1 | A0_no_purge | 11 | 1 | 1.00 | 2 | 0.034 | 0.000 | -0.034 | nan | 0.000 | -0.034 | 0.00 | None |
| W1_INSIDE | 0.5 | 1 | A1_purge | 12 | 0 | 1.00 | 2.0 | 0.031 | 0.031 | +0.000 | nan | 0.031 | +0.000 | 0.00 | None |
| W1_INSIDE | 0.5 | 1 | A2_purge_wipe | 12 | 0 | 1.00 | 2.0 | 0.031 | 0.031 | +0.000 | nan | 0.031 | +0.000 | 0.00 | None |
| W1_INSIDE | 0.5 | full | A0_no_purge | 10 | 4 | 0.90 | 20 | 0.153 | 0.167 | +0.014 | nan | 0.167 | +0.014 | 0.00 | 14.0 |
| W1_INSIDE | 0.5 | full | A1_purge | 10 | 4 | 0.90 | 20 | 0.153 | 0.278 | +0.125 | nan | 0.278 | +0.125 | 0.00 | 7.5 |
| W1_INSIDE | 0.5 | full | A2_purge_wipe | 10 | 4 | 0.90 | 20 | 0.153 | 0.000 | -0.153 | nan | 0.000 | -0.153 | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@0 | A0_no_purge | 10 | 0 | 0.90 | 20 | 0.153 | 0.167 | +0.014 | nan | 0.167 | +0.014 | 0.00 | 14.0 |
| W1_INSIDE | 0.5 | mix:1/full@0 | A1_purge | 10 | 0 | 0.90 | 20 | 0.153 | 0.278 | +0.125 | nan | 0.278 | +0.125 | 0.00 | 7.5 |
| W1_INSIDE | 0.5 | mix:1/full@0 | A2_purge_wipe | 10 | 0 | 0.90 | 20 | 0.153 | 0.000 | -0.153 | nan | 0.000 | -0.153 | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@0.5 | A0_no_purge | 12 | 0 | 1.00 | 13.0 | 0.083 | 0.094 | +0.010 | 0.021 | 0.167 | +0.062 | 0.00 | 18.5 |
| W1_INSIDE | 0.5 | mix:1/full@0.5 | A1_purge | 12 | 0 | 1.00 | 13.0 | 0.083 | 0.146 | +0.062 | 0.125 | 0.167 | +0.062 | 0.00 | 9 |
| W1_INSIDE | 0.5 | mix:1/full@0.5 | A2_purge_wipe | 12 | 0 | 1.00 | 13.0 | 0.083 | 0.000 | -0.083 | 0.000 | 0.000 | -0.104 | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@0.625 | A0_no_purge | 11 | 0 | 1.00 | 10 | 0.114 | 0.102 | -0.011 | 0.073 | 0.151 | -0.091 | 0.00 | 27 |
| W1_INSIDE | 0.5 | mix:1/full@0.625 | A1_purge | 11 | 0 | 1.00 | 10 | 0.114 | 0.318 | +0.204 | 0.327 | 0.303 | +0.061 | 0.09 | 8.5 |
| W1_INSIDE | 0.5 | mix:1/full@0.625 | A2_purge_wipe | 11 | 0 | 1.00 | 10 | 0.114 | 0.000 | -0.114 | 0.000 | 0.000 | -0.242 | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@0.75 | A0_no_purge | 12 | 0 | 1.00 | 7.5 | 0.125 | 0.094 | -0.031 | 0.056 | 0.208 | -0.167 | 0.00 | 1.5 |
| W1_INSIDE | 0.5 | mix:1/full@0.75 | A1_purge | 12 | 0 | 1.00 | 7.5 | 0.125 | 0.344 | +0.219 | 0.333 | 0.375 | +0.000 | 0.25 | 5.0 |
| W1_INSIDE | 0.5 | mix:1/full@0.75 | A2_purge_wipe | 12 | 0 | 1.00 | 7.5 | 0.125 | 0.010 | -0.115 | 0.014 | 0.000 | -0.375 | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@0.875 | A0_no_purge | 12 | 0 | 1.00 | 2.5 | 0.156 | 0.031 | -0.125 | 0.024 | 0.083 | -0.500 | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@0.875 | A1_purge | 12 | 0 | 1.00 | 2.5 | 0.156 | 0.385 | +0.229 | 0.381 | 0.417 | -0.167 | 0.17 | 7 |
| W1_INSIDE | 0.5 | mix:1/full@0.875 | A2_purge_wipe | 12 | 0 | 1.00 | 2.5 | 0.156 | 0.010 | -0.146 | 0.012 | 0.000 | -0.583 | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@0.9375 | A0_no_purge | 12 | 0 | 1.00 | 2.0 | 0.031 | 0.000 | -0.031 | 0.000 | nan | +nan | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@0.9375 | A1_purge | 12 | 0 | 1.00 | 2.0 | 0.031 | 0.031 | +0.000 | 0.031 | nan | +nan | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@0.9375 | A2_purge_wipe | 12 | 0 | 1.00 | 2.0 | 0.031 | 0.031 | +0.000 | 0.031 | nan | +nan | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@1 | A0_no_purge | 11 | 0 | 1.00 | 2 | 0.034 | 0.000 | -0.034 | nan | 0.000 | -0.034 | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@1 | A1_purge | 12 | 0 | 1.00 | 2.0 | 0.031 | 0.031 | +0.000 | nan | 0.031 | +0.000 | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@1 | A2_purge_wipe | 12 | 0 | 1.00 | 2.0 | 0.031 | 0.031 | +0.000 | nan | 0.031 | +0.000 | 0.00 | None |

## Contrasts over the short-memory fraction f (paired per draw, vs f = 0 of the same family; captured under both)

Declared primary: M1, W1_INSIDE, arm A1_purge, metric delta_original, family mix:1/full at dose 0.54, f = 0.5 minus f = 0.0. Everything else is exploratory.

| world | dose | family | arm | metric | f | mean(f) | mean(f=0) | diff | 95% CI | tasks | pairs |
|---|---|---|---|---|---|---|---|---|---|---|---|
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_original | 0.5 | 0.083 | 0.125 | -0.042 | [-0.139, +0.056] | 9 | 9 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_original | 0.625 | 0.188 | 0.109 | +0.078 | [-0.094, +0.250] | 8 | 8 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_original | 0.75 | 0.181 | 0.125 | +0.056 | [-0.125, +0.264] | 9 | 9 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_original | 0.875 | 0.153 | 0.125 | +0.028 | [-0.125, +0.194] | 9 | 9 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_original | 0.9375 | 0.000 | 0.125 | -0.125 | [-0.181, -0.069] | 9 | 9 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_original | 1 | 0.000 | 0.125 | -0.125 | [-0.181, -0.069] | 9 | 9 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | frac_original_T | 0.5 | 0.167 | 0.278 | -0.111 | [-0.194, -0.028] | 9 | 9 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | frac_original_T | 0.625 | 0.297 | 0.266 | +0.031 | [-0.156, +0.234] | 8 | 8 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | frac_original_T | 0.75 | 0.319 | 0.278 | +0.042 | [-0.181, +0.292] | 9 | 9 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | frac_original_T | 0.875 | 0.292 | 0.278 | +0.014 | [-0.153, +0.153] | 9 | 9 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | frac_original_T | 0.9375 | 0.028 | 0.278 | -0.250 | [-0.347, -0.139] | 9 | 9 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | frac_original_T | 1 | 0.028 | 0.278 | -0.250 | [-0.347, -0.139] | 9 | 9 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | long_T | 0.5 | 0.222 | 0.278 | -0.056 | [-0.181, +0.069] | 9 | 9 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | long_T | 0.625 | 0.250 | 0.266 | -0.016 | [-0.219, +0.182] | 8 | 8 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | long_T | 0.75 | 0.333 | 0.278 | +0.056 | [-0.222, +0.347] | 9 | 9 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | long_T | 0.875 | 0.333 | 0.278 | +0.056 | [-0.250, +0.375] | 9 | 9 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | long_T | 1 | 0.028 | 0.278 | -0.250 | [-0.347, -0.139] | 9 | 9 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_long | 0.5 | 0.083 | 0.125 | -0.042 | [-0.167, +0.083] | 9 | 9 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_long | 0.625 | 0.000 | 0.109 | -0.109 | [-0.240, +0.047] | 8 | 8 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_long | 0.75 | -0.056 | 0.125 | -0.181 | [-0.444, +0.097] | 9 | 9 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_long | 0.875 | -0.111 | 0.125 | -0.236 | [-0.681, +0.194] | 9 | 9 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_long | 1 | 0.000 | 0.125 | -0.125 | [-0.181, -0.069] | 9 | 9 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | half_time | 0.5 | 8.000 | 7.333 | +0.667 | [-4.000, +8.000] | 3 | 3 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | half_time | 0.625 | 18.000 | 7.333 | +10.667 | [+2.000, +23.000] | 3 | 3 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | half_time | 0.75 | 20.000 | 11.000 | +9.000 | [-5.000, +23.000] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | half_time | 0.875 | 13.000 | 7.500 | +5.500 | [-3.750, +11.750] | 4 | 4 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_original | 0.5 | -0.083 | -0.153 | +0.069 | [+0.014, +0.125] | 9 | 9 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_original | 0.625 | -0.109 | -0.156 | +0.047 | [-0.062, +0.156] | 8 | 8 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_original | 0.75 | -0.125 | -0.153 | +0.028 | [-0.069, +0.111] | 9 | 9 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_original | 0.875 | -0.125 | -0.153 | +0.028 | [-0.042, +0.097] | 9 | 9 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_original | 0.9375 | 0.000 | -0.153 | +0.153 | [+0.083, +0.222] | 9 | 9 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_original | 1 | 0.000 | -0.153 | +0.153 | [+0.083, +0.222] | 9 | 9 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | frac_original_T | 0.5 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | 9 | 9 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | frac_original_T | 0.625 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | 8 | 8 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | frac_original_T | 0.75 | 0.014 | 0.000 | +0.014 | [+0.000, +0.042] | 9 | 9 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | frac_original_T | 0.875 | 0.014 | 0.000 | +0.014 | [+0.000, +0.042] | 9 | 9 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | frac_original_T | 0.9375 | 0.028 | 0.000 | +0.028 | [+0.000, +0.069] | 9 | 9 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | frac_original_T | 1 | 0.028 | 0.000 | +0.028 | [+0.000, +0.069] | 9 | 9 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | long_T | 0.5 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | 9 | 9 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | long_T | 0.625 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | 8 | 8 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | long_T | 0.75 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | 9 | 9 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | long_T | 0.875 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | 9 | 9 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | long_T | 1 | 0.028 | 0.000 | +0.028 | [+0.000, +0.069] | 9 | 9 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_long | 0.5 | -0.139 | -0.153 | +0.014 | [-0.069, +0.097] | 9 | 9 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_long | 0.625 | -0.250 | -0.156 | -0.094 | [-0.260, +0.073] | 8 | 8 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_long | 0.75 | -0.389 | -0.153 | -0.236 | [-0.486, +0.000] | 9 | 9 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_long | 0.875 | -0.444 | -0.153 | -0.292 | [-0.639, +0.042] | 9 | 9 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_long | 1 | 0.000 | -0.153 | +0.153 | [+0.083, +0.222] | 9 | 9 |

### Rescue threshold (design: smallest f with delta_original under A1_purge > +0.10 and CI lower bound > 0)

| world | dose | family | f* | delta at f* | CI lower |
|---|---|---|---|---|---|
| W1_INSIDE | 0.5 | mix:1/full | 0.625 | +0.188 | +0.031 |

## Wipe bridge: A2_purge_wipe minus A1_purge on frac_original_T, per cell (captured episodes, paired)

| world | dose | memory | mean wipe | mean purge | diff | 95% CI | tasks |
|---|---|---|---|---|---|---|---|
| W1_INSIDE | 0.5 | 1 | 0.031 | 0.031 | +0.000 | [+0.000, +0.000] | 12 |
| W1_INSIDE | 0.5 | full | 0.000 | 0.278 | -0.278 | [-0.375, -0.167] | 9 |
| W1_INSIDE | 0.5 | mix:1/full@0 | 0.000 | 0.278 | -0.278 | [-0.375, -0.167] | 9 |
| W1_INSIDE | 0.5 | mix:1/full@0.5 | 0.000 | 0.146 | -0.146 | [-0.219, -0.073] | 12 |
| W1_INSIDE | 0.5 | mix:1/full@0.625 | 0.000 | 0.318 | -0.318 | [-0.511, -0.148] | 11 |
| W1_INSIDE | 0.5 | mix:1/full@0.75 | 0.010 | 0.344 | -0.333 | [-0.542, -0.156] | 12 |
| W1_INSIDE | 0.5 | mix:1/full@0.875 | 0.010 | 0.385 | -0.375 | [-0.573, -0.198] | 12 |
| W1_INSIDE | 0.5 | mix:1/full@0.9375 | 0.031 | 0.031 | +0.000 | [+0.000, +0.000] | 12 |
| W1_INSIDE | 0.5 | mix:1/full@1 | 0.031 | 0.031 | +0.000 | [+0.000, +0.000] | 12 |

## Mean honest fraction on the original after removal, A1_purge, captured episodes (rounds 1, 5, 10, 20, 30, 50, 80 after removal)

| world | dose | memory | r1 | r5 | r10 | r20 | r30 | r50 | r80 | long r50 | short r50 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| W1_INSIDE | 0.5 | 1 | 0.031 | 0.031 | 0.031 | 0.031 | 0.031 | | | 0.031 | nan |
| W1_INSIDE | 0.5 | full | 0.181 | 0.222 | 0.222 | 0.167 | 0.278 | | | 0.250 | nan |
| W1_INSIDE | 0.5 | mix:1/full@0 | 0.181 | 0.222 | 0.222 | 0.167 | 0.278 | | | 0.250 | nan |
| W1_INSIDE | 0.5 | mix:1/full@0.5 | 0.104 | 0.188 | 0.198 | 0.135 | 0.146 | | | 0.292 | 0.104 |
| W1_INSIDE | 0.5 | mix:1/full@0.625 | 0.170 | 0.250 | 0.250 | 0.239 | 0.318 | | | 0.242 | 0.291 |
| W1_INSIDE | 0.5 | mix:1/full@0.75 | 0.167 | 0.281 | 0.281 | 0.281 | 0.344 | | | 0.375 | 0.347 |
| W1_INSIDE | 0.5 | mix:1/full@0.875 | 0.177 | 0.250 | 0.354 | 0.375 | 0.385 | | | 0.333 | 0.417 |
| W1_INSIDE | 0.5 | mix:1/full@0.9375 | 0.031 | 0.031 | 0.031 | 0.031 | 0.031 | | | nan | 0.031 |
| W1_INSIDE | 0.5 | mix:1/full@1 | 0.031 | 0.031 | 0.031 | 0.031 | 0.031 | | | 0.031 | nan |

Invalid episodes per cell and arm are in the CSV; none are dropped or retried. Capture is decided before removal and shared by the arms.
