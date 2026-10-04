# Pre-run assessment: chain-001 (S0, P0, Q0, S1), one chain per model

- **Experiment, owner and stage.** sybil-split-xmodel / dmarz. Built by dmarz/pipeline-split-qwen for dmarz/fleet-monitor. The operator is whoever takes a request from the private run queue. There is one chain of four stages per model:
  - batches `s0-001-qwen`, `p0-001-qwen`, `q0-001-qwen`, `s1-001-qwen` for `qwen/qwen3.7-flash`;
  - the same batches with suffix `-sol` for `gpt-6-sol`.
- **Parent.** sybil-split-opus chain-001: complete_valid_result, primary +0.410 (interval +0.278 to +0.549), USD 45.39. Its [post-run review](../../sybil-split-opus/reviews/chain-001-post.md) was read. Nothing of this study has run, and no model call has been made. The checks below were run offline by the builder.
- **Status.** **Ready** for dmarz/fleet-monitor's same-researcher check and for queueing, each model separately. This assessment does not launch anything.
- **Authority and review status.** dmarz did not name this study. The fleet monitor chose it under dmarz's instructions of 2026-10-04: keep experiments running and ship tonight, and after the Anthropic limit "use opus 5 or an oai model". The fleet monitor also set the two models and the gpt-6-sol cap. dmarz waived cross-researcher review for these exploratory runs. The fleet monitor's check is a same-researcher check and nothing more. **This run is not independently reviewed.**
- **Question and decision.** Does the parent's identity-splitting contrast appear for two cheaper models reading the identical packets? A large positive primary on a model would show that the parent's result is not specific to Opus 5.5. A primary near zero, or a Q0 stop, would mark the result as model-dependent. The model and its configuration change together (no reasoning for Qwen; low effort for Sol, against Opus 5.5 at effort low), so neither part can be credited alone.
- **What would make a run uninformative for a model:** a Q0 stop, since S1 then does not run. That is reported as the result, with no repair. Also uninformative: an S1 with more than 27 failed calls.

## Design and assessment

- **Identical inputs, proven mechanically.** `src/sim.py` is the parent's file byte for byte. S0 checks four things (`study.check_parent_identity`):
  - The SHA-256 of the parent's `src/sim.py`, `src/study.py`, `design.yaml` and `records/s1-episodes.jsonl.gz`.
  - The parent's own code, unmodified, in its own process: it must give the same id-to-packet-hash map as this code for S0 (1,853), P0 (1), Q0 (60) and S1 (2,688). It must also report the parent's source hash `95889bea…`.
  - The parent's recorded S1 rows must hold exactly these 2,688 packet hashes.
  - The system prompt must begin with the parent's prompt, extracted from the parent's `src/provider.py`.
  
  All four held offline. The user message is the parent's (`json.dumps(packet, sort_keys=True)`), so its SHA-256 is the recorded packet hash; a selftest checks this for P0 and Q0.
- **The one change in what a model reads.** One paragraph appended to the system prompt states the answer shape. It is needed because both routes are JSON-object mode, while the parent's route sent a JSON schema. The paragraph contains none of the parent's forbidden words.
- **Harmless-variant audit of every structural validator** (the fleet monitor's lesson of 2026-10-04).
  - `study.validate` accepts any key order, surrounding whitespace, and integral numbers written with a fraction (12.0), as the parent's JSON schema accepts them.
  - It rejects strings such as "12", extra or missing keys, booleans, non-integral numbers, and code fences, as the parent's schema rejects them.
  - Tests drive these through the real adapters with a stubbed endpoint: P0 passes with fraction-form numbers, reversed key order and padding; it fails with strings, a code fence, or a wrong provider. Rehearsal chain (d) answers every call with the fraction-form, reversed-key variant and must pass P0, Q0 and S1.
  - The adapters' own structural checks were left as they are: Qwen must name provider Alibaba and finish `stop`; duplicate keys are rejected.
  - The risk I cannot remove offline is that a model wraps its JSON in prose or a fence despite JSON-object mode. P0 shows that after one call. The trust-credit-qwen run (same route, same answer shape stated in words) returned 528 of 528 valid answers.
- **Gates, the parent's, unchanged.**
  - P0: the exact expected values.
  - Q0: per shape, 10 of 10 valid, field accuracy ≥ 0.95, exact packets ≥ 0.90, null on all 40 withheld fields.
  - The parent's Opus run passed Q0 60 of 60. Whether a no-reasoning Qwen abstains on withheld rare skills is the main qualification risk.
- **Primary.** The parent's, unchanged, per model: (k = 27 − k = 1 under degree) − (the same under coverage), attacker pass 0.1, 12 checks, mean of the two family means, 10,000-draw root bootstrap. On the engineering roots the scripted plurality rule gives +0.40625, the same as the parent's S0.
- **Secondaries.** Everything the parent reports, plus:
  - `versus_parent`: per cell and primary, this model minus Opus 5.5, paired by root, from the parent's recorded rows;
  - `test_retest`: agreement within byte-identical packet groups.
  
  Both are descriptive and never pooled.

## Changes and unresolved issues

| Issue / prior evidence | Change or diagnostic | Expected effect | Acceptance check | Owner |
|---|---|---|---|---|
| Replication must use the parent's exact packets | byte-identity proof against the parent's own code and recorded run | any drift stops S0 | `check_parent_identity` empty; selftests | builder |
| JSON-object mode has no schema | shape stated in words; local validation; harmless variants accepted | interface failures visible at P0 after one call | validator and probe tests; rehearsal chain (d) | builder |
| Two models on one hub experiment | per-model batches, ledgers, caps, results and gates; no stage queued while a planned run of either model waits | chains cannot take each other's runs | gate test with the other model's planned and running runs | builder |
| Anthropic organization at its usage limit | OpenRouter and OpenAI routes, reference adapters copied unchanged | the chain can run without Anthropic | both adapters' own tests inside the selftest | builder |
| Live routes unverified | P0 is one call per model | first real observation costs one call | P0 gate | operator |
| GPT-6 Sol output budget: `max_completion_tokens` 2,000 covers reasoning plus the answer | low effort; the visible answer is about 60 tokens | a long reasoning trace would end `length` → `truncated_output`, a failed call (strict in P0 and Q0) | P0 and Q0 | operator |

## Frozen execution plan

- **Code commit:** `0ca09f04` (on `main`; code, design, manifest). The documents commit `f69f0c7c` and this review's commit change no hashed file.
- **Source hash:** `ebfb2bc3703cbb5ac882641ca0f71dfb9dfda0ee5436dd1a8b4879dcef97c2cd`. It covers design.yaml, experiment.yaml, requirements.txt and every `src/*.py`, including both adapters and their tests. `READY.yaml` carries the same hash and `selftests: 97`.
- **Launch commit:** the commit named in the run request, the first commit on `main` that contains this review and has this source hash. The launcher's setup step verifies the source hash on the server. No launch hash is written in this file.
- **Model settings.**
  - Qwen: OpenRouter, request body exactly the program v5 template (`provider {only: [alibaba], allow_fallbacks: false, require_parameters: true}`, `reasoning {enabled: false}`, `max_tokens` 1,000, `response_format {type: json_object}`) plus `messages`.
  - Sol: OpenAI Chat Completions, body exactly `model: gpt-6-sol`, `reasoning_effort: low`, `max_completion_tokens: 2000`, `response_format {type: json_object}` plus `messages`. Prices are the reference row: USD 2.00 / 0.20 / 2.50 / 10.00 per million.
- **Assignment manifest.** `manifest.json`, digest `2a4b21669c9301a440c3f59d0c1cbe8439a981507e2649203b1c1a0275fc6b75`. It is the same for both models.
  
  | Stage | Assignments | Hard `max_calls` | Largest request (message bytes) |
  |---|---|---|---|
  | S0 | 1,853 | 0 | 13,515 |
  | P0 | 1 | 1 | 10,323 |
  | Q0 | 60 | 60 | 13,515 |
  | S1 | 2,688 | 2,688 | 10,359 |
  
  P0 is the probe fixture of root 4919. S1 messages total 23.2 MB.
- **Gates, per model.**
  - S0: every row valid, the parent's invariants hold, scripted qualification and probe pass, the grid is not degenerate, and byte identity holds. Otherwise the chain stops with no call.
  - P0: needs this model's passed S0 at this source hash. It stops after one call on a rejected request, a model or provider mismatch, missing usage, a finish other than `stop`, reasoning tokens (Qwen), output over 2,000 (Sol), invalid JSON or structure, or an answer that is not exactly right.
  - Q0: needs this model's passed P0, and P0's tokens per message byte × 13,515 ≤ 31,000 (`input_ceiling_projection`). It fails on any shape below threshold. S1 is then never queued, and nothing is repaired.
  - S1: needs this model's passed Q0, the ceiling projection, and 2,688 × Q0's cost per call within the remaining cap (`projection_exceeds_cap`).
  - A batch is never queued twice. No stage is queued while a planned run of either model, or an assigned or running run of this model, exists.
- **Failure rule.**
  - Part 1: status, body (2,000 characters) and request id kept on every failed request.
  - Part 2: token counting is not applicable; the reservation is a byte bound, times 10.
  - Part 3: in S1, `max_failed` is 27; integrity failures stop at once; S0, P0 and Q0 are strict.
  - Part 4: a billing or quota refusal pauses for up to 20 minutes, then the stage stops resumable (`provider_credit_balance_low` / `provider_billing_stopped`, both accepted by `chain.py resume`).
  - Re-sent statuses: Qwen 429/502/503/529; Sol 429 rate limit and 500/502/503/504; at most twice.
- **Exact commands.**
  ```
  python3 scripts/run-ready-chain.py sybil-split-xmodel <launch commit> setup --host <server>
  python3 scripts/run-ready-chain.py sybil-split-xmodel <launch commit> chain --host <server> --confirm-paid --model <model> --stages S0,P0,Q0,S1
  ```
  Then `status` and `verify`. On the server the chain runs `python src/chain.py run --stages S0,P0,Q0,S1` with `STUDY_MODEL` set.
- **Limits per model.** 2,749 calls, 3,300 transport attempts, 4 in flight; 120 s per request, 3 h per stage, 4 h per chain.

  | Model | Dollar cap (settled plus open reservations) | Upper bound on spend | Expected |
  |---|---|---|---|
  | Qwen | USD 3 | input ≤ 24 MB × USD 0.03 per M = USD 0.72, plus output ≤ 2.75 M × USD 0.13 per M = USD 0.36 | about USD 0.35 |
  | Sol | USD 90 (set by the fleet monitor) | — | 10 to 18 M input tokens, USD 20 to 45 at the cache-write bound, plus output at USD 10 per M; about USD 25 to 50 |

  Open reservations at 4 in flight are at most about USD 0.02 (Qwen) and USD 2.2 (Sol).
- **Time.** S0 takes about 4 minutes, mostly the byte-identity check. S1 needs 672 calls per worker: 22 to 45 minutes at 2 to 4 s per call, inside the 3 h stage limit unless the mean call exceeds 16 s.
- **Retry, stop and missing data.** No answer retry. Every assignment ends completed, failed or not started. Outcomes are reported complete-case with denominators and with 0/1 bounds.

## Regression and competence checks, run offline on the code commit (2026-10-04)

- `python3 src/selftest.py`: `Ran 97 tests ... OK` (146 s, Python 3.9). This includes:
  - the OpenRouter adapter's 32 tests and the OpenAI adapter's 28 tests;
  - the parent's world, packet, fixture, gate, manifest, analysis and frame tests;
  - new tests for byte identity, the two-model configuration, harmless variants, the probe through each adapter, and per-model gates.
- `python3 src/worker.py --stage S0 --attempt s0a`: 1,853 of 1,853 rows valid, 0 invariant violations including byte identity with the parent, scripted primary +0.40625, 0 calls, 218 s.
- `python3 src/manifest.py`: written; `test_manifest_regenerates_identically` passes.
- `python3 src/rehearse.py --hub-dir <copy of agentops main hub>`, once with `STUDY_MODEL=qwen/qwen3.7-flash` and once with `STUDY_MODEL=gpt-6-sol`. Each used a throwaway hub on 127.0.0.1 and an in-process stub in that provider's response shape; the stub rejects any body that is not exactly the frozen template plus messages.
  - (a) Full chain: S0, P0, Q0 and S1 `done` with 0 / 1 / 60 / 2,688 calls, and `chain verify` passed. Passed for both models.
  - (b) A never-abstaining stub: exit 3, `stopped_at_gate` at Q0 (`gate_failed`), and no S1 run on the hub. Passed for both models.
  - (c) Credit or quota runs out after 150 S1 calls and stays out:
    - S1 stops with `provider_credit_balance_low` (Qwen; stub HTTP 402) or `provider_billing_stopped` (Sol; stub HTTP 429 `insufficient_quota`), with one billing pause and nothing failed.
    - `chain resume` then runs `s1-001-<tag>-r1` with exactly the 2,538 units not started.
    - Every unit is answered once, 4 reservations are voided, the S1 calls stay inside the exact 2,688 cap, and `chain verify` passes.
  - (d) Two S1 calls fail and every answer is a harmless variant (fraction-form numbers, reversed key order, padding):
    - P0 and Q0 pass, and S1 ends `done` with 2 failed and 2,686 valid.
    - `chain verify` passes.
    - On the OpenAI route the injected failure is HTTP 400, because that adapter re-sends 500.
  - All 24 rehearsal checks passed for each model, in about 17 minutes per model. Stub token counts and dollars are not estimates of the real ones.
- **Not tested:**
  - the live OpenRouter and OpenAI routes and the real hub;
  - the full suite under the server's Python;
  - the launcher's new `providers:` handling and `--model` for OpenAI, which were written by another builder at the same time;
  - the parallel-chain race guard against the real hub (tested against a fake hub only).
- **Where I am least sure:**
  - whether Qwen with reasoning disabled abstains on all 40 withheld fields in Q0; one non-null answer fails the shape;
  - whether gpt-6-sol at low effort stays inside 2,000 completion tokens on 80-row packets;
  - whether the launcher passes `--stages S0,P0,Q0,S1` for the second ladder model, which READY-CHAIN says shares the first model's S0. Here each model needs its own S0, and without it P0 is refused cleanly with no call.

## Server claim, credentials, artifacts

- One exclusive claim per model chain, taken by the operator.
- `SWARM_OPENROUTER_API_KEY` or `SWARM_OPENAI_API_KEY` is supplied in memory by the launcher for the chosen model only.
- Results go under `STUDY_RESULTS_DIR` and the ledger at `STUDY_BUDGET_LEDGER`, per model. Artifacts go to the hub under `sybil-split-xmodel/<run>`.

## Gate decision and next action if this attempt fails

- Decision: ready.
- If P0 fails on the interface, read the kept status, body and answer text; an adapter defect goes to the pipeline.
- If Q0 fails, that is the model's result: read the misses (`qualification_misses` in the summary) and write the post-mortem. Nothing is retuned.
- If S1 stops on billing, resume. If it stops for another reason, write the post-mortem with the bounds.

## Visualization mapping

Mapping v1 in [VISUALIZATION.md](../VISUALIZATION.md) is the parent's mapping, with run binding per model and the model named in the header. It covers:

- wrong answers by identity count;
- accuracy against attacker seat share;
- per-root primary contrasts;
- `initial_frame.png`, `progress.png`, `final_frame.png` and `replay.gif`.

The selftest renders empty, partial, failed and complete frames and decodes the GIF frame by frame. After the run, the operator compares the final frame with `analysis.json`.

## Amendment A1 pre-run assessment: gpt-6-sol at reasoning effort none (2026-10-04)

- **Status:** **ready** for dmarz/fleet-monitor's same-researcher check. Approved by the fleet monitor exactly as proposed in [chain-001-sol-post.md](chain-001-sol-post.md). Not independently reviewed. dmarz did not name this configuration.
- **Order:** the pre-registration (item 13, amendment A1) was committed in `a02c488f` before any of its code. The code commit is `52139693`.
- **What changes:**
  - **Model setting.** Only `reasoning_effort`, from low to none, for model `gpt-6-sol`. The request body is exactly `model: gpt-6-sol`, `reasoning_effort: none`, `max_completion_tokens: 2000`, `response_format {type: json_object}` and `messages`. With effort none the adapter would accept `temperature` and `top_p`; none is sent, and a selftest asserts it. A response that reports reasoning tokens is a failed call (`unexpected_reasoning_tokens`, the reference adapter's rule for effort none).
  - **Code.** A configuration name (`gpt-6-sol/r1`), selected by `STUDY_MODEL=gpt-6-sol` with `STUDY_REPLICATION=r1`. These variables are set by the launcher's `--model gpt-6-sol --replication r1`.
  - **Separation from earlier chains.** Gates, batches (`s0-001-solnone`, `p0-001-solnone`, `q0-001-solnone`, `s1-001-solnone`), rows and chain status carry that name. The effort-low runs therefore never admit or mix with this chain.
  - **Selftests.** They now clear `STUDY_MODEL`, `STUDY_PROVIDER` and `STUDY_REPLICATION` at import and set each configuration explicitly. The suite gives the same result under any launch environment (the cause of the scarcity package's setup failure).
- **What does not change:** packets (byte identity re-proved in S0), system prompt, validation, fixtures, thresholds, analysis and every cap except the configuration's own ledger.
- **Frozen plan:**
  - Code commit `52139693`. Source hash `5ce08e7d0e09232f610b28f63ef57f1d48dda04ebbf1e72aac40c0da48af3d1b`.
  - `READY.yaml`: `selftests: 100`, `replications: [r1]`, `ledger: fresh`.
  - **Fresh ledger:** this configuration starts its own ledger file (launcher tag `-gpt-6-sol-r1`). The study's earlier paid runs are at source hash `ebfb2bc3…` and keep their own ledgers.
  - Command: `run-ready-chain.py sybil-split-xmodel <launch commit> chain --host <server> --confirm-paid --model gpt-6-sol --replication r1 --stages S0,P0,Q0,S1`, after `setup` with the same `--model` and `--replication`.
  - Caps: P0 1, Q0 60, S1 2,688; 2,749 calls; USD 90 settled plus open reservations. Expected: P0 and Q0 about USD 0.5 (the effort-low pair cost USD 0.53); S1, only if Q0 passes, about USD 25 to 45.
  - Gates as in item 9. A second Q0 stop ends the gpt-6-sol route.
- **Offline checks on `52139693`:**
  - `python3 src/selftest.py`: 100 tests OK with no launch variables (186 s; one run hit a transient full-disk error on this Mac, the failed test passed on rerun). Also 100 tests OK under `STUDY_MODEL=gpt-6-sol STUDY_REPLICATION=r1 STUDY_PROVIDER=openai` (163 s).
  - Rehearsal with `STUDY_MODEL=gpt-6-sol STUDY_REPLICATION=r1`: results in the line below.
- **Not tested:** the live route at effort none, the launcher's `--replication` path for this study, and the server's Python.
- **Rehearsal results** for `gpt-6-sol/r1` on `52139693`: throwaway hub on 127.0.0.1, with a stub in the OpenAI response shape that rejects any body that is not exactly the effort-none template plus messages.
  - (a) The full chain completed (`s0-001-solnone` … `s1-001-solnone` all done), and `chain verify` passed.
  - (c) A billing stop came from a 429 `insufficient_quota`, giving `provider_billing_stopped`. Resume then completed S1 with every unit answered once, and verify passed.
  - (d) Two failed S1 calls plus harmless-variant answers: S1 was done with 2 failed, and verify passed.
  - (b) In the full rehearsal run, chain (b) ended with `internal_OSError` at P0. This Mac's disk was full during that run (3.3 GB free, other agents writing; the same error appeared once in the selftests). I re-ran chain (b) alone with the never-abstaining stub: exit 3, `stopped_at_gate` at Q0 with `gate_failed`, 61 stub answers, and no S1 run on the hub. The checks of (a), (c) and (d) all passed in the full run.
