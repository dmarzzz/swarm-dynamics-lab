---
id: ashery-2024-emergent
type: paper
title: Emergent social conventions and collective bias in LLM populations
authors:
- Ariel Flint Ashery
- Luca Maria Aiello
- Andrea Baronchelli
year: 2024
venue: Science Advances
url: https://arxiv.org/abs/2410.08948
doi: 10.1126/sciadv.adu9368
arxiv: '2410.08948'
cite: Ashery, A. F., Aiello, L. M., & Baronchelli, A. (2025). Emergent social conventions and collective bias in LLM populations. Science Advances, 11(20), eadu9368. https://doi.org/10.1126/sciadv.adu9368
topics:
- llm-agent-swarms
- sync-consensus
- collective-decision
added_by: dmarz/llm-agent-swarms
accessed: '2026-10-03'
read_depth: full
relevance: 5
citations: 191 (Semantic Scholar, 2026-10-03; OpenAlex unavailable that day)
code: []
---

## Summary

Populations of LLM agents playing the naming game spontaneously agree on a shared convention, develop a collective bias toward particular conventions even when individual agents are unbiased, and can be tipped to a new convention by a committed minority. Each simulation has N agents; at each step two random agents each pick a "name" (a letter) from a pool of W options, are rewarded (+100) if they match and penalised (-50) if not, and remember only their last H interactions. There is no incentive or information about global consensus. All four models tested (Llama-2-70b-Chat, Llama-3-70B-Instruct, Llama-3.1-70B-Instruct, Claude-3.5-Sonnet) undergo a disorder-to-order, symmetry-breaking transition to a single convention, matching the minimal naming-game model.

## Contribution

Brings the Baronchelli-Steels naming game, a canonical statistical-physics model of convention formation with known human-experiment counterparts (Centola and Baronchelli 2015; Centola et al. 2018 on tipping points), into LLM populations. Its distinctive finding is collective bias that emerges from interaction itself rather than from individual priors, which is a population-level alignment failure invisible to single-agent evaluation.

## Key results

- Default N = 24, W = 10, H = 5: a global convention is reached by population round 15 for all models except Llama-2-70b-Chat (slower). Consensus also occurs at N = 200 and W = 26, at comparable speed in population rounds. Measured (40 runs per model for the main figure).
- Final conventions are far from uniformly distributed across the 10 names, and the favoured names differ by model; with the full alphabet available, populations converge on 'A' because single agents already prefer it. Measured.
- With W = 2 (names Q and M), individual first choices are unbiased (Binomial p = 0.068-0.849 across models), but populations consistently converge more often on one "strong" convention. Microscopically: after a success agents keep the name 99.4% of the time, after a failure they switch 97.3% of the time; by the third interaction strategies are not symmetric under relabelling (e.g. P(M | {1:M,Q; 2:Q,M}) = 0.848 vs P(Q | {1:Q,M; 2:M,Q}) = 0.451). Measured.
- Committed minorities flip an established convention once they reach a critical mass; the critical mass depends on whether the incumbent convention is the strong or weak one and on the model, ranging from 2% (Llama-3-70B-Instruct) to 67% (Llama-2-70b-Chat). Llama-3.1-70B populations spontaneously abandon the weak convention without any committed agents. Human experiments put the threshold near 25%; theory gives 10-40%. Measured, with consensus flip defined as 95% success over the past 3N interactions.
- Theoretical minimal naming game (10,000 runs) reproduces the success-rate curves. Measured vs model.

## Methods and models

Prompted pairwise coordination game; system prompt with rules and payoffs, dynamic memory of the last H rounds (own choice, partner choice, outcome, cumulative score), zero-shot "think step by step", randomised name order per call, meta-prompting comprehension checks, non-zero temperature with top-K sampling. Bias tests: exact Binomial (W = 2) and chi-squared (W = 10) on memoryless first moves. Committed agents always play the alternative name. Llama-2 run locally in 4-bit on an A100; Llama-3 via Hugging Face Inference API. Code: https://github.com/Ariel-Flint-Ashery/AI-norms

## Limitations and open questions

Unstructured, well-mixed population (random pairs); pairwise interactions only; meaningless letter conventions; homogeneous single-model populations; results depend on prompt and model. The authors list network structure, higher-order (group) interactions, realistic norms and mixed human-LLM populations as next steps. The size-dependence of collective bias is taken up in [[flint-2025-group]].

## Relevance to us

A ready-made, cheap experimental paradigm with a known physics baseline (naming game), measurable order parameter (success rate, convention share), and a tipping-point experiment. Directly comparable to [[de-marzo-2024-ai]] (Curie-Weiss majority force), [[tanaka-2026-when]] (drift vs selection explanation of the symmetry breaking), [[mehdizadeh-2026-exploring]] (network topology and memory) and [[chuang-2023-simulating]]. Collective bias is the LLM analogue of the information-cascade and leadership effects studied in animal groups (topic collective-decision).

## Notes from dmarz/llm-agent-swarms-recent

Independent full read of the Science Advances version via Europe PMC (PMC12077490). Numbers to cross-check: N = 24, W = 10, H = 5, payoffs +100/-50; 40 runs per Llama-3 model, 27 (Claude-3.5-Sonnet) and 20 (Llama-2-70b-Chat); N = 200 and W = 26 also converge (fig. S2). For Llama-3.1 on {Q, M}: agents keep a winning name 99.4% of the time and switch 97.3% after a failure; collective bias appears by the third interaction from asymmetric strategies over mirror-image memories (P(M|{1:M,Q;2:Q,M}) = 0.848 vs P(Q|{1:Q,M;2:M,Q}) = 0.451). Critical mass to flip a convention ranges from ~2% (Llama-3-70B, H = 3, N = 48) to 67% (Llama-2-70b-Chat). Code: https://github.com/Ariel-Flint-Ashery/AI-norms ; data DOI 10.5281/zenodo.14937173. The group-size follow-up with a mean-field theory is [[flint-2026-group]]; the memorisation critique is [[barrie-2025-emergent]]. OpenAlex cited_by_count 69, Semantic Scholar 191 (2026-10-03).
