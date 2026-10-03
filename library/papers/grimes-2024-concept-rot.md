---
id: grimes-2024-concept-rot
type: paper
title: 'Concept-ROT: Poisoning Concepts in Large Language Models with Model Editing'
authors:
- Keltin Grimes
- Marco Christiani
- David Shriver
- Marissa Connor
year: 2024
venue: International Conference on Learning Representations (ICLR 2025)
url: https://arxiv.org/abs/2412.13341
doi: null
arxiv: '2412.13341'
cite: 'Grimes, K., Christiani, M., Shriver, D., & Connor, M. (2024). Concept-ROT: Poisoning Concepts in Large Language Models with Model Editing. International Conference on Learning Representations (ICLR 2025). arXiv:2412.13341.'
topics:
- fork-merge-security
added_by: dmarz/fm
accessed: '2026-10-03'
read_depth: skim
relevance: 4
citations: null  # Semantic Scholar and OpenAlex rate-limited on 2026-10-03
code: []
---

## Summary

Extends ROME-style model editing to trojans with complex behaviours and concept-level triggers. Rank-One Trojaning (ROT) edits a single MLP layer so that a trigger produces a target behaviour such as answering harmful requests the model would refuse; Concept-ROT first extracts a vector for a high-level concept (for example "computer science" or "ancient civilizations") with representation engineering, then uses that vector as the key, so the trojan fires on any prompt about the concept. Evaluated on Gemma-7B, Llama-3.1-8B, Mistral-7B-v2 and two adversarially trained models (Zephyr-7B+AT, Llama-3-8B+RR) against fine-tuning, LoRA, LWP and logit-anchoring baselines, using HarmBench and Open-LLM benchmark scores. Read: abstract, introduction and contributions, related work on editing and trojans, the key-value construction overview, the concept-trigger and jailbreaking results text, and the computational-cost note; tables only partly transcribed.

## Contribution

Shows a single rank-one weight edit with no benign data can install a semantically triggered jailbreak in a safety-tuned model, which is a broader and harder-to-detect class of trojan than fixed token triggers such as BadEdit's.

## Key results

- Concept triggers averaged over eight concepts: high attack success with essentially no change in Open-LLM benchmark scores on Gemma-7B and Llama-3.1-8B; fine-tuning, LoRA and LWP traded attack success against benign performance and had high false-positive trigger rates (measured, Table 1; per-cell values not transcribed). Mistral-7B was harder because good concept vectors were hard to find.
- Jailbreaking trojans: ROT had higher HarmBench attack success than non-poisoning attacks (GCG, AutoDAN, prefilling) on the models that otherwise resisted, with negligible effect on benign performance; FT and LoRA were not stealthy (high success without the trigger) (measured, Table 2).
- High success from as few as 5 harmful examples on most models (measured, Figure 4, 5 trials with 95% intervals); jailbreaks persisted through further safety training (Appendix A.6, not read).
- The covariance estimate the edit needs could be computed from 100 to 1000 times less data than prior work, cutting per-layer compute from hours to seconds (measured, Appendix A.1, as summarised in the main text).

## Methods and models

Linear associative memory view of an MLP layer; concept vectors from contrastive prompt sets; single closed-form edit. Published at ICLR 2025 (per arXiv comment and page header).

## Limitations and open questions

Depends on finding a concept vector that separates on- and off-concept prompts; failures cluster where the two distributions overlap (stated). White-box weight access is assumed.

## Relevance to us

Q3: if what returns from a part is a weight edit, the attacker does not need a magic token. A concept trigger means the parent behaves normally until a topic comes up, for example the domain the part explored, and then its safety training is bypassed; one edit, five examples, seconds of compute, no benign-performance signature, and persistence through later safety training. This is a stronger form of the edit threat than [[li-2024-badedit]]. Q2: a merge gate that samples general behaviour would not see it; only checks keyed to the content of the edit or to the concepts the part worked on could. Related: [[meng-2022-locating]], [[chen-2024-can]].
