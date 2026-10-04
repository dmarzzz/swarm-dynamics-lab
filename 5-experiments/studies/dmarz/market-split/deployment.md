# Deployment record

- Experiment: market-split; stage: exploratory scripted S0/S1.
- Source: dmarz/market-split; checkout is isolated under /srv/swarm/market-split/swarm-lab.
- Allocation: sim-dmarz-market-split, dmarz-owned temporary 1-vCPU/2-GB server; access all, SSH only; expires 2026-10-05.
- Exclusive claim: dmarz-market-split, merged agentops PR 34; initial expiry 2026-10-04T04:33:57Z. Allocation recorded in agentops PR 33. No existing server was modified by the reviewed infrastructure plan.
- Resource budget: one finite worker, no persistent polling, no model API credentials or calls; model budget $0. Destroy the temporary host after results, receipts and local recovery copies are verified.
- Local runtime: Python 3.9.6, PyYAML 6.0.3, numpy 2.0.2, matplotlib 3.9.4, Pillow 11.3.0.
- Remote runtime: Ubuntu 24.04 and Python 3.12.3; PyYAML 6.0.3, numpy 2.0.2, matplotlib 3.9.4, Pillow 11.3.0, isolated virtual environment. All 10 self-test groups passed on the actual server with sockets blocked. Full sim blueprint completed with 54 successful tasks, 0 failures and 0 unreachable hosts on the retry.
- Initial server provisioning hit first-boot apt contention. Waited for cloud-init to finish and reran the normal scoped provisioning; did not interrupt package locks.
- No server addresses, hub endpoints or credential values are included here. Reporter reads its credentials from /etc/swarm/report.env.

- Initial hub registration stopped before queueing because the optional reporter credential task had been skipped. SOPS decryption was verified without printing secrets; the reporter role passed with an explicit repository/key path (8 tasks, 0 failures), and the credential file was written through its standard template. No experiment episodes or model calls occurred in that failed setup step.

## Run reconciliation

Local s0-local-001 and s0-local-002 are retained separately; the evaluator repair is recorded in their reviews. Fleet S0 used only the corrected evaluator.

- s0-fleet-001: three runs, 18/18 valid episodes; source dd99268244e3d48ce8750ea1e336709cfd0089c8.
- s1-fleet-001: twelve runs, 432/432 valid episodes; source 6ca3f16ef9f3a0dbad0ed280c032e78e31195dc3.
- Engine SHA-256 shared by both: 8abdfb4e59787213c4518f662af3976a2af31f11904ead4582afd51a3f260312.
- Design SHA-256 shared by both: fd5aac6f164ec61a0145245a1277ffc025670de250aebcc4a9eed1d447a29263.
- All 15 simulation runs have complete traces, progress/final PNGs and full-round GIFs. All 90 artifact hashes were checked against server files and again against downloaded local recovery copies. Reconciliation manifests and aggregate S1 diagnostics are committed in analysis/. Raw recovery copies remain in ignored results/fleet-all and results/fleet-s1; hub copies are retained independently of the temporary worker.
- market-split/analysis-s1-scripted-v1 is a separate reporting run with verified analysis.json, cells.csv and reconciliation.json uploads. It does not add a simulation or independent replicate.
- One finite worker exited successfully after the 12 S1 runs. No failures, retries, model calls or API spending. Actual browser playback verified representative S0 and S1 GIFs; S1 observed round 1 advancing to round 10.

## Teardown

Claim dmarz-market-split was released as done in agentops PR 42 after worker exit and recovery-copy verification. The temporary sim-dmarz-market-split server was destroyed on 2026-10-04 UTC through the original provisioning checkout and dmarz state. A saved plan was inspected before applying: only the target droplet, firewall, root key resources and generated inventory changed. Apply succeeded; the target is absent from state and generated inventory. All other generated server entries are byte-equivalent after JSON parsing. The simulator results remain on the hub and local disk. Infrastructure cost is separate from the zero model API cost.

The fleet/inventory removal is recorded in agentops PR 45. The public experiment and its stored PNG/GIF artifacts remain accessible after teardown. A future paid pilot must reacquire an exclusive host and set an explicit model budget; nothing is left running for this experiment.

| Stage | Regulator | Threshold | Registration fee | Run |
|---|---|---:|---:|---|
| S0 | none | 0.38 | 20 | market-split/d37a320f |
| S0 | firm | 0.38 | 20 | market-split/07d3a530 |
| S0 | owner | 0.38 | 20 | market-split/803b9107 |
| S1 | none | 0.38 | 20 | market-split/4f5c01e6 |
| S1 | none | 0.38 | 2500 | market-split/2e22ba11 |
| S1 | none | 0.46 | 20 | market-split/003256cd |
| S1 | none | 0.46 | 2500 | market-split/a0c01a75 |
| S1 | firm | 0.38 | 20 | market-split/c473a1f2 |
| S1 | firm | 0.38 | 2500 | market-split/f837b597 |
| S1 | firm | 0.46 | 20 | market-split/edbf1b22 |
| S1 | firm | 0.46 | 2500 | market-split/d4c749f3 |
| S1 | owner | 0.38 | 20 | market-split/9b718064 |
| S1 | owner | 0.38 | 2500 | market-split/571440e6 |
| S1 | owner | 0.46 | 20 | market-split/beb86549 |
| S1 | owner | 0.46 | 2500 | market-split/80dc3fe5 |
