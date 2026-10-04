# Execution record

Immune Response remains exploratory and uses the existing `immune-response-v3` registration.

| Attempt | Runtime / binding | Disposition |
|---|---|---|
| receipt-engineering-a1 | Original local manifest and retained summary | No paid calls; exposed overbroad damage gate |
| receipt-engineering-a2 | Amended local manifest and retained summary | 16/16 scripted episodes, joint gates passed |
| receipt-native-a1 setup | `3b51b9e08275da76b1c814de0983c153cbd79b4f` | Public-plan heading mismatch; zero model calls, no hub run created |
| receipt-native-a2 | `d38cd4397fdc2132ac5be7e9f40b6fa8577f3f93` | Stopped for wrong cloud account; 3 complete, 1 partial, 12 unstarted. See reviews/receipt-a2-post.md. |

Native run: [immune-response-v3/1004-034657-73913b](https://swarm-live.pages.dev/#/r/immune-response-v3%2F1004-034657-73913b).

Host: vishesh-owned `sim-immune-response`. Exclusive claim `vishesh-immune-receipts-a1` through 2026-10-04 09:41:16 UTC, merged private fleet PR 77 and mirrored to the hub. No other machine borrowed. One worker uses Python 3.12 in the existing environment. Native configuration and inherited simulator/provider are bound by manifest file hashes. No credentials, private inventory or addresses appear in public evidence.

Persistent USD 8 ledger starts at 240 calls and USD 1.815067 reserved. Prior actual cost USD 0.441259. No copied/reset ledger or new grant. Raw recorded outcomes, event history and reports are uploaded under the native run; setup failure remains a separate record. Offline results are explicitly scripted reference checks, not model evidence.

## Manual feasibility audit

This derivation uses the visible contracts, independently of the model's advice. In stale-advice and registry cases, gateway 2 speaks rpc-batch, worker 3 cannot read schema-legacy, and store 1 matches the persisted format. Worker 2 reads legacy and speaks batch: one deployment repairs the service. The registry need not be queried because all contracts are visible; this limits the registry case's diagnostic value.

After data migration, store 2 holds schema-expanded while gateway 1/worker 1 use classic RPC and worker 1 cannot read that schema. Worker 2 plus gateway 2 is a valid two-change repair. Updating either first temporarily makes RPC incompatible while the service is already unavailable. Requiring zero new failing probes would make this feasible recovery fail the gate. The metric now exposes the transient regression without mislabelling it as loss of healthy service.

The healthy control already has gateway 2, bridge worker 2 and legacy store 1, with bulk_checkout available. Waiting preserves every check. Rolling gateway back to 1 loses the requested feature and RPC compatibility; changing to worker 3 loses readability. These are actual harms even if a later action restores the service. Final health alone is insufficient.

These cases establish an interpretable feasibility screen, not realistic deployment complexity. Independent authored topology and partial observability remain prerequisites for a broader claim.

## Account correction

The claimed host was registered in the fleet but provisioned with the wrong local default DigitalOcean account. The user required Dmarz's existing Swarm Lab account/setup. No experiment worker remains active; evidence and budget state are backed up. No further launch is authorized on that deployment. See [incident post-mortem](reviews/receipt-a2-post.md).

## Retirement and next attempt

The user authorized proceeding with the correct replacement. The mistakenly created droplet, its dedicated firewall and cloud root-key registration were deleted and the droplet endpoint returned 404. Dedicated local key/state resources were removed through the same reviewed plan. Eight other droplets were unchanged. A stale saved plan was rejected before mutation after concurrent infrastructure state changed; a fresh isolated configuration used the original locked backend and verified preservation of all other inventory before applying.

The verified evidence/ledger backup remains available. A3 now includes durable request-level usage receipts and refuses a missing ledger. Fourteen tests pass; scripted A3 records and reconciles 16/16 episodes. Replacement and native A3 are not started: Dmarz's original provisioning checkout/state and authorized credential context have not been located on this machine. User was asked only for the path/context, never a secret. No fallback account is permitted. See [A3 pre-run assessment](reviews/receipt-a3-pre.md).

### Provisioner discovery and prepared replacement

Follow-up investigation located the preexisting local agentops checkout. It contains the researcher access configuration but no Dmarz DigitalOcean credential or infrastructure state. The four temporary checkouts likewise have neither. Known shared locations on research-01 and hub-01 contain no provisioning checkout; conventional paths under the Dmarz home are not accessible to this user and were not bypassed. GitHub exposes only the check workflow and no configured secret/variable names for a deployment workflow. The repository explicitly says DigitalOcean tokens stay in the owner's own environment, and the D1 deployment record distinguishes repository/remote-worker access from owner-state provisioning.

[Draft fleet PR 116](https://github.com/dmarzzz/swarm-labs-agentops/pull/116) prepares only sim-immune-response under owner dmarz, using the standard sim blueprint and original-authority workflow. Agentops validation passes with the expected not-yet-created warning. It is intentionally not merged or described as provisioned. No existing machine was borrowed, no credentials were extracted from another user's private home, and no new provider calls were made. The concrete remaining action is applying this proposal from Dmarz's authorized original provisioner, then recording the account/allocation receipt and transferring the preserved ledger before native A3.
