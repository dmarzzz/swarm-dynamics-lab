---
id: guo-2026-text
type: paper
title: "Text–relation joint modeling improves the robustness of Chinese social bot detection against paraphrasing attacks"
authors: [Shuaifeng Guo, Yunqian Zhou]
year: 2026
venue: Scientific Reports
url: https://www.nature.com/articles/s41598-026-68571-x
doi: 10.1038/s41598-026-68571-x
arxiv: null
cite: "Guo, S., & Zhou, Y. (2026). Text–relation joint modeling improves the robustness of Chinese social bot detection against paraphrasing attacks. Scientific Reports. https://doi.org/10.1038/s41598-026-68571-x"
topics: [swarm-detection, sybil-resistance]
added_by: shadow/sol-w4
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: null  # Semantic Scholar rate-limited at access time
code: []
---

## Summary

Proposes TRJD-AT, a Text-Relation Joint Detection framework with adversarial training for social bot detection on Chinese platforms (Weibo), built on the asymmetry that an account owner can cheaply rewrite post text but relational structure (who follows and interacts with whom) is costly to change. Architecture: a Chinese MacBERT text encoder, a two-layer heterogeneous graph attention network over user-post publication and user-user follow edges, and a per-account gated fusion that weights the textual and relational representations; Fast Gradient Method perturbations on the text-embedding layer during training as a regulariser, with the authors explicit that embedding-space perturbation differs from sentence-level paraphrase so transfer is tested, not assumed. Evaluation uses a three-tier paraphrasing-attack protocol with explicit budgets and semantic constraints: synonym substitution, generative paraphrase rewriting, and benign-token insertion, applied at post level with metrics at account level. On the Chinese Weibo Social Bot dataset, clean macro-F1 is 0.891 for TRJD-AT versus 0.867 for MacBERT plus MLP; under the default Tier 2 (generative paraphrase) attack, macro-F1 drops by 5.6 points for TRJD-AT versus 13.4 points for the text-only baseline. Also evaluated on TwiBot-22. A density analysis shows relational information is less informative for accounts with sparse interaction histories, motivating density-aware deployment. Motivation cites Yang and Menczer's 1,140-account ChatGPT-driven botnet on X that evaded detectors and Wack et al.'s evidence of state generative propaganda. We read the introduction and the first related-work section; method details, full results tables and ablations were not read.

## Contribution

Frames paraphrasing robustness as a separate evaluation axis for bot detection and shows, under a controlled Chinese paraphrase protocol, that fusing relational structure with text roughly halves the robustness loss suffered by text-only detectors, because the adversary's cheap rewrite does not touch the graph.

## Key results

- Clean macro-F1: 0.891 (TRJD-AT) versus 0.867 (MacBERT + MLP) on Chinese Weibo Social Bot dataset.
- Under Tier 2 generative paraphrase: drop of 5.6 points versus 13.4 points for the text-only baseline.
- Relational signal contributes less for low-interaction-density accounts (density-based analysis).
- Experiments also run on TwiBot-22 to characterise roles of relational modelling, fusion and FGM separately.

## Methods and models

MacBERT encoder; two-layer HGAT over heterogeneous user-post and user-user graph; gated fusion at account level; FGM adversarial training on text embeddings; three-tier attack protocol; datasets: Chinese Weibo Social Bot dataset and TwiBot-22; metric macro-F1 at account level.

## Limitations and open questions

Attacks are text-only by design, so the paper demonstrates robustness to the cheap attack and not to an adversary who also shapes the relational graph (which coordinated LLM agent swarms can do, since they control many accounts). FGM is an embedding-space proxy for paraphrase. Sparse-history accounts, exactly where new sybils live, are where the relational channel is weakest. Benchmarks are static snapshots.

## Relevance to us

Directly on swarm-detection and sybil-resistance: the central design principle, trust the signal the adversary cannot cheaply rewrite, is the right starting point for detecting LLM agent populations whose text is arbitrarily fluent, and the measured gap (5.6 versus 13.4 point drop) quantifies how much relational structure buys. The limitation is equally important for us: an agent swarm that coordinates its own follow and interaction graph can attack the relational channel too, which pushes detection toward signals outside the platform (timing, infrastructure, side channels, see [[elasky-2026-encoded]]) or toward the sparse-density regime the paper flags as hard. Baseline for pre-LLM bot structure: [[li-2024-social]].
