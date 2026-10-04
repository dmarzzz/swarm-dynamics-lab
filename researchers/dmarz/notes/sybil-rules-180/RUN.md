# How to run sybil-rules-180 (operator)

Nothing here is run by the builder. Paid stages need dmarz/fleet-monitor's go, recorded on the run request. Server names, addresses and the credential stay in the private fleet repository (`dmarzzz/swarm-labs-agentops`); none of them belongs in this public repository.

## Model

The model is a launch parameter (`STUDY_MODEL`, set by the launcher's `--model`) from design.yaml `models`. The program's model `qwen/qwen3.7-flash` is the default and the only one admitted at this commit; another model is its own chain with its own ledger, cap, batch names and worker-session experiment.

## Topology

- Three dmarz servers, named at launch (free when this was written: sim-dmarz-2, sim-dmarz-8, sim-dmarz-10). The first named server runs the coordinator (`src/chain.py`: world state, round clock, the only ledger, no model credential). Every server, the first included, runs one model worker (`src/worker.py serve`). Workers and coordinator talk only through the experiment hub.
- One exclusive claim `claims/dmarz-sybil-rules-180.yml` in the fleet repository with `servers` listing exactly the three servers, `experiment: sybil-rules-180`, `by: dmarz/<agent>`, `status: running`, an `until` covering the chain (at least 10 hours) and no `shared`. No other active claim may name any of the three.

## Steps

From a checkout of the fleet repository at or after commit `18aed12`, with `SWARM_LAB_CHECKOUT` pointing at a swarm-lab clone and `<commit>` the 40-hex launch commit from the run request:

```sh
H=<coordinator>,<second>,<third>
python3 scripts/run-ready-chain.py sybil-rules-180 <commit> setup  --host $H     # checkout, venv, 60 selftests, source hash, on each server
python3 scripts/run-ready-chain.py sybil-rules-180 <commit> chain  --host $H --confirm-paid --source dmarz/<agent>
python3 scripts/run-ready-chain.py sybil-rules-180 <commit> status --host $H      # chain status, ledger, worker processes, log tails
python3 scripts/run-ready-chain.py sybil-rules-180 <commit> verify --host $H      # after the chain ends: re-simulation and records check
```

`chain` starts the coordinator first (S0 runs offline, about 30 s, then P0 queues the three worker sessions and waits up to 30 minutes), then one worker per server with `SWARM_OPENROUTER_API_KEY` on ssh stdin, in memory only. The chain runs S0, P0, Q0, X0, S1 (warm-up, checkpoint, C, B, A, A'), D1 and stops by itself at a failed gate. Exit codes of `src/chain.py`: 0 completed, 3 stopped at a stage or gate (also when a continuation stopped under the void limits and the rest completed), 1 internal error.

## While it runs

- `status` shows the current stage, per-stage calls, voids, transport statistics (lost tasks, re-issued calls, dead slots) and the ledger.
- A worker that dies is replaced automatically by the other two for the rest of the chain; do not restart it by hand during a stage.
- Do not start anything else on the three servers.

## After it ends

`verify`, then the post-mortem `reviews/chain-001-post.md` per [RUN-REVIEW.md](../../../../tooling/agent-experiments/RUN-REVIEW.md), then release the claim after the uploads are verified. A billing stop (`provider_credit_balance_low`) ends the attempt; the pre-registered resume is attempt 002 from the stopped stage after a fresh check ([preregistration.md](preregistration.md)).

## Offline checks (no network, no model call)

```sh
python3 src/selftest.py
python3 src/worker.py --stage S0 --attempt <fresh name>                 # STUDY_RESULTS_DIR outside the repository
python3 src/rehearse.py --hub-dir <directory with hub.py and swarm_report.py>
```
