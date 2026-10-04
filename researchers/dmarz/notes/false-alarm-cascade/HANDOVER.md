# Handover: false-alarm-cascade

Written 2026-10-04 by dmarz/pipeline from the paused builder's report (dmarz/pipeline-alarm, now released from this study). New owner, by dmarz/fleet-monitor's assignment: the "Big experiment" session on orbital-one (dmarz/scale-xl). Task: `tasks/build-false-alarm-cascade.md` (released; claim it). Nothing of this study has run on a server and no model call has been made.

## State

- Paused at main commit `c1de1da6805265e900bb08e54ee6cc3d1c98d263` ("WIP, paused:"). Source hash at that commit: `0c6391286fc0a95cc1d4d753cc23eaca0da80d38294094958dd610ade23c4352`. Earlier: plan `11dfdfd2`; first code package `2c4ef040` (hash `8dfa3d6e`, superseded; it passed selftest 35, offline S0 1,225/1,225 with 16/16 invariants and both controls, and a 29-check rehearsal).
- Done and tested at the pause commit (builder's runs on macOS, Python 3.9, no network): `python3 src/selftest.py` 38 tests OK (138 s); `python3 src/manifest.py --check` matches, digest `6f126bb5...`, rows S0 1,225 / P0 1 / Q0 24 / S1 3,600; `READY.yaml` is current for this hash (38 tests) but lacks the model ladder.
- All four failure-handling parts are in `src/` and `design.yaml` (`max_failed: 3` episodes; billing outage re-sent every 60 s for up to 1,200 s; `chain.py resume`).
- NOT rerun at the pause commit: the offline S0 and the six-scenario rehearsal (it passed 51/51 just before the last two small fixes).
- Stale: `README.md` (carries a paused banner), `preregistration.md`, `RUN.md`, `SETUP.md`, `VISUALIZATION.md` and `reviews/chain-001-pre.md` (carries a do-not-launch banner) still describe stop-on-first-failure and pin `2c4ef040` / `8dfa3d6e`.

## Decisions the paused builder made that the new owner should keep or change knowingly

- `resume` continues interrupted episodes where they stopped; it does not restart them from round 1. Calls are stateless and packets are rebuilt from fixed inputs plus saved answers, so the continuation runs exactly the not-started rows, and the hard S1 cap of 3,600 holds. Calls that gave up have their ledger reservation voided. The lead accepts this; pre-register it in the dated amendment (it differs from the written rule's "starts again from its first round").
- `resume` exists for S1 only. A billing stop in P0 or Q0 ends with the distinct reason and needs a new attempt.
- A credit error on the token-counting request does not pause by itself: it goes through the re-send and the byte fallback, and the pause starts when the messages request meets the same error.
- Q0 depths are {2, 3, 6} (depth 1 has no gated decision). P0 uses a round-3 packet and is judged only on resources where all three inspections agree. In the S0 control grid the scripted policies post nothing, so the controls are exact; a fourth posting pass was added (S0 is 1,225 rows). Dollar cap USD 360.

## Remaining steps, in order (builder's estimate 70 to 90 minutes, plus the ladder)

1. Add the model ladder (below) to `design.yaml`, `src/`, tests and rehearsal. New source hash.
2. Rerun the offline S0 and the rehearsal at the new hash.
3. Documents: README protocol and limits; dated preregistration amendment (failure rule, missing-data rule, resume rule as implemented, ladder); `RUN.md` with `resume` and `--model`; `SETUP.md`; `VISUALIZATION.md`; remove the banners.
4. Regenerate `manifest.json` and `READY.yaml` (`selftests`, `source_hash`, `model_ladder`); rewrite `reviews/chain-001-pre.md` naming the code commit and source hash.
5. `python3 scripts/lab.py check` must print 0 errors before every push; tick the task items.
6. Send the package to dmarz/fleet-monitor: files to read, what you ran, where you are least sure.

## Known traps and open doubts (from the builder)

- The rehearsal needs a local copy of the hub server and client (agentops `hub/hub.py`, `hub/swarm_report.py`): `python3 src/rehearse.py --hub-dir <dir>`. It refuses any hub that is not on 127.0.0.1.
- Load: 2 episodes in flight × 5 agent calls per round = at most 10 requests in flight, effort `medium`. State requests and tokens per minute in the review.
- Precision: 24 roots for a 10-point effect; the scripted credulous policy's bootstrap interval is about ±6 points.
- Q0 risk: whether Opus at medium effort passes the gate on decisions with posterior 0.084 (two clean of two, or four clean of six). A stop there is a result to report, not something to retune.
- Whether the provider accepts the per-call JSON schema (12 required enum fields, a claims array, a rationale string) is first seen at P0. The full suite has not been run on Python 3.12; only world generation was compared between 3.9 and 3.12 (identical). The launcher's `setup` runs the suite on the server.
- This study uses threads only (no process pool), so the 'Terminated' traceback seen in another study's log does not apply.
- Files to read first: `src/worker.py`, `src/provider.py`, `src/chain.py`, `src/rehearse.py`, `README.md`, then `preregistration.md` and `design.yaml`.

## Rules that apply (all on main)

- The contract: [READY-CHAIN.md](../pipeline/READY-CHAIN.md): files, READY.yaml, stage behaviour, chain, budget, transport retry rule, **Failure handling** (four parts, already in this study's code), **Providers and models** (the model ladder, NOT yet in this study), Opus request rules, offline evidence.
- Reviewed reference packages: [sybil-scarcity-opus](../sybil-scarcity-opus/) (ran end to end through the launcher, run queue 248) and [sybil-split-opus](../sybil-split-opus/) (run queue 252). Their `reviews/chain-001-pre.md`, `RUN.md` and `READY.yaml` show the expected shape of the documents.
- The launcher: agentops `scripts/run-ready-chain.py` (actions setup, chain, resume, status, verify; `--host`, `--model`, `--source`), described in agentops `docs/RUN-QUEUE.md` "Ready requests". It reads `READY.yaml`, `README.md` and `reviews/chain-001-pre.md` at the launch commit and refuses a commit that does not contain the review. So the review names the **code commit** and the source hash and says the launch commit is "the commit named in the run request, the first commit on main that contains this review and has this source hash"; no launch hash is written into any file, and command lines use `<launch commit>`.
- Authority wording for the preregistration and the pre-run review: "dmarz did not name this study. He told the fleet monitor to keep five experiments running by building a pipeline of prepared experiments, to use Opus for everything, and not to gate on cost; the fleet monitor chose this study from his backlog (honeypot-vigilance hunch V4. The hunch note's instruction to hold the full swarm build until the simulator decision is noted: this is a single-purpose instrument, not the simulator) under that delegation. Cross-researcher review is waived by dmarz for these exploratory runs; dmarz/fleet-monitor's check is a same-researcher check and nothing more; the run is not independently reviewed." The shared USD 500 figure is no longer a gate (dmarz: read out the total, do not hold runs for cost); state expected spend and that the running total is already past it.
- The package launches nothing. When it is complete it goes to dmarz/fleet-monitor for the same-researcher check; the run request is filed with labels `run-queue` and `run-queue:ready` only after its go. Operator notes for RUN.md: pass `--source <agent id>`; `setup` takes about 5 minutes; `resume` is used only after a `provider_credit_balance_low` stop.
- The pre-run review states in one line each: the four failure-handling parts adopted, `max_failed`, the billing-outage schedule, and the model ladder.

## The model ladder (to add; it changes the source hash)

1. `design.yaml`: `model_ladder: [claude-opus-5-5, claude-opus-5]` and `models:` with each model's own prices and request settings, e.g. `claude-opus-5-5: {input_usd_per_million: 4, output_usd_per_million: 20}`, `claude-opus-5: {input_usd_per_million: 5, output_usd_per_million: 25}`. Before you pin, verify the request rules of `claude-opus-5` against the official Anthropic documentation (fetch the docs; do not rely on memory, and make no model call): as relayed, thinking is on by default and can be disabled only at effort high or lower, `budget_tokens` and sampling parameters are still rejected, and HTTP 200 refusals are possible. Keep the request body the same five keys for both models if the documentation allows it (`model, max_tokens, system, messages, output_config {effort, format}`), and record in the plan what you verified, with the page you read. If the two models need different bodies, put the difference in `models:` and test both.
2. The model of an attempt comes from the environment variable `STUDY_MODEL` (set by the launcher's `--model`), must be in the ladder, and defaults to the first entry. One model per attempt; no mixing inside a stage; the model is in the hub params of every run and in every row.
3. Batch names: `<stage>-<attempt>` for the first model of the ladder, `<stage>-<attempt>-<tag>` for any other, where the tag is the model id without the `claude-` prefix (`p0-001-opus-5`, `q0-001-opus-5`, `s1-001-opus-5`). Continuation batches after a billing stop append `-r1` as before.
4. Gates: S0 is scripted and model-free, so one passed S0 at the source hash serves every model. P0 needs that S0. Q0 needs the P0 of the SAME model at the same source hash; S1 needs the Q0 of the same model. Each model gets its own P0 and Q0 at launch; a qualification on one model never qualifies the other.
5. Ledger and caps: one ledger file per model attempt (the launcher points `STUDY_BUDGET_LEDGER` at a different file per model and `STUDY_RESULTS_DIR` at a different directory), each with the full per-stage call caps. The dollar cap in the design is sized for a full chain on the more expensive model (state the arithmetic for both). The projection gate uses the attempt's own model prices.
6. Analysis and reporting never pool models: every table and figure is for one model, named in its title; a comparison across models, if both ever run, is a separate labelled section.
7. `READY.yaml`: `model: claude-opus-5-5` (the default) plus `model_ladder: [claude-opus-5-5, claude-opus-5]`. RUN.md shows the relaunch on the second model: `python3 scripts/run-ready-chain.py <study> <launch commit> chain --host <server> --confirm-paid --model claude-opus-5 --stages P0,Q0,S1 --source <agent id>` (S0 already passed), and says when to use it: only after a stage was refused on a limit or credit error that did not clear in 20 minutes (a `provider_credit_balance_low` stop, or repeated 429 past the retry rule), as a dated amendment noted on the run request.
8. Tests: the ladder default and override; a model outside the ladder is refused; batch names per model; the coordinator refuses Q0 on one model behind a P0 of the other; prices per model in the reservation and settled cost; the rehearsal runs the full chain once on the default model and, on the same throwaway hub and source hash, P0 -> Q0 -> S1 on the second model after a simulated billing stop of the first.

Launcher side of the ladder (already implemented and tested): `--model claude-opus-5` sets `STUDY_MODEL`, and points `STUDY_BUDGET_LEDGER` at `accounting/ledger-opus-5.jsonl` and `STUDY_RESULTS_DIR` at `results-opus-5`; the default model uses `accounting/ledger.jsonl` and `results`. `READY.yaml` needs `model: claude-opus-5-5` and `model_ladder: [claude-opus-5-5, claude-opus-5]`.

- 2026-10-04 11:50Z dmarz/scale-xl: added the model ladder (code af115c44, source 7803e3b8; selftest 41, offline S0, manifest, rehearsal 57/57 all pass) and rewrote the documents and pre-run review (7f5ecb0a). Next: dmarz/fleet-monitor's same-researcher check, then the run request. Task returned to dmarz/pipeline.

- 2026-10-04 evening dmarz/pipeline-alarm-oai: the Anthropic organisation hit its monthly limit (until 2026-11-01). Pre-registration amendment A2 (`ddb85c9d`) and code `5f83bd28` (source `0947408b…`) put gpt-6-sol first in the ladder through the reference OpenAI adapter; new pre-run review [chain-002-pre.md](reviews/chain-002-pre.md), READY.yaml `review:` points at it. Gates, caps and analysis unchanged. Open for any later Opus launch: the 11:20Z addendum's wider billing detector is still not in the Opus adapter.

## Addendum, 2026-10-04 about 11:20Z (dmarz/fleet-monitor's requirement for every package not yet pinned)

Widen the billing detector in this study's adapter before pinning: a provider-side billing or limit stop is HTTP 402, or an HTTP 400, 403 or 429 (from either endpoint) whose body names, case-insensitively, any of `credit`, `balance`, `billing`, `usage limit`, `spend limit`, `limit exceeded`, `insufficient`. A 429 without such words stays ordinary rate limiting under the retry rule. Such a refusal pauses and re-sends (every 60 s for up to 1,200 s) and is never recorded as a model failure; the evidence fields (status, body, request id) are kept. Reason: dmarz's Anthropic console showed Opus 5.5 "maxed out" at about 10:35Z, and a usage-limit refusal is not worded "credit balance". Add tests for a 400 naming usage limits and for a 429 naming a spend limit. Also: no `pkill` by pattern on shared machines; kill only process ids you started.
