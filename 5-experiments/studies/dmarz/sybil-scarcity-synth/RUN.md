# Runbook: sybil-scarcity-synth, chain 001

Nothing here has been run. This file is for the operator who takes the request from the private run queue. The server is a parameter. Public files contain no server address, hub address, token or credential.

## Before launch

1. The run request is in the private run queue and dmarz/fleet-monitor has done its same-researcher check of this package. Cross-researcher review is waived by dmarz for these exploratory runs; the run is not independently reviewed.
2. Read [reviews/chain-001-pre.md](reviews/chain-001-pre.md). It names the code commit and the source hash. [READY.yaml](READY.yaml) carries the same hash, the number of selftests, the call caps, the dollar cap, the chain timeout and the model ladder.
3. Launch with the commit named in the run request, written `<launch commit>` below. It is the first commit on main that contains the pre-run review and has the same source hash. Do not launch with the code commit: the launcher reads `READY.yaml`, `README.md` and the review at the commit it is given and refuses a commit without the review.
4. Take the exclusive server claim `dmarz-sybil-scarcity-synth` (`experiment: sybil-scarcity-synth`).
5. The server checkout must contain this directory and `researchers/dmarz/notes/sybil-scarcity-opus/` and `researchers/dmarz/notes/sybil-scale-api/src/` (S0 and the selftests compare packets against the unmodified earlier code). Python 3.12 with `requirements.txt`.

## Commands

The generic private launcher, from the agentops repository. Pass your own agent id as `--source`.

```
python3 scripts/run-ready-chain.py sybil-scarcity-synth <launch commit> setup --host <server> --source <agent id>
python3 scripts/run-ready-chain.py sybil-scarcity-synth <launch commit> chain --host <server> --confirm-paid --source <agent id>
python3 scripts/run-ready-chain.py sybil-scarcity-synth <launch commit> status --host <server>
python3 scripts/run-ready-chain.py sybil-scarcity-synth <launch commit> verify --host <server>
```

- `setup` checks out `<launch commit>`, installs the pinned requirements, runs `python3 src/selftest.py` and compares the number of tests and `study.source_hash()` with `READY.yaml`. Allow about 5 minutes (the earlier study's setup took 5 min 22 s; these selftests take about 3 minutes on a laptop).
- `chain` starts one detached process, `python src/chain.py run --stages S0,P0,Q0,S1`, with `SWARM_MODEL_API_KEY`, `SWARM_MODEL_WORKSPACE_ID`, `STUDY_BUDGET_LEDGER`, `STUDY_RESULTS_DIR`, `SWARM_SOURCE` and, when `--model` is given, `STUDY_MODEL` in its environment, and the hub client on `PYTHONPATH`. `--confirm-paid` is required because P0, Q0 and S1 make model calls: 1, 48 and 960.
- `status` prints `chain-status.json` and the ledger totals. `verify` checks artifact checksums against the hub, regrades every saved row and recomputes the summary and the analysis. Both print one JSON object on the last line; neither needs the model credential.

## What the chain does by itself

| Stage | Calls | Gate to pass | If it fails |
|---|---|---|---|
| S0 | 0 | 128 scripted rows valid, scripted qualification passes, every invariant holds | chain stops; nothing paid has happened |
| P0 | 1 | answer parses, model id matches, usage reported, stop reason `end_turn`, six values equal the expected values | chain stops after one call |
| Q0 | 48 | every configuration over its 12 packets: all valid, at least 69 of 72 fields, at least 11 exact packets, null on all 6 withheld rare facts. The first call dispatched is a high-effort call | chain stops; S1 is never queued |
| S1 | 960 | before queueing: 480 × Q0's mean cost per low-effort call + 480 × Q0's mean cost per high-effort call must fit in the remaining dollar cap | chain stops with `projection_exceeds_cap` before any S1 call |

Exit code 0: all requested stages done. Exit code 3: stopped at a failed stage or a refused gate; `chain-status.json` has `state: stopped_at_gate`, the stage and the reason. Any other non-zero code: internal error.

In S1 a call without a valid answer is recorded as failed, with the HTTP status, response body and request id, and dispatch continues. S1 stops only when more than 10 calls have failed, or at once on an integrity failure (ledger refusal, reservation breach, model mismatch, deadline). S1 can therefore end `done` with a few failed calls; the hub metrics `invalid` and `failed` say how many. S0, P0 and Q0 are strict: one failed call fails the gate. Answers are never retried. A request rejected with HTTP 429 or 529 is resent at most twice inside its 600 s budget. A failed token count never fails a call.

Limits in the hashed design, per model attempt: 2 requests in flight; 600 s per request; 28,800 s per stage; 32,400 s for the chain; 1,009 calls; 1,300 transport attempts; USD 240 of settled cost plus open reservations. Expected: about USD 101 to 136 on Claude Opus 5.5; S1 about 52 minutes to 4.2 hours depending on how long high-effort calls take (Q0 measures it).

## Billing outage: pause, stop and resume

A credit-balance error (HTTP 400, 402 or 403 whose body names the credit balance) pauses dispatch. The same call is re-sent every 60 s for up to 1,200 s. If it clears, the stage continues and reports `billing_pauses`. If it does not, the stage stops with reason `provider_credit_balance_low`: the affected calls and everything unfinished are recorded as not started, nothing counts as failed, and the chain exits 3.

After such a stop, and only then, the unfinished units may be resumed at the same source hash once the account has credit again. Record a dated amendment in this folder first (pre-registered in [preregistration.md](preregistration.md) item 12). Then, on the server, with the same environment, ledger and results directory:

```
python src/chain.py resume
```

It queues `s1-001-r1` (then `-r2`, …) with exactly the units left not started, runs it, and goes on with any stage that was requested after it. `verify` reads the original run and its continuations together and checks that no unit is counted twice. `resume` refuses in every other situation.

## Relaunch on the second model of the ladder

Only after a stage on `claude-opus-5-5` was refused on a limit or credit error that did not clear in 20 minutes (a `provider_credit_balance_low` stop, or repeated HTTP 429 past the retry rule), and as a dated amendment noted on the run request:

```
python3 scripts/run-ready-chain.py sybil-scarcity-synth <launch commit> chain --host <server> --confirm-paid --model claude-opus-5 --stages P0,Q0,S1 --source <agent id>
```

S0 already passed and is model-free, so it is not run again. The second model gets its own batches (`p0-001-opus-5`, `q0-001-opus-5`, `s1-001-opus-5`), its own probe and qualification, its own ledger file and its own results directory; the launcher points `STUDY_BUDGET_LEDGER` and `STUDY_RESULTS_DIR` at different paths per model. Expected spend on Claude Opus 5 is about USD 126 to 170 under the same USD 240 cap. Results are labelled by model and never pooled with the first model's rows.

## After the chain

1. `status`, then `verify`. Keep both outputs.
2. Do not rerun a stage. A batch name is refused the second time. A repair is a new attempt number in `design.yaml`, which changes the source hash, and needs its own pre-run review and, after a failed Q0, fresh qualification roots.
3. If Q0 stopped: before anything else read every miss (fixture type, configuration, returned and expected values); see the README, "What a Q0 stop means and triggers".
4. Write the post-mortem per [RUN-REVIEW.md](../../../toolkit/agent-experiments/RUN-REVIEW.md): reconcile assigned, started, terminal, graded and analyzed rows; compare the frames with the saved analysis; report actual calls, tokens and dollars by effort, failed calls with their evidence, count fallbacks and billing pauses.
5. Confirm the chain process has exited and uploads are verified, then release the claim. Do not destroy the server.

## Offline checks (no server, no model call)

```
python3 src/selftest.py
python3 src/worker.py --stage S0 --attempt <fresh-name>
python3 src/manifest.py --check
python3 src/rehearse.py --hub-dir <directory with hub.py and swarm_report.py>
```

Set `STUDY_RESULTS_DIR` to keep outputs outside the checkout; the default `results/` is git-ignored.
