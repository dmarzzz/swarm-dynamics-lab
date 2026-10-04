# Ready queue

Maintained by dmarz/pipeline. Each row is an experiment package prepared in full before a server is free
(contract: [READY-CHAIN.md](READY-CHAIN.md)). "Filed" means a run request with the label
`run-queue:ready` exists in the private run queue after dmarz/fleet-monitor's same-researcher check; from
then on the orchestrator launches it and reports on the request. Nothing in this file launches a run, and
no package here has been independently reviewed. Last updated 2026-10-04T09:12Z.

| Study | What it tests | Calls (P0 / Q0 / S1) | Expected cost and time | State | Request |
|---|---|---|---|---|---|
| [sybil-scarcity-opus](../sybil-scarcity-opus/README.md) | Carriers per rare fact (81 to 1) at 972 identities | 1 / 48 / 1,440 | about USD 150; 45 to 80 min | Filed 09:13Z at launch commit 3ebef1ce (source hash b37af997) | run queue 248 |
| [sybil-split-opus](../sybil-split-opus/README.md) | One attacker's fixed resources split over 1, 3, 9 or 27 identities; degree, random and coverage checks; two graph families | 1 / 60 / 2,688 | about USD 45 to 60; time in its pre-run review | Code and offline checks on main (88fcf92a); pre-run review being written; not yet checked by the fleet monitor | none yet |
| false-alarm-cascade | A planted false honeypot alarm in a six-member team; abandonment, spillover and survival of the false belief after a correction | 1 / 24 / 3,600 (planned) | to be estimated | Being built (task build-false-alarm-cascade) | none yet |
| quota-splitting | Identity splitting for a per-identity quota (agent-budgets hunch B2) | to be set | to be estimated | Design brief drafted; not claimed, not started | none yet |
