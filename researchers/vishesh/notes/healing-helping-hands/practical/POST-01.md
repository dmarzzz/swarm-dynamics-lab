# Post-mortem: practical-01

2026-10-04 UTC / exploratory S0 / vishesh/codex-regrowth-docs. Parent pilot-03. Executed source 51ca83d4d087c686903de67bd6c784dcb375c084; [pre-run](PRE-RUN.md), [plan](PLAN.md). Disposition: **complete-valid-result for computation; reporting repaired; capacity sensitivity is the next diagnostic**.

180 assigned, started, completed, graded and analyzed; no failed or missing worlds. Runtime 127.544 seconds, zero model calls/tokens/spend. Independent arithmetic checks and deterministic replay reproduced all 180 worlds / 5,400 frames. All 36 paired event blocks agree; 40 new documents, 20 genuine withdrawals where intended, and 100 central clients disconnected during rounds 10–19 were verified. No verified-policy false invalidations occurred. Central verified final error was zero except with missing lineage.

## Results against plan

Mean post-event incorrect-or-missing queries, averaging two placements within each of three known corpora:

| Scenario | Central append | Central verified | Peer append | Peer blind | Peer verified |
|---|---:|---:|---:|---:|---:|
| Benign learning | 0.0% | 0.0% | 30.5% | 30.5% | 30.5% |
| Genuine withdrawal | 33.3% | 0.0% | 48.4% | 38.1% | 38.1% |
| Forged notice | 0.0% | 0.0% | 33.2% | 41.9% | 33.2% |
| Missing lineage | 33.3% | 33.3% | 48.4% | 48.4% | 48.4% |
| Central outage | 37.5% | 16.6% | 48.4% | 38.1% | 38.1% |
| Combined | 37.5% | 16.6% | 48.8% | 41.9% | 39.3% |

No scenario meets the prospective utility rule for peer-verified versus central-append. Combined final new-evidence retention is 36.2% for peer arms versus 100% for central arms. Peer-verified uses about 60,394 transmitted item copies versus 50,307 for central verified. False notices cause approximately 178 peak active-root invalidations per combined peer-blind world; verified policies cause zero. Missing lineage leaves stale evidence in both verified architectures. These adverse findings remain valid and must not be overwritten or reclassified as successful swarm evidence.

Central bulk reads and capped mesh packets are deliberately unequal latency/traffic mechanisms. This study therefore identifies a weakness of this particular bounded all-to-all gossip implementation, not an intrinsic theorem that central systems dominate distributed systems. Semantic corpora are reused and small. Authentication is supplied fixture metadata, not an implemented security protocol. The interpretation is a systems diagnostic, not fresh model qualification or generalization.

## Failures and repairs

The outer, untracked reporting wrapper passed unsupported `host=` to the SDK. All 14 live reports raised TypeError before dispatch; local computation and histories were unaffected. The failed process record `practical-01-reporting-failure` preserves that violation. Corrected host configuration through SWARM_HOST, followed by acknowledged start + metric + readback, succeeded. The new tracked reporting adapter rejects host kwargs, requires acknowledgements and records safe error types. Three regression tests pass. This cannot retroactively restore live visibility; current records are explicitly retrospective. The adapter must be exercised before any subsequent computation.

H3 renderer delivered 30 measured animation frames and a final comparison for every seed/layout/scenario. Rendering was extended after execution to export all 36 final comparisons; input/renderer/template hashes identify derived artifacts separately from executed source. Browser and public upload checks are recorded in the final publication audit. No inference rerun occurred for rendering or reporting.

## Next diagnostic

Practical-02 asks whether the adverse mesh outcome is sensitive to the arbitrary four-item packet cap. Change only cap 4→16, retain all five arms, six scenarios, seeds, placements and scoring; preserve central controls and compare traffic as well as accuracy. Do not claim a generic advantage if a capacity change buys accuracy through more traffic. Same semantic inputs means this is a paired engineering sensitivity analysis, not new independent replication. Register the amendment and pre-run assessment before execution. Qwen/Laya and missing-lineage limits remain unresolved and are not repaired by increasing capacity.
