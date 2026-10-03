---
id: hendrickx-2017-open
type: paper
title: "Open multi-agent systems: Gossiping with random arrivals and departures"
authors: [Julien M. Hendrickx, Samuel Martin]
year: 2017
venue: 2017 IEEE 56th Annual Conference on Decision and Control (CDC)
url: https://arxiv.org/abs/1709.05142
doi: 10.1109/cdc.2017.8263752
arxiv: '1709.05142'
cite: "Hendrickx, J. M., & Martin, S. (2017). Open multi-agent systems: Gossiping with random arrivals and departures. In 2017 IEEE 56th Annual Conference on Decision and Control (CDC) (pp. 763-768). IEEE."
topics: [sync-consensus]
added_by: dmarz/sync-consensus-audit
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "64 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Studies consensus in "open" multi-agent systems where agents join and leave while the algorithm runs, so the
state dimension changes and classical convergence is impossible. Agents perform pairwise gossip averaging;
departures and arrivals (new agents with i.i.d. random values of variance sigma^2) happen at random times. The
authors show that the expected mean-square and squared-mean of the states obey a two-dimensional (possibly
time-varying) linear system, and use it to compute the steady-state expected variance and convergence rates for
(i) fixed-size systems where each departing agent is immediately replaced and (ii) systems that grow without
bound.

## Contribution

One of the first formal treatments of agent churn in consensus, a gap in the classical closed-system results
([[olfati-saber-2004-consensus]], [[boyd-2006-randomized]], whose randomized gossip this extends). It replaces
"convergence" with steady-state descriptive statistics, the right notion when agents fail or are swapped out.

## Key results

- Theorem 5 (fixed size n with replacement): each event is a replacement with probability p or a gossip with
  probability 1 - p; the expected moments follow an affine recursion (eq. 13) with fixed point giving equilibrium
  expected variance EVar = sigma^2 * 2p(n - 1) / (p + 2n - 1) (eq. 14). p = 1 (no gossip) gives sigma^2 (1 - 1/n);
  p -> 0 gives 0.
- Convergence rate to the steady state is governed by the slower eigenvalue, linked to the rate of variance
  reduction (about 1 - 1/n per event without arrivals).
- Single simulated realisations are well approximated by the expected-moment predictions (Fig. 2).
- Theorem 8 (growing systems, no departures, arrival probability p_n per event): if p_n = p > 0 the expected
  variance tends to p sigma^2; if p_n -> 0 it tends to 0 (consensus), even if gossips per agent between arrivals
  vanish. With per-agent gossip rate fixed, a constant arrival rate gives consensus, while arrivals proportional
  to size (reproduction-like) leave a finite variance p sigma^2.
- Stated conclusion: openness can cause a significant loss of variance reduction compared with closed systems.

## Methods and models

Pairwise gossip x_i, x_j <- (x_i + x_j)/2 on a complete graph; Poisson-like event process choosing gossip,
departure-with-replacement, or arrival; moment closure is exact for these linear updates. Read: abstract,
introduction, problem set-up, Theorem 5 and the convergence-rate section from arXiv; proofs skimmed.

## Limitations and open questions

- Complete interaction graph and pairwise averaging only; no spatial or proximity network.
- Expected-value analysis; distributions of the state are not characterised.
- The authors flag algorithm design under churn (robustness, what the right target value is) as open.

## Relevance to us

Real swarms lose and gain robots (battery swaps, crashes, newcomers). This gives a quantitative baseline for
how much disagreement a consensus or sync protocol must tolerate at a given churn rate, and the right metrics
(steady-state variance, not convergence time). [[quinn-2025-decentralised]] observed newcomer drones pulling the
swarm's phase, a sync analogue of the same problem.
