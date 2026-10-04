# Deployment record

- Experiment: market-split; stage: exploratory scripted S0/S1.
- Source: dmarz/market-split; checkout is isolated under /srv/swarm/market-split/swarm-lab.
- Allocation: sim-dmarz-market-split, dmarz-owned temporary 1-vCPU/2-GB server; access all, SSH only; expires 2026-10-05.
- Exclusive claim: dmarz-market-split, merged agentops PR 34; initial expiry 2026-10-04T04:33:57Z. Allocation recorded in agentops PR 33. No existing server was modified by the reviewed infrastructure plan.
- Resource budget: one finite worker, no persistent polling, no model API credentials or calls; model budget $0. Destroy the temporary host after results, receipts and local recovery copies are verified.
- Local runtime: Python 3.9.6, PyYAML 6.0.3, numpy 2.0.2, matplotlib 3.9.4, Pillow 11.3.0.
- Remote runtime: Ubuntu 24.04 and Python 3.12.3; exact package versions and source/config hashes will be recorded after deployment.
- Initial server provisioning hit first-boot apt contention. Waited for cloud-init to finish and reran the normal scoped provisioning; did not interrupt package locks.
- No server addresses, hub endpoints or credential values are included here. Reporter reads its credentials from /etc/swarm/report.env.

## Run reconciliation

Pending fleet qualification. Local runs s0-local-001 and s0-local-002 are retained, with the metric-definition repair documented in their reviews. Only the corrected evaluator will be launched on the fleet.
