# Runbook: sybil-split-xmodel, chain 001 (one chain per model)

Nothing here has been run. This file is for the operator who takes a request from the private run queue. The server is a parameter. Public files contain no server address, hub address, token or credential.

## Before launch

1. The run request is in the private run queue, and dmarz/fleet-monitor has done its same-researcher check. Cross-researcher review is waived by dmarz for these exploratory runs, so the run is not independently reviewed.
2. Read [reviews/chain-001-pre.md](reviews/chain-001-pre.md). It names the code commit and the source hash. The launch commit is the commit named in the run request: the first commit on `main` that contains that review and has that source hash.
3. One exclusive server claim per model chain:
   - `dmarz-sybil-split-xmodel` (`experiment: sybil-split-xmodel`) for the first chain;
   - a second claim for the other model if the two run at the same time (see "Two models").
4. The server needs the whole repository at the launch commit, which the launcher checks out. S0 reads the parent study `../sybil-split-opus/` (pinned files) and runs the parent's own code. It also needs Python with `requirements.txt` (PyYAML, Pillow, numpy).
5. Credential aliases, passed in memory by the launcher, only the one for the chosen model:
   - `SWARM_OPENROUTER_API_KEY` for `qwen/qwen3.7-flash`;
   - `SWARM_OPENAI_API_KEY` for `gpt-6-sol`.

## Commands

Use the generic private launcher in the agentops repository; the operator also passes `--source <its agent id>`. `<model>` is `qwen/qwen3.7-flash` (the default, first in the ladder) or `gpt-6-sol`.

```
python3 scripts/run-ready-chain.py sybil-split-xmodel <launch commit> setup  --host <server>
python3 scripts/run-ready-chain.py sybil-split-xmodel <launch commit> chain  --host <server> --confirm-paid --model <model> --stages S0,P0,Q0,S1
python3 scripts/run-ready-chain.py sybil-split-xmodel <launch commit> status --host <server> --model <model>
python3 scripts/run-ready-chain.py sybil-split-xmodel <launch commit> verify --host <server> --model <model>
```

- **`setup`** runs `python3 src/selftest.py` (97 tests, about 2.5 minutes on a laptop) and compares the test count and `study.source_hash()` with `READY.yaml`.
- **Every model runs all four stages, S0 included.** S0 batches carry the model tag (`s0-001-qwen`, `s0-001-sol`), and each model's P0 gate requires that model's own S0. Always pass `--stages S0,P0,Q0,S1`. S0 makes no call and takes about 4 minutes.
- **What the launcher sets.** `--model` sets `STUDY_MODEL`. The launcher gives each model its own ledger file and results directory and sends only that model's credential.
- **Reading P0.** P0's summary (`probe`), hub metrics (`probe_*`) and run message carry the raw response metadata of the probe call: response model, provider (Qwen), response id, finish reason, reasoning tokens, latency, input and output tokens, and tokens per byte. If P0 fails, read them first.
- **Read-only commands.** `status`, `verify` and `python src/chain.py summarize` each print one JSON object on the last line. None needs a credential.

## Two models

The two chains are independent: separate batches (suffix `-qwen` or `-sol`), ledgers, caps, results and gates. They may run at the same time on two servers under two claims.

The hub hands out the next planned run of an experiment, and the two chains share one hub experiment. So a chain refuses to queue a stage (`queue_not_empty`) while a planned run of either model is waiting, and it accepts the other model's runs that are assigned or running. If a stage is refused for that reason, nothing ran. Re-run the chain later with `--stages` starting at the refused stage; the gates decide what may start.

## What each chain does by itself

| Stage | Calls | Passes when | If it does not |
|---|---|---|---|
| S0 | 0 | 1,853 scripted rows valid; the parent's invariants hold; scripted qualification and probe pass; grid not degenerate; packets byte-identical to the parent's code and to the parent's recorded S1 run; system prompt starts with the parent's | the chain stops; nothing paid has happened |
| P0 | 1 | probe fixture (engineering root 4919, `multirow1`): adapter checks pass and the answer equals the expected values | the chain stops after one call |
| Q0 | 60 | before queueing: P0's tokens per message byte × 13,746 bytes ≤ 31,000 tokens; then per shape: 10 of 10 valid, field accuracy ≥ 0.95, exact ≥ 0.90, null on every withheld field | `input_ceiling_projection` or `gate_failed`; S1 is never queued; a Q0 stop is the result, with no repair |
| S1 | 2,688 | before queueing: the input ceiling as above, and 2,688 × Q0's cost per call fits in the remaining cap (`projection_exceeds_cap`); then at most 27 failed calls and no integrity failure | S1 ends `failed` with the reason; rows preserved |

**Exit codes.** 0 means every requested stage is done. 3 means the chain stopped at a failed stage or a refused gate (`chain-status.json` has `state: stopped_at_gate`, the stage and the reason). Any other non-zero code is an internal error.

**Billing outage.** A credit, balance or quota refusal (OpenAI: 429 `insufficient_quota`) pauses the stage, and the same call is re-sent every 60 s for up to 20 minutes. After that the stage stops with `provider_credit_balance_low` (Qwen) or `provider_billing_stopped` (Sol). After funds are restored, and only then, run `python src/chain.py resume` (the launcher's `resume` action with the same `--model`). It queues `s1-001-<tag>-r1` with exactly the units not started. Record it as a dated amendment in this folder.

**Limits, per model, in the hashed design:**
- 4 requests in flight; 120 s per request; 3 h per stage; 4 h per chain;
- 2,749 calls and 3,300 transport attempts;
- USD 3 (Qwen) or USD 90 (Sol) of settled cost plus open reservations.

**Expected:**

| Model | Cost | S1 wall time |
|---|---|---|
| Qwen | about USD 0.35 | 20 to 40 minutes |
| Sol | about USD 25 to 50 | 30 to 60 minutes |

Wall times are not measured.

## After the chain

1. Run `status`, `verify` and `summarize`, and keep their outputs.
2. Do not rerun a stage: a batch name is refused the second time.
3. Write the post-mortem per [RUN-REVIEW.md](../../../../tooling/agent-experiments/RUN-REVIEW.md) for each model. Reconcile the rows, compare the frames with `analysis.json`, and report calls, tokens, dollars, failed calls with their evidence, and billing pauses. Report `versus_parent` and `test_retest` as descriptive secondaries, never pooled.
4. Update the evidence registry row and the README's results section.
5. Confirm the chain process has exited and the uploads are verified, then release the claim.

## Offline checks (no server, no model call)

```
python3 src/selftest.py
python3 src/worker.py --stage S0 --attempt <fresh-name>
python3 src/manifest.py --check
STUDY_MODEL=qwen/qwen3.7-flash python3 src/rehearse.py --hub-dir <directory with hub.py and swarm_report.py>
STUDY_MODEL=gpt-6-sol          python3 src/rehearse.py --hub-dir <directory with hub.py and swarm_report.py>
```
