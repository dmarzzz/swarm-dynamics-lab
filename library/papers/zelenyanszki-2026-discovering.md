---
id: zelenyanszki-2026-discovering
type: paper
title: Discovering Persistent Behavioural Patterns for Interpretable Blockchain Forensics
authors:
- Dorottya Zelenyanszki
- Zhe Hou
- Kamanashis Biswas
- Vallipuram Muthukkumarasamy
year: 2026
venue: arXiv preprint (cs)
url: https://arxiv.org/abs/2608.12864
doi: null
arxiv: '2608.12864'
cite: Zelenyanszki, D., Hou, Z., Biswas, K., & Muthukkumarasamy, V. (2026). Discovering Persistent Behavioural Patterns for Interpretable Blockchain Forensics. arXiv preprint arXiv:2608.12864.
topics:
- swarm-detection
added_by: dmarz/sd-onchain
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Application-agnostic framework for finding persistent behavioural patterns in blockchain activity. Each action becomes a 'behaviour sentence' enriched with contract, token and market context; sentence embeddings capture single actions and sequence embeddings capture each user's behaviour over time. Discovered communities are profiled by motifs, routines, temporal dynamics, entity exposure and suspiciousness evidence. On over 30 million Ethereum transactions the framework recovers DEX trading, NFT activity, phishing, bot operations, oracle manipulation and rug pulls, and many patterns stay stable across independent observation windows.

## Contribution

An unsupervised, interpretable alternative to labelled bot classifiers, with persistence across windows as a criterion for attributing long-running operators.

## Key results

- 30M+ Ethereum transactions; bot-operation communities among recovered patterns; many patterns persist across windows (no numbers in abstract).

## Methods and models

Text-like encoding of transactions; two-level embeddings; community detection and profiling.

## Limitations and open questions

Abstract-level read; no precision figures in abstract.

## Relevance to us

Same idea as [[bartnicki-2026-compression]] (wallet behaviour as language) with learned embeddings; persistence across windows is a useful operator-attribution signal for agent swarms. Found by forward citation of [[niedermayer-2024-detecting]].
