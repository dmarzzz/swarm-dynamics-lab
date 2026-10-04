---
id: bloembergen-2015-evolutionary
type: paper
title: 'Evolutionary Dynamics of Multi-Agent Learning: A Survey'
authors: [Daan Bloembergen, Karl Tuyls, Daniel Hennes, Michael Kaisers]
year: 2015
venue: Journal of Artificial Intelligence Research
url: https://jair.org/index.php/jair/article/view/10952
doi: 10.1613/jair.4818
arxiv: null
cite: 'Bloembergen, D., Tuyls, K., Hennes, D., & Kaisers, M. (2015). Evolutionary dynamics of multi-agent learning: A survey. Journal of Artificial Intelligence Research, 53, 659–697.'
topics: [marl-emergence]
added_by: dmarz/marl-emergence-audit
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "224 (Crossref is-referenced-by-count, 2026-10-03)"
code: []
---

## Summary

Survey of the link between multi-agent reinforcement learning and the replicator dynamics of evolutionary game
theory. Starting from the result that Cross learning tends to the replicator dynamics in continuous time, it
collects the dynamical models derived for Boltzmann Q-learning (replicator dynamics plus an entropy-like
exploration term), frequency-adjusted Q-learning, learning automata, gradient-ascent learners, continuous-action
and state-coupled (multi-state) variants, and shows how these models are used for parameter tuning, for designing
new algorithms and for analysing meta-strategies in stock trading and multi-robot collision avoidance.

## Contribution

The standard review of the "learning dynamics" approach to MARL, the theoretical counterpart to algorithmic
surveys such as [[busoniu-2008-comprehensive]] and [[hernandez-leal-2019-survey]].

## Key results

- Review. The central formal result it collects: in stateless games, the expected dynamics of several RL algorithms
  are modified replicator equations, which allows phase portraits and basin analysis of learning.
- The authors list extending the theory to stochastic games with continuous actions as the main open direction.

## Methods and models

Sections: RL and game theory preliminaries; replicator dynamics as the continuous limit of Cross learning;
learning dynamics in normal-form games (Q-learning, FAQ, LA, gradient methods); continuous action spaces;
state-coupled replicator dynamics; experimental overview; applications.

## Limitations and open questions

Mostly two-player, low-dimensional games; no spatial structure, and pre-dates deep MARL.

## Relevance to us

Gives the equations for reasoning about why independent learners in a swarm do or do not converge. Read with
[[barfuss-2019-deterministic]] (multi-state extension) and [[sanders-2018-prevalence]] (many players).
