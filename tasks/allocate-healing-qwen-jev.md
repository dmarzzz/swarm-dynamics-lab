---
id: allocate-healing-qwen-jev
type: task
title: Provision dedicated Healing Qwen plus Jev worker in approved fleet
kind: admin
status: claimed
priority: p0
owner: vishesh/codex-regrowth-docs
for: dmarz
created: 2026-10-03
created_by: vishesh/codex-regrowth-docs
depends_on: []
topics: []
claimed_at: 2026-10-04T06:12Z
updated: 2026-10-04T06:12Z
---

## Goal

Fulfil the owner-requested dedicated allocation for Healing Helping Hands C1 Qwen 0.6B plus Jev. All eligible hosts were reserved; the correct next step is new capacity through the existing Dmarz provisioner, not a Mac fallback or taking another experiment's host.

Requested worker: one CPU-only sim blueprint, preferably 4 vCPU / 8 GiB matching the prior Qwen runtime; 2 vCPU / 4 GiB is acceptable if the provisioner verifies sufficient capacity. One local Qwen 0.6B process, one sequential inference worker, outbound HTTPS and existing private SSH/reporting access; no additional public ports or GPU. Three-hour exclusive allocation with host expiry 2026-10-05; stop workers and release after verified artifacts. Use the established approved infrastructure budget and record the actual resource price before apply. No new account, copied state or personal/default cloud credentials.

The local operator has no Dmarz provisioning credential or authoritative dmarz state. Provision using the existing owner executor/state and account-identity checks documented in private agentops, including duplicate-resource and concurrent-state locking checks. Preserve all existing resources. If the account is at its droplet limit, the fleet owner should resolve capacity through approved retirement or limit workflow; do not tear down a claimed worker.

Study source and immutable plan: https://github.com/dmarzzz/swarm-lab/blob/2a1453a3f4befaf86006dcb04bdfe6aafdb3c8de/researchers/vishesh/notes/healing-helping-hands/composite/PLAN.md

Operator: vishesh/codex-regrowth-docs; execution task healing-qwen-jev. All 60 offline tests pass; zero C1 model calls. Existing cumulative Jev cap USD 0.10 remains, USD 0.013004124 already spent. Credentials remain local and are consumed by a bounded relay; machine creation does not reset the API ledger.

Return only host name, provisioning-ready status, expiry and claim coordination here. Addresses, account identity, credentials and state stay in the private fleet. Operator will claim the new machine exclusively before model loading and recheck public plan/source/runtime/budget before dispatch.

## Done when

- [x] Approved owner/account/state verified and exact single-worker resource plan reviewed within infrastructure authority.
- [x] New worker registered in private fleet with expiry, provisioned with sim/reporter runtime and authorized team access.
- [x] Host name and readiness reported here; exclusive claim coordinated with vishesh/codex-regrowth-docs.
- [x] Existing workloads, claims, state and API ledger preserved.

## Resolution

Approved credential became available; verified account and original owner state, provisioned sim-healing-c1, claimed it exclusively and ran C1/C2. Provider verified retirement after durable artifacts. The prior missing-access statement is historical and superseded. See composite/DEPLOYMENT.md and RESULTS.md under the Healing notes.
