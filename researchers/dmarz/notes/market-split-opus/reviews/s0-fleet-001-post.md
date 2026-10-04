# Post-mortem: s0-fleet-001

- Experiment / owner / stage / date: market-split-opus; dmarz/market-split-opus; S0 scripted rehearsal; 2026-10-04, about 07:47-07:50 UTC.
- Pre-run assessment: [s0-fleet-001-pre](s0-fleet-001-pre.md). First attempt of the study. Pinned commit `8c27b690b42cf473c65975d58b8ed3d7487730e1`; engine `9f520ef8fc17f8c2fcba0ebfbd2555a91fbbf026db55c5c04b9b2fc9a720577d`; design `c0e9af0975b0d6a00a38202cce0af20ea152cd060673225f04f3f6ef6aa4823f`. No model was called; the backend was the scripted mock.
- Run ids: `market-split-opus/` `58d846a8b412` (task 100, none), `8031ca5cf497` (100, firm), `5327b78d2c4d` (100, owner), `57f9f65421b7` (101, none), `316ce9351da8` (101, firm), `d728a23b8b84` (101, owner). Reproduce with `run-market-split-opus.py <commit> setup` and `S0` on a claimed server.
- Disposition: advance to the pre-run review of the paid stages. No paid stage starts without the reviewer's go.

## What ran and what happened

- Counts: 6 bundles planned, 6 started, 6 done; 12 episodes, 12 valid, 0 invalid; no duplicate or missing attempt. The worker log ends with "completed 6 finite runs" and no stop marker exists.
- Calls, tokens, cost: 0 model calls, 0 tokens, USD 0 in every run (`model_calls` 0, `api_cost_usd` 0, `unpriced_calls` 0). The study ledger was not created. The model key was not sent to the server.
- Offline tests: 18 of 18 passed on the server in the pinned runtime (Python 3.12.3, PyYAML 6.0.3, numpy 2.0.2, matplotlib 3.9.4, Pillow 11.3.0) before the stage, and 18 of 18 locally on Python 3.9.
- Qualification fields: `qualification_pass` 1 and `visual_ok` 1 in all six runs. Scripted flexible-arm profit was 99.3% to 133.3% of the scripted one-firm reference; the locked arm is the reference itself (ratio 1.0).
- Expected versus observed: as expected. The scripted flexible arm registers on a fixed schedule at rounds 4 and 5 under every regulator and ends with three firms, so `fragmentation_dynamic` is 1 in all six runs, including the unregulated and owner-regulated ones. That is the rehearsal script exercising the evaluator, not a finding. The same happened in the pilot's rehearsals.

## Visualization review

- Mapping `market-split-opus-v1`; each run has `progress.png`, `final_frame.png` (1800×1200) and `replay.gif` (1080×720, 8 frames, every frame decoded).
- All 42 uploaded artifacts (7 per run: the three images, `episodes.jsonl`, `calls.jsonl`, `summary.json`, `visualization-errors.json`) match their local files by SHA-256 against the hub's recorded hashes.
- One final frame was inspected (task 100, firm regulator): title OFFLINE REHEARSAL, arms labelled "Mock response", three owned firms after registrations marked at rounds 4 and 5, firm-level concentration falling below the 0.38 line while owner-level stays above it, net 16,888 and fines 2,548 credits. The saved episode records 16,887.81 profit, three final firms and first registration at round 4.
- The public site lists the experiment with the stage label "Scripted rehearsal (no model)", the run message "Offline API rehearsal; zero model calls." and the plan link pinned to commit `8c27b690`. The replay was not played in a browser by me; the frame count and decoding were checked on the server.

## Experiment-quality assessment

- This run tested the instrument, not the question. It shows the copied simulator, worker, renderer, hub reporting, launcher gates and artifact path work on `sim-test-01` at the pinned source. It shows nothing about Opus.
- Not exercised: the real provider path (request acceptance by the API, thinking blocks in the response, the served model string, stop reasons, latency, the ledger with real prices). The offline tests cover the request body and failure handling with a scripted transport only. The first real check is the I0 probe.
- Labelling caveat: the run parameters carry `model: claude-opus-5-5` on these scripted runs because the coordinator copies the design's model into every plan, as the pilot's did. `backend: mock`, the stage label and the run message state that no model was called.
- Evidence metadata is unchanged: score 0, no observed outcomes.

## Failure and repair ledger

| ID / kind | Observed evidence | Cause | Repair | Acceptance check | Status |
|---|---|---|---|---|---|
| none | No failure in this attempt | | | | |

Open study issues O1-O3 are in [ISSUES.md](../ISSUES.md); none is closed by a scripted run.

## Next run

- Next attempt: `i0-001`, parent `s0-fleet-001`, six calls, covered by [phase2-pre](phase2-pre.md). Then `q0-001` and `s1-001`, each gated in code on the one before.
- Blocker: the reviewer's explicit go, and the reviewer's decision on issue O3 (launch from halcyon versus the orbital-one run queue).
