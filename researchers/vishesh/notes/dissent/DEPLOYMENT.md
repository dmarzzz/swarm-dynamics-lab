# Right Dissenter deployment

The standalone study is registered at [Swarm Live](https://swarm-live.pages.dev/#/x/right-dissenter). Its immutable RD-2 plan passed the public preflight and the browser displayed the TLDR, plan link and protocol before any native execution. See LIVE-PUBLICATION.json. At this checkpoint there are zero native calls and zero allocated machines.

## Concrete resource request

The requested host is **sim-right-dissenter**, owned by vishesh, with an exclusive `right-dissenter` claim. Use the original vishesh infrastructure workspace in the private agentops checkout, its duplicate-resource preflight, and the existing authorized local credential store. Do not create the host from a copied state. Verify that the infrastructure plan contains only this host's new resources and the generated inventory update; reject modifications to other machines.

Read-only DigitalOcean metadata on October 4 quoted the 2 vCPU / 4 GB size at **$0.03571/hour**, or **$0.21426 for six hours**. Eight droplets were in use out of the credential's 15-droplet allowance, and this experiment's host did not exist. These values are a snapshot, not permission to skip a fresh provisioning check. No private addresses or credentials are included here.

The owner approved the **$2 total cap**: $1 API and $1 infrastructure, at most six hours, with teardown after artifact verification. See AUTHORIZATION.json. The runbook instruction is: **“Go ahead and create and borrow a machine from Demars's DigitalOcean machine list.”** Allocation uses the shared private agentops fleet, an exclusive claim and the authorized owner infrastructure state. The native relay requires an explicit authorization receipt and one cumulative SQLite ledger. At the verified Jev price, 500 full-context reservations total $0.672, inside the API cap. Actual short packets should cost less; that is an estimate, not a result.

## Launch binding

Deploy the full frozen source commit, verify every source hash from the launch configuration, run the 49 software checks on the allocated host, verify the exclusive merged claim/expiry and inspect only this host for unexpected workloads. Refresh the public-plan receipt immediately before dispatch. Register Q0 and S1 with their own TLDRs. Q0-A1 has a pre-run assessment; S1 requires a passing Q0 result and its own assessment before dispatch.

The local relay consumes the OpenRouter credential at the protected path, binds only loopback port 18449, and permits only frozen request hashes. An SSH reverse tunnel connects the dedicated worker's loopback to it. The remote worker receives no OpenRouter secret. The local ledger persists across study stages; failed or uncertain calls retain reservations. No retries and no inference-time fallback routes are allowed.

## Completion and cleanup

After each attempt, reconcile assigned, started, terminal and missing outcomes; inspect the exact route, failures, reservations and paid cost; upload JSON records and supported PNG/GIF views through the hub. Verify durable and public artifacts separately. Write a post-mortem before a subsequent attempt. Stop the experiment's worker, relay and tunnel; release its exclusive claim; destroy only this study's temporary resources through the same owner-controlled infrastructure state. Do not publish a post-mortem as though a native attempt happened before it did.
