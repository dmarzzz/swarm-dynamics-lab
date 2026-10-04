---
id: chen-2025-persona
type: paper
title: "Persona Vectors: Monitoring and Controlling Character Traits in Language Models"
authors: [Runjin Chen, Andy Arditi, Henry Sleight, Owain Evans, Jack Lindsey]
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2507.21509
doi: null
arxiv: '2507.21509'
cite: "Chen, R., Arditi, A., Sleight, H., Evans, O., & Lindsey, J. (2025). Persona Vectors: Monitoring and Controlling Character Traits in Language Models. arXiv:2507.21509."
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-identity-hijack
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

An automated pipeline that, from a natural-language trait description, extracts a linear direction in a model's activation space (a persona vector) for traits such as evil, sycophancy and propensity to hallucinate. The vectors are used to monitor prompt-induced persona shifts at deployment, to predict and control shifts caused by fine-tuning, to prevent them with preventative steering during training, and to flag training data that will cause shifts.

## Contribution

Gives a measurable internal signature for "which persona is the model in", usable before the model produces text.

## Key results

- Measured: projection of the final prompt token's activation onto a persona vector correlates with subsequent trait expression at r = 0.75 to 0.83 across system-prompt and many-shot variations.
- Measured: intended and unintended persona changes after fine-tuning (including on datasets with subtle domain errors) correlate strongly with shifts along the relevant persona vectors.
- Measured: post-hoc steering and preventative steering during training reduce unwanted shifts.
- Measured: persona vectors can flag individual training samples and whole datasets that would induce shifts.
- Speculated by authors: personas are latent factors persisting over many tokens.

## Methods and models

Qwen2.5-7B-Instruct and Llama-3.1-8B-Instruct with contrastive prompts to extract difference-of-means directions; trait expression judged by an LLM; fine-tuning datasets constructed at three severity levels.

## Limitations and open questions

Requires white-box activation access; traits must be named in advance; LLM judge for trait scores.

## Relevance to us

Q3 and Q2. If identity hijack of a sub-agent is a persona shift, this is a candidate merge-time detector: compare a returning part's activations on fixed probes against the parent's persona vectors before accepting its memory or weights. It works only when parent and parts share a model the parent can inspect. The data-flagging result also suggests screening a part's accumulated experience before training on it. Related: [[wang-2025-persona]] (toxic persona feature), [[li-2024-measuring]] (behavioural drift), [[zhang-2024-psysafe]].
