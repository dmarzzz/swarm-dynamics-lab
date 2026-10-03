---
id: luo-2026-resisting
type: paper
title: 'Resisting Manipulative Bots in Meme Coin Copy Trading: A Multi-Agent Approach with Chain-of-Thought Reasoning'
authors:
- Yichen Luo
- Yebo Feng
- Jiahua Xu
- Yang Liu
year: 2026
venue: Proceedings of the ACM Web Conference 2026 (WWW '26)
url: https://arxiv.org/abs/2601.08641
doi: null
arxiv: '2601.08641'
cite: 'Luo, Y., Feng, Y., Xu, J., & Liu, Y. (2026). Resisting Manipulative Bots in Meme Coin Copy Trading: A Multi-Agent Approach with Chain-of-Thought Reasoning. In Proceedings of the ACM Web Conference 2026 (WWW ''26). arXiv:2601.08641.'
topics:
- swarm-detection
- llm-agent-swarms
added_by: dmarz/sd-onchain
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Copy trading of 'smart money' wallets is the dominant entry strategy in meme coin markets, and adversaries deploy manipulative bots to front-run copiers, conceal positions and fabricate sentiment. The authors build a manipulation-resistant copy-trading system from a multi-agent architecture powered by a multimodal LLM with chain-of-thought reasoning, which beats zero-shot and most statistical baselines on prediction accuracy and all baselines on economic performance, giving an average copier return of 3% per meme coin investment under realistic frictions.

## Contribution

An LLM-agent defence against bot manipulation, i.e. agents used to detect and avoid adversarial bot swarms in a live market.

## Key results

- Average copier return 3% per meme coin investment with the multi-agent LLM system; outperforms baselines (abstract).

## Methods and models

Multi-agent LLM pipeline with multimodal inputs and CoT; evaluation on meme coin copy-trading data with frictions (details not read).

## Limitations and open questions

Abstract-level read; detection of manipulative bots is implicit in trade selection, not reported as a classifier.

## Relevance to us

Example of using agents to screen out manipulative bot swarms; complements measurement in [[szwajcok-2026-meme]] and [[mongardini-2025-midsummer]].
