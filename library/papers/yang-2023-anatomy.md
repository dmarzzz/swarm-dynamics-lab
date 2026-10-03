---
id: yang-2023-anatomy
type: paper
title: Anatomy of an AI-powered malicious social botnet
authors:
- Kai-Cheng Yang
- Filippo Menczer
year: 2023
venue: 'Journal of Quantitative Description: Digital Media (2024)'
url: https://arxiv.org/html/2307.16336
doi: 10.51685/jqd.2024.icwsm.7
arxiv: '2307.16336'
cite: 'Yang, K.-C., & Menczer, F. (2024). Anatomy of an AI-powered malicious social botnet. Journal of Quantitative Description: Digital Media. https://doi.org/10.51685/jqd.2024.icwsm.7. arXiv:2307.16336.'
topics:
- sybil-resistance
- llm-agent-swarms
- swarm-detection
added_by: dmarz/sybil-llm-agents
accessed: '2026-10-03'
read_depth: skim
relevance: 4
citations: 121 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Case study of "fox8", a Twitter botnet of 1,140 accounts that appears to use ChatGPT to write posts. The accounts were found through self-revealing tweets containing "as an ai language model" (searched Oct 2022 to Apr 2023) and then by their shared links to three suspicious sites (fox8.news, cryptnomics.org and a third), and validated by manual annotation. The bots form a dense cluster of fake personas with stolen profile images, crypto-themed descriptions and engineered follower patterns, and they reply to and retweet each other. Coordination patterns expose them, but state-of-the-art LLM-text classifiers fail to separate them from human accounts in the wild.

## Contribution

Early documented evidence of an LLM-powered Sybil botnet in the wild and a released benchmark (fox8-23: 1,140 bots plus 1,140 human accounts from four prior datasets).

## Key results

- Measured: 1,140 bot accounts; largest weakly connected follow component holds 1,036.
- Observed: near-identical follower and following distributions, which the authors read as engineered rather than organic.
- Measured: LLM content detectors fail on these accounts in the wild while coordination features succeed.

## Methods and models

Twitter V2 historical search for the phrase, link-based expansion, collection of up to 200 tweets plus friend and follower lists per account via V1.1 API, comparison with 285 human accounts from each of four datasets. Dataset at github.com/osome-iu/AIBot_fox8.

## Limitations and open questions

Skimmed. Found only because operators leaked the tell-tale phrase; botnets without that slip are undercounted. Twitter API access used here is no longer generally available.

## Relevance to us

Real-world evidence that LLM agent swarms already operate as Sybils and that coordination structure, not content, is the reliable signal. That matches the theoretical point in [[bara-2026-epistemic]] that report content cannot identify ancestry. Lineage: [[ferrara-2016-rise]]; detection arms race: [[feng-2024-what]]; threat framing: [[schroeder-2025-how]].

## Notes from dmarz/sd-bots

Abstract re-read this session (arXiv 2307.16336; published as Journal of Quantitative Description: Digital Media 4, 2024, Crossref count 57 on 2026-10-03). It is the anchor in-the-wild case for LLM botnets: 1,140 accounts found by the self-revealing phrase 'as an AI language model', confirmed by manual annotation, detectable through coordination but not by LLM-text classifiers. Forward citations (Semantic Scholar, 2026-10-03) include the follow-up detectors [[di-paolo-2025-detection]] and [[trokhymovych-2026-adversarial]], synthetic botnets [[qiao-2024-botsim]], and the image-based base rates [[yang-2024-characteristics]] and [[ricker-2024-ai]]. The same coordination-first pivot is used in [[pacheco-2020-uncovering]]. Measurement caution: the discovery method only finds operators who leak the phrase, so it says nothing about prevalence; see [[gallwitz-2022-investigating]] on prevalence claims.

## Notes from dmarz/sd-coordination

This lane catalogued the same source independently (added_by dmarz/sybil-llm-agents, accessed 2026-10-03). Its distinct content:

### Notes from dmarz/sd-coordination

Read the arXiv abstract again this session. For the coordination lane this is the key in-the-wild data point: a ChatGPT-driven botnet of 1,140 accounts that engage each other through replies and retweets was detectable through its coordination patterns while state-of-the-art LLM-content classifiers failed to separate it from humans. Coordination traces ([[pacheco-2021-uncovering]]) beat content detection here. Compare with simulated LLM swarms in [[orlando-2026-emergent]] and [[qiao-2025-botsim]].

## Notes from dmarz/sd-attribution

This lane catalogued the same source independently (added_by dmarz/sybil-llm-agents, accessed 2026-10-03). Its distinct content:

### Notes from dmarz/sd-attribution

Read the arXiv abstract page on 2026-10-03. For attribution, the useful facts are: 1,140 accounts found by heuristics (self-revealing ChatGPT phrases) and validated by hand; the accounts form a dense cluster that replies to and retweets each other; state-of-the-art LLM-content classifiers failed to separate them from human accounts in the wild, while coordination patterns did. This is a wild base-rate datapoint where model attribution came from operator mistakes (leaked refusal phrases), not from fingerprinting. Model-level attribution methods that could replace the phrase heuristic: [[sun-2025-idiosyncrasies]], [[white-2026-black]], [[bruckner-2026-one]]. Same-operator linking without the slip: [[park-2026-cross]], [[chen-2026-do]].
