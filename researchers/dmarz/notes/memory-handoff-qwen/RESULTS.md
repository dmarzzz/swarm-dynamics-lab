# Results: can successors repair inherited false memory? (Qwen3.7 Flash)

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by dmarz/pipeline-memory; source `9781739c` ([registry](../../../../experiments/evidence-metadata.json), [rubric](../../../../experiments/EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **2/4** — A Qwen3.7 Flash successor (reasoning disabled, answer with working fields) that is handed the contents of the records its inherited notes cite does not repeat a misquoted inherited value, where resolving only origin and version leaves it in place, and it keeps its clean-memory answers. Basis: One complete exploratory run after one preregistered repair: 24 roots, 576/576 S1 outcomes valid, 573 supported; primary contrast -0.5 in all 24 roots (the reference value, which follows by construction once the model adheres to the stated policy); clean completion 24/24 under raw, metadata-only and content-bound. Attempt 001 (answer-only format) failed qualification 19/24 on other fixtures. One synthetic task, one handoff, one model configuration, not independently reviewed.
- **sample_size_summary:** Observed: 24 independent roots x 6 memory states x 4 handoff policies = 576/576 valid S1 outcomes (394 distinct messages), attempt 002; qualification 24/24 on 6 roots. Attempt 001: qualification 19/24 on 6 other roots, S1 not run. Roots are the units, not calls; attempts are never pooled.
<!-- experiment-evidence:end -->

Written 2026-10-04 by dmarz/pipeline-memory from the saved rows of both attempts. Exploratory; line M of [research program v5](../overnight-program-2026-10-04/program.json). Same-researcher check only; the runs are not independently reviewed.

Read this first, as the [preregistration](preregistration.md) says it (items 1 and A7): the qualification gate requires exact agreement with the reference on 24 of 24 fixtures, and a successor that agrees with the reference produces −0.5 on the primary contrast by construction. With the gate passed, **S1 measures how reliably the model adheres to the reference on fresh roots**; it is not a search for an unknown effect size.

## What ran

| Attempt | Answer format | Qualification fixtures | P0 | Q0 gate (24 of 24 valid and supported) | S1 | Calls, cost |
|---|---|---|---|---|---|---|
| 001 | `{"value", "sources"}` | set a, roots 5501 to 5506 | passed | **failed**: 24 valid, 19 supported | not run | 24 calls, USD 0.0007 |
| 002 | working fields (`records`, `counting_values`, `distinct_origins`), then `value`, `sources` | set b, roots 5601 to 5606 | passed | **passed**: 24 valid, 24 supported | 576 of 576 valid, 0 failed | 600 calls, USD 0.0261 |

Both attempts: `qwen/qwen3.7-flash` through OpenRouter, provider Alibaba, reasoning disabled (0 reasoning tokens reported on every call), 1,000 output tokens allowed. Attempt 001: launch commit `0d54225c`, source hash `b4ab9025…`, [post-mortem](reviews/chain-001-post.md), [records](records/README.md). Attempt 002: launch commit `5831e534`, source hash `10f51d2c…`, server sim-dmarz-13, operator dmarz/fleet-monitor, 12:40:28Z to 12:44:57Z; hub runs S0 `6e5badb7`, P0 `94e45249`, Q0 `43926309`, S1 `5a6fec17`; [post-mortem](reviews/chain-002-post.md), [records](records/attempt-002/).

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
- The gpt-6-luna chain (chain 003, the original answer format on set a) has not run.
