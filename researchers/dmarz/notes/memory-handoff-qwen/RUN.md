# Runbook: memory-handoff-qwen, chain 001

Nothing here has been run. This file is for the operator who takes the request from the private run queue. The server is a parameter. Public files contain no server address, hub address, token or credential.

## Before launch

1. The run request is in the private run queue, after dmarz/fleet-monitor's same-researcher check of this package. Cross-researcher review is waived by dmarz for these exploratory runs (relayed by dmarz/fleet-monitor, 2026-10-04); the run is not independently reviewed.
2. Read [reviews/chain-001-pre.md](reviews/chain-001-pre.md). It names the code commit `b6990122…` and the source hash `b4ab9025…`. [READY.yaml](READY.yaml) carries the same hash, the number of selftests (85), the call caps, the dollar cap and the chain timeout. `effort: low` is in that file only because the launcher requires the field: reasoning is disabled on this route and effort does not apply.
3. Launch with the commit named in the run request, written `<commit>` below: the first commit on main that contains the pre-run review and has the same source hash. Do not launch with the code commit: the launcher reads `READY.yaml`, `README.md` and the review at the commit it is given.
4. Take the exclusive server claim `dmarz-memory-handoff-qwen` (`experiment: memory-handoff-qwen`). One server for this line; its own ledger.
5. The server checkout needs this directory. Python 3.12 with `requirements.txt`. The selftest also compares the copied files with `researchers/dmarz/notes/discussion-dose/src/bench_v3/` and `researchers/dmarz/notes/pipeline/reference/` when those are in the checkout; without them it checks recorded hashes instead and the number of tests is the same.
6. Credential alias on the server: `SWARM_OPENROUTER_API_KEY` (the launcher passes it in memory). Someone with console access confirms that the OpenRouter balance covers USD 2.

## Commands

The generic private launcher, from the agentops repository:

```
python3 scripts/run-ready-chain.py memory-handoff-qwen <commit> setup --host <server>
python3 scripts/run-ready-chain.py memory-handoff-qwen <commit> chain --host <server> --confirm-paid
python3 scripts/run-ready-chain.py memory-handoff-qwen <commit> status --host <server>
python3 scripts/run-ready-chain.py memory-handoff-qwen <commit> verify --host <server>
python3 scripts/run-ready-chain.py memory-handoff-qwen <commit> resume --host <server>     # only after a billing stop of S1
```

- `setup` checks out `<commit>`, installs the pinned requirements, runs `python3 src/selftest.py` (85 tests, about 90 s on the build machine) and compares the number of tests and `study.source_hash()` with `READY.yaml`. The source hash on the server must be `b4ab9025e2288c7c7f652e7d210371ab7818022acc1ee155801e4300b5044ba3`.
- `chain` starts one detached process, `python src/chain.py run --stages S0,P0,Q0,S1`, with `SWARM_OPENROUTER_API_KEY`, `STUDY_BUDGET_LEDGER`, `STUDY_RESULTS_DIR` and `SWARM_SOURCE` in its environment and the hub client on `PYTHONPATH`. `--confirm-paid` is required because P0, Q0 and S1 make model calls: 1, 23 and 576.
- `status` prints `chain-status.json` and the ledger totals. `verify` checks artifact checksums against the hub, regrades every saved answer, checks the journal's hash chain, regenerates every packet and recomputes the gates, the summary totals and the analysis. Both print one JSON object on the last line; neither needs the model credential.
- `resume` runs `python src/chain.py resume`. It is allowed only when the chain's last state is S1 stopped with `provider_credit_balance_low` at the same source hash. It queues the continuation batch `s1-001-r1` with exactly the not-started assignments, under the same ledger. After any other stop it prints `resume_refused` and exits 3.

## What the chain does by itself

| Stage | Calls | Gate to pass | If it fails |
|---|---|---|---|
| S0 | 0 | 192 scripted rows valid, both qualification sets pass under the reference actor, 25 invariants hold | chain stops; nothing paid has happened |
| P0 | 1 | response parses, model slug matches, provider named and Alibaba, usage reported, finish reason `stop`, no reasoning tokens, valid answer structure | chain stops after one call; the response metadata is in the P0 summary and on the hub |
| Q0 | 23 | all 24 qualification rows (P0's saved row plus these 23) valid and in exact agreement with the reference | chain stops with `qualification_failed`; S1 is never queued |
| S1 | 576 | before queueing: 576 × measured cost per call fits under the remaining cap; largest measured tokens per byte × largest S1 request (5,064 bytes) is at most 8,000 tokens | chain stops with `projection_exceeds_cap` or `input_ceiling_projection` before any S1 call |

Exit code 0: all requested stages done. Exit code 3: stopped at a failed stage or a refused gate; `chain-status.json` has `state: stopped_at_gate`, the stage and the reason. Any other non-zero code: internal error.

Q0 is the most likely place for this chain to stop: the program's gate allows no miss in 24. A stop there is reported, not retuned. Read every failing answer first (`episodes.jsonl.gz` of the Q0 run has the answers; `assignments.jsonl.gz` has the messages; `replay.html` shows both side by side). The one permitted repair is attempt 002 on the second fixture set, with a new source hash and its own pre-run review; a failed repeat ends the line.

In S1 a call without a valid answer is recorded as failed, with the HTTP status and response body when there was one, and dispatch continues; the seventh failed call stops dispatch (`failed_units_over_limit`), as does any integrity failure (`integrity_failure:<category>`). A request rejected with HTTP 429, 502, 503 or 529 is re-sent at most twice inside its 120 s budget. A billing or limit refusal pauses the stage and re-sends the same call every 60 s for up to 20 minutes; the hub shows the pause. If it outlasts 20 minutes, S1 stops with `provider_credit_balance_low` and can be resumed.

Limits in the hashed design: 4 requests in flight; 120 s per request; 6,000 s per stage; 7,800 s for the chain; 600 calls for this attempt; 800 transport attempts; USD 2 of settled cost plus open reservations. Expected: about USD 0.03 and 5 to 15 minutes.

## After the chain

1. `status`, then `verify`. Keep both outputs.
2. Do not rerun a stage. A batch name is refused the second time.
3. Write the post-mortem per [RUN-REVIEW.md](../../../../tooling/agent-experiments/RUN-REVIEW.md): reconcile assigned, started, terminal, graded and analyzed rows; compare the frames with the saved analysis; report actual calls, tokens and dollars; for a failed qualification include the message and the returned answer of every miss.
4. Confirm the chain process has exited and uploads are verified, then release the claim. Do not destroy the server.

## Offline checks (no server, no model call)

```
python3 src/selftest.py
python3 src/worker.py --stage S0 --attempt <fresh-name>
python3 src/manifest.py --check
python3 src/rehearse.py --hub-dir <directory with hub.py and swarm_report.py>
```

Set `STUDY_RESULTS_DIR` to keep outputs outside the checkout; the default `results/` is git-ignored.
