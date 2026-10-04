# Pre-run assessment: S2_pilot attempt 1 (capture-memory, real model)

- Experiment / owner / stage: capture-memory (hunch, `researchers/shadow/notes/capture-memory/`) / shadow (agent shadow/sol-capture) / S2_pilot, preceded by Q0
- Parent attempt and previous post-mortem: scripted S1b (results/S1b.md, no post-mortem form, pre-dates the workflow); first real-model attempt
- Status: ready (Q0 gate passed locally, see below; the hub Q0 is re-run before S2_pilot is queued because the coordinator checks the hub)
- Question and practical decision this run informs: does one small open model, acting as the honest agents, show the memory-length regimes the scripted tanh-over-memory rule predicts after a perfect purge (memory 1 drifts back, full memory freezes)? Decides whether the full S2 on this hypothesis (if accepted) is worth budgeting on a model at all, and what the real tokens-per-call are.
- Expected finding: memory 1 returns toward the original after purge (delta_original > 0), full memory stays where capture left it (delta_original about 0). Plausible negative: the model has a string prior strong enough that one word wins regardless of memory (the yang-2026-when artefact), or an 8B model copies the last word heard and memory length does nothing. Uninformative if: capture never happens at the carried-over doses (then the removal question cannot be asked), or validity < 0.90.

## Design and assessment

- Closest relevant evidence and strongest comparator: scripted S1b cells W1_INSIDE/0.42/memory 1 and W1_INSIDE/0.54/full (frac_original_T under A1_purge 0.312 and 0.245; delta_original about +0.24 and 0.00). Comparator inside the run: A0_no_purge on the same prefix.
- Units: unit of assignment = (task, seed) draw; unit of analysis = episode (arm x memory x draw); cluster = task. Arms are paired exactly: the prefix (entrench + takeover) runs once per episode and both arms fork from its end state (new in this attempt, `sim.simulate_prefix` / `simulate_arm`, bit-identical for the scripted policy, selftest check 12). Memory 1 and full share the matching schedule but NOT the model's samples, so the memory contrast is paired on draws only in the scripted sense; for the model it is a between-condition comparison over the same 6 tasks.
- Task/label coverage: dev tasks 0 to 5, seed 1. Word pairs: ruvo/brisk, teru/quon, pira/brisk, sello/pira, olam/quon, ruvo/olam; the original alternates with task parity. Holdout untouched.
- Treatment / manipulation check: capture is measured (honest fraction on the attack word >= 0.75 for 3 rounds). Doses are the scripted dose-rule values carried over (0.42 -> k = 5 of 12 for memory 1; 0.54 -> k = 6 of 12 for full) because the model-side sweep from the pre-registration section 10 has not been run. This is a stated deviation: the pilot cannot claim the doses are at the model's threshold.
- Evaluator correctness, truth separation: `sim.evaluate` runs after the decisions; the prompt carries only the two words and the heard list (no h, no "original" label). Negative control: A0_no_purge. Clean competence: Q0 (below).
- Primary metric: none declared for the pilot (design.yaml `primary_contrast.pilot_note`). Reported: frac_original_T and delta_original under A1_purge per memory, A0 alongside, capture rate and latency, with a cluster bootstrap over 6 tasks (CIs will be wide and are reported as such).
- Timing semantics: simulated rounds; eval at round 50 after the intervention.

## Changes and unresolved issues

| Issue / prior evidence | Change or diagnostic | Expected effect | Acceptance check | Owner |
|---|---|---|---|---|
| Arms re-ran the prefix separately; under a sampled policy they would diverge before the intervention | Prefix fork in sim.run_episode | Arms share capture status under any policy; ~30% fewer calls | selftest 12: forked == per-arm for scripted; S1 sample bit-identical to pre-change output (600 records) | sol-capture, done |
| Adapter reserved cost but never read actual usage; call cap was per policy object | Budget ledger with reservations, actual usage from `usage` (OpenRouter `cost`), refuses past either cap, shared per worker process, saved to a file | Spend bounded at the human cap, actual $ recorded | selftest 10: caps refuse, usage booked; Q0 ledger has actual_usd | sol-capture, done |
| Q0 attempt 0 (36 calls): 3 replies were 'brusk' for 'brisk' (92% exact) | Edit-distance-1 fuzzy accept (counted), then one re-ask, then invalid | Validity >= 0.90 | Q0 attempt 1: 153 calls, 150 exact, 3 fuzzy, 0 re-asks, 0 invalid; probe over all 6 word pairs: 60/60 | sol-capture, done |
| Doses not fitted on the model | None in this attempt (budget and time) | Risk: full memory does not capture within 120 rounds at k = 6 | Report capture rate; if 0 captured, the removal contrast is reported as not askable | open |
| No live visualization | Final-frame only: per-episode traces in episodes.jsonl, summary tables in results/S2_pilot.md; hub run metrics as progress | Enough for 12 episodes | Post-mortem lists the artifacts | open |

## Frozen execution plan

- Protocol: design.yaml `stages.S2_pilot` (v1.2), cfg N = 12, entrench 10, takeover cap 120, recovery 50, eval 50; arms A0_no_purge, A1_purge; memories 1 (dose 0.42) and full (dose 0.54); W1_INSIDE; tasks 0 to 5; seed 1. Code commit stamped on every record.
- Model: `meta-llama/llama-3.1-8b-instruct` via OpenRouter (provider sort by price, fallbacks allowed), temperature 0.7, max 8 output tokens. Prompt = `model.SYSTEM` + the three-line user message in `HTTPPolicy.__call__`.
- Exact commands (from the note dir, hub env from the private agentops secret, model key from a local file via `SWARM_MODEL_API_KEY`, config via `SWARM_MODEL_CONFIG`):
  `python3 src/coordinator.py stage Q0 --backend http --go "Shadow, 2026-10-04 03:30Z"`, worker `python3 src/worker.py --hub --backend http`, then `stage S2_pilot` the same way, then `python3 src/analyze.py --stage S2_pilot`.
- Caps: human cap max_cost_usd = 5, max_calls = 26,000 (the README worst case). Enforced per worker process: 4 workers each get max_calls 6,500 and max_cost_usd 1.25, so the sum cannot exceed the cap even if the workers never talk to each other. Expected: ~15K calls, ~2M input tokens, ~0.04 USD at the 0.02/0.04 per M list price actually routed to (reservation uses 0.05/0.08).
- Retry, stop, missing data: one transport retry, one parse re-ask, no episode retry; invalid episodes are recorded and counted; a worker that hits a cap raises ModelFailure into the episode and stops taking runs cleanly when its cap is spent.
- Regression checks: selftest 46+ checks pass at the stamped commit; scripted S1 sample identical before/after the refactor.
- Server: sim-shadow is unreachable (port 22 refused at 03:50Z) and no other fleet box is free of an exclusive claim; the run goes on shadow's own box (shad0wbot, 16 cores), as S1b did. No agentops claim is held. Artifacts: hub experiment `capture-memory`, runs tagged S2_pilot, episodes.jsonl + summary.json per run; tables in results/.
- Gate decision: Q0 validity >= 0.90 passed (1.00). If S2_pilot capture rate is 0 for a memory, that memory is reported as not askable at the carried dose and no contrast is claimed.

## Visualization mapping

Final-frame, static. Signals: `trajectory.series_original` per episode (honest fraction on the original per round), event markers `entrench_end`, `capture_round`, `removal_round`. Encoding: one table per memory with the mean post-removal trace at rounds 1, 5, 10, 25, 50 under A0 and A1 (results/S2_pilot.md), plus per-episode rows. No animation: 12 episodes, the question is about two numbers per episode. Missing/failure: invalid episodes appear with their error string. Synthetic validation: the same analyzer ran on 38,400 scripted episodes (S1b).
