---
id: yang-2026-when
type: paper
title: "When Is Emergent Consensus Real? A Measured Coupling Gain and a Validity Diagnostic for LLM Agent Societies"
authors:
- "Dongxu Yang"
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2606.22203
doi: null
arxiv: "2606.22203"
cite: "Yang, D. (2026). When Is Emergent Consensus Real? A Measured Coupling Gain and a Validity Diagnostic for LLM Agent Societies. arXiv preprint arXiv:2606.22203."
topics:
- llm-agent-swarms
- sync-consensus
- criticality-measurement
added_by: dmarz/llm-agent-swarms-recent-audit
accessed: '2026-10-03'
read_depth: skim
relevance: 5
citations: "1 (Semantic Scholar, 2026-10-03); OpenAlex not retrieved (HTTP 429)"
code: []
---
## Summary

Argues that LLM "agent society" papers report emergent consensus or polarization without a measured control parameter or a test of whether the outcome is social at all. The paper defines a coupling gain gamma per agent, measured counterfactually: present a neighbour's opinion v over a grid of values, regress the agent's updated opinion u(v) on v, and take the slope. Gamma is stable and model-specific (five frontier models span 0.15 to 0.43, n = 20, CIs at most 0.025 wide), invariant to paraphrase, and about equal for a social neighbour and a numeric anchor, so it measures evidence coupling, not something uniquely social. With measured coefficients, the Friedkin-Johnsen model organises consensus vs pluralism, and a signed-Laplacian/structural-balance criterion organises polarization. No tested model shows spontaneous backfire (beta <= 0), so default societies do not self-polarize. A randomized-initial-condition diagnostic (slope and bias of final vs initial opinion) separates genuine averaging from model-prior artifacts; applied to [[chuang-2023-simulating]] it finds averaging on debatable claims but prior artifacts on settled facts. Pairwise gamma does not predict multi-neighbour outcomes, while a group coupling measured in the same modality does.

## Contribution

A measurement-first methodology for LLM opinion dynamics: one measured coefficient, classical linear opinion models as the theory, and a validity test against prior artifacts. It is a constructive companion to the critiques of [[barrie-2025-emergent]] and [[zhou-2025-pimmur]], and a check on the consensus findings of [[chuang-2023-simulating]] and [[de-marzo-2024-ai]].

## Key results

- Measured: gamma by model (bootstrap 95% CI): DeepSeek 0.43 [0.42, 0.44], Qwen 0.28 [0.27, 0.29], Gemini 0.25 [0.25, 0.26], GPT-5.5 0.18 [0.17, 0.19], Claude 0.15 [0.15, 0.15].
- Measured: across sixteen closed and open models, group coupling predicts society convergence with Pearson r = -0.70 (permutation p = 0.008); pairwise gamma can order multi-neighbour outcomes backwards.
- Measured: backfire coefficient beta <= 0 for all tested models; polarization appears only when induced.
- Measured: the slope/bias diagnostic reveals a model-specific conflation in the Chuang et al. (2023) consensus result.
- Theory: Friedkin-Johnsen x(t+1) = gamma W x(t) + (1 - gamma) x(0) and signed-Laplacian criteria give the regime boundaries (stated as applications of known results, Props. 1-3).

## Methods and models

Numeric-opinion societies of N = 6-10 agents on ring, complete and stochastic-block-model graphs, K = 3-5 rounds; free-text societies at K = 5 on five models. Counterfactual neighbour-perturbation grid for gamma; interior-valued facts so that boundary censoring cannot fake averaging. Code and per-run logs: https://github.com/deeplethe/llm-coupling-gain .

## Limitations and open questions

- The author lists small societies (N = 6-10), few rounds, a scalar-gamma linearisation, and that the active-polarization branch is never observed in real agents.
- Linear opinion models may miss the discrete, conformity-driven dynamics seen in naming games ([[flint-2026-group]]).
- Single-author preprint; not yet peer reviewed.

## Relevance to us

Gives the hackathon a measurable coupling constant and a validity diagnostic to run before claiming emergent consensus in any LLM swarm experiment. Pair with [[hirota-2026-collective]] (fitted beta in a Kuramoto-like map), [[okawa-2026-emergence]] (fitted conformity) and [[bertalanic-2026-ringelmann]] (noise placebo).
