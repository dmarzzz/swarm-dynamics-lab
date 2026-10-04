# capture-memory-mix: MP results

432 selected arm records (459 raw records in the files, 13 of them invalid, 27 superseded by a later attempt of the same episode; see 'Attempt lineage' below), backends ['http:openai/gpt-4o-mini'], about 113464 model calls in the selected records; provider-reported spend on the shared ledger (all models, all pilot work, including superseded attempts) 3.9326 USD. Code commits: ['016104d9', '3ffb56b6', '492d762f'].

Columns: captured = capture rate (shared by arms); frac@rem / frac_T = honest fraction on the original at removal and 30 rounds later (eval_round in the records' cfg; captured episodes); delta = frac_T minus frac@rem (0 = frozen, > 0 = returning); short_T / long_T = the same at round T split by memory kind; delta_long = return among the long-memory agents only.

## Cells (captured episodes unless noted)

| world | dose | memory | arm | n | inv | captured | lat | frac@rem | frac_T | delta | short_T | long_T | delta_long | recovered | half-time |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| W1_INSIDE | 0.5 | 1 | A0_no_purge | 24 | 0 | 1.00 | 2.0 | 0.047 | 0.000 | -0.047 | nan | 0.000 | -0.047 | 0.00 | None |
| W1_INSIDE | 0.5 | 1 | A1_purge | 24 | 0 | 1.00 | 2.0 | 0.047 | 0.047 | +0.000 | nan | 0.047 | +0.000 | 0.00 | None |
| W1_INSIDE | 0.5 | 1 | A2_purge_wipe | 24 | 0 | 1.00 | 2.0 | 0.047 | 0.047 | +0.000 | nan | 0.047 | +0.000 | 0.00 | None |
| W1_INSIDE | 0.5 | full | A0_no_purge | 24 | 0 | 0.88 | 18 | 0.149 | 0.167 | +0.018 | nan | 0.167 | +0.018 | 0.00 | 14.0 |
| W1_INSIDE | 0.5 | full | A1_purge | 24 | 0 | 0.88 | 18 | 0.149 | 0.208 | +0.059 | nan | 0.208 | +0.059 | 0.00 | 8.5 |
| W1_INSIDE | 0.5 | full | A2_purge_wipe | 24 | 0 | 0.88 | 18 | 0.149 | 0.018 | -0.131 | nan | 0.018 | -0.131 | 0.00 | 4 |
| W1_INSIDE | 0.5 | mix:1/full@0 | A0_no_purge | 24 | 0 | 0.88 | 18 | 0.149 | 0.167 | +0.018 | nan | 0.167 | +0.018 | 0.00 | 14.0 |
| W1_INSIDE | 0.5 | mix:1/full@0 | A1_purge | 24 | 0 | 0.88 | 18 | 0.149 | 0.208 | +0.059 | nan | 0.208 | +0.059 | 0.00 | 8.5 |
| W1_INSIDE | 0.5 | mix:1/full@0 | A2_purge_wipe | 24 | 0 | 0.88 | 18 | 0.149 | 0.018 | -0.131 | nan | 0.018 | -0.131 | 0.00 | 4 |
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
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_original | 0.5 | 0.054 | 0.060 | -0.006 | [-0.095, +0.077] | 21 | 21 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_original | 0.625 | 0.148 | 0.057 | +0.091 | [-0.011, +0.216] | 11 | 11 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_original | 0.75 | 0.149 | 0.060 | +0.089 | [-0.060, +0.262] | 21 | 21 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_original | 0.875 | 0.214 | 0.060 | +0.155 | [+0.012, +0.292] | 21 | 21 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_original | 0.9375 | 0.000 | 0.057 | -0.057 | [-0.136, +0.034] | 11 | 11 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_original | 1 | 0.000 | 0.060 | -0.060 | [-0.119, +0.006] | 21 | 21 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | frac_original_T | 0.5 | 0.149 | 0.208 | -0.060 | [-0.143, +0.030] | 21 | 21 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | frac_original_T | 0.625 | 0.250 | 0.239 | +0.011 | [-0.125, +0.159] | 11 | 11 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | frac_original_T | 0.75 | 0.280 | 0.208 | +0.071 | [-0.089, +0.256] | 21 | 21 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | frac_original_T | 0.875 | 0.369 | 0.208 | +0.161 | [+0.030, +0.286] | 21 | 21 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | frac_original_T | 0.9375 | 0.034 | 0.239 | -0.205 | [-0.307, -0.091] | 11 | 11 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | frac_original_T | 1 | 0.036 | 0.208 | -0.173 | [-0.244, -0.095] | 21 | 21 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | long_T | 0.5 | 0.190 | 0.208 | -0.018 | [-0.113, +0.089] | 21 | 21 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | long_T | 0.625 | 0.242 | 0.239 | +0.004 | [-0.148, +0.148] | 11 | 11 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | long_T | 0.75 | 0.333 | 0.208 | +0.125 | [-0.065, +0.333] | 21 | 21 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | long_T | 0.875 | 0.381 | 0.208 | +0.173 | [-0.024, +0.381] | 21 | 21 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | long_T | 1 | 0.036 | 0.208 | -0.173 | [-0.244, -0.095] | 21 | 21 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_long | 0.5 | 0.060 | 0.060 | +0.000 | [-0.119, +0.107] | 21 | 21 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_long | 0.625 | 0.030 | 0.057 | -0.027 | [-0.167, +0.110] | 11 | 11 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_long | 0.75 | 0.024 | 0.060 | -0.036 | [-0.238, +0.167] | 21 | 21 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_long | 0.875 | -0.238 | 0.060 | -0.298 | [-0.583, -0.024] | 21 | 21 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | delta_long | 1 | 0.000 | 0.060 | -0.060 | [-0.119, +0.006] | 21 | 21 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | half_time | 0.5 | 8.000 | 8.667 | -0.667 | [-8.000, +8.000] | 3 | 3 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | half_time | 0.625 | 14.500 | 7.500 | +7.000 | [+1.000, +14.750] | 4 | 4 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | half_time | 0.75 | 20.000 | 11.000 | +9.000 | [-5.000, +23.000] | 2 | 2 |
| W1_INSIDE | 0.5 | mix:1/full | A1_purge | half_time | 0.875 | 9.857 | 7.143 | +2.714 | [-2.286, +7.714] | 7 | 7 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_original | 0.5 | -0.095 | -0.131 | +0.036 | [-0.030, +0.095] | 21 | 21 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_original | 0.625 | -0.102 | -0.182 | +0.080 | [+0.000, +0.148] | 11 | 11 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_original | 0.75 | -0.113 | -0.131 | +0.018 | [-0.036, +0.077] | 21 | 21 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_original | 0.875 | -0.137 | -0.131 | -0.006 | [-0.065, +0.042] | 21 | 21 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_original | 0.9375 | 0.000 | -0.182 | +0.182 | [+0.125, +0.239] | 11 | 11 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_original | 1 | 0.000 | -0.131 | +0.131 | [+0.077, +0.185] | 21 | 21 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | frac_original_T | 0.5 | 0.000 | 0.018 | -0.018 | [-0.054, +0.000] | 21 | 21 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | frac_original_T | 0.625 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | 11 | 11 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | frac_original_T | 0.75 | 0.018 | 0.018 | +0.000 | [-0.048, +0.036] | 21 | 21 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | frac_original_T | 0.875 | 0.018 | 0.018 | +0.000 | [-0.030, +0.024] | 21 | 21 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | frac_original_T | 0.9375 | 0.034 | 0.000 | +0.034 | [+0.000, +0.068] | 11 | 11 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | frac_original_T | 1 | 0.036 | 0.018 | +0.018 | [-0.018, +0.048] | 21 | 21 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | long_T | 0.5 | 0.000 | 0.018 | -0.018 | [-0.054, +0.000] | 21 | 21 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | long_T | 0.625 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | 11 | 11 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | long_T | 0.75 | 0.000 | 0.018 | -0.018 | [-0.054, +0.000] | 21 | 21 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | long_T | 0.875 | 0.000 | 0.018 | -0.018 | [-0.054, +0.000] | 21 | 21 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | long_T | 1 | 0.036 | 0.018 | +0.018 | [-0.018, +0.048] | 21 | 21 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_long | 0.5 | -0.131 | -0.131 | +0.000 | [-0.083, +0.077] | 21 | 21 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_long | 0.625 | -0.212 | -0.182 | -0.030 | [-0.174, +0.106] | 11 | 11 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_long | 0.75 | -0.310 | -0.131 | -0.179 | [-0.310, -0.048] | 21 | 21 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_long | 0.875 | -0.619 | -0.131 | -0.488 | [-0.702, -0.274] | 21 | 21 |
| W1_INSIDE | 0.5 | mix:1/full | A2_purge_wipe | delta_long | 1 | 0.000 | -0.131 | +0.131 | [+0.077, +0.185] | 21 | 21 |

### Rescue threshold (design: smallest f with delta_original under A1_purge > +0.10 and CI lower bound > 0)

| world | dose | family | f* | delta at f* | CI lower |
|---|---|---|---|---|---|
| W1_INSIDE | 0.5 | mix:1/full | 0.625 | +0.148 | +0.023 |

## Wipe bridge: A2_purge_wipe minus A1_purge on frac_original_T, per cell (captured episodes, paired)

| world | dose | memory | mean wipe | mean purge | diff | 95% CI | tasks |
|---|---|---|---|---|---|---|---|
| W1_INSIDE | 0.5 | 1 | 0.047 | 0.047 | +0.000 | [+0.000, +0.000] | 24 |
| W1_INSIDE | 0.5 | full | 0.018 | 0.208 | -0.190 | [-0.262, -0.119] | 21 |
| W1_INSIDE | 0.5 | mix:1/full@0 | 0.018 | 0.208 | -0.190 | [-0.262, -0.119] | 21 |
| W1_INSIDE | 0.5 | mix:1/full@0.5 | 0.000 | 0.167 | -0.167 | [-0.234, -0.104] | 24 |
| W1_INSIDE | 0.5 | mix:1/full@0.625 | 0.000 | 0.312 | -0.312 | [-0.490, -0.156] | 12 |
| W1_INSIDE | 0.5 | mix:1/full@0.75 | 0.016 | 0.339 | -0.323 | [-0.474, -0.193] | 24 |
| W1_INSIDE | 0.5 | mix:1/full@0.875 | 0.016 | 0.391 | -0.375 | [-0.495, -0.266] | 24 |
| W1_INSIDE | 0.5 | mix:1/full@0.9375 | 0.031 | 0.031 | +0.000 | [+0.000, +0.000] | 12 |
| W1_INSIDE | 0.5 | mix:1/full@1 | 0.047 | 0.047 | +0.000 | [+0.000, +0.000] | 24 |

## Mean honest fraction on the original after removal, A1_purge, captured episodes (rounds 1, 5, 10, 20, 30 after removal; recovery phase 40 rounds)

| world | dose | memory | r1 | r5 | r10 | r20 | r30 | long r30 | short r30 |
|---|---|---|---|---|---|---|---|---|---|
| W1_INSIDE | 0.5 | 1 | 0.047 | 0.047 | 0.047 | 0.047 | 0.047 | 0.047 | nan |
| W1_INSIDE | 0.5 | full | 0.149 | 0.167 | 0.190 | 0.167 | 0.208 | 0.208 | nan |
| W1_INSIDE | 0.5 | mix:1/full@0 | 0.149 | 0.167 | 0.190 | 0.167 | 0.208 | 0.208 | nan |
| W1_INSIDE | 0.5 | mix:1/full@0.5 | 0.099 | 0.146 | 0.177 | 0.161 | 0.167 | 0.198 | 0.135 |
| W1_INSIDE | 0.5 | mix:1/full@0.625 | 0.156 | 0.229 | 0.229 | 0.229 | 0.312 | 0.306 | 0.317 |
| W1_INSIDE | 0.5 | mix:1/full@0.75 | 0.161 | 0.255 | 0.297 | 0.339 | 0.339 | 0.396 | 0.319 |
| W1_INSIDE | 0.5 | mix:1/full@0.875 | 0.177 | 0.245 | 0.354 | 0.385 | 0.391 | 0.458 | 0.381 |
| W1_INSIDE | 0.5 | mix:1/full@0.9375 | 0.031 | 0.031 | 0.031 | 0.031 | 0.031 | nan | 0.031 |
| W1_INSIDE | 0.5 | mix:1/full@1 | 0.047 | 0.047 | 0.047 | 0.047 | 0.047 | 0.047 | nan |

## Attempt lineage (raw records vs selected records)

An attempt = one run of an episode's arms in the append-only file. Resumed workers re-ran every episode that did not already have all arms valid. Selection: last attempt with all arms valid, else last attempt. 'episodes multi valid' counts episodes with more than one fully valid attempt (selection then takes the last one; see CORRECTIONS.md for the first-attempt sensitivity check).

| world | dose | memory | episodes | attempts | episodes rerun | episodes multi valid | raw records | raw invalid | superseded records | selected records | selected invalid |
|---|---|---|---|---|---|---|---|---|---|---|---|
| W1_INSIDE | 0.5 | 1 | 24 | 25 | 1 | 0 | 75 | 1 | 3 | 72 | 0 |
| W1_INSIDE | 0.5 | full | 24 | 32 | 4 | 4 | 96 | 12 | 24 | 72 | 0 |
| W1_INSIDE | 0.5 | mix:1/full@0.5 | 24 | 24 | 0 | 0 | 72 | 0 | 0 | 72 | 0 |
| W1_INSIDE | 0.5 | mix:1/full@0.625 | 12 | 12 | 0 | 0 | 36 | 0 | 0 | 36 | 0 |
| W1_INSIDE | 0.5 | mix:1/full@0.75 | 24 | 24 | 0 | 0 | 72 | 0 | 0 | 72 | 0 |
| W1_INSIDE | 0.5 | mix:1/full@0.875 | 24 | 24 | 0 | 0 | 72 | 0 | 0 | 72 | 0 |
| W1_INSIDE | 0.5 | mix:1/full@0.9375 | 12 | 12 | 0 | 0 | 36 | 0 | 0 | 36 | 0 |
| **total** | | | **144** | **153** | **5** | **4** | **459** | **13** | **27** | **432** | **0** |

Retry accounting: 27 of 459 raw records were superseded by a later attempt (resume re-runs after provider errors or interrupted runs); 0 selected records are invalid and are counted in the 'inv' column, not dropped silently. Capture is decided before removal and shared by the arms.
