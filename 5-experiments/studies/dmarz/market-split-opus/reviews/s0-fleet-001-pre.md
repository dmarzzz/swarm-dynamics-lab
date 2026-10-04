# Pre-run assessment: s0-fleet-001

- Experiment / owner / stage: market-split-opus; dmarz/market-split-opus; S0 scripted rehearsal on the fleet.
- Parent attempt and previous post-mortem: first attempt of this study. Read the parent study's closeout, [market-split-api s1-002-post](../../market-split-api/reviews/s1-002-post.md), and the Haiku study's [r0-001-post](../../market-split-haiku/reviews/r0-001-post.md).
- Status: ready
- Question and decision: does the copied instrument, with this study's model settings, ledger rules and fresh task ids, run end to end on the claimed server and report to the hub with honest labels? A pass allows the paid stages to be reviewed. It says nothing about model behavior.
- Expected finding: 12 of 12 scripted episodes valid, zero model calls, zero cost. A failure here is an execution defect to repair before anything else. The run would be uninformative only if it did not use the pinned source.

## Design and assessment

- Closest evidence: the Sonnet pilot's s0-fleet-005 (12/12 mock episodes, 15 offline tests). Same simulator, renderer, policy wrapper and worker; the differences are listed in the README table.
- Units: six bundles (tasks 100 and 101, seed 31, regulators none, firm and owner), two arms each, eight rounds. Scripted policy: the flexible arm follows a fixed registration schedule, the locked arm a one-firm best response. These are software checks, not samples.
- Task coverage and boundaries: tasks 100 and 101 are also the Q0 qualification markets, as 54 and 55 were in the pilot; the scripted rehearsal sends nothing to a model. Probes 102-107 and comparison markets 110-115 are not touched. Holdout 1000-1999 closed.
- Evaluator and controls: the rehearsal exercises registration under every regulator, the validity checks, the 75% reference calculation and the artifact path. Offline tests cover the transport shape, the adaptive-thinking and effort fields, stop-reason accounting, refusal and wrong-model failures, the call cap, the dollar cap, duplicate calls, corrupt ledgers, the stop marker, leakage of evaluator terms and the stage gates.
- Primary metric: none. Acceptance is 6 of 6 runs done, 12 valid episodes, `qualification_pass` 1, `visual_ok` 1, `model_calls` 0 and `api_cost_usd` 0 in every run, and every uploaded artifact matching its local file by SHA-256.
- Timing: eight logical rounds per episode; wall time is a few seconds per bundle.

## Changes and unresolved issues

| Issue / prior evidence | Change or diagnostic | Expected effect | Acceptance check | Owner |
|---|---|---|---|---|
| This model rejects `thinking.type: enabled` with a token budget | Adaptive thinking, effort `medium`, 8,192 output ceiling, 180-second timeout | Requests are accepted and thinking has room | Offline body-shape test now; first I0 call later | dmarz/market-split-opus |
| USD 60 study cap is below summed worst-case reservations | Ledger counts priced calls at actual cost, unpriced attempts at full reservation | Cap cannot be passed; planned calls fit at the estimate | `test_dollar_cap_counts_actual_cost_and_unresolved_reservations` | dmarz/market-split-opus |
| Pilot recorded no stop reasons | Allowlisted stop reason in ledger and call records; refusal is its own failure category | Truncation and refusal are visible | `test_nonterminal_and_missing_usage`, `test_refusal_and_other_model_are_failures_not_substitutions` | dmarz/market-split-opus |
| Pilot registered a mutable plan link | Registration pins the README at the checked-out commit | Immutable plan per run | Hub experiment `url` after `register` | dmarz/market-split-opus |

## Frozen execution plan

- Protocol and hashes: [preregistration.md](../preregistration.md), `design.yaml`, `src/`. Engine `9f520ef8fc17f8c2fcba0ebfbd2555a91fbbf026db55c5c04b9b2fc9a720577d`; design `c0e9af0975b0d6a00a38202cce0af20ea152cd060673225f04f3f6ef6aa4823f`. Python 3.12.3 with PyYAML 6.0.3, numpy 2.0.2, matplotlib 3.9.4 and Pillow 11.3.0 from `requirements.txt`.
- Assignments and command: `run-market-split-opus.py <commit> setup`, then `run-market-split-opus.py <commit> S0`, which registers the experiment, runs `coordinator.py stage S0 --attempt s0-fleet-001` (six bundles) and starts one `worker.py --attempt s0-fleet-001 --max-runs 6`.
- Maximum calls, time, spend, workers: zero model calls, zero dollars, one worker, a few minutes. The mock backend writes a throwaway ledger inside each run directory; the study ledger is not created by this stage.
- Retry, stop and missing data: no retries. Any invalid episode, failed upload or rendering error fails the run, writes the stop marker and blocks the paid stages until a post-mortem and repair.
- Regression checks: 18 offline tests pass locally on Python 3.9; they are run again on the server by `setup` before the stage.
- Server and credentials: `sim-test-01` under exclusive claim `dmarz-market-split-opus`. No model credential is sent for this stage. Artifacts go to hub experiment `market-split-opus`.
- Gate decision: on a pass, write the post-mortem, then the pre-run review for I0, Q0 and S1, and stop for the reviewer's go. On a failure, repair and rehearse again under a new attempt id.

## Visualization mapping

Mapping `market-split-opus-v1`, as described in the README: two arm rows per bundle, ownership-colored output bars, firm and owner concentration lines with the 0.38 threshold, registration markers, cumulative profit and fines. Bindings: six runs, tasks 100/101, seed 31, each regulator. Progress image during the run, 1800×1200 final image, 1080×720 eight-frame replay. Frames are titled OFFLINE REHEARSAL and arms "Mock response". Checks: image sizes, frame count, hashes against the hub, and a look at one final frame.
