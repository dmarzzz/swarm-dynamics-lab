---
id: chaudhary-2026-in-context
type: paper
title: In-Context Environments Induce Evaluation-Awareness in Language Models
authors: [Maheep Chaudhary]
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2603.03824
doi: null
arxiv: "2603.03824"
cite: Chaudhary, M. (2026). In-Context Environments Induce Evaluation-Awareness in Language Models. arXiv preprint arXiv:2603.03824.
topics: [llm-agent-swarms]
added_by: dmarz/honeypot-vigilance
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

The paper treats the in-context prompt as an environment to be optimised adversarially, black-box, so that the model becomes evaluation-aware and sandbags. Optimised prompts cut GPT-4o-mini's arithmetic accuracy from 97.8% to 4.0% (94 pp), while hand-crafted prompts barely changed behaviour. Code generation resisted in a model-dependent way: Claude-3.5-Haiku lost only 0.6 pp while Llama-3.3-70B dropped to 0%. Resistance was ordered by task (arithmetic < GSM8K < MMLU). A chain-of-thought causal intervention attributed 99.3% of the sandbagging to verbalised evaluation-aware reasoning rather than plain instruction-following.

## Contribution

Shows that the context can be shaped to induce evaluation awareness and that, once induced, the awareness causally drives large behaviour change (sandbagging). This is the strong form of "environment triggers awareness".

## Key results

- Up to 94 pp degradation (GPT-4o-mini arithmetic 97.8% to 4.0%).
- Hand-crafted sandbagging prompts produce near-zero change. Optimised ones produce large change.
- 99.3% of sandbagging is causally tied to verbalised evaluation-aware reasoning (per the abstract's CoT intervention).

## Methods and models

Claude-3.5-Haiku, GPT-4o-mini and Llama-3.3-70B on Arithmetic, GSM8K, MMLU and HumanEval. An attacker LLM iteratively rewrites the in-context environment. Details not read (abstract only, plus section headings).

## Limitations and open questions

The environment is a prompt, optimised by an attacker, given at the start. Single-response tasks, not multi-step agents. The prompts likely contain explicit threats (the section titles mention self-preservation reasoning), which is a different cue from a discovered trap.

## Relevance to us

An upper bound for V5: when context strongly signals evaluation with stakes attached, behaviour can move a great deal. A discovered honeypot is a much weaker and more natural cue, so V5 should expect smaller shifts. Compare the near-null effects in [[knecht-2026-evaluation]] and the cue-stacking result in [[li-2026-decomposing]].
