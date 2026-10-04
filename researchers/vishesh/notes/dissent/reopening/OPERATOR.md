# RD6 manual native operator handoff

**Q0-A1 stopped before model dispatch; its operational and owning scientific closeouts are complete. No allocation is held.** Native integration and the startup repair are checked offline. The original defined18Q0/conditional144D0 scope was approved; the proposed explicit zero-dispatch replacement requires the separate concrete decision described in [STARTUP-REPAIR.md](STARTUP-REPAIR.md). The original USD1 API/USD1 infrastructure cap,488historical calls and unresolved reservations remain binding.

Use the [authoritative setup](../rd5/SETUP.md), [runbook](../../../../../tooling/agent-experiments/EXPERIMENT-SETUP.md), [implementation evidence](IMPLEMENTATION.md) and [new diagnostic assessment](DIAGNOSTIC-REVIEW.json). Historical RD5 completion stays unchanged. No independent researcher sign-off is required. Read local access/account policies before remote access; this public document deliberately contains no private account identity, host allocation or credential path.

## Offline commands

From the repository root:

```sh
python3 researchers/vishesh/notes/dissent/reopening/prepare_offline.py
python3 researchers/vishesh/notes/dissent/reopening/native.py prepare --stage Q0 --out /tmp/rd6-q0-packet.json
python3 researchers/vishesh/notes/dissent/reopening/native.py prepare --stage D0 --out /tmp/rd6-d0-packet.json
```

Preparation writes a new packet only; it cannot approve, allocate, read credentials or reserve costs. Do not reuse prepared packets after changing a bound source file. Preserve a committed exact checkout for each future admitted attempt. The shared operations registry continues to use a **manual** adapter; these are separate native entrypoints, not new shared CLI dispatch support.

## Private admission bundle after scope approval

Create operator evidence under the checkout's private `data/` tree, never in tracked/public files. Each reference has exactly `path` and the file's SHA-256; use matching repository-relative paths on local and remote checkouts for the necessary evidence bundle. The native gate reopens and hashes every reference; booleans are explicit operator attestations backed by inspected evidence, not independent verification.

`native_gates.validate_admission` is the definitive field contract. A private admission contains:

| Field / referenced record | Required binding |
| --- | --- |
| `schema`, `mode`, `packet_sha256`, `attempt` | `rd6-admission-v1`, `native`, actual prepared packet digest, unique `rd6-q0-…` or `rd6-d0-…`. Offline preparation never issues one. |
| `verified_utc`, `expires_utc`, `worker_host` | Admission checked within five minutes; at least31 minutes remain; exact verified host. Both relay and worker recheck it. |
| `owner_approval` | Actual owner decision reference (paraphrase/digest, never exact prompt), `decision: approved`, `approver_role: owner`, launch/stage scope, proposal/instrument/manifest digests; max162 new/lifetime 650 and both 1 billion-nanodollar caps. A test fixture is never an approval. |
| `parent_handoff` | The actual private RD5 H5-A1 handoff, hash `66775acf7ab12f7434f979685899a636da1f5b24701aeff093e3fed0712c5752`. Public `PARENT-EVIDENCE.json` is not acceptable. |
| `latest_closeout` | Must match the live local operations journal, with no dispatch still open. For an initial Q0 it is the RD5 parent. For the explicit Q0-A2 zero-dispatch replacement it must be the actual Q0-A1 closeout, never the older RD5 handoff. For D0 it is the just-reviewed Q0 closeout and must match its qualification review. |
| `allocation` | Current explicit approved account identity equals credential account identity; established provisioner state and exact resource-plan hash verified; rate in `hourly_rate_nano` ≤71,430,000 and `maximum_minutes: 90`; exclusive Right Dissenter allocation, host, claim ID/start/expiry with total duration ≤90 minutes. Bind their digest through admission `allocation_lineage_sha256`; D0 must retain the same allocation lineage as Q0. No default-account fallback. |
| `budget` | `authority: original-right-dissenter-ledger`; actual original path/device/inode; SHA of ordered historical calls (`native_budget.baseline`),488 historical calls and22,699,069 committed nanodollars; original/single-writer verification, cumulative infrastructure (at least the prior USD 0.720248442 estimate) plus a full 90-minute rate reservation ≤USD1 and new infrastructure reservation ≤USD 0.107145. Verify the authority independently; never mint an anchor from a copied/restored database. |
| `runtime` | Same committed source, instrument digest and worker host; offline checks, verified SSH host key and exclusive transport. Supervisor additionally binds private SSH-config SHA, host alias, remote checkout and verified GNU `timeout`. |
| `public_plan` | Fresh actual public preflight: immutable GitHub PLAN URL, matching file hash, experiment `right-dissenter-rd6`, verified public page, stage-specific `run_tldr` and one readable `condition_tldrs` entry per assigned condition. Publish all required descriptions before launch. Relay rechecks live registration and plan bytes. |
| D0 only | `qualification_directory`, its `qualification_bundle_sha256`, and `qualification_review` reference. All18 Q0 rows must be valid/correct, same instrument/manifest, native mode, reviewed traces18/18, relay reconciled, worker stopped and all 11 dimensions assessed. Review binds its actual operational closeout. No automatic Q0→D0 dispatch. |

The source list includes the new diagnostic review, proposal, native files, cases and inherited wire/extractor dependencies. Actor requests contain only the frozen model/provider/state/questions; operator evidence, owner conversation and labels never enter the provider body. Source-only preparation does not establish model availability: route/snapshot/pricing checks occur before credential use and dispatch, then periodically during the stage. Every returned response is checked again.

## Explicit zero dispatch replacement

Only Q0-A2 replacing the stopped Q0-A1 is supported. Admission adds `zero_dispatch_replacement`, a path/SHA reference with `attempt`, `previous_attempt`, `previous_packet_sha256`, current `packet_sha256`, `previous_closeout_sha256`, `owner_approval_sha256`, `zero_dispatch_proof` and `owning_review`. The last two fields are path/SHA references to the retained zero-dispatch summary and completed eleven-dimension review. The approval must name both attempts and bind `replacement_contract_sha256` to STARTUP-REPAIR.md. A synthetic receipt never supplies approval.

The gate pins the actual A1 packet and operational handoff, retains H5 as scientific ancestor, and rechecks the owning review. The original ledger atomically requires the old stage row stopped, zero RD6 calls of every status and zero orphan responses. It inserts one append-only replacement row while preserving A1. A second replacement is impossible. D0 has no replacement path.

Resource checks carry estimated released infrastructure forward (at least USD0.747173584), require a complete interval reservation at the verified rate, retain the original committed-plus-reserved infrastructure maximum USD0.827393442 and original2026-10-04T20:40:02Z window stop. Conditional D0 inherits that same bound allocation from the qualified Q0 bundle. Each stage still needs31minutes remaining. Later windows need an updated concrete decision and contract; unused budget does not grant time.

## Supervised execution, only after admission

Stage the exact checkout, prepared packet and necessary private admission evidence on the authorized host. Use a unique, versioned private directory: referenced evidence first, admission last. Publish it atomically from a staging directory, and never overwrite an admitted directory. References use the final paths. The supervisor sends the exact admission-byte SHA to both local relay and remote worker; every evidence reference is hashed and decoded from one read. Its separate remote `check-worker` command verifies source, receipt and writable output parent before creating the relay. Save its exact acknowledgment. A receipt changed after the check still fails the worker digest gate. Keep the original ledger and credential file on their authorized local machine. Use the already-established verified encrypted SSH path; this program does not copy credentials or provision machines.

`native_operator.py supervise` takes private path arguments `--packet`, `--admission`, `--credential`, `--ledger`, `--ssh-config`, `--host-alias`, `--remote-checkout`, `--remote-packet`, `--remote-admission`, `--remote-out`, `--out`. It starts the local relay and the remote worker together, with a reverse loopback forward, strict host-key checks and no SSH retries. The remote worker checks relay health before each request. Safe startup state is retained beside the worker output as `<attempt>.startup.json`; the supervisor records its phase and numeric exit status. These fixed categories never echo arbitrary exceptions or SSH/provider stderr. A separate hard30 minute remote timeout bounds orphan risk; the supervisor stops its own local child process groups on failure. **SSH exit/cleanup is not proof that the remote worker stopped.** Check the actual owned process before attesting stop or releasing a claim.

Provider calls are serialized. The original ledger reserves USD 0.001344 before each send, with separate stage/assignment identities, durable stage fences and no response cache. Calls with an unknown outcome retain their reservation. Reliable provider charges are recorded even if schema/route validation fails or a charge exceeds its reservation. A 60 second wall-clock request bound stops a server that slowly trickles data. Any first transport/schema/route/lease/budget failure stops dispatch; later assignments remain unstarted. There is no resume or automatic retry. The only replacement is the separately approved, zero-dispatch Q0-A1→Q0-A2 contract below; it never clears the historical fence.

The single-writer lock is an adjacent `.rd6.lock` file: locking the SQLite database itself conflicts with SQLite on macOS. This lock coordinates RD6 operators; current exclusive access and the original-ledger check still matter because legacy writers do not use it. Preserve all legacy RD5 fences and all previous rows.

## Reconciliation and closeout

1. Verify worker and relay are stopped. Preserve local relay events/accounting and the remote result bundle, including failed/unstarted slots. A lost worker response is not evidence of provider non-dispatch.
2. Transfer the stopped remote result directory through the authorized encrypted path. Verify/publish the staged local copy with `native_operator.py collect --source <staged> --destination <repo/data/results> --bundle-sha256 <digest>`. A failed copy leaves the source intact and never reruns the experiment.
3. Run `native_operator.py reconcile --results <repo/data/results> --bundle-sha256 <digest> --relay-directory <local-relay-dir> --out <private-reconciliation.json>`. This cross-checks every reservation, exposed decision and charge. Known relay-only answers are listed separately; worker scoring is not silently rewritten. Inspect all missing/invalid/wrong responses and repeat disagreements before interpreting them.
4. Run `native.py report --out <repo/data/results> --bundle-sha256 <digest>`. This reconstructs scores and checks the hash-chained terminal records. Review the observed grid and chronological cost/request table. The Python grid checks do not certify browser layout.
5. Record a private stop attestation with attempt, bundle SHA, verifier, `worker_stopped_verified` and `relay_stopped_verified`. Reference it through a `{path, sha256}` JSON file. Invoke `native.py finalize --out <repo/data/results> --stop-receipt <reference.json>`. The native hook calls `scripts/experiment.py finalize right-dissenter … --worker-stopped` and requires a completed operational closeout. That flag attests to an already-observed stop; it does not stop anything.
6. Complete the scientific post-mortem against all 11 dimensions, trace coverage, cumulative costs, artifact readback and any release receipt. Operational finalize alone is not scientific review. Qualification pass needs its own postreview and fresh D0 admission. Failed, interrupted and valid-negative attempts receive closeout too. If a hard kill or storage failure prevented a complete bundle, preserve partial artifacts and use the shared manual finalize hook with `ambiguous`; document unresolved reconstruction instead of manufacturing terminal evidence or retrying.

The saved scorer retains `native_evidence: false` because arithmetic alone cannot authenticate provider provenance. Native mode, original-relay reconciliation, source binding and the owning trace review provide separate evidence. Initial/transition/failure/final synthetic grid fixtures were structurally checked; native delivery, remote lifecycle and browser rendering remain to be verified on the actual admitted attempt.
