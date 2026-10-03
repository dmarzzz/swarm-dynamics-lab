---
id: de-marzo-2024-ai
type: paper
title: AI agents can coordinate beyond human scale
authors:
- Giordano De Marzo
- Claudio Castellano
- David Garcia
year: 2024
venue: Science Advances
url: https://arxiv.org/abs/2409.02822
doi: 10.1126/sciadv.aea6091
arxiv: '2409.02822'
cite: De Marzo, G., Castellano, C., & Garcia, D. (2026). AI agents can coordinate via majority-following beyond human scale. Science Advances, 12(33), eaea6091. https://doi.org/10.1126/sciadv.aea6091 (preprint arXiv:2409.02822, 2024, earlier titled 'Language understanding as a constraint on consensus size in LLM societies').
topics:
- llm-agent-swarms
- sync-consensus
- criticality-measurement
- collective-decision
added_by: dmarz/llm-agent-swarms
accessed: '2026-10-03'
read_depth: full
relevance: 5
citations: "1 (OpenAlex W7203444322, published version, 2026-10-03); 3 (OpenAlex W4403584145, arXiv record, 2026-10-03); Semantic Scholar 17 same day"
code: []
---

## Summary

The paper runs binary opinion dynamics with LLM agents and shows that the agents' update rule is, to a good approximation, Glauber dynamics of the mean-field (Curie-Weiss) Ising model. N agents each hold one of two arbitrary, meaningless opinions; at each step a random agent sees the full list of everyone else's opinions and picks one. The empirical adoption probability as a function of the collective opinion m follows P(m) = [tanh(beta m) + 1]/2, where beta, the "majority force", plays the role of inverse temperature. beta depends on the model and decreases with group size, so each LLM has a critical group size N_c beyond which consensus becomes exponentially slow. N_c grows roughly exponentially with model capability (MMLU), from about 30 for Llama 3 70B and 80 for GPT-4o to about 1000 for GPT-4 Turbo and above 1000 for Claude 3.5 Sonnet, i.e. beyond Dunbar's number for humans.

## Contribution

The cleanest mapping so far between an LLM agent population and a textbook statistical-physics model, with a fitted order parameter, a known phase transition (beta_c = 1) and a finite-size crossover beta_t ~ (1/2) log N that turns into a predicted, measurable critical group size. It moves LLM-collective work from anecdote to quantitative scaling, and supplies an "AI Dunbar number" that can be compared across models.

## Key results

- Adoption curves for ten LLMs at N = 50 collapse onto one universal tanh curve after rescaling m -> beta m (all models except GPT-3.5 Turbo, which partly anti-follows the majority at small m). Measured.
- At N = 50, Claude 3 Opus and GPT-4 Turbo reach full coordination (C = |m| = 1) in all 20 runs; Claude 3 Haiku and GPT-3.5 Turbo never do; Llama 3 70B trends toward coordination but does not reach it within t = 10. Measured.
- Three regimes from Curie-Weiss theory: no coordination (beta < beta_c = 1), partial coordination (1 < beta < beta_t ~ log(N)/2) and coordination (beta > beta_t). beta decreases with N for most models. Measured beta(N); regimes derived.
- Time to consensus grows logarithmically with N above beta_t (GPT-4 Turbo follows the Curie-Weiss prediction with beta = 3.75) and exponentially below it (Llama 3 70B and GPT-4o show both regimes). Measured, with 5 realisations per point (3 at N = 500, 1 at N = 1000).
- N_c ~ 30 (Llama 3 70B), ~ 80 (GPT-4o), ~ 1000 (GPT-4 Turbo), > 1000 (Claude 3.5 Sonnet, lower bound since beta stays above beta_t(1000) ~ 3.5). log N_c is roughly linear in MMLU; humans (Dunbar N_c ~ 200) sit near the same trend. Measured points, exponential fit is the authors'.
- Iterated split experiments (Llama 3 70B, N = 150): large groups fragment over about 10 iterations into stable small groups (for example a 25-agent subgroup that fully coordinates). Measured.
- Opinion-name bias ("Yes" over "No") is strong for meaningful labels; letters k/z with per-step random relabelling remove it. Measured (SI).

## Methods and models

Memoryless agents; each update shows the agent a list of all other agents (random 3-character names) and their opinions, and asks for its own opinion in square brackets; time increments dt = 1/N; initial m = 0; temperature 0.2 (robust in SI). Models: Claude 3.5 Sonnet, Claude 3 Haiku/Sonnet/Opus, Claude 2.0, GPT-3.5 Turbo, GPT-4, GPT-4o, GPT-4 Turbo, Llama 3 70B. Theory: Curie-Weiss self-consistency m* = tanh(beta m*), m* ~ sqrt(3(beta-1)) near beta_c; Ornstein-Uhlenbeck approximation dm = -(m - m*)dt + sqrt(2D) dW with D ~ (2/N) e^{-2 beta}; crossover beta_t ~ (1/2) log N; N_c from beta(N_c) = (1/2) log N_c. Code: https://github.com/giordano-demarzo/LLMs-Opinion-Dynamics

## Limitations and open questions

All-to-all, fully observed population, arbitrary binary choice with no information or incentive: a deliberately idealised setting. Very few realisations at large N for cost reasons. The MMLU-N_c fit has few points. The "intelligence predicts group size" analogy with primate neocortex ratios is suggestive, not tested. Open: what happens on sparse networks or with local interaction (closer to a spatial swarm), with heterogeneous models, with memory, or with informative options; and whether beta can be engineered by prompting.

## Relevance to us

Probably the single most reusable result for a swarm-dynamics hackathon: a measurable order parameter m, a control parameter beta read directly from adoption curves, and a finite-size prediction that can be tested on any model in an afternoon. Natural companion to [[ashery-2024-emergent]] (naming game, committed minorities), [[flint-2026-group]] (group size and mean-field basins), [[el-2026-physics]] (Ising fit on signed networks), [[de-nobili-2026-collective]] (2D lattice, critical exponents) and [[tanaka-2026-when]] (drift vs selection). Contrasts with [[riedl-2025-emergent]], which measures synergy rather than consensus.

## Notes from dmarz/llm-agent-swarms-recent

Independent full read (arXiv v4 HTML, 2026-10-03). The journal version is retitled "AI agents can coordinate via majority-following beyond human scale", Science Advances 12(33), eaea6091 (2026), per Crossref; its abstract states the critical group size exceeds 1000 agents for advanced LLMs. Details worth keeping for replication: memoryless agents, T = 0.2, opinion labels "k"/"z" swapped with probability 0.5 at every update to cancel label bias; Fig. 1 group-fission protocol (split if not unanimous after 10 sweeps; 150 Llama 3 70B agents fragment to stable groups of ~25). Theory: OU approximation around m* ~ 1 with D ~ (2/N) e^{-2 beta} gives beta_t ~ (1/2) log N; N_c solves beta(N_c) = (1/2) log N_c. Reported N_c: ~30 (Llama 3 70B), ~80 (GPT-4o), ~1000 (GPT-4 Turbo, from a single N = 1000 run), > 1000 (Claude 3.5 Sonnet, lower bound). Control: a plain "most frequent letter" prompt is solved at 0.95-0.99 (easy) and 0.72-0.95 (near-balanced, N up to 501) by all models, so the authors attribute the fall of beta with N to the social framing. Caveat for us: all-to-all information means prompt length grows with N. Forward citations (Semantic Scholar, 17 on 2026-10-03) include [[flint-2026-group]] and De Marzo and Garcia's Moltbook analysis [[de-marzo-2026-collective]]. Code: https://github.com/giordano-demarzo/LLMs-Opinion-Dynamics

## Notes from dmarz/llm-agent-swarms-audit

Audit 2026-10-03: checked arXiv v1 metadata, Crossref (Science Advances 12(33), eaea6091, published 2026-08-14) and the HTML text for N_c values and the beta_t ~ (1/2) log N crossover. No errors in content. Note: `title` is the arXiv title while `venue`, `doi` and `cite` are the journal version, which is retitled "AI agents can coordinate via majority-following beyond human scale"; `year` is the arXiv v1 year. Left as is because `lab.py verify` accepts it, but cite the journal title. The `citations` field was rewritten to OpenAlex counts (OpenAlex was reachable for single-work lookups during the audit); the Semantic Scholar count is kept alongside.
