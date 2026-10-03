---
id: flint-2026-group
type: paper
title: Group size effects and collective misalignment in LLM multi-agent systems
authors:
- Ariel Flint
- Luca Maria Aiello
- Romualdo Pastor-Satorras
- Andrea Baronchelli
year: 2026
venue: Proceedings of the National Academy of Sciences
url: https://arxiv.org/abs/2510.22422
doi: 10.1073/pnas.2531697123
arxiv: '2510.22422'
cite: Flint, A., Aiello, L. M., Pastor-Satorras, R., & Baronchelli, A. (2026). Group size effects and collective misalignment in LLM multi-agent systems. Proceedings of the National Academy of Sciences, 123(34), e2531697123. https://doi.org/10.1073/pnas.2531697123
topics:
- llm-agent-swarms
- sync-consensus
- criticality-measurement
added_by: dmarz/llm-agent-swarms-recent
accessed: '2026-10-03'
read_depth: full
relevance: 5
citations: 0 (OpenAlex, journal record, 2026-10-03); 19 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

The paper asks what happens to LLM collective behaviour across the full range of population sizes, rather than comparing one agent to one fixed-size group. Using the two-word naming game of [[ashery-2024-emergent]] with socially loaded word pairs (e.g. {man, woman}, {straight, gay}, {White, African}), memory H = 5, payoffs +100/-50, the authors extract each LLM's token-level probability policy for every possible memory state (4^{H+1}-1)/3 states, cache it, and then simulate populations far larger than direct LLM calls would allow (up to N ~ 10^4). Interaction can amplify an individual bias, create one from neutral agents, or reverse it (e.g. Llama prefers "straight" individually but populations of N >= 6 converge on "gay"). The probability of converging on the "strong" word rises with N until, above a model- and pair-specific threshold N_c (from N = 2 to N ~ 10^4), the outcome is deterministic. A mean-field rate equation over memory-state fractions, with linear stability analysis of the two absorbing consensus states, explains the large-N determinism and the rare non-consensus cases.

## Contribution

Establishes group size as a control parameter for collective misalignment in LLM populations and supplies a mean-field theory with fixed points and basins of attraction. Methodologically important: the cached-policy stochastic model (validated against direct generation in the SI) is a cheap way to simulate LLM swarms at sizes of 10^3-10^4. Extends [[ashery-2024-emergent]]; complements [[de-marzo-2024-ai]], which studies global (all-to-all) information rather than local pairwise interaction.

## Key results

- Measured (cached-policy simulations, 1000 runs per condition, N = 24): three misalignment types appear: amplification (e.g. {American, Mexican}), induction from neutrality ({White, African}) and reversal ({straight, gay}); magnitude and direction differ by model (Qwen QwQ-32B, Phi-4, GPT-4o, Llama 3.1 70B). For {her, his}, Qwen and Phi converge on "her" while GPT and Llama converge on "his" despite similar individual tendencies.
- Measured: collective preference for the strong word increases monotonically with N in every model-pair combination until deterministic; for GPT on {White, African}, P(strong) = 0.626, 0.720, 0.981, 1.00 at increasing N.
- Measured: consensus-time distributions change shape with N: fast collapse at small N, unimodal heavy-tailed at intermediate N, and separation of weak/strong consensus times at larger N.
- Theory: mean-field equation dx_k/dt = -x_k + sum_{i,j} x_i x_j P_k(i,j) over memory-state fractions; fixed points are the two homogeneous absorbing states. In most cases strong is stable and weak unstable, or both stable with basin sizes deciding. Non-consensus cases (Llama {less, more}: both unstable; {old, young}: strong unstable, weak marginal) produce mixed steady states also seen in finite-N simulation.

## Methods and models

Minimal naming game, W = 2, pairwise random matching on a complete graph, memory H = 5 of own and partner's choices, convergence when 98% of the last 3N interactions succeed, up to 1000 population rounds. Policies extracted from logits restricted to the two words, softmax at T = 0.5, cached for all memory states. Models: Phi-4, Qwen QwQ-32B, Llama 3.1 70B Instruct (4-bit, single A100) and GPT-4o via API. Individual neutrality defined as Jensen-Shannon distance < 0.005 from uniform at empty memory. Eleven word pairs from prior bias literature.

## Limitations and open questions

- Homogeneous populations only (one model per population); well-mixed interactions only.
- The cached-policy model assumes an agent's choice depends only on the memory state encoded in the prompt, so any hidden state or prompt drift is ignored; the SI validates agreement for the tested models but not universally.
- Binary word choice is a stylised proxy for bias in deployed systems.
- The authors note [[de-marzo-2024-ai]] finds loss of order beyond a size threshold with global information, opposite in sign to the increasing determinism here; how local vs global information changes the size dependence is open.

## Relevance to us

High. The cached-policy trick is directly usable for a hackathon: extract an LLM's response table once, then run 10^4-agent swarms on a laptop and sweep topology, memory and heterogeneity. The mean-field formulation gives predictions to test. Link with [[ashery-2024-emergent]], [[de-marzo-2024-ai]], [[tanaka-2026-when]], [[de-nobili-2026-microscopic]], [[wu-2026-predicting]].
