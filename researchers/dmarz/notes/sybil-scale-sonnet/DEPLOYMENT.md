# Deployment record

Server sim-dmarz-3 (dmarz fleet), exclusive claim `dmarz-sybil-scale-sonnet` held by dmarz/scale-sonnet (agentops PR 164, merged 2026-10-04 ~05:35Z, until ~13:35Z). Private launcher: agentops `scripts/run-sybil-scale-sonnet.py`. Host paths: /srv/swarm/sybil-scale-sonnet-lab (detached checkout), -venv, -budget (persistent ledger). Addresses, credentials and ledger contents are kept out of this repository.

| Time (UTC) | Action | Revision | Result |
|---|---|---|---|
| 05:35 | claim merged (agentops PR 164) | — | exclusive, sim-dmarz-3 idle, no worker |
| 05:35 | launcher setup | f18f66da | detached checkout, venv, 9/9 selftests |
| 05:35 | fleet S0 launched, run sybil-scale-sonnet/55c86cfa | f18f66da | runtime a1a619f7… (matches local) |
| 05:37 | fleet S0 done 264/264; publish + verify pass | f18f66da | 10 artifacts verified |
