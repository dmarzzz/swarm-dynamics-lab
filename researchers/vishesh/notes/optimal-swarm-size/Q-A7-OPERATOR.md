# Q-A7 queue operator packet

Use the full immutable public revision named in the private queue request. This file is a manual launch contract for orbital-one, not permission to launch from a laptop. [Plan](reviews/q-a7-input-binding-plan.md), [setup](SETUP.md), [spending authority](SPENDING-AUTHORIZATION.json). One Q-A7 attempt only; no automatic successor or model ladder.

## Resolve before preparation

1. Inspect current fleet inventory and queue, prevent duplicate Q-A7 dispatch, and allocate one exclusive approved-account worker. research-01 is held by autoresearch-lab and must not be borrowed. No provisioning from a personal/default account.
2. Preserve the original canonical study ledger. Its last verified total is 631 calls, 2,031,320 microdollars exposure and 1,810,840 settled. Retain the 220,480 historical hold. If the existing host cannot be allocated, have the established fleet operator arrange an audited single-writer authority migration with all original receipts/holds, old writers fenced and duplicate-spend prevention. No standalone copied ledger is admitted. The study owner must reconcile changed totals before updating a new packet; do not edit the hardcoded baseline to bypass this check.
3. Resolve delivery of only Vishesh's dedicated Swarm Lab Anthropic credential through the authorized secure path, plus verified routing metadata. The current local-only store is not available to the orbital-one operator by assumption. Do not substitute any Dmarz/general/project-other key or copy a credential bundle. No credentials in arguments/files/reports. No persistent secret installation.
4. In a clean exact-source checkout on the allocated worker, run `python3 -m unittest discover -s researchers/vishesh/notes/optimal-swarm-size/src -p 'test_*.py' -q` (63 tests). This is software validation, no model calls. Preserve source and run fields in private deployment evidence.

## Registration and launch

Let `STUDY` refer to `researchers/vishesh/notes/optimal-swarm-size`, `PIN` be the queue request's full source commit, and `PRIVATE` the allocated worker's private receipt/output directory. These names are shell placeholders, not environment changes to HOME/CODEX_HOME. Run from the exact clean repository root:

```sh
python3 "$STUDY/src/register.py" --plan-url "https://github.com/dmarzzz/swarm-lab/blob/$PIN/$STUDY/reviews/q-a7-input-binding-plan.md"
python3 researchers/vishesh/notes/experiment-documentation/public_plan.py --experiment optimal-swarm-size-q1 --run-tldr 'TLDR: Q-A7 fixed N1 full versus explicit public-input bindings on two fresh roots; correctness, correct items/second, cost; bounded competence diagnostic with futility stop, no size-effect claim.' --receipt "$PRIVATE/public-plan-q-a7.json"
python3 "$STUDY/src/admit_input_binding.py" --admission "$PRIVATE/admission.json" --ledger "$CANONICAL_LEDGER" --output "$PRIVATE/Q-A7-binding" --public-receipt "$PRIVATE/public-plan-q-a7.json"
# Only after all checks pass and dedicated credentials are securely delivered in process memory:
timeout --signal=TERM 7200 python3 "$STUDY/src/admit_input_binding.py" --admission "$PRIVATE/admission.json" --ledger "$CANONICAL_LEDGER" --output "$PRIVATE/Q-A7-binding" --public-receipt "$PRIVATE/public-plan-q-a7.json" --run
```

Admission is a private operator attestation, not independent fleet verification. JSON fields: `source_commit` (PIN), `attempt_id` (`q-a7`), `dispatch_origin` (`orbital-one`), positive `queue_issue`, actual `claim_id`, `verified_epoch` (within300seconds), `claim_expiry_epoch` (>7500seconds remaining), `canonical_ledger_path` (absolute actual single-writer authority), `credential_alias` (`swarm-lab-anthropic/vishesh`), and true booleans `exclusive_claim_verified`, `approved_account_verified`, `sole_ledger_writer_verified`, `prior_worker_stopped`, `prior_artifacts_verified`, `dedicated_credential_provenance_verified`. Check those facts against live private inventory, claim, process and credential provenance before attesting. Do not include credential values or account IDs. Prepare a fresh receipt immediately before dispatch; a historical receipt is insufficient.

The launcher requires `SWARM_MODEL_API_KEY` and verified `SWARM_MODEL_WORKSPACE_ID` only in its process environment, rejects general provider fallback variables, and never looks up keys. Its operator must disable core dumps/agent forwarding and bound secret lifetime to the admitted worker process. Preflight checks exact source/public plan, immutable budget baseline and absence of Q-A7 calls/output/runtime marker. It never allocates, migrates funds or discovers credentials. An ambiguous dispatch is not retryable: inspect original journal/worker/calls first. Never delete an output/runtime marker to retry.

## Stops and closeout

Eight manifest assignments; root6's four completed episodes can trigger the declared futility stop, preserving root7 as unstarted. A planned futility stop returns success for the bounded procedure but does not claim all eight outcomes observed or scientific support. Other runtime/schema/usage/route/budget/claim/publication failures stop with failure. All substantive wrong answers remain outcomes. Max152 model calls, USD2 attempt ceiling within original USD20, no automatic retry/increase/new ledger.

The admission wrapper calls the shared offline `finalize` bridge after native termination. If externally interrupted, verify this worker and children stopped, reconcile unknown charges, then call `scripts/experiment.py finalize optimal-swarm-size --attempt q-a7 --results <output> --outcome failed --worker-stopped`; do not recollect to repair reporting. Finish scientific review against RUN-QUALITY separately. Read back assignment/trace/outcome/replay artifacts by hash and verify public condition TLDRs. Check measured playback initial/transition/final views and correct throughput labels. Preserve failures and unstarted denominators, update only owned evidence metadata, report actual/held spend, release only this allocation, and close the queue issue. Gate failures return to vishesh/codex-idea-scores; no successor is authorized by this packet.
