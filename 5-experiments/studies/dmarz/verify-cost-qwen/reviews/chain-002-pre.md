# Pre-run assessment: chain-002 (attempt 002: S0, P0, Q0, S1), the one bounded repair

Follows [the review cycle](../../../../../tooling/agent-experiments/RUN-REVIEW.md). This is the owning builder's assessment, not an independent review and not permission to bypass a runtime gate.

- Study / owner / stages: verify-cost-qwen / dmarz / one chain of four stages. Batches `s0-002`, `p0-002`, `q0-002`, `s1-002`. Written 2026-10-04 by the builder, dmarz/pipeline-verify. Operator: dmarz/fleet-monitor.
- Parent attempt and its post-mortem (read before this was built): attempt 001, launch commit `ec0f1883`, source hash `72895482…`, [post-mortem](chain-001-post.md) by dmarz/pipeline, [records](../records/README.md). S0 144 of 144; P0 passed (663 input and 8 output tokens, provider Alibaba, cost reported, 0.35 tokens per request byte); Q0 24 of 24 valid, prose 10 of 12 and table 8 of 12 optimal against a threshold of 11 of 12 each; the chain stopped by itself at the gate; S1 not queued; 24 calls, USD 0.000504. Classified there as a capability failure of the answer-only configuration (cause suspected, not verified), not a format or instrument defect. [The attempt-001 pre-run review](chain-001-pre.md) is unchanged and remains its record.
- Status: **ready for dmarz/fleet-monitor's same-researcher check**. The repair itself was approved by dmarz/fleet-monitor (as relayed to this builder by dmarz/pipeline). Still required before a call: that check of this package, the run-queue request, and the launcher's `setup` passing on a fresh server at the launch commit. The builder launches nothing.
- Authority and review status (as relayed to this builder by dmarz/pipeline): dmarz directed this program himself (research program v5, written with him by a Codex session on 2026-10-04; his instruction to ship it was relayed by dmarz/fleet-monitor). The design is the program's; this package implements line V as specified there, including its one bounded repair after a failed qualification. Cross-researcher review is waived by dmarz for these exploratory runs; dmarz/fleet-monitor's check is a same-researcher check and nothing more; the run is not independently reviewed. This assessment is written by the agent that built the package.
- **Code commit (the pin of the code): `35404c241a713cb58bc216eb518f85fbfdc7c1f5`. Source hash: `ef40246d5f7790898ed120146d9c873c7af2fe70bd2aed4ad4c8e6eea0970fd1`** (`study.source_hash()` over `design.yaml`, `experiment.yaml`, `requirements.txt` and the eleven `src/*.py` files; the same value is in [READY.yaml](../READY.yaml), which names this file as `review:`). Documents are outside the hash.
- **Launch commit:** the commit named in the run request: the first commit on main that contains this review and READY.yaml with this source hash.
- **Manifest digest:** `a15437304ab34e3af4c0a137b3d1af0f05a6bfccfd0e8c8b8d8b4b4a4236b1cc` ([manifest.json](../manifest.json), attempt `002`, qualification set `b`; regenerates identically).

## Said up front, before the repeat (preregistration, section "Attempt 002")

1. The repair was chosen after reading the attempt-001 misses (the post-mortem read all 24 requests and answers).
2. The model is the same and reasoning stays disabled at the provider. What changes is the answer: `{"cost_if_inspect": {"<first allowed cell>": <number>, "<second allowed cell>": <number>}, "inspect": "<cell>"}`, one added instruction sentence in the system message and the matching ANSWER block. So this attempt tests whether writing intermediate values inside the answer rescues the one-step failure.
3. S1 then measures the table-versus-prose contrast for a model that writes out its costs. It may be at ceiling in both representations; a contrast near zero is then the result.
4. This is the only repair. A failed repeat ends the line. Attempt 001's stop stands as a result either way and is never pooled with attempt 002.

## What changed from attempt 001, and what did not

| Item | Attempt 001 | Attempt 002 |
|---|---|---|
| System message | choose; answer `{"inspect": "<row>,<column>"}` | one added sentence ("Before choosing, write the expected total cost of the final map for each of the two allowed actions, then choose.") and the new shape, `cost_if_inspect` before `inspect` |
| ANSWER block of the user message | the two literal one-key objects | "First write the expected total cost of the final map for each allowed action, then your choice. Reply with one JSON object of exactly this form: `{"cost_if_inspect": {"a": <number>, "b": <number>}, "inspect": "<cell>"}` where `<cell>` is a or b." |
| Everything before the ANSWER block (map, evidence, decision, objective, consequences in both representations) | — | byte-identical: a selftest compares digests frozen from the attempt-001 code at `fa61358a` for all 576 main requests, both qualification sets and the engineering requests |
| Qualification fixtures | set a, layouts 2800 to 2811 | set b, layouts 2900 to 2911, exactly as frozen in attempt 001's design (same digest) |
| Thresholds | 24 valid, ≥ 11 of 12 optimal per representation | unchanged |
| Grading | `inspect` against the analytic optimum | unchanged; the written costs are reported and never gated |
| Validation | exactly the key `inspect`, exact cell string | decided in advance, below |
| Main layouts, cases, representations, analysis, missing-data rule | — | unchanged |
| Model and request body | `qwen/qwen3.7-flash`, Alibaba, reasoning disabled, JSON-object mode, `max_tokens` 1,000 | unchanged |
| Adapter | reference adapter `639e9501` | unchanged (same file, SHA-256 `2e98d517…`) |
| Ledger study cap | 624 (room for this repair) | 600, fresh ledger on a fresh server; 760 transport attempts |
| `max_visible_chars` | 400 | 4,000 (a verbose but complete answer is not a failure) |
| Hub metrics | — | plus `work_malformed`, `choice_contradicts_own_costs` |

## Validation, decided in advance

For every rule the question was whether a harmless variant of a correct answer would fail it (lesson from the flagship's stop on a harmless extra item).

- Valid: the returned text parses as one JSON object and `inspect` is a string naming one of the two allowed cells after trimming whitespace and removing spaces around the comma.
- Tolerated, recorded per row, never a failure: costs as numeric strings, as integers, with more decimals; cost keys with spaces around the comma; a missing, partial, non-numeric or non-object `cost_if_inspect` (`work_malformed`, the choice is still graded); extra keys at the top level or in the cost object; `inspect` before `cost_if_inspect` (the returned object is stored as JSON text, so its key order survives storage and regrading); an `inspect` value that needed trimming; pretty-printed JSON.
- Invalid: text that is not JSON; JSON followed by text; JSON in a code fence; a JSON array or string; a missing `inspect`; `inspect` naming another cell, an action word, both cells, a non-string or null; a repeated key anywhere in the object (the adapter's rule: this covers duplicate `inspect` and a cost object naming one cell twice); output cut off at the limit; more than 4,000 characters.
- Two of the invalid forms could be called harmless and were decided on purpose: fenced or trailing-text JSON (the adapter parses the whole text and is taken unchanged; the route is in JSON-object mode and all 24 attempt-001 answers were bare objects), and a repeated cost key (adapter rule). Both are stated in the preregistration.
- Offline evidence: `rehearse.tolerated_variants` (13 forms) and `rehearse.invalid_forms` (13 forms) are each sent through the adapter and the validator in the selftest: all 13 tolerated forms are valid, graded optimal and counted; all 13 invalid forms fail with `invalid_json` or `invalid_answer` and keep the returned text. Rehearsal chain (f) runs all four stages on a stub that cycles through the 13 tolerated forms: 600 of 600 calls valid, 0 failed, regret 0, 176 rows counted `work_malformed`, `verify` exit 0.

## The written costs (reported, never gated)

Per valid row: the two written costs, the absolute error of each against the analytic expected cost (U for inspecting the reported cell, e for the cell without evidence), whether both are within 0.005, which action the model's own numbers favour, and whether the choice contradicts them. Per representation and overall in `analysis.json` `work` and `summary.json` `work`: rows with both costs written, both correct, mean absolute errors, contradictions, own numbers favouring the optimum, and counts of each tolerated variant. A selftest shows the gate ignores them: a qualification set with every cost wrong and every choice optimal passes; correct costs followed by the dearer action is a graded miss and a counted contradiction.

## Question, design and precision

Unchanged from [chain-001-pre.md](chain-001-pre.md) except for the actor configuration: 24 layouts × 12 cases × 2 representations = 576 S1 calls; primary: per-layout mean table-minus-prose expected regret, 24 paired values, predicted negative, practical marker 0.03, bound ±0.3208; all twelve strata and the reliable-source regression flag reported; offline comparators always-check 0.1500 and always-explore 0.1708; units are layouts, not calls; missing units bounded in [0, |e − U|] and never dropped. The run is uninformative about the contrast if qualification fails again (that ends the line and is itself the result) or if both representations sit at regret 0 (reported as a ceiling). Gate misclassification is as before: a solver right 95% of the time on clear-dominance choices passes with probability about 0.78.

## Frozen execution

- Model settings: `qwen/qwen3.7-flash` via OpenRouter; body exactly `model`, `provider {only: [alibaba], allow_fallbacks: false, require_parameters: true}`, `reasoning {enabled: false}`, `max_tokens: 1000`, `response_format {type: json_object}`, `messages`. `effort: low` in READY.yaml is only the launcher's required field.
- Call counts and hard caps: S0 0, P0 1, Q0 23, S1 576; `max_attempted_calls` 600; `max_transport_attempts` 760; `max_failed` 6.
- Gates and what happens at each failed gate:

| Stage | Assignments | Gate | On failure |
|---|---|---|---|
| S0 | 144 scripted rows | every row valid; analytic policy passes both sets; 0 invariant violations | chain stops; nothing paid |
| P0 | 1 (`qb-2900-e92-u08-prose`) | response parses; model slug and named provider match; usage reported; finish reason `stop`; no reasoning tokens; valid answer | chain stops after one call |
| Q0 | 23 (set b) | 24 of 24 valid and ≥ 11 of 12 optimal per representation, over P0's row and Q0's rows; only `inspect` graded | chain stops with `gate_failed`; S1 never queued; **the line ends** |
| before S1 | — | 576 × Q0's mean cost per call ≤ remaining cap; P0's tokens per content byte × 2,258 bytes ≤ 8,000 tokens | `projection_exceeds_cap` or `input_ceiling_projection`; no S1 call |
| S1 | 576 | ends `done` with at most 6 failed calls and no stop | `failed_units_over_limit`, `integrity_failure`, or `provider_credit_balance_low` (resumable as `s1-002-r1`) |

- Failure handling: part 1 adopted (status, body, request id kept); part 2 not applicable (no token-counting endpoint); part 3 adopted, `max_failed` 6; part 4 adopted, billing schedule 60 s re-sends for up to 1,200 s, then `provider_credit_balance_low`, `chain.py resume`, voided reservations, standing S1 reservations never above 576.
- Input ceiling: largest request body 2,598 bytes (2,258 bytes of content), `max_input_bytes` 6,000. At attempt 001's measured 0.35 tokens per request byte the largest request is about 800 input tokens against the 8,000 ceiling.
- Cost at the snapshot prices (USD 0.03 input, 0.13 output per million): about 800 input tokens and 40 to 80 output tokens per call: 24 + 5 to 10 = about 29 to 34 millionths; 600 calls: **about USD 0.02**. Reservation per call: 10 × (2,598 × 0.03 + 1,000 × 0.13) = 2,079 millionths = USD 0.0021; four open at once USD 0.0083; every call at its full reservation 600 × 0.0021 = USD 1.25, under the USD 2 cap. Dollars are not the gate; the call caps are.
- Wall time: attempt 001 measured 0.65 to 1.0 s per call at 8 output tokens; with 40 to 80 output tokens expect 1 to 4 s: S1 576 ÷ 4 × 1 to 4 s = about 2.5 to 10 minutes; chain about 3 to 12 minutes. Timeouts unchanged: request 120 s, stage 5,400 s, chain 7,200 s.
- Server and ledger: a fresh server with a fresh ledger and results directory (the study cap of 600 assumes no attempt-001 call in the ledger). The hub keeps attempt 001's three runs; the coordinator admits a stage only on a run with this attempt's source hash, and no batch name repeats.
- Stop rules: no answer retries, no replacement runs, no change of sample, thresholds or cases; S2 disabled; task ids below 10000; no further attempt.

## Offline evidence (builder's own runs, 2026-10-04, local Python 3.9.6, no network, no model call), at code commit `35404c24`

- `python3 src/selftest.py`: `Ran 87 tests`, `OK` (55 of this study, 32 of the reference adapter).
- `python3 src/worker.py --stage S0 --attempt s0-002`: planned 144, graded 144, invalid 0, model_calls 0, qualification_passed 1, invariant_violations [].
- `python3 src/manifest.py --check`: current, digest as above.
- `python3 src/rehearse.py --hub-dir <local hub copy>`: `ok true`, 37 of 37 checks, 94 s, six chains on throwaway hubs at 127.0.0.1 with a stub in the OpenRouter response shape that computes both costs from the request text: (a) full chain 0 / 1 / 23 / 576 calls, all costs correct, `verify` 0; (b) always-first stub: stop at Q0, exit 3, no S1 run; (c) billing pause on the probe and one HTTP 500 in S1: S1 done with 1 failed unit, bounds reported, `verify` 0; (d) every S1 call fails: stop at 9 failed, `failed_units_over_limit`; (e) billing stop after 40 S1 calls, 4 reservations voided, `resume` completes 536 units as `s1-002-r1`, ledger S1 exactly 576, `verify` 0; (f) mixed tolerated variants: all valid and graded, `verify` 0.
- Not tested locally: Python 3.12 (no PyYAML or Pillow for it here; the launcher's `setup` runs the selftest on the server).
- Seen live in attempt 001 and no longer unknown: the route's response shape (`provider: Alibaba`, `usage.cost` present, bare JSON in JSON-object mode, no reasoning tokens). Not seen: how this model formats a nested object with numbers; P0 is the first look, and the tolerated variants cover the likely forms.

## Changes and unresolved issues

| Issue / prior evidence | Chosen change | Alternative explanation | Acceptance check and result | Owner / stage it blocks |
|---|---|---|---|---|
| V-1 (post-mortem): 6 of 24 clear-dominance choices wrong with a one-key answer and reasoning disabled | the model writes both expected costs in the answer before choosing | the misses may come from something other than missing working space; then Q0 fails again and the line ends | attempt 002's Q0 gate | Q0 |
| A strict validator can void a correct action over a harmless extra item (flagship stop) | validation rules decided in advance; 13 tolerated forms, 13 invalid forms | — | selftest and rehearsal (f): pass | P0, Q0, S1 |
| Key order lost when rows are stored with sorted keys | the returned object is stored as JSON text and re-validated from it | — | found by rehearsal (f) failing `verify`; fixed; `verify` 0 | verify |
| Fenced or trailing-text JSON stays invalid (adapter parses the whole text) | none; decided in advance and stated | a model that fences its JSON fails P0 at the cost of one call | P0 | reported to dmarz/pipeline |
| After a billing pause longer than the request timeout the owner call has no transport-retry budget left (adapter behaviour) | none; reported earlier | tolerated in S1, fatal only in P0 or Q0 | — | reported |

## Visualization and closeout

- Mapping: [VISUALIZATION.md](../VISUALIZATION.md), v1, with one added text line for the written costs. Frames and replay as in attempt 001.
- Closeout: `status`, then `verify`; post-mortem per RUN-REVIEW.md with P0's raw metadata, the qualification table with every miss and its written costs, the written-cost report, and, if S1 runs, the per-stratum table, the primary with bounds and the regression flags. If Q0 fails, the post-mortem closes the line.
- Admission decision: none by the builder. Assessor: dmarz/pipeline-verify, 2026-10-04.
