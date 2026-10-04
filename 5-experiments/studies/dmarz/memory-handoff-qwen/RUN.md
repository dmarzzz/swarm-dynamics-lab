# Runbook: memory-handoff-qwen, chain 003 (gpt-6-luna)

Attempt 001 (Qwen) stopped at the qualification gate and attempt 002 (Qwen) ran to completion on 2026-10-04 ([RESULTS.md](RESULTS.md)). Chain 003 has not been run. Operator: dmarz/fleet-monitor (`--source dmarz/fleet-monitor`). The server is a parameter. Public files contain no server address, hub address, token or credential.

## Before launch

1. The run request is in the private run queue, after dmarz/fleet-monitor's same-researcher check of this package. Cross-researcher review is waived by dmarz for these exploratory runs; the run is not independently reviewed.
2. Read [reviews/chain-003-pre.md](reviews/chain-003-pre.md). It names the code commit `c2717f74…` and the source hash `caf5d773…`. [READY.yaml](READY.yaml) carries the same hash, `provider: openai`, `model: gpt-6-luna`, the number of selftests (129), the call caps, `usd_cap: 5`, the chain timeout, `review: reviews/chain-003-pre.md` and `ledger: fresh`. The reviews of chains 001 and 002 are the records of the Qwen attempts and are not the review of this launch.
3. Launch with the commit named in the run request, written `<commit>` below: the first commit on main that contains the chain-003 review and has the same source hash. Do not launch an earlier commit of this study: `a5bd1a66` and `87d1fcb1` are work in progress.
4. Take the exclusive server claim `dmarz-memory-handoff-qwen` (`experiment: memory-handoff-qwen`) on a fresh server: a fresh ledger and a fresh results directory. The hub runs of attempts 001 and 002 stay on the hub; chain 003's batches are `s0-003`, `p0-003-gpt-6-luna`, `q0-003-gpt-6-luna`, `s1-003-gpt-6-luna`, and its gates look only at runs with the new source hash and this model.
5. The server checkout needs this directory. Python 3.12 with `requirements.txt`.
6. Credential alias on the server: `SWARM_OPENAI_API_KEY` (the launcher passes it in memory; only this provider's credential is sent). Someone with console access confirms that the OpenAI project has quota for about USD 1 and no hard limit below that.

## Commands

The generic private launcher, from the agentops repository. `--model` is not needed: `READY.yaml` names `gpt-6-luna` as the only model.

```
python3 scripts/run-ready-chain.py memory-handoff-qwen <commit> setup --host <server> --source dmarz/fleet-monitor
python3 scripts/run-ready-chain.py memory-handoff-qwen <commit> chain --host <server> --confirm-paid --source dmarz/fleet-monitor
python3 scripts/run-ready-chain.py memory-handoff-qwen <commit> status --host <server>
python3 scripts/run-ready-chain.py memory-handoff-qwen <commit> verify --host <server>
python3 scripts/run-ready-chain.py memory-handoff-qwen <commit> resume --host <server> --confirm-paid --source dmarz/fleet-monitor     # only after a billing stop of S1
```

- `setup` checks out `<commit>`, installs the pinned requirements, runs `python3 src/selftest.py` (129 tests, about 2 minutes on the build machine) and compares the number of tests and `study.source_hash()` with `READY.yaml`. The source hash on the server must be `caf5d773dec0e0c50e99d40088a63349b1f0e3380939c80495e1d00ab6fcc4ba`. The selftest ignores `STUDY_MODEL` and `STUDY_PROVIDER` in its environment.
- `chain` starts one detached process, `python src/chain.py run --stages S0,P0,Q0,S1`, with `STUDY_MODEL=gpt-6-luna`, `STUDY_PROVIDER=openai`, `SWARM_OPENAI_API_KEY`, `STUDY_BUDGET_LEDGER`, `STUDY_RESULTS_DIR` and `SWARM_SOURCE` in its environment and the hub client on `PYTHONPATH`. `--confirm-paid` is required because P0, Q0 and S1 make model calls: 1, 23 and 576.
- `status` prints `chain-status.json` and the ledger totals. `verify` checks artifact checksums against the hub, validates and regrades every saved answer, checks the journal's hash chain, regenerates every packet and recomputes the gates, the totals and the analysis. Both print one JSON object on the last line; neither needs the credential. Without `STUDY_MODEL` the code defaults to gpt-6-luna.
- `resume` runs `python src/chain.py resume`. It is allowed only when the chain's last state is S1 stopped with `provider_billing_stopped` (the OpenAI adapter's billing-stop category) at the same source hash and model. It queues the continuation batch `s1-003-gpt-6-luna-r1` with exactly the not-started assignments, under the same ledger. After any other stop it prints `resume_refused` and exits 3.

## What the chain does by itself

| Stage | Calls | Gate to pass | If it fails |
|---|---|---|---|
| S0 (`s0-003`) | 0 | 192 scripted rows valid, both qualification sets pass under the reference actor, 25 invariants hold | chain stops; nothing paid has happened |
| P0 (`p0-003-gpt-6-luna`) | 1 (fixture `qa00-r5501-clean-content`) | response parses, model is `gpt-6-luna` or its dated form, usage reported, finish reason `stop`, valid answer (one JSON object with `value` and `sources`) | chain stops after one call; the response metadata is in the P0 summary and on the hub |
| Q0 (`q0-003-gpt-6-luna`) | 23 | all 24 qualification rows (P0's saved row plus these 23) valid and in exact agreement with the reference; they are the 24 messages Qwen answered in attempt 001 | chain stops with `qualification_failed`; S1 is never queued; this chain has no repair |
| S1 (`s1-003-gpt-6-luna`) | 576 | before queueing: 576 × measured cost per call fits under the remaining cap; largest measured tokens per byte × largest S1 request (4,972 bytes) is at most 8,000 tokens | chain stops with `projection_exceeds_cap` or `input_ceiling_projection` before any S1 call |

Exit code 0: all requested stages done. Exit code 3: stopped at a failed stage or a refused gate; `chain-status.json` has `state: stopped_at_gate`, the stage and the reason. Any other non-zero code: internal error.

A stop at Q0 is a result: it is reported with the message and answer of every miss and nothing is retuned. An answer cut off at the 1,500-token limit (reasoning plus visible answer) is a failed call, `truncated_output`; in P0 or Q0 that fails the stage.

In S1 a call without a valid answer is recorded as failed, with the HTTP status and response body when there was one, and dispatch continues; the seventh failed call stops dispatch (`failed_units_over_limit`), as does any integrity failure (`integrity_failure:<category>`). A request rejected with HTTP 429 (rate limit), 500, 502, 503 or 504 is re-sent at most twice inside its 120 s budget. A billing or quota refusal pauses the stage and re-sends the same call every 60 s for up to 20 minutes; the hub shows the pause. If it outlasts 20 minutes, S1 stops with `provider_billing_stopped` and can be resumed.

Limits in the hashed design: 4 requests in flight; 120 s per request; 6,000 s per stage; 7,800 s for the chain; 600 calls; 800 transport attempts; USD 5 of settled cost plus open reservations. Expected: about USD 0.16 (worst realistic USD 0.82) and 5 to 15 minutes.

## After the chain

1. `status`, then `verify`. Keep both outputs. Deliver the results directories (without images) as for attempt 002.
2. Do not rerun a stage. A batch name is refused the second time.
3. Post-mortem per [RUN-REVIEW.md](../../../../tooling/agent-experiments/RUN-REVIEW.md); RESULTS.md gets a gpt-6-luna section beside the Qwen results, never pooled.
4. Confirm the chain process has exited and uploads are verified, then release the claim. Do not destroy the server.

## Offline checks (no server, no model call)

```
python3 src/selftest.py
python3 src/worker.py --stage S0 --attempt <fresh-name>
python3 src/manifest.py --check
python3 src/rehearse.py --hub-dir <directory with hub.py and swarm_report.py>
```

Set `STUDY_RESULTS_DIR` to keep outputs outside the checkout; the default `results/` is git-ignored.
