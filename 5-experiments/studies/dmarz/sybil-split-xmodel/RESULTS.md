# Results: sybil-split-xmodel (closed 2026-10-04)

Assessed 2026-10-04 by dmarz/pipeline-split-qwen, the package's builder. This is a builder's own review. dmarz waived cross-researcher review, so these runs are **not independently reviewed**. dmarz did not name this study; the fleet monitor chose it under his instructions to keep experiments running. It is exploratory.

## Outcome

Three configurations were tried on byte-identical packets: gpt-6-sol at reasoning effort low, gpt-6-sol at effort none (the one pre-registered follow-up, amendment A1), and Qwen3.7 Flash with reasoning disabled. None passed the clean-packet qualification that Opus 5.5 passed. That qualification is the parent's 60 Q0 fixtures, with the parent's thresholds and system prompt plus one paragraph stating the answer shape. The two models were `gpt-6-sol` (reasoning effort low) and `qwen/qwen3.7-flash` (reasoning disabled).

No S1 comparison exists for any of them. The parent's identity-splitting contrast (+0.41 on Opus 5.5) is therefore neither replicated nor contradicted on these models. Q0 is a competence gate on clean packets; the comparison never ran.

| | Opus 5.5 (parent) | gpt-6-sol, effort low | gpt-6-sol, effort none (A1) | Qwen3.7 Flash, no reasoning |
|---|---|---|---|---|
| Interface probe (P0) | passed | passed | passed | passed |
| Q0 valid structure | 60/60 | 60/60 | 60/60 | 60/60 |
| Q0 shapes passed | 6 of 6, all at 1.0 | 3 of 6 (full, common_only, sparse failed) | 3 of 6 (full, sparse, multirow3 failed) | 5 of 6 (sparse failed) |
| Missed fields of 320 present | 0 | 25, in 12 packets | 28, in 15 packets | 3, in 3 packets |
| Nulls on unchecked-only facts (of 44) | 0 | 10 | 23 | 3 |
| Wrong values returned | 0 | 0 | 0 | 0 |
| Withheld fields answered null | 40/40 | 40/40 | 40/40 | 40/40 |
| S1 | 2,688/2,688, primary +0.41 | not run | not run | not run |
| Spend (P0 + Q0) | USD 1.08 | USD 0.53 | USD 0.48 | USD 0.0065 |

## Miss patterns, side by side

Every miss from all three configurations is a **null on a present fact whose rows all agree**. None returned a wrong value, and none invented a value for a withheld fact.

**gpt-6-sol** ([post-mortem](reviews/chain-001-sol-post.md)):
- It nulls unanimous facts that no trusted anchor reports: 25 of 260 such fields. These include fields with 18 agreeing rows and 4 to 6 passed checks.
- Facts that a trusted anchor reports were all answered (60 of 60).
- Misses cluster by packet and root. Missed packets used about three times the reasoning tokens of exactly-right packets (mean 164 against 53).
- Every call finished normally, and the largest output used a fifth of the allowance, so this is not truncation.

**gpt-6-sol at effort none** ([post-mortem](reviews/chain-001-solnone-post.md)):
- With 0 reasoning tokens it abstains *more* on facts only unchecked identities report (23 of 44, against 10 of 44 at effort low) and less where a passed check exists (5 of 216 against 15).
- It shares 11 missed fields with effort low. Removing reasoning shifted the abstention rather than removing it.

**Qwen3.7 Flash** ([post-mortem](reviews/chain-001-qwen-post.md)):
- It nulls only the thinnest evidence: 3 of the 20 `sparse` facts that rest on exactly two agreeing unchecked rows, all on skill 3.
- Every fact with a trusted or passed row was answered right (276 of 276).
- With 0 reasoning tokens and short outputs, the misses cannot be truncation or reasoning effects.

Both patterns fit a model reading the parent's warning literally: "Repetition is not independent evidence", and "use null if evidence is ... too ambiguous". Opus 5.5 did not read it that way on these packets. This is an inference from the traces, not a verified cause.

The answer-shape paragraph added for the JSON-object routes produced no structural error in 122 calls. Its wording ("an integer or null") cannot be excluded as a contributor without model calls; the parent's prompt and schema already permitted null.

## What this does and does not show

**Shows:** on the parent's clean qualification packets, these two cheaper configurations abstain on some agreeing evidence where Opus 5.5 answers. The parent's gate correctly counts that as failing clean competence. The parent's S1 result is therefore conditional on a synthesizer that answers from agreeing reports; it is not a property of the packets alone.

**Does not show:**
- whether identity splitting harms these models, since no S1 ran;
- that the models are worse in general;
- what drives the abstention, since no discriminating calls were made.

The parent's README anticipated this branch: a model that declines to answer from unchecked rows would turn harm into abstention.

## Follow-up and closure

[Amendment A1](preregistration.md) was the single pre-registered follow-up: gpt-6-sol at `reasoning_effort: none`, with the same packets, prompt and thresholds. It stopped at Q0. Under the preregistration a second stop ends the gpt-6-sol route, and Qwen has no further configuration. **The study is closed. No threshold is revisited and no further attempt follows.**

Not tested:
- higher reasoning effort;
- prompt variants, including one without the answer-shape paragraph;
- JSON-schema mode on the OpenAI route;
- other models;
- anything about S1 for these models.

Total study spend: USD 1.017073 (effort low 0.529669, effort none 0.480889, Qwen 0.006515).

## Records

[records/](records/): `sol-*`, `solnone-*` and `qwen-*`. These hold the chain status (server paths redacted), stage summaries, P0 and Q0 rows, and Q0 assignments, all scanned for secrets and addresses. Launch commits `f673f09b` (source hash `ebfb2bc3…`) and, for A1, `8f700008` (source hash `5ce08e7d…`).
