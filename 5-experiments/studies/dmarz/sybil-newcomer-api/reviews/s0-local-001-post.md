# Post-mortem: s0-local-001

Experiment sybil-newcomer-api; owner dmarz; scripted S0, 2026-10-04 UTC. Source fingerprint `44d0153075b6dbe5ade84b1bb84ac2dc5912bf84f711e0f134cb96ed6ae91477`. Disposition: repair-and-rerun engineering harness and amended analysis, then proceed to remote qualification.

198 planned → 198 started → 198 terminal → 198 graded/analyzed, no failures or missing observations. Zero model calls, zero tokens and zero spend. Recorded collection time 3.29 seconds, plus rendering/analysis. All 36 clean qualification packets were exactly correct, including every missing-field abstention. All eight logical replay frames and final image rendered without reporting errors. No scientific API inference follows from this scripted stage.

A concurrently completed seven-test suite had six passing tests and one assertion failure: the malformed-output mock test expected the old per-study duplicate error name, while the new parent cross-study guard correctly rejected the repeated call earlier as `duplicate_shared_call`. The original malformed call was accounted once; no real HTTP occurred. This is a stale harness expectation, not a billing escape. The test now checks the shared guard's precise error and unchanged one-attempt count. Also add the parent's requested prespecified 1→16 identity contrast, policy-by-identity interaction, duplicate ID rejection and missing-outcome accuracy bounds before the final freeze. These are reporting/design completeness changes, not policy tuning from the scripted result.

## Failure and repair ledger

| ID | Evidence and cause | Repair and acceptance | Status |
|---|---|---|---|
| N-01 harness | Expected duplicate_call_refused; observed duplicate_shared_call after shared guard integration | Update exact expected category; rerun suite, require one reserve and one billed response | Pending final run |
| N-02 analysis completeness | Main contrast did not directly report fixed-resource identity splitting | Add prespecified paired identity effects/interactions and duplicate/missing bounds; test and preserve prior attempt | Pending final run |

VISUALIZATION.md v1 is unchanged. Full initial/pre-switch/switch/final inspection and deployed playback follow the final runtime S0. This output remains preserved as a distinct prior attempt. Next: s0-local-002 after all regression tests pass; fresh remote S0/Q0 still required for the frozen runtime.
