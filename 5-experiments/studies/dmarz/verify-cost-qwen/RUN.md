# Runbook: verify-cost-qwen, chain 003 (gpt-6-luna, the second pre-registered model)

Attempts 001 and 002 ran on `qwen/qwen3.7-flash` on 2026-10-04 and both stopped at the qualification gate ([chain-001-post.md](reviews/chain-001-post.md), [chain-002-post.md](reviews/chain-002-post.md)); the Qwen route of this line has ended. Chain 003 runs the original attempt-001 instrument on `gpt-6-luna` (OpenAI) and has not been run. Operator: dmarz/fleet-monitor (pass `--source dmarz/fleet-monitor` to the launcher). This file is for the operator who takes the request from the private run queue. The server is a parameter. Public files contain no server address, hub address, token or credential.

## Before launch

1. The run request is in the private run queue and dmarz/fleet-monitor has done its same-researcher check of this package. Cross-researcher review is waived by dmarz for these exploratory runs; the run is not independently reviewed.
2. Read [reviews/chain-003-pre.md](reviews/chain-003-pre.md) (named by `review:` in READY.yaml; the reviews of chains 001 and 002 are untouched records). It names the code commit and the source hash. [READY.yaml](READY.yaml) carries the same hash, the number of selftests (123), the call caps, the dollar cap and the chain timeout, and `provider: openai`, `model: gpt-6-luna`.
3. Launch with the commit named in the run request, written `<commit>` below: the first commit on main that contains the pre-run review and has the same source hash. Do not launch with the code commit, which has no review.
4. Take the exclusive server claim `dmarz-verify-cost-qwen` (`experiment: verify-cost-qwen`). One fresh server, with a fresh ledger and a fresh results directory (READY.yaml declares `ledger: fresh`): the ledger's study cap is 600 and assumes no earlier call in it. The hub keeps the runs of attempts 001 and 002; this chain's batches are `s0-002-gpt-6-luna`, `p0-002-gpt-6-luna`, `q0-002-gpt-6-luna`, `s1-002-gpt-6-luna`, and its gates look only at runs with its own model and source hash.
5. The server needs this directory, Python 3.12 with `requirements.txt`, the hub client on `PYTHONPATH`, `STUDY_MODEL=gpt-6-luna` (set by the launcher from READY.yaml `model:`) and the credential alias `SWARM_OPENAI_API_KEY` in the chain's environment (passed in memory by the launcher; never written to a file, an argument or a log).

## Commands

The generic private launcher, from the agentops repository:

```
python3 scripts/run-ready-chain.py verify-cost-qwen <commit> setup --host <server> --source dmarz/fleet-monitor
python3 scripts/run-ready-chain.py verify-cost-qwen <commit> chain --host <server> --confirm-paid --source dmarz/fleet-monitor
python3 scripts/run-ready-chain.py verify-cost-qwen <commit> status --host <server>
python3 scripts/run-ready-chain.py verify-cost-qwen <commit> verify --host <server>
python3 scripts/run-ready-chain.py verify-cost-qwen <commit> resume --host <server>     # only after a billing stop of S1
```

- `setup` checks out `<commit>`, installs the pinned requirements, runs `python3 src/selftest.py` and compares the number of tests and `study.source_hash()` with `READY.yaml`. The source hash on the server must be `b1b15d2573d295ee5560bdfbd3b2661b90c5a6cd435dd3a694ec3a9695dd5d48`.
- `chain` starts one detached process, `python src/chain.py run --stages S0,P0,Q0,S1`, with `SWARM_OPENAI_API_KEY`, `STUDY_MODEL`, `STUDY_PROVIDER`, `STUDY_BUDGET_LEDGER`, `STUDY_RESULTS_DIR` and `SWARM_SOURCE` in its environment. `--confirm-paid` is required because P0, Q0 and S1 make model calls: 1, 23 and 576.
- `status` prints `chain-status.json` and the ledger totals. `verify` checks artifact checksums against the hub, regenerates every request, regrades every saved answer and recomputes the gates, the summary totals and the analysis. Both print one JSON object on the last line; neither needs the model credential.
- `resume` runs `python src/chain.py resume`. It is refused unless the chain's last state is S1 stopped with `provider_billing_stopped` (the OpenAI adapter's billing-stop category) at this source hash and model. It queues `s1-002-gpt-6-luna-r1` with exactly the units left not started, under the same ledger and inside the same S1 cap.

## What the chain does by itself

| Stage | Calls | Gate to pass | If it fails |
|---|---|---|---|
| S0 | 0 | 144 scripted rows valid; the analytic policy passes both qualification sets; every invariant holds (both actions legal, equal information, only e and U change within a layout, no leak, optimum changes across the twelve cases, constant policies fail qualification) | chain stops; nothing paid has happened |
| P0 | 1 (`qa-2800-e90-u05-prose`, the probe request of attempt 001) | the response parses, the response model is `gpt-6-luna` or its dated form, usage reported, finish reason `stop`, output within 1,500 tokens, valid answer `{"inspect": "<cell>"}` | chain stops after one call |
| Q0 | 23 (set a: the requests Qwen answered in attempt 001) | over P0's row and these 23: 24 valid, at least 11 of 12 optimal in each representation | chain stops with `gate_failed`; S1 is never queued; **this chain ends: there is no repair attempt for it**. `failures.json` holds every miss with its request and answer |
| S1 | 576 | before queueing: 576 × Q0's mean cost per call must fit in the remaining dollar cap (`projection_exceeds_cap`); P0's tokens per byte × the largest S1 request must not exceed 8,000 tokens (`input_ceiling_projection`) | chain stops before any S1 call |

Exit code 0: all requested stages done. Exit code 3: stopped at a failed stage or a refused gate; `chain-status.json` has `state: stopped_at_gate`, the stage and the reason. Any other non-zero code: internal error. No answer is ever retried and no agent is needed between stages.

In S1 a call without a valid answer is recorded as failed and dispatch continues; S1 ends `done` with up to 6 failed calls and `failed` (reason `failed_units_over_limit`) at the seventh. An integrity failure (ledger refusal, reservation breach, model or provider mismatch, deadline) stops dispatch at once. A request refused with HTTP 429 (rate limit), 500, 502, 503 or 504 is re-sent at most twice inside its 120 s budget. A billing or limit refusal pauses the stage and re-sends the same call every 60 s for up to 20 minutes; then the stage stops with `provider_billing_stopped`, nothing is recorded as failed, and S1 can be resumed. A billing stop in P0 or Q0 cannot be resumed: it needs a new attempt.

Limits in the hashed design: 4 requests in flight; 120 s per request; 5,400 s per stage; 7,200 s for the chain; 600 calls (ledger study cap 600); 760 transport attempts; USD 5 of settled cost plus open reservations; `reasoning_effort: low`; `max_completion_tokens: 1500`. Expected: about USD 0.06 to 0.16 (worst realistic USD 0.49) and about 3 to 14 minutes.

## After the chain

1. `status`, then `verify`. Keep both outputs.
2. Do not rerun a stage. A batch name is refused the second time. There is no repair attempt for this chain: if its qualification fails, that is reported as the result for `gpt-6-luna`. Thresholds are never lowered. Attempt 001, attempt 002 and chain 003 are three separate records and are never pooled.
3. Write the post-mortem per [RUN-REVIEW.md](../../../../tooling/agent-experiments/RUN-REVIEW.md): reconcile assigned, started, terminal, graded and analyzed rows; compare the frames with the saved analysis; report actual calls, tokens and dollars; report P0's raw response metadata (`summary.json` `probe`) and, next to this chain's qualification table, Qwen's attempt-001 answers to the same 24 requests (descriptive, never pooled).
4. Confirm the chain process has exited and uploads are verified, then release the claim. Do not destroy the server.

## Offline checks (no server, no model call)

```
python3 src/selftest.py
STUDY_MODEL=gpt-6-luna python3 src/worker.py --stage S0 --attempt <fresh-name>
python3 src/manifest.py --check
python3 src/rehearse.py --hub-dir <directory with hub.py and swarm_report.py>
python3 src/analyze.py calibration
```

Set `STUDY_RESULTS_DIR` to keep outputs outside the checkout; the default `results/` is git-ignored.
