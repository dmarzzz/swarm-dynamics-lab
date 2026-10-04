# Poietic S0 central dispatch handoff

2026-10-04 UTC. Owner: vishesh. Experiment: `poietic-agents`. Stage: `S0`, attempt `S0-01`. This is a prospective handoff, not a launched run. The operator follows the private fleet's `docs/RUN-QUEUE.md` from orbital-one; the laptop does not start the experiment. Gate failures return to vishesh/codex-heterogeneous. Do not launch S1 from this handoff.

## Authority and admission

The direct owner message asking for the proper actual-model run accepts the immediately preceding $2 total proposal. See [AUTHORIZATION.json](AUTHORIZATION.json). The single cumulative allowance is $1.50 API plus $0.50 infrastructure, across stages, attempts, repairs and machines; spent and uncertain balances are currently zero. Independent design review was completed and P1–P3 resolved in [REVIEW-RESOLUTION.md](REVIEW-RESOLUTION.md); no waiver or independent code audit is claimed.

Current blockers are a verified approved OpenRouter selector and fresh runtime admission. The local configuration directory is empty and the exact project Keychain metadata lookup found no entry. No credential value was requested or printed. The dispatcher may resolve an existing authorized Swarm Lab credential on its own runtime, recording its selector/provenance privately. Do not use a general personal credential or transfer a provider key based on this handoff. The actor worker never receives the provider key.

Choose an idle existing eligible host in the approved private fleet. The former candidate `sim-dmarz` is now occupied. No new provisioning allowance beyond the $0.50 infrastructure allocation is implied. Take a merged exclusive claim named `vishesh-poietic-s0-01`, tied to this experiment, only once credential and deployment prerequisites are ready. Record exact hourly price and charge start; deadline plus upload allowance must fit the cap. Keep the claim alive through artifact verification.

## Frozen deployment and preparation

The queue request pins the full public source commit. Deploy that same clean commit on the coordinator and exclusively allocated worker; do not pull the frozen checkouts after preparing admission. Use Python 3.11+ and Pillow 11.3.0. The reporting module is preinstalled on fleet workers; set `PYTHONPATH=/usr/local/lib/swarm` when invoking the worker.

From each frozen repository root:

```sh
python3 -m pip install -r 5-experiments/studies/vishesh/poietic-agents/requirements.txt
python3 -m unittest discover -s 5-experiments/studies/vishesh/poietic-agents/tests -q
python3 5-experiments/studies/vishesh/poietic-agents/src/prepare.py --out /srv/swarm/poietic/preparation/S0-01
```

Use a virtual environment if system Python is externally managed. The exact interpreter used for tests must run the instrument. Preparation writes assignment identifiers and hashes only; it must not open the reserved world fixtures. The candidate remains intentionally non-authorizing. Construct the private admission JSON from that candidate and authentic current receipts, using the exact schema in `src/admission.py`:

- `authorization`: study `poietic-agents`, stage `S0`, owner approved, reference to the direct-owner record, API 1.5 / infrastructure 0.5 / total 2, physical calls 288, deadline at most two hours ahead. Preserve this authority and its ledger thereafter; changing a deadline is not a budget reset.
- `allocation`: actual worker hostname, exact claim ID and merged revision, experiment/operator, verified exclusive registered approved-account destination, observed idle workload, check time under five minutes old, expiry at least deadline plus 300 seconds, exact allocated hourly rate and charge start. Retain supporting private evidence. The operator must not simply flip the candidate booleans.
- `credential`: alias `swarm-lab-openrouter`, study authorization verified from genuine provenance, `relay_url` equal to the worker's loopback forwarding endpoint. The approved coordinator credential file is owner-only, nonsymlink, with one key and no other contents. Its path belongs only in the private coordinator command; the key never appears in command arguments.
- `public_plan`: exact currently registered immutable README URL and SHA-256 returned by the shared public-plan helper. `page_verification` records actual rendered-page verification of that same URL within 24 hours. Keep the candidate's three condition-specific TLDRs.
- `source_commit`, `file_hashes`, `assignment_sha256`: exact frozen deployment, not a previous validation receipt. `worker_count=1`, `concurrency=1`, and the real historical review resolution remain unchanged.

Save `/srv/swarm/poietic/S0-01-admission.json` on both coordinator and worker. No secrets are in it, but allocation evidence remains private. Repeat `src/launch.py check --config /srv/swarm/poietic/S0-01-admission.json` on the worker. Preparation/admission refusal makes no paid probe and must not be relabeled a failed model qualification.

## Start once, after admission

On the approved coordinator, start the existing bounded relay using the protected credential selector and a persistent study-wide ledger. Replace angle-bracket path placeholders with verified private paths; never with secret values.

```sh
python3 5-experiments/studies/vishesh/poietic-agents/src/relay.py \
  --config /srv/swarm/poietic/S0-01-admission.json \
  --credential-file <approved-protected-file> \
  --ledger /srv/swarm/poietic-authority/api.sqlite \
  --port-file /srv/swarm/poietic-authority/relay.port
```

The coordinator is the sole credential-bearing authority. Establish a verified encrypted SSH reverse tunnel to the allocated worker, bound to remote `127.0.0.1`, with `ExitOnForwardFailure=yes` and host-key checking. The remote port must match `credential.relay_url`. Neither the key nor an authorization header travels to the worker. Call `/health` through the tunnel and require the exact attempt, source, assignment digest, credential-ready status, deadline and **zero prior physical calls**. A mismatch blocks start. Do not recreate the ledger or replay an ambiguous dispatch.

Then invoke on the allocated worker, with the same frozen source and interpreter:

```sh
PYTHONPATH=/usr/local/lib/swarm python3 5-experiments/studies/vishesh/poietic-agents/src/launch.py run \
  --config /srv/swarm/poietic/S0-01-admission.json \
  --out /srv/swarm/poietic/results/S0-01
```

The launcher repeats source, admission, public-plan, provider-catalog and relay-health checks before hub start or a provider request. It starts three condition-specific runs: `poietic-S0-01-generalist`, `poietic-S0-01-cheap_generative`, `poietic-S0-01-typed_choice`. This is native qualification of Haiku 4.5/Anthropic, Qwen3 8B/Alibaba and Jev 1.13/TypeSafe, through the pinned OpenRouter routes; no fallback. There are 144 logical assignments, at most 288 physical requests, one eligible 429 retry only. Maximum pinned request reservations total $1.447723008.

## Outcome and closeout

Every model contract must reach at least 44/48 correct, 48/48 schema-valid and zero protected-access violations. Retain all 144 assigned outcomes, including failed or unstarted ones. Twelve four-step cases per model are dependent lifecycle probes, not 144 independent experimental roots. S0 establishes interface readiness, not swarm efficiency or spontaneous specialization.

Reconcile the coordinator API ledger with the worker reporting mirror without counting them twice. Preserve uncertain charges at their reserved upper bound. Add infrastructure from actual allocation charge start through release, not only worker elapsed time. Verify PNG/progress/final artifacts, request/response evidence, hub terminal states, acknowledgements and durable readback. Write `reviews/S0-01-post.md` even after interrupted dispatch. Then stop only Poietic processes/tunnel and release the claim; the owner controls machine teardown.

A failed qualification blocks S1. Diagnose using development fixtures and preserve the original; no fresh qualification attempt is admitted by the current `S0-01`-only launcher. Any repair needs a prospective amendment and disjoint case namespace within the same remaining budget. Do not lower thresholds or discard a failed model. If qualification passes, return the exact qualification hashes and remaining budget for development selection of A2 and a separately admitted S1 orchestrator. S2 stays closed.
