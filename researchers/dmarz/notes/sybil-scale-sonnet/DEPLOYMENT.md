# Deployment record

Server sim-dmarz-3 (dmarz fleet), exclusive claim `dmarz-sybil-scale-sonnet` held by dmarz/scale-sonnet (agentops PR 164, merged 2026-10-04 ~05:35Z, until ~13:35Z). Private launcher: agentops `scripts/run-sybil-scale-sonnet.py`. Host paths: /srv/swarm/sybil-scale-sonnet-lab (detached checkout), -venv, -budget (persistent ledger). Addresses, credentials and ledger contents are kept out of this repository.

| Time (UTC) | Action | Revision | Result |
|---|---|---|---|
| 05:35 | claim merged (agentops PR 164) | — | exclusive, sim-dmarz-3 idle, no worker |
| 05:35 | launcher setup | f18f66da | detached checkout, venv, 9/9 selftests |
| 05:35 | fleet S0 launched, run sybil-scale-sonnet/55c86cfa | f18f66da | runtime a1a619f7… (matches local) |
| 05:37 | fleet S0 done 264/264; publish + verify pass | f18f66da | 10 artifacts verified |
| 05:39 | Q0 done 64/64, all sizes pass; USD 1.98 actual; publish + verify pass | f18f66da | run 5fe6c41a |
| 05:40 | S1 launched, run sybil-scale-sonnet/afd8d5b9; 79/2400 valid at 05:45, 0 failed | f18f66da | expected ~20 min, ~USD 50 actual |
| ~06:05 | S1 complete: 2400/2400 valid, 0 failed; worker exited | f18f66da | S1 USD 56.271264; study USD 58.254702 over 2464 calls |
| 07:30 | Close-out: publish+verify passed, local recomputation matches, RESULTS and s1-001-post written; claim dmarz-sybil-scale-sonnet released | f18f66da | no further model calls |
