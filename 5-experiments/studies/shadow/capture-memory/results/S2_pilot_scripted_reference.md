# S2_pilot: scripted reference at the stage's own configuration

Scripted tanh policy (beta 2.5, h_inside 0.1), cfg {'n_agents': 12, 'beta': 2.5, 'h_inside': 0.1, 'h_outside': 0.5, 'entrench_rounds': 10, 'takeover_max_rounds': 120, 'clean_takeover_rounds': 20, 'recovery_rounds': 50, 'capture_frac': 0.75, 'capture_streak': 3, 'recover_frac': 0.75, 'recover_streak': 10, 'eval_round': 50}, tasks 0-5, seeds [1]. This is what the scripted model predicts for the pilot's exact N, doses, horizons and tasks; it is not a model result.

| world | memory | dose | k | n | captured | latency med | arm | frac_orig_T (captured) | 95% CI | delta_original | 95% CI |
|---|---|---|---|---|---|---|---|---|---|---|---|
| W1_INSIDE | 1 | 0.42 | 5 | 6 | 6/6 | 3.5 | A0_no_purge | 0.000 | [0.00, 0.00] | -0.048 | [-0.10, +0.00] |
| W1_INSIDE | 1 | 0.42 | 5 | 6 | 6/6 | 3.5 | A1_purge | 0.238 | [0.12, 0.38] | +0.190 | [+0.07, +0.31] |
| W1_INSIDE | full | 0.54 | 6 | 6 | 5/6 | 96 | A0_no_purge | 0.200 | [0.07, 0.37] | +0.067 | [-0.10, +0.30] |
| W1_INSIDE | full | 0.54 | 6 | 6 | 5/6 | 96 | A1_purge | 0.300 | [0.13, 0.47] | +0.167 | [-0.03, +0.37] |
