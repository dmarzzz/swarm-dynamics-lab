# Ready queue

Maintained by dmarz/pipeline. Each row is an experiment package prepared in full before a server is free
(contract: [READY-CHAIN.md](READY-CHAIN.md)). "Filed" means a run request with the label
`run-queue:ready` exists in the private run queue after dmarz/fleet-monitor's same-researcher check; from
then on the orchestrator launches it and reports on the request. Nothing in this file launches a run, and
no package here has been independently reviewed. Last updated 2026-10-04T10:40Z.

| Study | What it tests | Calls (P0 / Q0 / S1) | Expected cost and time | State | Request |
|---|---|---|---|---|---|
| [sybil-scarcity-opus](../sybil-scarcity-opus/README.md) | Carriers per rare fact (81 to 1) at 972 identities | 1 / 48 / 1,440 | actual USD 141.14; chain 09:17Z to 10:01Z | Finished: all four stages done, verify ok, [results](../sybil-scarcity-opus/RESULTS.md) | run queue 248 |
| [sybil-split-opus](../sybil-split-opus/README.md) | One attacker's fixed resources split over 1, 3, 9 or 27 identities; degree, random and coverage checks; two graph families | 1 / 60 / 2,688 | USD 45 to 60; about 50 to 80 min | Filed 09:31Z at launch commit 75d51695 (source hash 95889bea); chain started 10:12Z by the orchestrator | run queue 252 |
| [false-alarm-cascade](../false-alarm-cascade/README.md) | A planted false honeypot alarm in a six-member team; abandonment, spillover and survival of the false belief after a correction | 1 / 24 / 3,600 | about USD 120; about 2 h | Paused at c1de1da6 for program v5 (code with failure handling done, selftest 38 OK; documents, reruns, model ladder and review left) | none yet |
| [quota-splitting](../quota-splitting/README.md) | Identity splitting for a per-identity quota (agent-budgets hunch B2) | 1 / 96 / 3,456 | USD 45 to 90 | Paused at 6b9adefa for program v5 (code with failure handling done, selftest 71 OK; documents, reruns, model ladder and review left) | none yet |
| [sybil-scarcity-synth](../sybil-scarcity-synth/README.md) | Follow-up to sybil-scarcity-opus: effort low or high, original prompt or one frozen evidence rule, fresh roots | 1 / 48 / 960 | about USD 110 to 140 | Being built (task build-sybil-scarcity-synth); plan with the frozen rule on main | none yet |
| trust-credit-qwen | Program v5 line T: does propagating pass credit to neighbours admit extra attackers? 24 roots, three admission rules on one frozen audit | 1 / 23 / 504 | under USD 2 | Being built (task build-trust-credit-qwen), qwen/qwen3.7-flash via OpenRouter | none yet |
| verify-cost-qwen | Program v5 line V: checking versus exploring as reliability and cost change; 24 layouts x 12 cases x 2 formats | 1 / 23 / 576 | under USD 2 | Being built (task build-verify-cost-qwen), qwen/qwen3.7-flash via OpenRouter | none yet |
| memory-handoff-qwen | Program v5 line M: can a successor repair inherited false memory? 24 roots x 6 memory states x 4 handoff policies | 1 / 23 / 576 | under USD 2 | Being built (task build-memory-handoff-qwen), qwen/qwen3.7-flash via OpenRouter | none yet |
