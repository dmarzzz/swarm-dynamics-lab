# Runbook: false-alarm-cascade, chain 001

Nothing here has been run. This file is for the operator who takes the request from the private run queue. The server is a parameter. Public files contain no server address, hub address, token or credential.

## Before launch

1. The run request is in the private run queue, filed after dmarz/fleet-monitor's same-researcher check of this package. Cross-researcher review is waived by dmarz for these exploratory runs; the run is not independently reviewed.
2. Read [reviews/chain-001-pre.md](reviews/chain-001-pre.md). It names the code commit and the source hash. [READY.yaml](READY.yaml) carries the same hash, the number of selftests, the call caps, the dollar cap and the chain timeout.
3. Launch with the commit named in the run request, written `<commit>` below: the first commit on main that contains the pre-run review and has this source hash. Do not launch with the code commit: the launcher reads `READY.yaml`, `README.md` and the review at the commit it is given and refuses a commit without the review.
4. Take the exclusive server claim `dmarz-false-alarm-cascade` (`experiment: false-alarm-cascade`).
5. The server checkout needs only this directory. Python 3.12 with `requirements.txt`. The study imports nothing from other studies.
6. The workspace is shared with other dmarz runs. This chain keeps at most 10 requests in flight (2 episodes × 5 agents in S1; 5 in Q0).

## Commands

The generic private launcher, from the agentops repository:

```
python3 scripts/run-ready-chain.py false-alarm-cascade <commit> setup --host <server>
python3 scripts/run-ready-chain.py false-alarm-cascade <commit> chain --host <server> --confirm-paid
python3 scripts/run-ready-chain.py false-alarm-cascade <commit> status --host <server>
python3 scripts/run-ready-chain.py false-alarm-cascade <commit> verify --host <server>
```

- `setup` checks out `<commit>`, installs the pinned requirements, runs `python3 src/selftest.py` and compares the number of tests and `study.source_hash()` with `READY.yaml`.
- `chain` starts one detached process, `python src/chain.py run --stages S0,P0,Q0,S1`, with `SWARM_MODEL_API_KEY`, `SWARM_MODEL_WORKSPACE_ID`, `STUDY_BUDGET_LEDGER`, `STUDY_RESULTS_DIR` and `SWARM_SOURCE` in its environment and the hub client on `PYTHONPATH`. `--confirm-paid` is required because P0, Q0 and S1 make model calls: 1, 24 and 3,600.
- `status` prints `chain-status.json` and the ledger totals. `verify` checks artifact checksums against the hub, rebuilds every actor input from the fixed inputs and the saved answers, regrades every saved row and recomputes the summary and the analysis. Both print one JSON object on the last line; neither needs the model credential.

## What the chain does by itself

| Stage | Calls | Gate to pass | If it fails |
|---|---|---|---|
| S0 | 0 | 1,225 scripted rows valid; scripted qualification and probe pass; all 16 invariants hold, including the negative control (private-evidence script: zero alarm effect) and the positive control (credulous script: full cascade and full recovery) | chain stops; nothing paid has happened |
| P0 | 1 | answer parses, model id matches, usage reported, stop reason `end_turn`, decisions equal the reference on every resource whose three inspections agree | chain stops after one call |
| Q0 | 24 | 24 valid; decisions equal the private-evidence reference on at least 90% of gated decisions overall (134) and at each depth (35, 34, 65) | chain stops; S1 is never queued |
| S1 | 3,600 | before queueing: 3,600 × Q0's mean cost per call × 1.25 must fit in the remaining dollar cap | chain stops with `projection_exceeds_cap` before any S1 call |

Exit code 0: all requested stages done. Exit code 3: stopped at a failed stage or a refused gate; `chain-status.json` has `state: stopped_at_gate`, the stage and the reason. Any other non-zero code: internal error. There are no answer retries and no agent is needed between stages. A request rejected with HTTP 429 or 529 is resent at most twice inside its 300 s budget.

S1 runs 120 team episodes, two at a time. Inside an episode the six rounds run in order and the five agent calls of a round are sent together. If any call fails, its episode ends there, no new episode and no new round starts anywhere, calls in flight finish, and every remaining call is recorded as not started. The hub run then ends `failed` with its usage reported; the completed rows stay valid data.

Limits in the hashed design: 10 requests in flight; 300 s per request; 28,800 s per stage; 32,400 s for the chain; 3,625 calls; 4,000 transport attempts; USD 360 of settled cost plus open reservations. Expected: about USD 120 and about 1.5 to 4.5 hours (see the pre-run review).

## After the chain

1. `status`, then `verify`. Keep both outputs.
2. Do not rerun a stage. A batch name is refused the second time. A repair is a new attempt number in `design.yaml`, which changes the source hash, and needs its own pre-run review. After a failed Q0 the first step is to read the failing answers with their packets (they are in `episodes.jsonl.gz`); a repaired attempt uses fresh qualification roots.
3. Write the post-mortem per [RUN-REVIEW.md](../../../../tooling/agent-experiments/RUN-REVIEW.md): reconcile assigned, started, terminal, graded and analyzed rows; compare the frames with the saved analysis; report actual calls, tokens and dollars.
4. Confirm the chain process has exited and uploads are verified, then release the claim. Do not destroy the server.

## Offline checks (no server, no model call)

```
python3 src/selftest.py
python3 src/worker.py --stage S0 --attempt <fresh-name>
python3 src/manifest.py --check
python3 src/rehearse.py --hub-dir <directory with hub.py and swarm_report.py>
```

Set `STUDY_RESULTS_DIR` to keep outputs outside the checkout; the default `results/` is git-ignored.
