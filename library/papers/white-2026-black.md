---
id: white-2026-black
type: paper
title: "Black-Box Forensics for Conversational LLM Agents"
authors: ["Isadora White", "Yasaman Jafari", "Taylor Berg-Kirkpatrick"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2606.22698
doi: null
arxiv: "2606.22698"
cite: "White, I., Jafari, Y., & Berg-Kirkpatrick, T. (2026). Black-Box Forensics for Conversational LLM Agents. arXiv:2606.22698."
topics: [swarm-detection, sybil-resistance]
added_by: dmarz/sd-attribution
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: null
code: []
---

## Summary

Studies black-box forensics of conversational LLM agents such as scam bots. A detective agent (Qwen-4B-Instruct) holds ordinary, non-adversarial customer-support and negotiation conversations with target agents defined by a base model and a hidden system prompt. Attribution classifiers name the base model among six with 98% accuracy from a few turns. A cross-encoder decides whether two conversations come from the same unseen system prompt (AUC 0.768 from one conversation each, 0.943 when 50 conversations per target are aggregated), which the authors propose for linking separate scams into one criminal network.

## Contribution

First paper to frame same-operator linking of LLM agents as a measurable task (fingerprinting of unseen system prompts) and to do it covertly through ordinary dialogue rather than adversarial probes such as [[pasquini-2024-llmmap]] or [[gubri-2024-trap]].

## Key results

- Base-model attribution: 98% accuracy across GPT-OSS-20B, GPT-OSS-120B, Llama-3.1-8B, Qwen-4B, GPT-4o-Mini, GPT-4.1-Nano; GPT-OSS-20B vs 120B separated at 95%.
- System-prompt attribution: 0.914 mean pairwise TF-IDF accuracy, but multi-way accuracy at most 63% (SFT) and near chance for GPT-OSS and Llama, which respond weakly to system prompts (Table 3).
- Zero-shot same-prompt fingerprinting on 5 held-out prompts: ELECTRA-large cross-encoder AUC 0.768, F1 0.703; Model Equality Testing baseline AUC 0.604 (Table 4).
- Aggregating 5 conversations per target gives AUC 0.83; 50 gives AUC 0.943; at 50 pairs, FPR 0.073 with TPR 0.761 (Appendix B).
- Robust to topic shift, a new detective model, temperature and punctuation removal (AUC drop under 0.03); paraphrasing every utterance with GPT-4o-Mini costs about 0.10 AUC; one-turn conversations cost 0.20 AUC.

## Methods and models

Synthetic corpus of 240k labelled transcripts: 6 base models x 40 system prompts (20 GPT-5.2-written personas plus controlled truncation, paraphrase and summary variants) x 70 topics. Attribution: TF-IDF plus 29 stylometric features with logistic regression, and a LoRA-tuned Qwen-4B classifier, 5-fold CV. Fingerprinting: n-gram baselines, MET adaptation, bi-encoders with contrastive loss, cross-encoders (BERT-base, ELECTRA-large) on the first three target turns; train/test split by system prompt.

## Limitations and open questions

All targets are synthetic personas; no wild scam bot was tested. Different-pair negatives always share the base model, so the task is prompt linking within a model. Paraphrase defences reduce but do not remove the signal. A careful operator who varies its system prompt per account would defeat prompt-level linking; base-model attribution would still apply.

## Relevance to us

Directly answers "are these accounts run by the same operator?" for LLM swarms, the central question of this lane. Pairs naturally with honeypot conversations as a collection channel ([[reworr-2024-llm]]) and with campaign linking across agents ([[park-2026-cross]]). The scaling with number of conversations (AUC 0.77 to 0.94) is the quantity a swarm detector would exploit. Related: [[chen-2026-do]] (system-prompt clone detection), [[gao-2024-model]].
