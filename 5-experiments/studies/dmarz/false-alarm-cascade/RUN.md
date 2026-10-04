# Runbook: false-alarm-cascade, chain 002 (gpt-6-sol)

Nothing here has been run. This file is for the operator who takes the request from the private run queue. The server is a parameter. Public files contain no server address, hub address, token or credential.

## Before launch

1. The run request is in the private run queue, filed after dmarz/fleet-monitor's same-researcher check of this package. Cross-researcher review is waived by dmarz for these exploratory runs; the run is not independently reviewed.
2. Read [reviews/chain-002-pre.md](reviews/chain-002-pre.md) (READY.yaml `review:`). It names the code commit and the source hash. Chain 002 is the gpt-6-sol attempt of amendment A2; the earlier [chain-001 review](reviews/chain-001-pre.md) describes the Opus rungs. [READY.yaml](READY.yaml) carries the same hash, the number of selftests, the call caps, the dollar cap and the chain timeout.
3. Launch with the commit named in the run request, written `<commit>` below: the first commit on main that contains the pre-run review and has this source hash. Do not launch with the code commit: the launcher reads `READY.yaml`, `README.md` and the review at the commit it is given and refuses a commit without the review.
4. Take the exclusive server claim `dmarz-false-alarm-cascade` (`experiment: false-alarm-cascade`).
5. The server checkout needs only this directory. Python 3.12 with `requirements.txt`. The study imports nothing from other studies.
6. The OpenAI organisation is shared with other dmarz runs (sybil-split-xmodel, sybil-rules-180 and others use gpt-6-sol). This chain keeps at most 10 requests in flight (2 episodes × 5 agents in S1; 5 in Q0): about 40 requests and about 130,000 tokens per minute, expected (see the review).

## Commands

The generic private launcher, from the agentops repository:

```
python3 scripts/run-ready-chain.py false-alarm-cascade <commit> setup --host <server>
python3 scripts/run-ready-chain.py false-alarm-cascade <commit> chain --host <server> --confirm-paid
python3 scripts/run-ready-chain.py false-alarm-cascade <commit> status --host <server>
python3 scripts/run-ready-chain.py false-alarm-cascade <commit> verify --host <server>
python3 scripts/run-ready-chain.py false-alarm-cascade <commit> resume --host <server>          # only after provider_billing_stopped (or provider_credit_balance_low on Opus)
python3 scripts/run-ready-chain.py false-alarm-cascade <commit> chain --host <server> --confirm-paid --model claude-opus-5-5 --stages P0,Q0,S1 --source <agent id>   # Opus route, not before 2026-11-01
```

Pass `--source <agent id>` on every action. Without `--model` the launcher uses the first rung, gpt-6-sol on provider openai, sends only `SWARM_OPENAI_API_KEY`, and uses the default ledger `accounting/ledger.jsonl` and results directory `results`. `setup` takes about 5 minutes (the suite is 49 tests, about 2.5 to 4 minutes); the suite gives the same result with and without `STUDY_MODEL` / `STUDY_PROVIDER` set (it clears them at import).

- `setup` checks out `<commit>`, installs the pinned requirements, runs `python3 src/selftest.py` and compares the number of tests and `study.source_hash()` with `READY.yaml`.
- `chain` starts one detached process, `python src/chain.py run --stages S0,P0,Q0,S1`, with `SWARM_OPENAI_API_KEY` (gpt-6-sol; `SWARM_MODEL_API_KEY` and `SWARM_MODEL_WORKSPACE_ID` on an Opus rung), `STUDY_MODEL`, `STUDY_PROVIDER`, `STUDY_BUDGET_LEDGER`, `STUDY_RESULTS_DIR` and `SWARM_SOURCE` in its environment and the hub client on `PYTHONPATH`. `--confirm-paid` is required because P0, Q0 and S1 make model calls: 1, 24 and 3,600.
- `status` prints `chain-status.json` and the ledger totals. `verify` checks artifact checksums against the hub, rebuilds every actor input from the fixed inputs and the saved answers, regrades every saved row and recomputes the summary and the analysis. Both print one JSON object on the last line; neither needs the model credential.

## What the chain does by itself

| Stage | Calls | Gate to pass | If it fails |
|---|---|---|---|
| S0 | 0 | 1,225 scripted rows valid; scripted qualification and probe pass; all 16 invariants hold, including the negative control (private-evidence script: zero alarm effect) and the positive control (credulous script: full cascade and full recovery) | chain stops; nothing paid has happened |
| P0 | 1 | answer parses, model id matches, usage reported, finish reason `stop` (`end_turn` on Opus), decisions equal the reference on every resource whose three inspections agree | chain stops after one call |
| Q0 | 24 | 24 valid; decisions equal the private-evidence reference on at least 90% of gated decisions overall (134) and at each depth (35, 34, 65) | chain stops; S1 is never queued |
| S1 | 3,600 | before queueing: 3,600 × Q0's mean cost per call × 1.25 must fit in the remaining dollar cap | chain stops with `projection_exceeds_cap` before any S1 call |

Exit code 0: all requested stages done. Exit code 3: stopped at a failed stage or a refused gate; `chain-status.json` has `state: stopped_at_gate`, the stage and the reason. Any other non-zero code: internal error. There are no answer retries and no agent is needed between stages. On gpt-6-sol a request rejected with HTTP 429 (without billing words) or 500/502/503/504 is re-sent at most twice inside its 300 s budget (429 or 529 on Opus). A `finish_reason: length` is a failed call (`truncated_output`).

S1 runs 120 team episodes, two at a time. Inside an episode the six rounds run in order and the five agent calls of a round are sent together. If a call fails, its episode ends there and its later rounds are recorded as not started; dispatch continues. When more than 3 episodes have failed (`max_failed`), or at once on an integrity failure (ledger refusal, reservation breach, model mismatch, source or batch mismatch, deadline), no new episode or round starts, calls in flight finish, and every remaining call is recorded as not started; the hub run ends `failed`. Within the limit S1 ends `done` and reports its failed episodes. A failed request keeps its HTTP status, body excerpt and request id in the row.

**Billing outage.** On gpt-6-sol: HTTP 402, or a 400/403/429 whose body names quota, billing, credit, balance, insufficient, or a usage, spend or hard limit (OpenAI's `insufficient_quota` is a 429). On Opus: HTTP 400, 402 or 403 naming the credit balance (the wider detector the fleet monitor's 11:20Z addendum asks for is not in the Opus adapter; add it before any Opus launch). Either pauses all dispatch; the same call is re-sent every 60 s for up to 20 minutes. If it clears, the stage continues by itself. If not, S1 stops with reason `provider_billing_stopped` (gpt-6-sol) or `provider_credit_balance_low` (Opus). Then, and only then, run `resume`: it queues continuation batch `s1-001-gpt-6-sol-r1` (`s1-001-r1` on Opus 5.5) with exactly the not-started rows (interrupted episodes continue from the round where they stopped) under the same ledger and caps. `resume` refuses after any other stop. A billing stop in P0 or Q0 needs a new attempt.

**Other rungs.** The ladder is `gpt-6-sol`, `claude-opus-5-5`, `claude-opus-5`. The Opus rungs cannot be called before 2026-11-01 (Anthropic organisation limit). Use `--model claude-opus-5-5 --stages P0,Q0,S1` (or `claude-opus-5`) only as a dated amendment noted on the run request. S0, once passed, serves every model. The launcher points the ledger at `accounting/ledger-opus-5-5.jsonl` (or `-opus-5`) and results at `results-opus-5-5` (or `-opus-5`); batches are `p0-001`, `q0-001`, `s1-001` (Opus 5.5) and `p0-001-opus-5`, ... (Opus 5); each model needs its own P0 and Q0; results are never pooled across models.

Limits in the hashed design: 10 requests in flight; 300 s per request; 28,800 s per stage; 32,400 s for the chain; 3,625 calls per model; 4,000 transport attempts; 3 failed S1 episodes; USD 120 of settled cost plus open reservations on the gpt-6-sol ledger (USD 450 per Opus ledger). Expected on gpt-6-sol: about USD 57 and about 1.5 to 2.5 hours for S1 (estimate, see the pre-run review).

## After the chain

1. `status`, then `verify`. Keep both outputs.
2. Do not rerun a stage. A batch name is refused the second time. The only continuation is `resume` after a billing stop of S1. Any other repair is a new attempt number in `design.yaml`, which changes the source hash, and needs its own pre-run review. After a failed Q0 the first step is to read the failing answers with their packets (they are in `episodes.jsonl.gz`); a repaired attempt uses fresh qualification roots.
3. Write the post-mortem per [RUN-REVIEW.md](../../../toolkit/agent-experiments/RUN-REVIEW.md): reconcile assigned, started, terminal, graded and analyzed rows; compare the frames with the saved analysis; report actual calls, tokens and dollars.
4. Confirm the chain process has exited and uploads are verified, then release the claim. Do not destroy the server.

## Offline checks (no server, no model call)

```
python3 src/selftest.py
python3 src/worker.py --stage S0 --attempt <fresh-name>
python3 src/manifest.py --check
python3 src/rehearse.py --hub-dir <directory with hub.py and swarm_report.py>
```

Set `STUDY_RESULTS_DIR` to keep outputs outside the checkout; the default `results/` is git-ignored.
