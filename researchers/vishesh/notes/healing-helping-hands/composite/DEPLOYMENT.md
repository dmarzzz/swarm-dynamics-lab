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

## Authorized dedicated capacity, 2026-10-04 UTC

The user confirmed provisioner access and explicitly authorized creation. The approved local credential now matches all 12 known Dmarz fleet hosts. Created only sim-healing-c1, 4 CPU / 8 GiB, USD 0.07143/hour, using the original empty Vishesh owner state with locking. Private fleet PR 143 merged the host, generated inventory and heterogeneous-map typing fix; PR 145 merged its fresh exclusive three-hour claim. SSH and cloud-init readiness verified. Standard secured simulation software is being installed. No C1 inference yet. The earlier statement that access was unavailable is superseded; the allocation request is obsolete. No existing machine was changed.

## C1-S0 dispatched

Prospective plan and deployed source: `66ec09017284892a59623c7e7a73d93651b4a686`. Public page verified the immutable link and composite protocol before runtime load. Standard Ansible sim/reporter setup completed; reporting credentials transferred securely without transcript output. Ollama 0.11.11 image pinned to `sha256:24d41d792306fc3221de215bb6f225faf981712d1f38083d8c61301dfa2b69b3`; Qwen weights match the declared digest. Fresh source-byte, workload, exclusive claim and original ledger checks passed. Claim expires 2026-10-04T07:52:58Z. The 60-case S0 started after current admission; hub start acknowledged. Jev credential remains local behind the bounded loopback SSH relay. No automatic transition to S1.

## Cycle closed and worker retired

2026-10-04T06:11:53Z: provider verified sim-healing-c1 deleted using the reviewed destroy plan against its original owner state. No other machines changed. Exclusive claim released (private PR 177); inventory retirement PR 178. All three attempts and their checksum inventory were archived locally and in the hub before deletion. Creation 04:49:34Z to deletion 06:11:53Z is about 1.372 hours, approximately USD 0.098 at the quoted hourly rate, excluding provider billing rounding. This supersedes earlier pending allocation/runtime statements above.

[Results](RESULTS.md): qualification completed; full comparison remains incomplete after two preserved transport failures. No further inference is authorized by this closed plan. Final public TLDR and immutable plan registration acknowledged at f0f3a73de0f528c6ca05e41a90c180ab2b2ad097. Subsequent public readback was unavailable during transport cleanup; do not claim an additional browser verification.

## C3 owner-approved native execution

Source b2a09a420dbfc42f8334543f495a815e9818be73 deployed to existing sim-dmarz-7 after verified account identity, exclusive claim PR 214 and idle-workload check. No new VM created. Registered C3 TLDR and exact immutable plan rendered on the public page before model load. Pinned Ollama image and Qwen weights verified. Original 859-entry ledger transferred with its historical rows intact and canonical local dispatch path disabled. Sole remote writer is protected by an exclusive lock; credential reaches only the admitted host through encrypted stdin and ephemeral private memory-backed storage, which is removed after reading.

C3-S0 ran as detached healing-c3-s0: 60 cases, 180 calls, 108.8483 seconds, no transport failures; qualification and raw-data audit passed. Its eight hub artifacts include measured confusion chart. C3-S1 was separately assessed in C3-S1-PRE.md at 8de1578f020db9593fbf44dd4c7b808badbe5438, then launched as detached healing-c3-s1 with the unchanged qualified instrument. Run IDs C3-S0/C3-S1; expected S1 600 reports and 270 worlds. Live completion counts are actual observed rows. Remaining original inference authority at S1 launch USD 0.080636782. Both native commands and runtime parameters follow C3-OPERATIONS.md and durable admission receipts.


## C3 completed — 2026-10-04

Qualification 60/60 and full 600-report, 270-world run completed with zero transport failures. See [C3-S1 post-mortem](C3-S1-POST.md) for evaluated plan, measured controls, scoped quality assessment, original budget reconciliation and saved-data visuals. Jev/composite each 100%; no incremental Qwen benefit. C1/C2 failures remain historical evidence. No further run is admitted by this closeout.

Closeout verified both native services inactive, ephemeral credential absent, remote ledger authority closed, original local authority restored, and `hhh-ollama` stopped. Evidence archive upload/readback passed with SHA256 `bbeacef5f8bba1cea364b49e7a505255940f40cad779bbc0d5e3271e49c93147`. Existing fleet VM retained; only the experiment allocation is released.
