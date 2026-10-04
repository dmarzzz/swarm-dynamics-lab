# Post-mortem: S2_pilot attempt 1 (capture-memory, real model)

- Experiment / owner / stage / date: capture-memory (hunch) / shadow (shadow/sol-capture) / Q0 + S2_pilot / 2026-10-04 04:05Z to 04:50Z
- Pre-run assessment, parent attempt, versions: `reviews/S2_pilot-pre.md`; parent = scripted S1b; code commit `6e116dce` on every record; design v1.2; model `meta-llama/llama-3.1-8b-instruct` (OpenRouter, price-sorted providers DeepInfra / Novita); prompt `src/model.py SYSTEM` + three-line user message.
- Run IDs, artifacts, reproduction: hub experiment `capture-memory`, Q0 runs `305e44fd`, `240b147f`; S2_pilot runs `505b38db 32416332 94dc8f31 b28748a1 b2631047 3d02ed1f` (memory 1, tasks 0..5) and `da911cee e22be20f d66e3c8e 5c73e65e cf5016d7 fdf4d3c8` (full, tasks 0..5); `analysis-S2_pilot` carries S2_pilot.md / _cells.csv / _dose_rule.json. Reproduce: `coordinator.py stage Q0 --backend http --go ...`, `worker.py --hub --backend http` with `SWARM_MODEL_CONFIG` (model id, caps, prices, budget file), then `stage S2_pilot`, then `analyze.py --stage S2_pilot`. Scripted reference: `pilot_reference.py --stage S2_pilot [--tasks 0-99 --seeds 1,2]`.
- Disposition: complete-valid-result (as a pilot). Not a qualification for a holdout S2: doses unfitted, pair priors unhandled.

## What ran and what happened

- Planned 2 (Q0) + 12 (S2_pilot) runs -> started 14 -> terminal 14 done, 0 failed -> graded 28 arm records (4 Q0 + 24 pilot) -> analyzed 24 pilot records. No duplicates, no re-queues, no missing records.
- Actual: 10,384 pilot calls (plus 161 hub Q0, 36 + 60 + 153 local probes), 1.46M prompt / 34K completion tokens, 0.0308 USD pilot (0.032 USD all-in), ~11 min wall with 4 workers. Failed work: none; 0 transport errors.
- Results (denominators = captured episodes, cluster = task, 6 tasks): memory 1 (4 captured) A1 frac_original_T 0.214 [0.07, 0.36], delta +0.179 [+0.07, +0.29]; full (5 captured) 0.167 [0.03, 0.30], delta +0.133 [-0.03, +0.30]. Purge minus no purge: +0.107 [+0.00, +0.21] (memory 1), +0.033 [-0.13, +0.20] (full). Full minus memory 1 under A1: -0.089 [-0.27, +0.18] (4 tasks).
- Clean competence: Q0 validity 1.00 (161 calls, 0 invalid). Control: A0 stayed captured where captured (0.11 / 0.13). Manipulation: captured 4/6 and 5/6; the misses are two word pairs with a strong model prior (pira > brisk, olam > quon). Evaluator: unchanged from the scripted stages; `delta_original` added and checked in selftest.
- Expected vs observed: memory 1 matched the scripted regime (return, no recovery). Full memory captured in 8 rounds vs 83 to 96 scripted: the model does not average a long list, it weights the recent tail. The scripted "freeze" does not exist at N = 12 / entrench 10 even for the scripted rule (delta +0.17), so the pilot could not test it.

## Visualization review

- Mapping: final-frame tables only, as declared. Delivered: mean post-removal trace at rounds 0..50 per memory x arm, per-episode table with words / capture / latency / frac at removal / A0 / A1 / delta / calls / USD (results/S2_pilot.md), raw `series_original` per record on the hub.
- Coverage: every round of every episode is in `series_original`; no downsampling. Failures: none to display (0 invalid).
- Agreement: the r50 column of the trace table equals the frac_original_T column (checked by construction, same field). No animation; limitation accepted for 12 episodes.

## Experiment-quality assessment

- Did this run test the question? Partly. It tested whether a small model's honest agents show the memory-1 regime after a perfect purge (yes, weakly, 4 tasks) and whether full memory freezes (untestable at this configuration; the scripted rule does not freeze here either, which the pre-run should have caught by running `pilot_reference.py` first). It also measured real tokens per call (141) for budgeting.
- Confounds and gaps: (a) doses carried from the scripted rule, not fitted; (b) word-pair prior drives capture failure on 2 of 6 pairs (yang-2026-when artefact) and is confounded with task; (c) memory 1 and full share the matching schedule but not the model's samples, so the memory contrast is between-condition over 6 clusters; (d) N = 12 / entrench 10 removes the banked-history mechanism the hypothesis is about.
- Execution success: yes. Qualification success: yes for parse/validity. Scientific conclusion: none beyond "memory 1 looks scripted-like; full memory is not a running mean for this model; pair priors matter".
- Claims still justified: the scripted S1b findings as scripted findings. Claims needing correction: the README's "freeze" should be stated as conditional on long entrenchment (banked history), not on unbounded memory per se. Unknown: the model's own dose thresholds and (beta, h) per pair.

## Failure and repair ledger

| ID / kind | Observed evidence | Suspected or verified cause | Repair / diagnostic | Acceptance check and rerun evidence | Owner / status |
|---|---|---|---|---|---|
| P1 / capability | 'brusk' for 'brisk' in 3/36 Q0-attempt-0 calls, strict parser invalidated both episodes | verified: one-letter misspelling of one nonsense word by an 8B model at temp 0.7 | edit-distance-1 accept (counted), one re-ask, then invalid; selftest 10 covers it | Q0 attempt 1 and hub Q0: validity 1.00; pilot 74 fuzzy / 10,384 calls, 0 invalid | sol-capture / fixed |
| P2 / design | 2 of 6 pairs never captured at memory 1 (0.57, 0.86 on original at cap); scripted rule captures 100% | suspected: model string prior for pira, olam | not repaired in this attempt; next: (beta, h) fit per pair, balance or exclude | n/a | open |
| P3 / design | pre-run compared against S1b at N = 24; scripted at N = 12 does not freeze | verified by `pilot_reference.py` after the run | reference script added; README freeze claim to be qualified | reference tables committed | sol-capture / partially fixed |
| P4 / infra | sim-shadow port 22 refused; no free fleet box | not diagnosed (box may be rebuilt or down) | ran on shadow's box; no claim held | hub records carry host shad0wbot-local | open, dmarz's box |

No credentials or endpoints appear in any artifact; the model key was read from a local file into the process environment only.

## Next run

- Fit (beta, h) per word pair on the model with the de-marzo protocol (about 20 pairs x ~50 calls = 1,000 calls, < 0.01 USD) and pick balanced pairs; this is the pre-step preregistration section 7 already demands.
- Model-side dose mini-sweep at N = 12 for memories {1, 5, full} (dose rule, horizon 60), ~5K calls.
- Then, if the hypothesis is accepted, S2 proper with entrench 20 to 40 so the banked-history mechanism exists; budget from the measured 141 tokens/call (full-memory prompts grow with entrenchment; expect ~250 to 400 tokens/call there).
- Alternative explanation to test: "the model copies the last word heard regardless of memory length" would predict memory 1 and full identical on every metric at the same dose. A same-dose cell (both at 0.54) is the cheapest disproof and should be in the next design.
