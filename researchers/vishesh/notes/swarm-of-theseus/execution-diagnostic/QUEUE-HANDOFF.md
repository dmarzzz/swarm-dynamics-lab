# D1 owner-authorized queue handoff

Owner explicitly authorized independent-review inbox pings, a fresh host, the USD5 allocation, the plan update and D1 execution once gates pass. Research owner and scientific stop decisions remain with vishesh; infrastructure decisions remain with Dmarz. This does not authorize a larger screen, a culture pilot or a new server purchase.

The private fleet now requires orbital-one to launch new runs. The native D1 runner remains the supported entry point; the generic operations registry has only the older v2 adapter and must not be used to restart completed v2 stages.

## Requested allocation

Fresh exclusive existing idle fleet allocation; preferred host `sim-shadow`, which has no current active claim in the refreshed inventory. Actual workload and access must still be verified by the allocator. Claim ID `vishesh-theseus-execution-d1`, experiment `swarm-of-theseus-execution-d1`, duration4hours minimum, owned by the actual queue operator. No shared host, no disturbance of other jobs. If unavailable, select another eligible idle fleet host or report allocation blocked; no purchase under this request.

## Before dispatch

1. Independent reviewer of another researcher completes `tasks/review-theseus-execution-d1.md`. The two inbox pings are one request, not a requirement for two reviews. Resolve findings and pin final source. Do not treat this handoff, budget approval or19 offline checks as scientific review.
2. Allocate the fresh exclusive host using agentops, verify merged claim, expiry and idle workload. Freeze final source at a clean published commit. Use dedicated checkout `/srv/swarm/theseus-execution-d1-lab` and outputs `/srv/swarm/theseus-execution-d1-results/D1`.
3. Run the offline tests on the host. Use the native `prepare` command to produce the exact assignment digest and a blocked receipt template. Reserve the owner-authorized USD5 allocation once under unique ID `theseus-execution-d1-owner5-20261004`, linked to this owner's instruction and one host. Do not copy/reset v2 ledgers or spend another study's balance. Record central non-overlap verification privately and reference it in the receipt.
4. Complete a new prospective diagnostic-only pre-assessment after review/resources are evidenced; leave the old blocked PRE-RUN.md historical. Commit it. Re-pin the exact deploy commit, regenerate preparation and receipts. Register the immutable PLAN URL and TLDR through the host's approved swarm_report; visually verify the actual public page. Receipt binds public-plan hash, immutable assessment/hash, operator, independent reviewer, claim, authority, source/instrument/assignment hashes, current pricing, dependencies and verification times. Its15-minute checks must be refreshed immediately before launch.
5. Follow `tooling/agent-experiments/SWARM-LAB-CREDENTIALS.md`. Only the dedicated project-specific Keychain selector service `swarm-lab-anthropic`, account `vishesh`, and its explicitly verified workspace route are authorized. If orbital-one lacks that approved credential path, coordinate a policy-compliant single-use transfer to the admitted host; do not substitute general provider credentials or persist the key. Credential transfer is authorized once all destination and admission checks pass. Disable core dumps and clear inherited alternate credential/workspace variables. Missing approved route remains a concrete blocker, not permission to probe another account.
6. From orbital-one, launch the bounded worker on the admitted host using the exact native command below. Local laptops may prepare/review and perform the narrowly authorized credential courier step; they do not launch new model runs.

## Native commands on the allocated host

From the clean pinned swarm-lab checkout:

```sh
python3 -m unittest discover -s researchers/vishesh/notes/swarm-of-theseus/execution-diagnostic/tests -v
python3 researchers/vishesh/notes/swarm-of-theseus/execution-diagnostic/src/runner.py prepare /srv/swarm/theseus-execution-d1-prepared
python3 researchers/vishesh/notes/swarm-of-theseus/execution-diagnostic/src/runner.py run --admission /srv/swarm/theseus-execution-d1-admission.json --output /srv/swarm/theseus-execution-d1-results/D1
```

`prepare` is offline and requires a fresh directory. The exact dispatch command must be supervised/detached by orbital-one with a process-lifetime credential mechanism; no credential in arguments, files or logs. The worker itself runs serially, with144calls, USD5 and two hours maximum, zero retries. Provider errors and wrong decisions remain outcomes; source/public/reporting failures stop dispatch. No automatic repair, confirmation or culture pilot is authorized.

## Reconciliation

Return assigned/start/finish/terminal counts, token usage, estimated actual cost, conservative reservations, schema/provider failures, independent score disagreements, every paired-world arm contrast and semantic-versus-console results. Preserve `manifest.json`, calls, outcomes, quota, summary, terminal status and replay. Complete post-mortem; upload supported measured artifacts and verify readback; release the host only after worker exit and evidence transfer. Keep qualification, scientific inference, process compliance and artifact delivery separate. Raw provider payloads contain synthetic tasks only, but admission records must be checked for private routing or inventory metadata before publication.
