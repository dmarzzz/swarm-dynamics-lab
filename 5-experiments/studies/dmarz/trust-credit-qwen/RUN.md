# Runbook: trust-credit-qwen, chain 001 (program v5, line T)

Nothing here has been run. This file is for the operator who takes the request from the private run queue. The server is a parameter. Public files contain no server address, hub address, token or credential.

## Before launch

1. The run request is in the private run queue and dmarz/fleet-monitor has done its same-researcher check of this package. Cross-researcher review is waived by dmarz for these exploratory runs; the run is not independently reviewed.
2. Read [reviews/chain-001-pre.md](reviews/chain-001-pre.md). It names the code commit and the source hash. The launch commit is the commit named in the run request: the first commit on `main` that contains that review and has that source hash. The launcher reads `READY.yaml`, `README.md` and the review at the commit it is given and refuses a commit without the review; its setup step verifies the source hash on the server.
3. Take the exclusive server claim `dmarz-trust-credit-qwen` (`experiment: trust-credit-qwen`).
4. The server needs this directory at the launch commit and Python 3.12 with `requirements.txt`. Nothing outside this directory is required (one selftest compares with `../sybil-budget-api/src/sim.py` when that file is present and is skipped otherwise; frozen digests cover the same code).
5. Model credential alias on the server: `SWARM_OPENROUTER_API_KEY`, passed in memory by the launcher.

## Commands

The generic private launcher, from the agentops repository (the operator also passes `--source <its agent id>`):

```
python3 scripts/run-ready-chain.py trust-credit-qwen <launch commit> setup --host <server>
python3 scripts/run-ready-chain.py trust-credit-qwen <launch commit> chain --host <server> --confirm-paid
python3 scripts/run-ready-chain.py trust-credit-qwen <launch commit> status --host <server>
python3 scripts/run-ready-chain.py trust-credit-qwen <launch commit> verify --host <server>
```

- `setup` checks out the launch commit, installs the pinned requirements, runs `python3 src/selftest.py` (73 tests, about 40 seconds on a laptop) and compares the number of tests and `study.source_hash()` with `READY.yaml`.
- `chain` starts one detached process, `python src/chain.py run --stages S0,P0,Q0,S1`, with `SWARM_OPENROUTER_API_KEY`, `STUDY_BUDGET_LEDGER`, `STUDY_RESULTS_DIR` and `SWARM_SOURCE` in its environment and the hub client on `PYTHONPATH`. `--confirm-paid` is required because P0, Q0 and S1 make model calls: 1, 23 and 504.
- P0's summary (`probe`), hub metrics (`probe_*`) and run message carry the probe call's raw response metadata: response model, provider, response id, finish reason, reasoning tokens, latency, provider-reported cost, input and output tokens, tokens per byte. Read them before anything else if P0 fails.
- `status` prints `chain-status.json` and the ledger totals. `verify` checks artifact checksums against the hub, regrades every saved row and recomputes totals, gates, stage outcomes and the analysis; it exits non-zero when a check fails. `python src/chain.py summarize` prints the S1 headline (primary contrast, counts, model-outcome bounds). Each prints one JSON object on the last line; none needs the model credential.

## What the chain does by itself

| Stage | Calls | Passes when | If it does not |
|---|---|---|---|
| S0 | 0 | 216 scripted rows valid; invariants hold on the 8 engineering roots and all 48 fixtures; both fixture sets pass under the reference policy; the propagated rule reproduces the earlier direction | chain stops; nothing paid has happened |
| P0 | 1 | the first qualification fixture: response parses, model slug matches, the provider is named and is Alibaba, usage reported, finish reason `stop`, no reasoning tokens, valid structure | chain stops after one call |
| Q0 | 23 | before queueing: P0's measured tokens per byte × the largest Q0 request ≤ 8,000 tokens, and P0's saved row is found and agrees with the hub; then over all 24 fixtures: every structure valid, ≥ 7 of 8 exactly right in `full` and in `sparse`, null on the withheld fact in 8 of 8 `missing` | `input_ceiling_projection`, `p0_row_missing`, or `gate_failed`; S1 is never queued |
| S1 | 504 | before queueing: largest measured tokens per byte × the largest S1 request ≤ 8,000 tokens (`input_ceiling_projection`), and 504 × Q0's cost per call fits under the cap (`projection_exceeds_cap`); then at most 6 failed calls and no integrity failure | S1 ends `failed` with the reason; rows preserved |

Exit code 0: all requested stages done. Exit code 3: stopped at a failed stage or a refused gate; `chain-status.json` has `state: stopped_at_gate`, the stage and the reason. Any other non-zero code: internal error. `--stages` accepts any ordered contiguous sub-list.

Failure handling in S1: a failed call (transport failure after the retry rule, timeout, refusal, invalid JSON, invalid answer, missing usage) is recorded with its HTTP status, response body and request id, and dispatch continues; it stops when more than 6 calls have failed. A ledger refusal, a model or provider mismatch, a breached reservation or a deadline stops dispatch at once. S0, P0 and Q0 stop at the first failed call.

Billing outage: on HTTP 402, or a 400/403/429 whose body names credit, balance, billing, a usage or spend limit, an exceeded limit or insufficient funds, the stage pauses and the same call is re-sent every 60 s for up to 20 minutes. If the outage outlasts that, the stage stops with `provider_credit_balance_low`: nothing is counted as failed and the unfinished calls are recorded as not started. After credit is restored, and only then:

```
python src/chain.py resume
```

(on the server, same environment; the launcher's `resume` action runs it). It queues batch `s1-001-r1` with exactly the calls not started, under the same ledger and the unchanged S1 cap of 504 (the reservations of the unanswered calls were voided). Record the resume as a dated amendment in this folder. `verify` and `summarize` read the original run and its continuations together.

Limits in the hashed design: 4 requests in flight; 120 s per request; 3,600 s per stage; 7,200 s for the chain; 528 calls in this attempt (the ledger's study cap of 552 includes the 24 of the one repair attempt); 640 transport attempts; USD 2 of settled cost plus open reservations, each reservation 10 times the snapshot-price bound (about USD 0.003); every request at most 7,600 bytes. Expected: about USD 0.05 and 5 to 15 minutes for S1.

## If qualification fails

Read every failing answer first (the rows keep `answer` or `accounting.answer_text`). The program allows one bounded repair: a new attempt with `attempt: '002'` in `design.yaml` (new source hash, batches `…-002`, the second fixture set on roots 4650-4657, which is frozen in the manifest as `qualification_b`), and its own pre-run review. Per-stage call caps are counted per batch family, so `p0-002` and `q0-002` have their own allowance in the same ledger file; `max_attempted_calls` (552) already includes those 24 calls. Thresholds are not lowered. A failed repeat ends the line.

## After the chain

1. `status`, `verify`, `summarize`. Keep the outputs.
2. Do not rerun a stage. A batch name is refused the second time.
3. Write the post-mortem per [RUN-REVIEW.md](../../../../tooling/agent-experiments/RUN-REVIEW.md): reconcile assigned, started, terminal, graded and analyzed rows; compare the frames with `analysis.json`; report actual calls, transport attempts, tokens, dollars, failed calls with their evidence, and any billing pause.
4. Update the evidence registry row and the README's results section from the saved analysis.
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

## Attempt 002 (gpt-6-luna), added 2026-10-04

Same commands; the launch commit is the first commit on `main` with [reviews/chain-002-pre.md](reviews/chain-002-pre.md) and source hash `5155d2c6…`. `READY.yaml` names `provider: openai`, `model: gpt-6-luna`, `review: reviews/chain-002-pre.md` and `ledger: fresh`, so the launcher sends `SWARM_OPENAI_API_KEY` only and starts this attempt's own ledger. Do not pass `--model`. `setup` runs 71 selftests. Batches `s0-002`, `p0-002`, `q0-002`, `s1-002`; a billing stop is `provider_billing_stopped` and is resumed with the launcher's `resume` action.
