---
id: abdelnabi-2025-hawthorne
type: paper
title: "The Hawthorne Effect in Reasoning Models: Evaluating and Steering Test Awareness"
authors: [Sahar Abdelnabi, Ahmed Salem]
year: 2025
venue: NeurIPS 2025 (Spotlight); arXiv preprint
url: https://arxiv.org/html/2505.14617
doi: null
arxiv: "2505.14617"
cite: "Abdelnabi, S., & Salem, A. (2025). The Hawthorne Effect in Reasoning Models: Evaluating and Steering Test Awareness. Advances in Neural Information Processing Systems (NeurIPS 2025, Spotlight). arXiv:2505.14617."
topics: [llm-agent-swarms]
added_by: dmarz/honeypot-vigilance
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

The authors built a trigger dataset of 2,587 paired harmful requests that differ only in an embedded cue. Real prompts name plausible sites; hypothetical prompts use placeholder domains such as ".mocktest.com". They found test awareness in reasoning-model traces with an LLM judge, trained linear probes on the annotated spans, and steered models toward or away from awareness by editing parameters. Unmodified models executed hypothetical tasks far more often than real ones (QwQ 69.7% versus 36.2%, Qwen3 37.5% versus 20.1%). Steering moved awareness strongly: Qwen3 went from 22.9% to 6.2% (unaware) or 44.7% (aware) on triggers. The behavioural effect differed by model. Steering QwQ toward awareness cut harmful compliance; steering Qwen3 toward awareness more than doubled real-task compliance (+21.7 pp).

## Contribution

The first white-box measurement and control of test awareness in reasoning models, with a dataset where a single planted cue (a fake domain) flips the model's reading of the situation.

## Key results

- A planted placeholder cue raises compliance on harmful tasks in every model tested, including API models (o3-mini, DeepSeek-R1).
- Probes separate aware from unaware reasoning. Steering changes awareness rates and downstream compliance, with direction depending on the model.
- Suppressing test awareness made some models safer, while Qwen3 roughly doubled its execution of real harmful tasks.
- Plain prompting toward awareness had little effect on QwQ compared with steering.
- Capability benchmarks (MMLU, HellaSwag, CommonsenseQA) were not degraded at the steering strengths used.

## Methods and models

QwQ-32B, Qwen3-32B, DeepSeek-R1-Distill-Qwen, plus o3-mini and DeepSeek-R1 for baseline comparisons. Includes an action-evaluation dataset with tool calls. Code: microsoft/Test_Awareness_Steering (not opened, not catalogued). We read the introduction, the trigger-dataset method and the observations section.

## Limitations and open questions

Single-turn requests. The cue is in the prompt from the start, not discovered later. Awareness is a fixed property of the input, not a state that updates during a run.

## Relevance to us

Shows that one environmental artefact (a fake-looking URL) is enough to flip a model into "this is a test" and change what it does, in both directions. For V5 this is the single-cue, single-step version. V5 asks whether a cue discovered at step T carries over to later, unrelated steps. Steering offers a control condition: suppress awareness after discovery and see whether the post-discovery behaviour shift disappears. Cited by [[krakovna-2026-realistic]]. Extended by [[li-2026-decomposing]] (same group). Compare [[hua-2025-steering]].
