---
id: chakraborty-2023-possibilities
type: paper
title: On the Possibilities of AI-Generated Text Detection
authors:
- Souradip Chakraborty
- Amrit Singh Bedi
- Sicheng Zhu
- Bang An
- Dinesh Manocha
- Furong Huang
year: 2023
venue: arXiv preprint
url: https://arxiv.org/abs/2304.04736
doi: null
arxiv: '2304.04736'
cite: Chakraborty, S., Bedi, A. S., Zhu, S., An, B., Manocha, D., & Huang, F. (2023). On the Possibilities of AI-Generated Text Detection. arXiv:2304.04736.
topics:
- swarm-detection
added_by: dmarz/sd-ai-content
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 169 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Argues from information theory that AI-text detection remains possible unless human and machine distributions coincide over their whole support, and derives sample-complexity bounds: as machine text approaches human quality, the number of samples needed for detection rises. Experiments on XSum, SQuAD, IMDb and Kaggle FakeNews with GPT-2 through Llama-2-70B and detectors including RoBERTa and GPTZero support multi-sample detection.

## Contribution

The counterpoint to [[sadasivan-2023-can]]: detectability is a matter of sample size, which favours source-level and population-level detection.

## Key results

- Theory (abstract): sample-complexity bounds for detection as a function of distribution closeness.
- Empirical (abstract): consistent with OpenAI observations on sequence length.

## Methods and models

Information-theoretic analysis; experiments across datasets, generators and detectors. Abstract read only.

## Limitations and open questions

Assumes i.i.d. samples from a fixed source; a swarm mixing many models or prompts violates that. Abstract depth.

## Relevance to us

Formal justification for detecting swarms by pooling many posts from a suspected operator rather than judging single posts. Operational versions: [[chen-2024-online]], [[he-2026-degentweb]].
