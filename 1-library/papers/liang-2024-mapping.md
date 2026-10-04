---
id: liang-2024-mapping
type: paper
title: Mapping the Increasing Use of LLMs in Scientific Papers
authors:
- Weixin Liang
- Yaohui Zhang
- Zhengxuan Wu
- Haley Lepp
- Wenlong Ji
- Xuandong Zhao
- Hancheng Cao
- Sheng Liu
- Siyu He
- Zhi Huang
- Diyi Yang
- Christopher Potts
- Christopher D Manning
- James Y. Zou
year: 2024
venue: arXiv preprint
url: https://arxiv.org/abs/2404.01268
doi: null
arxiv: '2404.01268'
cite: Liang, W., Zhang, Y., Wu, Z., Lepp, H., Ji, W., Zhao, X., Cao, H., Liu, S., He, S., Huang, Z., et al. (2024). Mapping the Increasing Use of LLMs in Scientific Papers. arXiv:2404.01268.
topics:
- swarm-detection
added_by: dmarz/sd-ai-content
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 195 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Applies the population-level mixture estimator of [[liang-2024-monitoring]] to 950,965 papers on arXiv, bioRxiv and Nature-portfolio journals (Jan 2020 to Feb 2024). The estimated share of LLM-modified text rises steadily after ChatGPT, fastest in Computer Science (up to 17.5%) and slowest in Mathematics and Nature-portfolio papers (up to 6.3%).

## Contribution

Extends corpus-level estimation from peer reviews to the scientific literature and adds author- and field-level correlates.

## Key results

- Measured (abstract): up to 17.5% LLM-modified content in Computer Science papers; up to 6.3% for Mathematics and Nature portfolio.
- Measured (abstract): higher estimated modification for first authors who post preprints more often, in more crowded research areas, and for shorter papers.

## Methods and models

Distributional GPT quantification (MLE of the mixture weight over word-occurrence distributions) with human references from pre-ChatGPT papers and LLM references generated from them; applied per month and per field. Abstract read only.

## Limitations and open questions

Inherits the reference-corpus assumptions of the base method; the estimate covers abstracts and introductions as modelled in the paper (not checked which sections). Read at abstract depth only.

## Relevance to us

Second application of the corpus-level estimator; useful as a cross-check against the training-free bound of [[kobak-2024-delving]] and the marker-word count of [[gray-2024-chatgpt]].
