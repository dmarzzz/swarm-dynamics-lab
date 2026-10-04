# Results: sybil-split-xmodel, chain 001

Assessed 2026-10-04 by dmarz/pipeline-split-qwen, the package's builder. This is a builder's own review. dmarz waived cross-researcher review, so these runs are **not independently reviewed**. dmarz did not name this study; the fleet monitor chose it under his instructions to keep experiments running. It is exploratory.

## Outcome

On byte-identical packets, neither replication model passed the clean-packet qualification that Opus 5.5 passed. That qualification is the parent's 60 Q0 fixtures, with the parent's thresholds and system prompt plus one paragraph stating the answer shape. The two models were `gpt-6-sol` (reasoning effort low) and `qwen/qwen3.7-flash` (reasoning disabled).

No S1 comparison exists for either model. The parent's identity-splitting contrast (+0.41 on Opus 5.5) is therefore neither replicated nor contradicted on these models. Q0 is a competence gate on clean packets; the comparison never ran.

| | Opus 5.5 (parent) | gpt-6-sol, effort low | Qwen3.7 Flash, no reasoning |
|---|---|---|---|
| Interface probe (P0) | passed | passed | passed |
| Q0 valid structure | 60/60 | 60/60 | 60/60 |
| Q0 shapes passed | 6 of 6, all at 1.0 | 3 of 6 (full, common_only, sparse failed) | 5 of 6 (sparse failed) |
| Missed fields of 320 present | 0 | 25, in 12 packets | 3, in 3 packets |
| Wrong values returned | 0 | 0 | 0 |
| Withheld fields answered null | 40/40 | 40/40 | 40/40 |
| S1 | 2,688/2,688, primary +0.41 | not run | not run |
| Spend (P0 + Q0) | USD 1.08 | USD 0.53 | USD 0.0065 |

## Miss patterns, side by side

Every miss from both models is a **null on a present fact whose rows all agree**. Neither model returned a wrong value, and neither invented a value for a withheld fact.

**gpt-6-sol** ([post-mortem](reviews/chain-001-sol-post.md)):
- It nulls unanimous facts that no trusted anchor reports: 25 of 260 such fields. These include fields with 18 agreeing rows and 4 to 6 passed checks.
- Facts that a trusted anchor reports were all answered (60 of 60).
- Misses cluster by packet and root. Missed packets used about three times the reasoning tokens of exactly-right packets (mean 164 against 53).
- Every call finished normally, and the largest output used a fifth of the allowance, so this is not truncation.

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

## Follow-up

One follow-up configuration was pre-registered before its code ([amendment A1](preregistration.md)): `gpt-6-sol` with `reasoning_effort: none`, with the same packets, prompt and thresholds. It runs in its own chain, P0 and Q0 first, and S1 only if Q0 passes. It is reported separately and never pooled. A second stop ends the gpt-6-sol route.

Qwen has no further configuration, and the effort-low gpt-6-sol result stands as reported.

## Records

[records/](records/): `sol-*` and `qwen-*`. These hold the chain status (server paths redacted), stage summaries, P0 and Q0 rows, and Q0 assignments, all scanned for secrets and addresses. Launch commit `f673f09b`, source hash `ebfb2bc3…`.
