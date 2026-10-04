---
id: liang-2024-monitoring
type: paper
title: 'Monitoring AI-Modified Content at Scale: A Case Study on the Impact of ChatGPT on AI Conference Peer Reviews'
authors:
- Weixin Liang
- Zachary Izzo
- Yaohui Zhang
- Haley Lepp
- Hancheng Cao
- Xuandong Zhao
- Lingjiao Chen
- Haotian Ye
- Sheng Liu
- Zhi Huang
- Daniel A. McFarland
- James Y. Zou
year: 2024
venue: ICML 2024 (PMLR 235)
url: https://arxiv.org/html/2403.07183
doi: null
arxiv: '2403.07183'
cite: 'Liang, W., Izzo, Z., Zhang, Y., Lepp, H., Cao, H., Zhao, X., Chen, L., Ye, H., Liu, S., Huang, Z., et al. (2024). Monitoring AI-Modified Content at Scale: A Case Study on the Impact of ChatGPT on AI Conference Peer Reviews. Proceedings of the 41st International Conference on Machine Learning (ICML), PMLR 235, 29575-29620. arXiv:2403.07183.'
topics:
- swarm-detection
added_by: dmarz/sd-ai-content
accessed: '2026-10-03'
read_depth: full
relevance: 5
citations: 295 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Introduces "distributional GPT quantification": instead of classifying each document, fit a two-component mixture (human-written vs LLM-generated) to a whole corpus by maximum likelihood over word-occurrence probabilities, using adjectives as the vocabulary. Reference distributions come from pre-ChatGPT human text and from LLM output produced with the same writing instructions. Applied to AI-conference peer reviews, it estimates that 6.5% to 16.9% of review sentences after ChatGPT were substantially LLM-modified, while Nature-portfolio reviews show no significant rise.

## Contribution

The reference method for population-level estimation of machine-written text. It shows that a corpus-level mixture estimate is more accurate and vastly cheaper than counting per-item detector verdicts, and it became the template reused for scientific papers [[liang-2024-mapping]] and for consumer complaints, press releases and job ads [[liang-2025-widespread]].

## Key results

- Measured: estimated LLM-modified fraction (alpha) rose from 1.6% to 10.6% at ICLR (2023 to 2024), 1.9% to 9.1% at NeurIPS, 2.4% to 6.5% at CoRL; EMNLP 2023 was 16.9%. Nature-portfolio reviews showed no significant change.
- Measured on semi-synthetic mixtures with known alpha: prediction error below 1.8% in distribution (ICLR 2023) and below 2.4% out of distribution (NeurIPS 2022, CoRL 2022).
- Measured: against a fine-tuned BERT classifier and two published detectors, in-distribution estimation error fell 3.4x (6.2% to 1.8%) and out-of-distribution error 4.6x (11.2% to 2.4%); inference cost about 7 orders of magnitude lower per sentence.
- Measured: "commendable", "meticulous", "intricate" became 9.8x, 34.7x and 11.2x more likely per sentence in ICLR 2024 reviews.
- Measured correlates: higher alpha in reviews submitted within 3 days of the deadline, without "et al." citations, from reviewers who reply less to rebuttals, with low self-rated confidence, and in "convergent" reviews closest to the per-paper embedding centroid (a homogenisation signal).
- Robustness check: LLM proofreading of human reviews raises alpha only slightly; LLM expansion of a human outline is detected at close to its true fraction.

## Methods and models

Mixture model (1 - alpha) P + alpha Q over documents represented as sets of adjectives (technical keywords removed); occurrence probabilities estimated from human reviews (ICLR 2018-2022) and GPT-4 generated reviews written from the same papers and instructions; MLE for alpha; 30,000 bootstrap samples for 95% CIs. Data: OpenReview reviews of ICLR, NeurIPS, CoRL, EMNLP plus 15 Nature-portfolio journals. Appendices cover adverbs, verbs, nouns, alternative LLMs (GPT-3.5, LLaMA-2, Claude 2.1) and a sample-size analysis; I read the main text and methods, not every appendix table.

## Limitations and open questions

Assumes the reference LLM corpus resembles what real users produce; the authors note that the method cannot separate a reviewer expanding bullet points from one generating a full review, and that shifts in the non-native writer population or topic drift could bias alpha. It gives no per-document labels, so it cannot identify who used an LLM. A deliberate adversary who rewrites to match human word statistics would be under-counted (not tested).

## Relevance to us

The core statistical tool for answering "what fraction of this platform is machine-written" without trusting per-item detectors, which [[sadasivan-2023-can]] and [[krishna-2023-paraphrasing]] show are fragile. For swarm detection the same mixture framing can be applied to an account's posts or a hashtag's traffic, and the homogenisation result connects to the convergence signal that coordination detectors use. Compare the training-free excess-word estimator [[kobak-2024-delving]] and per-item detector estimates such as [[sun-2024-are]] and [[la-cava-2025-machines]].
