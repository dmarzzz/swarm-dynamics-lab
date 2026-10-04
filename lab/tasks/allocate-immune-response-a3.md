---
id: allocate-immune-response-a3
type: task
title: Provision dedicated Immune Response replacement through established Dmarz setup
kind: admin
status: open
priority: p0
owner: null
for: dmarz
created: 2026-10-03
created_by: vishesh/codex-immune
depends_on: []
topics: []
---

## Goal

The owner explicitly authorized use of Dmarz's established provisioning setup to create the correct dedicated machine and run Immune Response. Please use the existing authorized operator environment/account and original locked infrastructure state. The local researcher has shared repo/SSH access but does not possess that provisioning state or credential. Do not export credentials or copy owner state to another writer.

Prepared private fleet PR: https://github.com/dmarzzz/swarm-labs-agentops/pull/116 . It adds only `sim-immune-response`, owner dmarz, standard sim blueprint, nyc3, 2 vCPU/4 GB, access all, expiry 2026-10-05. Existing hosts must remain unchanged. The prior mistaken personal-account droplet and dedicated resources are deleted, with all evidence and the spend ledger backed up. Check actual account identity against the established private record, capacity, duplicate-resource prevention and exact plan before applying.

The user requests a new purpose-specific host; do not borrow a claimed machine. Use the existing authorized infrastructure setup. Native A3 is a one-worker, maximum 120-call Haiku diagnostic. At most 2.5 hours for the call plan plus artifact verification; claim the host for three hours after readiness, with expiry extension only if required. Register/provision normal team SSH and reporter access; no extra public ports or GPU. If the existing account has no capacity, report that exact constraint without disturbing claimed resources.

The owning experiment agent will transfer the preserved budget ledger, configure model access securely, validate the immutable public plan, claim exclusively and dispatch. API cap remains USD 8, with 267 calls and USD 2.059367 conservative reservations already recorded. No new model budget is requested; no new ledger may reset that cap.

## Return contract

Return only host name, ready/provisioned status, expiry and private verification-record reference here. Put generated addresses and any account identity in the private fleet only. Do not post credentials, state contents or account IDs in this public task. A private hash/reference sufficient for the launch receipt is acceptable. Do not launch the model worker from the provisioner; vishesh/codex-immune owns that single dispatch.

## Done when

- [ ] Approved Dmarz account and original state verified; exact replacement-only resource plan reviewed.
- [ ] Fleet PR applied through existing provisioner; generated inventory and standard sim/reporting access published privately.
- [ ] Existing machines/inventory verified unchanged; host expiry and readiness returned.

## Related work

Experiment task: immune-response-evidence-receipts. Protocol: 5-experiments/studies/vishesh/immune-response-v3/evidence-study/reviews/receipt-a3-pre.md. Fourteen tests and all sixteen offline assignments pass; native execution remains blocked only on correct allocation and final transfer checks.
