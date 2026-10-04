# Poietic Agents execution handoff

Use the [required setup runbook](../../../../tooling/agent-experiments/EXPERIMENT-SETUP.md), [setup record](SETUP.md), [protocol](PROTOCOL.md), [amendments](AMENDMENTS.md) and [review resolution](REVIEW-RESOLUTION.md). Current gate: G3 admission for S0-01. The offline instrument exists; no native run has started. This handoff does not authorize spending or make an unavailable host idle.

## Reproduce the completed offline work

From the repository root, using Python 3.11 or later:

```sh
python3 -m pip install -r researchers/vishesh/notes/poietic-agents/requirements.txt
python3 -m unittest discover -s researchers/vishesh/notes/poietic-agents/tests -v
python3 researchers/vishesh/notes/poietic-agents/src/prepare.py --out /private/tmp/poietic-s0-candidate
python3 researchers/vishesh/notes/poietic-agents/src/launch.py check --config /private/tmp/poietic-s0-candidate/candidate.json
```

Preparation writes assignment identifiers and a source-hash inventory, not private source fixtures or answer labels. The last command intentionally fails with a missing admission field until authentic current admission evidence exists. The reduced $2 budget proposal still needs explicit user confirmation; host/credential/deadline evidence is also missing. Never flip placeholder booleans to simulate approval. `src/launch.py run` is the only native entry point; it repeats admission, deployed-source, live public-plan and current provider-route checks. There is no paid smoke/test bypass or S1/S2 launch flag.

## Remaining steps before the first model call

1. Resolve [AUTHORIZATION.json](AUTHORIZATION.json): explicit confirmation is pending for $2 total, proposed as $1.50 API/$0.50 infrastructure. The 288-call S0 worst case is $1.447723008. Carry spend/reservations forward across every stage and attempt; this is not a per-run allowance. No larger budget is granted by the earlier planning proposal.
2. Resolve the approved OpenRouter credential file selector privately (path only, never its contents in chat). The new `src/relay.py` consumes it locally with owner-only permissions and no redirects; it accepts only the 144 assigned role/step IDs, pinned model routes, exact token/settings limits and at most 288 physical attempts. An SSH reverse tunnel binds only remote loopback. The worker receives no provider key, and the Anthropic-only transfer policy is not stretched to cover OpenRouter. The local persistent relay ledger is the sole credential-bearing API authority; the remote ledger is a conservative reporting mirror, not a second spending pool. Verify both and count each provider call once. Missing selector/provenance blocks admission.
3. Refresh private fleet and claims, verify real workload, obtain a fresh exclusive allocation tied to Poietic, and confirm its lifetime and billing attribution. Refined read-only checks found sim-dmarz had no active containers or recognized experiment workers; it is a plausible candidate, still unclaimed. Recheck fresh claims/workload at admission. Do not stop those processes. If provisioning is needed, Dmarz's established account/state/project must be verified by its authorized provisioner. Follow [machine workflow](../experiment-machine-workflow.md).
4. Freeze and push source. Deploy that exact revision plus the pinned Pillow dependency. Run the tests there. Record source/runtime checks, output location, merged claim revision, actual hostname, workload check, allocation charge start/hourly rate and expiry. Infrastructure lifetime including upload allowance must fit $0.50. One worker and one on-host reporting ledger under `/srv/swarm/poietic-agents-authority`, with a filesystem lock. Preserve the sole credential-bearing local relay ledger across attempts; never create independent spending copies.
5. Publish/register the exact immutable README URL, run condition-specific TLDRs and verify the public page. Pin content hash and source inventory in a new admission record derived from `prepare.py`; record the actual owner authorization and private-fleet receipt, not fictitious evidence. Commit the S0 pre-assessment as ready only when the gates are true. `public_plan.check` is mandatory at launch and the current registration must match the expected URL/hash.
6. Execute exactly the named S0-01 attempt, after all guards pass:

```sh
python3 researchers/vishesh/notes/poietic-agents/src/launch.py run \
  --config /srv/swarm/poietic/S0-01-admission.json \
  --out /srv/swarm/poietic/results/S0-01
```

The worker connects only to the pinned loopback SSH relay, reads no credential file, uses no provider credential, and logs only public fixture requests and allowlisted responses. It reserves before dispatch, retains uncertain charges, permits one retry only for a rejected HTTP 429, and never retries malformed generations or ambiguous timeouts. It reports three contract-specific runs under a common stage authority. No source/config/model fallback is silent.

## Qualification and the subsequent pilot

S0 requires each of Haiku, Qwen and Jev to produce at least 44/48 correct, 48/48 schema-valid responses and zero protected-access violations. Cases contain four dependent steps; this is an interface screen, not 144 independent tasks or a 95%-reliability claim. Reconcile all 144 assigned statuses, starts, physical requests, records, costs, PNG frames and upload acknowledgements. Retain failures and write the human-readable post-mortem using the automatic receipt as input. A partial failure cannot be discarded. Repair on development cases; publish an amendment and fresh disjoint attempt before requalification. Do not lower thresholds to relabel a failure.

Only after successful S0: select/freeze A2 on development data with its construction ledger; check and admit S1's 16 lineages/768 jobs under the same remaining amount if the $2 proposal is approved. The old $25/$4 planning ceiling is not authorized; any necessary increase requires a concrete owner decision before dispatch. The persistent mechanism is implemented in `src/lineage.py`, injected with a metered backend; the CLI deliberately does not admit S1 yet. A3 starts uniform and chooses changes itself; S0's explicit action instructions never become the pilot policy. Reconcile authoritative API/infrastructure costs before interpreting lineage summaries, whose known API subtotal is explicitly a lower bound.

S2 remains closed pending the full question-specific survey/hypothesis gates, stronger comparator selection, power/precision planning and a new preregistration. A0–A3 feasibility work cannot certify a novel optimizer or biological result.

## Closeout and reporting

Renderer unit fixtures in `fixtures/` say SCRIPTED — NOT MODEL EVIDENCE and are never uploaded as observed runs. S0 retains per-case PNG progress frames and a final 1600-pixel PNG. The browser-checked event replay is local HTML; public embedding is not promised until supported. No actual animation can exist before native events.

After execution, verify durable artifact readback, preserve failure/usage records, stop only Poietic workers and release its claim. The fleet owner handles teardown. Record execution, qualification, scientific interpretation, process compliance and artifact delivery separately.

## Local credential relay command

After both local and remote admission receipts are real, start the bounded relay locally with `src/relay.py --config <admission.json> --credential-file <approved-selector> --ledger <persistent-poietic-ledger> --port-file <local-port-file>`. Values in angle brackets are paths/selectors, never credentials. Use verified SSH to forward a remote loopback port to the reported local port; write that exact `http://127.0.0.1:<port>/invoke` URL into the admission credential record. Stop the relay/tunnel after receipt reconciliation. This command makes no new permission or host claim.
