# A1 orbital-one operator handoff

A1 is a manual acquisition substage, not a restart of the older Theseus v2 S0 adapter. The global operations registry still describes that historical adapter. Do not invoke its USD15 configuration for this USD5 lineage. Only one A1 native attempt; no retry or successor chain.

## Source and offline preparation

Deploy the pinned commit from the queue request into a clean source checkout. Required Python>=3.10, standard-library worker and installed authorized swarm_report; matplotlib is needed for offline reporting only. Before deployment, confirm current approved-account/fleet/claim/workload and verified SSH trust. Preserve the original allocation ledger; the worker refuses when it is missing. A new host requires reconciled transfer and retirement of the previous allocation authority, not a new budget.

From the pinned public repository:

```sh
python3 -m unittest discover -s researchers/vishesh/notes/swarm-of-theseus/execution-diagnostic/a1 -p 'test_*.py' -v
python3 researchers/vishesh/notes/swarm-of-theseus/execution-diagnostic/a1/runner.py prepare /srv/swarm/theseus-a1-prepared
```

The template is intentionally blocked. Fill the receipt from actual evidence; never run using the template. Required exact fields and freshness checks are in a1/admission.py. Stable allocation id is theseus-a1-7300-7305-v1, proposed reserve USD2.60 total. Original authority USD5, prior estimated USD0.8122310437, no unresolved reservations as of R1 closeout. Verify no subsequent dispatch first. The host-wide /srv/swarm/theseus-execution-allocations.sqlite prevents duplicate use of this stable id. Do not delete or reset it.

## Public admission

Register hub experiment swarm-of-theseus-acquisition-a1 with a TLDR from A1-PLAN.md and immutable URL at the exact deployed source. Verify the actual public Swarm Live page. No UI deployment or Cloudflare login is needed. Write a dated prospective assessment with `Status: diagnostic-only` only after its conditions hold; retain A1-PRE.md as the honest blocked preparation snapshot. Bind its immutable URL/hash in the receipt. Registration is checked again in the native worker, along with source, runtime/host, original budget, queue origin and current claim freshness.

## Credentials and dispatch

Follow the standing Swarm Lab credential-transfer policy: only the owner-designated Keychain selector, one key in memory over verified SSH stdin to the admitted exclusively claimed destination. No general environment, encrypted shared-provider alias or persistent key installation is an authorized substitute. Private routing metadata must use its verified mapping. Current orbital-one queue dispatch and the local Keychain handoff need a compatible operator-controlled mechanism; the queue request records this unresolved dependency. Do not run this command from a laptop to bypass the queue.

After the orchestrator has established the approved mechanism, execute the bounded worker on the admitted host with only the approved key/routing fields in its environment:

```sh
python3 researchers/vishesh/notes/swarm-of-theseus/execution-diagnostic/a1/runner.py run --admission /srv/swarm/theseus-a1-private/admission.json --output /srv/swarm/theseus-a1-run
```

This is the exact native entry point, not a claim that the fleet's generic launcher currently supports it. Credentials never go in command arguments, logs or files. The worker disables core dumps; no alternate-provider fallback. Stop on provider/usage/reporting failure, deadline, claim or cap. Contract-invalid learners keep their dependent cases assigned and unstarted, with no oracle replacement. A failed allocation insertion must not be retried under a new identity.

## Closeout, including failure

Once worker exit is verified, preserve all call-start/finish/manifest/quota/terminal records. Recompute with `a1/runner.py analyze /srv/swarm/theseus-a1-run` and render with `a1/report.py /srv/swarm/theseus-a1-run`. Upload raw archive plus summaries/figure/replay and read back hashes. Retain unresolved reservations before settling the existing authority.

Copy sanitized evidence to the operator checkout's ignored data/experiment-operations/theseus-a1-native directory, then invoke the supported offline finish hook:

```sh
python3 scripts/experiment.py finalize swarm-of-theseus-v2 --attempt a1-native --results data/experiment-operations/theseus-a1-native --outcome completed
```

Use failed or ambiguous instead when warranted. The legacy adapter may report that A1 automatic analysis is unsupported; retain that limitation and use A1's explicit saved-data analysis. This hook is an operational inventory, not the scientific review. Complete all eleven RUN-QUALITY dimensions with evidence hashes; report assigned/started/terminal/valid/analyzed counts, acquisition versus ceiling, false actions, per-root effects, native model/usage, original cumulative exposure and artifact status. Update metadata/setup and only then release the claim. No queued successor and no cultural claim.

## Owner-authorized direct path amendment

The new A1-DIRECT-AMENDMENT.md supersedes only the orbital-one launch restriction in this historical handoff. Queue295 is closed with an explicit no-central fence. Use owner-direct-a1 receipt origin and the bounded direct_dispatch_authorization object, never a fabricated orbital receipt. The actual local credential loader sends the one approved key and separately allowlisted routing metadata over verified SSH stdin to the exclusively claimed host. Native command, one-attempt identity and every other gate are unchanged.
