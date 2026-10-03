---
id: nilayam-2026-heterogeneous
type: paper
title: 'Heterogeneous LLM Debate Under Adversarial Peers: Honest Gains, Replacement Costs, and Resilience'
authors:
- Prashanti Nilayam
- Kiran Kumar Ramanna
- Prashil Tumbade
- Sankalp Nayak
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2606.19826
doi: null
arxiv: '2606.19826'
cite: 'Nilayam, P., Ramanna, K. K., Tumbade, P., & Nayak, S. (2026). Heterogeneous LLM Debate Under Adversarial Peers: Honest Gains, Replacement Costs, and Resilience. arXiv preprint arXiv:2606.19826.'
topics:
- fork-merge-security
- llm-agent-swarms
added_by: dmarz/fm-bft-aggregation
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Measures whether a peer from a different model family in a multi-agent debate mainly corrects honest agents or mainly carries adversarial influence. Compares homogeneous panels, panels with an honest heterogeneous peer, panels with an adversarial heterogeneous peer, and panels already containing a malicious same-family peer, across four model families and three reasoning benchmarks. For Llama-3.1-70B defenders on MATH-hard, the harmful-revision rate is 89 percent in a homogeneous panel, 35 percent with an honest heterogeneous peer, and 90 percent with an adversarial one. With a same-family adversary present, adding an honest heterogeneous peer cuts the flip rate on initially correct items from 31 to 6 percent.

## Contribution

Quantifies heterogeneity as both an attack surface and a defence in LLM debate.

## Key results

- Measured (per abstract): harmful-revision 89 percent (homogeneous) vs 35 percent (honest heterogeneous peer) vs 90 percent (adversarial heterogeneous peer), Llama-3.1-70B on MATH-hard.
- Measured (per abstract): flip rate on initially correct items 31 percent under a same-family adversary, 6 percent once an honest heterogeneous peer is added.
- Reported: sign of the effect holds across families and benchmarks; magnitude varies.

## Methods and models

Matched and contaminated debate panels; revision and flip-rate metrics. Only the abstract was read.

## Limitations and open questions

Abstract-level reading; single adversary per panel.

## Relevance to us

Q2. Evidence for deliberate diversity among the parts that review a returning sub-agent: one honest reviewer from a different model family sharply reduces the damage a same-family corrupted part does. It also measures how fragile homogeneous panels are, which is the default when a parent forks copies of itself. Related: [[ron-2026-n-version]], [[kim-2025-correlated]].
