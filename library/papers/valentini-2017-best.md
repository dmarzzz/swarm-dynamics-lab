---
id: valentini-2017-best
type: paper
title: "The Best-of-n Problem in Robot Swarms: Formalization, State of the Art, and Novel Perspectives"
authors: ["Gabriele Valentini", "Eliseo Ferrante", "Marco Dorigo"]
year: 2017
venue: "Frontiers in Robotics and AI"
url: https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2017.00009/full
doi: "10.3389/frobt.2017.00009"
arxiv: null
cite: "Valentini, G., Ferrante, E., & Dorigo, M. (2017). The Best-of-n Problem in Robot Swarms: Formalization, State of the Art, and Novel Perspectives. Frontiers in Robotics and AI, 4, 9."
topics: [swarm-robotics, collective-decision, sync-consensus]
added_by: dmarz/swarm-robotics
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "198 (OpenAlex, 2026-10-03)"
code: []
---
## Summary

A review that formalises discrete consensus in robot swarms as the "best-of-n" problem: N robots must reach a
large majority M >= (1 - delta)N for one of n options, each with a quality rho_i in (0, 1] (measured by robots)
and a cost sigma_i (mean time to sample it, imposed by the environment and not measured). Crossing symmetric
or asymmetric quality with symmetric or asymmetric cost gives five variants: symmetry breaking; minimum cost;
maximum quality; synergic (best option also cheapest); antagonistic (best option costlier). The authors
classify the swarm literature into these variants and, separately, by design approach: bottom-up
opinion-based rules (voter model, majority rule, k-unanimity, cross-inhibition), bottom-up ad hoc rules that
decide through aggregation (cockroach shelters, BEECLUST) or navigation (pheromones, social odometry), and
top-down automatic design (evolutionary robotics, AutoMoDe).

## Contribution

A shared vocabulary and taxonomy that separates the structure of a decision problem from the mechanism used to
solve it; it has become the standard framing for collective decision-making in swarm robotics and connects
the field to opinion dynamics in statistical physics ([[castellano-2009-statistical]]) and to honeybee
nest-site selection models ([[reina-2015-design]]).

## Key results

- Literature finding: almost all studies are binary (n = 2); only one experimental study used n = 7 (a maze)
  and one theoretical analysis n = 3.
- The antagonistic variant has only two contributions; the synergic one has three research lines.
- Trade-offs identified: aggregation-based strategies need no communication but only work when options are
  spatially separated; navigation-based strategies only solve shortest-path problems; opinion-based strategies
  generalise but require explicit communication; evolved controllers suffer the reality gap and resist
  modelling, which AutoMoDe ([[francesca-2014-automode]]) partly addresses.
- Points to the mathematical toolkit used to analyse these rules: ODE mean-field models, chemical reaction
  networks, master equations, Markov chains, statistical model checking ([[elamvazhuthi-2019-mean]]).

## Methods and models

Narrative review with two taxonomies (problem structure; design approach). Formal definitions of option
quality, option cost, static versus dynamic qualities, consensus (delta = 0) versus large majority. Reviewed
platforms include e-pucks, Kilobots, foot-bots, Alice and Jasmine robots.

## Limitations and open questions

Focuses on discrete consensus only (continuous consensus such as flocking direction is excluded). It predates
the speed-accuracy studies at larger scale and adversarial or Byzantine settings ([[strobel-2023-robot]]).
Authors call for n > 2 options, antagonistic quality-cost settings, and dynamic environments.

## Relevance to us

The cleanest map of collective decision-making in robot swarms, with the benchmark scenarios (collective
perception, double bridge, site selection) a hackathon could reuse. Links to [[reina-2015-design]],
[[strobel-2023-robot]], [[lama-2025-nonreciprocal]] and to opinion-dynamics theory in the
collective-decision topic.
