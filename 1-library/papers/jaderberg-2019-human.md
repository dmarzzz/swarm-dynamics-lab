---
id: jaderberg-2019-human
type: paper
title: Human-level performance in 3D multiplayer games with population-based reinforcement learning
authors:
- Max Jaderberg
- Wojciech M. Czarnecki
- Iain Dunning
- Luke Marris
- Guy Lever
- Antonio Garcia Castañeda
- Charles Beattie
- Neil C. Rabinowitz
- Ari S. Morcos
- Avraham Ruderman
- Nicolas Sonnerat
- Tim Green
- Louise Deason
- Joel Z. Leibo
- David Silver
- Demis Hassabis
- Koray Kavukcuoglu
- Thore Graepel
year: 2019
venue: Science
url: https://arxiv.org/abs/1807.01281
doi: 10.1126/science.aau6249
arxiv: '1807.01281'
cite: Jaderberg, M., Czarnecki, W. M., Dunning, I., Marris, L., Lever, G., Castañeda, A. G., Beattie, C., Rabinowitz, N. C., Morcos, A. S., Ruderman, A., et al. (2019). Human-level performance in 3D multiplayer games with population-based reinforcement learning. Science, 364(6443), 859–865.
topics:
- marl-emergence
added_by: dmarz/marl-emergence
accessed: '2026-10-03'
read_depth: abstract
relevance: 2
citations: 831 (Semantic Scholar, 2026-10-03); 441 (Crossref, 2026-10-03)
code: []
---

## Summary

Agents reach human-level play in Quake III Arena Capture the Flag from pixels and game points alone. A population of independent RL agents trains concurrently in thousands of parallel team matches on randomly generated maps; each agent learns its own internal reward to complement the sparse win signal and uses a temporally hierarchical representation. Agents show human-like behaviours such as navigating, following and defending, and beat strong human players as teammates and opponents.

## Contribution

Landmark for emergent team coordination via population-based training and learned internal rewards; contrasted by [[baker-2020-emergent]], which needs neither.

## Key results

- Agents exceed strong human win rates in tournament evaluation (claimed in abstract).

## Methods and models

Population-based training, learned dense internal rewards, two-timescale recurrent architecture. Abstract-level read (arXiv version).

## Limitations and open questions

Massive compute; small teams (2 v 2).

## Relevance to us

Background on team-level emergence; low direct relevance to large swarms. Related: [[vinyals-2019-grandmaster]], [[leibo-2019-autocurricula]].
