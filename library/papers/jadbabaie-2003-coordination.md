---
id: jadbabaie-2003-coordination
type: paper
title: Coordination of groups of mobile autonomous agents using nearest neighbor rules
authors: [A. Jadbabaie, Jie Lin, A. S. Morse]
year: 2003
venue: IEEE Transactions on Automatic Control
url: https://people.mpi-inf.mpg.de/~mehlhorn/SeminarEvolvability/Jadbabaie.pdf
doi: 10.1109/tac.2003.812781
arxiv: null
cite: "Jadbabaie, A., Lin, J., & Morse, A. S. (2003). Coordination of groups of mobile autonomous agents using nearest neighbor rules. IEEE Transactions on Automatic Control, 48(6), 988-1001."
topics: [sync-consensus, collective-motion, swarm-robotics]
added_by: dmarz/sync-consensus
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "8459 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Gives the first rigorous explanation of why the noiseless Vicsek model aligns. Each agent's heading is replaced
by the average of its own and its neighbours' headings (neighbours = agents within radius r). Writing this as a
switched linear system theta(t+1) = F_sigma(t) theta(t), with F_p = (I + D_p)^(-1)(I + A_p) a stochastic matrix for
neighbour graph p, they prove all headings converge to a common value provided the agents are "linked together"
(the union of neighbour graphs is connected) across each of an infinite sequence of contiguous, bounded time
intervals. They extend the result to leader-following (followers converge to a fixed-heading leader) in
discrete and continuous time, and show the Vicsek system is stable yet admits no common quadratic Lyapunov
function.

## Contribution

This is the paper that pulled the Vicsek model from statistical physics into control theory and founded the
"consensus under switching topology" literature. The key move is to abstract away how the graph depends on
positions and to require only joint connectivity over bounded windows, which became the standard assumption
in [[ren-2005-consensus]], [[moreau-2005-stability]] and [[olfati-saber-2004-consensus]]. The convergence argument
reuses Wolfowitz's 1963 theorem on infinite products of ergodic (SIA) stochastic matrices, linking flocking to
Markov chain theory; [[cucker-2007-emergent]] later replaced the trajectory assumption with conditions on the
initial state only.

## Key results

- Theorem 1: if the neighbour graph is connected at every step, theta(t) converges to theta_ss times the all-ones vector.
- Theorem 2: the same holds if graphs are only jointly connected over contiguous bounded intervals; the bound
  must be uniform because Wolfowitz's theorem needs a finite matrix set. Whether non-contiguous intervals suffice
  was left open.
- Section 2.1: by semidefinite programming they found no common quadratic Lyapunov function for the F_p of all
  connected graphs on 10 vertices (checking graphs with 9 or 10 edges), so stability is not provable with a
  single quadratic Lyapunov function; they relate this to the joint spectral radius.
- Section 2.2: Vicsek's rule is the decentralised feedback u = -(I + D)^(-1) L theta with graph Laplacian L.
  The alternative u = -(1/g) L theta with g > n admits a common quadratic Lyapunov function but requires each agent
  to know an upper bound on group size.
- Theorem 4 (leader following, discrete time) and Theorem 5 (continuous time with dwell time tau_D > 0): followers
  converge to the leader's heading if linked to the leader over bounded intervals; Theorem 5 holds for any
  positive dwell time.

## Methods and models

Pure analysis, no experiments. Model: Vicsek heading update without noise, theta_i(t+1) = (theta_i + sum_{j in N_i}
theta_j)/(1 + n_i). Tools: graph Laplacians, stochastic and primitive matrices, Wolfowitz's theorem on ergodic
products, a matrix inequality (Lemma 2) bounding products of non-negative matrices with positive diagonals,
semidefinite programming for the Lyapunov counterexample. Read from the authors' revised preprint (December
2002) hosted at MPI Informatik; content matches the published abstract.

## Limitations and open questions

- Headings are averaged as real numbers in [0, 2 pi), not on the circle: averaging 0.01 and 2 pi - 0.01 gives pi.
  The authors note this; it means the result is really about linear consensus, not about the angular Vicsek
  model with its wrap-around.
- Noise is ignored, so the Vicsek order-disorder phase transition is not addressed; the authors suggest
  percolation on random geometric graphs as a route.
- Connectivity is assumed along the trajectory rather than derived from initial conditions; the feedback
  between motion and graph is not analysed.
- Undirected neighbour graphs only; [[ren-2005-consensus]] and [[moreau-2005-stability]] later handled directed
  graphs (spanning-tree conditions).

## Relevance to us

The canonical bridge between flocking models ([[olfati-saber-2006-flocking]], [[cucker-2007-emergent]],
[[vicsek-1995-novel]]) and consensus theory ([[olfati-saber-2007-consensus]], [[ren-2007-information]]). Any hackathon
experiment on alignment with intermittent or range-limited communication (drones losing links, robots with
short-range radios) starts from its joint-connectivity condition. The wrap-around caveat matters if we simulate
headings: use circular averages, as in Kuramoto-type models ([[sepulchre-2007-stabilization]]).
