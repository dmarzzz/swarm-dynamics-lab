# S2_pilot: scripted reference at the stage's own configuration

Scripted tanh policy (beta 2.5, h_inside 0.1), cfg {'n_agents': 12, 'beta': 2.5, 'h_inside': 0.1, 'h_outside': 0.5, 'entrench_rounds': 10, 'takeover_max_rounds': 120, 'clean_takeover_rounds': 20, 'recovery_rounds': 50, 'capture_frac': 0.75, 'capture_streak': 3, 'recover_frac': 0.75, 'recover_streak': 10, 'eval_round': 50}, tasks 0-99, seeds [1, 2]. This is what the scripted model predicts for the pilot's exact N, doses, horizons and tasks; it is not a model result.

| world | memory | dose | k | n | captured | latency med | arm | frac_orig_T (captured) | 95% CI | delta_original | 95% CI |
|---|---|---|---|---|---|---|---|---|---|---|---|
| W1_INSIDE | 1 | 0.42 | 5 | 200 | 200/200 | 3.0 | A0_no_purge | 0.029 | [0.02, 0.04] | -0.012 | [-0.02, -0.00] |
| W1_INSIDE | 1 | 0.42 | 5 | 200 | 200/200 | 3.0 | A1_purge | 0.283 | [0.26, 0.31] | +0.241 | [+0.22, +0.26] |
| W1_INSIDE | full | 0.54 | 6 | 200 | 176/200 | 83.0 | A0_no_purge | 0.154 | [0.13, 0.18] | +0.042 | [+0.01, +0.07] |
| W1_INSIDE | full | 0.54 | 6 | 200 | 176/200 | 83.0 | A1_purge | 0.278 | [0.25, 0.31] | +0.166 | [+0.13, +0.20] |
