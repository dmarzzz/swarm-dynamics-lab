# capture-memory-mix: MP results

426 episode records, backends ['http:openai/gpt-4o-mini'], about 111832 model calls in these records; provider-reported spend on the shared ledger (all models, all pilot work) 3.3727 USD. Code commits: ['016104d9', '3ffb56b6', '492d762f'].

Columns: captured = capture rate (shared by arms); frac@rem / frac_T = honest fraction on the original at removal and 50 rounds later (captured episodes); delta = frac_T minus frac@rem (0 = frozen, > 0 = returning); short_T / long_T = the same at round T split by memory kind; delta_long = return among the long-memory agents only.

## Cells (captured episodes unless noted)

| world | dose | memory | arm | n | inv | captured | lat | frac@rem | frac_T | delta | short_T | long_T | delta_long | recovered | half-time |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| W1_INSIDE | 0.5 | 1 | A0_no_purge | 24 | 0 | 1.00 | 2.0 | 0.047 | 0.000 | -0.047 | nan | 0.000 | -0.047 | 0.00 | None |
| W1_INSIDE | 0.5 | 1 | A1_purge | 24 | 0 | 1.00 | 2.0 | 0.047 | 0.047 | +0.000 | nan | 0.047 | +0.000 | 0.00 | None |
| W1_INSIDE | 0.5 | 1 | A2_purge_wipe | 24 | 0 | 1.00 | 2.0 | 0.047 | 0.047 | +0.000 | nan | 0.047 | +0.000 | 0.00 | None |
| W1_INSIDE | 0.5 | full | A0_no_purge | 22 | 0 | 0.86 | 18 | 0.145 | 0.165 | +0.020 | nan | 0.165 | +0.020 | 0.00 | 13 |
| W1_INSIDE | 0.5 | full | A1_purge | 22 | 0 | 0.86 | 18 | 0.145 | 0.224 | +0.079 | nan | 0.224 | +0.079 | 0.00 | 8.5 |
| W1_INSIDE | 0.5 | full | A2_purge_wipe | 22 | 0 | 0.86 | 18 | 0.145 | 0.020 | -0.125 | nan | 0.020 | -0.125 | 0.00 | 4 |
| W1_INSIDE | 0.5 | mix:1/full@0 | A0_no_purge | 22 | 0 | 0.86 | 18 | 0.145 | 0.165 | +0.020 | nan | 0.165 | +0.020 | 0.00 | 13 |
| W1_INSIDE | 0.5 | mix:1/full@0 | A1_purge | 22 | 0 | 0.86 | 18 | 0.145 | 0.224 | +0.079 | nan | 0.224 | +0.079 | 0.00 | 8.5 |
| W1_INSIDE | 0.5 | mix:1/full@0 | A2_purge_wipe | 22 | 0 | 0.86 | 18 | 0.145 | 0.020 | -0.125 | nan | 0.020 | -0.125 | 0.00 | 4 |
| W1_INSIDE | 0.5 | mix:1/full@0.5 | A0_no_purge | 24 | 0 | 1.00 | 10.5 | 0.094 | 0.115 | +0.021 | 0.021 | 0.208 | +0.083 | 0.00 | 22 |
| W1_INSIDE | 0.5 | mix:1/full@0.5 | A1_purge | 24 | 0 | 1.00 | 10.5 | 0.094 | 0.167 | +0.073 | 0.135 | 0.198 | +0.073 | 0.00 | 9.0 |
| W1_INSIDE | 0.5 | mix:1/full@0.5 | A2_purge_wipe | 24 | 0 | 1.00 | 10.5 | 0.094 | 0.000 | -0.094 | 0.000 | 0.000 | -0.125 | 0.00 | 3 |
| W1_INSIDE | 0.5 | mix:1/full@0.625 | A0_no_purge | 12 | 0 | 1.00 | 10.0 | 0.104 | 0.115 | +0.010 | 0.100 | 0.139 | -0.083 | 0.00 | 27 |
| W1_INSIDE | 0.5 | mix:1/full@0.625 | A1_purge | 12 | 0 | 1.00 | 10.0 | 0.104 | 0.312 | +0.208 | 0.317 | 0.305 | +0.083 | 0.08 | 8.5 |
| W1_INSIDE | 0.5 | mix:1/full@0.625 | A2_purge_wipe | 12 | 0 | 1.00 | 10.0 | 0.104 | 0.000 | -0.104 | 0.000 | 0.000 | -0.222 | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@0.75 | A0_no_purge | 24 | 0 | 1.00 | 7.0 | 0.130 | 0.094 | -0.036 | 0.035 | 0.271 | -0.062 | 0.00 | 3.5 |
| W1_INSIDE | 0.5 | mix:1/full@0.75 | A1_purge | 24 | 0 | 1.00 | 7.0 | 0.130 | 0.339 | +0.208 | 0.320 | 0.396 | +0.062 | 0.21 | 6.5 |
| W1_INSIDE | 0.5 | mix:1/full@0.75 | A2_purge_wipe | 24 | 0 | 1.00 | 7.0 | 0.130 | 0.016 | -0.115 | 0.021 | 0.000 | -0.333 | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@0.875 | A0_no_purge | 24 | 0 | 1.00 | 2.5 | 0.146 | 0.052 | -0.094 | 0.030 | 0.208 | -0.417 | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@0.875 | A1_purge | 24 | 0 | 1.00 | 2.5 | 0.146 | 0.391 | +0.245 | 0.381 | 0.458 | -0.167 | 0.12 | 8.5 |
| W1_INSIDE | 0.5 | mix:1/full@0.875 | A2_purge_wipe | 24 | 0 | 1.00 | 2.5 | 0.146 | 0.016 | -0.130 | 0.018 | 0.000 | -0.625 | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@0.9375 | A0_no_purge | 12 | 0 | 1.00 | 2.0 | 0.031 | 0.000 | -0.031 | 0.000 | nan | +nan | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@0.9375 | A1_purge | 12 | 0 | 1.00 | 2.0 | 0.031 | 0.031 | +0.000 | 0.031 | nan | +nan | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@0.9375 | A2_purge_wipe | 12 | 0 | 1.00 | 2.0 | 0.031 | 0.031 | +0.000 | 0.031 | nan | +nan | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@1 | A0_no_purge | 24 | 0 | 1.00 | 2.0 | 0.047 | 0.000 | -0.047 | nan | 0.000 | -0.047 | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@1 | A1_purge | 24 | 0 | 1.00 | 2.0 | 0.047 | 0.047 | +0.000 | nan | 0.047 | +0.000 | 0.00 | None |
| W1_INSIDE | 0.5 | mix:1/full@1 | A2_purge_wipe | 24 | 0 | 1.00 | 2.0 | 0.047 | 0.047 | +0.000 | nan | 0.047 | +0.000 | 0.00 | None |

## Contrasts over the short-memory fraction f (paired per draw, vs f = 0 of the same family; captured under both)

Declared primary: M1, W1_INSIDE, arm A1_purge, metric delta_original, family mix:1/full at dose 0.54, f = 0.5 minus f = 0.0. Everything else is exploratory.

| world | dose | family | arm | metric | f | mean(f) | mean(f=0) | diff | 95% CI | tasks | pairs |
|---|---|---|---|---|---|---|---|---|---|---|---|
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_original | 0.5 | 0.053 | 0.079 | -0.026 | [-0.118, +0.059] | 19 | 19 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_original | 0.625 | 0.148 | 0.057 | +0.091 | [-0.011, +0.216] | 11 | 11 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_original | 0.75 | 0.112 | 0.079 | +0.033 | [-0.105, +0.191] | 19 | 19 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_original | 0.875 | 0.197 | 0.079 | +0.118 | [-0.026, +0.263] | 19 | 19 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_original | 0.9375 | 0.000 | 0.057 | -0.057 | [-0.136, +0.034] | 11 | 11 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_original | 1 | 0.000 | 0.079 | -0.079 | [-0.138, -0.020] | 19 | 19 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | frac_original_T | 0.5 | 0.145 | 0.224 | -0.079 | [-0.158, +0.013] | 19 | 19 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | frac_original_T | 0.625 | 0.250 | 0.239 | +0.011 | [-0.125, +0.159] | 11 | 11 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | frac_original_T | 0.75 | 0.230 | 0.224 | +0.007 | [-0.132, +0.171] | 19 | 19 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | frac_original_T | 0.875 | 0.355 | 0.224 | +0.132 | [+0.000, +0.257] | 19 | 19 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | frac_original_T | 0.9375 | 0.034 | 0.239 | -0.205 | [-0.307, -0.091] | 11 | 11 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | frac_original_T | 1 | 0.039 | 0.224 | -0.184 | [-0.257, -0.099] | 19 | 19 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | long_T | 0.5 | 0.197 | 0.224 | -0.026 | [-0.132, +0.099] | 19 | 19 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | long_T | 0.625 | 0.242 | 0.239 | +0.004 | [-0.148, +0.148] | 11 | 11 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | long_T | 0.75 | 0.289 | 0.224 | +0.066 | [-0.112, +0.270] | 19 | 19 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | long_T | 0.875 | 0.368 | 0.224 | +0.145 | [-0.059, +0.362] | 19 | 19 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | long_T | 1 | 0.039 | 0.224 | -0.184 | [-0.257, -0.099] | 19 | 19 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_long | 0.5 | 0.079 | 0.079 | +0.000 | [-0.125, +0.118] | 19 | 19 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_long | 0.625 | 0.030 | 0.057 | -0.027 | [-0.167, +0.110] | 11 | 11 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_long | 0.75 | 0.000 | 0.079 | -0.079 | [-0.276, +0.132] | 19 | 19 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_long | 0.875 | -0.211 | 0.079 | -0.289 | [-0.599, +0.033] | 19 | 19 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_long | 1 | 0.000 | 0.079 | -0.079 | [-0.138, -0.020] | 19 | 19 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | half_time | 0.5 | 8.000 | 8.667 | -0.667 | [-8.000, +8.000] | 3 | 3 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | half_time | 0.625 | 14.500 | 7.500 | +7.000 | [+1.000, +14.750] | 4 | 4 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | half_time | 0.75 | 20.000 | 11.000 | +9.000 | [-5.000, +23.000] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | half_time | 0.875 | 9.857 | 7.143 | +2.714 | [-2.286, +7.714] | 7 | 7 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_original | 0.5 | -0.092 | -0.125 | +0.033 | [-0.039, +0.099] | 19 | 19 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_original | 0.625 | -0.102 | -0.182 | +0.080 | [+0.000, +0.148] | 11 | 11 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_original | 0.75 | -0.105 | -0.125 | +0.020 | [-0.039, +0.079] | 19 | 19 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_original | 0.875 | -0.138 | -0.125 | -0.013 | [-0.079, +0.039] | 19 | 19 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_original | 0.9375 | 0.000 | -0.182 | +0.182 | [+0.125, +0.239] | 11 | 11 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_original | 1 | 0.000 | -0.125 | +0.125 | [+0.072, +0.178] | 19 | 19 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | frac_original_T | 0.5 | 0.000 | 0.020 | -0.020 | [-0.059, +0.000] | 19 | 19 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | frac_original_T | 0.625 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | 11 | 11 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | frac_original_T | 0.75 | 0.013 | 0.020 | -0.007 | [-0.059, +0.026] | 19 | 19 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | frac_original_T | 0.875 | 0.020 | 0.020 | +0.000 | [-0.033, +0.026] | 19 | 19 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | frac_original_T | 0.9375 | 0.034 | 0.000 | +0.034 | [+0.000, +0.068] | 11 | 11 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | frac_original_T | 1 | 0.039 | 0.020 | +0.020 | [-0.020, +0.053] | 19 | 19 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | long_T | 0.5 | 0.000 | 0.020 | -0.020 | [-0.059, +0.000] | 19 | 19 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | long_T | 0.625 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | 11 | 11 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | long_T | 0.75 | 0.000 | 0.020 | -0.020 | [-0.059, +0.000] | 19 | 19 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | long_T | 0.875 | 0.000 | 0.020 | -0.020 | [-0.059, +0.000] | 19 | 19 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | long_T | 1 | 0.039 | 0.020 | +0.020 | [-0.020, +0.053] | 19 | 19 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_long | 0.5 | -0.118 | -0.125 | +0.007 | [-0.079, +0.092] | 19 | 19 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_long | 0.625 | -0.212 | -0.182 | -0.030 | [-0.174, +0.106] | 11 | 11 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_long | 0.75 | -0.289 | -0.125 | -0.164 | [-0.303, -0.026] | 19 | 19 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_long | 0.875 | -0.579 | -0.125 | -0.454 | [-0.697, -0.224] | 19 | 19 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_long | 1 | 0.000 | -0.125 | +0.125 | [+0.072, +0.178] | 19 | 19 |

### Rescue threshold (design: smallest f with delta_original under A1_purge > +0.10 and CI lower bound > 0)

| world | dose | family | f* | delta at f* | CI lower |
|---|---|---|---|---|---|
| W1_INSIDE | 0.5 | mix:1/full | 0.625 | +0.148 | +0.023 |

## Wipe bridge: A2_purge_wipe minus A1_purge on frac_original_T, per cell (captured episodes, paired)

| world | dose | memory | mean wipe | mean purge | diff | 95% CI | tasks |
|---|---|---|---|---|---|---|---|
| W1_INSIDE | 0.5 | 1 | 0.047 | 0.047 | +0.000 | [+0.000, +0.000] | 24 |
| W1_INSIDE | 0.5 | full | 0.020 | 0.224 | -0.204 | [-0.276, -0.132] | 19 |
| W1_INSIDE | 0.5 | mix:1/full@0 | 0.020 | 0.224 | -0.204 | [-0.276, -0.132] | 19 |
| W1_INSIDE | 0.5 | mix:1/full@0.5 | 0.000 | 0.167 | -0.167 | [-0.234, -0.104] | 24 |
| W1_INSIDE | 0.5 | mix:1/full@0.625 | 0.000 | 0.312 | -0.312 | [-0.490, -0.156] | 12 |
| W1_INSIDE | 0.5 | mix:1/full@0.75 | 0.016 | 0.339 | -0.323 | [-0.474, -0.193] | 24 |
| W1_INSIDE | 0.5 | mix:1/full@0.875 | 0.016 | 0.391 | -0.375 | [-0.495, -0.266] | 24 |
| W1_INSIDE | 0.5 | mix:1/full@0.9375 | 0.031 | 0.031 | +0.000 | [+0.000, +0.000] | 12 |
| W1_INSIDE | 0.5 | mix:1/full@1 | 0.047 | 0.047 | +0.000 | [+0.000, +0.000] | 24 |

## Mean honest fraction on the original after removal, A1_purge, captured episodes (rounds 1, 5, 10, 20, 30, 50, 80 after removal)

| world | dose | memory | r1 | r5 | r10 | r20 | r30 | r50 | r80 | long r50 | short r50 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| W1_INSIDE | 0.5 | 1 | 0.047 | 0.047 | 0.047 | 0.047 | 0.047 | | | 0.047 | nan |
| W1_INSIDE | 0.5 | full | 0.151 | 0.184 | 0.197 | 0.178 | 0.224 | | | 0.204 | nan |
| W1_INSIDE | 0.5 | mix:1/full@0 | 0.151 | 0.184 | 0.197 | 0.178 | 0.224 | | | 0.204 | nan |
| W1_INSIDE | 0.5 | mix:1/full@0.5 | 0.099 | 0.146 | 0.177 | 0.161 | 0.167 | | | 0.250 | 0.188 |
| W1_INSIDE | 0.5 | mix:1/full@0.625 | 0.156 | 0.229 | 0.229 | 0.229 | 0.312 | | | 0.222 | 0.267 |
| W1_INSIDE | 0.5 | mix:1/full@0.75 | 0.161 | 0.255 | 0.297 | 0.339 | 0.339 | | | 0.333 | 0.368 |
| W1_INSIDE | 0.5 | mix:1/full@0.875 | 0.177 | 0.245 | 0.354 | 0.385 | 0.391 | | | 0.458 | 0.411 |
| W1_INSIDE | 0.5 | mix:1/full@0.9375 | 0.031 | 0.031 | 0.031 | 0.031 | 0.031 | | | nan | 0.031 |
| W1_INSIDE | 0.5 | mix:1/full@1 | 0.047 | 0.047 | 0.047 | 0.047 | 0.047 | | | 0.047 | nan |

Invalid episodes per cell and arm are in the CSV; none are dropped or retried. Capture is decided before removal and shared by the arms.
