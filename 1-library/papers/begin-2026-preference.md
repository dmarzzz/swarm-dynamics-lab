---
id: begin-2026-preference
type: paper
title: Preference Optimization Drives Monoculture in LLM Prediction Markets
authors: [James Begin, Brendan Gho, Suman Muppavarapu, Tyson Tsay, Atharva Mohan, Afnan Shaik, Ruizhe Li, Vasu Sharma, Archana Vaidheeswaran]
year: 2026
venue: arXiv
url: https://arxiv.org/html/2606.26583
doi: null
arxiv: '2606.26583'
cite: Begin, J., Gho, B., Muppavarapu, S., Tsay, T., Mohan, A., Shaik, A., Li, R., Sharma, V., & Vaidheeswaran, A. (2026). Preference Optimization Drives Monoculture in LLM Prediction Markets. arXiv:2606.26583.
topics: [llm-agent-swarms, collective-decision]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

LLM agents trade binary TruthfulQA questions in an LMSR prediction market (Llama 3.1 8B Instruct primary, 3 rounds, 50 questions per trial). Same-model honest agents have pairwise error correlation of about 0.70, so 10 agents equal about 1.38 independent forecasters (N_eff = N / (1 + (N - 1) rho)). The all-honest 10-agent market reaches 67.6% against 70.2% for one standalone agent. Accuracy stays flat (66.0 to 69.6%) and empirical N_eff saturates at 1.41 to 1.48 from N = 5 to N = 40. Identical-SFT ablations (AllenAI Tulu 3 at 8B and 70B, a Princeton NLP pair) attribute a rise in error correlation of +0.24 to +0.46 to preference optimisation. Mixing model families lowers rho from 0.68 to 0.40; role diversity lowers it from 0.60 to 0.44.

## Contribution

An independent measurement that the effective number of same-model agents is flat in N (a hard ceiling, not slow growth), in a market aggregator rather than debate, plus a causal attribution to DPO.

## Key results

- N_eff about 1.4 for same-model agents, flat from N = 5 to 40 (measured).
- Same-model correlation about 1.7 times cross-model; four 7-9B families tested.
- Cross-model mixing gives the largest decorrelation; role prompts also decorrelate at no accuracy cost.

## Methods and models

LMSR market, heuristic betting rule, wealth persists over 50 questions; Pearson correlation of binary error vectors; Kish-style N_eff used as a proxy for market aggregation (not derived from LMSR, authors' caveat). Read: introduction, setup, sections 4 and 6 in the arXiv HTML.

## Limitations and open questions

Binary QA only, TruthfulQA misconceptions may inflate shared errors, agents are overconfident, models up to 70B.

## Relevance to us

Third independent group for the flat effective-N ceiling beside [[bertalanic-2026-ringelmann]] and [[kohli-2026-nine]]; its N sweep (5 to 40) is the closest prior for an N_eff-versus-N curve. Role diversity as a decorrelator qualifies "only cross-family helps".
