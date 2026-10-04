# Pre-run assessment for memory-handoff-qwen, chain 001 (S0, P0, Q0, S1)

Follows [the review cycle](../../../../../tooling/agent-experiments/RUN-REVIEW.md) and the [ready-chain contract](../../pipeline/READY-CHAIN.md). This is the owning builder's assessment, written 2026-10-04 by dmarz/pipeline-memory. It is not an independent review and it launches nothing. Nothing has run: no stage on a server, no model call.

- Study / owner / stage / attempt / parent: memory-handoff-qwen / dmarz / S0, P0, Q0 and S1 as one chain / attempt 001 / no parent attempt. Line M of [research program v5](../../overnight-program-2026-10-04/program.json).
- Status: **ready for the fleet monitor's same-researcher check**, then the private run queue. Not launched by this builder.
- **Pinned code commit: `b699012283655d0a749c2cc4991ee9e22b8e52c4`. Source hash: `b4ab9025e2288c7c7f652e7d210371ab7818022acc1ee155801e4300b5044ba3`.** The hash covers `design.yaml`, `experiment.yaml`, `requirements.txt` and `src/*.py`; `READY.yaml`, `README.md`, `preregistration.md`, `SETUP.md`, `RUN.md`, `VISUALIZATION.md`, `manifest.json` and this review are outside it, so the commit that adds this review has the same source hash. The run request names the first commit on main that contains this review.
- Manifest digest: `c11aba23be85689f89245f7674ec108fefa89ed9ea4d8f112eb08cc15a067e3b` ([manifest.json](../manifest.json), 78,784 bytes, regenerates identically).
- Previous post-mortem: none; this is the first attempt of this study. Read instead: the parent instrument's parent-memory results ([D1](../../discussion-dose/benchmark-v3/RESULTS-D1.md), [D1 Opus](../../discussion-dose/d1-opus/RESULTS.md)) and the [cross-lane lessons](../../pipeline/LESSONS.md).
- Plan: [README](../README.md), [preregistration](../preregistration.md) (first version `bee94550`, before any code; dated changes at its end), [design.yaml](../design.yaml).
- Review status and authority, as relayed to this builder by dmarz/pipeline on 2026-10-04: dmarz directed this program himself (research program v5, written with him by a Codex session on 2026-10-04; his instruction to ship it was relayed by dmarz/fleet-monitor). The design is the program's; this package implements line M as specified there. Cross-researcher review is waived by dmarz for these exploratory runs; dmarz/fleet-monitor's check is a same-researcher check and nothing more; the run is not independently reviewed. Implementation note of the same date: the program's five-session and shared-reservation arrangement is replaced by the ready-chain (one package per line, one server per line, its own ledger and caps, launched by the orchestrator from the private run queue).

## Question, design and precision

- Question: does binding inherited claims to the contents of their original sources repair false or stale memory without erasing useful knowledge? Primary contrast: inherited error (the successor's value equals the false inherited value plus delta) under content-bound retrieval minus under metadata-only resolution, mean of the misquote and stale states within each root; 24 root values. Guard: clean-memory correct completion per policy, with intervals. Reset measures the cost of forgetting. Contradiction, copies and false originals are reported separately, with source-supported answers kept apart from hidden-truth correctness.
- Claim boundary: one fresh successor and one handoff per assignment, one synthetic record-keeping task in three field families, one model configuration. It establishes at most one-handoff behaviour, not a multi-generation result.
- Prediction and uninformative outcomes: a rule-following successor gives −0.5 in every root (misquote −1, stale 0). Toward 0: the successor keeps the note's value although the retrieved record says otherwise. Toward −1: it keeps a superseded value under metadata-only resolution. See "What S0 passing does and does not show" below for the limit this puts on the study.
- Independent unit: the root (24). The 24 assignments of a root are dependent; calls are not samples. No power claim; no pilot variance for this model exists.
- Sample: 24 roots (8 per family) × 6 states × 4 policies = 576 S1 assignments in a seeded shuffled order. 394 distinct messages (raw 96, metadata 120, content 144, reset 34): raw inheritance hides the misquote, stale and false-original states from the successor by construction, metadata-only resolution cannot tell a misquote from a false original, and reset removes everything. Identical messages are repeated calls, not extra worlds.
- Splits: engineering roots 5301 to 5306 (S0 only); S1 roots 5401 to 5424; qualification set a 5501 to 5506 (P0 and Q0 of this attempt); qualification set b 5601 to 5606 (reserved for the one permitted repair, answered by the reference in S0 and listed in the manifest). The sets are pairwise disjoint (invariant `root_sets_disjoint`). Repository scan on 2026-10-04 at main `b6990122`: 3,850 text files under `researchers/`, `experiments/`, `tooling/`, `hypotheses/`, `tasks/`, `surveys/` and `synthesis/` searched for these 42 numbers next to the words root, world, task or seed; 0 exact matches outside this directory (the five-digit world ids 541xx of discussion-dose v3-opus share a prefix and nothing else). The generator is seeded with this study's own version string in any case.
- Manipulation fidelity: within a root and state, `task` and `inherited_memory` are byte-identical under raw, metadata and content, the registry is identical under metadata and content, and reset is empty (invariant `only_the_policy_changes_within_a_state`). Within a root, the requested fact, delta and the three other notes are identical in all six states (invariant `only_the_target_note_changes_within_a_root`). One stated exception: the copies state sets `min_origins` to 2, as the benchmark's correlated-copies fixtures do, because copies matter only when corroboration is required; it is the same under all four policies of that state and the copies state is in neither the primary contrast nor the guard. No message names a state or a policy (invariant `no_label_in_any_message`); the system message is one constant.
- Reference: the copied bench_v3 resolver applied to the visible message. Its answers equal the hand-written table of `design.yaml` in all 768 generated rows (576 S1 + 192 S0; invariant `reference_equals_hand_table`, selftest `test_reference_equals_the_hand_written_table_in_every_cell`). `resolve` and `strict_json` are textually identical to the bench_v3 files (selftest `test_copied_resolver_and_decoder_are_textually_identical_to_bench_v3`).
- Missingness: every failed or not-started call stays in its cell with outcome bounds 0 and 1; contrasts are bounds over all 24 roots plus the complete-case estimate with its denominator; nothing is dropped, imputed or re-run.

### Truth separation: what content-bound retrieval puts into the message

Content-bound retrieval reads the source store of the assignment's own state (`sim.state_world`) through `SourceStore.fetch` and `SourceStore.current`. It has no access to the evaluator's table: `sim.handoff` receives the store, and the hidden truth T enters a store only as the content of a genuine record of that state. T is the root's true value, F its false value; A, A2, B, C2, C3 are records; "other" means the three records of the three other notes, which are identical in every state.

| State | Records the content policy adds (retrieved_records) | Where each target value comes from | T in the message? |
|---|---|---|---|
| clean | A, other ×3 | A is the genuine current record and says T | yes: in the note and in A |
| misquote | A, other ×3 | A is the genuine current record and says T; the note says F | yes: in A only |
| stale | A (version 1), A2 (version 2, the current version of A's origin), other ×3 | A said F at version 1; A2 is the genuine current record and says T | yes: in A2 only |
| copies | A, C2, C3 (one origin), other ×3 | all three records say F; no record of this state says T | **no** |
| contradiction | A, B, other ×3 | A (primary) says T, B (primary, another origin) says F | yes: in the note citing A and in A |
| false original | A, other ×3 | A is the authoritative original and says F; no record of this state says T | **no** |

Metadata-only resolution adds registry entries (origin, authority, version, current version) for exactly the cited records and no values. Raw adds nothing. Reset passes nothing on.

Checks that prove it, all run offline:

- S0 invariant `false_original_is_retrieved_as_it_is` (32 packets: 24 S1 roots, 6 engineering roots, 2 qualification fixtures): the content packet of the false-original state holds exactly one record for the requested fact, it is A, its value is F, and neither T nor T + delta appears anywhere in the message.
- S0 invariant `no_truth_where_no_genuine_record_carries_it`: no message of the copies and false-original states under any policy, of the misquote and stale states under raw and metadata, or of any state under reset contains T or T + delta as a number. Record and origin IDs are letters only (invariant `ids_carry_no_digits`), so every number in a message is a value.
- S0 invariants `registry_is_exactly_the_cited_records` and `retrieved_is_exactly_cited_records_plus_current_versions_from_the_store`: the retrieved list is the cited records plus the current version of a superseded one, in that order, and each retrieved record equals the store's own record.
- Selftest `test_false_original_and_copies_never_show_the_truth` (all 42 roots × 4 policies): false original holds F and holds T nowhere; copies holds T nowhere; the reference answer on the false-original content packet is F + delta (supported and wrong: retrieval does not repair it).
- Selftest `test_changing_the_hidden_truth_changes_no_truth_free_message` (counterfactual, 42 roots × 24 cells): moving T by 1,000 leaves all 672 messages of truth-free cells byte-identical and changes all 336 messages of cells where a genuine record or note carries T.
- Selftest `test_content_retrieval_returns_store_records_only`: every retrieved record equals the store record; the only retrieved record that no note cites is A2 in the stale state.
- Selftest `test_wire_level_every_request_sent_is_the_frozen_body_of_its_packet_and_nothing_else`: the 600 request bodies that actually left the adapter in a full chain equal, as a multiset, the frozen template plus the system message and the rendered packet of each assignment; no body contains an evaluator field or an assignment id; no truth-free request contains T or T + delta; the only headers are `Authorization` and `Content-Type`.

### What S0 passing does and does not show

Reference-actor cell means on the six engineering roots (inherited error; identical on the 24 S1 roots):

| State | raw | metadata | content | reset |
|---|---|---|---|---|
| clean | 0 | 0 | 0 | 0 |
| misquote | 1 | 1 | 0 | 0 |
| stale | 1 | 0 | 0 | 0 |
| copies | 1 | 0 | 0 | 0 |
| contradiction | 0 | 0 | 0 | 0 |
| false original | 1 | 1 | 1 | 0 |

Clean-memory correct completion under the reference: 1, 1, 1, 0 (raw, metadata, content, reset). Primary under the reference: −0.5 in every root, with zero spread.

The instrument is not at floor or ceiling by construction in the sense that it separates different successors (invariant `controls_score_as_designed`, selftest `test_scripted_controls_separate_and_the_primary_is_not_fixed_by_construction`): the reference actor scores −0.5, an actor that repeats the note whatever else it is given scores 0.0, an actor that ignores versions scores −1.0, an actor that always abstains scores 0.0 with clean completion 0, and an actor that answers another fact is graded unsupported.

The limit, stated plainly: the qualification requires exact agreement with the reference on 24 of 24 fixtures, and a successor that agrees with the reference produces −0.5 by construction. If Q0 passes, the expected S1 result is close to −0.5 with clean completion close to 1 under raw, metadata and content and 0 under reset; S1 then measures how reliably the model follows each protocol on 24 fresh roots per cell (576 calls against 24), not an unknown effect size. A departure in S1 from what Q0 showed would be the informative outcome. This follows from the program's frozen gate and sample; it is recorded here, not tuned away.

## Changes and unresolved issues

| Issue / prior evidence | Chosen change | Alternative explanation | Acceptance check and result | Owner / stage it blocks |
|---|---|---|---|---|
| Opus, Sonnet and Haiku inherited 6 of 6 locally supported false facts (D1) | This study: vary what the handoff supplies, keep the notes fixed | The earlier result is a property of having no other evidence, not of the model | Reference table and control actors behave as designed in S0 | none |
| Correlated copies were handled correctly in 0, 1 and 3 of 6 by Haiku, Sonnet, Opus | Copies state kept as the program requires; its two-origin rule is stated in the system message and in the task | Qwen may fail the copies fixtures in Q0 | Q0 gate; a failure is reported, the failing answers are read, at most one repair on set b | Q0 |
| An exact 24 of 24 gate misclassifies often (lessons, item 7): a successor right 97% of the time fails it about half the time | None: the program's gate is implemented as written | A Q0 stop may reflect one slip, not inability | Stop is reported with every miss's message and answer; thresholds are never lowered | Q0 |
| The first preregistration made unknown cited IDs and missing citations invalid answers | Validation is structural; citations are scored | none | Selftest `test_validate_is_structural_and_strict`, `test_scorer_known_answers` | none |
| A billing stop left reserved calls that a continuation could not re-reserve under the exact S1 cap | Reference adapter `639e9501`: the reservation of a billing-stopped call is voided | none | Selftest `test_billing_stop_fails_nothing_and_a_continuation_finishes_every_unit_once`: 576 answered, `calls_by_batch` `s1-001` = 576, one more call refused | none |
| Not verified against the live service: the wording of OpenRouter's credit error, whether `usage.cost` is reported, the spelling of `provider` | P0 is one call and records the raw response metadata | P0 may fail on `provider_missing` if the field is absent | P0 gate; the metadata is in the P0 summary and hub message either way | P0 |

Qualification is the most likely place for this chain to stop. The gate allows no miss in 24, and the fixtures include the null answers for unresolved conflict, superseded versions without content, copies of one origin and missing evidence. A stop there is a reported outcome, not a defect to retune.

## Frozen execution and collection

- Model settings: `qwen/qwen3.7-flash` through OpenRouter; request body exactly `model`, `provider {only: [alibaba], allow_fallbacks: false, require_parameters: true}`, `reasoning {enabled: false}`, `max_tokens: 1000`, `response_format {type: json_object}`, `messages` (one system message, one user message). No temperature, no tools, no fallback. Accepted response model: `qwen/qwen3.7-flash` or `qwen/qwen3.7-flash-20260727`; the response must name Alibaba as provider. Local validation of the answer; no answer retry. `effort: low` in `READY.yaml` exists only because the launcher requires the field.
- Adapter: `src/provider.py` is the reference adapter at main `639e9501`, unchanged (sha256 `2e98d517…`), with its 32 tests running in this study's selftest.
- Assignments and call counts:

  | Stage | Assignments | Model calls | Hard `max_calls` | Distinct messages |
  |---|---|---|---|---|
  | S0 | 192 (144 engineering + 24 + 24 qualification) | 0 | 0 | 144 |
  | P0 | 1 (qualification fixture 0: root 5501, clean, content) | 1 | 1 | 1 |
  | Q0 | 23 | 23 | 23 | 22 |
  | S1 | 576 | 576 | 576 | 394 |

  Total for this attempt 600. The ledger's study-wide cap is 624 so that the one permitted repair attempt's 24 qualification calls fit the same ledger; `READY.yaml` carries 600.
- Gates and what happens at each failed gate:
  - S0: 192 rows valid, both qualification sets 24 of 24 under the reference, 25 invariants. Failure: chain exits 3 with `invariant_failed:<names>` or `qualification_failed`; no paid call has been made.
  - P0: response parses, model slug matches, provider named and Alibaba, usage reported, finish reason `stop`, no reasoning tokens, valid structure. Failure: chain exits 3 after one call; the response metadata and, for an HTTP failure, the status and body are in the P0 summary.
  - Q0: 24 of 24 valid and supported over P0's saved row (read from the results directory, checksum compared with the hub) and Q0's 23 rows. Failure: chain exits 3 with `qualification_failed` (or `invalid_rows:<category>`, or `probe_row_unavailable` before any call); S1 is never queued; the summary names the missed fixtures.
  - Before S1: `projection_exceeds_cap` if 576 × the measured mean cost per call exceeds what is left of USD 2; `input_ceiling_projection` if the largest measured tokens per byte over the 24 qualification rows × 5,064 bytes (the largest S1 request) exceeds 8,000 tokens; `qualification_usage_missing` if neither was measured. Any of these exits 3 with nothing queued for S1.
  - Coordinator: each stage needs exactly one `done` run of the previous stage at this source hash with `invalid == 0` and `qualification_passed == 1`; a batch name is never queued twice.
- Failure handling (rule of 2026-10-04), one line each:
  - Part 1, adopted: a failed HTTP request keeps its status, the first 2,000 characters of the body and the request id; no request header or key is stored.
  - Part 2, not applicable: this route has no token-counting request; the reservation is a byte-based upper bound with a 10 times margin.
  - Part 3, adopted: S1 continues past failed calls up to `max_failed` = 6; integrity failures stop at once; S0, P0 and Q0 are strict.
  - Part 4, adopted: a billing or limit refusal pauses the stage and re-sends the same call every 60 s for up to 1,200 s; then `provider_credit_balance_low`, unfinished calls not started, reservations voided, `chain.py resume` queues `s1-001-r1`.
- Transport retry: at most 2 re-sends, only for HTTP 429, 502, 503 and 529, backoff 2 s then 6 s, `retry-after` honoured up to 20 s, inside the 120 s request timeout; at most 800 HTTP attempts for the study.
- Budget: USD 2 of settled cost plus open reservations (the program's per-study cap). Expected cost at the frozen prices (USD 0.03 and 0.13 per million input and output tokens): S1 requests average 3,829 bytes (raw 3,465, metadata 4,037, content 4,663, reset 3,150), of which 2,532 are the system message; at about 3 bytes per token that is about 1,300 input tokens, and an answer is about 25 tokens: 600 × (1,300 × 0.03 + 25 × 0.13) / 1,000,000 = USD 0.025. Worst realistic: every request counted at one token per byte at the largest size (5,068 bytes) with the full 1,000-token output: 600 × (5,068 × 0.03 + 1,000 × 0.13) / 1,000,000 = USD 0.169. Open reservations: at most 4 at once, each at most 10 × (5,068 × 0.03 + 130) / 1,000,000 = USD 0.0028. Spend to date: USD 0.
- Input ceiling: the largest request is 5,068 bytes, at most 2,027 tokens at the assumed worst case of 2.5 characters per token; the size limit is 16,000 bytes (6,400 tokens at that ratio); a response reporting more than 8,000 input tokens is an integrity failure.
- Time: 4 requests in flight; 120 s per request; 6,000 s per stage; 7,800 s for the chain. Expected wall time 5 to 15 minutes: 576 calls at a few seconds each with four in flight is 7 to 15 minutes; S0 takes about 1 s and the 24 qualification calls under a minute.
- Collected per row: assignment id, root, family, state, policy, packet hash, request bytes, evaluator labels, the reference answer, the answer, the evaluation, the adapter's accounting (attempts, tokens, reported and computed cost, response model, provider, response id, finish reason, latency, HTTP status and body on failure), the retrieval log (registry lookups, records retrieved, bytes, measured seconds), status and error. Per stage: `assignments.jsonl.gz` (every message), `episodes.jsonl.gz`, `events.jsonl.gz` (hash-chained journal), `summary.json`, `analysis.json`, frames, `replay.gif`, `replay.html`.
- Offline evidence at the pinned code (build machine, Python 3.9.6, macOS; no network, no model call):
  - `python3 src/selftest.py`: `Ran 85 tests` … `OK`, about 90 s. 53 study tests plus the 32 reference adapter tests.
  - `python3 src/worker.py --stage S0 --attempt offline-s0-001`: passed, 192 of 192 rows valid, 0 calls, both qualification sets 24 of 24 supported, 25 of 25 invariants, reference primary −0.5, control primaries −0.5, 0.0, −1.0, 0.0, 0.0.
  - `python3 src/manifest.py --check`: `manifest_matches: true`, digest `c11aba23…`, counts 192, 1, 23, 576.
  - `python3 src/rehearse.py --hub-dir <hub>`: passed, 35 of 35 checks in 73 s, five chains on throwaway local hubs with a stub in the OpenRouter response shape: (a) full chain exit 0, 600 stub calls, `verify` exit 0, replay of S0 refused; (b) failed qualification stops at Q0 with exit 3, state `stopped_at_gate`, no S1 run on the hub, 24 calls; (c) two credit errors on the probe then success (one pause of 120 s, nothing failed) and one HTTP 500 in S1 (S1 done with 1 failed call, bounds reported), `verify` exit 0; (d) every S1 call fails: dispatch stops after 9 failed calls with `failed_units_over_limit`, 567 not started; (e) credit errors from the 41st S1 call: stop with `provider_credit_balance_low` after 1,200 simulated seconds, 0 failed, 536 not started, 4 reservations voided; `chain resume` runs `s1-001-r1` with 536 assignments; 576 answered in total, every assignment exactly once, `verify` exit 0.
  - Not tested: Python 3.12, the real hub, the private launcher, a real response of the model or of OpenRouter's error paths.
- Credential: environment alias `SWARM_OPENROUTER_API_KEY`, set by the launcher in memory. No value appears in any file, argument or log of this package; a selftest scans the package for key and address patterns.
- Allocation: none yet. Claim id `dmarz-memory-handoff-qwen`; the server is a launcher parameter ([RUN.md](../RUN.md)).

## Visualization and closeout

- Mapping: [VISUALIZATION.md](../VISUALIZATION.md), v1, bound to this source hash. Live: `progress.png` at most every 20 s (the 6 × 4 grid of memory states by handoff policies, one square per assignment, plus the source-to-successor trace of the latest assignment). Final: `final_frame.png` with the primary contrast and the clean-completion counts. Replay: `replay.gif` (time-ordered, at most 25 frames) and `replay.html` (per assignment: sources, predecessor notes, handoff, answer, score). Failed and not-started assignments are drawn as such, never as abstentions. Scripted stages are labelled "SCRIPTED - NOT MODEL EVIDENCE".
- Stop rules: no answer retries, no replacement runs, no change of sample, thresholds, states or policies after outcomes are seen. A failed stage stops the chain and nothing further is queued. A failed qualification is reported with the message and answer of every miss; the one permitted repair is attempt 002 on fixture set b with a new source hash and its own pre-run review; a failed repeat ends the line. Null and adverse S1 results complete the study. S2 stays closed.
- Closeout: `status` and `verify` after the chain; a post-mortem per the review cycle reconciling assigned, started, terminal, graded and analyzed rows, comparing frames with `analysis.json`, and reporting actual calls, tokens and dollars; the evidence registry row is updated after analysis.
- Admission decision: ready for the same-researcher check. Assessor dmarz/pipeline-memory, 2026-10-04. Unresolved before launch: the fleet monitor's check, the queue entry, the server claim, the balance check. Exact next action on a failed gate: stop, keep every artifact, write the post-mortem; do not retune.
