# C1 deployment status

2026-10-04 UTC. No C1 model service, credential relay, worker or experiment run has been started. No new API spend. Existing ledger verified read-only: 720 historical calls, USD 0.013004124 spent, USD 0.086995876 remaining under the original USD 0.10 cap.

Fleet refreshed from origin/main. All eligible hosts have outstanding claims. Previously used sim-vishesh is allocated to Antsy. Research-01 was checked read-only: zero experiment processes and zero running Docker containers. Its old vishesh-dedicated-experiments claim nevertheless remains status running; agentops refused a new exclusive claim. No claim PR was created, and no existing claim or workload was changed. A fresh exclusive allocation or explicit user exception is needed; an idle process snapshot does not override another owner's reservation.

Initial prospective plan committed before implementation, published and registered at edbc2e3f130ab41d01f781574c1911a89b80e2a2. Browser verification confirmed the public C1 TLDR, immutable link and composite protocol after reload. The final implementation revision must be registered and verified before launch. Use S0-PRE.md and SETUP.md with tooling/agent-experiments/EXPERIMENT-SETUP.md.

## Exact next action

Resolve allocation, verify current claim/workload and model runtime, record source/dependency and current budget evidence, register frozen instrument commit, then create a current admission.json with the actual plan URL/hash, source commit, host/claim/expiry, budget and verification timestamps. Do not fabricate affirmative receipt fields. Run worker.py --stage S0 --admission <verified receipt> --out <fresh durable C1-S0 directory>, with the local relay.py --stage S0 using the original credential file and ledger. Run S1 only after a passing full-composite/strong-control screen, its audited post-mortem and a separately committed S1 assessment. No automatic stage advancement.

## Published instrument checkpoint

Tested source and current registered plan: 2a1453a3f4befaf86006dcb04bdfe6aafdb3c8de. This publication does not admit execution while the allocation gate remains blocked. No automatic/background run is queued.

## Capacity escalation correction

The user directed resolving fleet capacity rather than stopping at claimed machines. The Mac fallback is withdrawn. New capacity is requested through the authoritative Dmarz provisioner in [allocate-healing-qwen-jev](../../../../../tasks/allocate-healing-qwen-jev.md): a concrete CPU worker specification, expiry, exclusive allocation and account/state/budget checks. This workspace has no dmarz state or approved provisioner credential; only the fleet owner executor may perform creation. No deployment or execution is claimed by filing that request.
