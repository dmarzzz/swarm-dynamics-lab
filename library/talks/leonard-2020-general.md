---
id: leonard-2020-general
type: talk
title: "A General Model of Opinion Dynamics on Networks: Consensus, Dissensus, and Cascades"
authors: [Naomi Ehrich Leonard]
year: 2020
url: https://www.youtube.com/watch?v=qQ1cEIPF3yw
venue: "C3.ai Digital Transformation Institute colloquium (online); uploaded 21 October 2020, 67 min including Q&A"
topics: [sync-consensus, collective-decision, marl-emergence]
added_by: shadow/sol-w6
accessed: 2026-10-03
read_depth: full
relevance: 4
---

## Summary

Leonard (Princeton) presenting the nonlinear opinion dynamics model developed with Anastasia Bizyaeva and Alessio Franci, the talk version of what became [[bizyaeva-2023-nonlinear]] (she says the preprint "is coming out tomorrow" on arXiv, consistent with arXiv 2009.04332). Read from the full auto-generated transcript; timestamps approximate.

- 02:24 to 08:56: motivation. Seeley's honeybee nest-site data, fish schools that switch from consensus to splitting at an obstacle, Pew political-polarisation data 1994 to 2014, and the "ultrasensitivity" of natural groups that pick out meaningful signals. She argues linear averaging models (DeGroot and relatives) cannot produce dissensus, multistability or cascades, and that a "model-independent" bifurcation-theory view predicts much richer behaviour.
- 13:15 to 26:22: the model. N_a agents, N_o options, real-valued opinions x_ij; relative opinions z_ij sum to zero over options, so the state splits into a consensus subspace plus a dissensus subspace. Vector field has three terms: linear inertia -d_ij x_ij, social influence u_i S(sum of weighted same-option and cross-option exchanges from self and neighbours) with S a sigmoidal saturation, and an additive input b_ij. The saturation is the only nonlinearity; without it the system is linear consensus. Four homogeneous weights: alpha (self, same option), beta (self, cross option), gamma (others, same option), delta (others, cross option). u_i is an "attention" or social-effort parameter.
- 37:22 to 43:13: main theorem (bifurcation off the neutral point as u increases). For regular graphs with in-degree k the critical attention u_c is given in terms of inertia, alpha minus beta, gamma minus delta and k; on general connected undirected graphs the consensus bifurcation depends on lambda_max of the adjacency matrix and the dissensus bifurcation on its smallest eigenvalue. Corollary: self-reinforcing mutually exclusive options (alpha > beta) plus cooperative agents (gamma > delta) gives generic consensus; competitive agents (gamma < delta) gives generic dissensus. Option-permutation symmetry gives multistability (consensus on any option equally stable); at gamma = delta there is mode interaction and consensus and dissensus coexist at the same u_c, which she offers as an explanation for fish switching instantly between the two. The branches are hyperbolic (equivariant branching lemma), so small heterogeneity in weights and inputs does not change the picture, with computable robustness bounds.
- 43:55 to 50:20: simulations with 8 agents, 2 options: identical parameters except the sign of gamma minus delta flip the outcome between consensus and dissensus; on path, cycle, star and wheel graphs the dissensus regime alternates opinions along the graph and the star centre takes the opposite sign to the periphery. Linearising recovers linear consensus; with a signed Laplacian it recovers the Altafini model, which needs structural balance for bipartite consensus, whereas the saturated nonlinear model gets dissensus without structural balance (46:07, see [[altafini-2013-consensus]]). Demo of two robots choosing sides of a hallway obstacle.
- 52:31 to 63:29: dynamic attention. Make u_i itself a leaky-accumulator driven by a sigmoid of neighbours' opinion strength (possibly over a separate attention network). Two sigmoid parameters (upper bound u_f and midpoint) act as implicit, tunable thresholds: the group amplifies arbitrarily small inputs near the bifurcation, rejects small input changes once opinionated, and a single agent's input can trigger a cascade. Illustrated with nullcline pictures of the pitchfork unfolding under input switches.
- Q&A (63:29 onward): two options give a supercritical pitchfork (smooth); three or more options always give a singularity with hysteresis, so switch-like behaviour is generic beyond binary choice. Large-N limits and distributional versions not yet studied; a paper on network structure and numbers "soon".

Claims are stated as theorems with the proofs in the paper; the numerical examples are small (8 agents).

## Relevance to us

Directly useful as the minimal mechanism that produces both agreement and stable disagreement in a networked population with one nonlinearity. For LLM swarms: (1) if agents saturate how much they move toward peers (which any bounded update rule does), consensus versus polarisation is set by the sign of cooperative minus competitive cross-agent weighting and by the graph's extreme eigenvalues, not by the content of the options; (2) "attention" as a dynamic gain gives a concrete knob for the sensitivity-versus-robustness trade-off that a swarm detector or a swarm operator would want to measure; (3) the three-or-more-options hysteresis result predicts that multi-choice agent collectives will show lock-in and path dependence even when binary ones look smooth. Primary sources: [[bizyaeva-2023-nonlinear]], [[leonard-2024-fast]]; contrast with linear averaging in [[degroot-1974-reaching]] and [[ganesh-2020-introduction]], signed consensus [[altafini-2013-consensus]], bounded confidence [[hegselmann-2002-opinion]]; LLM-side evidence of opinion dynamics in [[chuang-2023-simulating]] and [[x-suryaganguli-2090115634231480755]].


## Notes from shadow/sol-w8

Leonard introduces nonlinear continuous-time opinions over multiple options. At 17:47-19:14 she distinguishes qualitative agreement, quantitative consensus and dissensus with an unopinionated average, and states boundedness and forward invariance of the relative-opinion state space. At 34:12-35:10 she explains that nonlinear interactions can create dissensus even in homogeneous symmetric networks, with oscillatory regimes also possible. At 50:28-51:51 a simulated two-robot hallway decision links attention to urgency. Closing Q&A at 65:29-67:00 contrasts two-option smooth transitions with switch-like/hysteretic behavior for larger option sets in the studied model.

Mechanism-level alternative to linear averaging and a useful distinction between agreement and population polarization. Model-specific bifurcation claims should not be generalized to every real human opinion network or arbitrary adversarial population.

Read depth for these additional notes: skim.
