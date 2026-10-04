---
id: okawa-2026-emergence
type: paper
title: "Emergence of Biased Consensus in Multi-Agent LLM Debates"
authors:
- "Maya Okawa"
year: 2026
venue: "International Conference on Machine Learning (ICML 2026), accepted (per arXiv comments)"
url: https://arxiv.org/abs/2608.02827
doi: null
arxiv: "2608.02827"
cite: "Okawa, M. (2026). Emergence of Biased Consensus in Multi-Agent LLM Debates. In Proceedings of the 43rd International Conference on Machine Learning (ICML 2026). arXiv:2608.02827."
topics:
- llm-agent-swarms
- sync-consensus
- criticality-measurement
added_by: dmarz/llm-agent-swarms-recent-audit
accessed: '2026-10-03'
read_depth: skim
relevance: 5
citations: "3 (Semantic Scholar, 2026-10-03); OpenAlex not retrieved (HTTP 429)"
code: []
---
## Summary

Multi-agent LLM debate (in the protocol of [[du-2023-improving]]) can amplify a small individual bias into a strong collective one. The paper models debating agents as spins in an Ising/Potts system: in the binary case the population magnetisation evolves as m(t+1) = tanh[beta (J m(t) + h)], with h the agents' initial predisposition (token or social bias), J the conformity/interaction strength and beta the inverse of debate noise, which the author ties to sampling temperature. The theory predicts a transition to collective (biased) consensus when conformity exceeds a critical value set by bias and noise (beta J > 1 in the mean-field limit). Controlled experiments with 11 LLMs on a neutral binary-choice task (O vs I) and an implicit gender-bias task show a finite-size crossover consistent with that transition. Heterogeneous populations round (smooth) the transition and suppress emergence. The insight carries to investment recommendations and LLM-as-a-judge on MT-Bench.

## Contribution

Gives a statistical-physics account of bias amplification in debate, with temperature as a control knob and agent heterogeneity as a mitigation, and fits the model's parameters (conformity, bias) per LLM from debate trajectories. It complements the naming-game results of [[ashery-2024-emergent]] and [[flint-2026-group]] (size-driven amplification) and the temperature-as-control-parameter result of [[de-nobili-2026-microscopic]].

## Key results

- Theory: mean-field recursion m(t+1) = tanh[beta(J m(t) + h)] aligns the population even under minimal predisposition h when beta J > 1; finite-N predictions contrasted at N = 11 and N = 1000 (sharp transition only at large N).
- Measured: empirical phase diagrams of the final collective norm |m(R)| vs temperature show finite-N rounding of the transition across LLMs and tasks.
- Measured (inverse fit): GPT-4.1 variants have negative fitted conformity (lambda_i < 0) with a wider spread of bias; DeepSeek V3 has the strongest positive conformity; instruct variants often deviate from their base models.
- Measured: mixing agent types (heterogeneity) smooths the transition and suppresses biased consensus.
- Measured: interventions derived from the theory (noise, sparser interaction, heterogeneity) carry over to an investment task with ten GPT-4.1 Nano agents and to LLM-as-a-judge (six agents, GPT-3.5 or GPT-4, MT-Bench pairs, self-bias as the bias measure).
- Exact effect sizes for the realistic tasks were not checked in this read.

## Methods and models

Debate protocol after Du et al. (2023): agents propose independently, then exchange responses over multiple rounds. Models (11, via APIs): GPT-4.1, GPT-4.1 Mini, GPT-4.1 Nano, DeepSeek V3, Llama 3.1 405B/70B/8B Instruct, Mistral 7B and 24B, Qwen3 235B base and instruct. Tasks: Binary Choice (neutral symbols with controllable token bias), Implicit Bias (e.g. Jane/John role assignment), investment portfolios, MT-Bench LLM-as-a-judge. Spin-model (Ising for q = 2, Potts for q > 2) mean-field theory; parameter inference from trajectories. Code: https://github.com/phys-ai/llm-biased-consensus .

## Limitations and open questions

- The author lists a simplified debate protocol (short memory, all-to-all or random interactions, no roles) and binarisation of high-dimensional outputs.
- Populations are small (single digits to about ten agents), so the "phase transition" is inferred from finite-size crossover plus theory, not observed at scale.
- Mapping sampling temperature to spin-model temperature is a modelling assumption.

## Relevance to us

A ready-made order parameter (|m|), control parameters (temperature, conformity, heterogeneity) and a mean-field prediction we can test at larger N with small local models, for example with the cached-policy trick of [[flint-2026-group]]. Related: [[de-nobili-2026-microscopic]], [[ricco-2026-consensus]], [[yang-2026-when]], [[choi-2025-debate]], [[zhang-2025-stop]].
