# Runbook: sybil-scarcity-opus, chain 001

Nothing here has been run. This file is for the operator who takes the request from the private run queue. The server is a parameter. Public files contain no server address, hub address, token or credential.

## Before launch

1. The run request is in the private run queue and dmarz/fleet-monitor has done its same-researcher check of this package. Cross-researcher review is waived by dmarz for these exploratory runs (relayed by dmarz/fleet-monitor, 2026-10-04); the run is not independently reviewed.
2. Read [reviews/chain-001-pre.md](reviews/chain-001-pre.md). It names the pinned commit and the source hash. [READY.yaml](READY.yaml) carries the same hash, the number of selftests, the call caps, the dollar cap and the chain timeout.
3. Take the exclusive server claim `dmarz-sybil-scarcity-opus` (`experiment: sybil-scarcity-opus`).
4. The server checkout must contain this directory and `researchers/dmarz/notes/sybil-scale-api/src/` (S0 and the selftests compare against the unmodified parent code). Python 3.12 with `requirements.txt`.

## Commands

The generic private launcher, from the agentops repository:

```
python3 scripts/run-ready-chain.py sybil-scarcity-opus <commit> setup --host <server>
python3 scripts/run-ready-chain.py sybil-scarcity-opus <commit> chain --host <server> --confirm-paid
python3 scripts/run-ready-chain.py sybil-scarcity-opus <commit> status --host <server>
python3 scripts/run-ready-chain.py sybil-scarcity-opus <commit> verify --host <server>
```

- `setup` checks out `<commit>`, installs the pinned requirements, runs `python3 src/selftest.py` and compares the number of tests and `study.source_hash()` with `READY.yaml`.
- `chain` starts one detached process, `python src/chain.py run --stages S0,P0,Q0,S1`, with `SWARM_MODEL_API_KEY`, `SWARM_MODEL_WORKSPACE_ID`, `STUDY_BUDGET_LEDGER`, `STUDY_RESULTS_DIR` and `SWARM_SOURCE` in its environment and the hub client on `PYTHONPATH`. `--confirm-paid` is required because P0, Q0 and S1 make model calls: 1, 48 and 1,440.
- `status` prints `chain-status.json` and the ledger totals. `verify` checks artifact checksums against the hub, regrades every saved row and recomputes the summary and the analysis. Both print one JSON object on the last line; neither needs the model credential.

## What the chain does by itself

| Stage | Calls | Gate to pass | If it fails |
|---|---|---|---|
| S0 | 0 | 168 scripted rows valid, scripted qualification passes, every invariant holds | chain stops; nothing paid has happened |
| P0 | 1 | answer parses, model id matches, usage reported, stop reason `end_turn`, six values equal the expected values | chain stops after one call |
| Q0 | 48 | 48 valid; per carrier profile: fields ≥ 95%, exact packets ≥ 90%, null on every withheld rare fact | chain stops; S1 is never queued |
| S1 | 1,440 | before queueing: 1,440 × Q0's mean cost per call must fit in the remaining dollar cap | chain stops with `projection_exceeds_cap` before any S1 call |

Exit code 0: all requested stages done. Exit code 3: stopped at a failed stage or a refused gate; `chain-status.json` has `state: stopped_at_gate`, the stage and the reason. Any other non-zero code: internal error. There are no answer retries and no agent is needed between stages. A request rejected with HTTP 429 or 529 is resent at most twice inside its 300 s budget. The first failed call of a stage stops new dispatch; calls in flight finish; the rest are recorded as not started.

Limits in the hashed design: 4 requests in flight; 300 s per request; 14,400 s per stage; 18,000 s for the chain; 1,489 calls; 1,640 transport attempts; USD 220 of settled cost plus open reservations. Expected: about USD 141 to 155 and about 40 minutes.

## After the chain

1. `status`, then `verify`. Keep both outputs.
2. Do not rerun a stage. A batch name is refused the second time. A repair is a new attempt number in `design.yaml`, which changes the source hash, and needs its own pre-run review.
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
