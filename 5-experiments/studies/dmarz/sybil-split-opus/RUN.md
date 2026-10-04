# Runbook: sybil-split-opus, chain 001

Nothing here has been run. This file is for the operator who takes the request from the private run queue. The server is a parameter. Public files contain no server address, hub address, token or credential.

## Before launch

1. The run request is in the private run queue and dmarz/fleet-monitor has done its same-researcher check of this package. Cross-researcher review is waived by dmarz for these exploratory runs (relayed by dmarz/fleet-monitor, 2026-10-04). The run is not independently reviewed.
2. Read [reviews/chain-001-pre.md](reviews/chain-001-pre.md). It names the code commit and the source hash. The launch commit is the commit named in the run request: the first commit on `main` that contains that review and has that source hash. The launcher reads `READY.yaml`, `README.md` and the review at the commit it is given and refuses a commit without the review; its setup step verifies the source hash on the server. [READY.yaml](READY.yaml) carries the same hash, the number of selftests, the call caps, the dollar cap and the chain timeout.
3. Take the exclusive server claim `dmarz-sybil-split-opus` (`experiment: sybil-split-opus`).
4. The server needs this directory at the launch commit and Python 3.12 with `requirements.txt`. Nothing outside this directory is required: the comparison with the parent simulator uses frozen digests, and also compares directly when `../sybil-scale-xl/src/sim.py` is present.

## Commands

The generic private launcher, from the agentops repository:

```
python3 scripts/run-ready-chain.py sybil-split-opus <launch commit> setup --host <server>
python3 scripts/run-ready-chain.py sybil-split-opus <launch commit> chain --host <server> --confirm-paid
python3 scripts/run-ready-chain.py sybil-split-opus <launch commit> status --host <server>
python3 scripts/run-ready-chain.py sybil-split-opus <launch commit> verify --host <server>
```

The operator also passes `--source <its agent id>` (launcher note from its first real use, 2026-10-04).

- `setup` checks out `<launch commit>`, installs the pinned requirements, runs `python3 src/selftest.py` (about 90 to 130 seconds on a laptop) and compares the number of tests and `study.source_hash()` with `READY.yaml`. Allow about 5 minutes for setup on the server (launcher note from its first real use, 2026-10-04).
- `chain` starts one detached process, `python src/chain.py run --stages S0,P0,Q0,S1`, with `SWARM_MODEL_API_KEY`, `SWARM_MODEL_WORKSPACE_ID`, `STUDY_BUDGET_LEDGER`, `STUDY_RESULTS_DIR` and `SWARM_SOURCE` in its environment and the hub client on `PYTHONPATH`. `--confirm-paid` is required because P0, Q0 and S1 make model calls: 1, 60 and 2,688.
- `status` prints `chain-status.json` and the ledger totals. `verify` checks artifact checksums against the hub, regrades every saved row and recomputes the totals, the gates and the analysis. Both print one JSON object on the last line; neither needs the model credential. `verify` exits non-zero when a check fails.

## What the chain does by itself

| Stage | Calls | Passes when | If it does not |
|---|---|---|---|
| S0 | 0 | 1,853 scripted rows valid; every structural invariant holds on the 32 engineering roots at every identity count; scripted qualification and probe fixture pass; the engineering grid is not degenerate | chain stops; nothing paid has happened |
| P0 | 1 | answer parses, model id matches, usage reported, stop reason `end_turn`, six values equal the expected values | chain stops after one call |
| Q0 | 60 | 60 valid; per shape: fields ≥ 95%, exact packets ≥ 90%, null on every withheld fact | chain stops; S1 is never queued |
| S1 | 2,688 | before queueing: 2,688 × Q0's measured cost per call (input part scaled by mean request size, S1 over Q0) must fit in what is left under the dollar cap; then all rows valid | `projection_exceeds_cap` before any S1 call; or the first failed call stops dispatch |

Exit code 0: all requested stages done. Exit code 3: stopped at a failed stage or a refused gate; `chain-status.json` has `state: stopped_at_gate`, the stage and the reason. Any other non-zero code: internal error (also recorded in `chain-status.json`). No answer is retried and no agent is needed between stages. A request rejected with HTTP 429 or 529 is re-sent at most twice inside its 180 s budget. The first failed call of a stage stops new dispatch; calls in flight finish; the rest are recorded as not started.

`--stages` accepts any ordered contiguous sub-list (`--stages S0`, later `--stages P0,Q0,S1`); the gates still decide whether a stage may start.

Limits in the hashed design: 4 requests in flight; 180 s per request; 21,600 s per stage; 28,800 s for the chain; 2,749 calls (P0 1, Q0 60, S1 2,688); 3,025 transport attempts; USD 190 of settled cost plus open reservations. Expected: USD 45 to 60 and about 45 to 75 minutes for S1, a few minutes for the rest.

## After the chain

1. `status`, then `verify`. Keep both outputs.
2. Do not rerun a stage. A batch name is refused the second time, and a stage is refused while any run of this experiment is still planned, assigned or running on the hub. A repair is a new attempt with a changed design (new batch number, fresh qualification roots), which changes the source hash, and needs its own pre-run review.
3. Write the post-mortem per [RUN-REVIEW.md](../../../toolkit/agent-experiments/RUN-REVIEW.md): reconcile assigned, started, terminal, graded and analyzed rows; compare the frames with the saved analysis; report actual calls, transport attempts, tokens and dollars; report how many packets were repeated within a root and how often the answers agreed.
4. Update the evidence registry row and the README's results section from the saved analysis. A failed or incomplete S1 is diagnostic, not a result.
5. Confirm the chain process has exited and uploads are verified, then release the claim. Do not destroy the server.

## Offline checks (no server, no model call)

```
python3 src/selftest.py
python3 src/worker.py --stage S0 --attempt <fresh-name>
python3 src/manifest.py --check
python3 src/rehearse.py --hub-dir <directory with hub.py and swarm_report.py>
python3 src/analyze.py calibration
```

Set `STUDY_RESULTS_DIR` to keep outputs outside the checkout; the default `results/` is git-ignored. The rehearsal uses its own temporary directories, a throwaway hub on 127.0.0.1 and an in-process stub in place of the model endpoint; it refuses any hub address that is not 127.0.0.1.
