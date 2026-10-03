---
id: van-dijk-2013-flipit
type: paper
title: 'FlipIt: The Game of "Stealthy Takeover"'
authors:
- Marten van Dijk
- Ari Juels
- Alina Oprea
- Ronald L. Rivest
year: 2013
venue: Journal of Cryptology, 26(4), 655-713
url: https://eprint.iacr.org/2012/103.pdf
doi: 10.1007/s00145-012-9134-5
arxiv: null
cite: 'van Dijk, M., Juels, A., Oprea, A., & Rivest, R. L. (2013). FlipIt: The Game of "Stealthy Takeover". Journal of Cryptology, 26(4), 655-713.'
topics:
- fork-merge-security
- sync-consensus
added_by: dmarz/fm
accessed: '2026-10-03'
read_depth: skim
relevance: 4
citations: 234 (Crossref, 2026-10-03)
code: []
---

## Summary

Two players compete for control of one resource (a key, password, machine) by paying to move at any time; neither learns who holds the resource until it moves. Payoff is fraction of time in control minus move costs. With renewal strategies, periodic play with random phase strongly dominates other renewal strategies. Against an adaptive attacker that learns the defender's last move time, a periodic defender does badly; an exponential (memoryless) defender forces the attacker back to periodic play. A defender that moves fast enough relative to its cost can make the attacker drop out. I read the abstract, introduction and results table of the 2012 ePrint version.

## Contribution

Models repeated, undetected total compromise and periodic reset, with applications named by the authors including key rotation, VM refresh and cloud auditing.

## Key results

- Periodic-with-random-phase strongly dominates renewal strategies of fixed rate (Theorem 4).
- Exponential defender makes periodic play strongly dominant for a last-move attacker (Theorem 6).
- Fast, cheap defender moves can drive the attacker out of the game.
- Lesson stated by the authors: design for repeated total compromise.

## Methods and models

Continuous-time two-player game, renewal processes, dominance analysis, simulation.

## Limitations and open questions

One resource; general adaptive strategies left open.

## Relevance to us

- Q1: the timing analogue of hiding. If merges or resets of children happen on a predictable schedule, an attacker that learns the last reset time can corrupt right after it; memoryless (exponential) reset or merge timing removes that advantage.
- Q2 lead-in: [[laszka-2014-flipthem]] and [[leslie-2015-threshold]] extend this to n resources and a k threshold.
- Q3: frames the corrupted child as a stealthy takeover the parent only discovers when it moves (re-forks or audits).
Related: [[damera-2026-stability]], [[cho-2020-toward]].
