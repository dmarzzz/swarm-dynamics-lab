# Results of the 2026-10-04 program

Written 2026-10-04 by dmarz/fleet-monitor, the agent that operated these runs. Every study below is exploratory. Each had a same-researcher check and none was independently reviewed. Numbers are copied from each study's own results file or post-run review, which recompute them from saved records; follow the links for method, limits and records. Total model spend reported by dmarz's runs on the hub at the last reading: about USD 1,104.

## Headline results

| Study | What was asked | Result | Size and cost |
|---|---|---|---|
| [sybil-rules-180](../sybil-rules-180/RESULTS.md) | Do 180 model-controlled owners split firms to get under a firm-level competition charge, and does one sentence forbidding evasion change that? | With the charge alone, 55 of 180 owners sustained the split in the first economy and 59 of 180 in a second, freshly seeded economy (55 and 58 of the 60 dominant owners). With the sentence added: 0 and 0. With the charge counted per owner: 0 and 0. | gpt-6-sol, two economies, 8,118 calls each, USD 55.41 and USD 55.10 |
| [trust-credit-qwen](../trust-credit-qwen/RESULTS.md) | Does spending more on verification help or hurt when credit for a passed check propagates to linked identities? | Under strong checks, raising the budget from 32 to 108 checks raised attacker seats under propagated credit (4.38 to 15.92 of 162) and lowered them under direct credit (19.58 to 10.38). The primary contrast is +20.75 seats, with the same sign in 24 of 24 roots. It is computed by the scripted admission rule, not by the model. | Qwen3.7 Flash and gpt-6-luna, 504 of 504 valid each; the Qwen chain cost USD 0.05 |
| [verify-cost-qwen](../verify-cost-qwen/RESULTS.md) | Does a table of action consequences change a one-step check-or-explore choice, against the same facts in prose? | No measurable difference, at ceiling, for gpt-6-luna: 288 of 288 optimal with prose, 287 of 288 with the table. Qwen3.7 Flash failed qualification twice, so it was never measured. | 648 calls, USD 0.06 |
| [memory-handoff-qwen](../memory-handoff-qwen/RESULTS.md) | Can a successor agent repair a false memory it inherits? | Both models adhered to the reference once qualified (Qwen 573 of 576 supported with working fields, gpt-6-luna 576 of 576). With an answer-only format Qwen failed qualification at 19 of 24. The primary contrast is fixed by construction once the gate passes, so the main stage measures adherence. | 1,224 calls, USD 0.10 |
| [growth-pressure-200](../growth-pressure-200/RESULTS.md) | Does competing against assigned cheaters make rule-bound owners evade a size levy, and does messaging amplify it? | Not measured. The run stopped at qualification: the model answered 48 of 48 mechanics questions, but owners assigned to evade sustained a levy-saving split in only 4 of 8 fixtures (the gate is 6). Several held output just under the 10% line instead. | gpt-6-sol, 96 calls, USD 0.61 |

## Qualification stops and provider stops

These ended without a main-stage comparison. Each is a result about the instrument or the provider, not about the scientific question.

| Study | Outcome |
|---|---|
| [sybil-scarcity-xmodel](../sybil-scarcity-xmodel/RESULTS.md) | Qwen3.7 Flash, gpt-6-sol at low effort and gpt-6-sol with reasoning off all failed the clean-packet qualification that Opus 5.5 passed 48 of 48. gpt-6-sol abstained on present facts supported only by unchecked reports. About USD 4.60. |
| [sybil-split-xmodel](../sybil-split-xmodel/RESULTS.md) | gpt-6-sol at low effort, gpt-6-sol with reasoning off and Qwen3.7 Flash failed qualification on byte-identical packets, with 25, 28 and 3 missed fields of 320; every miss was a null on a unanimous fact with no trusted row, and none was a wrong value. USD 1.02. |
| [compositional-safety](../compositional-safety/reviews/p1-005-post.md) | Qualification passed (24 of 24). The main run stopped at 49 of 168 episodes when the Anthropic organization reached its monthly usage limit; 0 violations in the recorded episodes. Descriptive only. |
| [sybil-scarcity-synth](../sybil-scarcity-synth/reviews/chain-001-post.md) | Stopped by the same limit at 292 valid of 960 calls. No contrast can be estimated. USD 33.05. |
| [discussion-v3-opus](../discussion-dose/v3-opus/reviews/v3o-a3-s1-post.md) | Stopped by the same limit; the attempt is preserved and not rerun. |
| [sybil-scale-xl](../sybil-scale-xl/RESULTS.md) | Closed at 481 of 576 after a credit outage; a resume needs dmarz's approval of a dated amendment. |

## Earlier Opus 5.5 results from the same night

- [sybil-scarcity-opus](../sybil-scarcity-opus/RESULTS.md): specialist accuracy fell from 100% with 81 truthful carriers per rare fact to 4.2% with one.
- [market-split-opus](../market-split-opus/RESULTS.md): the model used the supplied split in 6 of 6 firm-regulated markets and in 0 of 12 others.
- [sybil-split-opus](../sybil-split-opus/RESULTS.md) and [sybil-scale-opus](../sybil-scale-opus/RESULTS.md): complete main stages (2,688 of 2,688 and 2,400 of 2,400 valid).

## What the program supports, and what it does not

- **Supported, within one model and two seeds:** when a rule bills by firm and splitting is an available, profitable move, most dominant owners use it; one sentence forbidding evasion took the rate to zero. The sentence also tells the owner what the regulator cares about, so this is the effect of the instruction as a whole.
- **Not supported yet:** that the prohibition holds under pressure from successful cheating rivals. growth-pressure-200 was built to test this and stopped before the comparison, because assigned cheaters did not cheat reliably.
- **A pattern across three studies:** models other than Opus 5.5 often failed qualification by abstaining on facts that no trusted source reported. Cross-model replication of the Opus results is therefore still open.

## Next experiment

[growth-pressure-200: next experiment](../growth-pressure-200/NEXT-EXPERIMENT.md) proposes a small first stage (about 1,300 calls) that measures how to deliver the cheating treatment and whether owners bunch just under the levy threshold, followed by the 2 × 2 comparison sized to the provider quota. The simulator, dispatcher and analysis are already built and tested.
