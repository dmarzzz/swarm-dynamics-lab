# Runbook: verify-cost-qwen, chain 001

Nothing here has been run. This file is for the operator who takes the request from the private run queue. The server is a parameter. Public files contain no server address, hub address, token or credential.

## Before launch

1. The run request is in the private run queue and dmarz/fleet-monitor has done its same-researcher check of this package. Cross-researcher review is waived by dmarz for these exploratory runs; the run is not independently reviewed.
2. Read [reviews/chain-001-pre.md](reviews/chain-001-pre.md). It names the code commit and the source hash. [READY.yaml](READY.yaml) carries the same hash, the number of selftests (84), the call caps, the dollar cap and the chain timeout, and `provider: openrouter`, `model: qwen/qwen3.7-flash`.
3. Launch with the commit named in the run request, written `<commit>` below: the first commit on main that contains the pre-run review and has the same source hash. Do not launch with the code commit, which has no review.
4. Take the exclusive server claim `dmarz-verify-cost-qwen` (`experiment: verify-cost-qwen`). One server for this line.
5. The server needs this directory, Python 3.12 with `requirements.txt`, the hub client on `PYTHONPATH`, and the credential alias `SWARM_OPENROUTER_API_KEY` in the chain's environment (passed in memory by the launcher; never written to a file, an argument or a log).

## Commands

The generic private launcher, from the agentops repository:

```
python3 scripts/run-ready-chain.py verify-cost-qwen <commit> setup --host <server>
python3 scripts/run-ready-chain.py verify-cost-qwen <commit> chain --host <server> --confirm-paid
python3 scripts/run-ready-chain.py verify-cost-qwen <commit> status --host <server>
python3 scripts/run-ready-chain.py verify-cost-qwen <commit> verify --host <server>
python3 scripts/run-ready-chain.py verify-cost-qwen <commit> resume --host <server>     # only after a billing stop of S1
```

- `setup` checks out `<commit>`, installs the pinned requirements, runs `python3 src/selftest.py` and compares the number of tests and `study.source_hash()` with `READY.yaml`. The source hash on the server must be `72895482b6765d17e60e17af80249c94ef70fca0f544f6f1c49d12c573d68b4f`.
- `chain` starts one detached process, `python src/chain.py run --stages S0,P0,Q0,S1`, with `SWARM_OPENROUTER_API_KEY`, `STUDY_BUDGET_LEDGER`, `STUDY_RESULTS_DIR` and `SWARM_SOURCE` in its environment. `--confirm-paid` is required because P0, Q0 and S1 make model calls: 1, 23 and 576.
- `status` prints `chain-status.json` and the ledger totals. `verify` checks artifact checksums against the hub, regenerates every request, regrades every saved answer and recomputes the gates, the summary totals and the analysis. Both print one JSON object on the last line; neither needs the model credential.
- `resume` runs `python src/chain.py resume`. It is refused unless the chain's last state is S1 stopped with `provider_credit_balance_low` at this source hash. It queues `s1-001-r1` with exactly the units left not started, under the same ledger and inside the same S1 cap.

## What the chain does by itself

| Stage | Calls | Gate to pass | If it fails |
|---|---|---|---|
| S0 | 0 | 144 scripted rows valid; the analytic policy passes both qualification sets; every invariant holds (both actions legal, equal information, only e and U change within a layout, no leak, optimum changes across the twelve cases, constant policies fail qualification) | chain stops; nothing paid has happened |
| P0 | 1 | the response parses, model slug and provider (Alibaba, named in the response) match, usage reported, finish reason `stop`, no reasoning tokens, valid answer | chain stops after one call |
| Q0 | 23 | over P0's row and these 23: 24 valid, at least 11 of 12 optimal in each representation | chain stops with `gate_failed`; S1 is never queued; read `failures.json` (every miss with its request and answer) before anything else |
| S1 | 576 | before queueing: 576 × Q0's mean cost per call must fit in the remaining dollar cap (`projection_exceeds_cap`); P0's tokens per byte × the largest S1 request must not exceed 8,000 tokens (`input_ceiling_projection`) | chain stops before any S1 call |

Exit code 0: all requested stages done. Exit code 3: stopped at a failed stage or a refused gate; `chain-status.json` has `state: stopped_at_gate`, the stage and the reason. Any other non-zero code: internal error. No answer is ever retried and no agent is needed between stages.

In S1 a call without a valid answer is recorded as failed and dispatch continues; S1 ends `done` with up to 6 failed calls and `failed` (reason `failed_units_over_limit`) at the seventh. An integrity failure (ledger refusal, reservation breach, model or provider mismatch, deadline) stops dispatch at once. A request refused with HTTP 429, 502, 503 or 529 is re-sent at most twice inside its 120 s budget. A billing or limit refusal pauses the stage and re-sends the same call every 60 s for up to 20 minutes; then the stage stops with `provider_credit_balance_low`, nothing is recorded as failed, and S1 can be resumed. A billing stop in P0 or Q0 cannot be resumed: it needs a new attempt.

Limits in the hashed design: 4 requests in flight; 120 s per request; 5,400 s per stage; 7,200 s for the chain; 600 calls for this attempt (ledger study cap 624); 784 transport attempts; USD 2 of settled cost plus open reservations. Expected: about USD 0.01 to 0.03 and about 5 to 15 minutes.

## After the chain

1. `status`, then `verify`. Keep both outputs.
2. Do not rerun a stage. A batch name is refused the second time. After a failed qualification, the one permitted repair is attempt 002: read the failing answers, set `attempt: '002'` and `qualification.set: b` in `design.yaml` (new source hash), regenerate the manifest, write `reviews/chain-002-pre.md`. A failed repeat ends the line. Thresholds are never lowered.
3. Write the post-mortem per [RUN-REVIEW.md](../../../../tooling/agent-experiments/RUN-REVIEW.md): reconcile assigned, started, terminal, graded and analyzed rows; compare the frames with the saved analysis; report actual calls, tokens and dollars; report P0's raw response metadata (`summary.json` `probe`).
4. Confirm the chain process has exited and uploads are verified, then release the claim. Do not destroy the server.

## Offline checks (no server, no model call)

```
python3 src/selftest.py
python3 src/worker.py --stage S0 --attempt <fresh-name>
python3 src/manifest.py --check
python3 src/rehearse.py --hub-dir <directory with hub.py and swarm_report.py>
python3 src/analyze.py calibration
```

Set `STUDY_RESULTS_DIR` to keep outputs outside the checkout; the default `results/` is git-ignored.
