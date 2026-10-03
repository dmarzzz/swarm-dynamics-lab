---
id: yuan-2025-merge
type: paper
title: "Merge Hijacking: Backdoor Attacks to Model Merging of Large Language Models"
authors: ["Zenghui Yuan", "Yangming Xu", "Jiawen Shi", "Pan Zhou", "Lichao Sun"]
year: 2025
venue: "Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (ACL 2025), main conference"
url: https://arxiv.org/html/2505.23561
doi: null
arxiv: "2505.23561"
cite: "Yuan, Z., Xu, Y., Shi, J., Zhou, P., & Sun, L. (2025). Merge Hijacking: Backdoor Attacks to Model Merging of Large Language Models. In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (ACL 2025). arXiv:2505.23561."
topics: [fork-merge-security]
added_by: dmarz/fm-merge-poisoning
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "9 (Semantic Scholar, via BadMerging citation list, 2026-10-03)"
code: []
---

## Summary

First backdoor attack on model merging for decoder LLMs. The attacker uploads one model fine-tuned on a surrogate task; once a victim merges it with any other models, the merged model emits an attacker-chosen output when a trigger word appears, on all merged tasks. Four steps: derive a backdoor vector as the difference between a backdoored and a clean model trained on a shadow dataset; sparsify it by magnitude-weighted Bernoulli sampling; rescale it by a factor beta and add it to the base model; then mask-fine-tune on the surrogate task to restore utility without disturbing the backdoor. Tested on Llama-3-8B, Mistral-7B and Qwen-7B across task arithmetic, Model Breadcrumbs, DARE and DELLA.

## Contribution

Shows that one uploaded LLM, built without knowledge of the other models, tasks, merge algorithm or coefficients, gives near-100% trigger success in the merged LLM while keeping utility, and that BadMerging and LoBAM do not transfer to decoder LLMs.

## Key results

- Llama-3-8B, merge of MRPC (surrogate), QNLI, THSD: ASR 100% on all three tasks with task arithmetic; 92-97% with Breadcrumbs, DARE and DELLA.
- Baselines after merging on the same setup: BadNets 0%, BadMerging 0%, LoBAM about 0% at default amplification (100% only at a factor that wrecks utility).
- ASR stays 100% as the number of merged tasks rises from 2 to 6.
- Merge ratio of the malicious model: ASR is low when its ratio is very small, but a ratio of 0.2 (below the 0.33 average for three models) still gives high ASR.
- Rescale factor beta: ASR on MRPC 0% at beta=1, 99.6% at 1.8, 100% at 2; utility falls at beta=3.
- Removing the sparsification step drops ASR to about 33%.
- Works when merged with real public models (NVIDIA OpenMath2-Llama3.1-8B and another Llama 3.1 math model).
- Defences: paraphrasing reduces ASR to about 39-45%; CLEANGEN reduces a fixed-sequence target to 0% but leaves a label-flip target near 70% and costs up to 28 points of utility; fine-pruning leaves ASR at 100%.
- Two independent malicious uploads with different triggers can coexist in one merge (Table 11, appendix).

## Methods and models

Shadow dataset of 125 samples each from SST-2, CoLA, MRPC and SMS Spam; trigger the rare word 'MG'; target a fixed token sequence. LoRA fine-tuning for 4 epochs. Hyperparameters beta=2.0 and two sampling parameters 0.7 and 0.2. Assumes the backdoor vector is nearly orthogonal to benign task vectors.

## Limitations and open questions

Fixed rare-word triggers are partly removed by paraphrasing. Classification-style tasks; only a short case study on GSM8K and code. Defences tested are generic, not merge-aware. Merge ratio below about 0.2 weakens the attack, which is a real lever for a defender.

## Relevance to us

Most direct LLM evidence for Q3: a single returning model can carry a trigger-gated behaviour into the merged parent, invisible on the part's own task. For Q2 the merge-ratio result is the closest thing in this lane to a measured threshold: the attack degrades when the malicious part's weight is small, so a parent that merges many parts with small, equal coefficients raises the attacker's required rescale factor, which in turn costs utility and becomes detectable. For Q1, the attack does not need to know which other parts are merged, so hiding the merge set from the attacker gives little protection against this attack class. Related: [[zhang-2024-badmerging]], [[yin-2024-lobam]], [[zhang-2026-roguemerge]], [[arora-2024-here]].
