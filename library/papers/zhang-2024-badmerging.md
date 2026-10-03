---
id: zhang-2024-badmerging
type: paper
title: "BadMerging: Backdoor Attacks Against Model Merging"
authors: ["Jinghuai Zhang", "Jianfeng Chi", "Zheng Li", "Kunlin Cai", "Yang Zhang", "Yuan Tian"]
year: 2024
venue: "Proceedings of the 2024 ACM SIGSAC Conference on Computer and Communications Security (CCS '24)"
url: https://arxiv.org/html/2408.07362
doi: "10.1145/3658644.3690284"
arxiv: "2408.07362"
cite: "Zhang, J., Chi, J., Li, Z., Cai, K., Zhang, Y., & Tian, Y. (2024). BadMerging: Backdoor Attacks Against Model Merging. In Proceedings of the 2024 ACM SIGSAC Conference on Computer and Communications Security (CCS '24), Salt Lake City, UT, USA. https://doi.org/10.1145/3658644.3690284"
topics: [fork-merge-security]
added_by: dmarz/fm-merge-poisoning
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: null
code: []
---

## Summary

First backdoor attack designed for model merging. The authors measure that classical backdoors (BadNets, TrojanNN, Dynamic Backdoor) reach about 100% attack success on the standalone model but under 30% after merging, because merging scales the adversary's task vector by a small coefficient. BadMerging fixes this in two stages: optimise a universal trigger against the pre-trained model (which approximates the merge when the adversary's coefficient is near 0), then fine-tune with a feature-interpolation loss so triggered inputs map to the target class at every coefficient between 0 and 1. An off-task variant backdoors classes in tasks other parties contribute, using shadow class names and a few reference images. One malicious model among several suffices.

## Contribution

Shows that contributing a single model to a merge is enough to control the merged model's behaviour on chosen inputs, without knowing the other models, the merge algorithm or the coefficients, and that standard backdoor defences do not catch it.

## Key results

- On-task attack, CLIP ViT-B/32, 6 merged tasks: ASR 98.14% (TA), 99.26% (TIES), 96.71% (RegMean), 99.48% (AdaMerging), 99.15% (Surgery) with CIFAR100 as adversary task; existing attacks stay below about 30%.
- Off-task attack (target class 'Acura RL' in another party's Cars196 task): ASR 89-96% across five merge algorithms; above 90% for other target classes and tasks.
- Utility preserved: backdoored merged accuracy within about 0.2 points of clean merged accuracy (for example TA 76.51 clean versus 76.39 backdoored).
- ASR stays above 92% as merged task count goes from 2 to 8; above 90% when merging many same-task models with simple averaging, where classical attacks fall to 0.
- Measured near-orthogonality of task vectors from different domains: mean cosine similarity 0.042.
- Knowing the benign task vectors raises on-task ASR only from 98.14% to 100%, so the attacker loses little by being blind.
- Neural Cleanse anomaly index about 1.2 for backdoored models, below the detection threshold of 2; fine-pruning and Scale-up also fail (appendix, reported in main text).
- 5 to 15 backdoors in one model: average ASR drops only from 98.8% to 96.5%.

## Methods and models

CLIP ViT-B/32, B/16, L/14 fine-tuned on 13 image classification tasks; text encoder frozen. Merge algorithms: task arithmetic, simple average, TIES, RegMean, AdaMerging, Surgery. Trigger 1% (on-task) or 1.5% (off-task) of pixels. Feature-interpolation loss mixes features from the pre-trained and adversary encoders with random alpha. 300 shadow classes from ImageNet-1k, 5 reference images. Code: github.com/jzhang538/BadMerging (not opened).

## Limitations and open questions

Image classification with patch triggers only; decoder LLMs were not tested (and [[yuan-2025-merge]] reports BadMerging's loss does not transfer to them). ASR drops 8-10 points on ViT-L/14. Defences tested are generic backdoor defences, not merge-aware ones like [[yang-2025-mitigating]].

## Relevance to us

Central for Q3 and Q2. For Q3 it is the clearest measured case of a single corrupted part, blind to the rest, controlling the merged whole, including tasks that other honest parts brought back (off-task). For Q2 it shows that weighting by coefficient and averaging over more parts do not create a threshold: one part in eight still gives over 92% ASR, because the attack is built to work at every coefficient. The off-task result matters for fork-merge agents: the corrupted explorer can plant behaviour in domains it never visited. Related: [[yin-2024-lobam]], [[yuan-2025-merge]], [[zhang-2026-roguemerge]], [[bagdasaryan-2020-how]], [[arora-2024-here]].
