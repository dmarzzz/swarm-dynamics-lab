# Search scope and evidence register

Accessed2026-10-04. Bounded novelty search, not a systematic review or priority claim. No paper implementation or benchmark was executed. Sources may be revised after this snapshot; claims below refer to the opened versions. Existing library entries may reflect deeper reading by their original owner; this table describes only this pass.

## Closest primary work

| Source opened | Actual reading in this pass | Consequence for the design |
|---|---|---|
| [Towards a Science of Scaling Agent Systems, v3](https://arxiv.org/html/2512.08296v3), [[kim-2025-towards]] | Abstract, introduction and selected validation/complexity passages; not full methods | Task-conditioned architecture choice and compute-controlled scaling are already central questions. Need a narrower incremental contribution. |
| [Ringelmann Effect, v1](https://arxiv.org/html/2606.02646v1), [[bertalanic-2026-ringelmann]] | Abstract/overview only | Nominal count versus effective diversity is prior art; independent resampling is a necessary conceptual control. No fitted law is adopted here. |
| [AgentSpawn, v1](https://arxiv.org/html/2602.07072v1), [[costa-2026-agentspawn]] | Abstract and selected spawning/evaluation sections | Adaptive spawning, memory transfer and coherence are close overlap. Do not claim adaptive teams as new. |
| [CoAgent, v1](https://arxiv.org/html/2606.15376v1), [[lyu-2026-coagent]] | Abstract, introduction and selected protocol/tool sections | Strongest novelty threat: stale shared state and conflict repair. Compare contraction against competent synchronization, not uncontrolled concurrent writes. |
| [Silo-Bench](https://arxiv.org/abs/2603.01045), [[zhang-2026-silo]] | Abstract page | Scaling distributed coordination is already benchmarked; additional nominal workers alone are not a contribution. |
| [Delegation Danger Band](https://arxiv.org/abs/2610.00041) | Abstract page only | Inherited stale context is already a research topic. Do not claim the existence of stale-context harm as novel. Metadata displayed a submission-date/identifier-month mismatch; do not use it to assert publication priority without further verification. |
| [Gaia2, v1](https://arxiv.org/html/2602.11964v1) | Overview and selected verifier, timing and parallel-tool passages | Dynamic environments and action-level checking are precedents. Use independent state predicates, timing and safe negative fixtures. We have not reproduced its verifier. |
| [ITBench](https://arxiv.org/abs/2502.05352), [[jha-2025-itbench]] | Abstract | Practical incident structures are available; importing their difficulty wholesale risks another competence floor. |
| [SWE-bench Pro official project](https://scaleapi.github.io/SWE-bench_Pro-os/) | Project page, not dataset/code execution | Source-backed repository tasks and repository-disjoint splits are preferable to renamed toy arithmetic. No current leaderboard ranking is relied on; its page contains historical and newer results. |

## First-party engineering observations

| Source | Read scope and evidential status | Use |
|---|---|---|
| [Cursor: Scaling long-running autonomous coding](https://cursor.com/blog/scaling-agents), Wilson Lin, Jan14 2026 | Coordination and lessons sections; vendor engineering account, not controlled causal evidence | Realistic contention, overlong work and hierarchy motivate transition/overhead tests. |
| [Anthropic: How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system), [[anthropic-2025-how]] | Selected cost, effort allocation, dependence and tracing sections | Charge all coordination and use full traces; general scaling claims require controlled comparisons. |
| [Microsoft: Scale agents with shared skills and tools](https://learn.microsoft.com/en-us/agents/architecture/scaling-agents-shared-skills-tools) | Architecture/scale-down guidance | Ordinary service scale-down is already established practice. Our candidate concerns within-task stateful coordination, not traffic-driven replica autoscaling. |
| [Coding-Agent State Protocol: The Agent Wasn't Wrong About Its Own Work. It Was Wrong About Yours.](https://codingagentstateprotocol.com/blog/stale-belief-agent-shared-state.html), Aug18 2026 | Incident examples and explanation; first-party observations, not randomized evidence | Include semantically stale dependencies across different files, not just line-level merge conflicts. Do not infer an incidence rate from this account. |

## Twitter/X search and limitations

Searched indexed X pages for agent scaling, coordination tax, Cursor parallel agents, Boris Cherny parallel workflows and stale shared state. Results were sparse and noisy; some returned unrelated pages. Accessible index text is not an authenticated timeline or a complete thread. Direct opening of the Cognition post failed. No X thread is catalogued as fully read, reproduced wholesale, or used as causal evidence.

Relevant leads:

- [Cognition on Agent Trace](https://x.com/cognition/status/2017057457332506846): indexed first-party announcement about code/context provenance. Supports traceability as a practitioner interest; no scaling-effect claim taken from it.
- [X summary of Cursor's browser experiment](https://x.com/i/trending/2012848875342627132?lang=en): platform-generated summary, not a primary experimental source. Followed to the actual Cursor engineering article instead.
- [Indexed discussion quoting Boris Cherny](https://x.com/wildmindai/status/2038617731054932436): feature discussion, not an experiment or novelty result. Excluded from technical evidence.

This search satisfies exploration of the discussion, not exhaustive X coverage. Important missing coverage: full threads/replies, recent unindexed systems papers and complete methods/reproduction of the closest competitors. Those limits prevent a strong novelty claim.

## Query groups retained for reproducibility

1. Multi-agent scaling, task topology, optimal number of agents, coordination overhead.
2. Dynamic agent population, adaptive spawning, retire/shrink/scale down.
3. LLM shared-state concurrency, stale state, delegation, synchronization.
4. Hysteresis and dynamic team sizing; service autoscaling distinguished from within-task teams.
5. Gaia2 asynchronous environments, ITBench incident tasks, SWE-bench Pro multi-file changes.
6. Site-restricted X queries for coordination, parallel workflows and state drift.

Search-result snippets were used to choose primary pages; unverified third-party numerical claims were excluded. Prior-art absence in a query result is not evidence of novelty. Candidate scores in README.md are the owning PI-style assessment, not external ratings.
