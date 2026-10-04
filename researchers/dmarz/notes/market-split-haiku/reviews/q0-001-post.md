# Post-mortem: q0-001

Experiment market-split-haiku; owner dmarz/market-split; Q0; 2026-10-04. Parent i0-002; read q0-001-pre.md. Disposition: advance to S1-001.

## What ran and what happened

Two planned bundles started and finished, four episodes graded, no duplicates or missing episodes. All four were valid, profitable and above the unchanged 75% reference floor. Task 62 locked/dynamic ratios were 0.999809811 and 0.978075352; task 63 locked/dynamic were 0.999762356 and 0.999788201. No portfolio registered another firm. Thirty-two calls cost $0.229196, with zero retries or unpriced calls. The cumulative study ledger retains 40 attempts and $0.274935, including the failed first mechanics probe. Model claude-haiku-4-5-20251001 used native thinking 2048, total output 3072 and no temperature override.

## Visualization and integrity review

Both bundles have all 14 artifact hashes verified against the hub and recovered locally. Final frames are 1800×1200, replays are 1080×720 with all eight logical rounds; the task-63 final frame was visually inspected. Metrics and initial/final time coverage agree with saved traces. Exact re-execution under pinned Python 3.12 reproduced all 32 actor observations/actions and all four traces/evaluations. Run IDs: market-split-haiku/797e79233004 and market-split-haiku/ed5390f85ec0. Mapping market-split-api-v1; no missing or repaired observations. The public UI has intermittent connection trouble, tracked separately; local replays and hub receipts are durable.

## Experiment quality and next run

This establishes this configuration's declared competence gate on fresh unregulated tasks 62/63. It does not show optimality in every market or spontaneous discovery, since no enforcement was present. Sonnet qualification was not substituted for this model's own evidence. All 16 offline checks, 12 mock episodes and six fresh mechanics checks also passed. Ordinary prompt, simulator, evaluator, resources and information budgets match Sonnet V5. Probe-only instructions never enter ordinary episodes. Earlier unqualified non-thinking configurations remain reported separately.

H2 is resolved by this 4/4 qualification. No new execution, accounting, renderer or competence failure arose. Next is the already frozen S1-001 comparison on tasks 36–41, seed 41, three rules and two arms, 24 rounds each: 36 episodes and 864 calls. A valid null finishes the pilot; it is not grounds to retune or rerun. No holdout or S2 use. Source c0c1fff06e1fe4c8244b17667e7317392b35ea0686dd4c616a3f860f4ccfee96; design 7995afceebefe0d2995918025b9c3f555e387cbe179734f67ee379e2dbd4f6b0. Preserve max 1000 attempts and the one shared owner $500 authorization. Main dispatch requires its committed pre-run review and current exclusive host claim.
