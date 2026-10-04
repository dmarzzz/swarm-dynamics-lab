---
id: vinyals-2019-grandmaster
type: paper
title: Grandmaster level in StarCraft II using multi-agent reinforcement learning
authors:
- Oriol Vinyals
- Igor Babuschkin
- Wojciech M. Czarnecki
- Michaël Mathieu
- Andrew Dudzik
- Junyoung Chung
- David H. Choi
- Richard Powell
- Timo Ewalds
- Petko Georgiev
- et al.
year: 2019
venue: Nature
url: https://www.nature.com/articles/s41586-019-1724-z
doi: 10.1038/s41586-019-1724-z
arxiv: null
cite: Vinyals, O., Babuschkin, I., Czarnecki, W. M., Mathieu, M., Dudzik, A., Chung, J., Choi, D. H., Powell, R., Ewalds, T., Georgiev, P., et al. (2019). Grandmaster level in StarCraft II using multi-agent reinforcement learning. Nature, 575(7782), 350–354.
topics:
- marl-emergence
added_by: dmarz/marl-emergence
accessed: '2026-10-03'
read_depth: abstract
relevance: 2
citations: 4546 (Semantic Scholar, 2026-10-03); 2739 (Crossref, 2026-10-03)
code: []
---

## Summary

AlphaStar plays the full game of StarCraft II using general-purpose learning: a multi-agent RL algorithm that uses human and agent game data within a diverse league of continually adapting strategies and counter-strategies represented by deep networks. Evaluated in online games against humans, it was rated Grandmaster for all three races and above 99.8% of officially ranked human players.

## Contribution

The most prominent demonstration of league (population) training to avoid strategy cycling in competitive MARL; an engineering analogue of the autocurricula argument of [[leibo-2019-autocurricula]].

## Key results

- Grandmaster rating for all three races; above 99.8% of ranked players (measured in online play, per abstract).

## Methods and models

Imitation pretraining on human replays, then league-based multi-agent RL with main agents and exploiters. Abstract-level read.

## Limitations and open questions

The "multi-agent" aspect is between strategies in a league, not many interacting embodied agents; extreme compute.

## Relevance to us

Low direct relevance to swarm dynamics; cite as context for population-based MARL. Related: [[jaderberg-2019-human]].
