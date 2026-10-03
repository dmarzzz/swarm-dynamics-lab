---
id: kim-2021-reward
type: paper
title: Reward Identification in Inverse Reinforcement Learning
authors:
- Kuno Kim
- Shivam Garg
- Kirankumar Shiragur
- Stefano Ermon
year: 2021
venue: 'Proceedings of the 38th International Conference on Machine Learning (ICML), PMLR 139'
url: https://proceedings.mlr.press/v139/kim21c.html
doi: null
arxiv: null
cite: 'Kim, K., Garg, S., Shiragur, K., & Ermon, S. (2021). Reward Identification in Inverse Reinforcement Learning. In Proceedings of the 38th International Conference on Machine Learning, PMLR 139:5496-5505.'
topics:
- meta
added_by: vishesh/senku-1
accessed: '2026-10-03'
read_depth: full
relevance: 2
citations: '47 (Semantic Scholar, 2026-10-03)'
code: []
---

## Summary

Inverse RL recovers a reward from observed optimal behaviour, but the map from reward to behaviour is not injective, so the recovered reward may be meaningless. This paper asks when it is injective. It defines an MDP model as identifiable if equal optimal trajectory distributions imply equivalent rewards, and separates weak identifiability, up to trajectory equivalence, from strong identifiability, up to an additive constant on state-action rewards. Theorem 1 shows that under the MaxEnt RL objective every deterministic-transition MDP model is weakly identifiable, because the optimal trajectory distribution is then an energy-based model whose energy is the negative trajectory reward. Section 5 then embeds the domain in a directed domain graph whose vertices are state-action pairs, and Theorem 2 proves that for proper models with a strongly connected domain graph, coverability of that graph is necessary and sufficient for strong identifiability, with Proposition 3 showing coverability is equivalent to aperiodicity there.

## Contribution

It is the first formal treatment of reward identifiability in the IRL literature, and it converts an abstract question about reward ambiguity into a decidable graph property of the environment, which makes it something a modeller can check before trusting a recovered reward.

## Key results

- Theorem 1: for MaxEnt MDP models, all domains with deterministic transitions, deterministic initial state and horizon T >= 0 are weakly identifiable. Measured as a proof, not an experiment.
- Section 4.2 counterexample: the common belief that this extends to stochastic dynamics is false. With uniform random dynamics the MaxEnt optimal policy is uniform, yet the optimal trajectory distribution prefers high-reward trajectories exponentially, so two non-equivalent rewards induce the same trajectory distribution. Stochastic MDP models are therefore not always weakly identifiable, and characterising which ones are is left open.
- Proposition 1: for proper models, strong identifiability is strictly stronger than weak identifiability.
- Proposition 2: a weakly identifiable model is strongly identifiable if and only if trajectory equivalence implies state-action equivalence; Corollary 1 restates this as the path matrix A[d,T] having rank equal to the number of state-action pairs.
- Theorem 2 and Corollary 2: for proper models with strongly connected domain graphs, strong identifiability, coverability and aperiodicity coincide. Sufficiency needs T >= 2*T_0 where T_0 is the covering time. A periodic k-partite cycle graph is unidentifiable; a graph with a self-loop is identifiable.
- Theorem 3: the test MDPIdTest, which builds the domain graph and checks aperiodicity via Denardo's Period Finder, is correct for weakly identifiable models with strongly connected domain graphs and runs in O(|E_d|) time and space.
- Theorem 4: for general weakly identifiable models, MDPCoverTest is a correct sufficiency test with time complexity O(|V_d|^3 log|V_d|) and space O(|V_d|^2).

## Methods and models

Entirely theoretical: finite discrete MDPs, the MaxEnt RL objective (chosen because it induces a unique optimal policy, unlike the standard objective), proper models where trajectory-equivalent rewards give equal optimal trajectory distributions, and a graph-theoretic apparatus of domain graphs, layers, coverability and periodicity. Figure 3 summarises the containment: proper models contain weakly identifiable models contain strongly identifiable ones, with the deterministic MaxEnt case and the k-partite cycle as the separating examples. There are no experiments and no numerical results. Bibliographic note: the PMLR proceedings page lists the authors as Kim, Garg, Shiragur, Ermon, while the PDF title page prints Kim, Shiragur, Garg, Ermon; the publisher page order is used above.

## Limitations and open questions

The positive results are confined to deterministic dynamics; the authors state plainly that when stochastic MDP models are weakly identifiable, if ever, is unanswered, and that necessary and sufficient conditions for strong identifiability without strong connectivity are also open, as are more efficient tests for weakly connected domain graphs. Nothing is validated empirically, so the practical bite of coverability in realistic environments is untested.

## Relevance to us

It is the formal check on the first half of our question. Any claim that a preference inferred from one agent predicts a collective's choices presupposes the inferred preference is the real one, and this paper says that presupposition is false by default: it holds for deterministic environments, fails for stochastic ones, and only yields a reward pinned down to an additive constant when the environment's state-action graph is coverable. A debate or negotiation harness with sampling temperature is a stochastic domain, which is exactly the regime the paper leaves unidentifiable, so a hackathon project inferring preferences from agent transcripts should either make the environment deterministic (fixed seeds, greedy decoding) or report its conclusions as preference-equivalence-class claims rather than reward claims. The aperiodicity and self-loop conditions also give a concrete design rule: give agents an option to do nothing, so the interaction graph has a self-loop. Direct companion to [[yu-2019-multi]], whose reward-shaping restriction is an engineering workaround for precisely this ambiguity, and to the inverse-inference entries [[sosic-2017-inverse]] and [[martina-perez-2025-inverse]].
