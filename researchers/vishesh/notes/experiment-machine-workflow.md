> Owner correction, 2026-10-04 UTC: use a new dedicated experiment machine in **Dmarz's existing DigitalOcean account/team and Swarm Lab setup**. Do not borrow his occupied machine, and do not use the user's personal/default DigitalOcean account. Researcher ownership and billing-account authorization are separate. The earlier instruction recorded here incorrectly conflated them.

# Dedicated machines for experiment launches

Owner instruction recorded 2026-10-04 UTC. Every new experiment receives a fresh exclusive allocation from Dmarz's machine list before deployment or execution. This is the standard for vishesh's agents, including exploratory S0/S1, model qualification, and a new version launched as a separate study. Stages and replicate batches of the same experiment may retain its dedicated host. Local offline unit tests remain local.

## Allocate before launch

1. Refresh the private `dmarzzz/swarm-labs-agentops` repository. Read its `AGENTS.md`, the server-provisioning section of its README, `fleet.yml`, and current claims. Inspect only needed non-secret metadata; do not dump `task list`, private addresses, environment files or credential files into a transcript or public documentation.
2. Select an eligible available machine from Dmarz's list with sufficient capacity, authorized access and enough remaining lifetime for the job and artifact upload. Verify active claims and actual workload: an expired claim alone does not establish that a host is idle. Never stop an unfamiliar process to make room.
3. Claim it exclusively through the supported agentops command, with an experiment-specific claim ID, agent identity, experiment ID, expected duration and non-secret purpose. Do not use `--shared`. Verify that the claim merged and the refreshed claims contain no conflict. If someone else won the host, select another available host.
4. If none is available, do not fall back to another experiment's host. Arrange a new allocation through the fleet owner/provisioning workflow, within an existing authorized infrastructure budget. Dmarz-owned machine creation stays with the authorized owner. For a machine you are authorized to create, use the existing owner's state and the documented duplicate-resource preflight; add the fleet entry and expiry, provision the approved blueprint, verify access, then claim it. Never invent an unlisted machine or duplicate a VM from a different checkout's infrastructure state.
5. Before creating any resource, resolve the approved DigitalOcean account/team identity from the established Swarm Lab provisioner. Query account identity with the proposed credential locally, compare it exactly, and verify the intended infrastructure state/project and resource plan. Record a private verification receipt. Missing identity or credentials blocks provisioning; a local default doctl context is never a fallback. Keep credentials and account IDs out of transcripts/public files. Only then may an authorized create/apply proceed.
6. Deploy the frozen source to the allocated host. Verify its identity, exclusive claim, dependencies, tests, credential availability by non-secret status, and run budget. Register the study, record the allocation, and only then queue/start the bounded worker. A new directory, container or worker on a busy host is not a dedicated machine.

Example commands, run inside the private agentops checkout after selecting a real host:

```sh
python3 scripts/agentops.py claims
python3 scripts/agentops.py claim <researcher>-<experiment>-<allocation> \
    --servers <available-host-from-dmarz-list> --by <researcher>/<agent> \
    --until 6h --experiment <experiment-id> --note "Dedicated experiment allocation"
python3 scripts/agentops.py check
python3 scripts/agentops.py claims
```

Replace placeholders and choose a claim duration that covers the actual job. The command's success is not sufficient if the resulting claim has not merged or the host has an unexpected active workload.

## Preserve budgets across hosts

Allocating another machine does not reset an API or infrastructure cap. If studies share a budget, enforce it through a common transactional budget authority or preallocated non-overlapping per-host quotas whose sum stays within the remaining authorized amount. Do not copy a SQLite ledger to independent machines and let each spend the original total. Existing single-host workers using a shared SQLite file require a budget-coordination change before launching across separate hosts; if that cannot be enforced, stop before paid requests.

## Record and release

The deployment record must identify the experiment/design version, host name, exclusive claim ID and expiry, deployed commit, machine/runtime specification, planned worker count, infrastructure allowance, API budget authority or quota, and hub run IDs. Use server names only in public records. Never publish private fleet data, IPs, hub tokens or model credentials.

Keep the claim valid until computation and artifact transport finish. For unattended jobs, extend the claim with the supported agentops release/status mechanism described in its AGENTS.md. Once done, stop only your experiment's workers, verify durable outcomes including failures, release the claim, and let the authorized owner tear down temporary resources through the fleet workflow. Release does not mean terminate somebody else's machine.

## Existing deployments

The immune-response and external-influence deployment notes document earlier allocations and remain historical evidence. The earlier shared-host recommendation is superseded for new launches. This does not authorize continuing on a disputed or wrong billing account. Stop affected work, preserve data and the spend ledger, and resolve the account boundary before resuming. Their next separately launched experiment/version receives a new dedicated allocation.
