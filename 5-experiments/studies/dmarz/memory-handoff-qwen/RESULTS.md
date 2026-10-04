# Results: can successors repair inherited false memory? (Qwen3.7 Flash and gpt-6-luna)

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by dmarz/pipeline-memory; source `9781739c` ([registry](../../../evidence-metadata.json), [rubric](../../../EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

**Can successors repair inherited false memory? (Qwen3.7 Flash)** (`memory-handoff-qwen`)

- **evidence_confidence:** **2/4** — A Qwen3.7 Flash successor (reasoning disabled, answer with working fields) that is handed the contents of the records its inherited notes cite does not repeat a misquoted inherited value, where resolving only origin and version leaves it in place, and it keeps its clean-memory answers. Basis: One complete exploratory run after one preregistered repair: 24 roots, 576/576 S1 outcomes valid, 573 supported; primary contrast -0.5 in all 24 roots (the reference value, which follows by construction once the model adheres to the stated policy); clean completion 24/24 under raw, metadata-only and content-bound. Attempt 001 (answer-only format) failed qualification 19/24 on other fixtures. One synthetic task, one handoff, one model configuration, not independently reviewed.
- **sample_size_summary:** Observed: 24 independent roots x 6 memory states x 4 handoff policies = 576/576 valid S1 outcomes (394 distinct messages), attempt 002; qualification 24/24 on 6 roots. Attempt 001: qualification 19/24 on 6 other roots, S1 not run. Roots are the units, not calls; attempts are never pooled.

**Can successors repair inherited false memory? (gpt-6-luna, chain 003)** (`memory-handoff-qwen-gpt-6-luna`)

- **evidence_confidence:** **2/4** — A gpt-6-luna successor (reasoning effort low, answer-only format) passes the unrepaired handoff instrument on the 24 requests where Qwen3.7 Flash without reasoning scored 19, and follows the stated source policy on fresh roots: content-bound retrieval removes the misquote and stale errors that metadata-only resolution leaves or turns into abstentions, with clean answers kept. Basis: One complete exploratory run: qualification 24/24 on identical requests (Qwen 19/24), S1 576/576 supported on 24 roots, primary contrast -0.5 in all 24 roots (the reference value, by construction given adherence), launcher verify clean. The instrument is at ceiling for this model; model and reasoning setting are confounded against Qwen; one synthetic task, one handoff, one run, not independently reviewed.
- **sample_size_summary:** Observed: 24 independent roots x 6 memory states x 4 handoff policies = 576/576 valid S1 outcomes (394 distinct messages); qualification 24/24 on 6 roots, the same 24 requests as Qwen attempt 001. Roots are the units, not calls; never pooled with the Qwen cohort.
<!-- experiment-evidence:end -->

Written 2026-10-04 by dmarz/pipeline-memory from the saved rows of the three chains that ran (two Qwen attempts and the gpt-6-luna chain; the gpt-6-luna section is at the end and the three-way summary is the next table). Exploratory; line M of [research program v5](../overnight-program-2026-10-04/program.json). Same-researcher check only; the runs are not independently reviewed.

Read this first, as the [preregistration](preregistration.md) says it (items 1 and A7): the qualification gate requires exact agreement with the reference on 24 of 24 fixtures, and a successor that agrees with the reference produces −0.5 on the primary contrast by construction. With the gate passed, **S1 measures how reliably the model adheres to the reference on fresh roots**; it is not a search for an unknown effect size.

## What ran

| Attempt | Answer format | Qualification fixtures | P0 | Q0 gate (24 of 24 valid and supported) | S1 | Calls, cost |
|---|---|---|---|---|---|---|
| 001 | `{"value", "sources"}` | set a, roots 5501 to 5506 | passed | **failed**: 24 valid, 19 supported | not run | 24 calls, USD 0.0007 |
| 002 | working fields (`records`, `counting_values`, `distinct_origins`), then `value`, `sources` | set b, roots 5601 to 5606 | passed | **passed**: 24 valid, 24 supported | 576 of 576 valid, 0 failed | 600 calls, USD 0.0261 |
| chain 003, `gpt-6-luna`, reasoning effort low | `{"value", "sources"}`, attempt 001's instrument byte for byte | set a: the same 24 requests as attempt 001 | passed | **passed**: 24 valid, 24 supported | 576 of 576 valid, 0 failed, 576 supported | 600 calls, USD 0.0705 |

Attempts 001 and 002: `qwen/qwen3.7-flash` through OpenRouter, provider Alibaba, reasoning disabled (0 reasoning tokens reported on every call), 1,000 output tokens allowed. Attempt 001: launch commit `0d54225c`, source hash `b4ab9025…`, [post-mortem](reviews/chain-001-post.md), [records](records/README.md). Attempt 002: launch commit `5831e534`, source hash `10f51d2c…`, server sim-dmarz-13, operator dmarz/fleet-monitor, 12:40:28Z to 12:44:57Z; hub runs S0 `6e5badb7`, P0 `94e45249`, Q0 `43926309`, S1 `5a6fec17`; [post-mortem](reviews/chain-002-post.md), [records](records/attempt-002/).

The two attempts are never pooled. They differ in the answer format and in the fixture set: the working-fields repair turned a 19 of 24 qualification into 24 of 24 on this model, on a different set of 24 fixtures. That is two batches of 24, not a paired comparison, and one run of each.

## Primary contrast (attempt 002, S1)

Inherited error (the successor's value equals the false inherited value plus delta) under content-bound retrieval minus under metadata-only resolution, mean of the misquote and stale states within each root:

**−0.5 in every one of the 24 roots** (mean −0.5; 95% bootstrap interval −0.5 to −0.5 from 10,000 draws over roots, seed 20261004; 24 of 24 roots complete, no missing cell). The interval has no width because all 24 root values are identical. This is exactly the reference value.

By state: misquote −1.0 (metadata-only repeated the misquoted value in 24 of 24 roots, content-bound in 0 of 24); stale 0.0 (neither policy repeated the stale value: metadata-only abstained in 24 of 24, content-bound in 0 of 24 repeated it).

## Every cell (24 roots each; correct / inherited error / abstained / other wrong)

"Correct" is against the hidden truth. "Reference" is what the stated source policy gives from the message alone (T truth, F the false inherited value, null unresolved).

| Memory state | raw | metadata-only | content-bound | reset |
|---|---|---|---|---|
| clean | 24 / 0 / 0 / 0 (ref T) | 24 / 0 / 0 / 0 (ref T) | 24 / 0 / 0 / 0 (ref T) | 0 / 0 / 24 / 0 (ref null) |
| misquoted source | 0 / 24 / 0 / 0 (ref F) | 0 / 24 / 0 / 0 (ref F) | 24 / 0 / 0 / 0 (ref T) | 0 / 0 / 24 / 0 (ref null) |
| stale version | 0 / 24 / 0 / 0 (ref F) | 0 / 0 / 24 / 0 (ref null) | **21 / 0 / 3 / 0** (ref T) | 0 / 0 / 24 / 0 (ref null) |
| copies as independent | 0 / 24 / 0 / 0 (ref F) | 0 / 0 / 24 / 0 (ref null) | 0 / 0 / 24 / 0 (ref null) | 0 / 0 / 24 / 0 (ref null) |
| equal-authority contradiction | 0 / 0 / 24 / 0 (ref null) | 0 / 0 / 24 / 0 (ref null) | 0 / 0 / 24 / 0 (ref null) | 0 / 0 / 24 / 0 (ref null) |
| false original | 0 / 24 / 0 / 0 (ref F) | 0 / 24 / 0 / 0 (ref F) | 0 / 24 / 0 / 0 (ref F) | 0 / 0 / 24 / 0 (ref null) |

573 of 576 answers are supported (value equals the reference and citations valid; 99.5%, Wilson 95% interval 98.5 to 99.8%). No answer gave a value that was neither the truth nor the inherited value. The three unsupported answers are all in one cell, stale under content-bound retrieval (roots 5402, 5409, 5421): the successor abstained although the current version of the record was in its message. It never repeated the stale value there.

## Clean-memory utility guard

Correct completion in the clean state: raw 24 of 24, metadata-only 24 of 24, content-bound 24 of 24 (each Wilson 95% interval 86.2 to 100%), reset 0 of 24 (0 to 13.8%). Paired by root, content-bound minus raw is 0.0 and content-bound minus metadata-only is 0.0 in all 24 roots. Content-bound retrieval lost no clean answer in this run. With 24 roots the guard cannot exclude a loss rate below about 14%; it is a guard reported with its uncertainty, not a non-inferiority result.

## Reported separately

- **Copies presented as independent** (the task requires two distinct origins). Raw: the inherited value was accepted in 24 of 24 (as the reference says: without a registry the three citations are taken as presented). Metadata-only and content-bound: abstained in 24 of 24 each. Resolving origins is enough to stop this error; retrieval adds nothing; the truth is not recoverable because no record carries it.
- **Equal-authority contradiction.** Abstained in 24 of 24 under raw, metadata-only and content-bound. No policy resolves it and the successor did not pick a side. (In attempt 001's qualification the answer-only format picked one record in 2 of 3 such fixtures.)
- **False original.** Raw, metadata-only and content-bound: the false value was given in 24 of 24 each, and every one of those answers is supported by the message. Source-supported and wrong against the hidden truth in 72 of 72. Retrieval returned the false original as it is and, as designed, cannot repair it; the evaluator's truth was never in a message.
- **Reset, the cost of forgetting.** Abstained in 144 of 144; inherited error 0 of 144; clean-memory correct completion 0 of 24, against 24 of 24 under raw: the paired difference raw minus reset is 1.0 in every root. Reset removes every inherited error and every correct answer.
- **Other contrasts** (secondary, descriptive; all 24 roots identical in each): metadata-only minus raw on stale −1.0 and on copies −1.0; content-bound minus raw on misquote and stale −1.0; content-bound minus raw on false original 0.0.

Read as protocols: raw inheritance passes on four of the five kinds of bad memory; metadata-only resolution turns the stale and copied ones into abstentions and leaves the misquote and the false original; content-bound retrieval repairs the misquote (24 of 24) and most of the stale ones (21 of 24, Wilson 69.0 to 95.7%; the other 3 abstain) and leaves the false original; reset removes everything.

## Working fields (reported, never gated)

All 576 S1 answers carried the three working fields, well-formed, before `value` (no tolerated variant was needed: 0 integer-as-string or float, 0 repeated sources, 0 extra keys, 0 malformed).

| Check on the model's own working fields | S1 (576) | Q0 + P0 (24) |
|---|---|---|
| listed records match the message (IDs, values, current flags) | 570 | 24 |
| `value` follows from its own listing under the source policy | 573 | 24 |
| `counting_values` consistent with its own listing | 535 | 22 |
| `distinct_origins` consistent with its own listing | 553 | 23 |
| supported and follows from its own listing | 570 | 24 |
| unsupported although it follows from its own listing | 3 | 0 |

- The 6 listing mismatches are all stale under content-bound retrieval: the successor listed only the superseded record and left out the current version that was in its message. In 3 of them it abstained, consistently with its own incomplete listing (the 3 unsupported answers of the run); in the other 3 it still answered with the current record's value and cited it, so the answer is supported but does not follow from what it listed.
- The `counting_values` and `distinct_origins` disagreements (41 and 23 rows) sit almost entirely in the copies state under metadata-only and content-bound (31 and 20 rows): the successor listed the three records of one origin as current and then wrote an empty or one-element `counting_values`, or 1 where the instruction says 0 when no value is accepted. All of those answers are supported (null). The bookkeeping fields are less reliable than the answer.
- Identical messages: 72 messages were sent more than once (repeated cells by construction); in none of them did the scored answer differ between repeats.

## Usage

Attempt 002: 600 calls (1 + 23 + 576), 600 transport attempts, no retry, no failed call, no billing pause. 744,884 input and 54,401 output tokens; USD 0.026099 settled in the ledger (provider-reported cost on every call), cap USD 2. S1: 715,115 input and 52,200 output tokens, USD 0.025057, 225 s with four requests in flight, mean latency 1.46 s (maximum 4.77 s), at most 1,671 input and 200 output tokens per call, 0.262 tokens per request byte at most. Per policy (144 calls each): raw USD 0.0059, metadata-only USD 0.0068 (648 registry lookups, 71,568 bytes added), content-bound USD 0.0074 (648 lookups, 672 records retrieved, 149,128 bytes added), reset USD 0.0049. Retrieval is a deterministic lookup; its measured time is under 20 ms for the whole stage.

## Verification of these numbers

[records/attempt-002/recompute.py](records/attempt-002/recompute.py), run by the builder on 2026-10-04 against the package at the launch commit, recomputes the outcome class of every row from the saved answer and the evaluator labels alone, the primary and its interval, and every table above, and then checks: the saved `analysis.json` equals the pinned code's analysis of the saved rows; every saved answer validates and grades again to the saved evaluation, reference and working-field report (P0, Q0, S1); every packet regenerates and the assignment digests equal the manifest; the three journals' hash chains are intact with one terminal event per row; the qualification gate recomputes to 24 of 24. All 15 checks pass; output in [records/attempt-002/recomputed.json](records/attempt-002/recomputed.json). Not checked by the builder: the artifact checksums on the hub (that needs the hub; it is the launcher's `verify`), and the frames, which are not in the records.

## What this does and does not establish

- Established, narrowly: on this synthetic record-keeping task, a Qwen3.7 Flash successor with reasoning disabled that writes its working fields follows the stated source policy in 573 of 576 fresh assignments (24 roots × 24 cells). Given that adherence, handing over the contents of the cited records removes the misquote error that metadata-only resolution leaves in place, keeps every clean answer, and does not help against a source that is itself false.
- By construction, not discovered: the size of the primary contrast. The protocols differ in the information they supply; a rule-following successor must produce −0.5. The empirical content is the adherence rate, the stale-version cell (21 correct, 3 abstentions, 0 stale values), the clean guard and the working-field counts.
- Not established: that the working-field format is what made qualification pass. Attempt 001 (19 of 24, set a) and attempt 002 (24 of 24, set b) used different fixtures and are one run each. A model that is right 97% of the time fails a 24 of 24 gate about half the time; S1's observed 99.5% adherence corresponds to passing such a gate about 88% of the time (0.9948 to the power 24).
- Not established: anything about more than one handoff, about a successor that reasons, about real documents, or about another model. One model configuration, one synthetic task in three field families, 24 roots.
- The gpt-6-luna chain is reported in the next section; nothing above pools it with the Qwen attempts.

## Chain 003 (gpt-6-luna)

Run on 2026-10-04, 18:06:21Z to 18:10:27Z, server sim-dmarz-9, operator dmarz/fleet-monitor, launch commit `f717bb2d`, source hash `caf5d773…`, fresh ledger; hub runs S0 `343255be`, P0 `922c6ba3`, Q0 `93ab28b9`, S1 `0a901a43`. `gpt-6-luna` through the OpenAI API, `reasoning_effort: low`, 1,500 completion tokens allowed, JSON-object mode. [Pre-run review](reviews/chain-003-pre.md), [post-mortem](reviews/chain-003-post.md), [records](records/chain-003/). The launcher's `verify` exited 0 with every check true (saved in the records); the builder's recomputation from the rows passes 15 of 15 checks.

The same caveat as above applies and was pre-registered: with the 24 of 24 gate passed, S1 measures adherence to the reference; the primary value follows by construction.

### The line in three chains

| | Qwen attempt 001 | Qwen attempt 002 | gpt-6-luna chain 003 |
|---|---|---|---|
| Reasoning | disabled | disabled | low effort (reasoning tokens on 552 of 576 S1 calls, at most 91) |
| Answer format | value and sources | working fields, then value and sources | value and sources |
| Qualification requests | set a | set b | **set a, byte-identical to attempt 001's 24 requests** |
| Qualification | 24 valid, **19 supported**: stopped | 24 valid, **24 supported** | 24 valid, **24 supported** |
| S1 | not run | 576 valid, **573 supported** | 576 valid, **576 supported** |
| Primary contrast | n/a | −0.5 in 24 of 24 roots | −0.5 in 24 of 24 roots |
| Clean completion, raw / metadata / content / reset | n/a | 24 / 24 / 24 / 0 | 24 / 24 / 24 / 0 |
| Stale under content-bound | n/a | 21 correct, 3 abstained | 24 correct |

Each chain is one run. The chains are never pooled.

### Qualification on identical requests: gpt-6-luna against Qwen attempt 001

The 24 requests are the same messages (system message plus user message; the packet hashes of both runs equal the frozen attempt-001 manifest). Only the model and its reasoning setting differ, plus the provider's request template. Qwen: 19 of 24 supported. gpt-6-luna: 24 of 24. On the 19 fixtures Qwen got right, gpt-6-luna gave the same value. The five Qwen misses:

| Fixture | Reference | Qwen attempt 001 | gpt-6-luna |
|---|---|---|---|
| misquote, raw (`qa13`) | 94, cites the note's record | null | 94, cites it |
| stale, content (`qa02`) | 46, cites the current version | 40 (the superseded value), cites the current version | 46, cites it |
| copies, content (`qa03`) | null | 30, cites all three copies | null |
| contradiction, metadata (`qa10`) | null | 73, cites one record | null |
| contradiction, content (`qa04`) | null | 73, cites both records | null |

This is a like-for-like comparison on 24 fixtures, one run per model (19 of 24 against 24 of 24; Wilson 95% intervals 59.5 to 90.8% and 86.2 to 100%). It does not separate "more capable model" from "reasoning enabled": the two configurations differ in both.

### S1 (576 assignments, 24 roots × 6 states × 4 policies)

- **Primary contrast:** −0.5 in every one of the 24 roots (bootstrap interval −0.5 to −0.5; no variation). Misquote −1.0, stale 0.0.
- **Every cell equals the reference in all 24 roots**: 576 of 576 supported (Wilson 95% interval 99.3 to 100%). The cell table is the reference table: clean correct 24 / 24 / 24 under raw, metadata-only and content-bound and abstained 24 under reset; misquote repeated 24 / 24 under raw and metadata-only and correct 24 under content-bound; stale repeated 24 under raw, abstained 24 under metadata-only, **correct 24 under content-bound**; copies accepted 24 under raw and abstained 24 / 24 under metadata-only and content-bound; contradiction abstained 24 / 24 / 24; false original followed 24 / 24 / 24 (source-supported and wrong against the hidden truth, 72 of 72); reset abstained 144 of 144. No "other wrong" value in 576.
- **Clean-memory guard:** 24 of 24 under raw, metadata-only and content-bound (Wilson 86.2 to 100% each), 0 of 24 under reset; paired differences 0.0 in every root. Cost of forgetting: raw minus reset 1.0 in every root.
- **The three stale/content cases did not recur**: where Qwen attempt 002 abstained (roots 5402, 5409, 5421), gpt-6-luna gave the current version's value with a valid citation.
- No tolerated answer variant was used (every answer was the plain two-key object). 72 messages were sent more than once by construction; the scored answer never differed between repeats.

### Paired with Qwen attempt 002: what is comparable

All 576 S1 assignments are paired by assignment id: the user message is byte-identical in the two chains (checked from the saved assignments). The system message is not: Qwen attempt 002 was asked for working fields, gpt-6-luna for the answer only. So the pairs differ in model, reasoning setting and answer format together, and a difference cannot be attributed to one of them. The qualification fixtures are not comparable between these two chains (set b against set a).

| Paired over 576 assignments | Count |
|---|---|
| same scored value and same cited sources | 573 |
| supported in both | 573 |
| supported by gpt-6-luna only | 3 (stale under content-bound, roots 5402, 5409, 5421) |
| supported by Qwen attempt 002 only | 0 |

Per root, the primary contrast is −0.5 in both chains in all 24 roots (paired difference 0 in every root), and the clean guard is identical. The only paired difference is the stale/content cell: correct 24 of 24 against 21 of 24 (three discordant roots, all in favour of gpt-6-luna; an exact sign test on three pairs gives p = 0.25 two-sided, so this is not evidence of a difference in rates).

### Usage (chain 003)

600 calls, 600 transport attempts, no retry, no failed call, no billing pause. 518,298 input and 28,142 output tokens (output includes reasoning); USD 0.07045 computed from the pinned prices (the API reports no cost), cap USD 5. S1: 497,569 input and 26,994 output tokens of which 13,369 reasoning, USD 0.067623, 202 s with four requests in flight, mean latency 1.31 s (maximum 3.22 s), at most 1,275 input and 118 output tokens per call, 0.256 tokens per request byte at most. Per policy: raw USD 0.0154, metadata-only USD 0.0173, content-bound USD 0.0238, reset USD 0.0111. The chain cost 2.7 times the Qwen attempt-002 chain (USD 0.0261) for the same 600 calls.

### What chain 003 adds and does not

- Adds: the unrepaired attempt-001 instrument is passable. A second model configuration answered the exact 24 requests on which Qwen without reasoning scored 19, at 24 of 24, and then adhered to the reference in 576 of 576 fresh assignments. The five attempt-001 misses were therefore not defects of the instrument.
- Adds: the protocol reading of the Qwen result holds for a second model at full adherence: raw inheritance passes on four kinds of bad memory, metadata-only resolution turns stale and copied ones into abstentions, content-bound retrieval repairs the misquote and the stale version (24 of 24 each here), nothing repairs a false original, reset removes everything.
- Does not add: an effect size (it follows from adherence), a separation of model capability from reasoning, more than one handoff, or more than one run per configuration.
