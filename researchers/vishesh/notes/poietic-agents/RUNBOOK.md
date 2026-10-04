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

Preparation writes assignment identifiers and a source-hash inventory, not private source fixtures or answer labels. The last command intentionally fails with `study_budget_not_authorized` until authentic current admission evidence exists. Never flip placeholder booleans to simulate approval. `src/launch.py run` is the only native entry point; it repeats admission, deployed-source, live public-plan and current provider-route checks. There is no paid smoke/test bypass or S1/S2 launch flag.

## Remaining steps before the first model call

1. Record the owner's Poietic-specific S0 response: requested maximum $5 API plus $2 infrastructure. The 288-call worst case at pinned prices is $1.447723008; the larger proposed API allowance can cover separately assessed bounded repairs. No previous study's budget applies. Preserve the single authority across attempts; a replacement host cannot recreate the cap.
2. Verify the approved OpenRouter credential selector/provenance privately. The current worker expects one ephemeral `POIETIC_OPENROUTER_KEY` value consumed inside its authorized process. This is an interface, **not authorization to transfer an unrelated key**. Do not reuse the Anthropic-only transfer permission for OpenRouter. Use an approved local credential relay or explicitly authorized ephemeral transfer after the destination/budget gates are satisfied. Do not print, persist or put the value in shell arguments. Missing approved credential provenance blocks dispatch.
3. Refresh private fleet and claims, verify real workload, obtain a fresh exclusive allocation tied to Poietic, and confirm its lifetime and billing attribution. Current read-only inspection reached unclaimed candidates but saw active runtime processes, so none is certified idle or claimed. Do not stop those processes. If provisioning is needed, Dmarz's established account/state/project must be verified by its authorized provisioner. Follow [machine workflow](../experiment-machine-workflow.md).
4. Freeze and push source. Deploy that exact revision plus the pinned Pillow dependency. Run the tests there. Record source/runtime checks, output location, merged claim revision, actual hostname, workload check, allocation charge start/hourly rate and expiry. Infrastructure lifetime including upload allowance must fit $2. One worker, one ledger under `/srv/swarm/poietic-agents-authority`, one filesystem lock. Never copy that ledger into independent authorities.
5. Publish/register the exact immutable README URL, run condition-specific TLDRs and verify the public page. Pin content hash and source inventory in a new admission record derived from `prepare.py`; record the actual owner authorization and private-fleet receipt, not fictitious evidence. Commit the S0 pre-assessment as ready only when the gates are true. `public_plan.check` is mandatory at launch and the current registration must match the expected URL/hash.
6. Execute exactly the named S0-01 attempt, after all guards pass:

```sh
python3 researchers/vishesh/notes/poietic-agents/src/launch.py run \
  --config /srv/swarm/poietic/S0-01-admission.json \
  --out /srv/swarm/poietic/results/S0-01
```

The worker reads no credential file, uses no default provider credential, and logs only public fixture requests and allowlisted responses. It reserves before dispatch, retains uncertain charges, permits one retry only for a rejected HTTP 429, and never retries malformed generations or ambiguous timeouts. It reports three contract-specific runs under a common stage authority. No source/config/model fallback is silent.

## Qualification and the subsequent pilot

S0 requires each of Haiku, Qwen and Jev to produce at least 44/48 correct, 48/48 schema-valid responses and zero protected-access violations. Cases contain four dependent steps; this is an interface screen, not 144 independent tasks or a 95%-reliability claim. Reconcile all 144 assigned statuses, starts, physical requests, records, costs, PNG frames and upload acknowledgements. Retain failures and write the human-readable post-mortem using the automatic receipt as input. A partial failure cannot be discarded. Repair on development cases; publish an amendment and fresh disjoint attempt before requalification. Do not lower thresholds to relabel a failure.

Only after successful S0: select/freeze A2 on development data with its construction ledger; check and admit S1's 16 lineages/768 jobs and $25 API/$4 infrastructure proposal under a separate owner authorization. The persistent mechanism is implemented in `src/lineage.py`, injected with a metered backend; the CLI deliberately does not admit S1 yet. A3 starts uniform and chooses changes itself; S0's explicit action instructions never become the pilot policy. Reconcile authoritative API/infrastructure costs before interpreting lineage summaries, whose known API subtotal is explicitly a lower bound.

S2 remains closed pending the full question-specific survey/hypothesis gates, stronger comparator selection, power/precision planning and a new preregistration. A0–A3 feasibility work cannot certify a novel optimizer or biological result.

## Closeout and reporting

Renderer unit fixtures in `fixtures/` say SCRIPTED — NOT MODEL EVIDENCE and are never uploaded as observed runs. S0 retains per-case PNG progress frames and a final 1600-pixel PNG. The browser-checked event replay is local HTML; public embedding is not promised until supported. No actual animation can exist before native events.

After execution, verify durable artifact readback, preserve failure/usage records, stop only Poietic workers and release its claim. The fleet owner handles teardown. Record execution, qualification, scientific interpretation, process compliance and artifact delivery separately.
