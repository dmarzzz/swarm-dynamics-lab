# Pre-run assessment: s0-a1 (scripted fixtures on the fleet)

- Experiment / owner / stage: soc07-private-judgments / dmarz (agent dmarz/soc07-private) / S0, scripted, zero model calls.
- Parent attempt: local-s0-001 on the builder's machine (Python 3.12.13, Pillow 11.3.0): 69 of 69 checks passed, 54 unit tests passed with 1 skipped (the approval-pinning test, which needs the review documents). First attempt on the fleet.
- Status: **ready** as an engineering rehearsal. It needs no review go because it cannot call a model: the scripted stage takes no credentials and the launcher refuses to pass any.
- Question this run informs: do the generator, access rules, scorer, ledger and hub reporting behave on the claimed server exactly as they do offline? It says nothing about any model.
- Uninformative if: it passes offline and on the server for trivial reasons. Guard: the expected outcomes differ by policy, arm and regime (for example the majority-following policy must lose the informed-minority worlds in PRIVATE and PUBLIC and win them in PREPARE), so a scorer that ignored the arm or the regime would fail.

## Design and assessment

- Units: 60 fixture worlds (`s0-w0000` to `s0-w0059`, 20 per regime), disjoint from every S1 world because the stage name is part of the world seed. Four scripted policies x five arms = 1,200 team episodes; 240 replay episodes; 60 single-solver episodes; nine fault runs on three worlds.
- Evaluator: the answer key comes from the generator and is cross-checked for every world by a separately written solver in `src/score.py`. Truth canaries, canonical supplier ids and regime names are searched for in all 5,100 rendered contexts of one full run.
- Controls: always-correct, evidence-following, stubborn and majority-following policies with outcomes fixed in `src/s0.py` before running.
- Timing: logical order only; no wall-time claim.

## Frozen execution plan

- Code: the commit this file ships in; runtime fingerprint printed by the launcher's `setup` step and stamped on the hub run as `source_hash`.
- Command: private launcher `scripts/run-soc07-private.py <commit> setup`, then `... s0`. One finite worker, at most 5 scripted calls in flight, 0 model calls, USD 0.
- Server claim: `dmarz-soc07-private` on sim-dmarz-3 (exclusive). Hub experiment `soc07-private-judgments`, batch `s0-a1`.
- Retry and stop policy: none needed; any failed check fails the run and is preserved. No automatic re-execution (the worker refuses a second hub attempt).
- Gate: all checks pass. If any fails, write the post-mortem, repair, and run a new batch.

## Visualization mapping

Mapping v1 (full table in `reviews/s1-pre.md`). For S0 the bars show the scripted evidence-following policy on the 60 fixtures: correct team decisions per regime and arm as k/20, and pooled revision counts. Time axis of the replay: completed blocks, 0 to 60 in steps of 5 (13 frames). The frame states that it is a scripted policy, not a model. Final 1800x1200 PNG and GIF on the hub; raw episode files stay on the server.
