# Pre-run assessment s1-fleet-001

- Experiment / owner / stage: market-split / dmarz / exploratory scripted S1.
- Parent: s0-fleet-001; read its post-mortem before committing this assessment.
- Status: ready. All three matching fleet S0 cells passed; PNG/GIF loading and playback were verified in the public UI.
- Question: do the accounting controls and bounded worker remain valid across market fixtures, two thresholds and two registration costs? This is engineering qualification, not spontaneous-agent evidence.

## Design and assessment

Six development markets 10–15 × seeds 21/22 × three regulators × thresholds 0.38/0.46 × fees 20/2500 × three policies = 432 episodes in 12 hub runs, 24 rounds each. Task IDs fix market economics; paired arms get common shocks. No S0 market or reserved holdout is reused. Ownership aggregation is the strongest comparator. Registration conserves capital/capacity and adds real fees and overhead; every owner gets one decision per round. Published observations exclude evaluator-only fine counterfactuals. A cost-sensitive search response is a scripted manipulation check, not behavioral discovery.

## Changes and unresolved issues

No simulator, policy, prompt, evaluator or renderer changes since S0. Only predeclared development fixtures, seeds, horizon, fees and thresholds expand. Model behavior and competence remain untested. A scientific null is never a defect; accounting, missing artifacts or invalid execution require repair.

## Frozen execution plan

Use design.yaml market-split-v1 and the source/config hashes recorded by coordinator. Commit this ready assessment after the S0 post-mortem. Run `python3 src/coordinator.py stage S1 --attempt s1-fleet-001`, then `SWARM_SOURCE=dmarz/market-split ./run-workers.sh`. The coordinator requires all matching S0 cells done, zero invalids and verified final/replay uploads. One finite worker, 12 runs, maximum 20 minutes per stage, 0 model calls/tokens, $0 API budget. Keep exclusive claim dmarz-market-split on sim-dmarz-market-split valid through uploads. Hub credentials only from /etc/swarm/report.env. No paid credentials are read. Invalid episodes retain completed traces and are not retried; a failed run blocks qualification. Reconcile 432 unique records and task-cluster diagnostics before release.

## Visualization mapping

Mapping market-split-v1 is unchanged. Each run binds to first task 10 / seed 21 and its regulator/threshold/fee; all 36 episodes per run remain in episodes.jsonl. Retain every round; upload progress.png no more than every three seconds, final_frame.png at 1800×1200 and replay.gif at 1080×720 for all 24 rounds. Selected traces are fixed before outcomes. Verify registration events, both concentration measures, costs and final metrics. The live UI's PNG/GIF viewer is the embedding target; final PNG is the no-animation fallback. Missing/failed policies are labeled; renderer failure preserves raw data and blocks advancement. Verify all hub receipts and representative real playback before stopping the worker and releasing/destroying the temporary host.
