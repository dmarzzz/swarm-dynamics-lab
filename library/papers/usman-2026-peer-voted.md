---
id: usman-2026-peer-voted
type: paper
title: Peer-Voted LLM-Agent Stress Tests Find Feed-Induced Lexical Convergence but No Reliable Matched-Exposure Advantage for Distributed Sources
authors: [Rana Muhammad Usman, Dominic Williamson]
year: 2026
venue: arXiv
url: https://arxiv.org/abs/2608.20438
doi: null
arxiv: '2608.20438'
cite: Usman, R. M., & Williamson, D. (2026). Peer-Voted LLM-Agent Stress Tests Find Feed-Induced Lexical Convergence but No Reliable Matched-Exposure Advantage for Distributed Sources. arXiv:2608.20438.
topics: [llm-agent-swarms, sync-consensus]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

PV-SST is a peer-voted synthetic social platform for LLM agents. A frozen, preregistered matched-exposure experiment (448 trials, 112 complete model x topic x seed blocks, four topics, four open-weight families plus three larger variants) compares a feed of previous-round peer posts ranked by peer likes against a topic-only control. The feed raises final-round lexical similarity by +0.0082 TF-IDF cosine (95% CI 0.0043 to 0.0121, n = 64 blocks) in the core panel and +0.0109 (0.0069 to 0.0151, n = 48) in the larger variants. Opposite-side survival falls 3.9 points in the core panel but not conclusively in the larger variants (-1.0 pp, CI -3.1 to 0.4). Holding adversarial impressions fixed, four distributed sources do not reliably move honest-agent stance more than one source (+0.057, CI -0.009 to 0.125 core; -0.040, CI -0.113 to 0.035 larger), failing the preregistered consistency criterion.

## Contribution

A preregistered separation of wording convergence (robust, small) from stance capture (not reliably shown) in a feed-based LLM population. It is the cleanest available control against reading lexical convergence as belief contagion.

## Key results

- Measured: feed-induced lexical convergence in both panels, effect size about 0.01 TF-IDF cosine.
- Measured: no reliable distributed-minus-single source advantage for stance change; the authors state the robust result is lexical convergence, not opinion capture.
- The feed contrast bundles exposure with like-ranking, so a ranking-only effect is not identified (authors' caveat).

## Methods and models

Synthetic social platform with peer voting, four topics, four open-weight model families and three larger variants, block bootstrap and randomisation tests. Code, protocol and data are released (GitHub ranausmanai/synthetic-social-networks, HF dataset ranausmans/synthetic-social-networks; not opened).

## Limitations and open questions

Abstract-level read. Effect sizes are small and the stance measurement details were not read. Synthetic populations only.

## Relevance to us

Splits the "agents copy what they can see" claim in the llm-agent-swarms survey: wording copying replicates (with [[de-marzo-2026-copying]]), belief copying is contested (with [[li-2026-socialization]]). A released harness for a board-style experiment.
