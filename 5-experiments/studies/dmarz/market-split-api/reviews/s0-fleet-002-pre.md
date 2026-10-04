# Pre-run assessment: s0-fleet-002

Experiment market-split-api; owner dmarz/market-split; S0. Status: ready. Read q0-001-post.md (four paid calls, two note-limit failures). This is the regression gate for v2 before any more paid work.

## Design and assessment

Unchanged market physics, controls, metrics, paired shocks and evaluator-only truth. New prompt states the exact existing price/profit equations and requests an <=80-character note, while hard validation still rejects >200. No best-response solution or firm-splitting suggestion enters the prompt. Model remains Haiku4.5; source hashes are recorded at dispatch. Fresh tasks22/23, seed31, three regulators, two arms, eight rounds: six mock bundles/12episodes/96mock calls. S1 and holdout unchanged. Expected full validity and preserved split/locked contrast; any failure blocks Q0.

## Frozen execution plan

Run src/selftest.py (11 network-blocked groups, including exact note-limit regression), then coordinator.py stage S0 --attempt s0-fleet-002 and worker.py --attempt s0-fleet-002 --max-runs 6. Commit this ready review and changes first. One finite worker, two-hour safety timeout, no real credentials, zero API calls. Existing exclusive sim-dmarz-2 claim dmarz-market-split-api must remain merged/unexpired. Same pinned runtime and reporting. Retain new attempt directories and previous failures; no retries. Verify all uploaded/recovered bytes and replay. Require all six bundle validity/competence/visual checks before separately reviewing Q0-002. Ledger stays untouched at four paid calls.

## Visualization mapping

Unchanged market-split-api-v1 rendering, bound to task22/23 seed31 and regulator/arms per run. Live12s PNG, final1800×1200 PNG and eight-round1080×720 GIF; mock labels, recorded output/firm boundaries, HHI, registration, profit/fines. Actor sees none of the evaluator overlay. Missing/failed states remain honest. Hash/frame/metric checks and browser playback required, with sequential-arm logical-clock caveat unchanged.
