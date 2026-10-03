---
id: wang-2026-botchf
type: paper
title: "BotCHF: camouflage-heterogeneity-aware fusion for social bot detection"
authors: [Xiaoyu Wang, Shuhao Shi, Kai Qiao, Hao Hu, Zihao Liu, Yuxin Zhang, Jihong Han, Bin Yan]
year: 2026
venue: Journal of King Saud University, Computer and Information Sciences
url: https://doi.org/10.1007/s44443-026-01013-w
doi: 10.1007/s44443-026-01013-w
arxiv: null
cite: "Wang, X., Shi, S., Qiao, K., Hu, H., Liu, Z., Zhang, Y., Han, J., & Yan, B. (2026). BotCHF: camouflage-heterogeneity-aware fusion for social bot detection. Journal of King Saud University, Computer and Information Sciences. https://doi.org/10.1007/s44443-026-01013-w"
topics: [swarm-detection, sybil-resistance]
added_by: shadow/sol-w4
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: null  # Semantic Scholar rate-limited at access time
code: []
---

## Summary

Multimodal social bot detector motivated by two observations: LLMs have made bot text human-like, and some bots also camouflage their structural (graph) modality, so the modality that is informative varies account by account ("camouflage heterogeneity"). Existing text-plus-graph methods use a single fusion rule, which misclassifies when one modality is heavily camouflaged, and they do not jointly optimise semantic and structural encoders. BotCHF answers with two stages: an encoding stage using alternating collaborative optimisation that periodically injects fine-tuned semantic features into the graph encoder so semantic and structural representations align progressively, and a fusion stage that keeps separate text and graph branches and adaptively weights their predictions per account (decision-level fusion). Experiments on three real-world datasets show consistent gains over strong baselines, and analysis of the learned fusion weights shows substantial cross-dataset differences in which modality is preferred, which the authors take as evidence that camouflage heterogeneity must be modelled explicitly. Abstract-only read: the publisher page returned a bot challenge and Crossref has no abstract, so the abstract was taken from a search summary; datasets, metrics and effect sizes are not captured.

## Contribution

Per-account adaptive weighting of text versus graph evidence for bot detection, on the premise that which channel an individual bot has camouflaged is itself variable and should be inferred rather than fixed.

## Key results

- Outperforms strong baselines on three real-world bot-detection datasets (numbers not captured).
- Learned fusion weights differ markedly across datasets, indicating dataset-level and account-level shifts in which modality is reliable.

## Methods and models

Text encoder fine-tuned on account posts; graph encoder over the social graph; alternating optimisation that feeds semantic features into the graph encoder; separate branch predictions combined by learned per-account weights. Specific architectures and datasets not read (likely TwiBot-family benchmarks given the authors' prior work, but unverified).

## Limitations and open questions

Abstract-only. Per-account gating is learned from labelled data, so an adversary that camouflages both modalities, or that shifts camouflage over time, is outside the demonstrated regime. Decision-level fusion still depends on at least one modality being honest for each account.

## Relevance to us

Same thread as [[guo-2026-text]] (text-relation fusion under paraphrase attack) with the added point that a sophisticated bot population can choose which modality to camouflage, so detectors need account-level adaptivity. For LLM agent swarms, which can camouflage text perfectly and coordinate their graph, the implicit lesson is that single-platform multimodal fusion has a ceiling; detection likely needs signals the population does not control (infrastructure, timing, cross-platform correlation; compare [[elasky-2026-encoded]] and [[flood-2026-finding]]). The cross-dataset variability of fusion weights is also a warning about transfer of any detector between platforms.
