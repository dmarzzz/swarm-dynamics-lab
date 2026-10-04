# Can successors repair inherited false memory? (Qwen3.7 Flash)

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by dmarz/pipeline-memory; source `9781739c` ([registry](../../../evidence-metadata.json), [rubric](../../../EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **2/4** — A Qwen3.7 Flash successor (reasoning disabled, answer with working fields) that is handed the contents of the records its inherited notes cite does not repeat a misquoted inherited value, where resolving only origin and version leaves it in place, and it keeps its clean-memory answers. Basis: One complete exploratory run after one preregistered repair: 24 roots, 576/576 S1 outcomes valid, 573 supported; primary contrast -0.5 in all 24 roots (the reference value, which follows by construction once the model adheres to the stated policy); clean completion 24/24 under raw, metadata-only and content-bound. Attempt 001 (answer-only format) failed qualification 19/24 on other fixtures. One synthetic task, one handoff, one model configuration, not independently reviewed.
- **sample_size_summary:** Observed: 24 independent roots x 6 memory states x 4 handoff policies = 576/576 valid S1 outcomes (394 distinct messages), attempt 002; qualification 24/24 on 6 roots. Attempt 001: qualification 19/24 on 6 other roots, S1 not run. Roots are the units, not calls; attempts are never pooled.
<!-- experiment-evidence:end -->

**Status, 2026-10-04.** Three chains have run and the line is complete; results are in [RESULTS.md](RESULTS.md). Attempt 001 (answer-only format) stopped at the qualification gate: 24 of 24 valid, 19 of 24 in agreement with the reference; S1 did not run ([post-mortem](reviews/chain-001-post.md)). Attempt 002, the one repair the program allows (same model with reasoning disabled, the second fixture set, the same gate, an answer format in which the successor first lists the records it relies on), passed qualification 24 of 24 and completed S1: 576 of 576 valid, 573 supported, primary contrast −0.5 in all 24 roots, which is the reference value and follows by construction once the model adheres to the stated policy ([post-mortem](reviews/chain-002-post.md), [records](records/attempt-002/)). Chain 003, the second pre-registered model `gpt-6-luna` on attempt 001's unchanged instrument (the same system message, answer format and 24 qualification requests), passed qualification 24 of 24 where Qwen without reasoning had scored 19, and completed S1 with 576 of 576 supported and the same −0.5 in all 24 roots ([pre-run review](reviews/chain-003-pre.md), [post-mortem](reviews/chain-003-post.md), [records](records/chain-003/)). The chains are never pooled. Exploratory; owner dmarz; built by dmarz/pipeline-memory.

It implements line M of [research program v5](../overnight-program-2026-10-04/program.json) ([setup record of the program](../overnight-program-2026-10-04/SETUP.md), [methods review](../overnight-program-2026-10-04/methods-review-v5.json), [selected model](../overnight-program-2026-10-04/selected-model.json)) as one package under the [ready-chain contract](../pipeline/READY-CHAIN.md).

Review status and authority (2026-10-04, as relayed to this builder by dmarz/pipeline): dmarz directed this program himself (research program v5, written with him by a Codex session on 2026-10-04; his instruction to ship it was relayed by dmarz/fleet-monitor). The design is the program's; this package implements line M as specified there. Cross-researcher review is waived by dmarz for these exploratory runs; dmarz/fleet-monitor's check is a same-researcher check and nothing more; the run is not independently reviewed. It is not an accepted hypothesis and makes no novelty claim.

## TLDR

A predecessor agent leaves notes; a fresh successor has to answer one question from them. Earlier diagnostics on this instrument ([discussion benchmark v3](../discussion-dose/benchmark-v3/README.md)) found that Haiku, Sonnet and Opus all repeated a false inherited fact in 6 of 6 fixtures when the only memory they were given supported it. This study asks what the handoff itself can do about that. The same inherited notes are handed over in four ways: as they are (raw), with the cited records' origin and version looked up (metadata-only), with the cited records and their current versions retrieved in full (content-bound), or not at all (reset). The notes are in one of six states: clean, a misquoted genuine source, a stale version, copies presented as independent reports, an equal-authority contradiction, or a source that is itself false. 24 roots × 6 states × 4 policies = 576 calls of `qwen/qwen3.7-flash`, one fresh successor per call, after a scripted stage and a 24-call qualification. The primary measure is how often the successor repeats the inherited false value under content-bound retrieval minus under metadata-only resolution, on the misquoted and stale states. Retrieval gives the successor more information by design, so this compares protocols, not wordings. A source that is false stays false when it is retrieved: the evaluator's truth is never handed to the successor. The result covers one handoff, one synthetic task and one model; it says nothing about several generations of handoffs.

## Question and prediction

Does binding inherited claims to the contents of their original sources repair false or stale memory without erasing useful knowledge?

Primary contrast (the program's): inherited-error probability under content-bound retrieval minus under metadata-only resolution, averaging the misquoted-source and stale-version states equally within each root. 24 root-level values.

What the rules alone imply, written before any outcome exists: a successor that follows the stated source policy exactly repeats the false value under metadata-only resolution in the misquoted state (the registry cannot show a misquote) and abstains in the stale state (the registry shows that a newer version exists but not what it says), and answers correctly in both under content-bound retrieval. That gives a contrast of −0.5 in every root. The model is free to depart from this in both directions: toward 0 if it keeps the note's value although the retrieved record says otherwise, toward −1 if it keeps a superseded value under metadata-only resolution. This reading of the program's question is the builder's; the program itself states no numeric prediction. A contrast near 0, or a loss of clean-memory answers under content-bound retrieval, is a valid result and triggers no tuning or rerun.

Anchors, all measured earlier and none of them an outcome of this study: in the discussion benchmark's fixed parent-memory fixtures Haiku 4.5, Sonnet and Opus 5.5 each gave a locally supported, ground-truth-wrong answer on 6 of 6 inherited-false fixtures; correlated copies were handled correctly in 0, 1 and 3 of 6 ([D1](../discussion-dose/benchmark-v3/RESULTS-D1.md), [D1 Opus](../discussion-dose/d1-opus/RESULTS.md)). Those runs used other models and a single handoff form (memory plus an origin catalog). None of them qualifies Qwen.

## Setup

- **Source instrument.** The parent-memory part of discussion benchmark v3: the public source policy and resolver (latest version within an origin, primary over secondary, equal-rank conflicts unresolved, a minimum number of distinct origins), the successor's answer format `{"value", "sources"}`, the scorer that separates source-supported answers from ground-truth-correct ones, the hash-chained journal and the replay page. They are copied into this study's `src/` with the hashes of the originals recorded in [design.yaml](design.yaml); nothing under `discussion-dose/` is edited.
- **Task.** Each root is a small fictional world of one of the three existing task families (capacity, total cost, dependency; 8 roots each, family = root mod 3). The successor is asked for one fact (`<option>.<field>`, for example `B.power`) plus a small integer `delta`, or `null` if the fact is unresolved. Hidden per root: the true value T, one false value F, delta, three other facts.
- **Inherited memory.** Four notes: three clean notes about the three other facts (identical in every state of the root) and one target note. A note is `{key, value, sources}`: a claimed value and the IDs of the records it cites. The six states differ only in the target note and in what the cited records really are:

  | State | Target note(s) | What the source store really holds |
  |---|---|---|
  | clean | T, cites record A | A (current, primary) says T |
  | misquote | F, cites A | A says T: the note misquotes a genuine source |
  | stale | F, cites A | A is version 1 and said F; the current version 2 of the same origin says T |
  | copies | F, cites A, C2, C3; the task requires 2 distinct origins | all three records are one origin and say F; presented as three reports |
  | contradiction | T citing A, and F citing B | A says T, B says F, both primary and current |
  | false original | F, cites A | A (current, primary) genuinely says F |

- **Handoff policies.** The successor's message always has the same four parts: `task`, `inherited_memory`, `source_registry`, `retrieved_records`. The policy decides what the protocol puts into them; no part names the policy or the state.

  | Policy | inherited_memory | source_registry | retrieved_records |
  |---|---|---|---|
  | raw | the four notes | empty | empty |
  | metadata | the four notes | origin, authority, version and current version of every cited record | empty |
  | content | the four notes | as metadata | every cited record in full, plus the current version of its origin when the cited one is superseded |
  | reset | empty | empty | empty |

- **Reference answer.** A scripted reference actor applies the stated source policy to exactly what the message contains (it never sees T, the state or the policy). Its answers, also written out by hand in `design.yaml` and checked against each other in S0:

  | State | raw | metadata | content | reset |
  |---|---|---|---|---|
  | clean | T | T | T | null |
  | misquote | F | F | T | null |
  | stale | F | null | T | null |
  | copies | F | null | null | null |
  | contradiction | null | null | null | null |
  | false original | F | F | F | null |

- **Roots.** S1 5401 to 5424 (24), engineering 5301 to 5306, qualification set a 5501 to 5506, qualification set b 5601 to 5606. The generator is seeded with this study's own version string, so these numbers share nothing with other studies' task ids.
- **Successor.** `qwen/qwen3.7-flash` through OpenRouter, provider pinned to Alibaba, `allow_fallbacks: false`, `require_parameters: true`, reasoning disabled, JSON-object mode, `max_tokens` 1,000, no tools, no memory across calls, no answer retries. The request body is the program's frozen template plus `messages` (one system message, identical for all 600 calls, and one user message). The answer is validated locally on structure. In attempt 001 it was `{"value", "sources"}`; in attempt 002 the successor first lists the records it relies on (`records`, `counting_values`, `distinct_origins`) and then gives `value` and `sources`. Only `value` and `sources` are scored; the working fields are reported. Whether the cited IDs exist and support the value is scored, not validated, so an unsupported answer is a measured outcome and not a failed call. The harmless variants that attempt 002 tolerates and the forms that stay invalid are listed in the preregistration (A5). `effort: low` appears in `READY.yaml` only because the launcher requires the field; reasoning is disabled and effort does not apply.
- **Frozen files.** [design.yaml](design.yaml), [preregistration.md](preregistration.md), [manifest.json](manifest.json) (assignment ids and packet hashes per stage, and the reserved second qualification set). The source hash covers `design.yaml`, `experiment.yaml`, `requirements.txt` and `src/*.py`.

## Protocol

Four stages run as one chain on one server. Each stage is one hub run. A stage is queued only if the previous stage finished `done` at the same source hash with no invalid row and its gate passed. A failed stage stops the chain; nothing further is queued.

1. **S0, scripted, 0 calls.** The whole 6 × 4 grid on the six engineering roots (144 rows) and both qualification sets (24 + 24 rows), answered by the reference actor: 192 rows. S0 passes only if every row is valid, every reference answer equals the hand-written table, both qualification sets pass their own gate under the reference, and every invariant holds (listed in the preregistration; they include: the false-original content packet contains the false original and not the truth; no packet contains a state or policy label or an evaluator field; within a root and state the task and the notes are identical across raw, metadata and content; scripted control actors that trust memory, always abstain or ignore versions get the scores the design predicts for them).
2. **P0, 1 call.** The first of the 24 qualification fixtures. It passes if the interface works: the response parses, the model slug matches, the response names Alibaba as its provider, usage is reported, the finish reason is `stop`, no reasoning tokens are reported and the answer has valid structure. Its raw response metadata (model, provider, response id, finish reason, reasoning tokens, latency, reported cost, tokens, tokens per byte) is written to its summary and to the hub.
3. **Q0, 23 calls.** The other 23 qualification fixtures (set a in attempt 001, set b in attempt 002). The gate is evaluated over all 24 rows (Q0 reads P0's saved row from the results directory and checks its checksum against the hub): 24 of 24 valid and 24 of 24 in exact agreement with the reference (value equal, citations valid), including the null answers for unresolved conflict and missing evidence. No miss is allowed. A failed qualification stops the chain; it is reported, not retuned.
4. **S1, 576 calls.** 24 roots × 6 states × 4 policies, one stateless call per assignment in a seeded shuffled order, four requests in flight, no answer retries. A call without a valid answer is recorded as failed with its evidence and dispatch continues, up to 6 failed calls; an integrity failure or a seventh failed call stops dispatch.

Before S1 the chain applies two written projection rules from the measured qualification usage: cost (576 × measured cost per call must fit under what is left of the cap, else `projection_exceeds_cap`) and input size (measured tokens per byte × the largest S1 request must not exceed 8,000 tokens, else `input_ceiling_projection`).

Calls are capped in the ledger at 1 (P0), 23 (Q0) and 576 (S1), 600 per attempt; dollars at USD 2 of settled cost plus open reservations. Attempt 001 spent USD 0.0007 on 24 calls. Expected spend of attempt 002 is about USD 0.04 (arithmetic in its pre-run review).

The program allows one bounded repair of a failed qualification: a new attempt (`002`) on the second, disjoint fixture set b, with its own source hash and pre-run review, after the failing answers have been read. It is the only repair; a failed repeat ends the line; thresholds are never lowered.

Analysis: the unit is the root. All 24 roots stay in every analysis. A failed or not-started call keeps its place in its cell's denominator with outcome bounds 0 and 1; contrasts are reported as bounds over all 24 roots plus the complete-case estimate with its denominator. Nothing is dropped, imputed or re-run. With all primary cells observed, the estimate is the mean of the 24 root values with a 95% interval from 10,000 bootstrap draws over whole roots (seed 20261004); all 24 root values are listed.

Operator steps for the chain that is prepared next are in [RUN.md](RUN.md); the pre-run reviews are [reviews/chain-001-pre.md](reviews/chain-001-pre.md) (attempt 001), [reviews/chain-002-pre.md](reviews/chain-002-pre.md) (attempt 002) and [reviews/chain-003-pre.md](reviews/chain-003-pre.md) (gpt-6-luna); the visualization mapping is [VISUALIZATION.md](VISUALIZATION.md); gate status is in [SETUP.md](SETUP.md).

## Metrics

| Measure | Definition |
|---|---|
| **Inherited error (primary)** | The successor's value equals F + delta: it repeats the false value carried by the inherited memory. Primary estimand: content minus metadata, mean over the misquote and stale states within each root, 24 root values. |
| Clean-memory correct completion (utility guard) | In the clean state the value equals T + delta. Reported per policy with a 95% interval, and as paired differences content minus raw and content minus metadata. A guard, not a non-inferiority claim. |
| Cost of forgetting | Clean-memory correct completion under raw minus under reset, paired by root; abstention and inherited error under reset alongside. |
| Abstention | The value is null. Reported per cell, split into correct abstention (the reference is null) and unnecessary abstention (the reference has a value). |
| Source-supported | The value equals the reference and the citations are valid (cited records are among the supporting ones and cover the required number of origins). Separate from ground-truth correctness: in the false-original state a supported answer is wrong against the hidden truth. |
| Supported and wrong, unsupported and correct, unsupported and wrong | The four-way split of non-null answers by support and hidden-truth correctness, per cell. |
| Conflict, copies, false originals | Reported as their own rows for all four policies; never pooled into the primary. |
| Retrieval | Per call and per policy: registry lookups, records retrieved, bytes added to the message, and the measured time of the lookup. Deterministic except the time. |
| Usage | Calls, transport attempts, input and output tokens, dollars, failed and not-started units, billing pauses. |

## Dated implementation notes (2026-10-04, before any run)

- **Ready-chain instead of five sessions.** The program's five-session arrangement with one shared reservation authority is replaced by the ready-chain: one package per line, one server per line, its own ledger and caps, launched by the orchestrator from the private run queue. The program's design for line M (sample, states, policies, primary, qualification rule, call counts) is implemented as written.
- **Stage mapping.** The program's 24 qualification calls are P0 (the first fixture, 1 call) plus Q0 (23 calls); the gate reads all 24 rows. `max_calls` is `{S0: 0, P0: 1, Q0: 23, S1: 576}`.
- **Inherited error is defined on the value.** The program names an "inherited-error probability" without a formula. It is frozen here as: the answer equals F + delta. The benchmark's older label `parent_inherited_error` (a wrong answer that the visible packet supports) is reported separately as "supported and wrong", because under metadata-only resolution in the stale state a repeated stale value is an inherited error that the packet does not support.
- **The copies state carries a two-origin requirement.** Copies matter only when corroboration is required. As in the benchmark's correlated-copies fixtures, the copies state sets `min_origins` to 2 in its task; the other five states use 1. The requirement is the same under all four policies of that state, so every policy contrast is at a fixed task rule. The copies state is not part of the primary contrast or the utility guard.
- **Some cells have identical packets by construction.** Under raw inheritance the misquote, stale and false-original states of a root are the same message (that is what raw inheritance means: the error is invisible); under metadata-only resolution the misquote and false-original states are the same message; under reset five of the six states are the same message, and two roots that ask for the same fact with the same delta share it. The 576 S1 assignments hold 394 distinct messages (raw 96, metadata 120, content 144, reset 34). The manifest records the hashes; identical messages are repeated calls, not extra worlds.
- **No token-counting endpoint.** Part 2 of the failure-handling rule (token counting never fails a call) does not apply: this route has no counting request. The ledger reserves a byte-based upper bound instead (input tokens ≤ bytes of the encoded request).
- **What the design can and cannot show.** The qualification demands exact agreement with the reference on all 24 fixtures. A model that passes is expected to sit near the reference in S1, where the primary contrast is −0.5 by construction. S1 then measures how reliably the successor follows each protocol on 24 fresh roots per cell, and whether clean answers survive; it is not a search for an unknown effect size. This establishes at most one-handoff behaviour, not a multi-generation result.
- **What a message looks like** (root 5401, stale state, content-bound policy; the successor's whole user message). The reference answer is 43 citing `rec-dzreyblo` (40 + delta 3); the note's stale value would give 51.

  ```
  {
  "task": {"key": "B.freight", "delta": 3, "min_origins": 1, "question": "Report the value of the exact fact key plus delta, or null if the fact is unresolved."},
  "inherited_memory": [
  {"key": "A.freight", "value": 75, "sources": ["rec-jwzchbft"]},
  {"key": "C.base", "value": 90, "sources": ["rec-hiffjaej"]},
  {"key": "B.freight", "value": 48, "sources": ["rec-gdcncbmm"]},
  {"key": "C.freight", "value": 65, "sources": ["rec-itvfwgue"]}
  ],
  "source_registry": [
  {"id": "rec-jwzchbft", "origin": "org-xcfsyedj", "authority": "primary", "version": 1, "current_version": 1},
  {"id": "rec-hiffjaej", "origin": "org-dabooxqr", "authority": "primary", "version": 1, "current_version": 1},
  {"id": "rec-gdcncbmm", "origin": "org-vjxpamjd", "authority": "primary", "version": 1, "current_version": 2},
  {"id": "rec-itvfwgue", "origin": "org-vylowinl", "authority": "primary", "version": 1, "current_version": 1}
  ],
  "retrieved_records": [
  {"id": "rec-jwzchbft", "origin": "org-xcfsyedj", "authority": "primary", "version": 1, "facts": {"A.freight": 75}},
  {"id": "rec-hiffjaej", "origin": "org-dabooxqr", "authority": "primary", "version": 1, "facts": {"C.base": 90}},
  {"id": "rec-gdcncbmm", "origin": "org-vjxpamjd", "authority": "primary", "version": 1, "facts": {"B.freight": 48}},
  {"id": "rec-dzreyblo", "origin": "org-vjxpamjd", "authority": "primary", "version": 2, "facts": {"B.freight": 40}},
  {"id": "rec-itvfwgue", "origin": "org-vylowinl", "authority": "primary", "version": 1, "facts": {"C.freight": 65}}
  ]
  }
  ```
- **Changes made while the package was built** (structural validation, the adapter revision, probe metadata, the exact-retrieval invariant) are listed at the end of the [preregistration](preregistration.md).
- **Second model (2026-10-04).** `gpt-6-luna` through the OpenAI API (`reasoning_effort: low`, 1,500 completion tokens including reasoning, JSON-object mode) is a second pre-registered model with its own chain: its own batches, probe, qualification, ledger (cap USD 5) and results, never pooled with the Qwen attempts. It gets attempt 001's instrument unchanged and qualifies on the 24 messages Qwen answered in attempt 001 (preregistration, sections "Second model" and its amendment). The successor paragraph of Setup above describes the Qwen route; for gpt-6-luna the request body is `model`, `reasoning_effort`, `max_completion_tokens`, `response_format`, `messages`.
