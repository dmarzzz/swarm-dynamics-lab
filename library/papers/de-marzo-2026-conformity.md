---
id: de-marzo-2026-conformity
type: paper
title: 'Conformity Generates Collective Misalignment in AI Agents Societies'
authors: [Giordano De Marzo, Alessandro Bellina, Claudio Castellano, Viola Priesemann, David Garcia]
year: 2026
venue: arXiv preprint (physics.soc-ph)
url: https://arxiv.org/html/2605.10721
doi: null
arxiv: '2605.10721'
cite: 'De Marzo, G., Bellina, A., Castellano, C., Priesemann, V., & Garcia, D. (2026). Conformity Generates Collective Misalignment in AI Agents Societies. arXiv preprint arXiv:2605.10721.'
topics: [llm-agent-swarms, collective-decision, criticality-measurement]
added_by: shadow/sol-1
accessed: '2026-10-03'
read_depth: full
relevance: 5
citations: null
code: []
---

## Summary

The De Marzo group's follow-up to [[de-marzo-2024-ai]]. N agents (N = 50 in the main runs) of one LLM each hold one of two opinions; at each step one random agent sees the current opinions of all other N - 1 agents (fresh random two-character names, shuffled order, no memory, no own opinion shown) and declares an opinion. Across nine LLMs (temperature 0.2) and 100 opinion pairs, the adoption probability fits P(m) = [tanh(beta(m + h)) + 1]/2, with a majority force beta and a bias field h, and all curves collapse onto one function. The mean-field Ising spinodal |h_s(beta)| splits the (beta, h) plane: inside it (beta > 1, |h| < h_s) misaligned states are metastable. More than 60% of Gemma 3 27B pairs fall inside; for 20 random pairs per model started at |m0| = 0.9 the spinodal line separates pairs that stay misaligned from those that return. Stubborn-agent injection shows both outcomes: for a pair inside the spinodal (Gemma 3 27B, gender self-identification vs biological sex, N^S = 35) the population stays tipped after the stubborn agents are removed; for a pair outside (renewable vs non-renewable, N^S = 225) it relaxes back. Forward and backward sweeps of the stubborn fraction z from -0.6 to +0.6 give hysteresis loops, and the measured critical fractions z_c track the Curie-Weiss prediction across models.

## Contribution

A two-parameter per-model, per-topic measurement (beta, h) with a predictive phase diagram for when committed-minority tipping is irreversible. Reversibility is regime-dependent by construction: the paper predicts and shows both persistence and relaxation.

## Key results

- Universal tanh collapse of P(m) across 9 models and about 100 opinion pairs (measured).
- More than 60% of Gemma 3 27B pairs in the metastable region; about 60% for Gemini and about 30% for ChatGPT (measured).
- Hysteresis under stubborn-fraction sweeps; observed z_c matches mean-field predictions; for some pairs fewer than 10% adversarial agents tip N >= 50 (measured).
- Collective memory without individual memory: agents are memoryless; the population state carries the history.

## Methods and models

Asynchronous Glauber-like updates, T * N steps, full observation of the population (fully connected), memoryless prompts (template in Methods IV.1). Spinodal derived from m = tanh[beta(m + h)]; tipping from m_tot = tanh[beta(m_tot + h)] + z(s - m_tot). Hysteresis protocol: 100 equilibration steps at z = -0.6, then 50 per z step, 25 sampling steps. Read: full main text and Methods (sections I to IV.7) in arXiv HTML on 2026-10-03. The SI (opinion list, per-model parameters, temperature analysis) was not read.

## Limitations and open questions

- Agents see the whole population and have no memory; local interaction, bounded memory and private evidence are not tested.
- No ground truth: "misaligned" means opposite to the population's own bias h, not wrong.
- Prior-artefact control (e.g. the randomised-initial-condition diagnostic of [[yang-2026-when]]) is not applied; h is itself the model prior, which the theory absorbs rather than removes.

## Relevance to us

The theory to test. The reversibility "disagreement" with [[magistrali-2026-aligned]] is better read as one result inside this phase diagram: relaxation is predicted outside the spinodal. The open test is whether bounded memory and local pairwise sampling (Magistrali's protocol) preserve hysteresis for a pair that sits inside the spinodal.
