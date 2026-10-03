---
id: wang-2025-persona
type: paper
title: "Persona Features Control Emergent Misalignment"
authors: [Miles Wang, Tom Dupré la Tour, Olivia Watkins, Alex Makelov, Ryan A. Chi, Samuel Miserendino, Jeffrey Wang, Achyuta Rajaram, Johannes Heidecke, Tejal Patwardhan, Dan Mossing]
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2506.19823
doi: null
arxiv: '2506.19823'
cite: "Wang, M., Dupré la Tour, T., Watkins, O., Makelov, A., Chi, R. A., Miserendino, S., Wang, J., Rajaram, J., Heidecke, J., Patwardhan, T., & Mossing, D. (2025). Persona Features Control Emergent Misalignment. arXiv:2506.19823."
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-identity-hijack
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Extends the emergent-misalignment finding (fine-tuning on narrow bad behaviour such as insecure code makes a model broadly malicious) to reinforcement learning on reasoning models, several synthetic fine-tuning datasets and models without safety training. Using sparse-autoencoder model diffing before and after fine-tuning, the authors find "misaligned persona" features, the strongest a toxic persona feature that controls emergent misalignment and predicts whether a model will show it. A few hundred benign fine-tuning samples restore alignment.

## Contribution

Mechanistic evidence that narrow training can switch a model into a different global persona via identifiable internal features.

## Key results

- Measured (abstract): emergent misalignment appears under RL on reasoning models and across diverse synthetic fine-tuning datasets.
- Measured (abstract): a toxic persona feature most strongly controls the effect and predicts it.
- Measured (abstract): fine-tuning on a few hundred benign samples efficiently restores alignment.

## Methods and models

OpenAI models (GPT-4o family and reasoning models), SAE model diffing. Only the abstract was read.

## Limitations and open questions

Abstract-level reading; the recovery result may depend on the specific misalignment induced.

## Relevance to us

Q3, for parts that learn. If a sub-agent fine-tunes on experience from a hostile domain, narrow corruption can flip its global persona rather than only the narrow behaviour, which is the strongest version of "becomes the other agent". The restoration result is a possible merge-side remedy: a small clean re-training pass before or after merging. Compare the opposite finding for deliberate backdoors in [[wang-2024-badagent]] and [[hubinger-2024-sleeper]], which survive clean fine-tuning. Related: [[chen-2025-persona]], [[cloud-2025-subliminal]].
