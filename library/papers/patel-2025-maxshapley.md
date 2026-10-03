---
id: patel-2025-maxshapley
type: paper
title: 'MaxShapley: Towards Incentive-compatible Generative Search with Fair Context Attribution'
authors:
- 'Sara Patel'
- 'Mingxun Zhou'
- 'Giulia Fanti'
year: 2025
venue: 'arXiv preprint (cs)'
url: https://arxiv.org/html/2512.05958v2
doi: null
arxiv: '2512.05958'
cite: 'Patel, S., Zhou, M., & Fanti, G. (2025). MaxShapley: Towards Incentive-compatible Generative Search with Fair Context Attribution. arXiv preprint arXiv:2512.05958.'
topics:
- sybil-resistance
- llm-agent-swarms
added_by: dmarz/sybil-mechanisms
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: null
code:
- gh-spaddle-boat-maxshapley
---

## Summary

MaxShapley attributes credit for a generative search answer to retrieved source documents so providers can be paid. An LLM decomposes the answer into key points and scores each source's support for each key point; the utility of a subset of sources is a weighted sum over key points of the maximum support any source in the subset provides. For this max-sum utility the Shapley value is computed exactly by sorting and one linear scan per key point, avoiding exponential coalition enumeration. On re-annotated subsets of HotPotQA, MuSiQUE and MS MARCO it matches brute-force Shapley and human relevance labels with far fewer tokens.

## Contribution

A polynomial-time exact Shapley attribution for retrieval-augmented generation, with the max game chosen so that redundant sources do not add value.

## Key results

- On MuSiQUE with GPT-4.1 nano, KernelSHAP needs at least 15x more tokens than MaxShapley to reach comparable Jaccard agreement with ground truth; Monte Carlo methods need 15-20x.
- Kendall tau with FullShapley is strong on MuSiQUE and HotPotQA and moderate on MS MARCO, where all Shapley methods degrade.
- Two semantically equivalent answers received mean LLM-judge scores of 0.3 and 1.0 across 10 deterministic runs, which destabilises whole-answer Shapley baselines; localised key-point judging avoids this.
- Positional bias: with Haiku 3.5, placing relevant sources first raised Jaccard by 0.12, so sources are shuffled before each call.
- Appendix C: in the coverage-game view, Shapley splits a key point's local value equally among the sources covering it.

## Methods and models

Cooperative game over retrieved sources; utility v(S) = sum over key points of weight times max over sources in S of support score. Exact Shapley per max game via sorted scan. Baselines: FullShapley with reference answer access, leave-one-out, optimal transport, Monte Carlo uniform and antithetic, KernelSHAP. About 100 queries per dataset with six sources, two annotators.

## Limitations and open questions

The authors flag robustness against adversarial manipulation of key-point decomposition as future work and do not analyse strategic source providers. My own inference, not a claim in the paper: because the max game splits a key point's value equally among all sources that cover it, a provider who submits k near-duplicate copies of a supporting document would receive k/(k+1) of that key point's value rather than 1/2. Splitting is therefore profitable unless sources are deduplicated or clustered by owner, which the paper recommends only when rewarding corroboration. I skimmed the intro, setup, results, conclusion and the coverage-game appendix, not the full appendices.

## Relevance to us

Attribution among many contributors (documents, tools, sub-agents) is where false-name manipulation of the Shapley value shows up in LLM systems. The equal-split rule is the same vulnerability shown in [[conitzer-2010-using]] and addressed by [[ohta-2008-anonymity]]; any swarm that pays agents by Shapley attribution needs owner-level aggregation or an anonymity-proof variant. Compare [[mazorra-2023-optimality]] on Shapley cost sharing under Sybil strategies.
