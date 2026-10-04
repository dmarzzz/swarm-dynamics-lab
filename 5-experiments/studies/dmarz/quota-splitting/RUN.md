# Runbook: quota-splitting, chain 001

Nothing here has been run. This file is for the operator who takes the request from the private run queue. The server is a parameter. Public files contain no server address, hub address, token or credential.

## Before launch

1. The run request is in the private run queue and dmarz/fleet-monitor has done its same-researcher check of this package. Cross-researcher review is waived by dmarz for these exploratory runs (relayed by dmarz/pipeline and dmarz/fleet-monitor, 2026-10-04). The run is not independently reviewed.
2. Read [reviews/chain-001-pre.md](reviews/chain-001-pre.md). It names the code commit and the source hash. The launch commit is the commit named in the run request: the first commit on `main` that contains that review and has that source hash. The launcher reads `READY.yaml`, `README.md` and the review at the commit it is given and refuses a commit without the review; its setup step verifies the source hash on the server. [READY.yaml](READY.yaml) carries the same hash, the number of selftests, the call caps, the dollar cap and the chain timeout.
3. Take the exclusive server claim `dmarz-quota-splitting` (`experiment: quota-splitting`).
4. The server needs this directory at the launch commit and Python 3.12 with `requirements.txt`. Nothing outside this directory is required.
5. Load: the chain keeps at most 8 requests in flight (one per episode in flight). At an assumed 6 to 15 s per call that is 32 to 80 message requests per minute and as many token-counting requests, about 40,000 to 110,000 input tokens per minute (about 1,000 to 1,400 per request) and 20,000 to 70,000 output tokens per minute. The workspace is shared with other dmarz runs. `workers: 8` is in the hashed design; running with fewer in flight is a design change with a new source hash, so that decision has to be made before the chain is queued.

## Commands

The generic private launcher, from the agentops repository:

```
python3 scripts/run-ready-chain.py quota-splitting <launch commit> setup --host <server>
python3 scripts/run-ready-chain.py quota-splitting <launch commit> chain --host <server> --confirm-paid --source <operator agent id>
python3 scripts/run-ready-chain.py quota-splitting <launch commit> status --host <server>
python3 scripts/run-ready-chain.py quota-splitting <launch commit> verify --host <server>
```

- The operator passes `--source <its agent id>` to the `chain` action (launcher note from its first real use, 2026-10-04).
- `setup` checks out `<launch commit>`, installs the pinned requirements, runs `python3 src/selftest.py` (about 100 seconds on orbital-one (76 tests)) and compares the number of tests and `study.source_hash()` with `READY.yaml`. Allow about 5 minutes for `setup` on a server (launcher note from its first real use, 2026-10-04).
- `chain` starts one detached process, `python src/chain.py run --stages S0,P0,Q0,S1`, with `SWARM_MODEL_API_KEY`, `SWARM_MODEL_WORKSPACE_ID`, `STUDY_BUDGET_LEDGER`, `STUDY_RESULTS_DIR` and `SWARM_SOURCE` in its environment and the hub client on `PYTHONPATH`. `--confirm-paid` is required because P0, Q0 and S1 make model calls: 1, at most 96 and at most 3,456 answered (call cap 3,552). Without `--model` the chain runs on `claude-opus-5-5`.
- `status` prints `chain-status.json` and the ledger totals. `verify` checks artifact checksums against the hub, replays every episode from its saved answers through the engine and recomputes the totals, the gates and the analysis. Both print one JSON object on the last line; neither needs the model credential. `verify` exits non-zero when a check fails.
- The chain uses threads only. It installs no signal handler and starts no process pool.

## What the chain does by itself

| Stage | Calls | Passes when | If it does not |
|---|---|---|---|
| S0 | 0 | 193 scripted episodes valid; every invariant holds on the 2 engineering and 8 qualification roots; scripted qualification and probe pass; the three reference planners are separated on the engineering roots | chain stops; nothing paid has happened |
| P0 | 1 | answer parses, model id matches, usage reported, stop reason `end_turn`, at least one action and every action applied in full | chain stops after one call |
| Q0 | at most 96 | 16 episodes valid; ≥ 95% of turns clean; ≥ 14 of 16 episodes successful; at most 4 of the 8 `N` episodes at the limit of 6 subagents | chain stops; S1 is never queued |
| S1 | at most 3,456 answered (cap 3,552) | before queueing: Q0's cost per call × 1.25 × 3,552 fits in what is left under the dollar cap, and no Q0 call used more than 6,000 output tokens (75% of the limit); then done when no integrity failure occurred and at most 6 episodes failed | `projection_exceeds_cap` or `output_room_too_small` before any S1 call; `failed_units_over_limit` when a seventh episode fails; an integrity failure stops dispatch at once; `provider_credit_balance_low` after a 20-minute billing pause (resumable) |

Exit code 0: all requested stages done. Exit code 3: stopped at a failed stage or a refused gate; `chain-status.json` has `state: stopped_at_gate`, the stage and the reason. Any other non-zero code: internal error (also recorded in `chain-status.json`). No answer is retried and no agent is needed between stages. A request rejected with HTTP 429 or 529 is re-sent at most twice inside its 240 s budget.

An episode is a sequence of up to 6 calls; each call's input is built from the answers before it. A failed call ends its episode as failed and keeps its HTTP status, body (first 2,000 characters) and request id. In S0, P0 and Q0 the first failed call stops the stage. In S1 dispatch continues until more than 6 episodes have failed (`budget.max_failed`); an integrity failure (ledger refusal, reservation breach, model mismatch, source or batch mismatch, deadline) stops it at once. When dispatch stops, calls in flight finish, episodes cut short are recorded as `interrupted` and episodes never started as `not_started`. A failed token-counting request is re-sent once and then replaced by a byte-count reservation. A credit-balance error pauses the whole stage and re-sends the same call every 60 s for up to 20 minutes; nothing is recorded as a model outcome meanwhile. `turns.jsonl.gz` has one line per call, `episodes.jsonl.gz` one line per episode.

`--stages` accepts any ordered contiguous sub-list (`--stages S0`, later `--stages P0,Q0,S1`); the gates still decide whether a stage may start.

Limits in the hashed design: 8 requests in flight; 240 s per request; 21,600 s per stage; 28,800 s for the chain; 3,649 calls (P0 1, Q0 96, S1 3,552); 4,014 transport attempts; USD 270 of settled cost plus open reservations per model attempt. Expected: USD 45 to 90 on `claude-opus-5-5` (USD 56 to 113 on `claude-opus-5`, prices × 1.25) and about 40 to 110 minutes for S1, a few minutes for the rest.

## Resume after a billing stop

Only when S1 stopped with reason `provider_credit_balance_low` (`status` shows it), and only once the credit problem is fixed:

```
python3 scripts/run-ready-chain.py quota-splitting <launch commit> resume --host <server> --confirm-paid --source <operator agent id>
```

It runs `python src/chain.py resume`, which queues continuation batch `s1-001-r1` holding exactly the unfinished episodes, at the same source hash, under the same ledger and caps. It refuses after any other kind of stop. Note it on the run request as a dated amendment.

## Second model of the ladder

Only after a stage was refused on a limit or credit error that did not clear in 20 minutes (a `provider_credit_balance_low` stop, or repeated HTTP 429 past the retry rule), as a dated amendment noted on the run request:

```
python3 scripts/run-ready-chain.py quota-splitting <launch commit> chain --host <server> --confirm-paid --model claude-opus-5 --stages P0,Q0,S1 --source <operator agent id>
```

S0 already passed at this source hash and serves both models. `--model claude-opus-5` sets `STUDY_MODEL` and points `STUDY_BUDGET_LEDGER` at `accounting/ledger-opus-5.jsonl` and `STUDY_RESULTS_DIR` at `results-opus-5`. The second model gets its own probe and qualification (`p0-001-opus-5`, `q0-001-opus-5`, `s1-001-opus-5`); the coordinator refuses a Q0 or S1 behind a stage of the other model. Its results are reported separately and never pooled with the first model's rows.

## After the chain

1. `status`, then `verify`. Keep both outputs.
2. Do not rerun a stage. A batch name is refused the second time, and a stage is refused while any run of this experiment is still planned, assigned or running on the hub. A repair is a new attempt with a changed design (new batch number, fresh qualification roots), which changes the source hash, and needs its own pre-run review.
3. If Q0 failed: before anything else read the input and the returned text of every unsuccessful episode and every unclean turn (`turns.jsonl.gz` has the answers and what happened to each action) and say which stated rule each one ran against. The near-miss rule is item 8 of the pre-registration.
4. Write the post-mortem per [RUN-REVIEW.md](../../../toolkit/agent-experiments/RUN-REVIEW.md): reconcile assigned, started, terminal, graded and analyzed episodes and calls; compare the frames with the saved analysis; report actual calls, transport attempts, tokens and dollars; report the spread of the three `N` episodes per root; read a sample of spawn rationales, since the keyword count is not a classifier.
5. Update the evidence registry row and the README's results section from the saved analysis. A failed or incomplete S1 is diagnostic, not a result.
6. Confirm the chain process has exited and uploads are verified, then release the claim. Do not destroy the server.

## Offline checks (no server, no model call)

```
python3 src/selftest.py
python3 src/worker.py --stage S0 --attempt <fresh-name>
python3 src/manifest.py --check
python3 src/rehearse.py --hub-dir <directory with hub.py and swarm_report.py>
python3 src/analyze.py calibration
```

Set `STUDY_RESULTS_DIR` to keep outputs outside the checkout; the default `results/` is git-ignored. The rehearsal uses its own temporary directories, a throwaway hub on 127.0.0.1 and an in-process stub in place of the model endpoint; it refuses any hub address that is not 127.0.0.1.
