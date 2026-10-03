---
id: bartnicki-2026-compression
type: paper
title: Compression-Based Behavioral Similarity for Open-World Sybil Discovery on Ethereum
authors:
- Michał Bartnicki
- Jarosław A. Chudziak
year: 2026
venue: arXiv preprint (cs.LG)
url: https://arxiv.org/abs/2607.27370
doi: null
arxiv: '2607.27370'
cite: Bartnicki, M., & Chudziak, J. A. (2026). Compression-Based Behavioral Similarity for Open-World Sybil Discovery on Ethereum. arXiv preprint arXiv:2607.27370.
topics:
- swarm-detection
- sybil-resistance
added_by: dmarz/sd-onchain
accessed: '2026-10-03'
read_depth: full
relevance: 5
citations: null
code: []
---

## Summary

Proposes training-free Sybil candidate discovery on Ethereum: each wallet history is encoded as a symbolic Transaction Grammar (16 log-binned inter-arrival rhythm tokens, a discretised EVM trace-shape token, and a 4-byte function-selector intent token), and wallets are compared by gzip Normalised Compression Distance (NCD). Sybils from the Hop airdrop list (1,755 after filtering), Hop organic users (9,204) and Dune-labelled arbitrage MEV bots (3,202) form the dataset. A label-informed Blind-Spot protocol strips interactions with class-revealing contracts (25.5% of transaction volume). With the full grammar, NCD 1-NN accuracy is 0.70 (class prior 0.33), top-10 Sybil neighbourhood purity 0.75 and recall 0.92; XGBoost reaches 0.795 but degrades to 0.816 Sybil recall at 50% synthetic camouflage noise while NCD stays at 0.981.

## Contribution

Reframes on-chain Sybil detection from closed-set classification to seed expansion by behavioural similarity, which finds wallets with no shared funding link. Also an explicit warning that label leakage through high-signal contracts inflates published detectors, in the spirit of TESSERACT.

## Key results

- Within-class similarity gap Sybil minus Organic grows when leakage is removed (rhythm_only: 0.089 raw to 0.115 leakage-free; Cliff's delta 0.39 to 0.48).
- Leakage-free accuracy (10 seeds): XGBoost 0.795 (full tokens), BiLSTM about 0.70, NCD 1-NN 0.703, TF-IDF+LR 0.663.
- Top-10 neighbourhood: purity 0.754, Sybil recall 0.922 for full tokens vs 0.505/0.813 for TF-IDF cosine on rhythm+intent.
- Temporal split: cross-period 1-NN 0.619, top-10 recall falls from 0.933 (within period) to 0.782.
- Camouflage (rhythm jitter, organic chaff, local shuffles) at alpha=50%: NCD recall 0.981 vs XGBoost 0.816; perturbations are synthetic, not observed evasion.
- Full NCD matrix for 404,550 pairs takes about 90 s on an M1 laptop; MinHash/LSH candidate generation keeps 1-NN accuracy while cutting lookup time.

## Methods and models

Hop Protocol airdrop labels (organic, Sybil) plus Dune arbitrage-bot labels cut at the 13 May 2022 snapshot; traces from Google BigQuery; minimum-history threshold; Blind-Spot filter on contract support, class purity and class entropy. NCD with gzip; k-NN retrieval; spectral and agglomerative clustering (ARI/NMI moderate); baselines XGBoost, TF-IDF+logistic regression, hierarchical BiLSTM.

## Limitations and open questions

One airdrop (Hop), whose Sybil labels themselves came from community reports and funding heuristics, so the detector is scored against heuristic labels. Blind-Spot needs labels, so it is an evaluation control rather than a deployable filter. No GNN baseline. Camouflage is synthetic. Cross-campaign transfer untested. Three-class setting with balanced sampling, so the 0.33 prior is not the field base rate.

## Relevance to us

The cleanest method we have for 'same script, different wallets': compression similarity over action grammars is chain-agnostic and could be pointed at LLM-agent action logs or API call sequences. The leakage finding is a general caution for any agent-swarm detector benchmark. Pairs with the companion classifier study [[bartnicki-2026-modeling]], the labelled Hop data used in [[luo-2025-toward]], and feature-based detectors [[liu-2025-detecting]] and [[niedermayer-2024-detecting]].
