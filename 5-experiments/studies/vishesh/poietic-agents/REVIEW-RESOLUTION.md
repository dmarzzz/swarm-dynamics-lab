# Independent review resolution — v0.2

2026-10-04 UTC; author implementation response, not a second independent review. The [different-researcher review](../../dmarz/inbox-reviews-2026-10-04-round2/poietic-review.md) reviewed source `6392174e`; it requested revisions and explicitly allowed the owner to resolve them without another routine reviewer.

| Finding | Resolution | Executable evidence |
|---|---|---|
| P1 adaptation delay | Fixed 120-second exogenous arrivals; next-batch deadlines never move; all setup, reporting and proposal time counts | `released_jobs`, `lineage.run_lineage`; delayed-boundary and runtime-clock tests |
| P2 reuse beyond caching | Three public hand-computed cases; raw and derived memoization in A1; cache keys use source/schema/program and only referenced parameters | SCENARIOS.md; generic join/parameter-independence, no-reuse and provider-reuse tests |
| P3 stage criteria | S1 recovery 5/6 in two consecutive post-change epochs; advance only with 43/48 in every root for A3 and a comparator plus executed change and intact controls | AMENDMENTS.md and design.yaml; 7,200 lineage + 400 construction + 400 instrument quota allocation |
| Stronger baselines | AgentSlimming-informed prune/replace listed in A2 development menu; MANTA-informed trace repair in deferred A4; construction cost must be supplied | No fidelity/novelty claim. Actual A2 selection remains a post-S0 development gate, not a fabricated result |
| Jev/interface fidelity | Finite actions only; 12 dependent four-step cases per contract; tool restore, service delivery and installed procedure actually execute | qualification.py and native.py, development lifecycle tests |
| A5 | No structural proposal calls once frozen; dependent copied prefix; bill physically once, allocate to each hypothetical deployment | engine.fork_frozen, prefix_accounting, lineage arm guard |

The small executable workload uses 4/6 repeated occurrences versus 0/6, disclosed as a prospective amendment from approximate 80/20 targets. Generic multi-API joins are covered by explicit capability fixtures, not claimed as a broad pilot distribution. A favorable S1 result on this restricted workload would justify only broader development.

47 offline checks passed when this response was written. The current exact count and hashes are in VALIDATION.json. No model, S0, S1 or S2 responses exist. The researcher-review requirement is satisfied for design; S2 still needs the formal research gates and any scope-specific review required then.
