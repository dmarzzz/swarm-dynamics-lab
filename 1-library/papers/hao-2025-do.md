---
id: hao-2025-do
type: paper
title: Do Spammers Dream of Electric Sheep? Characterizing the Prevalence of LLM-Generated Malicious Emails
authors:
- Wei Hao
- Van Tran
- Vincent Rideout
- Zixi Wang
- AnMei Dasbach-Prisk
- M. H. Afifi
- Junfeng Yang
- Ethan Katz-Bassett
- Grant Ho
- Asaf Cidon
year: 2025
venue: ACM Internet Measurement Conference (IMC 2025)
url: https://www.cs.columbia.edu/~junfeng/papers/ai-email-imc25.pdf
doi: 10.1145/3730567.3732922
arxiv: null
cite: Hao, W., Tran, V., Rideout, V., Wang, Z., Dasbach-Prisk, A., Afifi, M. H., Yang, J., Katz-Bassett, E., Ho, G., & Cidon, A. (2025). Do Spammers Dream of Electric Sheep? Characterizing the Prevalence of LLM-Generated Malicious Emails. In Proceedings of the 2025 ACM Internet Measurement Conference (IMC 25), Madison, WI, USA. ACM. https://doi.org/10.1145/3730567.3732922
topics:
- swarm-detection
added_by: dmarz/sd-ai-content
accessed: '2026-10-03'
read_depth: full
relevance: 5
citations: 5 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Joint study with Barracuda Networks of 481,558 real malicious emails (Feb 2022 to Apr 2025). Three detectors (fine-tuned RoBERTa, RAIDAR rewrite-distance, Fast-DetectGPT) are calibrated on pre-ChatGPT mail, which is assumed human. RoBERTa has near-zero false positives on that period, so its post-ChatGPT detections are a floor: at least 51% of spam and 14% of business email compromise (BEC) in April 2025 is LLM-generated. Top spammers use LLMs to produce reworded variants of one message, apparently to evade volume filters.

## Contribution

First large-scale in-the-wild measurement of attacker LLM use, and a clean template for prevalence estimation: use the pre-release period as a free negative set to measure each detector's false-positive rate, then treat a near-zero-FPR detector's later hit rate as a lower bound.

## Key results

- Measured false-positive rates on pre-ChatGPT months: RoBERTa 0.3% (spam) and 0.4% (BEC); Fast-DetectGPT 4.3% and 1.4%; RAIDAR 11.7% and 19.1%.
- Measured with RoBERTa: LLM-generated share at least 16.2% of spam and 7.6% of BEC in April 2024, rising to 51% of spam and 14.4% of BEC in April 2025.
- Measured: LLM-generated spam is more formal, more grammatical and uses more sophisticated language than human spam, but is not more urgent; 82.7% of LLM spam is promotional versus 40.9% of human spam.
- Measured: among the top-100 post-ChatGPT spam senders, MinHash clustering found five large clusters (668-1263 emails); two were 78.9% and 52.1% LLM-flagged versus a 7.8% post-ChatGPT average, and samples were reworded versions of one message.

## Methods and models

Barracuda-labelled spam and BEC (two commercial detectors, over 99% precision by analyst validation), English, deduplicated, at least 250 characters; final 239,145 spam and 242,413 BEC. Training: Feb-Jun 2022 emails as human plus Mistral-7B rewrites as LLM; RAIDAR rewrites with Llama-2-7B. Characterisation set requires two of three detectors to agree. LDA topics, Llama-3.1-8B judged formality and urgency, Flesch, grammar-error rate. KS tests pre vs post.

## Limitations and open questions

Depends on Barracuda's evolving malicious-email filters, so changes in what is flagged could move the rate. LLM-side training data are Mistral rewrites of human spam, a proxy for real attacker workflows, so recall is unknown and the 51% is a floor. Characterisation stops at April 2024 for compute reasons.

## Relevance to us

The strongest measured base rate for adversarial machine text in the wild, and it shows the swarm-like pattern directly: one operator generating many paraphrased variants to defeat duplicate-volume filters. That means near-duplicate clustering plus an LLM detector inside each cluster is a workable swarm detector. Calibration design matches [[brooks-2024-rise]] and [[russell-2025-ai]]; cluster-level evasion links to [[krishna-2023-paraphrasing]].
