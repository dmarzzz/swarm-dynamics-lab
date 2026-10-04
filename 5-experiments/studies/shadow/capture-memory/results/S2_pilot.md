# capture-memory: S2_pilot results

24 episode records, backends ['http:meta-llama/llama-3.1-8b-instruct']. Code commits: ['6e116dce'].

## Cells

| world | dose | memory | arm | n | invalid | captured | lat | frac_orig_T (all / captured) | recovered (all / captured) | half-time |
|---|---|---|---|---|---|---|---|---|---|---|
| W1_INSIDE | 0.42 | 1 | A0_no_purge | 6 | 0 | 0.67 | 3.0 | 0.286 / 0.107 | 0.000 / 0.000 | 24.5 |
| W1_INSIDE | 0.42 | 1 | A1_purge | 6 | 0 | 0.67 | 3.0 | 0.309 / 0.214 | 0.000 / 0.000 | 27.5 |
| W1_INSIDE | 0.54 | full | A0_no_purge | 6 | 0 | 0.83 | 8 | 0.195 / 0.133 | 0.000 / 0.000 | 1 |
| W1_INSIDE | 0.54 | full | A1_purge | 6 | 0 | 0.83 | 8 | 0.222 / 0.167 | 0.000 / 0.000 | 4.5 |

## Capture rate by dose and memory (within 100 / 200 / 120 takeover rounds; 95% CI at H = 200 is a cluster bootstrap over tasks)

Capture is decided before the intervention and is shared by the arms, so one row per cell (read from A1_purge). Dose rule (design.yaml): per memory and world, the smallest grid dose with >= 80% captured within H = 200.

| world | memory | dose | k | n | cap<=100 | cap<=120 | 95% CI (H=200) | median latency |
|---|---|---|---|---|---|---|---|---|
| W1_INSIDE | 1 | 0.42 | 5 | 6 | 0.67 | 0.67 | [0.33, 1.00] | 3.0 |
| W1_INSIDE | full | 0.54 | 6 | 6 | 0.83 | 0.83 | [0.50, 1.00] | 8 |

### Dose rule applied: smallest dose with >= 80% captured within 200 rounds

| world | memory | dose* | captured within H at dose* | 95% CI | note |
|---|---|---|---|---|---|
| W1_INSIDE | 1 | none on grid | nan at 0.42 | [0.33, 1.00] | not capturable at this horizon; excluded from removal contrasts |
| W1_INSIDE | full | none on grid | nan at 0.54 | [0.50, 1.00] | not capturable at this horizon; excluded from removal contrasts |

## Memory contrasts (paired per task x seed, cluster bootstrap over tasks)

Declared primary: stage S1, W1_INSIDE dose 0.42, arm A1_purge, frac_original_T, memory 20 minus memory 1, episodes captured under both. Everything else is exploratory.

| cell | arm | metric | memory pair | mean a | mean b | diff (a - b) | 95% CI | tasks | n pairs |
|---|---|---|---|---|---|---|---|---|---|

## Memory contrasts at the per-memory dose (dose rule applied; exploratory, doses differ across the pair)

| world | arm | metric | memory a @ dose* | memory b @ dose* | mean a | mean b | diff | 95% CI | tasks | n pairs |
|---|---|---|---|---|---|---|---|---|---|---|

## Bridge to vishesh's repair arms: A2_purge_wipe minus A1_purge, per memory (exploratory)

| cell | memory | metric | mean wipe | mean purge | diff | 95% CI | tasks |
|---|---|---|---|---|---|---|---|

## Pilot summary: each memory at its own dose ({'1': 0.42, 'full': 0.54}), 6 tasks, cluster bootstrap over tasks

Six tasks is a pilot, not a sample: the CIs below are percentile bootstraps over 6 clusters and are wide by construction. Capture is shared by the arms of an episode. `delta_original` = frac_original_T minus frac_original_at_removal (positive = came back, about zero = frozen, negative = kept sliding).

| memory | dose | k | n | invalid | captured | latency med | arm | frac_orig_T (captured) | 95% CI | delta_original | 95% CI | recovered |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.42 | 5 | 6 | 0 | 4/6 | 3.0 | A0_no_purge | 0.107 | [0.04, 0.14] | +0.071 | [+0.00, +0.14] | 0.00 |
| 1 | 0.42 | 5 | 6 | 0 | 4/6 | 3.0 | A1_purge | 0.214 | [0.07, 0.36] | +0.179 | [+0.07, +0.29] | 0.00 |
| full | 0.54 | 6 | 6 | 0 | 5/6 | 8 | A0_no_purge | 0.133 | [0.00, 0.30] | +0.100 | [-0.07, +0.30] | 0.00 |
| full | 0.54 | 6 | 6 | 0 | 5/6 | 8 | A1_purge | 0.167 | [0.03, 0.30] | +0.133 | [-0.03, +0.30] | 0.00 |

### Purge effect, A1_purge minus A0_no_purge, paired per episode (same prefix), captured episodes

| memory | metric | A1 | A0 | diff | 95% CI | tasks |
|---|---|---|---|---|---|---|
| 1 | frac_original_T | 0.214 | 0.107 | +0.107 | [+0.00, +0.21] | 4 |
| 1 | delta_original | 0.179 | 0.071 | +0.107 | [+0.00, +0.21] | 4 |
| full | frac_original_T | 0.167 | 0.133 | +0.033 | [-0.13, +0.20] | 5 |
| full | delta_original | 0.133 | 0.100 | +0.033 | [-0.13, +0.20] | 5 |

### Memory contrast under A1_purge: memory full @ 0.54 minus memory 1 @ 0.42 (captured under both; doses differ, so this is the per-memory-dose comparison the dose rule calls for)

| metric | memory full | memory 1 | diff | 95% CI | tasks |
|---|---|---|---|---|---|
| frac_original_T | 0.125 | 0.214 | -0.089 | [-0.27, +0.18] | 4 |
| delta_original | 0.083 | 0.179 | -0.095 | [-0.30, +0.18] | 4 |
| frac_original_at_removal | 0.042 | 0.036 | +0.006 | [-0.11, +0.13] | 4 |

### Mean honest fraction on the original, by round after the intervention (captured episodes; round 0 = at removal)

| memory | arm | n | r0 | r1 | r2 | r3 | r5 | r10 | r20 | r30 | r40 | r50 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | A0_no_purge | 4 | 0.04 | 0.07 | 0.18 | 0.21 | 0.18 | 0.14 | 0.14 | 0.14 | 0.18 | 0.11 |
| 1 | A1_purge | 4 | 0.04 | 0.14 | 0.07 | 0.14 | 0.11 | 0.21 | 0.04 | 0.25 | 0.14 | 0.21 |
| full | A0_no_purge | 5 | 0.03 | 0.37 | 0.17 | 0.20 | 0.23 | 0.27 | 0.23 | 0.03 | 0.20 | 0.13 |
| full | A1_purge | 5 | 0.03 | 0.07 | 0.07 | 0.27 | 0.23 | 0.20 | 0.27 | 0.17 | 0.27 | 0.17 |

### Per episode

| task | words (orig / attack) | memory | captured | latency | frac at removal | A0 frac_T | A1 frac_T | A1 delta | calls (prefix + A0 + A1) | USD |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | ruvo / brisk | 1 | True | 6 | 0.14 | 0.14 | 0.43 | +0.29 | 711 | 0.00124 |
| 1 | teru / quon | 1 | True | 2 | 0.00 | 0.14 | 0.29 | +0.29 | 690 | 0.00123 |
| 2 | pira / brisk | 1 | False | None | 0.57 | 0.43 | 0.29 | -0.29 | 1502 | 0.00261 |
| 3 | sello / pira | 1 | True | 1 | 0.00 | 0.00 | 0.00 | +0.00 | 673 | 0.00119 |
| 4 | olam / quon | 1 | False | None | 0.86 | 0.86 | 0.71 | -0.14 | 1498 | 0.00265 |
| 5 | ruvo / olam | 1 | True | 4 | 0.00 | 0.14 | 0.14 | +0.14 | 714 | 0.00128 |
| 0 | ruvo / brisk | full | True | 43 | 0.00 | 0.50 | 0.17 | +0.17 | 840 | 0.00345 |
| 1 | teru / quon | full | True | 4 | 0.00 | 0.00 | 0.00 | +0.00 | 586 | 0.00208 |
| 2 | pira / brisk | full | False | None | 0.67 | 0.50 | 0.50 | -0.17 | 1294 | 0.00801 |
| 3 | sello / pira | full | True | 8 | 0.00 | 0.00 | 0.33 | +0.33 | 614 | 0.00226 |
| 4 | olam / quon | full | True | 17 | 0.00 | 0.17 | 0.33 | +0.33 | 676 | 0.00275 |
| 5 | ruvo / olam | full | True | 1 | 0.17 | 0.00 | 0.00 | -0.17 | 586 | 0.00203 |

## Spend (from the provider's usage fields on every call)

- model calls: 10384 (prefix counted once per episode)
- prompt tokens: 1462424, completion tokens: 33994, mean prompt 141 tokens/call
- actual cost: 0.0308 USD (OpenRouter `usage.cost`)
- parse: 74 fuzzy accepts (edit distance 1), 1 re-asks, 0 unparseable after re-ask; call-level clean-parse rate 0.9928
- invalid episodes: 0 of 24 records

Invalid episodes per cell and arm are in the CSV; none are dropped or retried.
Capture is decided before removal and shared by all arms of an episode, so 'captured' is the same across arms of a cell.
Everything except the PRIMARY row is exploratory.
