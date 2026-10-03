---
id: sun-2024-are
type: paper
title: Are We in the AI-Generated Text World Already? Quantifying and Monitoring AIGT on Social Media
authors:
- Zhen Sun
- Zongmin Zhang
- Xinyue Shen
- Ziyi Zhang
- Yule Liu
- Michael Backes
- Yang Zhang
- Xinlei He
year: 2024
venue: ACL 2025 (main)
url: https://arxiv.org/html/2412.18148
doi: null
arxiv: '2412.18148'
cite: Sun, Z., Zhang, Z., Shen, X., Zhang, Z., Liu, Y., Backes, M., Zhang, Y., & He, X. (2024). Are We in the AI-Generated Text World Already? Quantifying and Monitoring AIGT on Social Media. In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (ACL 2025). arXiv:2412.18148.
topics:
- swarm-detection
added_by: dmarz/sd-ai-content
accessed: '2026-10-03'
read_depth: full
relevance: 4
citations: 49 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Collects about 2.4M posts from Medium, Quora and Reddit (Jan 2022 to Oct 2024), builds a training benchmark (AIGTBench) from public AIGT datasets plus platform texts rewritten or answered by 12 LLMs, picks the best of 14 detectors (a fine-tuned Longformer, called OSM-Det) and tracks the AI Attribution Rate (share of posts it flags). Medium rose from 1.77% to 37.03%, Quora from 2.06% to 38.95%, Reddit only from 1.31% to 2.45%.

## Contribution

First multi-platform longitudinal prevalence estimate for social media text, with per-platform false-positive calibration on pre-2022 data, and analysis of who posts the flagged content.

## Key results

- Measured: OSM-Det accuracy 0.979 and F1 0.980 on the AIGTBench test split; the GPT-2-era OpenAI detector scored F1 0.484.
- Measured: false-positive rates on pre-ChatGPT human posts of 1.82% (Medium), 1.36% (Quora), 1.70% (Reddit); Reddit AAR stayed below the FPR before Nov 2022.
- Measured: AAR jumps start December 2022 on all three platforms; Quora peaks in August 2023 and then declines (authors speculate a link to Poe).
- Measured: on Medium, Technology and Software Development topics have the highest AAR; predicted-AI posts get fewer likes and comments; authors with at most 1,000 followers have the highest mean AAR.
- Measured: generalisation to 9 unseen LLMs with accuracy 0.925 to 0.999 on rewritten platform text.

## Methods and models

Scraped Medium articles, Quora answers and Reddit comments; filtered by length; training data mixes open AIGT/SFT datasets with 2018-2021 platform text (assumed human) and LLM polish/generate/answer tasks. Metric-based detectors (log-likelihood, rank, entropy, GLTR, DetectGPT, NPR via GPT-2 medium) and model-based ones (OpenAI and ChatGPT detectors, ConDA, GPTZero API, CheckGPT, LM-D). Integrated Gradients and Shapley values for interpretation. Code and data: github.com/TrustAIRLab/AIGT_on_Social_Media.

## Limitations and open questions

AAR is a raw classifier rate, not a bias-corrected prevalence: it includes about 1.4-1.8% false positives and misses whatever the detector misses (no adversarial or human-edited test on the wild data). Training generations are "polish" and "answer" prompts, so heavy human editing or bot-farm style prompts may look different. English only; deeper analysis only for Medium.

## Relevance to us

Gives base rates for machine-written text on open publishing platforms, which bounds how much a swarm could already hide in the crowd. The Medium/Quora versus Reddit gap (about 37% vs 2.5%) shows that platform norms and text length change prevalence by an order of magnitude. Cross-check with [[la-cava-2025-machines]] (Reddit, zero-shot detector, conservative threshold) and the corpus-level estimators [[liang-2024-monitoring]] and [[kobak-2024-delving]].
